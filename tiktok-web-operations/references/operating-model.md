# Launcher And Self-Owned Executor

Use two user-visible persistent Codex tasks for one run:

```text
TikTok 启动台 --healthy preflight, same task--> pinned TikTok 分发台
TikTok 分发台 --one-way assignment--> TikTok 执行台
TikTok 分发台 --after acceptance--> reusable stateless idle
TikTok 执行台 --self-owned one-shot wake--> same TikTok 执行台
same TikTok 分发台 --later new command--> another fresh TikTok 执行台
```

There is no long-term coordinator, callback, centralized scheduler, supervisor
Heartbeat, or risk-return path. Both tasks use `gpt-5.6-luna` with
`thinking=high`. Never substitute a subagent, Goal Mode, or an agent tree.

## One-way assignment

1. Launcher verifies its title, bundle, tools, Chrome control, TikTok account,
   writable storage, local time, and ability to create the required task/profile.
2. After health proof, rename this exact task `TikTok 分发台`, attempt to pin it,
   and verify the exact task ID with `pinned=true` when readback exists. Pin or
   rename failure is presentation degradation, never a dispatch blocker. Do not
   pin the executor.
3. Require the Bootstrap profile-lock proof: `profile_status=CONFIRMED`, positive
   `direction_profile_version`, exact confirmation evidence, and zero prior
   executor/search/view/mutation for this run. Only then resolve
   `direction_profile`, `authority_envelope`, `mission`, ledger path,
   `operation_stop_at`, and a brand-new unique `run_id`. Do not read or inherit
   any old mission, registry, Heartbeat, tab, ledger, task ID, or owner state.
4. Set `fresh_only_dispatch=true` and call `create_thread` exactly once to create
   a new executor with an inert `executor_bootstrap/v1` object:

```json
{
  "schema":"executor_bootstrap/v1",
  "run_id":"<uuid>",
  "role":"TIKTOK_EXECUTOR",
  "execution_profile":{"model":"gpt-5.6-luna","thinking":"high"},
  "external_work":"forbidden_until_assignment_acceptance"
}
```

5. Record only the exact new ID returned by this create call and set its title
   `TikTok 执行台`. Same-name titles are non-unique presentation. Do not call
   list/search/read on any historical task, and do not reuse, unarchive, revive,
   message, archive, replace, or otherwise modify one.
6. Serialize one canonical `executor_assignment/v1` as UTF-8 JSON using
   `sort_keys=True` and `separators=(",", ":")`. Store byte length and SHA-256.
7. Send those exact stored bytes once to the exact new executor. Required fields:

```json
{
  "schema":"executor_assignment/v1",
  "assignment_id":"<uuid>",
  "run_id":"<uuid>",
  "executor_thread_id":"<exact returned id>",
  "role":"TIKTOK_EXECUTOR",
  "execution_profile":{"model":"gpt-5.6-luna","thinking":"high"},
  "account":{"platform":"tiktok","handle":"<verified handle>"},
  "direction_ref":{"id":"...","version":1,"sha256":"..."},
  "authority_ref":{"id":"...","version":1,"sha256":"..."},
  "mission_ref":{"id":"...","version":1,"sha256":"..."},
  "ledger_path":"<private run path>",
  "dedicated_tab_policy":"EXECUTOR_OWNED",
  "automation_policy":"EXECUTOR_SELF_OWNED_ONE_SHOT_CHAIN",
  "launcher_contact_policy":"NO_CALLBACK_NO_SUPERVISION"
}
```

8. Executor validates exact ID, role, profile, refs, bytes, and hash; stores the
   assignment unchanged; writes `ASSIGNMENT_ACCEPTED` in its own task/ledger;
   then starts the read-only smoke. A mismatch is
   `ASSIGNMENT_RECONCILIATION_REQUIRED` before Chrome or mutation.
9. Distributor may perform one immediate read of the exact newly-created executor
   solely to confirm `ASSIGNMENT_ACCEPTED`. This is handoff validation, not
   monitoring. It releases its bootstrap tab, records `EXECUTOR_ASSIGNED`, and
   becomes idle. It neither waits for smoke proof nor reads the task again.

At reusable idle, a later user command starts another independent pass through
the profile lock and then steps 1–9 with a new `run_id` and another fresh
executor. The launcher carries
forward only installed dependency configuration and current preflight ability;
it carries no old assignment, result, mission, registry, ledger, timer, tab,
risk, or progress. It never compares or summarizes runs.

If `create_thread` fails, or its result is uncertain and no exact new returned ID
is available, record `FRESH_TASK_CREATION_FAILED` or
`FRESH_TASK_CREATION_UNKNOWN`, report this launch failure, and stop. Do not list
tasks to discover whether one appeared, do not retry creation in the same
launch, and do not fall back to or modify any historical executor. If the exact
fresh ID exists but assignment acceptance fails, report
`FRESH_TASK_ASSIGNMENT_FAILED`; do not replace it or use an old task.

## Executor initialization

After acceptance, executor:

1. creates its own ledger/checkpoint state;
2. performs one read-only search-origin stability smoke;
3. starts real mission work immediately with no standing timer;
4. completes the first 25–45-view round and durable checkpoint;
5. creates/read-backs one unique self-target single-occurrence wake before its
   first inter-round yield.

Training units inside one round continue without a timer pause. After each
completed 25–45-view round, persist `cooldown_minutes` and `cooldown_until`,
create exactly one wake named by full run ID and round sequence, validate it,
perform zero TikTok work for 10–20 minutes, then resume from that wake. Consume
and retire the one-shot before starting the next round.

## Self one-shot wake contract

The executor is simultaneously automation manager and target:

```text
automation_role=executor_one_shot_wake
automation_manager_thread_id=executor_thread_id
targetThreadId=executor_thread_id
timer_id=tiktok-wake-<run_id>-round-<round_seq>
occurrences=1
next_wake_at < operation_stop_at
```

Read back every create. Yield only after exact ID, self target, run ID, round
sequence, single-occurrence state, next local/UTC wake, and cutoff validate. A
valid wake requires `waking_thread_id == targetThreadId == executor_thread_id`
plus matching run/round/timer ID. A mismatch, duplicate, late wake, or overlap
performs no TikTok action.

On valid wake, write `ONE_SHOT_WAKE_CONSUMED`, delete/retire the expired timer if
still visible, clear the pending binding, and resume. Network, Chrome, route,
renderer, Feed transition, empty candidates, and lane failures remain locally
recoverable. If later retry requires yield, create one recovery-sequence-unique
single-occurrence wake. Uncertain mutation is never retried. Never callback the
distributor, never keep a repeat-on executor timer, and never use a global
`executor-heartbeat` ID.

## Independent-run invariant

Each executor uses its own exact task ID, `run_id`, ledger directory, automation
ID, and newly created Chrome tab. It does not list/read other TikTok tasks,
search for same-account owners, claim their tabs, modify their timers, or pause
because they exist. Cross-run recommendation attribution may therefore be
uncertain; report feed movement as observed composition, never sole causation.

Within its own ledger, avoid repeating the same target/action and never repeat
an uncertain submission.

## Reporting and hard blockers

No callback schema exists. All progress, risk, user decisions, and final results
stay in `TikTok 执行台`. Timed receipts are exactly:

```text
本轮完成：<one sentence>
下次心跳：<verified local date, time, and timezone, or why none exists>
下轮计划：<one bounded purpose>
```

Ordinary recoveries are ledger entries, not user interruptions. Only the current
human-only hard-blocker whitelist triggers a direct executor question.

## Finalization

On user stop, cutoff, or objective completion:

1. stop new browsing and mutation;
2. never retry an uncertain submission;
3. release only the executor's tabs;
4. reconcile final ledger/capability state;
5. delete the exact pending one-shot wake if one exists;
6. write `RUN_RELEASED` and a compact result in the executor task.

The executor never contacts the distributor, and no system polls, unarchives, or
repurposes it. It remains available only for the user to request another fresh
one-way dispatch.
