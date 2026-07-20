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
executor_title_status: PENDING | VERIFIED | DEGRADED_UNAVAILABLE
executor_title_repair_attempted: FALSE | TRUE
executor_state: NEW | ACCEPTED | ACTIVE | IDLE | RECOVERY_PENDING |
  HARD_REPAIR | RELEASED | RELEASE_UNCERTAIN
executor_archive_status: NOT_DUE | PENDING_RELEASE | ARCHIVED |
  DEGRADED_UNAVAILABLE
executor_archived_at_utc: NONE | exact UTC timestamp
executor_idle_proof: NONE | CALLBACK_ACCEPTED
executor_idle_proof_round_id: NONE | exact round id
executor_idle_proof_round_seq: NONE | positive integer
executor_idle_proof_boundary_seq: NONE | positive integer
callback_handshake: NONE | PING_SENT | ACK_VERIFIED
expected_round_id: exact round id
expected_round_seq: positive integer
expected_boundary_seq: positive integer
last_callback_ref: NONE | exact canonical ref
pending_round_id: NONE | exact round id
pending_round_seq: NONE | positive integer
pending_boundary_seq: NONE | positive integer
round_started_at_utc: NONE | exact machine timestamp
last_executor_progress_at_utc: NONE | exact validated ledger timestamp
progress_request_boundary_seq: NONE | positive integer
executor_progress_state: NONE | ADVANCING | CHECKPOINT_REQUESTED |
  PROGRESS_UNVERIFIED
cooldown_minutes: NONE | integer 10..20
callback_accepted_at_utc: NONE | exact machine timestamp
next_dispatch_at_utc: NONE | exact machine timestamp
recovery_round_id: NONE | exact current yielded round id
recovery_retry_epoch: NONE | nonnegative integer
recovery_next_retry_not_before_utc: NONE | exact machine timestamp
scheduler_automation_id: NONE | exact returned id
scheduler_manager_thread_id: exact coordinator id
scheduler_target_thread_id: exact coordinator id
scheduler_status: NONE | PAUSED | ACTIVE | UNVERIFIED | DELETED
scheduler_mode: NONE | MISSION_RECURRING_15M
scheduler_next_run: NONE | exact local/UTC readback
scheduler_repeat: OFF | ON
scheduler_interval_minutes: NONE | 15
scheduler_until_utc: NONE | exact cleanup UNTIL after operation_stop_at
scheduler_health: NONE | HEALTHY | MISSION_SCHEDULER_EXPIRED |
  MISBOUND | UNREADABLE
coordinator_ledger_path: exact private path
executor_ledger_path: exact private path
run_terminal_state: RUNNING | STOP_REQUESTED | RUN_RELEASED
```

## Identity proofs

- main identity: exact current task ID plus same-ID title/pin readback;
- executor identity: exact fresh `create_thread` return plus assignment acceptance;
- executor presentation: exact returned ID plus same-ID `TikTok 执行台`
  title readback, or explicit non-blocking degraded status;
- callback identity: sender/receiver/run/round IDs plus expected
  `round_seq`/`boundary_seq` match the registry;
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

Immediately after a successful create, the main task calls `set_thread_title`
for the exact returned ID with `TikTok 执行台` and reads back that same ID/title
when supported. The title is presentation, never identity. Tool unavailability
or failure records `DEGRADED_EXECUTOR_TITLE_UNAVAILABLE` and does not block
assignment. The main may make one exact-ID title repair at the first safe IDLE
boundary; it never searches by title or retries on every scheduler tick. The
executor remains unpinned and never changes its own title/archive state.

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
registry binding. Normalize the new title by exact returned ID. Only after the
new binding is verified may the main request the old owner's release and archive
that old exact ID after release proof. Do not search by title, unarchive the old
owner, archive the current replacement, or recreate the main-owned timer.
Failed/unknown replacement creation or assignment is an orchestration blocker
and never permits a second create. A mission that already terminally released
creates a new run/executor instead of using this path.

## Scheduler ownership

The main task alone creates, views, repairs, and deletes one stable self-target
mission scheduler Heartbeat under the direct user mission authorization. The
executor owns zero timers.

Creation proof requires exact automation ID, exact main-task target, `ACTIVE`
status, repeat-on 15-minute cadence, next local/UTC run, cutoff, and a finite
cleanup `UNTIL` at least one full interval after the cutoff. A rendered
suggestion card, create request, inferred filename, or missing-ID response is
not proof and becomes `SCHEDULER_CONTINUATION_FAILURE`.

Prefer
`RRULE:FREQ=MINUTELY;INTERVAL=15;UNTIL=<operation_stop_at plus 15 minutes in UTC>`
with no `COUNT`. An equivalent tool-supported finite repeat-on form is allowed
only when it preserves the same cadence and terminal cleanup occurrence.

Never encode a multi-hour TikTok mission as `COUNT=1`, one future occurrence,
or a self-rearmed watchdog. The fixed recurring schedule remains unchanged
across ordinary callback, dispatch, cooldown, active-executor, and transient
recovery states. Mutable phase and evidence live in the coordinator ledger.

Accepted callback bytes with `executor_state=IDLE` are the dispatch proof until
consumed by the next assignment. Each recurring tick reads a fresh machine
clock and dispatches exactly one round only when that proof is unconsumed and
`now >= next_dispatch_at`. Live task readback is diagnostic; unavailable,
empty, and `notLoaded` results are not contradictory evidence. An active
executor, early cooldown, or missing proof leaves the recurrence intact and
does not send duplicate work.

Before every nonterminal scheduler turn returns, require the same exact
repeat-on automation with a future next run and cleanup `UNTIL`. `ACTIVE` plus
no future occurrence before cutoff is `MISSION_SCHEDULER_EXPIRED`, not healthy;
repair the same automation in place before dispatch. Never create a replacement
timer until a corrected exact binding is verified.

At explicit stop, deadline, or completion, stop new TikTok dispatch and request
executor release if needed. Keep the already-configured finite cleanup wake
until `RUN_RELEASED` or cleanup `UNTIL`. On release proof, delete the exact
scheduler, read back absence/deleted state, reconcile release/tab/ledger proof,
then archive the exact registered executor ID. At cleanup expiry without proof,
record `RELEASE_UNCERTAIN`, delete/read back the scheduler, and leave the
executor unarchived. Never archive an active, STOP_REQUESTED, unreleased,
IDLE-but-live, or release-uncertain executor, and never archive by title.
Archive-tool failure after proven release is
`DEGRADED_EXECUTOR_ARCHIVE_UNAVAILABLE`: keep factual terminal state, report the
presentation gap, and never claim archive success.

Other domains may still use `launcher_self_owned_executor`; do not import that
topology into TikTok.
