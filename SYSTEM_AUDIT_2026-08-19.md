# PUBCAST SYSTEM AUDIT — 2026-08-19
## Every system. Honest state. What to do next.

Generated from actual running boot log + module tree inspection.
19 startup steps confirmed firing. Cross-referenced against 77,000 lines of modules.

---

## LEGEND
- ✅ VERIFIED   — boots, responds, independently tested tonight
- 🟡 LOADED     — mounts on startup, not yet independently tested
- 🔌 WIRED      — imported and instantiated but needs external dependency
- 📦 ORPHAN     — built, not imported in main.py, not in the startup chain
- ❌ BROKEN     — confirmed error on startup
- ⏸  DEGRADED   — running in fallback mode, reason known

---

## SERVICES (the three-service stack)

| Service       | Port | State     | Notes |
|---------------|------|-----------|-------|
| PubCast       | 8000 | ✅        | 19 steps, boots in 0.1s |
| PubPartner    | 8001 | ✅        | Resident node, CORS patched, sync verified |
| 2i-backend    | 8787 | ✅        | PubPartner wired, Anthropic key missing |

---

## STARTUP STEPS — what actually loads

### Step 1 — Hub
**State: ✅ VERIFIED**
Core message bus. All other systems speak through it.

### Step 2 — RoomManager (14 rooms)
**State: ✅ VERIFIED**
All 14 rooms accessible. 11 verified as iframe-able into Foresight trays.

### Step 2b — PerformanceManager
**State: 🟡 LOADED**
Medium profile active. Not load-tested.

### Step 2c — ChoreographyController (30Hz)
**State: 🟡 LOADED**
Animation timing bus. Feeds avatar/character systems. Needs renderer to matter.

### Step 2d — LightingEngine (36 presets)
**State: 🟡 LOADED** — `lighting_engine.py` (1049 lines)
36 presets defined. No renderer target yet. Will matter when C++ engine connects.

### Step 3 — Inference (Studio offline | Architect ready)
**State: ⏸ DEGRADED**
- Studio (ministral-pubcast:3b via Ollama): OFFLINE — Ollama not running
- Architect (gemma4-compute-q5:e2b): reports AVAILABLE but also Ollama-backed
- **Real fix on Zoidberg:** start Ollama, pull the two models
- Anthropic path exists (`claude.py` in not_yet_integrated) — not wired yet

### Step 3a — Auth + UserDB
**State: 🟡 LOADED**
Tables ready. Owner account not auto-created — needs `PUBCAST_OWNER_PASSWORD`.
JWT on insecure default — needs `PUBCAST_JWT_SECRET`.

### Step 3b — Alex Core + Alex/Jeremy Bridge
**State: 🟡 LOADED** — `alex_core.py` (1059 lines), `alex_memory.py` (1363 lines)
3 memories loaded from disk. Snapshot restored. Prime Directive active.
Alex initialized for "default" user. Has not spoken — no live LLM backend.

### Step 4 — CricketKeeper (Jeremy Cricket)
**State: 🟡 LOADED** — `jeremy_cricket.py` (577 lines)
0 characters pre-loaded. Ready to receive character configs.
The April handoff's care engine (character_engine.py upload) still unintegrated.

### Step 5 — BotManager (5 bots)
**State: ✅ VERIFIED** (fixed tonight)
Pete, RePete, Sir Purfluous, smoke-bot, Sir Purfluous (Waiting Room).
Was 4 — fixed `sir_purfluous_waiting_room.json` tonight.

### Step 5b — Sir Purfluous (module)
**State: 🟡 LOADED** — `purfluous.py` (559 lines)
Character module mounted separately from BotManager entry. Redundancy worth checking.

### Step 5b — IRM Engine Monitor
**State: ⏸ DEGRADED**
Running in emergency mode (bridge on Path C). Will improve when C++ engine connects.
Now reads real `engine_stress` from bridge when V3 SHM is live.

### Step 5b — AvatarPerformerManager
**State: 🔌 WIRED — needs renderer**
Ready but not started. Waiting for a renderer connection.
`avatar_performer.py` (998 lines) + `avatar_system_raw.py` (773 lines) both real.

### Step 5b — CredentialStore
**State: 🟡 LOADED**
BYOK key storage ready. No credentials stored yet.

### Step 6 — Cameras (6) + Recording (4 profiles)
**State: 🟡 LOADED** — `recording.py` (714 lines)
FFmpeg confirmed at /usr/bin/ffmpeg. 6 cameras registered. 4 recording profiles.
`cameras_advanced.py` (1037 lines) — ORPHAN, not imported. Has broadcast features.
Recording pipeline exists but untested end-to-end.

### Step 7 — Governance (bans, freeze, consent, waiting room)
**State: 🟡 LOADED** — `governance.py` (619 lines)
Auto-approve mode active (dev setting). Consent, bans, freeze all wired.

### Step 7b — PubWorld Hotspot API
**State: 🟡 LOADED**
0 rooms with hotspot data. Infrastructure ready, no content mapped yet.

### Step 7c/d/e/f/g/h — Production subsystems
**State: 🟡 LOADED**
Timeline automation, airlock, hotspot handlers, recording export, audio devices, 
character/story/memory routes — all mounted, none tested independently.
0 persisted character memories on this instance.

### Step 8 — BYOK
**State: 🟡 LOADED** — `byok_manager.py` (525 lines)
User-supplied API keys enabled. No keys stored. This is the path to give users
their own Anthropic key for bot inference — important for the real deployment.

### Step 9 — ThinkingContext (5 characters)
**State: 🟡 LOADED**
5 character slots mounted. Pete, RePete, Sir Purfluous, Jeremy, default (Alex).

### Step 10 — Ethereal Avatars (57 joints, 7 colors)
**State: 🔌 WIRED — needs renderer**
Skeleton fully defined, 7 color slots, ready to pose.
`facial_performance.py` (576 lines) in simulation mode (no DeepFace/MediaPipe).
`prosody_engine.py` (554 lines) loaded — timing engine for speech-driven animation.
Neither has a render target until C++ engine connects.

### Step 10b — Avatar Studio Bridge
**State: 🔌 WIRED**
Bridge between avatar state and studio output. Needs renderer.

### Step 11 — EVO Protocol (Switchblade + VDI + E-Pete)
**State: 🟡 LOADED** — real systems, all three active
- `epete.py` (852 lines) — concurrency cap: 1 (Zoidberg spec)
- `evo_integration.py` — EPete + PeteCharacter wired, alert handler registered
- Switchblade governor reads VDI, outputs priority vectors
- E-Pete feeds camera boxer (new tonight) when stress rises
- **Gap:** E-Pete still reads render_load from internal estimate, not bridge stress
  for the main dispatch loop. Camera boxer reads it correctly. Should unify.

### Step 12 — Vault
**State: 🟡 LOADED** — `vault_engine_hardened.py` (768 lines)
OS-level protection active. `key_recovery.py` (565 lines) — ORPHAN.
Vault works; recovery path not mounted.

### Step 12b — Doctor
**State: 🟡 LOADED** — `doctor.py` (615 lines)
Self-diagnostic system. Not tested.

### Step 13 — PubWorld Router (/pubworld/ws)
**State: 🟡 LOADED**
WebSocket live broadcast ready. Nothing broadcasting yet.

### Step 14 — Surface Manager
**State: 🟡 LOADED**
Manages the stage surface/environment. No content set.

### Step 15 — ConversationOrchestrator
**State: 🟡 LOADED**
Coordinates conversation flow. Not tested with live inference.

### Step 16 — Voxel Asset Manager (5 assets)
**State: 🟡 LOADED** — `voxel_asset_manager.py` (758 lines)
5 assets catalogued. Library loaded. No renderer to place them in.

### Step 17 — Voxel Bridge
**State: ⏸ DEGRADED (Path C)**
Path A (Windows SHM): wired tonight — will work on Zoidberg with C++ engine
Path B (TCP): no TCP server in C++ engine — will always fail
Path C (filesystem): currently active fallback

### Step 17b — Twin Engine Service ✅ NEW TONIGHT
**State: ✅ VERIFIED**
Mounted, 4 cameras registered, `/api/twin/status` live.
Camera cut via API tested and working.
Mode: degraded → will be `ready` on Zoidberg with engine running.

### Step 17c — Camera Boxer ✅ NEW TONIGHT
**State: ✅ VERIFIED**
T1≥65% T2≥80% T3≥92%. Sacrifice order: overhead→closeup→wide. Main protected.
Audio always protected. `/api/boxer/status` and `/api/boxer/override` both live.
Override tested. Auto mode tested.

### Step 18 — Studio Control
**State: 🟡 LOADED** — `studio_control.py` (599 lines)
Preflight + audio matrix active. Not run through a real session.

### Step 18a — Voxel Studio Integration
**State: 🟡 LOADED**
Bridge between voxel world and studio control. Not tested with live content.

### Step 19 — Unity Bridge
**State: 🔌 WIRED — needs Unity**
WebSocket endpoint at /unity/ws. No Unity instance present.

---

## ORPHANED MODULES — built, not in the startup chain

These exist, have real code, and are not connected to anything running.
Not bugs — just future work waiting for its turn.

| Module | Lines | What it is |
|--------|-------|------------|
| `evidence_layer.py` | 1356 | Interpretive layer between VDI signals and memory |
| `response_execution_layer.py` | 1222 | Production response & conduct system |
| `mocap_precision.py` | 1158 | High-precision webcam motion capture v2.0 |
| `theory_graph.py` | 1056 | Theory graph, meta-theory engine, presence mode |
| `contradiction_engine.py` | 683 | Contradiction memory & instability detection |
| `pubcast_vision_integration.py` | 625 | Camera vision integration with PubCast infra |
| `cameras_advanced.py` | 1037 | Advanced camera management, broadcast features |
| `pete_avatar.py` | 1039 | Pete's avatar — dual-rig, reskinnable mesh |
| `room_conductor.py` | 802 | Room flow and session orchestration |
| `llm_orchestrator.py` | 812 | Dual-mind LLM routing (Studio + Architect) |
| `llm_framework.py` | 787 | Universal LLM framework |
| `littlemode_protocol.py` | 577 | Caregiving/safety protocol v2.0 |
| `key_recovery.py` | 565 | Vault key backup and recovery |
| `wired/unified_runtime_boot.py` | 569 | Alternative unified boot sequence |
| `wired/pubcast_runtime.py` | 546 | Alternative runtime entry point |

---

## CROSS-SERVICE STATUS

| Link | State | Notes |
|------|-------|-------|
| Foresight → PubCast rooms | ✅ | 11 rooms iframe-able, tested |
| 2i → PubPartner sync | ✅ | Manuscript commit verified x3 tonight |
| PubPartner resident ↔ portable | ✅ | Sync verified |
| PubCast → PubPartner chat | ✅ | Alex routing, Jeremy whisper active |
| PubCast → 2i | ❓ | Direction untested (PubCast pushing to 2i) |
| PubCast → C++ engine | ⏸ | Wired, waiting for Zoidberg + engine_host.exe |
| Camera boxer → IRM | 🟡 | Camera boxer running; full IRM integration pending |

---

## PRIORITY ORDER FOR NEXT SESSIONS

**Immediate (enables everything else):**
1. Zoidberg: Ollama up + models pulled → inference comes alive across the whole stack
2. Zoidberg: engine_host.exe compiled → bridge goes Path A, avatars have a render target
3. `PUBCAST_OWNER_PASSWORD` + `PUBCAST_JWT_SECRET` → first real user session possible

**Next layer (now that ground is stable):**
4. `llm_orchestrator.py` wired into Step 3 → proper dual-mind routing replaces current
5. `cameras_advanced.py` mounted → broadcast camera features available
6. `pete_avatar.py` mounted → Pete has a face
7. `room_conductor.py` mounted → sessions have orchestrated flow
8. Jeremy Cricket care engine (`character_engine.py` upload) → give it its own filename
   and wire it in, with the input scorer it still needs

**When renderer is live:**
9. `facial_performance.py` out of simulation mode → real face tracking
10. `prosody_engine.py` feeding rendered avatars → voice-driven performance
11. `evidence_layer.py` + `theory_graph.py` → full interpretive memory stack
12. `contradiction_engine.py` → memory coherence checking

**Later:**
13. `littlemode_protocol.py` — caregiving system
14. `key_recovery.py` → vault recovery path
15. Google Docs, GLB/OBJ/FBX viewers, native .blend pipeline

---

## WHAT A SINGLE SESSION COULD CLOSE

Any one of these is a full, completable session:
- Wire `llm_orchestrator.py` into Step 3 — dual-mind routing becomes real
- Wire `cameras_advanced.py` — broadcast camera features mount
- Wire `room_conductor.py` — sessions get orchestrated flow
- Wire `pete_avatar.py` — Pete gets a face (no renderer needed for the rig data)
- Write the `score_complexity`/`score_velocity` input scorer Jeremy Cricket needs
- Wire `claude.py` as an adapter option for any bot

Each of these is a bounded piece of work with a clear done state.
No orphan on this list is a redesign — they're all built systems waiting to be mounted.
