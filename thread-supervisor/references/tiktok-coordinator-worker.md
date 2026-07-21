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
TikTok 执行台 --ROUND_COMPLETED|YIELDED|BLOCKED|RELEASED callback--> TikTok 主控台
TikTok 主控台 --15-minute recurring scheduler tick when due--> next round
```

Use exactly two persistent tasks for one active mission. The main task owns
profile/mission versions, strategy, exact executor registry, callback validation,
`next_dispatch_at`, one stable self-target mission recurring Heartbeat, user decisions, and final
reporting. It never owns a TikTok operating tab or performs TikTok mutations.

The executor owns one dedicated Chrome tab, raw evidence, within-round recovery,
and one bounded 25-45-view round at a time. It never creates, updates, views, or
deletes an automation.

During an active round, append a local `ROUND_PROGRESS` ledger row after each
10 newly qualified views and whenever entering recovery. This is not a callback,
does not make the executor IDLE, and cannot authorize dispatch. The main may
read only the known executor-ledger tail on its scheduled wake to update
`last_executor_progress_at_utc` without touching Chrome.

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
- Immediately set that exact ID's title to `TikTok 执行台` and verify same-ID
  readback when supported; title failure is non-blocking degradation, never a
  reason to search by title or create another executor.
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
hash, sender, `round_seq`, and expected `boundary_seq` match. `boundary_seq`
starts at 1 for a logical round and identifies each bounded executor segment.
Duplicate, late, misbound, or out-of-sequence callbacks perform no dispatch.

When one Chrome recovery pass remains unresolved, use
`status=ROUND_YIELDED`, `recovery_state=RECOVERY_PENDING`, and IDLE. Preserve the
same round ID/sequence, counts, remaining budgets, resume cursor, dedup set, and
frozen action keys. The first due scheduler tick sends one
`resume_mode=RECOVERY_FIRST` assignment for that same round with the next
`boundary_seq`. Repeated yields increment both `retry_epoch` and boundary
sequence; they never create a new logical round, executor, timer, or budget
reset. A completed round increments `round_seq` and resets `boundary_seq=1`.
Chrome/runtime diagnosis, including `CHROME_CONTENT_CHANNEL_TIMEOUT`, atomic
browser-boundary calls, scope probes, UI locator freshness, and mutation
uncertainty, lives only in
`tiktok-web-operations/references/runtime-and-recovery.md`. This protocol
accepts the resulting callback state; it must not replace an owner, rewrite the
Heartbeat, or duplicate an action because a content channel timed out.

Also require `qualified_view_contract=STRICT_QUALIFIED_VIEW_V2` and exact
ledger reconciliation before accepting the counts. A stable page, caption,
action attempt, or absolute progress value is not consumption proof. The
qualified total must equal unique ledger rows that contain source proof,
multiple forward playback observations, continuous watch meeting the
duration-based floor, and concrete premise/payoff evidence. Keep For You
`sampled` identities separate from qualified views.

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
- If an ACTIVE boundary has no new validated `ROUND_PROGRESS` or callback for
  60 minutes, send one exact `CHECKPOINT_OR_YIELD/v1` request for that boundary.
  If no evidence follows, record `PROGRESS_UNVERIFIED`; do not duplicate the
  request, dispatch, interrupt an uncertain mutation, replace a merely unreadable
  owner, or delete the Heartbeat. Later progress or the normal cutoff resolves it.
- An accepted `ROUND_YIELDED` callback dispatches one recovery-first resume of
  the same round at/after its stored retry time; the Heartbeat remains unchanged.
- Request a missing status/callback at most once per expected boundary; later ticks wait
  without duplicate messages. No-change ticks use `DONT_NOTIFY` only after
  recurring readback succeeds.
- At/after cutoff, send no new TikTok work and request release. Keep the finite
  cleanup occurrence until `RUN_RELEASED` or cleanup `UNTIL`. At unresolved
  expiry record `RELEASE_UNCERTAIN`, delete/read back the Heartbeat, and leave
  the executor unarchived.

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

1. Stop new TikTok dispatch.
2. Request executor release when needed.
3. Retain the finite cleanup wake while awaiting worker resource-release proof.
4. On proof, delete the exact coordinator timer and read back deleted/absent
   state. On cleanup expiry without proof, record `RELEASE_UNCERTAIN`, delete
   the timer, and do not archive.
5. Reconcile the registry, executor, tab, ledger, and timer states.
6. Archive only the exact released executor ID and read back archive state when
   supported. Never archive a live current owner or any task found by title.
7. Finalize with archive proof or explicit
   `DEGRADED_EXECUTOR_ARCHIVE_UNAVAILABLE`; never fabricate cleanup success.
