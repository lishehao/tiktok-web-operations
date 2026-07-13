# Role And Stage Contract

This is the authority for TikTok task ownership. TikTok uses
`coordinator_worker` with one pinned main task and one unpinned executor.

## Role cards

### TIKTOK_COORDINATOR — temporary `TikTok 启动台`, steady `TikTok 主控台`

```text
objective: keep one confirmed mission strategically aligned and continuously
scheduled until stop, cutoff, or completion.
owns: install/preflight; profile and mission; exact executor registry; callback
acceptance; search direction; cooldown; fixed scheduler Heartbeat; user reports;
hard-repair conversation; finalization.
reads: public/installed bundle, current account proof, exact executor callbacks,
coordinator ledger, scheduler readback.
writes: canonical assignments, coordinator checkpoints, next_dispatch_at,
scheduler decisions, user reports.
never: operate TikTok; own an operating Chrome tab; mutate content; accept a
callback from a non-registered task/run/round; dispatch while executor active.
```

The first presentation action is `TikTok 启动台`. After healthy preflight,
rename that same exact task `TikTok 主控台`, attempt to pin it, and keep the task
as the mission's user-facing control surface. Rename/pin failure is non-blocking
presentation degradation. The executor is never pinned.

### TIKTOK_EXECUTOR — `TikTok 执行台`

```text
objective: complete one bounded round assignment accurately and callback.
owns: dedicated Chrome tab; TikTok page state; candidate selection; authorized
actions; raw evidence ledger; within-round recovery; release proof.
reads: exact assignment, own ledger tail, live platform state.
writes: evidence/checkpoints and one structured callback per boundary.
never: own/update/delete Heartbeat; choose cooldown or next strategy; ask the
user directly; contact another task; run after callback while idle; broaden
authority; overlap itself.
```

## Stage machine

| Stage | Owner | Work | Exit proof | Next |
|-|-|-|-|-|
| `C0_BOOTSTRAP` | task titled `TikTok 启动台` | install/upgrade, read-only preflight, required user repair | healthy dependencies/account | `C0_MAIN_READY` |
| `C0_MAIN_READY` | same task | rename `TikTok 主控台`, pin/readback, profile lock | main identity plus confirmed profile | `C1_CREATE` |
| `C1_CREATE` | main | fresh-create one executor and canonical assignment | exact IDs and `ASSIGNMENT_ACCEPTED` | `C1_HANDSHAKE` |
| `C1_HANDSHAKE` | main + executor | exact `CALLBACK_PING/ACK` and scheduler create/readback | callback proof plus verified fixed scheduler | `C2_DISPATCH` |
| `C2_DISPATCH` | main | send exactly one `round_assignment/v1` | `ROUND_DISPATCHED`, executor ACTIVE | main `C3_WAIT`, executor `E1_RUN` |
| `C3_WAIT` | main | await callback; scheduler wakes may no-op | valid callback or terminal signal | `C4_REPLAN` or `C6_FINALIZE` |
| `C4_REPLAN` | main | accept callback, update strategy, machine-calculate cooldown | `next_dispatch_at`, pending next round, executor IDLE | `C5_COOLDOWN` |
| `C5_COOLDOWN` | main scheduler | no-op until due; dispatch once when due | next round dispatched or cutoff | `C3_WAIT` or `C6_FINALIZE` |
| `E0_ACCEPT` | executor | validate assignment and handshake | exact IDs/refs, callback ACK | `E1_RUN` |
| `E1_RUN` | executor | one 25–45-view search-led round plus interactions | durable checkpoint | `E2_CALLBACK` |
| `E2_CALLBACK` | executor | send one `round_callback/v1` | accepted send, executor IDLE | wait for `C2_DISPATCH` or stop |
| `E3_HARD_REPAIR` | executor | stop affected work and callback exact evidence | main/user repair clears state | next assignment or `E4_RELEASE` |
| `E4_RELEASE` | executor | stop, reconcile ledger, release owned tab, callback | `RUN_RELEASED` | terminal |
| `C6_FINALIZE` | main | stop dispatch, delete scheduler, require release proof | scheduler absent and executor released | terminal |

## Callback and scheduler invariants

- Perform a live callback handshake before TikTok work.
- Accept exactly one callback for the expected run/round sequence.
- Executor callbacks and becomes idle after every completed round.
- Main chooses strategy and 10–20 minute cooldown from callback evidence.
- Main owns exactly one fixed recurring scheduler; executor owns zero timers.
- Scheduler wakes no-op before due, while executor is active, or with no pending
  callback-derived round.
- Use fresh machine UTC for `next_dispatch_at`; never trust model-estimated or
  out-of-order ledger timestamps.
- Timer readback without exact automation ID/target/status/next run is not proof.
- User stop, deadline, or completion deletes the scheduler only after stopping
  new dispatch and requesting executor release.

## Failure routing

Ordinary candidate, route, page, network, evidence, and lane failures stay
inside the current bounded round. An uncertain mutation freezes only that exact
target/action. When a failure ends the round, executor callbacks the smallest
scope. Persistent login/account mismatch, CAPTCHA, explicit lock/ban,
credential need, or sole Chrome-control failure returns to the main task; the
main asks the user once. Historical failures never block a clean current run.

## Audit checklist

- Setup attempted `TikTok 启动台`, then same-task `TikTok 主控台` plus pin.
- No executor or TikTok work existed before profile confirmation.
- Exactly one fresh executor ID was registered for the mission.
- Callback ping/ack succeeded before external work.
- Main scheduler was created/read back under direct user authorization.
- Executor owns one tab/ledger and no automation.
- Every 25–45-view round ends in one accepted callback and IDLE state.
- Main chose next clusters, action emphasis, and cooldown from evidence.
- No dispatch happened before `next_dispatch_at` or while executor ACTIVE.
- At terminal state, scheduler deletion and executor release were both proven.
