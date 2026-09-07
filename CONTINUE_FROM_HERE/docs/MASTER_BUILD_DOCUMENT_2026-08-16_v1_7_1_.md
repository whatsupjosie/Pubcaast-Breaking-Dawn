# MASTER BUILD DOCUMENT

PROJECT: PubPartner / 2i / RVF Integration
DOCUMENT VERSION: 1.7
DATE: 2026-08-16
STATUS: Living engineering blueprint / continuity source

---

# 00 — PURPOSE

This document is the durable logical source for continued development of the project.
The physical source tree in this bundle contains the actual current implementation and
historical/reference material. Development work may be designed, written, debugged,
and tested in chat; at meaningful checkpoints, the resulting implementation and
state should be consolidated back into this document.

A future session should be able to use this document together with the physical files
in the bundle to reconstruct what the system is, what has actually been proven, and
what must happen next.

The master is NOT permission to invent missing functionality. Source files, test
results, and explicit evidence outrank assumptions.

---

# 01 — AUTHORITY MAP

## Manuscript authority

2i remains the manuscript/editor authority.

## Partner/federation authority

PubPartner is the synchronization, partner-state, and federation authority. It must
not silently become the source of truth for 2i's private implementation state.

## Host/orchestration

The larger RVF/Prime/PubCast program remains the host/orchestration environment.

## User-facing environment

The existing 2i / PubPartner / RVF UI material is reference/current application
material, not automatically part of the federation core.

## Federation boundary

Federation synchronizes explicitly canonical entities. It does not synchronize
implementation internals merely because they exist locally.

---

# 02 — CURRENT STATE

CURRENT FEDERATION BUILD:
`01_CANONICAL_CURRENT/PubPartner_Federation_v0_2/`

CURRENT 2i BACKEND:
`01_CANONICAL_CURRENT/2i-backend/`

FULL EXISTING PROGRAM:
`01_CANONICAL_CURRENT/rvf_full_program_extracted/`

VERIFIED FEDERATION TEST COUNT:
17 tests currently execute in the reconciled federation working tree; the original bundled
set contained 14 tests. The 17-test result was re-executed during the v1.2 document audit
and is current evidence for the reconciled working tree. The original bundle remains a
historical/package baseline until rebuilt.

HISTORICAL CLAIM:
An earlier transcript reported 33/33. Those additional tests are not present in
this bundle and therefore are not current evidence.

REMAINING PRIMARY PROOF:
Live 2i -> resident PubPartner manuscript round-trip, followed by real portable /
resident federation synchronization.

---

# 03 — CURRENT FEDERATION CAPABILITIES

Implemented in the canonical v0.2 build:

- persistent portable/resident node identity
- vector-clock synchronization
- offline-first change exchange
- field-level concurrent merge/conflict handling
- idempotent change application
- FastAPI service layer
- manuscript commit/retrieval contract
- memory candidate capture/list/promote flow
- authentication configuration
- SQLite thread-safety hardening
- service tests
- adversarial concurrency tests

The physical source and tests in the canonical directory are authoritative for the
exact implementation.

---

# 04 — FEDERATION PROTOCOL

Core concepts:

- stable node identity
- vector clocks
- change identifiers
- envelopes
- capabilities
- cursor-based exchange
- idempotent application
- tombstones where represented by the current protocol
- explicit conflict recording
- field-level merge semantics

Wall-clock timestamps are not authoritative for ordering.

The complete protocol definition is in:
`01_CANONICAL_CURRENT/PubPartner_Federation_v0_2/docs/PROTOCOL.md`

---

# 05 — SYNC BOUNDARY

The following should NOT be silently synchronized as ordinary canonical entities:

- raw `.2i` documents
- provider credentials
- browser implementation state
- ephemeral UI state
- unreviewed affect inference
- SQLite implementation internals
- provider caches

If a future feature requires one of these to cross the boundary, it needs an explicit
architecture decision and test coverage.

---

# 06 — MEMORY AUTHORITY

Memory candidates and durable memory are separate authority levels.

The existing candidate/promotion gate must remain explicit.

Remote synchronization must not silently turn an unreviewed candidate into durable
memory.

The exact implementation must be inspected before adapting donor memory behavior.

---

# 07 — PROJECT INVARIANTS

1. Never silently overwrite concurrent user state.
2. 2i remains manuscript authority.
3. Federation synchronizes canonical entities, not implementation internals.
4. Historical test claims are not current evidence.
5. Unit tests are not live integration proof.
6. Live integration is not production-readiness proof.
7. Donor code is reference until deliberately adapted against current boundaries.
8. Memory promotion remains an explicit authority boundary.
9. Unreviewed affect inference must not silently become durable user memory.
10. Portable and resident nodes must remain independently useful while disconnected.
11. Valid bidirectional synchronization must converge.
12. Unsafe concurrent changes must remain observable as conflicts.
13. Preserved baselines must remain recoverable.
14. Work must be non-destructive unless a change is explicitly intentional and recorded.
15. A green test result must correspond to an actually executed test.

---

# 08 — CANONICAL FILE AREAS

## Federation

`01_CANONICAL_CURRENT/PubPartner_Federation_v0_2/`

Important files:

- `pubpartner_federation/engine.py`
- `pubpartner_federation/store.py`
- `pubpartner_federation/identity.py`
- `pubpartner_federation/protocol.py`
- `pubpartner_federation/service.py`
- `pubpartner_federation/memory.py`
- `tests/test_sync.py`
- `tests/test_service.py`
- `tests/test_concurrency.py`
- `docs/ARCHITECTURE.md`
- `docs/PROTOCOL.md`
- `README.md`
- `TEST_RESULT.txt`

## 2i integration target

`01_CANONICAL_CURRENT/2i-backend/`

The larger 2i/RVF integration material is also preserved under:
`01_CANONICAL_CURRENT/rvf_full_program_extracted/bella-faux-pas/`

## Full program

`01_CANONICAL_CURRENT/rvf_full_program_extracted/`

This is preserved so future development can inspect real existing code instead of
reconstructing it from memory or summaries.

---

# 09 — VERIFIED BASELINES

Preserved immutable references:

- `02_VERIFIED_BASELINES/PubPartner_Federation_v0_1(1).zip`
- `02_VERIFIED_BASELINES/rvf-full-program-original.zip`

Do not overwrite these.

---

# 10 — REFERENCE / DONOR MATERIAL

`03_REFERENCE_MATERIAL/`

Includes audits, patches, transcripts, identity/concurrency reference files, and
other supporting material.

The donor audit is particularly important. It rejects wholesale merging of Thinking
Context and EQ Suit and identifies only narrow candidates for possible adaptation.

Before adapting provider or memory behavior, inspect the production implementation
in the canonical/full program rather than trusting donor abstractions.

---

# 11 — DONOR EXTRACTION LEDGER

## Jeremy task/topic retrieval

STATUS: Investigate only.

Requirement: inspect the production Alex/Jeremy bridge and confirm the existing
responsibility boundaries before adapting any donor retrieval pattern.

## Jeremy timing observations

STATUS: Investigate only.

Requirement: verify the existing implementation before introducing timing state.

## CircuitBreaker

STATUS: Investigate only.

Potential use: dependency-free per-provider wrapper if the current dispatcher lacks
an equivalent.

Rule: do not introduce a second provider abstraction.

## Thinking Context

STATUS: Rejected for wholesale integration.

## EQ Suit

STATUS: Rejected for wholesale integration.

---

# 12 — TESTING MODEL

Testing states are intentionally distinct:

IMPLEMENTED
-> code exists.

UNIT-TESTED
-> isolated behavior has executed automated coverage.

INTEGRATION-TESTED
-> components communicated through their real interfaces.

DEPLOYMENT-TESTED
-> behavior was verified in the intended deployment topology.

PROVEN
-> relevant adversarial/recovery testing has also been completed for the risk level.

Never collapse these labels.

---

# 13 — CURRENT TEST EVIDENCE

## Federation v0.1

Historical independent verification: 6/6 tests passed.

## Federation v0.2

Current bundled suite: 14 tests.

Recorded bundled result: 14/14 passed in the packaging verification run.

Reconciled hardening run: 17/17 passed after atomic transaction, restart-clock, and
dominant-remote-patch preservation hardening.

## Concurrency

Adversarial coverage includes simultaneous manuscript commits across contested
chapters and simultaneous memory captures. The intended assertion is that requests
succeed without torn writes and stored revisions remain complete.

## Live servers

Two local PubPartner processes were previously brought up successfully, resident on
port 8000 and portable on port 8001, with healthy responses.

## Still unproven

- real Node/2i -> resident PubPartner manuscript commit
- real portable -> resident synchronization across separate processes
- real resident -> portable synchronization across separate processes
- convergence after independent offline edits
- live same-field conflict behavior
- production authentication boundary
- restart/persistence verification in the deployment topology

---

# 14 — INTEGRATION ACCEPTANCE MATRIX

| Integration / Property | Current status |
|---|---|
| Federation unit suite | VERIFIED: 17/17 reconciled working-tree tests |
| Concurrency regression | VERIFIED by bundled adversarial tests |
| Resident PubPartner startup | Previously demonstrated |
| Portable PubPartner startup | Previously demonstrated |
| 2i -> live resident commit | NOT PROVEN: canonical 2i runtime dependencies unavailable in sandbox |
| PubPartner manuscript retrieval after 2i commit | VERIFIED directly; 2i-mediated retrieval NOT PROVEN |
| 2i fallback with PubPartner unavailable | NOT PROVEN live |
| Portable -> resident live sync | VERIFIED live via `/api/sync/trigger` |
| Resident -> portable live sync | VERIFIED live baseline exchange |
| Offline independent edits converge | NOT PROVEN |
| Same-field conflict surfaced live | VERIFIED live |
| Memory candidate isolation from entity sync | VERIFIED live |
| Identity survives restart | VERIFIED by persisted identity implementation; restart-clock regression VERIFIED |
| Role mismatch rejection | TEST/VERIFY |
| Configured bearer authentication | VERIFIED live |
| Production provider dispatcher path | INSPECT |
| Alex/Jeremy production field path | INSPECT |
| MemoryCore promotion path | INSPECT |

---

# 15 — NEXT BUILD ORDER

## BLOCKING ACCEPTANCE WORK

1. Run the canonical v0.2 suite from a clean environment.
2. Start clean resident PubPartner.
3. Start 2i against resident PubPartner.
4. POST a real manuscript commit through 2i.
5. Retrieve the manuscript directly from PubPartner.
6. Verify project/chapter identity and exact content.
7. Test 2i fallback when PubPartner is unavailable.
8. Start clean portable and resident nodes.
9. Exercise portable -> resident sync.
10. Exercise resident -> portable sync.
11. Verify convergence after independent offline edits.
12. Exercise a genuine same-field conflict.

## HARDENING

13. Verify candidate memory does not leak through normal entity synchronization.
14. Verify node identity survives restart.
15. Verify role mismatch is rejected.
16. Verify configured bearer authentication.
17. Test malformed/expired/replayed sync material where supported by the current protocol.
18. Add live HTTP integration tests against actual processes.

## INVESTIGATION

19. Inspect the production provider dispatcher.
20. Determine whether a CircuitBreaker is actually missing.
21. Inspect AlexJeremyBridge end-to-end.
22. Inspect MemoryCore promotion/durability path.
23. Only then consider narrowly scoped donor adaptations.

## PACKAGING

24. Produce a fresh test report.
25. Update BUILD_STATUS.
26. Update this master.
27. Update CONTINUITY_AND_HANDOFF.
28. Produce the next continuity bundle.

---

# 16 — CHAT-FIRST DEVELOPMENT WORKFLOW

During active development, the conversation is the workshop.

Code may be written, revised, tested, and reasoned about in chat without repeatedly
materializing the entire project to disk.

Use explicit file identifiers when practical:

`FILE: PP-SYNC-001`
`PATH: pubpartner_federation/engine.py`

At meaningful checkpoints, consolidate the resulting implementation/state into this
master document.

When the user asks to materialize the program, walk the file manifest and construct
the actual filesystem from the recorded source and paths.

---

# 17 — FILE RECORD FORMAT FOR FUTURE WORK

For newly developed files, use:

FILE ID: [stable identifier]
PATH: [relative filesystem path]
STATUS: [PLANNED / IN PROGRESS / COMPLETE / VERIFIED]
PURPOSE: [description]
DEPENDENCIES: [file IDs]
SOURCE:

```text
[complete source when this document is being used as the source blueprint]
```

Do not create duplicate competing versions without explicitly naming the status and
reason.

---

# 18 — EVIDENCE LEDGER

Use this structure for important claims:

CLAIM:
[claim]

EVIDENCE:
[test/report/file/command]

DATE:
[date]

ENVIRONMENT:
[environment]

STATUS:
[VERIFIED / HISTORICAL / UNPROVEN / FAILED]

NOTES:
[notes]

This prevents historical transcript claims from becoming accidental current facts.

---

# 19 — BUG / DEBUGGING RECORD

For every important bug:

BUG ID:
[ID]

SYMPTOM:
[description]

ROOT CAUSE:
[description]

FIX:
[description]

REGRESSION TEST:
[test]

STATUS:
[OPEN / FIXED / VERIFIED]

---

# 20 — RELEASE RULES

A release candidate is not declared merely because the unit suite is green.

Before release, the relevant integration topology must be exercised, recovery and
restart behavior must be tested, and the bundle must include an accurate handoff and
current evidence record.

---

# 21 — SESSION LOG

## 2026-08-16 — Continuity consolidation

Completed:

- Reviewed current continuity handoff and build status.
- Confirmed canonical federation source and current bundled test evidence.
- Added this master build document to the continuity architecture.
- Added explicit authority map, invariants, evidence discipline, integration matrix,
  donor ledger, and blocking/investigation/packaging separation.
- Preserved physical source tree and historical baselines.
- Audited the embedded executable code in this master against the reconciled federation
  source and corrected documentation/source mismatches.
- Re-executed the reconciled federation suite: 17/17 passed.

Next:

- Prove the live 2i -> resident PubPartner path.
- Prove portable/resident synchronization.
- Harden the real HTTP/deployment boundary.

## 2026-08-16 — Live execution acceptance run

Completed:

- Executed the bundled federation suite: 14/14 passed.
- Started a real resident PubPartner process and verified commit/retrieval over HTTP.
- Started independent resident/portable processes and verified live synchronization.
- Verified a live same-field conflict remained observable.
- Verified configured bearer authentication with missing, wrong, and correct tokens.
- Verified manuscript and node-identity persistence across a real restart.
- Verified candidate-memory isolation during live synchronization.
- Syntax-checked the canonical 2i `server.js` successfully.

Not yet proven:

- Real 2i Express runtime, because canonical runtime dependencies are absent from the bundle and the sandbox cannot reach the npm registry.
- Full 2i -> PubPartner live round-trip through the Node process.
- Full PubCast/Foresight/browser cold-boot acceptance.

Findings:

- The current 2i `npm test` script is a placeholder that intentionally exits with failure and must be replaced before release.
- The current manuscript endpoint sends full manuscript fields per commit; this explains why live endpoint-level independent edits can conflict on multiple fields even though the underlying federation engine supports field-level patch merging.

## 2026-08-16 — Master code-integrity audit

Completed:

- Reconciled §21A executable code against the physical federation implementation.
- Corrected the store helper name mismatch.
- Corrected the hardening-test file path mismatch.
- Removed the implication that non-reconciled snippets are accepted implementation.
- Executed the canonical reconciled federation suite: 17 passed in 0.80s.

Status:

- Embedded accepted federation code: VERIFIED.
- Speculative chat-generated integration code: explicitly rejected.
- Live 2i → resident PubPartner proof: still outstanding.
- Live portable/resident process synchronization proof: still outstanding.

---


# 21A — CODE INTEGRITY STANDARD

The master may contain executable source only when that source has been reconciled
against the physical implementation and syntax-checked/tested in the applicable
working tree. Code that is architectural guidance, a template, or not yet reconciled
must not be presented as accepted implementation.

For this document revision:

- Python executable blocks in §21A were compared against the reconciled federation source.
- The federation suite was executed from the reconciled working tree.
- Result: `17 passed in 0.80s`.
- One documentation defect was corrected: the real store helper is `_commit_if_needed()`,
  not `_commit_if_outer()`.
- The hardening regressions live in the canonical `tests/test_sync.py`; they are not a
  separate `tests/test_hardening_additions.py` file.
- No speculative HTTP routes, provider APIs, or invented constructor signatures are
  accepted as source in this document.

# 21A — CONSOLIDATED ACCEPTED FUNCTIONAL CODE

This section records code that has survived source reconciliation and execution in the
current federation working tree. It is not a collection of speculative snippets.
Only code shown here with STATUS VERIFIED may be treated as accepted implementation.

## FILE: `pubpartner_federation/store.py`
STATUS: VERIFIED
PURPOSE: SQLite persistence, thread safety, and atomic multi-step state transitions.

Accepted implementation requirements:

- `sqlite3.connect(..., check_same_thread=False)` is paired with an `RLock`.
- `transaction()` wraps an entire logical state transition in `BEGIN IMMEDIATE` and
  rolls the whole transition back on failure.
- Individual `put()`, `record_change()`, `mark_change()`, and `add_conflict()` calls
  do not commit when they are executing inside a parent transaction.
- `observed_clock()` reconstructs persisted causal state from stored entities and
  changes so process restart does not reset vector-clock knowledge.

Core accepted code:

```python
from contextlib import contextmanager
from typing import Iterator

@contextmanager
def transaction(self) -> Iterator[sqlite3.Connection]:
    """Run one logical state transition atomically."""
    with self.lock:
        if self._closed:
            raise RuntimeError("sync store is closed")

        outermost = self._tx_depth == 0
        if outermost:
            self.db.execute("BEGIN IMMEDIATE")

        self._tx_depth += 1
        try:
            yield self.db
        except Exception:
            self._tx_depth -= 1
            if outermost:
                self.db.rollback()
            raise
        else:
            self._tx_depth -= 1
            if outermost:
                self.db.commit()


def _commit_if_needed(self) -> None:
    if self._tx_depth == 0:
        self.db.commit()


def observed_clock(self) -> VectorClock:
    """Recover persisted causal state after process restart."""
    with self.lock:
        clock = VectorClock()

        for row in self.db.execute(
            "SELECT version FROM entities"
        ).fetchall():
            clock = clock.merge(
                VectorClock.from_dict(
                    json.loads(row["version"])
                )
            )

        for row in self.db.execute(
            "SELECT version FROM changes"
        ).fetchall():
            clock = clock.merge(
                VectorClock.from_dict(
                    json.loads(row["version"])
                )
            )

        return clock
```

## FILE: `pubpartner_federation/engine.py`
STATUS: VERIFIED
PURPOSE: Apply local and remote federation changes atomically while preserving patch
semantics and causal state.

Accepted constructor behavior:

```python
def __init__(self, node_id: str, store: SyncStore):
    if not isinstance(node_id, str) or not node_id.strip():
        raise ValueError("node_id must not be empty")

    self.node_id = node_id
    self.store = store
    self.clock = store.observed_clock()
```

Accepted local-upsert transaction boundary:

```python
def upsert(
    self,
    entity_type: str,
    entity_id: str,
    fields: Dict[str, Any],
) -> Change:
    if not isinstance(fields, dict):
        raise TypeError("fields must be a dict")

    with self.store.transaction():
        current = self.store.get(entity_type, entity_id)
        base = (
            current.version
            if current is not None
            else VectorClock()
        )

        self.clock = (
            self.clock
            .merge(base)
            .increment(self.node_id)
        )

        merged = (
            dict(current.fields)
            if current is not None and not current.deleted
            else {}
        )
        merged.update(fields)

        entity = Entity(
            entity_type,
            entity_id,
            merged,
            self.clock,
            False,
        )

        change = self._change(
            entity,
            base,
            fields,
            False,
        )

        self.store.put(
            entity,
            changed_fields=fields.keys(),
        )
        self.store.record_change(change)
        self.store.mark_change(change.change_id)
        return change
```

Accepted dominant-remote-patch behavior:

```python
if remote.version.dominates(local.version):
    if remote.deleted:
        entity = remote_to_entity(remote)
        changed_fields = None
    else:
        merged = dict(local.fields)
        merged.update(remote.fields)
        entity = Entity(
            local.entity_type,
            local.entity_id,
            merged,
            remote.version,
            False,
        )
        changed_fields = remote.fields.keys()

    self.store.put(
        entity,
        changed_fields=changed_fields,
    )
    self.store.mark_change(change.change_id)
    return ApplyResult(True)
```

This specifically prevents a dominant remote PATCH from deleting unrelated local
fields. A remote deletion remains a tombstone and therefore replaces the entity as
an intentional destructive operation.

Accepted remote-apply transaction boundary:

```python
def apply(self, change: Change) -> ApplyResult:
    with self.store.transaction():
        if self.store.has_change(change.change_id):
            return ApplyResult(False, duplicate=True)

        remote = change
        local = self.store.get(
            change.entity_type,
            change.entity_id,
        )

        self.clock = self.clock.merge(change.version)

        if local is None:
            entity = remote_to_entity(remote)
            self.store.put(
                entity,
                changed_fields=remote.fields.keys(),
            )
            self.store.mark_change(change.change_id)
            return ApplyResult(True)

        if local.version.dominates(remote.version):
            self.store.mark_change(change.change_id)
            return ApplyResult(False, ignored=True)

        if remote.version.dominates(local.version):
            if remote.deleted:
                entity = remote_to_entity(remote)
                changed_fields = None
            else:
                merged = dict(local.fields)
                merged.update(remote.fields)
                entity = Entity(
                    local.entity_type,
                    local.entity_id,
                    merged,
                    remote.version,
                    False,
                )
                changed_fields = remote.fields.keys()

            self.store.put(
                entity,
                changed_fields=changed_fields,
            )
            self.store.mark_change(change.change_id)
            return ApplyResult(True)

        if remote.deleted:
            reason = "concurrent_delete_update"
            remote_entity = remote_to_entity(remote)
            self.store.add_conflict(local, remote_entity, reason)
            self.store.mark_change(change.change_id)
            return ApplyResult(
                False,
                conflict=Conflict(
                    local.entity_type,
                    local.entity_id,
                    local,
                    remote_entity,
                    reason,
                ),
            )

        if local.deleted:
            reason = "concurrent_update_delete"
            remote_entity = remote_to_entity(remote)
            self.store.add_conflict(local, remote_entity, reason)
            self.store.mark_change(change.change_id)
            return ApplyResult(
                False,
                conflict=Conflict(
                    local.entity_type,
                    local.entity_id,
                    local,
                    remote_entity,
                    reason,
                ),
            )

        conflicts = []
        for key, remote_value in remote.fields.items():
            local_field_version = self.store.field_version(
                local.entity_type,
                local.entity_id,
                key,
            )
            if local_field_version.strictly_dominates(
                remote.base_version
            ) and local.fields.get(key) != remote_value:
                conflicts.append(key)

        if conflicts:
            reason = (
                "concurrent_fields:"
                + ",".join(sorted(conflicts))
            )
            remote_entity = remote_to_entity(remote)
            self.store.add_conflict(local, remote_entity, reason)
            self.store.mark_change(change.change_id)
            return ApplyResult(
                False,
                conflict=Conflict(
                    local.entity_type,
                    local.entity_id,
                    local,
                    remote_entity,
                    reason,
                ),
            )

        merged = dict(local.fields)
        applied_fields = []
        for key, value in remote.fields.items():
            local_field_version = self.store.field_version(
                local.entity_type,
                local.entity_id,
                key,
            )
            if not local_field_version.strictly_dominates(
                remote.base_version
            ):
                merged[key] = value
                applied_fields.append(key)

        merged_entity = Entity(
            local.entity_type,
            local.entity_id,
            merged,
            local.version.merge(remote.version),
            False,
        )
        self.store.put(
            merged_entity,
            changed_fields=applied_fields,
        )
        self.store.mark_change(change.change_id)
        return ApplyResult(True)
```

The complete current implementation remains authoritative in the physical file:
`01_CANONICAL_CURRENT/PubPartner_Federation_v0_2/pubpartner_federation/engine.py`.

## FILE: `tests/test_sync.py`
STATUS: VERIFIED
PURPOSE: Regression coverage for the hardening defects addressed during this session.
The tests below are the exact current tests in the canonical synchronization test file.

```python
def test_newer_remote_patch_preserves_unrelated_local_fields(tmp_path):
    a, b = make(tmp_path, "travel"), make(tmp_path, "resident")
    a.upsert("profile", "p1", {"tone": "warm", "pace": "slow"})
    b.receive(a.envelope())

    a.upsert("profile", "p1", {"tone": "direct"})
    assert b.store.get("profile", "p1").fields == {"tone": "warm", "pace": "slow"}

    result = b.receive(a.envelope(b.clock))[0]
    assert result.applied is True
    assert b.store.get("profile", "p1").fields == {"tone": "direct", "pace": "slow"}


def test_restart_recovers_persisted_vector_clock(tmp_path):
    path = tmp_path / "restart.db"
    first = SyncEngine("travel", SyncStore(path))
    first.upsert("profile", "p1", {"tone": "warm"})
    first_clock = first.clock.to_dict()["travel"]
    first.store.close()

    second = SyncEngine("travel", SyncStore(path))
    assert second.clock.to_dict()["travel"] == first_clock
    change = second.upsert("profile", "p1", {"tone": "direct"})
    assert change.version.to_dict()["travel"] > first_clock
    second.store.close()


def test_local_upsert_is_atomic_when_change_recording_fails(tmp_path, monkeypatch):
    store = SyncStore(tmp_path / "atomic.db")
    engine = SyncEngine("travel", store)

    original = store.record_change

    def fail_record(change):
        raise RuntimeError("simulated change-record failure")

    monkeypatch.setattr(store, "record_change", fail_record)

    with pytest.raises(RuntimeError, match="simulated change-record failure"):
        engine.upsert("profile", "p1", {"tone": "warm"})

    assert store.get("profile", "p1") is None
    assert store.export_changes(engine.clock) == []

    monkeypatch.setattr(store, "record_change", original)
    change = engine.upsert("profile", "p1", {"tone": "warm"})
    assert change.change_id
    store.close()
```

These tests execute as part of the 17-test canonical federation suite.

## NOT CONSOLIDATED FROM CHAT

The following earlier chat-generated code remains rejected until it is reconciled
against the physical source and executed:

- speculative replacement `contracts.py`
- speculative `manuscript.py`
- speculative JavaScript `pubpartner-client.js`
- speculative JS fallback wrapper
- invented WebSocket integration routes
- invented conflict/replay endpoint shapes
- any protocol envelope schema not matching `docs/PROTOCOL.md`

They are not part of the accepted implementation.


# 21B — LIVE EXECUTION EVIDENCE — 2026-08-16

This section records tests actually executed against the physical source tree in the
continuity bundle. These results supersede assumptions but do not erase distinctions
between bundled, reconciled-working-tree, and live deployment evidence.

## Federation packaged bundle

Environment:
`01_CANONICAL_CURRENT/PubPartner_Federation_v0_2/`

Command:
`python -m pytest -q`

Result:
`14 passed in 0.88s`

STATUS:
VERIFIED — current bundled source.

## Resident PubPartner real-process smoke test

Process:
real `python -m pubpartner_federation.service`

Port:
`18000`

Verified:

- `/health` returned `status=healthy`.
- manuscript commit returned HTTP 200.
- direct manuscript retrieval returned HTTP 200.
- committed content was preserved exactly.
- persisted node identity was reported.

STATUS:
VERIFIED — real process / real HTTP / local SQLite.

## Resident ↔ portable real-process synchronization

Processes:

- resident: `18100`
- portable: `18101`

Verified:

- both independent processes started successfully;
- resident manuscript commit succeeded;
- portable synchronization through `/api/sync/trigger` succeeded;
- portable retrieved the resident manuscript through its own HTTP service;
- synchronized entity preserved the manuscript content.

STATUS:
VERIFIED — real process-to-process HTTP synchronization.

## Live same-field conflict

Two independent processes were started from a common baseline.

Resident changed `content` to `resident edit`.
Portable changed `content` to `portable edit`.

After synchronization:

- the operation returned a conflict record;
- both divergent values remained observable in the conflict;
- neither value was silently overwritten.

STATUS:
VERIFIED — live process-level same-field conflict detection.

## Live configured bearer authentication

A real resident process was started with:

`PP_API_KEY=secret-key`

Observed:

- missing token → HTTP 401;
- incorrect token → HTTP 401;
- correct token → HTTP 200.

STATUS:
VERIFIED — live configured authentication boundary.

## Live restart persistence

A real resident process was started against a persistent data directory.

After commit, the process was terminated and restarted against the same directory.

Verified:

- node identity survived restart;
- manuscript content survived restart.

STATUS:
VERIFIED — live restart/persistence behavior.

## Live memory-candidate isolation

A real portable process captured a memory candidate.

A synchronization trigger was then executed toward a separate resident process.

Verified:

- synchronization transferred zero ordinary entity changes;
- resident candidate list remained empty;
- portable candidate remained local.

STATUS:
VERIFIED — candidate memory does not leak through ordinary entity synchronization.

## Important live integration finding

The current manuscript HTTP endpoint sends a complete manuscript field set on each commit.
Therefore, a live "independent different-field edit" test through that endpoint is NOT the
same operation as the federation engine's true field-level patch test.

The federation engine's direct test suite already verifies non-overlapping field merges.
The live HTTP manuscript endpoint currently produces full-field manuscript patches.

This distinction must be preserved in future acceptance work rather than mislabeling a
full-entity conflict as a federation merge defect.

## 2i runtime limitation discovered during this run

`01_CANONICAL_CURRENT/2i-backend/server.js` passes Node syntax checking.

The canonical backend dependency tree is not installed in the supplied bundle and the
sandbox cannot resolve `registry.npmjs.org`; therefore the real Express process could not
be started in this execution environment.

The package currently contains:

`"test": "echo \"Error: no test specified\" && exit 1"`

Therefore:

- 2i runtime execution remains UNPROVEN in this sandbox;
- `npm test` is NOT accepted evidence;
- the test script itself is a release blocker and must be replaced with an actual suite;
- this is an environment/dependency limitation plus a real packaging/test-quality defect,
  not evidence that `server.js` itself fails runtime.

## 2i manuscript route source verification

The canonical `server.js` was inspected directly.

Verified source behavior:

- `POST /api/manuscript/commit` exists;
- required `project_id`, `chapter_id`, and `content` are validated;
- configured `PUBPARTNER_URL` is called through HTTP;
- PubPartner success returns the remote `manuscript_id`;
- PubPartner failure falls back to local acknowledgment;
- failed remote routing is explicitly distinguished from unconfigured routing.

STATUS:
SOURCE-VERIFIED / RUNTIME-UNPROVEN.



## 2026-08-16 — PubPartner / Iteration Wallet three-solution workflow decision

Completed:

- Evaluated three development models for the two PubPartner / Iteration Wallet
  deployments: sequential standalone-first, integrated-first, and shared-core/separate-
  boundary simultaneous development.
- Rejected standalone-first as the primary workflow because it delays integration discovery.
- Rejected integrated-first because it risks host dependency and weak standalone operation.
- Accepted shared-core, separate-boundary, simultaneous development with layered acceptance.

Decision:

- The two PubPartner / Iteration Wallet deployments will be developed in both operating
  modes at the same time.
- Shared domain/core behavior is implemented once.
- Standalone lifecycle/transport and PubCast integration adapters remain separate.
- Every shared-core change must be validated against both standalone and integrated use.


# END MASTER BUILD DOCUMENT

---

# 27 — PHASE 01/02 EXECUTION — 2026-08-16

## Phase 01 — Source reconciliation

STATUS: COMPLETE

The current working bundle was inspected directly.

Verified program areas:

- `pubpartner/` — federation/service implementation
- `2i-backend/` — Express communication backend
- `pubcast/` — PubCast host/runtime
- `integration/` — cross-process acceptance laboratory

The supplied working bundle does not contain the 2i writer/editor frontend or its `.2i` serialization implementation. Therefore the full writer/editor document persistence layer is not currently certifiable from this bundle.

The actual 2i backend entrypoint is:

`2i-backend/server.js`

The package manifest and lockfile declare Express, CORS, Axios, and dotenv.

## Phase 02 — 2i backend/state integrity

STATUS: PARTIAL — BACKEND HARDENED; EDITOR/DOCUMENT LAYER UNAVAILABLE IN BUNDLE

Verified backend routes:

- `GET /health`
- `POST /api/claude`
- `GET /api/thesaurus`
- `POST /api/manuscript/commit`
- `GET /api/messages`
- `DELETE /api/messages/clear`

Important authority finding:

The 2i backend does not act as the durable manuscript store. Manuscript synchronization is delegated to PubPartner when configured. Local fallback is explicitly reported as unsynchronized/degraded. The full editor/document authority remains outside this backend and cannot be certified here without the actual writer/editor source.

Accepted hardening in this phase:

- message IDs use `crypto.randomUUID()` rather than `Math.random()`;
- consecutive-commit identifier uniqueness is covered by regression test;
- graceful shutdown centralizes cleanup of background timers;
- cleanup timers are explicitly `unref()`-ed;
- stale PubPartner TODO text was removed because the route is implemented.

Verification:

- all JavaScript files under `2i-backend/` pass `node --check`;
- the 2i runtime suite could not be freshly executed in this sandbox because `node_modules` is incomplete and the environment cannot download uncached npm packages.

This remains an environment/package-install limitation, not a claim of application failure.

Required continuation when the full 2i frontend/document source is available:

- save/load round-trip;
- `.2i` version compatibility;
- chapter/branch persistence;
- draft-buffer persistence;
- reading-position persistence;
- protected/locked material persistence;
- chat-history persistence;
- interrupted-save recovery;
- malformed-document handling;
- older-document migration.



---

# 35 — PHASE 02 SELF-REVIEW / TWO DEBUG ROUNDS — 2026-08-16

## Scope

Reviewed the Phase 02 2i backend changes after implementation, then performed two independent debugging passes.

## Round 1 finding

A real lifecycle defect was found in the just-completed hardening pass: the shutdown path referenced `rateLimitCleanupInterval` even though the cleanup timer had been declared as `rateLimitSweeper`.

This was not cosmetic. A SIGTERM/SIGINT could enter the shutdown function and raise `ReferenceError` before the server-close path completed.

### Fix

- consolidated rate-limit cleanup to one authoritative timer;
- canonical cleanup handle is now `rateLimitCleanupInterval`;
- duplicate anonymous cleanup sweep removed;
- shutdown explicitly clears the canonical timer;
- `shutdownStarted` prevents duplicate termination signals from creating competing shutdown sequences.

## Round 2 verification

Executed:

- Node syntax check of `2i-backend/server.js`;
- Node syntax check of `2i-backend/test/server.test.js`;
- complete JavaScript syntax sweep of `2i-backend/**/*.js`;
- Python compile sweep of `pubpartner`, `pubcast`, and `integration`;
- dynamic 2i lifecycle execution using controlled dependency shims;
- single SIGTERM shutdown;
- duplicate SIGTERM shutdown.

Results:

- JavaScript syntax: PASS
- Python compile: PASS
- single-signal shutdown: PASS, exit 0
- duplicate-signal shutdown: PASS, exit 0

## Known environment limitation

The working bundle does not contain a complete installed Node dependency tree, and the sandbox cannot retrieve uncached npm packages. Therefore the normal 2i npm suite was not falsely reported as executed in this pass.

## Pre-existing warnings

Python compile emits two non-blocking `SyntaxWarning` messages in PubCast:

- `pubcast/modules/secure_secrets.py` — invalid escape sequence `\s`;
- `pubcast/modules/wired/pubcast_voxel_hollow_patch.py` — invalid escape sequence `\.`.

These are outside the Phase 02 change set and remain queued for the PubCast hardening pass.

## Current Phase 02 status

BACKEND HARDENING: VERIFIED BY STATIC + DYNAMIC LIFECYCLE TESTING
EDITOR/DOCUMENT PERSISTENCE: UNPROVEN — REQUIRED 2i FRONTEND/DOCUMENT SOURCE IS NOT IN THIS WORKING BUNDLE

## Next

Proceed to the durable 2i outbound queue, then federation tombstone semantics, conflict resolution, and PubPartner service-boundary hardening.


# 23 — PUBPARTNER / ITERATION WALLET DUAL-MODE DEVELOPMENT RULE

## Scope

This rule is specifically for the **two PubPartner / Iteration Wallet deployments** and
their relationship to standalone operation and PubCast-integrated operation. It is not a
general instruction to couple every subsystem in the project.

## Three-solution test

The proposed development models were evaluated as three alternatives:

### Solution A — Separate sequential workstreams

Finish standalone PubPartner / Iteration Wallet behavior first, then begin integrated
PubCast wiring.

**Result:** Rejected as the primary workflow.

Reason: it delays discovery of integration-specific failures and encourages a late-stage
adapter layer to be built against assumptions rather than the actual core behavior.

### Solution B — Integrated-only first

Optimize the systems around PubCast wiring first, then retrofit standalone operation.

**Result:** Rejected.

Reason: it risks host-dependent behavior, weakens independent usefulness, and can cause
standalone authority/lifecycle boundaries to become accidental dependencies on PubCast.

### Solution C — Shared core, separate boundaries, simultaneous development

Develop standalone correctness and integrated behavior concurrently, while keeping the
shared domain/core implementation independent from host-specific adapters, transport,
and lifecycle code.

**Result:** ACCEPTED.

This model gives early feedback from both operating modes without forcing the modes into
one runtime path. It also preserves the existing authority model: the same core behavior
is hardened once, while each deployment mode receives its own boundary and acceptance
tests.

## Resulting rule

> **For the two PubPartner / Iteration Wallet deployments: develop standalone and
> integrated behavior simultaneously, but keep the core shared and the deployment
> boundaries separate.**

The rule has four mandatory parts:

1. **Shared core:** persistence, synchronization, identity, memory authority, provider
   authority, and other domain behavior should be implemented once and remain independent
   of PubCast.
2. **Separate boundaries:** standalone transports/lifecycles and PubCast integration
   adapters may differ; they must not become competing authorities.
3. **Simultaneous development:** fixes that improve the shared core should be validated
   against both standalone and integrated use rather than waiting for one mode to finish
   before testing the other.
4. **Layered acceptance:** each mode keeps its own tests; shared-core tests prove common
   semantics; integration tests prove the adapter/host boundary.

## Practical model

```text
                    SHARED PUBPARTNER / ITERATION WALLET CORE
                                   |
                    +--------------+--------------+
                    |                             |
                    v                             v
          STANDALONE BOUNDARY             PUBCAST INTEGRATION
          / lifecycle / transport        adapter / lifecycle / transport
                    |                             |
                    v                             v
              standalone use                integrated use
```

The integrated path must never make standalone operation depend on PubCast.
The standalone path must never become a reason to duplicate core state or authority.

## Acceptance implication

For every shared-core change, ask two questions:

- Does it preserve standalone operation for the two PubPartner / Iteration Wallet
  deployments?
- Does it preserve the integrated PubCast path without introducing a second authority?

A change is not complete until both answers are verified at the appropriate test level.

## Decision

STATUS: **ACCEPTED / ARCHITECTURAL WORKFLOW RULE**

The rule should govern subsequent PubPartner / Iteration Wallet development unless
new executed evidence demonstrates that the boundary itself is inadequate.


# 22 — 2i Two-Round Self-Review / Hardening

## 2026-08-16 — Round 1: source-level review

Completed:

- Removed the redundant `rateLimitCleanupInterval` alias; shutdown now clears the single authoritative `rateLimitSweeper` interval.
- Corrected payload-size calculation to use UTF-8 byte length rather than JavaScript character count.
- Added per-request correlation IDs using `crypto.randomUUID()` and the `X-Request-Id` response header.
- Replaced the global error handler's use of the client IP as a fake request ID with the actual request correlation ID.
- Documented `RATE_LIMIT_WINDOW_MS` and `RATE_LIMIT_SWEEP_MS` in `.env.example`.
- Removed an unsafe test design that would have imported `server.js` into the test process and started an extra listener.
- Re-ran a TODO/stub/placeholder scan across the modified 2i backend area; no production placeholders were found.

## 2026-08-16 — Round 2: dynamic lifecycle attack

Executed against the actual `2i-backend/server.js` source under controlled dependency shims:

- startup;
- health request;
- request correlation header;
- SIGTERM shutdown;
- duplicate SIGTERM during shutdown;
- clean exit;
- clean shutdown logging.

RESULT: `DYNAMIC_LIFECYCLE_PASS`

Evidence record: `engineering/SELF_REVIEW_ROUND_1_2_2026-08-16.md`

Limitation:
The complete npm suite remains environment-blocked because the working bundle does not contain a complete installed dependency tree and the sandbox cannot reach the npm registry. The dynamic test validates the changed lifecycle behavior but does not replace full real-dependency execution.

STATUS: VERIFIED BY STATIC REVIEW + DYNAMIC LIFECYCLE TEST.
