# Role And Stage Contract

This is the authority for TikTok task ownership and lifecycle. The topology is
`launcher_self_owned_executor`; coordinator/callback topology does not apply.

## Role cards

### TIKTOK_LAUNCHER — `TikTok 启动台`

```text
objective: establish one healthy, assigned TikTok execution task, then idle.
owns: bundle install/upgrade; read-only preflight; initial mission resolution;
one executor creation; one canonical assignment; disposable bootstrap tab.
reads: public bundle, installed manifests, current login/account, user input.
writes: launcher handoff record and immutable assignment reference.
outputs: EXECUTOR_ASSIGNED or one concrete bootstrap repair request.
never: become TikTok 主控台; operate a mission; own/create a Heartbeat; supervise;
poll after handoff; receive callback; make later decisions; touch executor tabs.
```

The first available presentation action is title `TikTok 启动台`. Healthy
handoff does not rename or promote this task. It remains launcher and becomes
idle. Rename failure is `DEGRADED_RENAME_UNAVAILABLE`, not a blocker.

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
| `L0_BOOTSTRAP` | launcher | immediate title; bundle validation/install; read-only preflight | healthy dependencies/login/account and released bootstrap tab | `L1_ASSIGN` |
| `L1_ASSIGN` | launcher | resolve defaults; create one executor; send canonical assignment | exact executor ID, assignment hash, `ASSIGNMENT_ACCEPTED`; launcher idle | launcher `L2_IDLE`, executor `E0_SMOKE` |
| `L2_IDLE` | launcher | no monitoring or operating work | none; new work requires a new explicit setup/mission invocation | terminal idle |
| `E0_SMOKE` | executor | one read-only search-origin smoke and ledger append | account/tab stability, parseable ledger, zero mutation | `E1_RUN` |
| `E1_RUN` | executor | continuous search-led training, held-out validation, authorized lanes, self-heartbeat | durable checkpoints until stop/cutoff | remain or `E2_HARD_REPAIR`/`E3_FINALIZE` |
| `E2_HARD_REPAIR` | executor + user | ask directly only for a human-only current blocker | verified clearance | `E1_RUN` or `E3_FINALIZE` |
| `E3_FINALIZE` | executor | stop work, release owned tab, reconcile ledger, retire self timer | `RUN_RELEASED`, no repeated uncertain submission | `E4_COMPLETE` |
| `E4_COMPLETE` | executor | one final result in its own task | delivered | terminal |

A Heartbeat firing never proves a stage exit. Logical units may run back to back
without waiting for a timer.

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
- Launcher created at most one executor and became idle after acceptance.
- No `TikTok 主控台`, callback target, coordinator timer, or supervisor timer.
- Executor owns exactly one self-target recurring Heartbeat and dedicated tab.
- Runs never inspect, coordinate with, or block on other TikTok tasks.
- Each executor has one mission, one ledger namespace, and one timer namespace.
