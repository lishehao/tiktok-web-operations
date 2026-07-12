---
name: tiktok-web-operations
description: >-
  Run authorized TikTok web operations through the user's logged-in Chrome
  session. Covers one-time setup, persistent search-led recommendation
  calibration, Favorites, TikTok Reposts, short comments, publishing,
  analytics, recovery, and a launcher-to-self-owned-executor task topology.
---

# TikTok Web Operations

Operate TikTok from the user's existing logged-in Chrome with durable evidence.
For persistent operation use the `launcher_self_owned_executor` topology from
`$thread-supervisor`: one temporary launcher and one independent execution task.

## Operating objectives

Cultivation missions optimize two observable proxies:

1. `profile_alignment`: qualified search-origin viewing and held-out For You
   samples increasingly match the chosen audience/persona.
2. `account_strength_proxy`: durable, contextual Favorites, TikTok Reposts and
   proactive comments demonstrate genuine community participation.

These are operating proxies, not proof of TikTok's private ranking weights or a
promise of reach. For `运营`, `培养`, `养号`, `增长`, or `增加权重`, default
Favorite, Repost, and proactive comment to `pending_fresh_gate`; keep post Like
disabled unless the user explicitly requests it. Browse-only requests stay
read-only. Zero outward actions is valid only when no qualified candidate
exists, a lane is unavailable, or the action would be repetitive or unsafe;
record the exact reason.

## Roles

### TikTok 启动台 (`TIKTOK_LAUNCHER`)

Its first available presentation action is renaming the current task
`TikTok 启动台`. It has one objective: install/upgrade and validate the bundle,
run read-only Chrome/TikTok preflight, resolve the initial mission using explicit
values plus safe defaults, fresh-create exactly one new `TikTok 执行台`, send one canonical
assignment, verify that the assignment was accepted, release its disposable tab,
then become idle.

The launcher never becomes `TikTok 主控台`, never creates or owns a Heartbeat,
never supervises the execution task, never receives callbacks, and never acts as
a later risk or decision surface. A rename-tool failure is
`DEGRADED_RENAME_UNAVAILABLE`; it does not block setup.

Every setup/bootstrap/new operating start is `fresh_only_dispatch=true`. The
launcher calls `create_thread` once and accepts only that call's newly returned
exact task ID plus a new `run_id`. It must not list, search, read, reuse,
unarchive, revive, replace, message, archive, or modify any historical TikTok
executor. Old tasks remain untouched history whether their title matches, they
are archived, or they are still live. If fresh creation fails or returns an
uncertain result, report `FRESH_TASK_CREATION_FAILED|UNKNOWN` for this launch and
stop; never fall back to an old task or make a replacement create call.

### TikTok 执行台 (`TIKTOK_EXECUTOR`)

It has one objective: execute one accepted mission until user stop, deadline, or
objective completion. It owns its dedicated Chrome tab, direction/authority/
mission versions after assignment, raw ledger, checkpoints, capability matrix,
recovery, user reports, and one self-targeted recurring Heartbeat. Future user
changes and hard-blocker repair happen directly in this task.

The executor never calls back the launcher, never reads or supervises other
TikTok tasks, never claims another task's tab, never creates descendants, and
never treats another Chrome/TikTok owner as a blocker. Independent runs use
independent task IDs, ledgers, Heartbeats, and Chrome tabs.

Read `references/role-and-stage-contract.md` and
`references/operating-model.md` before creating an execution task or Heartbeat.

## Entrypoints

| User request | Behavior |
|-|-|
| Installer/setup prompt | Rename to `TikTok 启动台`, automatically install/upgrade, validate, and run preflight in the same turn. |
| Clear mission with a healthy installation | Reuse only dependency health, resolve safe defaults, and fresh-create/assign a new executor in the same turn. Never reuse an operating task. |
| `继续` or `开始` without details | Default to North American college/dorm life, 3 hours, standard intensity. |
| Direction only | Use that direction and default duration to 3 hours. |
| Duration only | Use the packaged college/dorm direction and that duration. |
| Browse-only wording | Search/view only; do not infer mutation authority. |
| Cultivation/growth wording | Enable Favorite/Repost/Comment as independent `pending_fresh_gate`; Like disabled. |
| `自动发短评论` | Within the accepted audience/language/voice envelope, comments are contextual, preferably 2–12 words, and never over 30 words. |

Do not pause merely to announce an available upgrade or ask again for a value
the user already supplied. Region/language is normally inferred. For universal
lifestyle topics such as pets, food, travel, or humor, default to `global
English with North American bias` unless the user specifies otherwise.

## Mission contract

Resolve and store:

- `persona_name`, `target_audience`, `region_language`;
- `content_pillars`, `excluded_topics`, `voice_and_comment_style`;
- `search_seed_clusters`, `future_post_alignment`;
- `duration`, `operation_stop_at`, intensity, and action authority.

The latest explicit user instruction is the highest operating input within
system safety, current authorization, exact account identity, submission
certainty, and real platform capability. It replaces conflicting defaults,
historical warnings, old mission fields, and recovery suggestions. Historical
ended failures remain ledger evidence only.

## Search-led operating loop

1. Search three distinct approved clusters.
2. Assess the first five results per cluster and open every suitable strong-core
   result. A normal unit contains 9–15 qualified search-origin views; fewer is an
   honest no-action unit, not a blocker.
3. Watch enough to understand premise/payoff and record actual progression when
   available. Search cards and direct-known URLs do not count as qualified
   training views.
4. Evaluate eligible Favorite, Repost, and proactive-comment lanes on genuine
   candidates. Use the smallest genuine signal; do not stack all actions.
5. After two units or roughly 20–30 new qualified views, sample 5–10 sequential
   For You items as held-out validation.
6. Adjust search clusters from rolling evidence and repeat continuously until
   `operation_stop_at` or user stop. Model/browser latency changes throughput;
   do not promise a fixed number of units per hour.

For You is validation, not the primary training surface. Use one continuous
native feed; no reload/reset/goto-home between sampled items. Prefer the visible
native next/down control. If it fails, mark only the validation lane
`partial|unavailable` and continue healthy search training. Do not add random
delays, cursor jitter, or fake human behavior.

## Mutation lanes

Keep Like, Favorite, Repost, proactive comment, comment Like, Not interested,
follow, reply, generic Share, publishing, and profile changes separate. Each
authorized lane must pass its own one-action persistence gate in the current
account/runtime.

- Favorite: selected immediately, stable near +3 seconds and +10 seconds, then
  reload/reopen and account-level evidence when available.
- Repost: only TikTok's explicit `Repost`/`Undo repost`; opening Share is
  read-only navigation and generic Share/copy/send are never substitutes.
- Proactive comment: submit once, never exceed 30 words, and require post-reload
  visibility. Never duplicate an uncertain send.
- Like: disabled by default because it is an independent capability lane.

A lane failure suspends only that lane. An uncertain mutation freezes only that
exact target/action and is never retried; search/view and independent safe lanes
continue.

## Chrome and recovery

- Use only the user's existing Chrome profile and TikTok login. Never enter,
  store, or bypass credentials.
- Every executor creates and owns a dedicated tab. Never reuse a tab ID from a
  prompt, prior turn, memory, or another task.
- The launcher and executor do not list, search, read, inspect, interrupt,
  message, unarchive, revive, archive, replace, or coordinate with another TikTok task.
  Another task using Chrome, TikTok, or the same account is not a blocker.
- Classify stale binding/browser disconnect, DNS/network `ERR_*`, proxy/TLS,
  HTTP status, `ERR_BLOCKED_BY_CLIENT`, and blank/render faults separately.
- In the same logged-in Chrome: record code+URL, bounded retry, create/rebind a
  fresh owned tab if needed, probe TikTok home and a neutral HTTPS site, then
  re-confirm account and target before continuing.
- Describe only a `可能原因` from the exact code and probes. Never clear cookies,
  switch browser, change proxy/TLS, or retry an uncertain mutation.

Ordinary technical, candidate, route, evidence, and single-lane failures are
local outcomes. Auto-recover, rotate, checkpoint, or wait for the next self
Heartbeat without asking the user. Ask directly in the executor only when the
user must fix a current persistent login/account mismatch, CAPTCHA/challenge,
explicit account lock/ban, credential requirement, or unavailable sole allowed
Chrome control.

## Self-owned Heartbeat

After assignment acceptance, the executor creates exactly one repeat-on
`executor_heartbeat` targeted to its own exact task ID, with finite
`operation_stop_at`/`UNTIL`. It immediately reads back and verifies automation
ID, `targetThreadId`, repeat state, next local/UTC run, and cutoff.

The Heartbeat is a continuation/recovery carrier, not a quota or a reason to
pause healthy work. If the executor is already running, a wake does no
overlapping work. If idle/yielded before cutoff, it resumes from the last valid
checkpoint. Ordinary failure never deletes the Heartbeat. For a misbound or
misconfigured timer, create and verify the correct replacement, switch the
stored binding, then retire the old timer. Retire only after user stop, deadline,
objective completion, or terminal release.

No launcher/coordinator/supervisor Heartbeat exists. The executor alone creates,
views, updates, replaces, and retires its own automation. Every valid wake and
normal progress report uses exactly three lines:

```text
本轮完成：<one sentence>
下次心跳：<verified local date, time, and timezone, or why none exists>
下轮计划：<one bounded purpose>
```

## Evidence and completion

Append and validate one JSONL record after every consumed search-origin post,
each five-card assessment, mutation attempt, and For You checkpoint. Store raw
evidence and resume cursor in the executor's ledger; never in the Heartbeat
prompt.

At deadline, explicit stop, or objective completion: stop new external work,
resolve no uncertain mutation by repetition, release only owned tabs, reconcile
the final ledger, retire the exact self Heartbeat, and report in the executor
task. The launcher remains idle and is not contacted.

Use Chinese for user reports while preserving exact URLs, handles, hashtags,
error codes, and UI labels.
