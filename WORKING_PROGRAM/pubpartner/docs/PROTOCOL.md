# PubPartner Sync Protocol 0.1

## Envelope

```json
{
  "protocol": "pubpartner-sync/0.1",
  "sender_node": "travel-001",
  "changes": [],
  "cursor": {"version": {"travel-001": 12}},
  "capabilities": [
    "entity-sync",
    "vector-clocks",
    "idempotency",
    "conflict-recording",
    "tombstones"
  ],
  "conflicts": []
}
```

## Change

```json
{
  "change_id": "sha256...",
  "node_id": "travel-001",
  "entity_type": "preference",
  "entity_id": "tone",
  "fields": {"value": "direct"},
  "version": {"travel-001": 12},
  "deleted": false
}
```

## Conflict policy

- remote dominates local: apply remote
- local dominates remote: ignore remote
- concurrent:
  - disjoint fields: merge
  - same field differs: record conflict, preserve local
  - delete vs update: record conflict

Wall-clock time is not authoritative.

Authentication, encryption, enrollment, and device authorization belong to
the deployment security layer. A content hash is not authentication.
