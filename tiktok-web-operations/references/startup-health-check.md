# Startup Health Check And Main-Task Handoff

Use this reference for install, upgrade, and mission launch. The same setup task
becomes the pinned `TikTok 主控台` and remains the mission control surface.

## Preflight record

```text
coordinator_title: TikTok 启动台 | TikTok 主控台 | DEGRADED_RENAME_UNAVAILABLE
coordinator_pin: TRUE | DEGRADED_PIN_UNAVAILABLE | UNVERIFIED
bundle_action: INSTALL | UPGRADE | NOOP | DEFERRED_ACTIVE_RUNTIME | BLOCKED
bundle_version:
skill_validation: PASSED | FAILED
chrome_control: AVAILABLE | RECONNECTED | UNAVAILABLE
chrome_content_channel: AVAILABLE | CHROME_CONTENT_CHANNEL_TIMEOUT | UNVERIFIED
tiktok_session: LOGGED_IN:@handle | LOGGED_OUT | UNVERIFIED
account_warning: NONE_VISIBLE | PRESENT | UNVERIFIED
thread_tools: READY | UNAVAILABLE
callback_tools: READY | UNAVAILABLE
automation_update: READY | UNAVAILABLE
canonical_store: WRITABLE | UNAVAILABLE
dedicated_tab_creation: AVAILABLE | UNAVAILABLE
local_time:
coordinator_ledger_path:
dependency_status: READY | HARD_REPAIR_REQUIRED
profile_status: DRAFT | PROPOSED | CONFIRMED
direction_profile_version: NONE | positive integer
profile_confirmation_evidence: NONE | exact user turn/ref
```

## Ordered checks

1. First available presentation action: set title `TikTok 启动台`. On failure,
   record `DEGRADED_RENAME_UNAVAILABLE` and continue.
2. Download and validate the canonical GitHub bundle; apply
   `version-management.md`. Never mix two bundle versions.
3. Prove the existing Chrome browser binding, then create one disposable tab.
   An empty tab list is normal after cleanup; only an explicit disconnect
   invalidates the browser binding. Use `runtime-and-recovery.md` for layered
   control, tab metadata, content-channel, scope-probe, and account classification.
4. Open TikTok read-only; prove exact logged-in handle and absence of a current
   blocking challenge/warning. Never enter credentials or codes.
5. Prove thread create/read/title/message tools and `automation_update` exist.
   Do not pretend that tool presence proves callback or scheduler behavior.
6. Prove writable canonical/coordinator/executor ledger paths and calculate a
   finite `operation_stop_at` from machine time.
7. Finalize only the disposable setup tab.
8. After health proof, rename this same task `TikTok 主控台`, attempt to pin it,
   and read back exact ID plus `pinned=true` when supported. Presentation failure
   does not block the profile gate. Never pin the executor.

Do not inspect unrelated TikTok tasks. Another Chrome/TikTok owner is not a
blocker. Active-runtime inspection is allowed only for version replacement
safety, not operational coordination.

Before mission authorization, preflight never creates a retry Heartbeat. If one
bounded pass still shows a transient Chrome/network/render fault, record
`PREFLIGHT_RECOVERY_PENDING` rather than TikTok/account risk and retry in the
current setup turn when the control surface permits. Ask the user only for the
hard-repair whitelist. After an authorized mission scheduler exists, all later
Chrome retries use the persistent cross-wake contract in
`runtime-and-recovery.md`.

## Bootstrap profile lock

No executor, TikTok search, watched video, or outward interaction may exist
while `profile_status != CONFIRMED`.

Use at most two user-facing rounds:

1. If direction is missing, ask one open question covering account identity,
   target audience, and intended future posts. Skip when already clear.
2. Display one structured proposal with persona, audience, inferred
   region/language, 3–5 pillars, exclusions, comment voice, future-post
   alignment, duration/intensity, and interaction policy. User corrections count
   as confirmation unless another draft is explicitly requested.

A detailed request that supplies a usable direction and asks to start/operate is
canonical confirmation; fill reversible omissions from defaults and do not ask
again. A bare `继续` confirms only a visible proposal. `用默认设置开始` confirms
the packaged defaults.

Safe defaults:

- direction: North American college/dorm life;
- duration: 3 hours, standard intensity;
- universal lifestyle region/language: global English with North American bias;
- cultivation lanes: Like/Favorite/Repost/Comment independently eligible with
  `parallel_engagement=true`;
- browse-only wording: all mutations disabled.

Defaults fill missing proposal fields; they never bypass profile confirmation.

## Create, reuse, handshake, schedule, dispatch

Follow `operating-model.md`:

1. require confirmed profile and exact canonical refs;
2. at a new-mission boundary, generate one new run ID and fresh-create exactly one unpinned
   `TikTok 执行台`; store only the exact new ID;
3. set that exact new ID's title to `TikTok 执行台` and verify same-ID readback
   when supported; record non-blocking title degradation if unavailable;
4. send `executor_assignment/v2` and require `ASSIGNMENT_ACCEPTED`;
5. perform real `CALLBACK_PING/v1` -> `CALLBACK_ACK/v1` to the exact main task;
6. create one stable main-target mission recurring Heartbeat under the direct
   user mission authorization and read back exact ID, target, `ACTIVE` repeat-on
   15-minute cadence, next local/UTC run, cutoff, and cleanup `UNTIL`;
7. dispatch round 1 immediately and enter callback wait.

If callback handshake fails, perform no TikTok external work and report
`CALLBACK_UNAVAILABLE`. If the scheduler is only suggested or lacks exact
ID/readback, do not claim multi-hour unattended continuation; report
`SCHEDULER_CONTINUATION_FAILURE`. Never ask the executor to create a substitute.

Historical same-title tasks are not candidates. A fresh create failure/unknown
result ends this launch without title search, reuse, unarchive, or replacement.
Title normalization failure does not change this rule and never authorizes a
title search or duplicate create.

After launch, keep that exact executor for all rounds and all continuation or
direction messages within the same active mission. Do not repeat profile setup,
change `run_id`, or call `create_thread` because the executor returned IDLE.
Version any changed refs and send them with the next bounded assignment.

If the registry lacks an exact executor ID, or the exact registered executor is
proven `STALE_OWNER_TOMBSTONE`, retired, archived, or released while the mission
is still active, create at most one replacement for the same `run_id`. Increment
`executor_generation`, store old/new exact IDs, reason, timestamp, and last
accepted cursor, then repeat assignment acceptance and callback handshake before
resuming. `notLoaded`, empty/unavailable task read, host/network failure, or
transient tool failure never proves absence. A failed or uncertain replacement
does not permit another create. A post-terminal instruction starts a new mission.

## User-facing handoff

When direction is missing, use this three-line novice handoff and say only:

```text
TikTok 已准备好，当前账号：@handle。
下一步只要告诉我：想把账号做成什么方向，以及运营多久。
例如：“做北美宠物账号，持续 10 小时。”不确定就回复：“用默认设置开始。”
```

A direction/duration reply dispatches without another confirmation round.
Do not append architecture, callback, scheduler, registry, or capability
terminology to this beginner-facing handoff.
