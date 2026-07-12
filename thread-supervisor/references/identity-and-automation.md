# Thread Identity And Automation Ownership

A title, focused window, list/search result, directory, cached summary, or old
prompt is not task identity. Use the exact ID returned by `create_thread` and
exact tool readback.

## Launcher/self-owned executor state

Mutable state associated with `executor_assignment/v1`:

```text
launcher_title: TikTok 启动台 | TikTok 分发台 | DEGRADED_RENAME_UNAVAILABLE
launcher_pinned: TRUE | DEGRADED_PIN_UNAVAILABLE | UNVERIFIED
launcher_state: PREFLIGHT | DISTRIBUTOR_READY | ASSIGNING | REUSABLE_IDLE
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
pending_wake_id: NONE | tiktok-wake-<run_id>-round-<round_seq> | tiktok-recovery-<run_id>-<recovery_seq>
pending_wake_target_thread_id: NONE | exact executor id
pending_wake_occurrences: NONE | 1
pending_wake_next_at: NONE | exact local/UTC timestamp
operation_stop_at:
cooldown_minutes: NONE | integer 10..20
cooldown_until: NONE | exact local/UTC timestamp
round_seq: non-negative integer
recovery_seq: non-negative integer
resume_cursor:
run_terminal_state: RUNNING | STOP_REQUESTED | RUN_RELEASED
```

The launcher records only the current dispatch's immutable handoff provenance
until acceptance, then discards run working state and becomes `REUSABLE_IDLE`. It is
not a manager, callback target, replacement owner, or automation owner.

After domain health proof, the same exact launcher task may become a pinned
distributor presentation. Verify the exact task ID with `pinned=true` when tool
readback exists. Pin/title failure is non-blocking degradation and never causes
a replacement task. Executors remain unpinned.

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

In `self_owned_executor_tick`, the executor alone creates, views, consumes, and
retires its one-shot timers. Create none at assignment acceptance. At a round
checkpoint require one occurrence, a run/round-unique ID, exact self target,
next local/UTC wake, and a wake earlier than mission cutoff. Verify readback
before yield.

If already running, a wake does no overlap. On a valid wake, record consumption,
delete/retire the expired automation if still present, clear `pending_wake_id`,
and resume. Uncertain submission is never retried. A misbound or uncertain wake
does no external work and is not silently replaced in the same checkpoint.

For a recoverable failure that must retry later, use the same one-occurrence
pattern with a unique recovery sequence. At most one pending wake exists. Stop,
deadline, or completion deletes only that exact pending wake after resource and
ledger reconciliation. Never use the distributor as timer owner and never use a
global `executor-heartbeat` ID.

Domains explicitly selecting coordinator-managed timers use their own contract;
they do not override a self-owned executor domain.
