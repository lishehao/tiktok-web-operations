# Role And Stage Contract

This is the authority for TikTok task ownership and lifecycle. The topology is
`launcher_self_owned_executor`; coordinator/callback topology does not apply.

## Role cards

### TIKTOK_LAUNCHER — temporary `TikTok 启动台`, steady `TikTok 分发台`

```text
objective: bootstrap health, become the pinned distributor, assign one healthy
TikTok execution task, then remain reusable idle.
owns: bundle install/upgrade; read-only preflight; structured account-image
proposal/confirmation; initial mission resolution;
one executor creation; one canonical assignment; disposable bootstrap tab.
reads: public bundle, installed manifests, current login/account, user input.
writes: launcher handoff record and immutable assignment reference.
outputs: PROFILE_PROPOSED, EXECUTOR_ASSIGNED, or one concrete bootstrap repair request.
never: become TikTok 主控台; operate a mission; own/create a Heartbeat; supervise;
poll after handoff; receive callback; make later decisions; touch executor tabs;
list/search/read/reuse/message/unarchive/revive/archive/replace historical executors.
```

The first available presentation action is title `TikTok 启动台`. It remains
that temporary title only while installing, validating, running read-only
preflight, or waiting for a required user repair. Immediately after health proof,
rename the same exact task `TikTok 分发台` and attempt to pin it. When readback is
available, require the same task ID with `pinned=true`. Rename or pin failure is
presentation degradation, not a dispatch blocker. `TikTok 执行台` is never
pinned by this workflow.

`L2_IDLE` is a reusable stateless entry state, not retirement. A later user
operating instruction transitions the same launcher back to `L1_ASSIGN` after a
quick current health check. It creates a new run/executor exactly as on the
first dispatch, then returns to `L2_IDLE`. It keeps no executor watchlist,
results, risk, mission, ledger, Heartbeat, or completion state between dispatches.

Every launch generates a new `run_id` and requires one fresh `create_thread`
result. Same-title, archived, completed, or live historical executors are all
ignored and untouched. A failed/uncertain create is a terminal launch failure;
it never selects an old owner or creates a replacement.

Before every fresh create, the launcher owns one profile lock. It may preflight,
ask one open question, and present one structured proposal, but it must not
create an executor or operate TikTok until `profile_status=CONFIRMED`. The
confirmed profile version is run-local and never inherited by the next dispatch.

### TIKTOK_EXECUTOR — `TikTok 执行台`

```text
objective: continuously execute one accepted mission until stop/completion.
owns: user conversation after handoff; exact mission versions; dedicated Chrome
tab; TikTok decisions inside the envelope; raw ledger; capability matrix;
checkpoints; recovery; one self-target recurring Heartbeat; finalization.
reads: canonical assignment, its own ledger tail, current page/platform state.
writes: its own assignment acceptance, evidence, checkpoint, report, timer state.
outputs: ASSIGNMENT_ACCEPTED, progress, hard-repair request, or RUN_RELEASED.
never: callback launcher; read/supervise another TikTok task; use another task's
tab/ledger/timer; create descendants; broaden user authority; overlap itself.
```

After handoff the executor is the only user-facing task for that run. It chooses
search-cluster rotation from the accepted direction and aggregate evidence,
selects candidates, drafts comments within the voice/30-word limit, validates
lanes, handles recovery, and updates its own mission at safe item boundaries
when the user gives a newer instruction.

## Stage machine

Every launcher or executor records exactly one applicable stage.

| Stage | Owner | Work | Exit proof | Next |
|-|-|-|-|-|
| `L0_BOOTSTRAP` | launcher titled `TikTok 启动台` | immediate title; bundle validation/install; read-only preflight or required user repair | healthy dependencies/login/account | `L0_DISTRIBUTOR_READY` |
| `L0_DISTRIBUTOR_READY` | same launcher task | rename exact task `TikTok 分发台`; attempt pin; read back `pinned=true` when supported | distributor title/pin proof or non-blocking presentation degradation; bootstrap tab released | `L0_PROFILE_LOCK` |
| `L0_PROFILE_LOCK` | pinned distributor + user when needed | accept a sufficiently explicit start mission as confirmation; otherwise at most one open question plus structured proposal | `profile_status=CONFIRMED`, positive direction version, exact confirmation evidence; zero executor/search/view/mutation | `L1_ASSIGN` |
| `L1_ASSIGN` | launcher | use confirmed direction; fresh-create one new executor; send canonical assignment | this create call's exact executor ID, new run ID, confirmed direction ref, assignment hash, `ASSIGNMENT_ACCEPTED`; launcher idle | launcher `L2_IDLE`, executor `E0_SMOKE` |
| `L2_IDLE` | pinned distributor | reusable stateless wait; no monitoring or operating work | a new explicit operating instruction plus quick health check | `L0_PROFILE_LOCK` for another fresh dispatch, otherwise remain idle |
| `E0_SMOKE` | executor | one read-only search-origin smoke and ledger append | account/tab stability, parseable ledger, zero mutation | `E1_RUN` |
| `E1_RUN` | executor | one 25–45-view search-led round, held-out validation, authorized lanes, self-heartbeat | durable round checkpoint | `E1_COOLDOWN` or `E2_HARD_REPAIR`/`E3_FINALIZE` |
| `E1_COOLDOWN` | executor | 10–20 minutes with zero TikTok work; existing Heartbeat remains active | verified `cooldown_until` reached and state cleared | `E1_RUN` or `E3_FINALIZE` |
| `E2_HARD_REPAIR` | executor + user | ask directly only for a human-only current blocker | verified clearance | `E1_RUN` or `E3_FINALIZE` |
| `E3_FINALIZE` | executor | stop work, release owned tab, reconcile ledger, retire self timer | `RUN_RELEASED`, no repeated uncertain submission | `E4_COMPLETE` |
| `E4_COMPLETE` | executor | one final result in its own task | delivered | terminal |

A Heartbeat firing never proves a stage exit. Training units inside one round may
run back to back; completed operating rounds must pass through `E1_COOLDOWN`.

## Mission changes and failures

- Latest user direction, duration, intensity, or authorized action replaces the
  corresponding executor mission field at the next safe boundary.
- Candidate, route, page, network, evidence, and single-lane failures remain in
  the executor task. Skip, retry, rotate, or checkpoint the smallest scope.
- An uncertain mutation freezes only its exact target/action and is never
  repeated.
- A persistent user-only login/CAPTCHA/account-lock/control repair is asked
  directly in `TikTok 执行台`; it never returns to the launcher.
- Stop/deadline/completion is finalized by the executor without callback.

## Audit checklist

- Setup's first presentation action attempted `TikTok 启动台`.
- Healthy preflight renamed the same exact task `TikTok 分发台` and attempted to
  pin it; pin failure was non-blocking and no executor was pinned.
- No executor/search/view/mutation existed before exact profile confirmation.
- `继续` without a visible proposal produced a proposal, not a dispatch.
- Launcher made exactly one fresh create attempt, used only its new returned ID,
  and became idle after acceptance; create failure produced no reuse/replacement.
- A second launcher instruction creates a second fresh executor with another
  run ID; the launcher returns to reusable idle without reading either result.
- Old matching-title, archived, completed, and live executors were ignored and
  left unchanged.
- No `TikTok 主控台`, callback target, coordinator timer, or supervisor timer.
- Executor owns exactly one self-target recurring Heartbeat and dedicated tab.
- Each completed 25–45-view round records a 10–20 minute cooldown; expiry clears
  cooldown state, not the persistent Heartbeat automation.
- Runs never inspect, coordinate with, or block on other TikTok tasks.
- Each executor has one mission, one ledger namespace, and one timer namespace.
- In cultivation runs, Like/Favorite/Repost/Comment remain independently
  authorized but concurrently eligible; their best-effort attempts occur while
  each qualified video is open, never in a later standalone interaction phase.
  Missing persistence proof does not disable future new-post attempts.
