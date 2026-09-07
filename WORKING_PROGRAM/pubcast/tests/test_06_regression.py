"""
test_06_regression.py — Regression tests for known bugs
═════════════════════════════════════════════════════════
Each test here documents a specific bug that was found and fixed.
If someone re-introduces the bug, the test catches it before it ships.

Bug registry:
  REG-001  /ws/unity and /ws/studio shadowed by /ws/{room} catch-all
  REG-002  lighting_apply calls hub.broadcast_system_event without null guard
  REG-003  _chat_callback fires bot_mgr for __purfluous__ user_id (potential loop)
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MAIN_PY = ROOT / "main.py"


# ─────────────────────────────────────────────────────────────────────────────
# REG-001: WebSocket route shadowing
# ─────────────────────────────────────────────────────────────────────────────

def test_reg001_ws_unity_not_shadowed_by_ws_room(raw_app):
    """REG-001: /ws/unity must be registered before /ws/{room} in the route list.

    SYMPTOM: Unity Bridge WebSocket appeared to connect but silently failed —
    Hub returned {"type":"error"} for all Unity protocol messages.
    ROOT CAUSE: /ws/{room} registered before /ws/unity. Starlette first-match wins.
    FIX: Moved /ws/unity and /ws/studio before /ws/{room} in main.py.
    """
    from starlette.routing import WebSocketRoute
    ws_routes = [r for r in raw_app.routes if isinstance(r, WebSocketRoute)]
    paths = [r.path for r in ws_routes]

    assert "/ws/unity" in paths,   "REG-001: /ws/unity not registered"
    assert "/ws/{room}" in paths,  "REG-001: /ws/{room} not registered"

    unity_pos    = paths.index("/ws/unity")
    catchall_pos = paths.index("/ws/{room}")
    assert unity_pos < catchall_pos, (
        f"REG-001 REGRESSION: /ws/unity (pos {unity_pos}) comes after "
        f"/ws/{{room}} (pos {catchall_pos}). Unity Bridge is broken."
    )


def test_reg001_ws_studio_not_shadowed_by_ws_room(raw_app):
    """REG-001: /ws/studio must be registered before /ws/{room}."""
    from starlette.routing import WebSocketRoute
    ws_routes = [r for r in raw_app.routes if isinstance(r, WebSocketRoute)]
    paths = [r.path for r in ws_routes]

    assert "/ws/studio" in paths,  "REG-001: /ws/studio not registered"
    studio_pos   = paths.index("/ws/studio")
    catchall_pos = paths.index("/ws/{room}")
    assert studio_pos < catchall_pos, (
        f"REG-001 REGRESSION: /ws/studio (pos {studio_pos}) comes after "
        f"/ws/{{room}} (pos {catchall_pos}). Studio Control Room WS is broken."
    )


# ─────────────────────────────────────────────────────────────────────────────
# REG-002: Missing null guard on hub in lighting_apply (static AST check)
# ─────────────────────────────────────────────────────────────────────────────

def test_reg002_lighting_apply_has_hub_null_guard():
    """REG-002: lighting_apply must check `if hub is not None` before calling
    hub.broadcast_system_event().

    SYMPTOM: Calling /api/lighting/apply/{preset_id} during tests or before
    lifespan completes raised AttributeError: 'NoneType' has no attribute
    'broadcast_system_event'.
    FIX: Added `if hub is not None:` guard around the broadcast call.
    """
    source = MAIN_PY.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # Find the lighting_apply function
    lighting_fn = None
    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "lighting_apply":
            lighting_fn = node
            break

    assert lighting_fn is not None, "lighting_apply function not found in main.py"

    # Check that the hub.broadcast_system_event call is inside an if-hub guard
    # We do this by looking for an If node that tests `hub is not None` or `hub`
    # and contains the broadcast call
    hub_broadcast_guarded = False
    for node in ast.walk(lighting_fn):
        if not isinstance(node, ast.If):
            continue
        # Check the test condition references 'hub'
        condition_src = ast.unparse(node.test) if hasattr(ast, "unparse") else ""
        if "hub" not in condition_src:
            continue
        # Check the body contains broadcast_system_event
        body_src = ast.unparse(node) if hasattr(ast, "unparse") else ""
        if "broadcast_system_event" in body_src:
            hub_broadcast_guarded = True
            break

    assert hub_broadcast_guarded, (
        "REG-002 REGRESSION: lighting_apply calls hub.broadcast_system_event "
        "without a null guard. This will raise AttributeError when hub is None."
    )


# ─────────────────────────────────────────────────────────────────────────────
# REG-003: Purfluous / bot feedback loop guard
# ─────────────────────────────────────────────────────────────────────────────

def test_reg003_chat_callback_guards_purfluous_user():
    """REG-003: _chat_callback must not call bot_mgr for __purfluous__ messages.

    SYMPTOM (potential): Purfluous posts as user_id='__purfluous__'. If bot_mgr
    responds to its own nudges, bots would loop indefinitely.
    FIX: `if bot_mgr is not None and user_id != '__purfluous__':` guard in
    _chat_callback.

    This test checks the source of main.py statically.
    """
    source = MAIN_PY.read_text(encoding="utf-8")
    # The guard must be present somewhere near the bot_mgr.on_chat_message call
    assert "__purfluous__" in source, \
        "REG-003: __purfluous__ sentinel not found in main.py"
    # Check it's used in a conditional context near on_chat_message
    lines = source.splitlines()
    found_guard = False
    for i, line in enumerate(lines):
        if "__purfluous__" in line:
            # Look in a window around this line for on_chat_message
            window = "\n".join(lines[max(0, i-3):i+5])
            if "on_chat_message" in window or "bot_mgr" in window:
                found_guard = True
                break
    assert found_guard, (
        "REG-003 REGRESSION: __purfluous__ guard not found near bot_mgr call. "
        "Purfluous nudges may trigger bot echo loops."
    )


# ─────────────────────────────────────────────────────────────────────────────
# Additional regression: bot self-reply guard in BotManager
# ─────────────────────────────────────────────────────────────────────────────

def test_reg003b_bot_manager_has_self_echo_guard():
    """BotManager.on_chat_message must skip messages where sender == this bot.

    Without this guard, a bot's own reply triggers another reply → infinite loop.
    """
    bots_py = (ROOT / "modules" / "bots.py").read_text(encoding="utf-8")
    # The guard: `if user_id == bot_uid: continue`
    assert "user_id == bot_uid" in bots_py or "user_id == self.bot_user_id" in bots_py, (
        "BotManager is missing the self-echo guard. Bots will reply to their own messages."
    )


def test_reg003c_bot_manager_has_bot_to_bot_guard():
    """BotManager must skip messages from other bots unless directly mentioned."""
    bots_py = (ROOT / "modules" / "bots.py").read_text(encoding="utf-8")
    assert 'startswith("bot-")' in bots_py or "startswith('bot-')" in bots_py, (
        "BotManager is missing the bot-to-bot chatter guard."
    )
