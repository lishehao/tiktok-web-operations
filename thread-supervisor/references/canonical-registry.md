# Canonical Registry And Versioned Envelopes

Use this reference whenever a persistent coordinator/executor pair must compare
identity, authority, mission, or callback data across Threads. Natural-language
prompts are transport; they are never the canonical value.

## Two-phase bootstrap

An executor Thread ID does not exist until `create_thread` returns, so a complete
run registry cannot truthfully be frozen before creation. Use two distinct
objects and never pretend they are one:

1. Before `create_thread`, write one canonical `bootstrap_envelope`. It contains
   only the verified coordinator identity, run identity, required execution
   profile, schema, and the inert instruction to wait. The create prompt embeds
   this exact serialized object once and must not restate its fields in prose.
2. After `create_thread` returns the exact executor ID, create one canonical
   `identity_registry` generation. Send its exact bytes once in `SELF_REGISTRY`.
   The executor stores those bytes, recomputes the hash, and returns
   `THREAD_READY` with the exact registry reference.
3. Every later dispatch, callback, heartbeat prompt, and stop transaction carries
   only references to the accepted canonical objects plus its bounded payload.
   Never reconstruct identity, role, model, authority, or direction as prose.

The create prompt may explain how to parse the delimited canonical JSON, but it
must not contain a second independently written registry snapshot. The executor
does no Chrome, platform, ledger, or automation work before `THREAD_READY` is
accepted by the coordinator.

## Canonical serialization

All canonical objects use this exact algorithm:

```text
encoding: UTF-8
format: JSON
object keys: lexicographically sorted at every depth
array order: preserved exactly
whitespace: none outside JSON string values
separators: ',' and ':'
unicode: literal UTF-8, not ASCII escaping
numbers: JSON numbers only; timestamps and IDs are strings
hash: lowercase SHA-256 hex of the exact UTF-8 bytes
```

Equivalent Python is:

```python
payload = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
sha256 = hashlib.sha256(payload).hexdigest()
```

Write the bytes once to a private coordinator-side path outside either managed
Skill tree. Record the path, schema, object ID, version/generation, byte length,
and SHA-256 in the run ledger. Later messages copy the stored bytes or carry the
reference; they do not call a model to regenerate the object. Compare hashes
first and exact bytes when both sides expose them.

Every reference has this shape:

```json
{"id":"<object id>","schema":"<schema>","sha256":"<64 lowercase hex>","version":1}
```

## Object split

### Bootstrap envelope

Schema `thread_bootstrap/v1`:

```json
{
  "bootstrap_id":"<unique id>",
  "coordinator":{"host_id":"<host>","thread_id":"<exact id>"},
  "execution_profile":{"model":"gpt-5.6-luna","thinking":"high"},
  "external_work":"forbidden_until_registry_ack",
  "run_id":"<unique run id>",
  "run_nonce":"<unique nonce>",
  "schema":"thread_bootstrap/v1"
}
```

Role descriptions, mutation authorization, direction prose, ledger paths, and
an executor ID do not belong here.

### Identity registry

Schema `thread_identity_registry/v1`. This is immutable for one
`registry_generation`:

```json
{
  "account":{"handle":"@handle","platform":"tiktok"},
  "automation_manager_thread_id":"<coordinator id>",
  "callback_target_thread_id":"<coordinator id>",
  "coordinator":{"host_id":"<host>","role_code":"TIKTOK_COORDINATOR","thread_id":"<exact id>"},
  "dedicated_tab_policy":"EXECUTOR_OWNED_TAB_PER_BLOCK",
  "execution_profile":{"model":"gpt-5.6-luna","thinking":"high"},
  "executor":{"generation":1,"host_id":"<host>","role_code":"TIKTOK_EXECUTOR","thread_id":"<exact id>"},
  "ledger_path":"<private absolute path>",
  "registry_generation":1,
  "registry_id":"<unique id>",
  "run_id":"<unique run id>",
  "run_nonce":"<unique nonce>",
  "schema":"thread_identity_registry/v1",
  "writer_policy":"EXECUTOR_SOLE_RUN_LEDGER_AND_MUTATION_WRITER"
}
```

Use enums such as `TIKTOK_EXECUTOR`; do not make prose role descriptions an
equality boundary. A real executor replacement creates a new registry generation
and hash. It never edits the accepted generation in place.

### Versioned operating objects

Direction, authorization, user instruction, capability state, stop time,
round/mission parameters, progress/resume state, Heartbeat IDs/next-run state,
owner state, and release
state can change. They do not belong in the immutable identity registry.

Store them as separate objects:

- `direction_profile/v1`: structured audience, region/language, pillars,
  exclusions, voice, and future-post alignment; versioned and hashed.
- `authority_envelope/v1`: per-action booleans/states and safety limits;
  versioned and hashed. Do not use one prose `mutation_authorization` string.
- `mission_instruction/v1`: instruction version, direction reference, authority
  reference, operation stop time, and the current high-level objective.
- `block_dispatch/v1` for bounded-round domains: block/slot ID, trigger,
  parameters, capability snapshot reference, callback schema version, and the
  canonical references needed for the block.
- `mission_dispatch/v2` for continuous-resumable domains: mission generation,
  trigger/resume cursor, logical sample thresholds, capability/lane snapshot,
  callback schema version, and the canonical references needed to resume the
  same mission without duplicating work.
- mutable runtime state: owner liveness, retired/replacement IDs, heartbeat IDs,
  targets/repeat/next-run, round slot or mission progress/resume state, circuit
  state, and finalization evidence.

A user change creates a new direction, authority, or mission version and hash.
The coordinator sends one `VERSION_COMMIT` transaction; the executor acknowledges
the new references before the next safe work boundary. A changed authorization value must not
be disguised as a registry repair. Older versions remain append-only evidence.

Every dispatch contains, at minimum:

```json
{
  "authority_ref":{"id":"...","schema":"authority_envelope/v1","sha256":"...","version":1},
  "block_id":"...",
  "direction_ref":{"id":"...","schema":"direction_profile/v1","sha256":"...","version":1},
  "mission_ref":{"id":"...","schema":"mission_instruction/v1","sha256":"...","version":1},
  "registry_ref":{"id":"...","schema":"thread_identity_registry/v1","sha256":"...","version":1},
  "schema":"block_dispatch/v1"
}
```

The bounded block payload may add query/sample/action fields, but it must not
repeat canonical values as hand-written prose. The executor checks the four
references and the current accepted versions before Chrome connection. A
callback echoes the same references.

## Validation outcomes

- Same structured value with different input key order canonicalizes to the same
  bytes and hash: accept.
- Same meaning expressed with different prose is irrelevant when a structured
  enum/object is canonical: do not compare the prose.
- Different structured authorization, direction, model, ID, account, ledger, or
  stop value produces a different hash: require the correct version transaction
  or stop before external work.
- Wrong `execution_profile` is `REGISTRY_PROFILE_MISMATCH`; do not silently
  substitute a model.
- Unknown/mismatched reference is `registry_mismatch`; do not connect Chrome.
- Exact accepted references plus a valid bounded payload allow the block gate to
  continue.

## Registry reconciliation

`registry_mismatch` is a safe stop, not an invitation to keep rewriting prompts.
Run exactly one `REGISTRY_RECONCILIATION` transaction before any external work:

1. Freeze dispatch and verify that no Chrome tab, platform action, uncertain
   submission, or heartbeat was created for the unaccepted registry.
2. Read the stored bootstrap bytes, coordinator registry artifact, executor
   `THREAD_READY` reference, and disputed dispatch reference. Compare schema,
   ID, version/generation, hash, and exact bytes where available.
3. If one accepted canonical registry exists and only the dispatch reference is
   wrong, resend the same bounded block once with the stored accepted references.
   Do not rewrite or summarize any canonical object.
4. If no canonical artifact exists, create/SELF snapshots disagree, the executor
   accepted mixed values, or the source cannot be proven, classify
   `REGISTRY_BOOTSTRAP_CONTAMINATION`. Do not guess which prose snapshot wins.
5. View and stop/remove only automations exactly bound to this run and executor.
   Pre-proof bootstrap should normally have none. Confirm zero external work and
   retire the contaminated executor ID.
6. The verified coordinator may create at most one clean replacement executor
   for the same run/authority without user confirmation. Create a new registry
   generation from structured source values, send one exact `SELF_REGISTRY`,
   require matching `THREAD_READY`, then retry the pending smoke once.
7. Record old/new executor IDs, old/new registry references, reconciliation
   reason, automation cleanup, replacement count, and smoke result. Require one
   canonical live executor and zero old-target automations.
8. If reconciliation or the one clean replacement fails, stop with
   `ORCHESTRATION_REGISTRY_BLOCKER` and report it only through the coordinator.

Do not reuse a contaminated executor, send alternating snapshots, weaken hash
checks, create parallel executors, create a heartbeat before proof, or interpret
this as Chrome/TikTok/account enforcement.

## Audit requirements

Before an external block, require all of the following:

- one stored bootstrap reference and one accepted identity-registry reference;
- create prompt contains no second prose registry;
- `SELF_REGISTRY` bytes hash to the stored identity reference;
- `THREAD_READY` source is the registered executor and echoes the same reference;
- execution profile is exactly the required supported profile;
- current direction/authority/mission references are accepted;
- dispatch carries references rather than re-rendered immutable prose;
- callback target equals the canonical coordinator ID;
- replacement count is zero or one, never more;
- no automation exists before smoke plus first real block proof.
