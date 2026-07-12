# Startup Health Check And Reusable Fresh Dispatch

Use this reference for install, upgrade, or first mission launch. The launcher
performs preflight and one-way assignment; it never becomes a coordinator.
After initial setup, the same launcher remains a reusable stateless dispatch
entry. Later commands use quick current health checks, not historical run state.

## Preflight record

```text
launcher_title: TikTok 启动台 | TikTok 分发台 | DEGRADED_RENAME_UNAVAILABLE
dispatcher_pin: TRUE | DEGRADED_PIN_UNAVAILABLE | UNVERIFIED
bundle_action: INSTALL | UPGRADE | NOOP | DEFERRED_ACTIVE_RUNTIME | BLOCKED
bundle_version:
skill_validation: PASSED | FAILED
chrome_control: AVAILABLE | RECONNECTED | UNAVAILABLE
tiktok_session: LOGGED_IN:@handle | LOGGED_OUT | UNVERIFIED
account_warning: NONE_VISIBLE | PRESENT | UNVERIFIED
thread_tools: READY | UNAVAILABLE
fresh_only_dispatch: REQUIRED
fresh_create_attempts: 0 | 1
fresh_executor_thread_id: NONE | exact newly returned id
fresh_create_state: NOT_STARTED | CREATED | FAILED | UNKNOWN
executor_profile_support: gpt-5.6-luna/high | UNAVAILABLE
one_shot_wake_support: AVAILABLE | UNAVAILABLE
canonical_store: WRITABLE | UNAVAILABLE
dedicated_tab_creation: AVAILABLE | UNAVAILABLE
local_time:
ledger_path:
dependency_status: READY | HARD_REPAIR_REQUIRED
profile_status: DRAFT | PROPOSED | CONFIRMED
direction_profile_version: NONE | positive integer
profile_confirmation_evidence: NONE | exact user turn/ref
```

## Ordered checks

1. First available presentation action: set title `TikTok 启动台`. On tool
   failure record `DEGRADED_RENAME_UNAVAILABLE` and continue.
2. Download and validate the canonical GitHub bundle; apply
   `version-management.md`. A valid newer bundle upgrades automatically. Never
   merge trees or hot-reload an active managed runtime.
3. Create one disposable Chrome tab and prove Chrome control. Classify and
   bounded-recover errors using `runtime-and-recovery.md`.
4. Open TikTok read-only; prove exact logged-in handle and absence of a current
   blocking challenge/warning. Never enter credentials or codes.
5. Prove task create/read/title/message tools and `automation_update` support.
   Prove executor creation with `gpt-5.6-luna` and `thinking=high`.
6. Prove a private canonical object store and writable ledger path. Read local
   time and calculate finite `operation_stop_at`.
7. Prove a newly created executor can own a dedicated Chrome tab and create a
   self-target single-occurrence heartbeat-kind wake with unique caller-supplied
   ID. Do not create the real timer in preflight.
8. Finalize only the disposable launcher tab.
9. After all required health checks pass, rename this exact task
   `TikTok 分发台`, attempt to pin it, and read back the exact task ID with
   `pinned=true` when supported. A rename/pin failure is presentation degradation
   and does not block the profile gate or dispatch. Never pin an executor.

Do not list, inspect, interrupt, archive, or coordinate with other TikTok tasks.
Another Chrome/TikTok owner is irrelevant to this run's preflight. The installer
may inspect active managed runtimes only for safe bundle hot-reload fencing; it
does not use that inspection as operational coordination.

## Bootstrap profile lock

After healthy preflight, lock the account image before mission creation. No
executor, TikTok search, watched video, or outward interaction may exist while
`profile_status != CONFIRMED`.

Use at most two user-facing rounds:

1. If direction is missing, ask one open question covering account identity,
   target audience, and intended future posts. If the user's initial message is
   already specific, skip this question.
2. Infer and display one structured proposal with:
   `persona_name`, `target_audience`, `region_language`, 3–5
   `content_pillars`, `excluded_topics`, `voice_and_comment_style`,
   `future_post_alignment`, duration/intensity, and interaction policy. Ask for
   confirmation or final replacement values. Supplied replacement values count
   as confirmation unless the user explicitly requests another draft.

Record `profile_status=PROPOSED` and the exact proposal hash before asking. On
confirmation, persist `profile_status=CONFIRMED`, increment
`direction_profile_version`, and store exact user evidence. Only then create the
canonical `direction_ref` used by assignment.

A detailed request that supplies a usable direction and explicitly asks to
start/operate is canonical confirmation; fill reversible omissions from the
declared safe defaults and dispatch after the distributor rename/pin without an
extra question. Advice/review wording without a start request is not
confirmation. A bare `继续`/`开始`
confirms only a proposal already visible in this launcher. If none exists,
display the default proposal and wait.

## Resolve confirmed mission

Apply explicit values first. Safe defaults:

- direction: North American college/dorm life;
- duration: 3 hours, standard intensity;
- universal lifestyle region/language: `global English with North American bias`;
- cultivation lanes: Like/Favorite/Repost/Comment are four independent
  `best_effort_attempt` lanes with `parallel_engagement=true`;
- browse-only lanes: all mutations disabled.

Defaults fill missing proposal fields; they never bypass confirmation.

## Create and hand off

Follow `operating-model.md`:

1. require `profile_status=CONFIRMED` and one exact confirmed
   `direction_profile_version`; otherwise stop before creation;
2. generate a new `run_id`; make exactly one fresh `create_thread` attempt for a
   new `TikTok 执行台` with Luna/High and inert bootstrap;
3. store only that call's exact newly returned ID;
4. send one canonical `executor_assignment/v1` referencing the confirmed
   `direction_ref`;
5. require `ASSIGNMENT_ACCEPTED` before external work;
6. release launcher Chrome and record `EXECUTOR_ASSIGNED`;
7. pinned distributor becomes `L2_IDLE` and performs no later
   supervision/callback work.

On every later new operating instruction sent to the same launcher, repeat only
the current dependency/account health checks and the fresh create/assignment
steps with a new run ID. Do not repeat installation unless version management
requires it. After acceptance return to `L2_IDLE` again. This is a new dispatch,
not continuation or aggregation of an old run.

The launcher must not list/search/read historical tasks, choose a same-title
task, reuse/unarchive/revive/message/archive/replace an old executor, or inherit
an old mission/registry/Heartbeat/tab/ledger. Old archived, completed, and live
runs remain untouched. A create failure/unknown result ends this launch with one
fresh-task error report and no fallback or replacement.

The executor then performs the read-only smoke and starts real mission work with
no standing timer. At its first completed round it creates/read-backs its own
run/round-unique one-shot wake before cooldown. Future user interaction goes
directly to `TikTok 执行台`.

## User-facing handoff

When no account image was supplied, the already renamed/pinned distributor asks:

```text
TikTok 已准备好，当前账号：@handle。
下一步只要告诉我：想把账号做成什么方向，以及运营多久。
例如：“做北美宠物账号，持续 10 小时。”不确定就回复：“用默认设置开始。”
```

Do not append architecture, dependency, capability-matrix, profile-field, or
policy explanations to this successful handoff. A reply containing direction
and optional duration is an explicit operating instruction in this context;
compile reversible omissions from defaults and dispatch without another
confirmation. `用默认设置开始` confirms all packaged defaults and dispatches
directly. Never turn either reply into another proposal-confirmation round.

For a bare `继续`/`开始` that is not the exact default command and has no visible
proposal, show the default proposal and wait once. Never say operation started
before the applicable confirmation.
When the initial request contains a usable direction and explicit start/operate
instruction, compile it as the confirmed profile and dispatch without an extra
question. If it is detailed but asks only for advice/review, show the structured
proposal and obtain confirmation before dispatch.
