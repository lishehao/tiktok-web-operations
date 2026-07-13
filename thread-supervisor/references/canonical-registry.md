# Canonical Assignment And Versioned Envelopes

Natural-language prompts are transport, never canonical state. Use exact JSON
bytes and references for persistent task assignment and callback acceptance.

## Serialization

Canonical objects use UTF-8 JSON, recursively sorted keys, preserved array
order, no extra whitespace, literal Unicode, and lowercase SHA-256:

```python
payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
sha256 = hashlib.sha256(payload).hexdigest()
```

Reference shape:

```json
{"id":"<id>","schema":"<schema>","sha256":"<64 hex>","version":1}
```

Store exact bytes once outside managed Skill trees. Later messages copy stored
bytes or references; they never ask a model to recreate identity or authority.

## TikTok coordinator-worker objects

Create `executor_bootstrap/v2` with run ID, role, execution profile, exact main
task ID, and `external_work=forbidden_until_assignment_and_callback_acceptance`.

After fresh creation returns an exact ID, create `executor_assignment/v2` with:

- assignment/run/coordinator/executor IDs and execution profile;
- exact account, `direction_ref`, `authority_ref`, and `mission_ref`;
- coordinator/executor ledger paths and dedicated-tab policy;
- `callback_policy=ROUND_BOUNDARY_TO_EXACT_COORDINATOR`;
- `automation_policy=COORDINATOR_OWNED_FIXED_SCHEDULER`.

The executor validates bytes/hash/identity and records `ASSIGNMENT_ACCEPTED`.
External work remains forbidden until exact `CALLBACK_PING/v1` and
`CALLBACK_ACK/v1` proof succeeds.

Each `round_assignment/v1` includes run/round IDs, three clusters, exclusions,
view boundary, For You plan, action emphasis, authority ref, deadline, and
resume cursor. Each `round_callback/v1` includes exact IDs/sequence, status,
view/feed/action counts, cluster evidence, cursor, capability delta, blocker,
executor state, and ledger-tail ref.

The main task accepts a callback only when exact IDs, run, expected round,
schema, hash, and sender match. Duplicate, late, misbound, or out-of-sequence
callbacks perform no dispatch.

Direction, authority, and mission are independently versioned by the main task.
The executor never edits those objects; it reports observations. Mutable
strategy, cooldown, scheduler ID, and pending round stay in the main ledger.
Raw browser evidence and target/action deduplication stay in the executor ledger.

## Reconciliation

Before external work compare exact task IDs, role, execution profile, callback
target, and all refs. Any mismatch is `ASSIGNMENT_RECONCILIATION_REQUIRED` and
permits no external work. One bounded resend of the same stored bytes is allowed
only when no mixed assignment or uncertain submission exists.
