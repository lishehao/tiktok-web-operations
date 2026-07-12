# Canonical Assignment And Versioned Envelopes

Natural-language prompts are transport, never canonical state. Use exact JSON
bytes and references for persistent task assignment.

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
bytes or references; they never ask a model to recreate identity/authority.

## Launcher/self-owned executor objects

Before creation use `executor_bootstrap/v1` containing only run ID, role,
execution profile, and `external_work=forbidden_until_assignment_acceptance`.
After `create_thread` returns exact ID, create `executor_assignment/v1` with:

- assignment/run/executor IDs and structured role;
- execution profile and exact account;
- `direction_ref`, `authority_ref`, `mission_ref`;
- ledger path, dedicated resource policy, self-owned automation policy;
- `launcher_contact_policy=NO_CALLBACK_NO_SUPERVISION`.

The executor validates bytes/hash/its exact ID and records
`ASSIGNMENT_ACCEPTED`. No callback target, coordinator identity, supervisor
timer, or launcher-owned mutable state belongs in this schema.

When a domain requires a profile lock, `direction_ref` may be created only from
the exact canonical proposal whose state is `CONFIRMED`. Draft/proposed profile
objects, defaults not shown to the user, or remembered prior-run profiles cannot
enter an assignment.

For `fresh_only_dispatch`, `run_id` is newly generated for every launch and
`executor_thread_id` must equal the exact ID newly returned by that launch's
single create call. No historical registry/mission/authority/ledger/timer/tab or
same-title task is an input. If no exact new ID was returned, no assignment
object may be created and no historical ID may be substituted.

The same launcher may perform multiple independent fresh-only dispatches across
user turns. Each dispatch has a distinct run ID, assignment ID, executor ID, and
canonical object set. No field points back to a prior run, and no worker return
or result becomes launcher input.

Direction, authority, and mission are independently versioned. The executor is
their sole writer after acceptance, applying new user instructions at safe
boundaries. Mutable progress, timer ID, next wake, resume cursor, lane state,
and finalization state stay in its runtime ledger, not immutable assignment.

## Coordinator-worker objects

Domains explicitly selecting `coordinator_worker` may define a separate
identity registry with coordinator and callback fields. Never import those
fields into a domain declaring `launcher_self_owned_executor`.

## Reconciliation

Before external work compare exact executor ID, role, execution profile, and all
refs. Any mismatch is `ASSIGNMENT_RECONCILIATION_REQUIRED`; perform no external
work or mutation. One bounded resend of the same stored bytes is allowed only
when no uncertain submission or mixed assignment exists.
