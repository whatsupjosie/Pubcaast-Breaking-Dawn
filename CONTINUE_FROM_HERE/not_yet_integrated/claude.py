"""
adapters/claude.py — UAI Claude Adapter
Wraps Anthropic's Messages API.
"""

from __future__ import annotations

import logging
from typing import Dict, List

import anthropic

from .base import BaseAdapter

logger = logging.getLogger("uai.adapter.claude")


class ClaudeAdapter(BaseAdapter):

    def __init__(self, api_key: str, cfg: Dict):
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        engine_cfg   = cfg.get("engines", {}).get("claude", {})
        self._model  = engine_cfg.get("model", "claude-opus-4-5")
        self._max_tokens = engine_cfg.get("max_tokens", 2048)
        logger.info("ClaudeAdapter using model: %s", self._model)

    async def complete(
        self,
        message: str,
        history: List[Dict],
        system_prompt: str = "",
    ) -> str:
        messages = self._format_history(history)
        messages.append({"role": "user", "content": message})

        kwargs = {
            "model":      self._model,
            "max_tokens": self._max_tokens,
            "messages":   messages,
        }
        if system_prompt.strip():
            kwargs["system"] = system_prompt

        response = await self._client.messages.create(**kwargs)
        return response.content[0].text
