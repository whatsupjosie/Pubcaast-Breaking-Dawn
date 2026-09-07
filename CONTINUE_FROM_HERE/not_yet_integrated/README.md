# Before you merge any of these in

## DANGER — naming collision
`character_engine.py` is Jeremy Cricket's adaptive-care state machine
(Mode / VarianceSignal / TOTAL_CARE_MANDATE). It is NOT the same thing
as `WORKING_PROGRAM/pubcast/modules/character_engine.py`, which is a
real, load-bearing system (bot turn-taking, thought logging, calibration).

Same filename, same intended folder, completely different job. Give it
its own name before it goes anywhere near the working tree.

## unified_bridge.py
The corrected Python bridge for the C++ twin engine (V3.9 DX12).
All 5 bugs from the original fixed and verified against bridge.h.
This goes on ZOIDBERG — run it against engine_host.exe.
On Zoidberg: cl /nologo /O2 /EHsc /std:c++17 /Isrc src/engine_host.cpp /Fe:engine_host.exe

## twin_engine_service.py
ALREADY WIRED INTO PUBCAST — it's in modules/ and mounted in main.py.
This copy is here for reference only. Do not merge again.

## memory_api.py
Two real defects — imports pubcast_memory_hardened (doesn't exist) and
hardcoded JWT secret. Likely superseded by personal_ai_memory_api.py.
Confirm before touching either.

## prosody_engine.py, facial_performance.py
Near-identical to what's already running. Reference only.

## evo_integration.py
The RUNNING version is more advanced than this copy (already has E-Pete
+ PeteCharacter wired). Do not merge over the live one.

## claude.py
Real, clean, working async Anthropic adapter. Not yet wired. No collision
risk. Safe to add to modules/ when ready to give a bot a real Claude voice.

Full detail in SESSION_HANDOFF_2026-08-19.md section 01.8.
