# PubPartner Federation v0.1

This is the first implementation slice of the revised architecture:

    Portable PubPartner + 2i
              |
              | bidirectional sync
              v
    Resident PubPartner + 2i
              |
            PubCast
              |
          Foresight

## Rules

1. Portable and resident deployments share one logical sync protocol.
2. Synchronize canonical PubPartner entities, never raw databases.
3. Sync is bidirectional and offline-first.
4. Delivery is idempotent.
5. Concurrent changes are detected with vector clocks.
6. Disjoint concurrent fields merge.
7. Same-field concurrent writes become explicit conflicts.
8. Deletes use tombstones.
9. 2i remains manuscript authority.
10. PubPartner remains partner/communication authority.
11. PubCast remains host/orchestration authority.

## First entity classes

- partner profile / identity state
- durable partner memories
- explicit user preferences
- conversation/session continuity
- approved guidance/configuration
- provenance and synchronization metadata

Do not initially synchronize raw `.2i` documents, provider credentials,
browser implementation state, ephemeral UI state, unreviewed affect inferences,
internal SQLite pages, or provider caches.

## Integration boundary

The existing 2i -> PubPartner communication path remains the application
communication boundary. Federation sits above canonical PubPartner state and
does not replace PubPartner's existing MemoryCore, Alex/Jeremy bridge,
provider dispatcher, or lifecycle.

The first production transport should be HTTP request/response. WebSocket/event
streaming can later improve propagation latency without becoming required for
correctness.

## Current status

Implemented here:

- durable sync store
- vector clocks
- idempotent changes
- offline bidirectional synchronization
- safe disjoint-field merge
- explicit conflict recording
- tombstone deletion
- capability envelopes
- regression tests

This slice is deliberately non-destructive: it does not alter the existing
PubPartner, 2i, or PubCast source trees. The next source-level pass should
mount this engine behind PubPartner's canonical runtime.
