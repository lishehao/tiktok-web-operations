# Coordinator And Executor

Use two persistent Codex tasks for one active TikTok mission:

```text
TikTok 启动台 --healthy same-task transition--> pinned TikTok 主控台
TikTok 主控台 --round_assignment/v1--> TikTok 执行台
TikTok 执行台 --round_callback/v1--> TikTok 主控台
TikTok 主控台 --scheduler says due--> next round_assignment/v1
```

Both tasks use `gpt-5.6-luna` with `thinking=high`. Never substitute a subagent,
Goal Mode, or an agent tree.

## Main-task initialization

1. Run install/upgrade and read-only preflight while titled `TikTok 启动台`.
2. After health proof, rename the same exact task `TikTok 主控台`, attempt to pin
   it, and verify `pinned=true` when supported. Presentation failure is degraded,
   not a second-task reason.
3. Complete the confirmed profile gate and create canonical direction,
   authority, and mission objects.
4. Generate a new run ID and fresh-create exactly one unpinned `TikTok 执行台`.
   Record only the exact new ID returned by that call; never select a historical
   same-title task.
5. Send `executor_assignment/v2` with exact main/executor/run IDs and callback
   target. Require `ASSIGNMENT_ACCEPTED`.
6. Prove a real callback handshake before external work:

```text
TikTok 主控台 -> CALLBACK_PING/v1
TikTok 执行台 -> CALLBACK_ACK/v1 -> exact TikTok 主控台
```

7. Create one main-task-targeted recurring scheduler Heartbeat under the direct
   user mission authorization. Normally use a five-minute recurrence. Require
   exact automation ID, exact main-task target, ACTIVE/repeat-on state, next
   local/UTC run, and mission cutoff readback. If creation produces only a
   suggestion card or lacks an exact ID/readback, record
   `SCHEDULER_CONTINUATION_FAILURE`; never claim unattended continuation.
8. Dispatch `round_assignment/v1` for round 1 immediately.

## Canonical assignment

`executor_assignment/v2` contains:

```json
{
  "schema":"executor_assignment/v2",
  "assignment_id":"<uuid>",
  "run_id":"<uuid>",
  "coordinator_thread_id":"<exact main task id>",
  "executor_thread_id":"<exact returned executor id>",
  "role":"TIKTOK_EXECUTOR",
  "execution_profile":{"model":"gpt-5.6-luna","thinking":"high"},
  "account":{"platform":"tiktok","handle":"<verified handle>"},
  "direction_ref":{"id":"...","version":1,"sha256":"..."},
  "authority_ref":{"id":"...","version":1,"sha256":"..."},
  "mission_ref":{"id":"...","version":1,"sha256":"..."},
  "executor_ledger_path":"<private path>",
  "coordinator_ledger_path":"<private path>",
  "dedicated_tab_policy":"EXECUTOR_OWNED",
  "callback_policy":"ROUND_BOUNDARY_TO_EXACT_COORDINATOR",
  "automation_policy":"COORDINATOR_OWNED_FIXED_SCHEDULER"
}
```

Serialize canonical JSON with sorted keys and compact separators. The executor
validates exact bytes/hash/identity before Chrome work.

## Bounded round contract

The main task sends one `round_assignment/v1` containing run/round IDs, three
search clusters, exclusions, 25–45 qualified-view boundary, For You sample,
interaction emphasis, current authority ref, deadline, and resume cursor.

The executor runs that round continuously, owns all TikTok/browser decisions
inside the envelope, checkpoints incrementally, then sends exactly one
`round_callback/v1`:

```json
{
  "schema":"round_callback/v1",
  "run_id":"<uuid>",
  "round_seq":1,
  "coordinator_thread_id":"<exact main task id>",
  "executor_thread_id":"<exact executor id>",
  "status":"ROUND_COMPLETED|ROUND_BLOCKED|RUN_RELEASED",
  "qualified_views":{"search":0,"for_you":0,"total":0},
  "feed_composition":{"core":0,"adjacent":0,"drift":0},
  "mutation_attempts":{"like":0,"favorite":0,"repost":0,"comment":0},
  "cluster_evidence":[],
  "resume_cursor":{},
  "capability_delta":{},
  "blocker":null,
  "executor_state":"IDLE|HARD_REPAIR|RELEASED",
  "ledger_tail_ref":{"path":"...","sha256":"..."}
}
```

After sending the callback, the executor performs no TikTok work until it
receives the next valid round assignment or stop instruction.

## Strategy and cooldown

The main task accepts callbacks only for its exact run/executor and expected
round sequence. From rolling evidence it chooses the next search clusters and
interaction emphasis. It then reads a fresh machine clock and stores:

```text
cooldown_minutes: integer 10..20
callback_accepted_at_utc: exact machine timestamp
next_dispatch_at_utc: callback_accepted_at_utc + cooldown_minutes
pending_round_seq: current round + 1
executor_state: IDLE
```

Use 15 minutes normally, 10 for read-only/low-yield work, and 20 for mutation-
or recovery-heavy work. This is workload pacing, not randomized stealth.

## Fixed scheduler

The main task owns one recurring Heartbeat for the mission. The executor owns no
timer. On every wake, use real machine UTC and exact registry state:

1. At/after user stop or `operation_stop_at`, stop dispatch and delete the exact
   scheduler.
2. If no accepted callback is pending, executor is active, or
   `actual_now < next_dispatch_at`, perform no dispatch.
3. If due and executor is verified idle, send one canonical next-round
   assignment, persist `ROUND_DISPATCHED`, and clear the pending flag.
4. Never send catch-up rounds, never infer completion from a title, and never
   create a replacement timer per round.

The scheduler prompt holds only stable identity, registry/ledger paths, wake
rules, and cutoff. Mutable strategy and evidence stay in the main ledger.

## Failure and finalization

Ordinary candidate, page, network, Chrome, Feed, and single-lane problems are
handled inside the executor's bounded round. If they end the round, callback the
smallest affected scope. Human-only login/CAPTCHA/account-lock/control blockers
return to the main task, which asks the user once.

At stop/deadline/completion the main task stops dispatch, sends one stop command
when needed, deletes its exact scheduler, requires the executor's
`RUN_RELEASED` callback with owned-tab release proof, reconciles both ledgers,
and reports the final result.
