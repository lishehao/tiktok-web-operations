# Thread Identity And Automation Ownership

Use this reference for every persistent coordinator/executor pair and every
heartbeat attached to a Thread. A title, focused window, project directory, or
old prompt is not identity proof.

## Immutable run registry

Create one registry before external work:

```text
run_id:
run_nonce:
coordinator_thread_id:
coordinator_title:
coordinator_host_id:
coordinator_project_or_cwd:
executor_thread_id:
executor_title:
executor_host_id:
execution_profile:
authority_envelope_hash_or_version:
ledger_path:
operation_stop_at:
automation_owner_thread_id:
heartbeat_automation_id: NONE | exact id
heartbeat_target_thread_id: NONE | exact id
operation_timer_state: NONE | ACTIVE | DEGRADED | COMPLETE
operation_timer_next_tick_at: NONE | timestamp
operation_timer_stop_at: NONE | timestamp
first_install_supervision_state: NOT_APPLICABLE | PENDING | ACTIVE | CONSUMED | DEGRADED
first_install_supervision_started_at: NONE | timestamp
first_install_supervision_ends_at: NONE | timestamp
first_install_supervision_checkpoints: NONE | timestamps
durable_install_state_path: NONE | local path outside managed Skill tree
identity_state: UNVERIFIED | VERIFIED | MISMATCH
pair_state:
```

The only authoritative identity sources are:

- starter/coordinator: unique nonce title resolved with `list_threads`, then
  confirmed with `read_thread` in the expected host/project/cwd context;
- executor: the exact ID returned by `create_thread`, confirmed by
  `read_thread` and the callback transport's `source_thread_id`;
- callback destination: the registered coordinator ID;
- heartbeat ownership: `targetThreadId` returned by an `automation_update` view
  of the exact automation ID.

Never derive identity from a directory suffix, copied URL, remembered ID,
focused Codex window, task ordering, matching title alone, another coordinator's
registry, or an automation prompt.

## Thread title contract

Keep final user-facing titles minimal:

```text
主控台
执行器
```

Because these final titles are intentionally non-unique, never use them to
discover identity. For starter self-registration, temporarily rename the task to
`主控台注册 · <run_nonce>`, resolve and verify the exact Thread ID, store that ID
in the registry, then set the final title to `主控台`. The executor identity is
the exact ID returned by `create_thread`; set its final title to `执行器` only
after recording that ID.

Keep account, platform, run ID, model, duration, status, version, and strategy in
the immutable registry or description, not the title. After final naming, do not
rename either task for routine state changes. A matching final title is never
identity or ownership proof.

## Pair state machine

Use one state at a time:

```text
BOOTSTRAP_NO_ID
  -> COORDINATOR_VERIFIED
  -> EXECUTOR_CREATED
  -> PAIR_READY
  -> ROUND_RUNNING
  -> ROUND_COMPLETE -> ROUND_RUNNING
  -> STOPPING -> IDLE
  -> RETIRED

Any identity or automation mismatch -> IDENTITY_BLOCKED
Any domain blocker -> BLOCKED_OR_WAITING
```

Before every thread dispatch, callback reconciliation, heartbeat creation,
heartbeat update, heartbeat execution, stop request, replacement, or archive:

1. Re-read the immutable registry.
2. Resolve the exact relevant task with `read_thread`.
3. Compare actual tool target/source with the registered ID.
4. Continue only when the values match byte-for-byte.

Do not repair an identity mismatch by guessing another target or by reusing a
similar task title.

## Automation owner invariant

A Thread-owned heartbeat must be created from and attached to its own verified
coordinator Thread:

```text
automation_owner_thread_id == heartbeat_target_thread_id == coordinator_thread_id
```

The executor never creates, updates, deletes, inherits, or owns a heartbeat. A
bootstrap, installer, Skill-development task, sibling coordinator, or external
supervisor must not create a heartbeat on behalf of the operating coordinator.
Send an instruction to the registered coordinator and let that coordinator
create its own heartbeat.

## Heartbeat creation transaction

Only create a heartbeat when the user requested proactive timed continuation,
callbacks are unreliable, or a domain Skill explicitly authorizes an unattended
time-bounded run.

A domain may define every multi-round duration as timer-authorized. In that
case, create one durable coordinator-owned timer after pair readiness, reuse the
same logical automation throughout the run, and never create per-round timers.

1. Require `identity_state=VERIFIED` and `pair_state=PAIR_READY` or
   `ROUND_COMPLETE`.
2. Set `automation_owner_thread_id` to the exact coordinator ID.
3. Inspect existing automations. Reuse only one whose stored
   `target_thread_id`, `run_id`, purpose/lane, and owner all match. Never update
   a similarly named automation attached to another Thread.
4. Create the heartbeat with explicit `targetThreadId=coordinator_thread_id`
   when the tool exposes that field. Include `run_id` and a short nonce in the
   name and stable prompt.
5. Record the returned automation ID, then immediately call automation view on
   that exact ID.
6. Require the readback to match kind, status, name, run ID, and
   `targetThreadId`. Store the ID and target only after this proof.
7. If readback is missing or mismatched, mark `AUTOMATION_TARGET_MISMATCH`,
   disable continuation, and do not dispatch external work from that heartbeat.

If the current transaction itself created a misbound heartbeat and no firing is
possible or in flight, delete that exact automation immediately and report the
failed transaction. Never delete or retarget a pre-existing automation with a
different owner; report it to the user or its verified owner.

## Heartbeat update and deletion

Before update or deletion, view the exact automation ID and verify:

- `targetThreadId == coordinator_thread_id`;
- stored `run_id` and purpose match the registry;
- the current Thread is the verified coordinator/owner;
- no replacement automation transaction is in flight.

If any check fails, do not mutate the automation. Return
`AUTOMATION_OWNERSHIP_MISMATCH` with expected and actual IDs.

When updating, preserve stable fields and change only cadence, active watchlist,
notification policy, or stop time authorized by the user/domain envelope. When
the run retires, the verified coordinator deletes or pauses only its registered
heartbeat and clears the automation fields from its registry.

## Heartbeat firing gate

On every wakeup, the coordinator must verify its identity again before reading
or dispatching:

1. The waking Thread ID equals `heartbeat_target_thread_id` and
   `coordinator_thread_id`.
2. The automation ID equals the registered heartbeat ID.
3. The active executor ID, run ID, account/project, authority envelope, and stop
   time match the registry.
4. The executor is idle and the prior block has a terminal callback.
5. The circuit is closed and the stop time has not passed.

If the wakeup lands in the wrong Thread, do not forward it, operate the external
system, dispatch the executor, or adopt that automation. Report
`MISBOUND_HEARTBEAT_NO_ACTION` and stop.

## Callback identity gate

Accept a worker callback only when all of these match:

- transport `source_thread_id == executor_thread_id`;
- payload coordinator/executor IDs match the registry;
- payload run ID and ledger match the registry;
- callback target is the exact coordinator ID;
- the reported block ID is the currently running block.

A callback received by a Skill-development, bootstrap, sibling, or historical
Thread is misrouted evidence, not permission for that Thread to coordinate the
run.
