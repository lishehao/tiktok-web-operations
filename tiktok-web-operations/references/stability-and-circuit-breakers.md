# Stability And Circuit Breakers

The executor owns recovery and at most one pending self-target one-shot wake. Circuit
breakers are lane/surface scoped unless the hard-blocker whitelist is proven.

## One-shot continuation invariant

Do not create a standing timer at startup. The forbidden transition is
`yield required -> no verified one-shot continuation`. At a completed round or
a recoverable retry boundary, create/read-back one run/sequence-unique,
self-target, single-occurrence wake before yielding.

The later wake rechecks the stored `auto_resume_condition`. An uncertain
submission is never retried. Unaffected search/view and action lanes continue.

For a misbound/duplicate/misconfigured timer, do no external work. Delete it
only when exact identity is known; do not create multiple candidates in one
checkpoint. A checkpoint may yield only after one exact timer readback succeeds.

On valid wake, record consumption, retire the expired timer if still visible,
and clear the binding. Explicit stop, `operation_stop_at`, objective completion,
or terminal release deletes the exact pending wake, if any. No distributor,
launcher, coordinator, or supervisor timer exists.

## Lane breakers

- Favorite, Repost, Like, proactive comment, comment Like, Not interested,
  follow, reply, publishing, and profile edit are separate lanes.
- Missing persistence or post-action proof never disables a lane. Record
  `attempted`; only the exact uncertain target/action is not retried.
- Two consecutive native For You transition failures disable only held-out Feed
  validation; qualified search training continues.
- Empty candidates produce a completed no-action checkpoint and cluster
  rotation, never a mission block.
- Malformed ledger data pauses mutation for bounded repair; it does not alter an
  already verified pending wake or require user confirmation.

## Whole-mission hard boundary

Use only `blocker-minimization.md`'s live human-repair whitelist. The executor
asks directly and releases owned Chrome while waiting. If a timed recheck is
useful and authorized, it creates one unique recovery wake; otherwise it waits
for the user's repair. Historical evidence never opens a circuit.

## Independent-run stability

Never list/read other TikTok tasks, inspect their status, claim their tabs,
modify their automations, or create a same-account lock. Isolation is by exact
executor task ID, run ID, ledger, timer, and newly created Chrome tab.
