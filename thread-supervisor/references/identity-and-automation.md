# Thread Identity And Automation Ownership

A title, list result, directory, cached summary, or old prompt is not task
identity. Use exact IDs returned by thread and automation tools plus readback.

## TikTok coordinator-worker registry

```text
coordinator_thread_id: exact pinned TikTok 主控台 id
coordinator_title: TikTok 启动台 | TikTok 主控台 | DEGRADED_RENAME_UNAVAILABLE
coordinator_pinned: TRUE | DEGRADED_PIN_UNAVAILABLE | UNVERIFIED
coordinator_state: BOOTSTRAP | READY | DISPATCHING | WAITING_CALLBACK |
  COOLDOWN | SCHEDULER_RECOVERY | HARD_REPAIR | FINALIZING | RELEASED
run_id: exact uuid
profile_ref: exact confirmed canonical ref
direction_ref: exact canonical ref
authority_ref: exact canonical ref
mission_ref: exact canonical ref
operation_stop_at: exact UTC plus local rendering
executor_thread_id: exact current canonical id returned by initial or permitted replacement create
executor_generation: positive integer, initial 1
old_executor_thread_id: NONE | exact retired same-run executor id
new_executor_thread_id: NONE | exact current replacement executor id
executor_replacement_reason: NONE | REGISTERED_EXECUTOR_ID_MISSING |
  STALE_OWNER_TOMBSTONE | RETIRED_DURING_ACTIVE_MISSION
executor_replaced_at_utc: NONE | exact UTC timestamp
last_accepted_resume_cursor_ref: NONE | exact canonical ref
executor_title: TikTok 执行台
executor_state: NEW | ACCEPTED | ACTIVE | IDLE | HARD_REPAIR | RELEASED
executor_idle_proof: NONE | CALLBACK_ACCEPTED
executor_idle_proof_round_seq: NONE | positive integer
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
scheduler_status: NONE | PAUSED | ACTIVE | UNVERIFIED | DELETED
scheduler_phase: NONE | ACTIVE_WATCHDOG | COOLDOWN_WAKE | STATE_RETRY |
  DEGRADED_RECOVERY
scheduler_occurrence: NONE | ONE
scheduler_next_run: NONE | exact local/UTC readback
scheduler_encoding: COUNT_1 | FINITE_INTERVAL_UNTIL_ONE_FUTURE_RUN
scheduler_retry_count: nonnegative integer
scheduler_future_wake_count: 0 | 1
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

## Initial creation, reuse, and same-run replacement

For a new mission, call `create_thread` once and recognize only its exact new
returned ID. Do not select a historical same-title task. A failed/unknown create
does not authorize title search, unarchive, reuse, or a duplicate replacement.
Record `FRESH_TASK_CREATION_FAILED|UNKNOWN` in the main task.

After the executor is registered, the main task may read/message that exact task
for assignment, callback validation, dispatch, and stop. It does not inspect
unrelated TikTok tasks. The executor reads/messages only its exact main task.

Keep that same registered executor across every round and every continuation or
direction update in the active mission. `IDLE`, round completion, cooldown, and
a new user message in the same main task do not authorize a new task. Keep the
run ID and version any changed refs for the next bounded assignment.

Strictly separate diagnostic uncertainty from owner absence:

- `notLoaded`, empty/unavailable task read, host/network unavailable, and
  transient task-tool failure -> `LIVENESS_UNVERIFIED_TRANSIENT`; retain owner,
  preserve pending work, and use bounded scheduler recovery;
- missing exact registered ID, `failed to resolve rollout path` / `file does
  not exist`, or explicit archived/retired/released state while the mission is
  active -> replacement-eligible absence/stale proof.

For replacement-eligible proof, create at most one executor with the same run
ID, increment `executor_generation`, record old/new exact IDs, reason, UTC, and
last accepted resume cursor, and send a fresh `executor_assignment/v2`. Require
`ASSIGNMENT_ACCEPTED` plus a new callback handshake, then atomically replace the
registry binding. Do not search by title, unarchive the old owner, or recreate
the main-owned timer. Failed/unknown replacement creation or assignment is an
orchestration blocker and never permits a second create. A mission that already
terminally released creates a new run/executor instead of using this path.

## Scheduler ownership

The main task alone creates, views, updates, and deletes one stable self-target
phase timer under the direct user mission authorization. The executor owns zero
timers. Never poll an active executor every five minutes.

Creation proof requires exact automation ID, exact main-task target,
phase/one-occurrence state, next local/UTC run, and cutoff. A rendered suggestion
card, create request, inferred filename, or missing-ID response is not proof and
becomes `SCHEDULER_CONTINUATION_FAILURE`.

Do not use a requested `PAUSED` status as proof; direct creation may normalize
it to `ACTIVE`. Prove stopped polling by enumerating exactly one future run from
readback. If immediate create rejects `DTSTART` or bare `COUNT=1` reports no
future run, encode the same semantics with finite
`INTERVAL=<minutes>;UNTIL=<just after one interval>` and verify it.
Keep `UNTIL` at least two minutes beyond the intended occurrence and shorter
than the interval, then enumerate the one remaining future run.

After dispatch, ordinary scheduling is paused and the same timer carries only
one `ACTIVE_WATCHDOG` at dispatch + 60 minutes. A valid callback updates that
same exact automation in place to one `COOLDOWN_WAKE` at `next_dispatch_at`.
The due cooldown wake dispatches one round and rearms the same timer as the next
watchdog. A watchdog never dispatches while executor is active. Never send
catch-up bursts, create/delete a timer per round, or fall back to five-minute
NOOP polling.

Accepted callback bytes with `executor_state=IDLE` are the dispatch proof until
consumed by the next assignment. Live task readback is diagnostic; unavailable,
empty, and `notLoaded` results are not contradictory evidence. If canonical
proof is missing, keep the pending round and update the same timer to one five-
minute `STATE_RETRY`; after three consecutive failures, keep one 15-minute
`DEGRADED_RECOVERY` wake and notify once.

Before every nonterminal scheduler turn returns, require
`scheduler_future_wake_count=1`. `ACTIVE` plus zero future occurrences is
`EXPIRED_ORPHAN`, not healthy. A naked NOOP is forbidden.

At explicit stop, deadline, completion, or terminal release, stop new dispatch,
request executor release if needed, delete the exact scheduler, and read back
its absence/deleted state.

Other domains may still use `launcher_self_owned_executor`; do not import that
topology into TikTok.
