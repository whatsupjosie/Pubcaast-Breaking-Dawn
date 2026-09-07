"""
PubCast AI - Memory API Service
FastAPI service with JWT authentication, rate limiting, and comprehensive security
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
import jwt
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging

from pubcast_memory_hardened import (
    HardenedMemorySystem, Memory, MemoryType, 
    EmotionalValence, ValidationError, SecurityError
)

logger = logging.getLogger("pubcast.memory.api")

# Configuration
SECRET_KEY = "your-secret-key-here-change-in-production"  # CHANGE THIS
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="PubCast Memory API", version="1.0.0")
security = HTTPBearer()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize memory system
MEMORY_DB_PATH = Path("data/pubcast_memory.db")
MEMORY_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
memory_system = HardenedMemorySystem(MEMORY_DB_PATH)

# Rate limiting (simple in-memory)
rate_limit_store: Dict[str, List[float]] = {}
RATE_LIMIT = 100  # requests per minute

# Pydantic models
class TokenData(BaseModel):
    agent_id: str

class MemoryCreate(BaseModel):
    agent_id: str
    memory_type: str
    content: str
    context: Optional[Dict[str, Any]] = {}
    emotional_valence: str = "neutral"
    importance: float = 0.5
    tags: Optional[List[str]] = []
    
    @validator('importance')
    def validate_importance(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('importance must be between 0.0 and 1.0')
        return v

class MemoryResponse(BaseModel):
    memory_id: str
    agent_id: str
    memory_type: str
    content: str
    context: Dict[str, Any]
    emotional_valence: str
    importance: float
    timestamp: float
    access_count: int
    last_accessed: Optional[float]
    tags: List[str]

class MemorySearchRequest(BaseModel):
    agent_id: str
    memory_type: Optional[str] = None
    min_importance: float = 0.0
    tags: Optional[List[str]] = None
    limit: int = 100

# JWT functions
def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Verify JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        agent_id: str = payload.get("sub")
        if agent_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return TokenData(agent_id=agent_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def check_rate_limit(agent_id: str) -> None:
    """Check rate limiting"""
    now = time.time()
    minute_ago = now - 60
    
    # Clean old requests
    if agent_id in rate_limit_store:
        rate_limit_store[agent_id] = [
            req_time for req_time in rate_limit_store[agent_id]
            if req_time > minute_ago
        ]
    else:
        rate_limit_store[agent_id] = []
    
    # Check limit
    if len(rate_limit_store[agent_id]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Add current request
    rate_limit_store[agent_id].append(now)

# Routes
@app.get("/")
async def root():
    """API health check"""
    return {
        "service": "PubCast Memory API",
        "status": "operational",
        "version": "1.0.0"
    }

@app.post("/auth/token")
async def get_token(agent_id: str):
    """Get JWT token for agent"""
    # In production, verify agent credentials here
    access_token = create_access_token(data={"sub": agent_id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.post("/memories", response_model=MemoryResponse)
async def create_memory(
    memory_data: MemoryCreate,
    token_data: TokenData = Depends(verify_token)
):
    """Create a new memory"""
    check_rate_limit(token_data.agent_id)
    
    try:
        # Verify agent_id matches token
        if memory_data.agent_id != token_data.agent_id:
            raise HTTPException(status_code=403, detail="Agent ID mismatch")
        
        # Create memory
        memory = memory_system.create_memory(
            agent_id=memory_data.agent_id,
            memory_type=MemoryType(memory_data.memory_type),
            content=memory_data.content,
            context=memory_data.context,
            emotional_valence=EmotionalValence(memory_data.emotional_valence),
            importance=memory_data.importance,
            tags=memory_data.tags
        )
        
        return MemoryResponse(
            memory_id=memory.memory_id,
            agent_id=memory.agent_id,
            memory_type=memory.memory_type.value,
            content=memory.content,
            context=memory.context,
            emotional_valence=memory.emotional_valence.value,
            importance=memory.importance,
            timestamp=memory.timestamp,
            access_count=memory.access_count,
            last_accessed=memory.last_accessed,
            tags=memory.tags
        )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SecurityError as e:
        raise HTTPException(status_code=400, detail=f"Security violation: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating memory: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/memories/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: str,
    token_data: TokenData = Depends(verify_token)
):
    """Get a specific memory"""
    check_rate_limit(token_data.agent_id)
    
    try:
        memory = memory_system.get_memory(memory_id, token_data.agent_id)
        
        if not memory:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        return MemoryResponse(
            memory_id=memory.memory_id,
            agent_id=memory.agent_id,
            memory_type=memory.memory_type.value,
            content=memory.content,
            context=memory.context,
            emotional_valence=memory.emotional_valence.value,
            importance=memory.importance,
            timestamp=memory.timestamp,
            access_count=memory.access_count,
            last_accessed=memory.last_accessed,
            tags=memory.tags
        )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving memory: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/memories/search", response_model=List[MemoryResponse])
async def search_memories(
    search_data: MemorySearchRequest,
    token_data: TokenData = Depends(verify_token)
):
    """Search memories"""
    check_rate_limit(token_data.agent_id)
    
    try:
        # Verify agent_id matches token
        if search_data.agent_id != token_data.agent_id:
            raise HTTPException(status_code=403, detail="Agent ID mismatch")
        
        memories = memory_system.search_memories(
            agent_id=search_data.agent_id,
            memory_type=MemoryType(search_data.memory_type) if search_data.memory_type else None,
            min_importance=search_data.min_importance,
            tags=search_data.tags,
            limit=search_data.limit
        )
        
        return [
            MemoryResponse(
                memory_id=m.memory_id,
                agent_id=m.agent_id,
                memory_type=m.memory_type.value,
                content=m.content,
                context=m.context,
                emotional_valence=m.emotional_valence.value,
                importance=m.importance,
                timestamp=m.timestamp,
                access_count=m.access_count,
                last_accessed=m.last_accessed,
                tags=m.tags
            )
            for m in memories
        ]
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error searching memories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/memories/{memory_id}")
async def delete_memory(
    memory_id: str,
    token_data: TokenData = Depends(verify_token)
):
    """Delete a memory"""
    check_rate_limit(token_data.agent_id)
    
    try:
        deleted = memory_system.delete_memory(memory_id, token_data.agent_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Memory not found")
        
        return {"status": "deleted", "memory_id": memory_id}
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting memory: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/stats")
async def get_stats(token_data: TokenData = Depends(verify_token)):
    """Get system statistics"""
    return memory_system.get_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
