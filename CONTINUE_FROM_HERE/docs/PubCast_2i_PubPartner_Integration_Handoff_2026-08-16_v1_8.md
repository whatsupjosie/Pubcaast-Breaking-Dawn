HANDOFF VERSION: 1.7

# PubCast / 2i / PubPartner Integration Handoff

## Source-grounded architecture review and hookup plan

**Date:** 2026-08-16
**Revision:** 1.2 — Phase 02 self-review / lifecycle hardening

## Executive conclusion

2i and PubPartner are a functional duo inside PubCast, but they should
remain independently runnable systems.

The correct relationship is:

    Foresight UI
          |
        PubCast
          |
      +---+----------------+
      |                    |
     2i <---- communication ----> PubPartner
      |                    |

manuscript/editor communication, Alex/Jeremy, memory/provider spine

The important architectural point is that PubPartner is not useful
merely as a second visual application. Its value to 2i comes from the
communication/intelligence layer it supplies. Conversely, 2i owns the
manuscript/editor experience and should not absorb PubPartner's internal
intelligence, memory, or provider authority.

The existing source/evidence shows that a real 2i -\> PubPartner path
has already been established and exercised: role routing -\> Alex
identity/memory bridge -\> Jeremy context -\> LLM call. The previous
implementation found that the two systems were originally calling
different, unconnected API paths and added a compatibility route. That
working path should now be formalized rather than replaced.

------------------------------------------------------------------------

# 1. What was actually inspected

The available project material includes:

-   the current 2i writer's-room frontend, including the v20/hardfix
    line of work;
-   the PubCast/PubPartner FastAPI backend and its verified
    boot/integration notes;
-   PubPartner's shared spine and provider path;
-   the Foresight v18 frontend and its service/connection concepts;
-   the Thinking Context and EQ donor audits, used to identify conflicts
    and reusable ideas;
-   the previous integration/debugging record, including the
    already-tested 2i -\> PubPartner path.

This is therefore a source-derived integration plan, not a generic
proposed architecture.

------------------------------------------------------------------------

# 2. 2i: what it owns

The current 2i frontend is a substantial writer's-room application.

It owns:

-   manuscript state;
-   committed manuscript lines;
-   current draft buffer;
-   chapters;
-   current chapter;
-   branch state;
-   reading position;
-   generation pool;
-   protected/locked material;
-   document persistence;
-   `.2i` document structure;
-   reference/continuity UI;
-   chat UI;
-   co-writing/editor workflow.

The document payload currently records a `2i-document` version 3 object
containing manuscript state, reading state, branch/pointer/pool state,
chat history, speed, and co-writing mode.

That means PubCast should not become the authoritative owner of the
manuscript itself. PubCast should host/orchestrate 2i; 2i should
continue owning its document/editor state.

## Critical implication

Do not make PubPartner responsible for directly modifying 2i's committed
manuscript.

The safe direction is:

    PubPartner
        |
        v
    suggestion/action
        |
        v
       2i
        |
        v

user approval \| v manuscript mutation

------------------------------------------------------------------------

# 3. 2i's current communication architecture

The frontend has a local provider-adapter model.

It can currently be configured for:

-   Claude;
-   OpenAI/OpenAI-compatible services;
-   local OpenAI-compatible endpoints such as Ollama/LM Studio.

The frontend's current chat path builds a system message containing
manuscript context and then sends that context plus chat history through
`callLLM()`.

The manuscript context is deliberately compact:

-   recent committed manuscript text;
-   current draft buffer;
-   most recent/read line.

The current chat history is capped at 16 role/content pairs.

This is good evidence for the context boundary we want: 2i already knows
how to assemble the writer-facing context. What it needs in integrated
mode is a different transport/authority path, not a second manuscript
engine.

------------------------------------------------------------------------

# 4. PubPartner: what it owns

PubPartner contains the communication/intelligence spine.

The source identifies these as existing PubPartner authorities:

-   `AlexCore`
-   `MemoryCore`
-   `GroundingAnchor` family
-   `AlexJeremyBridge`
-   `VerbatimVault`
-   `FCP1Packet`
-   `PubPartnerSpine`
-   `ProviderNeutralizer`
-   `PubPartnerProviderDispatcher`
-   `alex_routes.py`

`PubPartnerSpine` explicitly wires Alex/Jeremy state, session storage,
provider dispatch, profiles, guidance, and related runtime state.

The Alex route resolves an appropriate Alex instance/provider and passes
the message, context metadata, user identity, and typing information
into Alex processing.

This means 2i should talk to the PubPartner boundary, not directly to
Alex internals, Jeremy internals, memory storage, or provider SDKs.

------------------------------------------------------------------------

# 5. The already-proven 2i -\> PubPartner path

This is the most important existing integration fact.

The previous source-level work found that 2i and PubPartner were using
completely different, unconnected API paths.

A compatibility route was added.

The resulting path was exercised end-to-end:

    2i request
       |
       v
    PubCast/PubPartner route
       |
       v
    role routing
       |
       v
    Alex identity/memory bridge
       |
       v
    Jeremy context
       |
       v
    LLM/provider call
       |
       v
    response

The integration was tested honestly: when no LLM was reachable, it
failed rather than manufacturing a fake response.

This is the strongest existing hookup and should become the foundation
of the final integration.

------------------------------------------------------------------------

# 6. The major architectural mistake to avoid

Do not solve the integration by putting direct provider calls back into
2i.

The current 2i provider adapters are useful for standalone operation.

They should remain available in standalone mode.

But when 2i is running inside PubCast with PubPartner available, the
preferred path should be:

    2i
      |
      v
    PubPartner
      |
      v
    Alex/Jeremy/Memory
      |
      v
    PubPartnerProviderDispatcher
      |
      v
    provider

This preserves PubPartner's provider authority, memory path,
neutralization path, and Alex/Jeremy communication model.

The donor audit specifically identifies direct provider clients as a
conflicting second provider authority.

------------------------------------------------------------------------

# 7. Standalone operation

The systems need three legitimate operating modes.

## 7.1 2i standalone

2i runs by itself.

It keeps its local editor/document/provider behavior.

No PubCast dependency should be required.

## 7.2 PubPartner standalone

PubPartner runs through its own canonical application/runtime.

Its existing startup separation should remain intact.

PubPartner should not silently acquire a second PubCast lifecycle or
alternate memory system just because integration support exists.

## 7.3 PubCast integrated

PubCast hosts/coordinates the two:

    PubCast
      +-- 2i
      +-- PubPartner

This is the intended "duo" mode.

The applications remain distinct internally.

------------------------------------------------------------------------

# 8. PubCast's correct job

PubCast should become the host/orchestration layer.

Its responsibilities should include:

-   lifecycle;
-   service discovery;
-   shared session identity;
-   room/workspace identity;
-   integration routing;
-   capability reporting;
-   optional event transport;
-   eventual room/multi-agent orchestration.

It should not duplicate:

-   2i's manuscript state;
-   PubPartner's memory;
-   PubPartner's Alex/Jeremy logic;
-   PubPartner's provider dispatch.

The existing PubCast backend genuinely boots and exposes health data,
with 18 subsystems initializing in the tested build.

That makes it a viable host layer rather than something that needs to be
replaced with a new wrapper application.

------------------------------------------------------------------------

# 9. Foresight's position

Foresight is the visual operating shell.

The actual Foresight v18 file was identified and reconstructed from the
project material.

Its fan/connection UI already has a service-oriented concept:
model/service connection, latency, offline state, and related runtime
visibility.

Therefore the clean hierarchy is:

    Foresight
        |
        v
      PubCast
        |
        +--- 2i
        |
        +--- PubPartner

Foresight should not become the hidden owner of 2i or PubPartner.

It should ask PubCast for service state and launch/open the appropriate
application surface.

------------------------------------------------------------------------

# 10. Embedding 2i

For the first integrated milestone, embedding the 2i frontend inside the
PubCast/Foresight environment is reasonable.

But the embedding should be a presentation decision, not an
architectural coupling.

Prefer:

    Foresight/PubCast shell
          |
          v
       2i surface
          |
          v
       PubCast API
          |
          v
      PubPartner

Do not make the iframe/window itself the communication layer.

The browser surface should be replaceable without changing the backend
contract.

------------------------------------------------------------------------

# 11. Recommended communication boundary

The exact already-working compatibility endpoint should be inspected and
promoted to the canonical contract.

The contract should carry, at minimum:

    session identity
    user identity
    project/document identity where available
    user message
    manuscript context
    conversation history/reference
    requested mode/role if applicable

The response should carry:

    response text
    role/speaker identity
    request/session identity
    structured error information
    optional suggestions/actions

The important thing is not the exact endpoint name. The important thing
is that there is ONE documented contract rather than several overlapping
chat routes.

------------------------------------------------------------------------

# 12. Context architecture

Do not send the entire `.2i` document to PubPartner for every message.

Use layered context:

    PubCast session
        |
        +-- project/document identity
        |
        +-- 2i manuscript context
        |
        +-- current writing context
        |
        +-- current conversation
        |
        +-- current user message
        |
        v
    PubPartner context assembly
        |
        +-- Alex
        +-- Jeremy
        +-- MemoryCore
        +-- provider
        |
        v
      response

The existing 2i context builder already uses recent locked manuscript
text, current buffer text, and the most recent line. That is an
appropriate compact baseline.

------------------------------------------------------------------------

# 13. Memory must remain singular

Do not introduce a second PubPartner memory database just to improve 2i
integration.

The donor audit explicitly identifies alternate memory implementations
as dangerous duplication.

PubPartner already has `MemoryCore`.

2i owns manuscript/project state.

PubPartner owns interpersonal/partner memory.

Those are different things.

The correct relationship is:

    2i manuscript/project context
               |
               v
          PubPartner
               |
               v
           MemoryCore

Not:

    2i memory
       +
    PubPartner memory
       +
    another Jeremy memory
       +
    another donor memory

------------------------------------------------------------------------

# 14. Jeremy/Alex division of labor

The project material describes a two-voice model:

Jeremy: literal task/topic read and relevant context

Alex: line-reading / interpersonal interpretation

AI: melds the two into the actual response

`AlexJeremyBridge` appears to be the intended plumbing for this: it
builds an entry packet, accepts Jeremy signaling, applies the signal
overlay, and subjects the result to authority review before the AI turn.

One remaining source-level question is whether the current production
packet preserves the Jeremy read and Alex read as distinct fields all
the way into the AI turn.

That is a targeted verification item, not a reason to redesign the
bridge.

------------------------------------------------------------------------

# 15. Donor systems: what to use and what not to use

The Thinking Context and EQ systems are not safe to merge wholesale.

Thinking Context has:

-   its own lifecycle hook;
-   its own memory database;
-   background room watchers;
-   autonomous nudge machinery;
-   a different host contract.

EQ Suit has:

-   direct provider clients;
-   its own WebSocket room system;
-   its own multi-agent orchestration;
-   a separate emotional-state authority.

These would create competing authorities inside PubPartner.

## Useful extraction

The strongest useful Thinking Context idea is Jeremy's relevance-based
context enrichment pattern, rebuilt against PubPartner's `MemoryCore`.

The dependency-free circuit breaker is also a safe utility candidate for
the provider dispatcher.

## Do not import

-   alternate memory stores;
-   alternate provider adapters;
-   autonomous nudge queues;
-   second FastAPI lifespan;
-   EQ Suit's emotion-as-fact state machine;
-   EQ Suit's direct LLM clients;
-   EQ Suit's room orchestrator.

------------------------------------------------------------------------

# 16. Provider authority

Integrated mode should have one provider authority:

    PubPartnerProviderDispatcher

All external provider calls from the integrated PubCast/PubPartner path
should pass through that authority.

The donor audit specifically recommends any circuit-breaker wrapper sit
around the outbound provider call, leaving `ProviderNeutralizer` and the
existing result contract intact.

This also gives us one place to add:

-   retry;
-   timeout;
-   circuit breaker;
-   provider health;
-   latency measurement;
-   provider selection.

------------------------------------------------------------------------

# 17. Event architecture: later, not first

Do not introduce a WebSocket architecture merely because PubCast will
eventually need real-time rooms.

First make request/response boring and reliable.

Initial:

    2i -> PubPartner -> response -> 2i

Later:

    PubCast event bus
       |
       +-- 2i
       +-- PubPartner
       +-- Foresight

Possible future events:

    session.created
    session.closed
    document.opened
    document.changed
    partner.connected
    partner.disconnected
    generation.started
    generation.completed
    generation.failed
    provider.changed
    room.changed

That should be Phase 2+.

------------------------------------------------------------------------

# 18. Session identity

Integrated mode needs one PubCast session identity.

Conceptually:

    pubcast_session_id
         |
         +-- 2i session/document context
         |
         +-- PubPartner conversation/session

This prevents the UI from creating a new disconnected conversation
identity every time the embedded surface reloads.

The exact session implementation should reuse existing PubPartner
session machinery rather than create another database/schema.

------------------------------------------------------------------------

# 19. Manuscript actions

Eventually PubPartner should be able to propose structured actions to
2i.

Examples:

    suggest continuation
    suggest revision
    analyze scene
    summarize chapter
    identify continuity issue
    propose character behavior
    compare branches
    surface relevant memory

But the authority boundary remains:

    PubPartner proposes
          |
          v
         2i
          |
          v
       user decides
          |
          v
    manuscript changes

No silent AI mutation of committed manuscript text.

------------------------------------------------------------------------

# 20. Health and capability discovery

PubCast should expose a simple service/capability model.

Conceptually:

    PubCast       READY
    PubPartner    READY
    2i            READY
    Provider      READY/DEGRADED/OFFLINE

And capabilities:

    2i:
      manuscript
      documents
      chat

    PubPartner:
      communication
      Alex
      Jeremy
      memory
      provider

    PubCast:
      sessions
      rooms
      orchestration
      events

Foresight should display this rather than hardcoding assumptions.

------------------------------------------------------------------------

# 21. Startup sequence

The intended cold-start sequence should be:

    START PUBCAST
         |
         v
    PubCast initializes
         |
         +-- PubPartner initializes
         |
         +-- 2i becomes available
         |
         v
    Foresight opens
         |
         v
    service discovery
         |
         +-- PubCast READY
         +-- PubPartner READY
         +-- 2i READY
         |
         v
    Open 2i
         |
         v
    type message
         |
         v
    2i -> PubPartner
         |
         v
    Alex/Jeremy/Memory/provider
         |
         v
    response
         |
         v
    2i displays response

That is the first real integrated acceptance milestone.

------------------------------------------------------------------------

# 22. Implementation plan

## Phase 0 --- source reconciliation

Before more architectural changes:

1.  identify the exact current PubCast entrypoint;
2.  identify the exact PubPartner entrypoint;
3.  identify the exact 2i version to ship;
4.  identify the already-working compatibility route;
5.  identify the exact Foresight version;
6.  identify all existing launch scripts.

Do not create replacement launchers until this inventory is complete.

## Phase 1 --- stabilize the existing communication path

1.  inspect the compatibility route;
2.  document its request/response contract;
3.  identify whether it is already the correct production boundary;
4.  remove any redundant competing path;
5.  make 2i's integrated chat client call that boundary;
6.  retain local provider adapters for standalone mode.

## Phase 2 --- make PubCast the host

Add/verify:

    service health
    capability discovery
    session identity
    launch/attach lifecycle

Do not duplicate PubPartner internals.

## Phase 3 --- connect Foresight

Foresight should:

    start/attach to PubCast
    display PubCast health
    display 2i availability
    display PubPartner availability
    open 2i inside the environment

## Phase 4 --- browser-level integration test

Cold boot the entire stack.

Test:

    Foresight visible
    PubCast ready
    PubPartner ready
    2i visible
    chat request leaves 2i
    PubPartner receives it
    Alex/Jeremy path executes
    provider executes
    response returns
    response renders in 2i

Then close/reopen and test session/document continuity.

## Phase 5 --- richer context

Only after Phase 4:

    selected text
    chapter identity
    project identity
    branch identity
    continuity/reference context
    structured suggestions

## Phase 6 --- events and deeper PubCast orchestration

Only after the request/response contract is stable:

    event bus
    rooms
    real-time state
    partner presence
    multi-agent orchestration

------------------------------------------------------------------------

# 23. Testing discipline

The previous project history demonstrates why aggregate test claims are
not sufficient.

The backend's old README claimed production readiness and 53/53 passing.
Actual testing exposed syntax failures, missing dependencies, file
corruption, test collection failures, stale tests, naming mismatches,
missing subsystems, and a much larger failing population.

Therefore the integration acceptance record should name exact tests and
exact behavior.

Required categories:

### Contract

-   valid chat request;
-   malformed request;
-   missing service;
-   provider unavailable;
-   timeout;
-   invalid response.

### Integration

-   2i -\> PubPartner;
-   PubPartner -\> Alex;
-   PubPartner -\> Jeremy;
-   PubPartner -\> provider;
-   provider -\> PubPartner;
-   PubPartner -\> 2i.

### Lifecycle

-   2i standalone;
-   PubPartner standalone;
-   PubCast standalone;
-   PubCast + 2i;
-   PubCast + PubPartner;
-   complete stack.

### Persistence

-   `.2i` compatibility;
-   document save/load;
-   PubPartner session persistence;
-   no duplicate memory store.

### Browser

Use a real browser for the complete integrated smoke test. Source
history explicitly identifies the lack of real browser testing as a
confidence gap.

------------------------------------------------------------------------

# 24. Current known gaps to carry forward

The repaired PubCast/PubPartner backend was reported as genuinely
booting and exposing health, and the 2i -\> PubPartner path was tested.

However, the broader backend is not equivalent to "finished."

Known project evidence includes:

-   missing `purfluous_mgr`;
-   missing `performer_mgr`;
-   missing credential-store implementation;
-   missing `/api/inference/status`;
-   missing `/api/bots/{id}/speak`;
-   a large number of tests that still require individual triage.

Those are separate from the core 2i/PubPartner hookup and should not be
allowed to block the first integrated user-facing milestone unless they
are on the actual startup path.

------------------------------------------------------------------------

# 25. The target architecture

The final mental model should be:

                         FORESIGHT
                    visual operating shell
                              |
                              v
                           PUBCAST
                 host / lifecycle / sessions
                              |
                 +------------+------------+
                 |                         |
                 v                         v
                2i <------ communication -----> PubPartner
                 |                              |
          manuscript/editor                Alex/Jeremy
          document state                   MemoryCore
          writer workflow                  provider path
                 |                              |
                 +------------------------------+
                                |
                                v
                              LLM

Ownership:

    Foresight
        visual environment

    PubCast
        host/orchestration/session/event layer

    2i
        manuscript + writer/editor state

    PubPartner
        communication/intelligence + Alex/Jeremy/memory/provider spine

The systems remain independent.

The integration makes them useful together.

------------------------------------------------------------------------

# 26. Immediate next move

Do not redesign the three systems.

The next engineering pass should be a focused integration pass:

1.  verify the exact existing 2i -\> PubPartner route;
2.  verify the exact current PubPartner startup/runtime;
3.  verify the exact current PubCast startup/runtime;
4.  create one canonical integrated chat client in 2i;
5.  make PubCast own service discovery/session identity;
6.  make Foresight launch/display the integrated environment;
7.  embed/open 2i;
8.  run the cold-start end-to-end browser test;
9.  fix only what that path actually breaks;
10. then deepen context and event integration.

The central rule is:

> **Do not make 2i and PubPartner one program. Make them two programs
> that become one working system when PubCast hosts them.**


-------------------------------------------------------------------------------

# 27. Live execution evidence — 2026-08-16

This section records only work actually executed in the current sandbox
against the supplied project material.

## 27.1 PubPartner federation

Bundled canonical federation package:

- 14/14 bundled tests passed.
- Reconciled hardened working tree: 17/17 tests passed.
- SQLite thread-safety regression passed.
- Atomic local-upsert failure rollback passed.
- Persisted vector-clock recovery across restart passed.
- Dominant remote patch preserves unrelated local fields.

The 17-test result belongs to the reconciled working tree and should not be
retroactively attributed to the original 14-test bundle.

## 27.2 Real resident/portable HTTP execution

Two independent PubPartner processes were started with separate data stores.
The following were executed successfully:

- resident health;
- portable health;
- real manuscript commit/retrieval;
- real HTTP synchronization;
- live same-field conflict observation;
- configured bearer authentication: missing token rejected, wrong token rejected,
  correct token accepted;
- restart persistence of node identity and manuscript state;
- candidate-memory isolation from ordinary entity synchronization.

## 27.3 2i execution boundary

`2i-backend/server.js` passes syntax validation.

The supplied canonical backend could not be started as a real Express process in
this sandbox because the required npm dependency tree is absent and the sandbox
cannot resolve the npm registry.

The current npm test script is also a deliberate failing placeholder and is a
release blocker until replaced by a real test suite.

Therefore:

- 2i source inspection: VERIFIED;
- 2i Node runtime execution: UNPROVEN in this environment;
- 2i -> PubPartner live process round-trip: NOT YET PROVEN.

-------------------------------------------------------------------------------

# 28. Engineering direction assessment

The current architecture is directionally correct.

The strongest design decision is the separation of authority:

    Foresight
        visual environment
           |
        PubCast
        host/session/lifecycle
          / \
         /   \
       2i   PubPartner
       |       |
   manuscript  Alex/Jeremy
   editor      MemoryCore
               provider authority

Do not collapse these into one application merely to make integration easier.
The value is that each system remains independently useful while the host layer
makes them operate as one coherent environment.

The next phase should therefore be integration hardening, not wholesale redesign.

-------------------------------------------------------------------------------

# 29. Potential pitfalls and active engineering risks

## 29.1 False confidence from unit tests

A green federation suite does not prove that the actual 2i process talks to the
actual PubPartner process correctly.

Required discipline:

    source proof
    -> component proof
    -> real process proof
    -> complete topology proof

## 29.2 Full-manuscript HTTP commits versus field-level engine patches

The federation engine supports field-level patch merge semantics.
The current manuscript HTTP endpoint sends a complete manuscript field set per
commit.

Therefore an HTTP-level independent edit can legitimately conflict across many
fields even though the underlying engine correctly supports non-overlapping field
merges.

Do not use the HTTP manuscript endpoint as a substitute for testing the engine's
field-level semantics.

## 29.3 Session identity fragmentation

Reloading an embedded 2i surface must not silently create a new PubPartner
conversation/session.

PubCast should own the shared session identity and pass it through both systems.

## 29.4 Silent manuscript mutation

PubPartner must propose actions to 2i; it must not silently rewrite committed
manuscript state.

Any future structured action protocol needs explicit user-approval semantics.

## 29.5 Provider authority duplication

2i standalone provider adapters are legitimate.
Integrated mode must continue to route through the real PubPartner provider
authority rather than creating a second integrated provider path.

Do not create a replacement `PubPartnerProviderDispatcher` merely because that
name appears in older design notes; verify the current physical provider authority
first.

## 29.6 Memory authority leakage

Candidate memory, temporary inference, Jeremy signals, and durable MemoryCore
state must remain distinct.

A transient observation must not become durable user memory merely because it is
convenient to persist.

## 29.7 Startup dependency cycles

Do not let:

    PubCast -> PubPartner -> PubCast

become a mandatory initialization cycle.

Services must be able to start independently, report degraded/unavailable peers,
and attach when the host is ready.

## 29.8 Browser surface becoming the backend contract

The iframe/window/embedded surface is replaceable.
The HTTP/session contract must remain stable if the visual shell changes.

## 29.9 Fallback semantics becoming misleading

When PubPartner is unavailable, 2i must remain locally useful.

A successful local save must never be reported as successful remote
synchronization.

## 29.10 Authentication assumptions

Development mode may have authentication disabled.
Production acceptance must exercise configured authentication explicitly.
Health/readiness behavior should be tested separately from mutation authorization.

## 29.11 Replay and idempotency drift

Every synchronized change must have stable identity and be harmlessly replayable.
A retry must not create another logical mutation, another memory, or another
revision.

## 29.12 Restart/cursor drift

Persistent identity and persisted vector-clock knowledge are separate requirements.
Both must survive restart.

A persistent node ID with a reset causal clock is still a broken federation node.

## 29.13 SQLite concurrency is not the whole concurrency problem

The thread-safety defect was real and fixed, but database thread safety does not
prove semantic concurrency correctness.

Continue testing:

- same-entity concurrent updates;
- conflicting field updates;
- replay storms;
- failure during multi-step transitions;
- restart during synchronization.

## 29.14 Dependency completeness

The 2i bundle currently does not contain a usable npm runtime dependency install in
the present sandbox.

Before release, the package must either ship its dependency installation path or
provide a fully reproducible offline build artifact.

## 29.15 Placeholder release scripts

A package whose `npm test` intentionally exits with failure is not release-ready,
even if the application source itself passes syntax checking.

## 29.16 Evidence contamination

Historical transcript claims must never be promoted to current evidence merely
because they are repeated in later notes.

Every acceptance claim should identify:

- exact source revision/bundle;
- exact command;
- exact test;
- exact environment;
- exact result.

-------------------------------------------------------------------------------

# 30. Recommended next engineering sequence

## BLOCK A — finish 2i runtime readiness

1. Restore/install the actual 2i dependency tree in a reproducible environment.
2. Replace the placeholder npm test script with real automated tests.
3. Start the actual Node/Express process.
4. Exercise `/api/manuscript/commit` against the real resident PubPartner.
5. Verify the response and failure/fallback semantics.
6. Verify local manuscript persistence when PubPartner is unavailable.

## BLOCK B — establish the canonical integrated chat path

1. Inspect the actual 2i chat transport code.
2. Promote one real request/response boundary to the canonical integrated contract.
3. Carry session identity, user identity, project/document identity, manuscript
   context, conversation history, and requested mode only where already supported.
4. Route integrated requests through PubPartner rather than direct provider calls.
5. Preserve 2i's standalone provider path.

## BLOCK C — harden the host layer

1. Establish PubCast service discovery.
2. Establish shared `pubcast_session_id`.
3. Establish attach/start semantics without circular startup dependencies.
4. Make Foresight display service state rather than hardcoding assumptions.
5. Keep 2i and PubPartner independently runnable.

## BLOCK D — full live acceptance

Cold boot:

    Foresight
       |
    PubCast
       |
      / \
     /   \
   2i   PubPartner
         |
    Alex/Jeremy/Memory/provider

Verify:

1. all processes start;
2. service discovery reports correct state;
3. session identity is shared;
4. 2i sends a real request;
5. PubPartner receives it;
6. Alex/Jeremy path executes;
7. actual provider path executes;
8. response returns;
9. response renders in 2i;
10. document/session survives reload;
11. PubPartner failure degrades cleanly;
12. complete evidence is archived.

## BLOCK E — only after the boring path works

Then add:

- richer selected-text context;
- chapter/branch identity;
- structured suggestions;
- continuity/reference context;
- event bus;
- rooms/presence;
- deeper PubCast orchestration.

-------------------------------------------------------------------------------

# 31. Recommended engineering preparation before the final acceptance run

The following are worthwhile additions because they increase diagnostic value
without changing system authority:

- reusable real-process integration harness;
- deterministic isolated test data directories;
- automatic process logs on failure;
- port allocation/cleanup;
- evidence archive per acceptance run;
- state snapshots before and after high-risk synchronization operations;
- fault-injection tests for timeout, provider failure, dropped peer, replay,
  malformed sync data, and process death;
- post-restart state verifier;
- capability/readiness reporting;
- browser smoke runner for the complete stack.

These should be implemented as test/support infrastructure rather than new runtime
authorities inside PubPartner.

-------------------------------------------------------------------------------

# 32. Things deliberately NOT to build yet

Do not introduce these merely because they appear attractive:

- second memory database;
- second provider dispatcher;
- alternate chat API;
- websocket-driven integration before request/response is stable;
- autonomous nudge machinery from donor code;
- EQ Suit's emotional-state authority;
- duplicate manuscript engine;
- replacement PubCast launcher before startup inventory is complete.

Every one of these increases architectural surface area before the core path is
proven.

-------------------------------------------------------------------------------

# 33. Direction of the program

The project is now past the point where broad feature accumulation is the best use
of effort.

The federation core has enough substance to serve as a real synchronization layer.
The live resident/portable tests demonstrate that the service is not merely a unit
test artifact. The remaining uncertainty is primarily at the integration boundaries:
2i runtime availability, canonical chat transport, shared session identity, and
PubCast/Foresight lifecycle.

The best direction is therefore:

    stabilize
        -> prove
            -> integrate
                -> harden
                    -> enrich

not:

    add features
        -> add abstractions
            -> add more features
                -> test later

The most valuable product outcome is not three tightly coupled applications. It is
three strong systems whose boundaries are so clean that the user experiences them
as one coherent environment.

That gives us:

- 2i as the serious writer/editor;
- PubPartner as the persistent communication/intelligence partner;
- PubCast as the host and coordination layer;
- Foresight as the visual environment.

The architecture should preserve those strengths rather than flatten them.

-------------------------------------------------------------------------------

# 34. Evidence ledger additions — 2026-08-16

CLAIM:
Resident and portable PubPartner processes can synchronize over real HTTP.

EVIDENCE:
Two independent local PubPartner processes with separate data directories were
started and exercised through their HTTP interfaces.

DATE:
2026-08-16

ENVIRONMENT:
Sandboxed execution environment; local resident and portable nodes.

STATUS:
VERIFIED

NOTES:
Baseline transfer and live conflict observation succeeded.

---

CLAIM:
A live same-field manuscript conflict remains observable rather than silently
choosing one version.

EVIDENCE:
Independent resident and portable manuscript edits were synchronized and a
conflict record was returned.

DATE:
2026-08-16

ENVIRONMENT:
Two independent PubPartner processes.

STATUS:
VERIFIED

NOTES:
The manuscript HTTP endpoint submits the full field set; this is distinct from the
engine-level field-patch merge tests.

---

CLAIM:
Configured bearer authentication rejects missing and incorrect credentials and
accepts the correct credential.

EVIDENCE:
Live HTTP requests against a configured PubPartner process.

DATE:
2026-08-16

ENVIRONMENT:
Resident PubPartner process.

STATUS:
VERIFIED

---

CLAIM:
Node identity and manuscript state survive process restart.

EVIDENCE:
The same PubPartner data directory was reused across a real process shutdown and
restart; both identity and manuscript content were retained.

DATE:
2026-08-16

ENVIRONMENT:
Resident PubPartner process.

STATUS:
VERIFIED

---

CLAIM:
The real 2i Node/Express runtime has completed a live round-trip with PubPartner.

STATUS:
UNPROVEN

NOTES:
The supplied canonical dependency tree is not installed in the current sandbox,
and npm registry access is unavailable. `server.js` passes syntax validation but
runtime execution remains outstanding.

-------------------------------------------------------------------------------

# 35. Session log — engineering risk consolidation

## 2026-08-16

Completed:

- performed live PubPartner federation execution;
- verified real resident/portable synchronization;
- verified live conflict handling;
- verified authentication;
- verified restart persistence;
- verified candidate-memory isolation;
- reconciled the distinction between engine-level field patches and full-manuscript
  HTTP commits;
- identified 2i dependency/test-script blockers;
- reviewed the architecture against observed runtime behavior;
- added explicit engineering pitfalls, evidence rules, and next-step sequencing.

Current priority:

    2i runtime
      -> real 2i/PubPartner round-trip
      -> canonical integrated chat contract
      -> PubCast session/lifecycle
      -> Foresight host integration
      -> full browser acceptance

-------------------------------------------------------------------------------

# END HANDOFF


---

# 27. Phase 02 self-review and two-round debugging — 2026-08-16

The Phase 02 2i backend hardening was reviewed after implementation rather than being accepted on first-pass inspection.

## Real defect found and fixed

The graceful-shutdown path referenced `rateLimitCleanupInterval` while the original cleanup timer was named `rateLimitSweeper`. A signal during normal operation could therefore raise a `ReferenceError` before the server-close path completed.

The correction consolidated rate-limit cleanup to one authoritative timer and made shutdown idempotent with a `shutdownStarted` guard.

## Executed verification

- JavaScript syntax sweep across the 2i backend: PASS
- Python compile sweep across PubPartner/PubCast/integration: PASS
- dynamic 2i startup with controlled dependency shims: PASS
- single SIGTERM graceful shutdown: PASS, process exit 0
- duplicate SIGTERM handling: PASS, process exit 0

## Remaining limitation

The standard Node/npm test suite still cannot be executed from the supplied working bundle because required npm packages are not installed and uncached package retrieval is unavailable in the current sandbox. This remains an environment/package-install limitation, not evidence of runtime failure.

## Additional note

Two pre-existing PubCast Python `SyntaxWarning` messages remain and are outside the current 2i phase. They are recorded for the PubCast hardening pass rather than silently ignored.

---

# 28. Next engineering sequence

1. Build the real durable 2i outbound queue.
2. Prove restart-safe queue replay and duplicate suppression.
3. Close PubPartner tombstone/capability semantics.
4. Add explicit federation conflict resolution.
5. Enforce PubPartner service-level request-size limits.
6. Complete Alex/Jeremy/MemoryCore end-to-end verification.
7. Complete provider resilience at the existing provider authority.
8. Re-run the real 2i ↔ PubPartner process-level acceptance.
9. Stabilize PubCast as host.
10. Open and integrate Foresight.
11. Execute cold-boot browser acceptance.

The current strategic direction remains: finish and harden the existing products rather than replacing their authorities with a new umbrella architecture.


## 2026-08-16 — 2i lifecycle hardening / two-round review

Completed:
- Re-reviewed the prior 2i lifecycle changes before adding further functionality.
- Removed redundant rate-limit cleanup ownership and made shutdown clear the single authoritative sweeper.
- Corrected payload-size measurement to UTF-8 bytes.
- Added request correlation IDs and `X-Request-Id` response headers.
- Updated `.env.example` with the configurable rate-limit settings.
- Performed a dynamic lifecycle test with dependency shims covering startup, health, request correlation, SIGTERM, duplicate SIGTERM, clean exit, and shutdown logging.

RESULT: `DYNAMIC_LIFECYCLE_PASS`

Remaining environment limitation: the complete real-dependency Node suite cannot be executed in this sandbox until the missing npm dependencies are locally available.

Next: obtain/restore the actual 2i dependency tree, execute the full real Node test suite, then continue to the durable outbound queue.


# 36. Foresight v19 Surface Studio — 2026-08-16

A Foresight v19 UI variant has now been constructed from the existing v18 Counter
and tray architecture, incorporating the useful Gemini-generated PubWorld surface,
material, and Canvas-lighting ideas.

The new UI file is:

`foresight/foresight_ui_v19_surface_merged.html`

The design deliberately keeps the existing authority boundaries:

- Foresight owns presentation and UI interaction.
- PubCast `/api/surfaces` owns PubWorld surface records.
- PubCast `/api/lighting` owns persistent lighting state.
- The UI does not create a parallel surface store or lighting backend.

The Gemini prototypes are retained as reference material rather than becoming a
second production UI.

Static verification completed:

- embedded JavaScript syntax checks pass;
- HTML parses successfully;
- duplicate DOM IDs are absent;
- real `/api/surfaces` and `/api/lighting` contracts are referenced;
- original v18 UI remains preserved.

Outstanding acceptance:

- run the merged v19 UI in a real browser;
- verify live `/api/surfaces` loading and authenticated creation;
- verify responsive behavior and visual fidelity;
- then decide whether v19 becomes the canonical shipped Foresight UI.


---

# 37. Foresight v19 review / integration hardening — 2026-08-16

Foresight v19 now combines the existing Counter/fan/tray architecture with selected
Gemini-derived surface/material/lighting work. The merge was reviewed after construction.

Corrections made:

- lighting client routes aligned to the actual PubCast `/api/lighting/active` and
  `/api/lighting/apply` endpoints;
- fine-grained lighting controls use the existing lighting WebSocket protocol;
- invalid HTML tail structure was corrected;
- browser storage access was hardened;
- surface creation now distinguishes 401/403 authorization failure;
- a Foresight endpoint/document contract test was added.

Verification:

- embedded JS syntax: PASS;
- document structure: PASS;
- duplicate DOM IDs: none;
- Foresight contract tests: 3/3 PASS;
- selected PubCast integrity/routing/health tests: PASS;
- controlled Chromium runtime smoke: PASS, no page errors after hardening.

The browser smoke remains limited by the sandbox's localhost/file navigation policy, so
full real-browser network acceptance against the live PubCast service remains an explicit
open gate.

The architectural rule remains unchanged: Foresight is the presentation authority;
PubCast owns the surface and lighting service authorities; PubPartner/2i authorities are
not duplicated by the UI.


# 38. Foresight v21 Surface Materials target model

The Foresight appearance system now follows a target-first model. The user chooses the
object being changed before choosing a material. This is specifically a Foresight
presentation-layer capability; it does not change PubPartner, 2i, or PubCast authority.

Targets:

- Countertop
- Tray Surface
- Tray Border
- UI Frame
- Typography
- Robot Arm
- Fan / Menu

Material profiles currently expose roughness, metalness, transmission, sheen,
reflectivity, refraction, and prism/dispersion controls. Refraction and dispersion are
visual approximations rather than physically based rendering.

The target/material profile is stored through the existing Foresight browser-storage
adapter when persistence is available. No second backend state authority is introduced.
PubCast remains authoritative for `/api/surfaces` and `/api/lighting/*`.

The UI's slider controls are real range inputs and are intended to behave like the rest
of the system's scrollable control surfaces: visible, adjustable, persisted where
possible, and safe when storage is restricted.

The robot arm and fan/menu are explicit appearance targets because they are part of the
Foresight navigation mechanism rather than decorative afterthoughts.

Verification for v21:

- embedded JavaScript syntax: PASS;
- DOM/document structure: PASS;
- duplicate IDs: none;
- Foresight contract suite: 3/3 PASS.

Live browser/network acceptance remains outstanding.

## Foresight v22 review result — 2026-08-16

The target-first Surface Materials implementation was re-reviewed after v21. Two real
defects were found and corrected:

- target-specific profiles were stored independently but were not all applied to the live
  UI simultaneously; a per-target renderer now applies persisted appearance state to the
  Countertop, tray surfaces, borders, frame, typography, robot arm, and fan/menu;
- one legacy persistence block bypassed the shared restricted-storage-safe adapter and was
  reconciled.

Verification now recorded for v22:

- Foresight contract/target tests: 5/5 PASS;
- all embedded Foresight JavaScript syntax: PASS;
- PubPartner federation tests: 14/14 PASS;
- 2i server syntax: PASS;
- Python compile sweep: PASS;
- HTML structure and duplicate IDs: PASS.

A targeted broader PubCast route/health/regression run remains 116 passed / 18 failed;
those failures are pre-existing PubCast source/test drift rather than regressions from the
Foresight target/material work. They are retained as explicit PubCast cleanup work.

Evidence file:
`foresight/FORESIGHT_V22_REVIEW_2026-08-16.md`



# 39. Final three-round hardening status — 2026-08-16

The v7 working bundle was subjected to three final hardening rounds.

### Verified

- PubPartner federation 14/14.
- Foresight contract/target 5/5.
- PubCast targeted host/health 7/7.
- 2i syntax clean.
- Python compile clean.
- Foresight HTML structurally clean.
- No duplicate IDs.

### Explicitly unproven / environment blocked

- Real 2i process startup in this sandbox: blocked by missing npm dependencies (`express`) and unavailable package cache/network.
- Final federation deployment run: timed out before completion, therefore UNPROVEN.
- Real browser/network localhost acceptance: OPEN due sandbox browser navigation policy.

These are evidence states, not failures to be hidden.

The current top-level master/handoff pair is authoritative; previous copies are retained in `history/previous_docs/`.
