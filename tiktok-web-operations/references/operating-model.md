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

## Steady-state role cards

| Task | One job | Reads | Decides | Returns |
|-|-|-|-|-|
| `TikTok 主控台` | Decide what/when/stop for the next bounded round | user instruction, mission/authority, accepted callback, machine clock | next clusters, exclusions, round envelope, cooldown, timer phase, hard repair, finalization | one assignment/timer action/user report |
| `TikTok 执行台` | Execute the assigned Chrome round and report facts | exact assignment, own ledger/cursor, live TikTok state | exact queries/posts, watch progression, candidate fit, comment text, authorized action attempts, within-round recovery | one accepted callback, then IDLE |

The main task never chooses an exact post or drafts an exact comment. The
executor never changes direction, authority, round size, cooldown, Heartbeat,
or mission state. Executor recommendations are explicitly non-binding evidence.

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
5. Call `set_thread_title` for that exact returned ID with `TikTok 执行台`, then
   read back the same ID/title when supported. If unavailable, persist
   `DEGRADED_EXECUTOR_TITLE_UNAVAILABLE`, continue, and allow only one exact-ID
   repair attempt at the first executor-IDLE boundary. Never search by title.
6. Send `executor_assignment/v2` with exact main/executor/run IDs and callback
   target. Require `ASSIGNMENT_ACCEPTED`.
7. Prove a real callback handshake before external work:

```text
TikTok 主控台 -> CALLBACK_PING/v1
TikTok 执行台 -> CALLBACK_ACK/v1 -> exact TikTok 主控台
```

8. Create one stable main-task-targeted mission recurring Heartbeat under the
   direct user mission authorization. Require exact automation ID, exact
   main-task target, `ACTIVE` repeat-on 15-minute schedule, next local/UTC run,
   mission cutoff, and cleanup `UNTIL` readback. If creation produces only a
   suggestion card or lacks an exact ID/readback, record
   `SCHEDULER_CONTINUATION_FAILURE`; never claim unattended continuation.
9. Dispatch `round_assignment/v1` for round 1 immediately.

## Same-mission continuation and owner recovery

The executor is mission-scoped, not round-scoped. After every accepted round
callback, and whenever the user continues or adjusts an active mission in
`TikTok 主控台`, reuse the exact registered `executor_thread_id`. Keep the
`run_id`; version changed direction/authority/mission refs and apply them to the
next non-overlapping bounded assignment. Do not create a new executor because a
round completed, a cooldown started, or the executor is IDLE.

The main may create one replacement inside the same run only when:

- the canonical registry has no exact `executor_thread_id`; or
- the exact registered task is proven `STALE_OWNER_TOMBSTONE` (including
  `failed to resolve rollout path` / `file does not exist`), retired, archived,
  or released before the active mission has ended.

`notLoaded`, empty/unavailable `read_thread`, host/network unavailability, and
transient tool failure are `LIVENESS_UNVERIFIED_TRANSIENT`, not owner absence.
Keep the same owner and mission recurring Heartbeat, preserve pending work, and retry later.

For a permitted replacement: keep `run_id`, increment `executor_generation`,
record `old_executor_thread_id`, `new_executor_thread_id`, exact reason, and UTC
timestamp, carry the last accepted resume cursor, issue one new canonical
`executor_assignment/v2`, and repeat assignment acceptance plus callback
handshake. Normalize the replacement title by its exact returned ID under the
same presentation rule. Atomically register and validate the new exact ID before
dispatch, then request old-owner release. Archive the old exact ID only after
its release proof; never archive the newly bound current owner. The main-owned
timer is updated in place; it is never recreated for owner replacement. A
failed/unknown replacement create or failed assignment ends replacement with
one orchestration blocker and no second create.

After `RUN_RELEASED`, cutoff, completion, or explicit terminal stop, a later
operating instruction is a new mission: repeat the profile boundary as needed,
generate a new run ID, and fresh-create a new executor.

## Canonical assignment

`executor_assignment/v2` contains:

```json
{
  "schema":"executor_assignment/v2",
  "assignment_id":"<uuid>",
  "run_id":"<uuid>",
  "executor_generation":1,
  "predecessor_executor_thread_id":null,
  "coordinator_thread_id":"<exact main task id>",
  "executor_thread_id":"<exact returned executor id>",
  "role":"TIKTOK_EXECUTOR",
  "execution_profile":{"model":"gpt-5.6-luna","thinking":"high"},
  "account":{"platform":"tiktok","handle":"<verified handle>"},
  "direction_ref":{"id":"...","version":1,"sha256":"..."},
  "authority_ref":{"id":"...","version":1,"sha256":"..."},
  "mission_ref":{"id":"...","version":1,"sha256":"..."},
  "resume_cursor_ref":null,
  "executor_ledger_path":"<private path>",
  "coordinator_ledger_path":"<private path>",
  "dedicated_tab_policy":"EXECUTOR_OWNED",
  "callback_policy":"ROUND_BOUNDARY_TO_EXACT_COORDINATOR",
  "automation_policy":"COORDINATOR_OWNED_MISSION_RECURRING_15M"
}
```

Serialize canonical JSON with sorted keys and compact separators. The executor
validates exact bytes/hash/identity before Chrome work.

## Bounded round contract

The main task sends one `round_assignment/v1` containing run/round IDs, three
search clusters, exclusions, 25–45 qualified-view boundary, For You sample,
interaction emphasis, current authority ref, deadline, and resume cursor.
For an authorized cultivation mission it also contains the authoritative lane
envelope below; emphasis may rank candidates but may not delete or zero a lane:

```json
{
  "mutation_lanes": {
    "like": "best_effort_attempt",
    "favorite": "best_effort_attempt",
    "repost": "best_effort_attempt",
    "comment": "best_effort_attempt"
  },
  "parallel_engagement": true,
  "comment_policy": {
    "status": "ACTIVE",
    "target": 10,
    "min": 7,
    "max": 12,
    "ceiling": 15
  }
}
```

Reset `comment_policy` for every round. Previous comment volume, a quality
shortfall, an executor suggestion, or drifted For You evidence cannot become
`PAUSED_UNTIL_NEW_CLUSTER_MATCH` or zero comment values. Only a current newer
user revocation, browse-only mission, or explicit current Comment hard block
may change `status` away from `ACTIVE`; record that exact cause and scope.

The assignment states **what outcome and envelope** to execute, not exact
candidate URLs, exact comments, or browser steps. Those are executor decisions
made from live evidence. The main task cannot perform part of the round itself.

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
  "next_round_suggestions":{"binding":false},
  "resume_cursor":{},
  "capability_delta":{},
  "blocker":null,
  "executor_state":"IDLE|HARD_REPAIR|RELEASED",
  "ledger_tail_ref":{"path":"...","sha256":"..."}
}
```

After sending the callback, the executor performs no TikTok work until it
receives the next valid round assignment or stop instruction.

The callback contains observed facts. `next_round_suggestions` may propose
clusters, emphasis, or risks, but cannot change authority, schedule work, or act
as a next assignment. The main task accepts/rejects those suggestions against
the current mission and writes the sole next-round decision.

## Strategy and cooldown

The main task accepts callbacks only for its exact run/executor and expected
round sequence. From rolling evidence it chooses the next search clusters and
interaction emphasis. Treat executor recommendations as evidence, not authority:
`cooldown comments until new cluster match` means rotate search and judge each
new opened post, never freeze the entire next round. For You drift affects the
held-out validation plan only. The main then reads a fresh machine clock and
stores:

```text
cooldown_minutes: integer 10..20
callback_accepted_at_utc: exact machine timestamp
next_dispatch_at_utc: callback_accepted_at_utc + cooldown_minutes
pending_round_seq: current round + 1
executor_state: IDLE
idle_proof: CALLBACK_ACCEPTED
idle_proof_round_seq: current round
```

Use 15 minutes normally, 10 for read-only/low-yield work, and 20 for mutation-
or recovery-heavy work. This is workload pacing, not randomized stealth.

## Mission recurring scheduler

The main task owns one stable self-targeted scheduler Heartbeat for the mission;
the executor owns no timer. Create it once before round 1 with a 15-minute
repeat-on cadence and finite cleanup `UNTIL` at least one full interval after
`operation_stop_at`. The cutoff remains the exact no-new-work boundary. Do not
use `COUNT=1`, one-occurrence scheduling, a self-rearmed watchdog, or one timer
per round.

Read back exact ID, target, `ACTIVE` status, repeat-on cadence, next local/UTC
run, cutoff, and cleanup `UNTIL`. The stable prompt holds only identity,
registry/ledger paths, dispatch gates, and cutoff; mutable phase, strategy, and
evidence stay in the main ledger.

1. After every `ROUND_DISPATCHED`, leave the recurring schedule unchanged.
2. When the exact callback arrives, compute the 10–20 minute cooldown, persist
   canonical callback-IDLE proof and `next_dispatch_at`, and leave the recurring
   schedule unchanged.
3. On every tick, read a fresh machine clock. Dispatch exactly one next-round
   assignment only when the callback-IDLE proof is unconsumed and
   `now >= next_dispatch_at`. A live task read remains optional diagnostic
   evidence, not a prerequisite.
4. If the executor is active, the cooldown is early, or required proof is
   missing, perform no dispatch and preserve the recurrence. Request one missing
   callback/status at most once per round; later ticks wait without duplicates.
   After successful recurring readback, unchanged ticks use `DONT_NOTIFY`.
5. Retain the exact owner and scheduler across `notLoaded`, empty read,
   host/network/tool faults, and ordinary round blockers. Enter same-run owner
   replacement only with strict missing/stale proof.
6. At/after cutoff, send no new work, request release when needed, delete the
   exact Heartbeat, and finalize. Never send catch-up rounds.

Before every nonterminal scheduler turn returns, require the same exact
repeat-on Heartbeat with a future next run and cleanup `UNTIL`. `status=ACTIVE`
with no future occurrence before cutoff is `MISSION_SCHEDULER_EXPIRED`; repair
the same automation in place before dispatch. A callback or single wake is
never the sole continuation mechanism.

## Failure and finalization

Ordinary candidate, page, network, Chrome, Feed, and single-lane problems are
handled inside the executor's bounded round. If they end the round, callback the
smallest affected scope. Human-only login/CAPTCHA/account-lock/control blockers
return to the main task, which asks the user once.

At stop/deadline/completion the main task stops dispatch, sends one stop command
when needed, requires the executor's `RUN_RELEASED` callback with owned-tab
release proof, deletes and reads back its exact scheduler, and reconciles both
ledgers. It then archives only the exact registered executor ID and reads back
that same task's archive state when supported. `set_thread_archived` failure or
unavailability becomes `DEGRADED_EXECUTOR_ARCHIVE_UNAVAILABLE`; it does not
change the mission's factual terminal state and must not be reported as archive
success. Never archive before release, by title, or while the executor is the
current owner of a live mission.
