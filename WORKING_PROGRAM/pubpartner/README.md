# PubPartner Federation v0.2 — Continuation Build

This directory is the current federation implementation carried forward from the 2026-08-16 build session.

## Current verified state

The exact test suite contained in this directory was run during packaging: **14 passed**.

The earlier development transcript reported a larger 33-test run. Those additional test files are not present in this canonical copy, so that historical claim is not treated as current bundled evidence.

## Included

- persistent portable/resident node identity
- vector-clock offline-first synchronization
- field-level concurrent merge/conflict handling
- idempotent change application
- FastAPI HTTP service
- manuscript commit/retrieval contract
- memory candidate capture/list/promote flow
- configurable bearer authentication
- SQLite concurrency hardening
- sync and service tests

## Run

    python -m pytest -q

## Next integration target

The next proof is the real Node/2i backend -> resident PubPartner manuscript commit path, followed by a live portable/resident HTTP sync round-trip.

Do not modify the archived baseline or reference copies in the parent continuity bundle.

---

## Configuration reference

Added 2026-08-16. Every variable below is read by the running code; none were
previously documented. Nothing above this line has been edited.

| Variable | Default | Effect |
|---|---|---|
| `PP_DATA_DIR` | `./data` | Directory holding `identity.json`, `sync.db`, `memory.db`. One node per directory. |
| `PP_ROLE` | `resident` | `resident` or `portable`. Recorded in `identity.json` on first start and **cannot be changed afterwards** — starting an existing node under a different role is refused rather than silently relabelled. |
| `PP_NODE_ID` | generated | Node id used only when creating a new identity. Ignored once `identity.json` exists; the persisted id always wins. |
| `PP_HOST` | `127.0.0.1` | Bind address when run via `python -m pubpartner_federation.service`. |
| `PP_PORT` | `8000` | Bind port for the same. |
| `PP_API_KEY` | unset | When set, every endpoint except `/health` requires `Authorization: Bearer <key>`. Unset means no authentication at all — `/health` returning `auth_configured: false` is the way to check. |
| `PP_PEER_API_KEY` | unset | Credential this node presents **to** a peer during `/api/sync/trigger`. When unset the caller's own inbound `Authorization` header is forwarded instead, which assumes one federation-wide secret and hands this node's inbound credential to whatever host the caller named. Set it whenever peers do not share a single key. |
| `PP_PEER_URL` | unset | Default peer for `/api/sync/trigger` when the request body omits `peer_url`. |

### Federation topology

Synchronization is **direct-peer, not gossip**. A node republishes only the
changes it authored; changes received from a peer are applied and deduplicated
but are not re-exported. A third node must therefore sync against each author
directly — chaining A → B → C does not carry A's work to C. This is asserted by
`test_changes_received_from_a_peer_are_not_re_exported` in the integration
laboratory, so if the property ever changes that test will say so.
