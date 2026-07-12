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

## Resolve initial mission

Apply explicit values first. Safe defaults:

- direction: North American college/dorm life;
- duration: 3 hours, standard intensity;
- universal lifestyle region/language: `global English with North American bias`;
- cultivation lanes: Favorite/Repost/Comment `pending_fresh_gate`; Like disabled;
- browse-only lanes: all mutations disabled.

Ask only when a missing value changes authorization or an irreversible action.
Preferences such as region, intensity, tone detail, and sub-pillar mix normally
use reversible defaults and never block dispatch.

## Create and hand off

Follow `operating-model.md`:

1. generate a new `run_id`; make exactly one fresh `create_thread` attempt for a
   new `TikTok 执行台` with Luna/High and inert bootstrap;
2. store only that call's exact newly returned ID;
3. send one canonical `executor_assignment/v1`;
4. require `ASSIGNMENT_ACCEPTED` before external work;
5. release launcher Chrome and record `EXECUTOR_ASSIGNED`;
6. launcher becomes `L2_IDLE` and performs no later supervision/callback work.

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

When no mission direction/duration was supplied, the launcher may say:

```text
状态健康。当前账号：@handle。
你想把账号运营成什么方向、持续多久？这会影响搜索、观看和评论口吻；收藏、Repost、短评论是可观测活跃度信号，不保证 TikTok 内部权重或曝光。
你也可以直接回复“继续”，我会按北美大学生 / dorm life、3 小时开始。
```

When the initial request already contains a mission, do not wait for this extra
turn: use quick health reuse, resolve defaults, create/assign the executor, and
handoff immediately.
