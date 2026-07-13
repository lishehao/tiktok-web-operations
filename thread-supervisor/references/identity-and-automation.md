# Thread Identity And Automation Ownership

A title, list result, directory, cached summary, or old prompt is not task
identity. Use exact IDs returned by thread and automation tools plus readback.

## TikTok coordinator-worker registry

```text
coordinator_thread_id: exact pinned TikTok 主控台 id
coordinator_title: TikTok 启动台 | TikTok 主控台 | DEGRADED_RENAME_UNAVAILABLE
coordinator_pinned: TRUE | DEGRADED_PIN_UNAVAILABLE | UNVERIFIED
coordinator_state: BOOTSTRAP | READY | DISPATCHING | WAITING_CALLBACK |
  COOLDOWN | HARD_REPAIR | FINALIZING | RELEASED
run_id: exact uuid
profile_ref: exact confirmed canonical ref
direction_ref: exact canonical ref
authority_ref: exact canonical ref
mission_ref: exact canonical ref
operation_stop_at: exact UTC plus local rendering
executor_thread_id: exact fresh returned id
executor_title: TikTok 执行台
executor_state: NEW | ACCEPTED | ACTIVE | IDLE | HARD_REPAIR | RELEASED
callback_handshake: NONE | PING_SENT | ACK_VERIFIED
expected_round_seq: positive integer
last_callback_ref: NONE | exact canonical ref
pending_round_seq: NONE | positive integer
cooldown_minutes: NONE | integer 10..20
callback_accepted_at_utc: NONE | exact machine timestamp
next_dispatch_at_utc: NONE | exact machine timestamp
scheduler_automation_id: NONE | exact returned id
scheduler_manager_thread_id: exact coordinator id
scheduler_target_thread_id: exact coordinator id
scheduler_status: NONE | ACTIVE | UNVERIFIED | DELETED
scheduler_repeat: NONE | ON
scheduler_next_run: NONE | exact local/UTC readback
coordinator_ledger_path: exact private path
executor_ledger_path: exact private path
run_terminal_state: RUNNING | STOP_REQUESTED | RUN_RELEASED
```

## Identity proofs

- main identity: exact current task ID plus same-ID title/pin readback;
- executor identity: exact fresh `create_thread` return plus assignment acceptance;
- callback identity: sender/receiver/run/round IDs match registry and sequence;
- scheduler identity: exact automation ID plus
  `targetThreadId == scheduler_manager_thread_id == coordinator_thread_id`;
- external tab: handle created and recorded by the exact executor.

Perform `CALLBACK_PING/v1` and `CALLBACK_ACK/v1` before external work. A readable
executor title or successful outbound send is not callback proof.

## Fresh executor creation

For a new mission, call `create_thread` once and recognize only its exact new
returned ID. Do not select a historical same-title task. A failed/unknown create
does not authorize title search, unarchive, reuse, or a duplicate replacement.
Record `FRESH_TASK_CREATION_FAILED|UNKNOWN` in the main task.

After the executor is registered, the main task may read/message that exact task
for assignment, callback validation, dispatch, and stop. It does not inspect
unrelated TikTok tasks. The executor reads/messages only its exact main task.

## Scheduler ownership

The main task alone creates, views, and deletes one self-target recurring
scheduler under the direct user mission authorization. Normally use a
five-minute recurrence. The executor owns zero timers.

Creation proof requires exact automation ID, exact main-task target,
ACTIVE/repeat-on state, next local/UTC run, and cutoff. A rendered suggestion
card, create request, inferred filename, or missing-ID response is not proof and
becomes `SCHEDULER_CONTINUATION_FAILURE`.

At every wake require exact main/run/timer binding and use fresh machine UTC.
No-op when executor is active, no accepted callback-derived round is pending, or
current time is before `next_dispatch_at`. When due, dispatch one round and clear
the pending flag. Never send catch-up bursts or create a new timer per round.

At explicit stop, deadline, completion, or terminal release, stop new dispatch,
request executor release if needed, delete the exact scheduler, and read back
its absence/deleted state.

Other domains may still use `launcher_self_owned_executor`; do not import that
topology into TikTok.
