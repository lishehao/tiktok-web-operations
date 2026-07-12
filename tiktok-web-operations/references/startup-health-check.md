# Startup Health Check And Reusable Fresh Dispatch

Use this reference for install, upgrade, or first mission launch. The launcher
performs preflight and one-way assignment; it never becomes a coordinator.
After initial setup, the same launcher remains a reusable stateless dispatch
entry. Later commands use quick current health checks, not historical run state.

## Preflight record

```text
launcher_title: TikTok 启动台 | DEGRADED_RENAME_UNAVAILABLE
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
automation_support: AVAILABLE | UNAVAILABLE
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
   self-target repeat-on Heartbeat. Do not create the real timer in preflight.
8. Finalize only the disposable launcher tab.

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

A detailed request is not automatically confirmation unless it explicitly says
the profile is final or to start with that exact profile. A bare `继续`/`开始`
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
7. launcher becomes `L2_IDLE` and performs no later supervision/callback work.

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

The executor then performs the read-only smoke, creates/validates its own
Heartbeat, and starts real mission work in its own task. Future user interaction
goes directly to `TikTok 执行台`.

## User-facing handoff

When no account image was supplied, the launcher asks:

```text
状态健康。当前账号：@handle。
你希望这个账号未来以什么身份、面向什么人群、发布什么内容？一句话描述即可，我会整理成完整画像给你确认。
```

Then present one proposal and wait for `确认`, `继续`, `开始`, explicit final
corrections, or “按此开始”. Never say operation started before that confirmation.
When the initial request already contains a detailed profile, skip the open
question but still display the structured proposal and obtain the one
confirmation unless the user explicitly declared that exact profile final.
