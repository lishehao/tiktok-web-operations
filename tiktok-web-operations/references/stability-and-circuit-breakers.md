# Stability And Circuit Breakers

The executor owns within-round recovery; the main task owns one stable mission recurring Heartbeat.
Circuit breakers are lane/surface scoped unless the hard-blocker whitelist is proven.

## Coordinator continuation invariant

Before external work require callback ping/ack plus one verified main-target
15-minute repeat-on scheduler. Executor callbacks and becomes idle at every
round boundary. The main task machine-calculates `next_dispatch_at`; the first
recurring tick at or after due dispatches one round from the accepted callback's
canonical IDLE proof. An uncertain submission is never retried.

Before cutoff, every scheduler turn must finish with the same verified recurring
Heartbeat and a future next run, whether it dispatches or waits. Transient
`read_thread` failure, empty response, `notLoaded`, active executor, early
cooldown, and missing callback proof do not erase accepted state or alter the
recurrence. Request missing callback/status at most once per expected boundary; later ticks
wait quietly.

Treat an actual wake within plus or minus five minutes of its scheduled
occurrence as `ON_TIME_WITH_TOLERANCE`. Continue the ordinary gate without timer
repair, missed-slot escalation, catch-up, or notification. A larger delta is
`WAKE_TIME_DRIFT` and receives bounded scheduler/host diagnosis while the same
recurrence and pending state survive. Actual-time cutoff remains exact.

An executor that exhausts one same-Chrome recovery pass returns
`ROUND_YIELDED/RECOVERY_PENDING` and IDLE. The main preserves that round's ID,
sequence, counts, remaining budgets, cursor, dedup set, and frozen action keys.
Each due tick may dispatch one `RECOVERY_FIRST` resume of the same round;
repeated failure increments `retry_epoch` and yields again. This cross-wake loop
continues without deleting the Heartbeat or creating a new executor/round.

For a misbound/duplicate/misconfigured scheduler, do no dispatch. Repair the
exact binding in place; if replacement is unavoidable, verify the corrected
replacement before disabling the old one. Never create a per-round substitute.
Explicit stop, `operation_stop_at`, or objective completion stops new TikTok
work and requests release. Keep the finite cleanup wake until `RUN_RELEASED` or
cleanup `UNTIL`; at unresolved expiry record `RELEASE_UNCERTAIN`, delete/read
back the timer, and do not archive.

Treat `ACTIVE` plus no future occurrence before cutoff as
`MISSION_SCHEDULER_EXPIRED`. While the mission is live, repair the same exact
15-minute repeat-on schedule in place; after cutoff, finalize rather than
reviving missed work.

## Lane breakers

- Favorite, Repost, Like, proactive comment, cultivation reply, comment Like,
  Not interested, follow, publishing, and profile edit are separate capability
  sub-lanes. Proactive comment and cultivation reply may share one authorized
  comment budget; a failure in either remains scoped to the exact action.
- Missing persistence or post-action proof never disables a lane. Record
  `attempted`; only the exact uncertain target/action is not retried.
- Write `MUTATION_INTENT` plus a stable `action_key` before the native call. A
  tool timeout after the call may have been issued becomes `MUTATION_UNKNOWN`;
  that key is never issued again after recovery.
- Two consecutive native For You transition failures disable only held-out Feed
  validation; qualified search training continues.
- Empty candidates produce a completed no-action checkpoint and cluster
  rotation, never a mission block.
- Malformed ledger data pauses mutation for bounded repair; it does not delete,
  pause, or duplicate the mission scheduler and does not require user confirmation.

## Whole-mission hard boundary

Use only `blocker-minimization.md`'s live human-repair whitelist. The executor
callbacks exact evidence and releases owned Chrome when appropriate; the main
task asks the user. Historical evidence never opens a circuit.

## Independent-run stability

Main and executor coordinate only with each other's exact registered IDs. Never
inspect unrelated TikTok tasks, claim their tabs, modify their automations, or
create a same-account lock.
