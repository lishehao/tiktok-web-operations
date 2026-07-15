# TikTok Coordinator-Worker Protocol

Use this reference only when the TikTok domain explicitly selects the persistent
two-task coordinator/worker topology. Also read `canonical-registry.md` and
`identity-and-automation.md` directly from `SKILL.md`.

## Contents

- Topology
- Executor identity and reuse
- Bounded round callbacks
- Coordinator phase timer
- Release

## Topology

```text
TikTok 启动台 --healthy same-task transition--> pinned TikTok 主控台
TikTok 主控台 --bounded round_assignment/v1--> TikTok 执行台
TikTok 执行台 --ROUND_COMPLETED|BLOCKED|RELEASED callback--> TikTok 主控台
TikTok 主控台 --one callback-armed cooldown wake--> next round
```

Use exactly two persistent tasks for one active mission. The main task owns
profile/mission versions, strategy, exact executor registry, callback validation,
`next_dispatch_at`, one stable self-target phase timer, user decisions, and final
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

## Coordinator phase timer

Create one coordinator-owned self-target phase timer under the user's direct
mission authorization. Record and read back exact automation ID, target, current
phase, one-future-occurrence state, next local/UTC run, and cutoff.

Reuse that exact timer in place:

- After round dispatch, arm one 60-minute `ACTIVE_WATCHDOG` only.
- After a valid callback, replace the watchdog schedule with one
  `COOLDOWN_WAKE` at exact `next_dispatch_at`.
- At the cooldown wake, consume callback-IDLE proof, dispatch one round, and
  rearm the next watchdog.
- If required proof is missing, preserve pending work and use one five-minute
  `STATE_RETRY`. After three failures, retain one 15-minute
  `DEGRADED_RECOVERY` wake and notify once.
- Delete and finalize only on user stop, mission cutoff, or terminal release.

Do not rely on requested `PAUSED` state. Prove exactly one future occurrence by
readback. If direct `DTSTART` or bare `COUNT=1` produces no future run, use the
tool-supported finite `INTERVAL+UNTIL` encoding with an `UNTIL` buffer of at
least two minutes but shorter than the interval.

Before every nonterminal wake returns, require exactly one future occurrence.
`ACTIVE` with no future occurrence is `EXPIRED_ORPHAN`; repair it in place while
the mission lives or delete it during terminal finalization.

Read machine time when accepting callbacks and compare epoch values on wake.
Never derive due time from model-estimated timestamps, create/delete one timer
per round, run a five-minute active-worker polling loop, or send catch-up bursts.

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
