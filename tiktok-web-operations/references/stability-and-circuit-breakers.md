# Stability And Circuit Breakers

The executor owns recovery and one self-target recurring Heartbeat. Circuit
breakers are lane/surface scoped unless the hard-blocker whitelist is proven.

## Heartbeat survival invariant

The forbidden transition is `ordinary failure -> delete Heartbeat`. Keep the
valid executor Heartbeat repeat-on through network, Chrome, route, renderer,
Feed transition, empty-candidate, lane, and uncertain-mutation failures.

Each later wake rechecks the stored `auto_resume_condition`. An uncertain
submission is never retried. Unaffected search/view and action lanes continue.

For a misbound/duplicate/misconfigured timer: create and read back the correct
replacement first, switch the executor's stored automation binding, then retire
the old timer. Never create a continuation gap.

Retire only for explicit user stop, `operation_stop_at`, objective completion,
or terminal executor release. No launcher/coordinator/supervisor timer exists.

## Lane breakers

- Favorite, Repost, Like, proactive comment, comment Like, Not interested,
  follow, reply, publishing, and profile edit are separate lanes.
- Missing persistence or post-action proof never disables a lane. Record
  `attempted`; only the exact uncertain target/action is not retried.
- Two consecutive native For You transition failures disable only held-out Feed
  validation; qualified search training continues.
- Empty candidates produce a completed no-action checkpoint and cluster
  rotation, never a mission block.
- Malformed ledger data pauses mutation for bounded repair; it does not delete
  the timer or require user confirmation.

## Whole-mission hard boundary

Use only `blocker-minimization.md`'s live human-repair whitelist. The executor
asks directly, keeps its timer, releases owned Chrome while waiting, and resumes
after verified clearance. Historical evidence never opens a circuit.

## Independent-run stability

Never list/read other TikTok tasks, inspect their status, claim their tabs,
modify their automations, or create a same-account lock. Isolation is by exact
executor task ID, run ID, ledger, timer, and newly created Chrome tab.
