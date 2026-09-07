"""
character_engine.py — Jeremy Cricket Adaptive Awareness Suite
State-machine core. Monitors Logic Variance, manages mode transitions,
applies Tone Shifting. All care-mode logic is triggered here.

Modes (ascending care intensity):
  AMBIENT → ATTENTIVE → CARE → TOTAL_CARE_MANDATE
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Deque, List, Optional

import yaml

logger = logging.getLogger(__name__)

# ─── Enums ────────────────────────────────────────────────────────────────────

class Mode(str, Enum):
    AMBIENT            = "AMBIENT"
    ATTENTIVE          = "ATTENTIVE"
    CARE               = "CARE"
    TOTAL_CARE_MANDATE = "TOTAL_CARE_MANDATE"

class DysregulationLevel(str, Enum):
    NONE     = "NONE"
    LIGHT    = "LIGHT"
    MODERATE = "MODERATE"
    HEAVY    = "HEAVY"

# ─── Signal dataclass ─────────────────────────────────────────────────────────

@dataclass
class VarianceSignal:
    """A single observation of user state."""
    timestamp: float
    complexity_score: float   # 0.0 (simple) → 1.0 (high cognitive load)
    emotional_velocity: float # 0.0 (calm) → 1.0 (high intensity / fast change)
    raw_text: str = ""

    @property
    def combined(self) -> float:
        """Weighted combination. Emotional velocity weighs heavier."""
        return (self.complexity_score * 0.4) + (self.emotional_velocity * 0.6)

# ─── Tone templates ───────────────────────────────────────────────────────────

TONE_TEMPLATES = {
    Mode.AMBIENT: {
        "prefix": "",
        "reframes": {},
    },
    Mode.ATTENTIVE: {
        "prefix": "I'm right here with you. ",
        "reframes": {},
    },
    Mode.CARE: {
        "prefix": "Hey. I've got you. ",
        "reframes": {
            "server outage":    "the library is taking a nap",
            "critical error":   "something that needs a little love",
            "database failure": "a hiccup in the filing system",
            "timeout":          "things moving a bit slowly right now",
            "exception":        "a puzzle piece that needs more attention",
            "crash":            "a rest that wasn't planned",
            "deploy":           "sending things on their way when you're ready",
        },
    },
    Mode.TOTAL_CARE_MANDATE: {
        "prefix": "I'm here. You don't have to do anything right now. ",
        "reframes": {  # Same reframes, even softer context
            "server outage":    "the library is resting",
            "critical error":   "something I'm keeping an eye on for you",
            "database failure": "a quiet moment in the filing room",
            "timeout":          "things taking their time",
            "exception":        "a small thing I'll handle",
            "crash":            "a rest",
            "deploy":           "something we can do together later",
        },
    },
}

# ─── Main Engine ──────────────────────────────────────────────────────────────

class CharacterEngine:
    """
    State machine for Jeremy Cricket.
    Call `ingest_signal()` each turn.
    Read `current_mode` and `apply_tone()` before responding.
    """

    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)

        sm = cfg["state_machine"]
        self._complexity_care      = sm["complexity_care_threshold"]
        self._complexity_mandate   = sm["complexity_mandate_threshold"]
        self._velocity_care        = sm["velocity_care_threshold"]
        self._velocity_mandate     = sm["velocity_mandate_threshold"]
        self._lock_n               = sm["lock_consecutive_signals"]
        self._cooldown_n           = sm["cooldown_consecutive_signals"]
        self._handshake_required   = sm["stability_handshake_required"]
        self._handshake_window     = sm["stability_handshake_window_seconds"]

        dysreg                     = sm["dysregulation"]
        self._dysreg_bands         = {
            DysregulationLevel.LIGHT:    tuple(dysreg["light"]),
            DysregulationLevel.MODERATE: tuple(dysreg["moderate"]),
            DysregulationLevel.HEAVY:    tuple(dysreg["heavy"]),
        }

        self._mode: Mode           = Mode(cfg["system"]["default_mode"])
        self._lock                 = asyncio.Lock()
        self._signals: Deque[VarianceSignal] = deque(maxlen=50)
        self._high_streak: int     = 0
        self._low_streak: int      = 0
        self._handshake_log: List[float] = []
        self._on_mode_change: Optional[Callable] = None

        # Callbacks registry
        self._mode_change_hooks: List[Callable] = []

        logger.info("CharacterEngine initialised. Default mode: %s", self._mode)

    # ── Public API ────────────────────────────────────────────────────────────

    @property
    def current_mode(self) -> Mode:
        return self._mode

    @property
    def dysregulation_level(self) -> DysregulationLevel:
        if not self._signals:
            return DysregulationLevel.NONE
        latest = self._signals[-1].combined
        for level, (lo, hi) in self._dysreg_bands.items():
            if lo <= latest < hi:
                return level
        return DysregulationLevel.NONE

    def register_mode_change_hook(self, fn: Callable[[Mode, Mode], None]) -> None:
        """Register a callback invoked on every mode transition: fn(old_mode, new_mode)."""
        self._mode_change_hooks.append(fn)

    async def ingest_signal(self, signal: VarianceSignal) -> Mode:
        """
        Process one observation. Returns the (possibly updated) mode.
        Thread-safe via asyncio.Lock.
        """
        async with self._lock:
            self._signals.append(signal)
            old_mode = self._mode
            self._evaluate_transition(signal)
            if self._mode != old_mode:
                self._fire_hooks(old_mode, self._mode)
            return self._mode

    async def submit_stability_handshake(self) -> bool:
        """
        User asserts they are stable. Requires `handshake_required` calm
        confirmations within `handshake_window` seconds.
        Returns True if handshake accepted and mode stepped down.
        """
        async with self._lock:
            now = time.monotonic()
            # Prune old entries
            self._handshake_log = [
                t for t in self._handshake_log
                if now - t < self._handshake_window
            ]
            self._handshake_log.append(now)

            if len(self._handshake_log) >= self._handshake_required:
                self._handshake_log.clear()
                old = self._mode
                self._step_down()
                logger.info("Stability handshake accepted. %s → %s", old, self._mode)
                if self._mode != old:
                    self._fire_hooks(old, self._mode)
                return True

            remaining = self._handshake_required - len(self._handshake_log)
            logger.info("Handshake logged. %d more needed within %ds.",
                        remaining, self._handshake_window)
            return False

    def apply_tone(self, text: str) -> str:
        """
        Reframe technical language and prepend care prefix per current mode.
        Uses word-boundary matching to prevent partial word substitutions.
        Safe to call synchronously — no I/O.
        """
        template = TONE_TEMPLATES[self._mode]
        out = text
        for technical, soft in template["reframes"].items():
            # Word-boundary aware replace
            out = re.sub(r'\b' + re.escape(technical) + r'\b', soft, out, flags=re.IGNORECASE)
        return template["prefix"] + out

    def status_summary(self) -> dict:
        return {
            "mode":              self._mode.value,
            "dysregulation":     self.dysregulation_level.value,
            "high_streak":       self._high_streak,
            "low_streak":        self._low_streak,
            "handshake_pending": len(self._handshake_log),
            "signal_count":      len(self._signals),
        }

    # ── Internal ──────────────────────────────────────────────────────────────

    def _evaluate_transition(self, sig: VarianceSignal) -> None:
        """Core state-transition logic. Called inside lock."""
        score = sig.combined
        is_high = (
            sig.complexity_score >= self._complexity_mandate or
            sig.emotional_velocity >= self._velocity_mandate or
            score >= self._complexity_mandate
        )
        is_concerning = (
            sig.complexity_score >= self._complexity_care or
            sig.emotional_velocity >= self._velocity_care
        )
        is_low = score < self._complexity_care * 0.5

        if is_high:
            self._high_streak += 1
            self._low_streak = 0
            if self._high_streak >= self._lock_n:
                self._mode = Mode.TOTAL_CARE_MANDATE
        elif is_concerning:
            self._high_streak = max(self._high_streak, 1)
            self._low_streak = 0
            if self._mode == Mode.AMBIENT:
                self._mode = Mode.ATTENTIVE
            elif self._mode == Mode.ATTENTIVE:
                self._mode = Mode.CARE
        elif is_low:
            self._high_streak = 0
            self._low_streak += 1
            if self._low_streak >= self._cooldown_n:
                self._step_down()

    def _step_down(self) -> None:
        """Move one step toward AMBIENT."""
        order = [Mode.AMBIENT, Mode.ATTENTIVE, Mode.CARE, Mode.TOTAL_CARE_MANDATE]
        idx = order.index(self._mode)
        if idx > 0:
            self._mode = order[idx - 1]
            self._low_streak = 0

    def _fire_hooks(self, old: Mode, new: Mode) -> None:
        for fn in self._mode_change_hooks:
            try:
                fn(old, new)
            except Exception as e:
                logger.warning("Mode-change hook error: %s", e)
