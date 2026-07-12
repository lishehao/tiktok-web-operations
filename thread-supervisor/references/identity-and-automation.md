# Thread Identity And Automation Ownership

A title, focused window, list/search result, directory, cached summary, or old
prompt is not task identity. Use the exact ID returned by `create_thread` and
exact tool readback.

## Launcher/self-owned executor state

Mutable state associated with `executor_assignment/v1`:

```text
launcher_title: TikTok 启动台 | DEGRADED_RENAME_UNAVAILABLE
launcher_state: PREFLIGHT | ASSIGNING | REUSABLE_IDLE
launcher_dispatch_sequence: monotonically increasing local count
pre_dispatch_gate_state: NONE | DRAFT | PROPOSED | CONFIRMED
pre_dispatch_gate_ref: NONE | exact canonical ref
dispatch_policy: FRESH_ONLY
fresh_create_attempts: 0 | 1
executor_thread_id:
executor_title: TikTok 执行台
executor_owner_state: NEW | ASSIGNMENT_ACCEPTED | ACTIVE | HARD_REPAIR | RELEASED
run_id:
assignment_ref:
direction_ref:
authority_ref:
mission_ref:
ledger_path:
automation_topology: self_owned_executor_tick
automation_manager_thread_id: exact executor id
executor_heartbeat_id:
executor_heartbeat_target_thread_id: exact executor id
executor_heartbeat_repeat: ON | OFF
executor_heartbeat_next_tick_at:
operation_stop_at:
resume_cursor:
run_terminal_state: RUNNING | STOP_REQUESTED | RUN_RELEASED
```

The launcher records only the current dispatch's immutable handoff provenance
until acceptance, then discards run working state and becomes `REUSABLE_IDLE`. It is
not a manager, callback target, replacement owner, or automation owner.

A later command creates a new run ID and executor. It never resolves, reads, or
inherits an earlier executor. `launcher_dispatch_sequence` may distinguish
launcher invocations but is not a cross-run registry, watchlist, or result log.

A calling domain may require `pre_dispatch_gate_state=CONFIRMED` before creation.
Thread Supervisor validates the exact gate ref and exit proof; it never infers
confirmation from defaults, a draft, a historical profile, or a bare continue
without a visible proposal.

## Identity proof

- executor identity: exact ID returned by creation plus assignment acceptance;
- automation identity: exact automation ID and view readback;
- valid self wake:
  `waking_thread_id == targetThreadId == automation_manager_thread_id == executor_thread_id`;
- external tab/resource: handle created and recorded by this executor in the
  current control session.

Independent executors never list/read one another, inspect same-account state,
reuse titles as identity, or claim another resource/timer.

## Fresh-only creation failure

For a fresh-only launch, historical owner discovery and recovery do not exist.
Do not list, search, read, reuse, unarchive, revive, message, archive, replace,
or modify old executors, including same-title, archived, completed, stale, or
currently live tasks. They remain untouched history.

Make one fresh create attempt. If it fails or returns no exact new ID, record
`FRESH_TASK_CREATION_FAILED|UNKNOWN` and stop this launch. Do not probe task
lists, retry creation, create a replacement, or fall back to an old ID. If the
new exact task cannot accept assignment, record `FRESH_TASK_ASSIGNMENT_FAILED`
and stop without replacement. Owner-liveness/tombstone classification is not a
TikTok launcher path.

## Heartbeat ownership

In `self_owned_executor_tick`, the executor alone creates, views, updates,
replaces, and retires its timer. Require repeat-on and finite cutoff. Immediately
verify exact ID, target, repeat, next local/UTC run, and cutoff.

If already running, a wake does no overlap. Ordinary technical/lane failure
keeps the timer active. Uncertain submission is never retried. For a bad timer,
create/read back the replacement, switch stored binding, then retire the old
timer. Stop/deadline/completion begins finalization; retire only after external
resource release and ledger reconciliation.

Domains explicitly selecting coordinator-managed timers use their own contract;
they do not override a self-owned executor domain.
