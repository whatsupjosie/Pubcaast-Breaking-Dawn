# ENGINEERING RUN — 2026-08-16 (revision 3)

Supplement to `MASTER_BUILD_DOCUMENT_2026-08-16_v1_3.md`. Nothing in the bundle,
the Master Build Document, or the PubPartner README was altered — only appended
to. Revisions 1 and 2 are archived in `evidence/`, not deleted.

Environment: Ubuntu container, Node v22.22.2, npm 10.9.7, Python 3.12.3.
Bundle integrity: **719/719 files verified** against `00_HANDOFF/MANIFEST.sha256`.

```
PubPartner federation unit suite      14 passed
2i standalone suite (npm test)        16 passed / 0 failed
Cross-process integration laboratory  60 passed
PubCast own suite (pre-existing)      556 passed / 25 failed / 7 errors
```

---

## 00 — The two defects this debugging pass found in my own work

Both were introduced by my BUG-004 fix (making manuscript commits real deltas).
Both were invisible to the 55 tests that were green when I declared it fixed.
Both are silent data loss.

### BUG-013 — a partial patch erased every field it did not mention
**Severity: silent data loss on every replica.**

A `Change` carries a patch, not an entity. `apply()` handled the
"remote dominates local" branch with
`store.put(remote_to_entity(remote))`, which replaced the stored fields with
*only the patch fields*. This was harmless for as long as every commit submitted
the complete manuscript. The moment I made commits deltas, a peer editing one
field deleted the other six on every replica that received the change.

Observed directly:

```
P after first sync:  [character_names, content, message_id,
                      plot_elements, style_notes, timestamp, user_id]
R commits content only -> changed_fields: ['content']
P after second sync: [content, message_id, timestamp]
character_names: <<<GONE>>>   plot_elements: <<<GONE>>>
style_notes:     <<<GONE>>>   user_id:       <<<GONE>>>
```

**Fix:** merge the patch into local fields instead of replacing them, with the
tombstone case handled explicitly.
**Guarded by:** `test_dominating_partial_patch_must_not_erase_untouched_fields`,
`test_deep_chain_of_single_field_deltas_preserves_every_field`.

Why the suite missed it: every test exercised either entity *creation* (`local is
None`) or the *concurrent merge* branch. The dominating-patch branch — the most
common one in normal sequential replication — had no coverage at all.

### BUG-014 — a stale editor silently reverted a peer's edit, with no conflict
**Severity: silent data loss, and the exact failure BUG-004 was meant to fix.**

Computing the delta against *current stored state* is not sufficient. An editor
holds a whole document. If a peer changes a field the editor has not reloaded,
the editor's copy of that field still differs from stored state and is
indistinguishable from a deliberate revert.

Observed directly:

```
P edits plot_elements -> ['P-added'], replicated to R
R commits its stale document + one content edit
  changed_fields = ['content', 'plot_elements']   <-- plot_elements is stale, not authored
after 4 sync rounds: converged, 0 conflicts recorded
  R: plot_elements ['cold open']     P: plot_elements ['cold open']
```

Both replicas converged on the *wrong* value. P's work was destroyed with zero
conflicts recorded — a §21 violation.

**Fix:** the commit route accepts an optional `base_version` (the manuscript
version the client last saw). A submitted field whose stored field-version has
moved past that base changed underneath the client, so its value is stale rather
than authored: it is excluded from the patch and a
`stale_client_fields:<names>` conflict is recorded. Backward compatible — a
client that omits `base_version` gets the previous, unprotected behaviour, and
the response now always returns `version` so clients can supply it next time.
2i forwards the value verbatim and neither caches nor synthesises it, because 2i
does not hold manuscript authority.

After the fix:

```
status: committed  changed_fields: ['content']  stale_fields: ['plot_elements']
R: 'R new line' ['P-added']    P: 'R new line' ['P-added']    conflicts: 1
```

**Guarded by:** `test_stale_client_cannot_silently_revert_a_peers_edit`,
`test_base_version_does_not_block_a_deliberate_revert_by_the_same_author`,
`test_omitting_base_version_keeps_the_older_behaviour_and_says_so`,
and a 2i test that proves the pass-through against a recording partner.

---

## 01 — Other corrections made this pass

- **Response `version` was re-read from the store after the write.** Under a
  concurrent commit that re-read could return someone else's version, and a
  client echoing it back as `base_version` would claim to have seen work it
  never received. Now taken from the change itself.
- **Two assertions accepted a range of outcomes** (`status in (200, 400, 413,
  422)` and `(200, 401, 403)`). Both behaviours are deterministic. Pinned to the
  actual values so a change in behaviour fails loudly.
- **LWW provenance convergence was asserted, never tested.** Now verified across
  P→R only, R→P only, and bidirectional sync, over repeated rounds. It holds.

---

## 02 — Bug record

| ID | Summary | Class | Status |
|---|---|---|---|
| BUG-001 | 2i reported success on a broken partner response | implementation | FIXED |
| BUG-002 | Concurrent creation silently discarded an author's content | data integrity | FIXED |
| BUG-003 | Vector clock reset on every restart | implementation | FIXED |
| BUG-004 | Stale field resubmission blocked a peer's edit | integration | FIXED (completed by BUG-014) |
| BUG-005 | One shared rate-limit bucket per IP across all routes | implementation | FIXED |
| BUG-006 | Rate-limit store grew without bound | resource leak | FIXED |
| BUG-007 | Bearer comparison leaked the secret through timing | security | FIXED |
| BUG-008 | Sync forwarded the caller's credential to a peer | security | MITIGATED |
| BUG-009 | PubCast could not boot without audio hardware | runtime blocker | FIXED |
| BUG-010 | Non-ASCII auth header caused 500 instead of 401 | **mine** | FIXED |
| BUG-011 | Launch script and doctor disagreed on required dirs | implementation | FIXED |
| BUG-012 | Test suite required an undeclared dependency | test infra | FIXED |
| BUG-013 | Partial patch erased untouched fields | **mine, data loss** | FIXED |
| BUG-014 | Stale editor silently reverted a peer's edit | **mine, data loss** | FIXED |

Four of fourteen were mine. Three of those four were introduced while fixing
something else, which is the pattern worth watching.

---

## 03 — Open items

- **OPEN-001** — a conflict blocks the whole change, not just the conflicting
  field. Existing intentional design, left alone under §05.
- **OPEN-002** — 2i's `queued-locally` is not a queue. If PubPartner is
  unreachable the commit lives in in-memory history and dies with the process.
  Highest-value remaining correctness item on the proven path.
- **OPEN-003** — PubCast's own suite: 25 failures, 7 errors, pre-existing and
  unchanged by this session. The 7 errors are test-order pollution, not broken
  code (the file passes 7/7 in isolation; a corrupted `pathlib.Path` leaks out
  of earlier tests, reproducing with the second half of the alphabetical
  ordering but with no single file). Inventory in
  `evidence/pubcast_known_failures.txt`. Worth prioritising: 5 authorization-
  parity failures (security-relevant) and a websocket event-type contract
  mismatch (`presence` vs `production_state`).
- **OPEN-004** — there is no conflict *resolution* endpoint. Conflicts can be
  listed via `GET /api/sync/conflicts` but not resolved, so a genuine collision
  leaves the two replicas divergent with no supported way to settle it.
- **OPEN-005** — PubPartner enforces **no request-size limit**. It accepts and
  durably stores a 12MB manuscript body. 2i caps requests at 10MB, so the cap
  exists only for traffic routed through 2i; a direct client bypasses it. Pinned
  by `test_oversized_request_is_rejected_without_killing_the_node`, whose name is
  now aspirational and says so in a comment.
- **OPEN-006** — every sync envelope advertises a `tombstones` capability, but
  there are zero delete endpoints. `SyncEngine.delete()` is unreachable over
  HTTP, so a peer negotiating on that capability is being told something untrue.

---

## 04 — Acceptance gates (handoff §42)

```
2i standalone              WORKING              16 tests, real process
PubPartner standalone      WORKING              14 unit + real process
PubCast standalone         BOOTS                7 tests; 25 known internal failures

2i <-> PubPartner          FUNCTIONALLY PROVEN
resident <-> portable      FUNCTIONALLY PROVEN

PubCast + 2i               UNPROVEN
PubCast + PubPartner       COEXISTENCE ONLY     no hosting exercised
Foresight + PubCast        UNPROVEN             Foresight never opened
complete browser stack     UNPROVEN
```

---

## 05 — Next, in priority order

1. **Foresight.** Still untouched. `03_REFERENCE_MATERIAL/foresightv18.bundle`
   is a git bundle; unpacking it and identifying its entrypoint is the remaining
   Phase A work and the gate for Phases F and G.
2. **PubCast hosting.** The host boots and the services coexist. Attachment,
   capability discovery and shared `pubcast_session_id` are the Phase E
   substance and are not started.
3. **OPEN-002**, the durable local spool.
4. **OPEN-004**, conflict resolution — currently a collision is observable but
   unfixable.
5. **OPEN-003 triage**, starting with authorization parity.

---

## 06 — A note on method

Every defect in §00 was found by running the system and looking at what came
out, not by reading the code. The 55 tests that were green when I declared
BUG-004 fixed were green because they exercised the branches I had thought
about. The two branches I had not thought about — the dominating-patch path and
the stale-client path — were both silently destroying data.

A green suite is evidence about the paths it covers and nothing else.
