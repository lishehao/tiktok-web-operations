# TikTok Coordinator-Worker Protocol

Use this reference only when the TikTok domain explicitly selects the persistent
two-task coordinator/worker topology. Also read `canonical-registry.md` and
`identity-and-automation.md` directly from `SKILL.md`.

## Contents

- Topology
- Executor identity and reuse
- Bounded round callbacks
- Coordinator mission scheduler
- Release

## Topology

```text
TikTok 启动台 --healthy same-task transition--> pinned TikTok 主控台
TikTok 主控台 --bounded round_assignment/v1--> TikTok 执行台
TikTok 执行台 --ROUND_COMPLETED|BLOCKED|RELEASED callback--> TikTok 主控台
TikTok 主控台 --15-minute recurring scheduler tick when due--> next round
```

Use exactly two persistent tasks for one active mission. The main task owns
profile/mission versions, strategy, exact executor registry, callback validation,
`next_dispatch_at`, one stable self-target mission recurring Heartbeat, user decisions, and final
reporting. It never owns a TikTok operating tab or performs TikTok mutations.

The executor owns one dedicated Chrome tab, raw evidence, within-round recovery,
and one bounded 25-45-view round at a time. It never creates, updates, views, or
deletes an automation.

Keep the role sentence literal:

- `TikTok 主控台`: decide **what the next round is, when it runs, or whether to
  stop**. Never select exact posts, write comments, or touch TikTok.
- `TikTok 执行台`: **execute that one round in Chrome and return facts**. Never
  choose direction, authority, cooldown, Heartbeat, or the next assignment.

The main-to-executor message is an assignment envelope. The executor-to-main
message is evidence plus optional `binding=false` suggestions. Neither task may
perform the other task's missing work.

## Executor identity and reuse

- Create one fresh executor for a new mission and record its exact returned ID.
- Require assignment acceptance and a real callback handshake before external
  work.
- Reuse the registered executor for normal rounds and active-mission
  continuations. A new user message, callback, IDLE state, or cooldown does not
  authorize another executor.
- Replace only when the exact registered ID is missing or the exact executor is
  proven stale/retired. Increment generation, record old/new IDs and reason, and
  require fresh assignment acceptance plus callback handshake.
- Retain the owner across transient `notLoaded`, empty read, host, network, or
  tool failures.
- A terminally released mission starts a new run and executor.

An accepted exact round callback with `executor_state=IDLE` remains canonical
until the next dispatch consumes it. Later `read_thread` results are diagnostic;
unavailable, empty, or `notLoaded` reads do not invalidate accepted callback
proof.

## Bounded round callbacks

Before external work, reconcile coordinator/executor/run IDs and canonical
references, then complete `CALLBACK_PING/v1` and `CALLBACK_ACK/v1`.

At round completion, the executor sends one canonical callback and becomes idle.
The main task accepts it only when coordinator, executor, run, round, schema,
hash, sender, and sequence match. Duplicate, late, misbound, or out-of-sequence
callbacks perform no dispatch.

After acceptance, the main task chooses the next three search clusters,
interaction emphasis, and a 10-20 minute cooldown. Dynamic strategy and pending
round state stay in the main ledger; raw browser evidence and deduplication stay
in the executor ledger.

Interaction emphasis is not authority. In an authorized cultivation mission,
every round assignment retains Like/Favorite/Repost/Comment as four
`best_effort_attempt` lanes and resets Comment to `ACTIVE` with
target/min/max/ceiling `10/7/12/15`. A prior target hit, quality shortfall,
executor recommendation, or drifted For You checkpoint may change search
clusters but may not zero or globally pause Comment. Treat `new cluster match`
as a per-opened-video candidate decision. Only a newer user revocation,
browse-only mission, or current explicit Comment hard block may narrow it.

## Coordinator mission scheduler

Create one coordinator-owned self-target mission scheduler Heartbeat under the
user's direct mission authorization. Configure it repeat-on every 15 minutes,
without `COUNT=1`, and set finite `UNTIL` at least one full interval after the
exact no-new-work cutoff so a terminal cleanup wake remains possible. Record
and read back exact automation ID, target, status, interval, repeat-on schedule,
next local/UTC run, cutoff, and cleanup `UNTIL`.

Keep that exact Heartbeat unchanged across ordinary callbacks and rounds:

- A callback persists canonical IDLE proof, next clusters, cooldown, and
  `next_dispatch_at`; it does not rewrite the schedule.
- Each tick dispatches exactly one round only when unconsumed callback-IDLE
  proof exists and `now >= next_dispatch_at`.
- An active executor, early cooldown, missing callback, or transient read/tool/
  network fault performs no dispatch and leaves the recurrence intact.
- Request a missing status/callback at most once per round; later ticks wait
  without duplicate messages. No-change ticks use `DONT_NOTIFY` only after
  recurring readback succeeds.
- At/after cutoff, send no new work, request release when needed, delete the
  exact Heartbeat, and finalize.

Before every nonterminal scheduler turn returns, require the same exact
`ACTIVE`, repeat-on 15-minute Heartbeat with a future run and cleanup `UNTIL`.
`ACTIVE` with no future run before cutoff is `MISSION_SCHEDULER_EXPIRED`; repair
the same schedule in place before dispatch.

Read machine time when accepting callbacks and on every tick. Never derive due
time from model-estimated timestamps, create/delete one timer per round, use a
one-occurrence self-rearm chain, or send catch-up bursts.

If timer creation, update, or readback fails, do not claim unattended
continuity. Report `SCHEDULER_CONTINUATION_FAILURE` while preserving completed
evidence.

## Release

At explicit stop, deadline, completion, or terminal release:

1. Stop new dispatch.
2. Request executor release when needed.
3. Require worker resource-release proof.
4. Delete the exact coordinator timer and read back deleted/absent state.
5. Finalize only after the registry, executor, tab, and timer states reconcile.
