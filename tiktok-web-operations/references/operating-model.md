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

7. Create one stable main-task-targeted phase timer under the direct user
   mission authorization. Require exact automation ID, exact main-task target,
   current phase, one-occurrence state, next local/UTC run, and mission cutoff
   readback. If creation produces only a
   suggestion card or lacks an exact ID/readback, record
   `SCHEDULER_CONTINUATION_FAILURE`; never claim unattended continuation.
8. Dispatch `round_assignment/v1` for round 1 immediately.

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
Keep the same owner and phase timer, rearm bounded recovery, and retry later.

For a permitted replacement: keep `run_id`, increment `executor_generation`,
record `old_executor_thread_id`, `new_executor_thread_id`, exact reason, and UTC
timestamp, carry the last accepted resume cursor, issue one new canonical
`executor_assignment/v2`, and repeat assignment acceptance plus callback
handshake. Atomically register the new exact ID before dispatch and retire the
old registry binding. The main-owned timer is updated in place; it is never
recreated for owner replacement. A failed/unknown replacement create or failed
assignment ends replacement with one orchestration blocker and no second create.

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
  "automation_policy":"COORDINATOR_OWNED_CALLBACK_FIRST_PHASE_TIMER"
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

## Callback-first phase timer

The main task owns one stable phase-timer automation for the mission. The
executor owns no timer. Keep its exact ID and update its schedule in place:

Runtime encoding: do not assume requested `PAUSED` persists, and do not force
`DTSTART` on immediate create. Prove exactly one future occurrence from readback.
Use `COUNT=1` only when it has a future run; otherwise use finite
`INTERVAL+UNTIL` that leaves exactly one future run. Put `UNTIL` at least two
minutes after the intended occurrence and keep the buffer shorter than the
interval.

1. After every `ROUND_DISPATCHED`, stop ordinary polling and arm one
   `ACTIVE_WATCHDOG` for 60 minutes after dispatch, bounded by cutoff.
2. When the exact callback arrives, compute the 10–20 minute cooldown and update
   the same timer to one `COOLDOWN_WAKE` at exact `next_dispatch_at`.
3. At a valid due cooldown wake, consume the accepted callback's canonical IDLE
   proof, send one next-round assignment, persist `ROUND_DISPATCHED`, and rearm
   the same timer as the next single active-round watchdog. A live task read is
   optional diagnostic evidence, not a prerequisite.
4. At a watchdog wake, never dispatch over an active executor. Read only the
   registered executor: rearm once when progress is recent, request one missing
   callback/status when idle, retain the owner and rearm recovery when liveness
   is transiently unverified, or enter the one-attempt same-run replacement path
   only with strict missing/stale-owner proof.
5. When required callback/identity proof is absent, do not discard the pending
   round. Rearm the same timer for one five-minute `STATE_RETRY`. Optional
   diagnostic-read failure alone does not block dispatch when canonical proof
   exists.
   After three consecutive failures, keep one 15-minute
   `DEGRADED_RECOVERY` wake and notify once.
6. Never send catch-up rounds, infer completion from a title, poll an active
   executor every five minutes, or create/delete a replacement timer per round.

At every wake before cutoff, enforce `future_wake_count=1` on readback. A bare
NOOP is invalid. `status=ACTIVE` with no future occurrence is
`EXPIRED_ORPHAN`, not healthy continuity; repair it in place for a live mission
or delete it during terminal finalization.

The timer prompt holds only stable identity, registry/ledger paths, phase rules,
and cutoff. Mutable phase, strategy, and evidence stay in the main ledger.

## Failure and finalization

Ordinary candidate, page, network, Chrome, Feed, and single-lane problems are
handled inside the executor's bounded round. If they end the round, callback the
smallest affected scope. Human-only login/CAPTCHA/account-lock/control blockers
return to the main task, which asks the user once.

At stop/deadline/completion the main task stops dispatch, sends one stop command
when needed, deletes its exact scheduler, requires the executor's
`RUN_RELEASED` callback with owned-tab release proof, reconciles both ledgers,
and reports the final result.
