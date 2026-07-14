# Stability And Circuit Breakers

The executor owns within-round recovery; the main task owns one stable phase timer.
Circuit breakers are lane/surface scoped unless the hard-blocker whitelist is proven.

## Coordinator continuation invariant

Before external work require callback ping/ack plus one verified main-target
phase timer. Executor callbacks and becomes idle at every round boundary. The
main task machine-calculates `next_dispatch_at`; callback updates the same timer
to one cooldown wake, and due wake dispatches one round from the accepted
callback's canonical IDLE proof.
Active rounds have one 60-minute watchdog, never five-minute polling. An
uncertain submission is never retried.

Before cutoff, every scheduler wake must finish with exactly one verified future
wake or one dispatched round plus watchdog. Transient `read_thread` failure,
empty response, or `notLoaded` does not erase accepted callback-IDLE proof. If
required proof is genuinely missing, preserve the pending round and rearm a
five-minute state retry; after three failures retain a 15-minute degraded-
recovery wake and notify once. Never exit with a naked NOOP.

For a misbound/duplicate/misconfigured phase timer, do no dispatch. Delete it only
when exact identity is known; never create a per-round substitute. Explicit
stop, `operation_stop_at`, objective completion, or terminal release deletes the
main task's exact scheduler after executor release is requested.

Treat ACTIVE plus no future occurrence as `EXPIRED_ORPHAN`. While the mission is
live, repair the same exact timer in place; after cutoff, finalize rather than
reviving missed work.

## Lane breakers

- Favorite, Repost, Like, proactive comment, cultivation reply, comment Like,
  Not interested, follow, publishing, and profile edit are separate capability
  sub-lanes. Proactive comment and cultivation reply may share one authorized
  comment budget; a failure in either remains scoped to the exact action.
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
