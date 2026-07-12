# Thread Identity And Automation Ownership

A title, focused window, list/search result, directory, cached summary, or old
prompt is not task identity. Use the exact ID returned by `create_thread` and
exact tool readback.

## Launcher/self-owned executor state

Mutable state associated with `executor_assignment/v1`:

```text
launcher_title: TikTok 启动台 | DEGRADED_RENAME_UNAVAILABLE
launcher_state: PREFLIGHT | ASSIGNING | IDLE
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

The launcher records only immutable handoff provenance and becomes idle. It is
not a manager, callback target, replacement owner, or automation owner.

## Identity proof

- executor identity: exact ID returned by creation plus assignment acceptance;
- automation identity: exact automation ID and view readback;
- valid self wake:
  `waking_thread_id == targetThreadId == automation_manager_thread_id == executor_thread_id`;
- external tab/resource: handle created and recorded by this executor in the
  current control session.

Independent executors never list/read one another, inspect same-account state,
reuse titles as identity, or claim another resource/timer.

## Owner failure before handoff

`failed to resolve rollout path ... file does not exist` is
`STALE_OWNER_TOMBSTONE`. Host unavailable, timeout, network, or tool transport
fault is `LIVENESS_UNVERIFIED_TRANSIENT` and must not immediately create a
duplicate.

Before any external work, a launcher may create at most one clean replacement
for a definitively failed new executor. Record old/new exact IDs and assignment
ref. After accepted handoff the launcher is idle and does not monitor, revive,
or replace the executor.

Archived executors are retired and are never automatically unarchived.

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
