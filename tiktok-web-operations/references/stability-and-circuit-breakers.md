# Stability And Circuit Breakers

The executor owns within-round recovery; the main task owns one stable phase timer.
Circuit breakers are lane/surface scoped unless the hard-blocker whitelist is proven.

## Coordinator continuation invariant

Before external work require callback ping/ack plus one verified main-target
phase timer. Executor callbacks and becomes idle at every round boundary. The
main task machine-calculates `next_dispatch_at`; callback updates the same timer
to one cooldown wake, and due wake dispatches one round only when executor IDLE.
Active rounds have one 60-minute watchdog, never five-minute polling. An
uncertain submission is never retried.

For a misbound/duplicate/misconfigured phase timer, do no dispatch. Delete it only
when exact identity is known; never create a per-round substitute. Explicit
stop, `operation_stop_at`, objective completion, or terminal release deletes the
main task's exact scheduler after executor release is requested.

## Lane breakers

- Favorite, Repost, Like, proactive comment, comment Like, Not interested,
  follow, reply, publishing, and profile edit are separate lanes.
- Missing persistence or post-action proof never disables a lane. Record
  `attempted`; only the exact uncertain target/action is not retried.
- Two consecutive native For You transition failures disable only held-out Feed
  validation; qualified search training continues.
- Empty candidates produce a completed no-action checkpoint and cluster
  rotation, never a mission block.
- Malformed ledger data pauses mutation for bounded repair; it does not create
  frequent polling or require user confirmation.

## Whole-mission hard boundary

Use only `blocker-minimization.md`'s live human-repair whitelist. The executor
callbacks exact evidence and releases owned Chrome when appropriate; the main
task asks the user. Historical evidence never opens a circuit.

## Independent-run stability

Main and executor coordinate only with each other's exact registered IDs. Never
inspect unrelated TikTok tasks, claim their tabs, modify their automations, or
create a same-account lock.
