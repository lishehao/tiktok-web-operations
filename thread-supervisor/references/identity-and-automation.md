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
coordinator_pinned: true | false
executor_pinned: true | false
archive_temporary_on_complete: true | false
archive_retired_executor_after_release: true | false
execution_profile:
authority_envelope_hash_or_version:
ledger_path:
operation_stop_at:
automation_manager_thread_id:
automation_topology: coordinator_tick | coordinator_managed_worker_tick
heartbeat_automation_id: NONE | exact id
heartbeat_target_thread_id: NONE | exact id
operation_heartbeat_automation_id: NONE | exact id
operation_heartbeat_target_thread_id: NONE | exact executor id
operation_heartbeat_repeat: NONE | ON | OFF
operation_heartbeat_next_tick_at: NONE | timestamp
supervisor_heartbeat_automation_id: NONE | exact id
supervisor_heartbeat_target_thread_id: NONE | exact coordinator id
supervisor_heartbeat_repeat: NONE | ON | OFF
supervisor_heartbeat_next_tick_at: NONE | timestamp
operation_timer_state: NONE | ACTIVE | DEGRADED | COMPLETE
operation_timer_next_tick_at: NONE | timestamp
operation_timer_next_purpose: NONE | short bounded purpose
operation_timer_stop_at: NONE | timestamp
heartbeat_receipt_policy: silent_unless_event | always_three_lines
run_terminal_state: RUNNING | STOP_REQUESTED | EXECUTOR_RELEASED | RUN_COMPLETED | RUN_FINALIZATION_BLOCKED
run_completion_reason: NONE | deadline_reached | user_stopped | objective_complete | terminal_risk | cancelled
executor_release_state: NONE | STOPPED_AND_RELEASED | RELEASE_UNVERIFIED
final_callback_id: NONE | exact callback id
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
- automation management: the verified coordinator recorded as manager plus
  `targetThreadId`, repeat state, next run, and cutoff returned by an
  `automation_update` view of each exact automation ID.

Never derive identity from a directory suffix, copied URL, remembered ID,
focused Codex window, task ordering, matching title alone, another coordinator's
registry, or an automation prompt.

## Thread presentation contract

The calling domain supplies final titles and lifecycle policy. Use these generic
defaults only when no domain values exist:

```text
coordinator_title = 主控台
executor_title = 执行器
coordinator_pinned = false
executor_pinned = false
```

Final titles may collide and must never be used to discover identity. For starter
self-registration, temporarily rename the task to
`<coordinator_title>注册 · <run_nonce>`, resolve and verify the exact Thread ID,
store that ID in the registry, then set `coordinator_title` and its pin state.
The executor identity is the exact ID returned by `create_thread`; set
`executor_title` and its pin state only after recording that ID.

Keep account, platform, run ID, model, duration, status, version, and strategy in
the immutable registry or description, not the title. After final naming, do not
rename either task for routine state changes. A matching final title is never
identity or ownership proof.

Pinning is presentation state, not ownership proof. Never archive an active task,
a task with an owned heartbeat or tab, or a task with unresolved external-action
certainty. A domain may keep registered idle workers unarchived for reuse and
archive only completed temporary diagnostics or released, retired workers.

## Pair state machine

Use one state at a time:

```text
BOOTSTRAP_NO_ID
  -> COORDINATOR_VERIFIED
  -> EXECUTOR_CREATED
  -> PAIR_READY
  -> ROUND_RUNNING
  -> ROUND_COMPLETE -> ROUND_RUNNING
  -> STOPPING
  -> EXECUTOR_RELEASED
  -> RUN_COMPLETED -> IDLE
  -> RETIRED

Any identity or automation mismatch -> IDENTITY_BLOCKED
Any domain blocker -> BLOCKED_OR_WAITING
Missing final release proof -> RUN_FINALIZATION_BLOCKED
```

`ROUND_COMPLETE` means one bounded round ended; it is never whole-run
completion. A heartbeat tick is only a time signal. Declare `RUN_COMPLETED` only
after a terminal executor callback proves release, final evidence is reconciled,
and the coordinator has retired its managed run heartbeat(s).

Before every thread dispatch, callback reconciliation, heartbeat creation,
heartbeat update, heartbeat execution, stop request, replacement, or archive:

1. Re-read the immutable registry.
2. Resolve the exact relevant task with `read_thread`.
3. Compare actual tool target/source with the registered ID.
4. Continue only when the values match byte-for-byte.

Do not repair an identity mismatch by guessing another target or by reusing a
similar task title.

## Automation manager invariant

Every run heartbeat is created, updated, paused, and deleted only by the exact
verified coordinator:

```text
automation_manager_thread_id == coordinator_thread_id
```

The target depends on the calling domain's declared topology:

```text
coordinator_tick:
  heartbeat_target_thread_id == coordinator_thread_id

coordinator_managed_worker_tick:
  operation_heartbeat_target_thread_id == executor_thread_id
  supervisor_heartbeat_target_thread_id == coordinator_thread_id
```

In the second topology the operation heartbeat may wake the executor, but this
does not give the executor ownership. The executor never creates, updates,
renews, pauses, deletes, inherits, or retargets an automation. A bootstrap,
installer, Skill-development task, sibling coordinator, or external supervisor
must not manage the operating coordinator's automations.

## Heartbeat creation transaction

Only create a heartbeat when the user requested proactive timed continuation,
callbacks are unreliable, or a domain Skill explicitly authorizes an unattended
time-bounded run.

A domain may define every multi-round duration as timer-authorized. It must also
declare one supported topology. `coordinator_tick` uses one durable coordinator-
target timer. `coordinator_managed_worker_tick` uses one repeat-on operation
heartbeat targeting the executor and one lower-frequency repeat-on supervisor
heartbeat targeting the coordinator. Neither topology may use per-round
automations or `COUNT=1` followed by worker self-renewal.

1. Require `identity_state=VERIFIED` and `pair_state=PAIR_READY` or
   `ROUND_COMPLETE`.
2. Set `automation_manager_thread_id` to the exact coordinator ID.
3. Inspect existing automations. Reuse only one whose stored
   `target_thread_id`, `run_id`, purpose/lane, and manager all match. Never update
   a similarly named automation attached to another Thread.
4. Create the required heartbeat(s) with explicit target(s) from the declared
   topology. For worker-tick operation require `targetThreadId=executor_thread_id`;
   for supervisor require `targetThreadId=coordinator_thread_id`. Include `run_id`
   and a short role nonce in each name/prompt.
5. Record each returned automation ID, then immediately call automation view on
   each exact ID.
6. Require every readback to match kind, status, name, run ID, target, repeat-on
   state when required, next run, local/UTC schedule, and finite cutoff. Store
   IDs/targets only after this proof.
7. If readback is missing or mismatched, mark `AUTOMATION_TARGET_MISMATCH`,
   disable continuation, and do not dispatch external work from that heartbeat.

If the current transaction itself created a misbound heartbeat and no firing is
possible or in flight, delete that exact automation immediately and report the
failed transaction. Never delete or retarget a pre-existing automation with a
different manager; report it to the user or its verified manager.

## Heartbeat update and deletion

Before update or deletion, view the exact automation ID and verify:

- `targetThreadId` equals the registered target for that automation role;
- stored `run_id` and purpose match the registry;
- the current Thread is the verified coordinator/manager;
- no replacement automation transaction is in flight.

If any check fails, do not mutate the automation. Return
`AUTOMATION_OWNERSHIP_MISMATCH` with expected and actual IDs.

When updating, preserve stable fields and change only cadence, active watchlist,
notification policy, or stop time authorized by the user/domain envelope. When
the run retires, the verified coordinator deletes or pauses only its registered
heartbeat and clears the automation fields from its registry.

## Heartbeat firing gate

On every wakeup, the target Thread must verify its identity and automation role
before reading or acting:

1. For coordinator tick/supervisor wake, the waking Thread equals the registered
   coordinator target. For operation wake, it equals the registered executor
   target.
2. The automation ID equals the registered ID for that role.
3. The active executor ID, run ID, account/project, authority envelope, and stop
   time match the registry.
4. The executor is idle and the prior block has a terminal callback.
5. The circuit is closed and the stop time has not passed.

If the wakeup lands in the wrong Thread, do not forward it, operate the external
system, dispatch the executor, or adopt that automation. Report
`MISBOUND_HEARTBEAT_NO_ACTION` and stop.

## Heartbeat receipt transaction

The calling domain selects `heartbeat_receipt_policy`. Keep
`silent_unless_event` as the generic default; use `always_three_lines` only when
the domain or user explicitly requires a visible receipt for every valid tick.

For `always_three_lines`, after each valid coordinator/supervisor heartbeat:

1. Reconcile work completed since the previous tick and choose at most one next
   bounded action. If the executor is still running, the next action is to wait
   for its callback; never overlap it.
2. Compute the next relevant tick as the earlier of the useful cadence and
   `operation_stop_at`. View all registered run heartbeat(s), and require their
   readback schedule/target/ID/repeat/cutoff to match. Update only when the
   calling domain's cadence or operation template actually changed.
3. Only after successful readback, store `operation_timer_next_tick_at` and
   `operation_timer_next_purpose`, then emit exactly three concise lines in the
   coordinator Thread:

```text
本轮完成：<one sentence>
下次心跳：<YYYY-MM-DD HH:mm timezone>
下轮计划：<one bounded purpose>
```

Use the user's local timezone and include the date. Never display an inferred or
unverified schedule. If update/readback fails, use
`下次心跳：未建立（调度校验失败）` and set the plan to safe pause/repair.

At the final tick use `下次心跳：无（进入终止结算）`; at `RUN_COMPLETED` use
`下次心跳：无（任务已完成）`; while waiting for a user decision, report the
verified next safety/deadline tick when one remains, otherwise use
`无（等待你的决定）`. Heartbeat IDs, registry fields, and internal state names
remain hidden.

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

## Whole-run completion transaction

When the deadline is reached, the user stops, or the authorized objective is
complete:

1. The verified coordinator sets `run_terminal_state=STOP_REQUESTED`, records one
   completion reason, and dispatches no further ordinary work.
2. Send one terminal `STOP_AND_RELEASE` or domain-equivalent message to the exact
   executor ID, even when the executor appears idle. It must add no new external
   action; it only resolves submission certainty, releases owned resources,
   appends a final ledger checkpoint, and returns one terminal callback.
3. Accept that callback only through the normal identity gate. Require
   `terminal_event=EXECUTOR_RELEASED`, `release_state=STOPPED_AND_RELEASED`, final
   cumulative evidence, and no unresolved external action.
4. Set `run_terminal_state=EXECUTOR_RELEASED`, then verify and delete/pause only
   every coordinator-managed run heartbeat. Mark `operation_timer_state=COMPLETE`.
5. Reconcile the final ledger/counters and set `run_terminal_state=RUN_COMPLETED`.
   The coordinator then emits one user-facing completion summary in its own
   Thread. It never callbacks a bootstrap or Skill-development Thread.

If the executor is missing, the callback identity fails, release is unverified,
or submission certainty is unresolved, set `RUN_FINALIZATION_BLOCKED`. Do not
claim completion or delete evidence merely because the deadline or a heartbeat
arrived.
