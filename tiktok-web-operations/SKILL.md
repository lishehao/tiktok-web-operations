---
name: tiktok-web-operations
description: >-
  Run authorized TikTok web operations through the user's logged-in Chrome
  session. Covers one-time setup, persistent search-led recommendation
  calibration, Favorites, TikTok Reposts, short comments, publishing,
  analytics, recovery, and a coordinator-to-executor callback topology.
---

# TikTok Web Operations

Operate TikTok from the user's existing logged-in Chrome with durable evidence.
For persistent operation use the `coordinator_worker` topology from
`$thread-supervisor`: the setup task becomes one pinned `TikTok 主控台`; one
fresh `TikTok 执行台` performs bounded Chrome rounds and callbacks the main task.

## Operating objectives

Cultivation missions optimize two observable proxies:

1. `profile_alignment`: qualified search-origin viewing and held-out For You
   samples increasingly match the chosen audience/persona.
2. `account_strength_proxy`: contextual Like, Favorite, TikTok Repost, and
   proactive-comment attempts demonstrate active community participation.

These are operating proxies, not proof of TikTok's private ranking weights or a
promise of reach. For `运营`, `培养`, `养号`, `增长`, or `增加权重`, default post
Like, Favorite, Repost, and proactive comment to four independent
`best_effort_attempt` lanes with `parallel_engagement=true`. Browse-only requests stay
read-only. Zero outward actions is valid only when no qualified candidate
exists, a lane is unavailable, or the action would be repetitive or unsafe;
record the exact reason.

## Roles

### TikTok 启动台 → TikTok 主控台 (`TIKTOK_COORDINATOR`)

Its first available presentation action is renaming the current task
`TikTok 启动台`. That title is temporary and covers only install/upgrade,
validation, read-only Chrome/TikTok preflight, and a user repair that prevents
health proof. Immediately after every required preflight passes, rename the same
exact task `TikTok 主控台`, attempt to pin that exact task, and verify
`pinned=true` when readback exists. Rename/pin failure is presentation
degradation and never blocks dispatch.

The pinned main task has one objective: own the confirmed profile, mission,
strategy, executor registry, callback acceptance, inter-round cooldown,
scheduler Heartbeat, user reports, and finalization. It never operates TikTok or
owns a Chrome operating tab.

After profile confirmation, fresh-create exactly one unpinned `TikTok 执行台`,
record its exact returned ID, prove a callback handshake, create/read-back one
coordinator-targeted callback-first phase timer under the user's direct mission
authorization, then dispatch bounded rounds. A rename/pin failure is
`DEGRADED_RENAME_UNAVAILABLE|PIN_UNAVAILABLE`; it does not block setup.

Every new mission generates a new `run_id` and calls `create_thread` once. The
main task accepts only that call's exact new executor ID. It never selects,
unarchives, revives, or reuses a historical same-title executor. During the
mission it may read/message only the registered executor for assignment,
callback, dispatch, stop, and release. If fresh creation fails or is uncertain,
report `FRESH_TASK_CREATION_FAILED|UNKNOWN`; never fall back to an old task.
Never fallback to a historical owner by title, archive state, or readable summary.

### TikTok 执行台 (`TIKTOK_EXECUTOR`)

It has one objective: execute exactly one bounded round assignment at a time.
It owns its dedicated Chrome tab, raw evidence ledger, within-round recovery,
candidate decisions, and authorized TikTok actions. At checkpoint, hard repair,
or terminal release it sends one structured callback to the exact main task and
becomes idle. It never creates, updates, views, or deletes a Heartbeat.

The executor never chooses the next round, cooldown, or mission direction;
never reads or supervises unrelated TikTok tasks; never claims another task's
tab; never creates descendants; and never treats another Chrome/TikTok owner as
a blocker. It accepts work only from its registered main task and exact run ID.

Read `references/role-and-stage-contract.md` and
`references/operating-model.md` before creating an execution task or Heartbeat.

## Entrypoints

| User request | Behavior |
|-|-|
| Installer/setup prompt | Rename to `TikTok 启动台`, automatically install/upgrade, validate, and run preflight; on health rename the same task `TikTok 主控台` and pin it. |
| Clear mission with a healthy installation | Rename/pin as main task first. Treat a sufficiently explicit start instruction as canonical profile confirmation and fresh-create one executor without another question. |
| `继续` or `开始` after a visible profile proposal | Treat as confirmation of that exact proposal and proceed. |
| `继续` or `开始` without a visible profile proposal | Produce the packaged default proposal; do not start until the user confirms it. |
| `用默认设置开始` | Confirm the packaged default profile and dispatch directly without another question. |
| Direction/duration reply to the setup handoff | Treat it as an operating instruction, fill reversible omissions from defaults, and dispatch without another confirmation round. |
| Direction only | Complete a structured proposal from that direction and ask for one confirmation. |
| Duration only | Produce the packaged default direction proposal with that duration and ask for one confirmation. |
| Browse-only wording | Search/view only; do not infer mutation authority. |
| Cultivation/growth wording | Enable post Like, Favorite, Repost, and Comment as four independent `best_effort_attempt` lanes with parallel engagement during viewing. |
| `自动发短评论` | Within the accepted audience/language/voice envelope, comments are contextual, preferably 2–12 words, and never over 30 words. |

Do not pause merely to announce an available upgrade or ask again for a value
the user already supplied. Region/language is normally inferred. For universal
lifestyle topics such as pets, food, travel, or humor, default to `global
English with North American bias` unless the user specifies otherwise.

## Mission contract

### Bootstrap account-image lock

Preflight may complete before direction is known, but no executor creation,
TikTok search, video viewing, or interaction is allowed until
`profile_status=confirmed`.

Use at most two user-facing rounds:

1. ask one open question: what identity should this account represent, for whom,
   and what should it eventually publish? If the initial user message already
   answers this, skip the question;
2. present one inferred structured proposal and ask the user to confirm or name
   final replacement values. A correction message that supplies those values
   confirms the revised profile unless it explicitly asks to review another
   draft. Do not interrogate every field separately.

The proposal contains `persona_name`, `target_audience`, `region_language`,
3–5 `content_pillars`, `excluded_topics`, `voice_and_comment_style`,
`future_post_alignment`, duration/intensity, and interaction policy. Store
`profile_status=draft|proposed|confirmed` plus
`direction_profile_version`. Only the exact proposal the user confirmed becomes
`direction_ref` and may enter `executor_assignment/v1`.

A detailed initial instruction that supplies a usable direction and explicitly
asks to start/operate is canonical confirmation; compile missing reversible
fields from shown safe defaults and do not add a confirmation round. A detailed
description that asks for advice/review but not operation remains input only. A bare
`继续` confirms only a proposal already shown. If no proposal has been shown,
present the default proposal and wait once.

The setup handoff itself establishes operating context. A reply that supplies a
direction and optional duration is therefore an explicit operating instruction,
even if it omits the word “start”; compile the confirmed profile and dispatch.
The exact reply `用默认设置开始` confirms the packaged defaults and also
dispatches directly.

Every new mission in the pinned main task repeats this profile lock. A completed
historical mission is evidence only; it never silently becomes the new profile.

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

One executor operating round targets 35 qualified watched videos with an allowed
range of 25–45. This is a work-size boundary, not an exact quota:

- normally 25–35 strong-core search-origin views plus 5–10 sequential For You
  validation views;
- if For You is unavailable, search-origin views may fill the whole round;
- thumbnails, duplicates, clear drift, and failed loads do not count;
- after 25 qualified views, finish at the next natural boundary when quality or
  runtime conditions justify it; never exceed 45 before a durable checkpoint;
- a normal 35-view round may contain multiple search units and makes exactly one
  callback to the main task at its checkpoint.

1. Search three distinct approved clusters.
2. Assess the first five results per cluster and open every suitable strong-core
   result. A normal unit contains 9–15 qualified search-origin views; fewer is an
   honest no-action unit, not a blocker.
3. Watch enough to understand premise/payoff and record actual progression when
   available. Search cards and direct-known URLs do not count as qualified
   training views.
4. Immediately after each qualified view is understood and before navigating
   away, evaluate all four eligible Like/Favorite/Repost/Comment lanes. Execute
   justified native actions once in that same browsing flow; do not defer
   engagement to a separate post-view phase.
5. After two units or roughly 20–30 new qualified views, sample 5–10 sequential
   For You items as held-out validation.
6. At the end of every completed 25–45-view round, persist a durable checkpoint
   and callback `ROUND_COMPLETED/v1` with counts, cluster evidence, For You mix,
   lane attempts, resume cursor, blockers, and executor state `IDLE`.
7. The main task chooses 10–20 minutes of cooldown from that evidence, stores an
   exact machine-clock `next_dispatch_at`, adjusts the next three search
   clusters and action emphasis, and updates its stable phase timer to dispatch
   the next bounded round once when due. Use 15 minutes by default, 10 for
   read-only/low-yield work, and 20 for mutation- or recovery-heavy work. During
   cooldown the executor performs no TikTok work. Repeat until
   `operation_stop_at` or user stop; do not promise fixed hourly throughput.

For You is validation, not the primary training surface. Use one continuous
native feed; no reload/reset/goto-home between sampled items. Prefer the visible
native next/down control. If it fails, mark only the validation lane
`partial|unavailable` and continue healthy search training. Do not add random
delays, cursor jitter, or fake human behavior.

## Mutation lanes

Keep Like, Favorite, Repost, proactive comment, comment Like, Not interested,
follow, reply, generic Share, publishing, and profile changes separate. Each
authorized lane uses attempt evidence rather than a persistence gate.

- Favorite: click the visible native Favorite control once. Do not wait +3/+10
  seconds, reload/reopen, or seek account-level proof.
- Repost: only TikTok's explicit `Repost`/`Undo repost`; opening Share is
  read-only navigation and generic Share/copy/send are never substitutes.
- Proactive comment: submit once and never exceed 30 words. Do not reload/reopen
  to verify it. Never duplicate an uncertain send.
- Like: click the visible native Like control once on a fitting post. Do not
  reload/reopen or seek account-level proof.

`parallel_engagement=true` means all four lanes stay concurrently eligible
throughout the viewing round. It does not mean mechanically applying all four to
every video. Normally Like may accompany at most one higher-intent action on a
strong candidate, while Favorite, Repost, and Comment are distributed across
the most fitting posts. Every round evaluates every qualified video for all
lanes and attempts each lane at least once when its native control is available
on a genuine, non-repetitive candidate; otherwise log unavailable/hard-blocked.

Use distinct strong-core posts for the four first attempts as those posts are
encountered in the normal viewing flow. Do not stop browsing to create a separate
interaction block, and do not finish all viewing before beginning interaction.

A non-persistent or unverified result does not suspend a lane or prevent future
attempts on new posts. An uncertain mutation freezes only that exact
target/action and is never retried; search/view and independent lanes continue.

Record interaction results only as `attempted | unavailable | hard_blocked`.
`attempted` means the visible native click/send was issued once; it is not a
claim of server persistence or success. Do not perform post-action waiting,
reload/reopen, profile-tab checks, or account-level verification for these four
operating lanes.

### Comment-priority policy

Give proactive Comment the highest candidate-selection weight because it can
produce visible community feedback such as organic likes and replies. Treat that
feedback as evidence of comment resonance, not proof of TikTok account weight or
distribution causality.

For a normal 35-target / 25–45-view round, use
`comment_attempt_target=6`, `comment_attempt_min=4`,
`comment_attempt_max=8`, with an absolute safety ceiling of 10. This is a quality
range: if fewer than four genuinely strong candidates exist, record the
shortfall and do not publish generic filler.

Generate comments in this order:

1. understand the video's exact setup/payoff;
2. inspect visible live comment culture;
3. draft an original post-specific joke;
4. only when the joke is weak, slang is unclear, or the reference is
   time-sensitive, use Web Search for current meme/slang context;
5. transform research into a new line—never copy a TikTok comment, search
   snippet, meme caption, creator wording, or another one-liner.

Limit meme research to at most two focused Web searches per operating round so
research does not consume the browsing budget. Search is supporting context,
not a substitute for watching the video. Score drafts for specificity, context
fit, meme resonance, brevity, and safety. Prefer 2–12 words; 30 words remains the
hard ceiling. Reject generic praise, engagement bait, repeated templates,
targeted harassment, protected-trait attacks, and sexualization of minors.

## Chrome and recovery

- Use only the user's existing Chrome profile and TikTok login. Never enter,
  store, or bypass credentials.
- Every executor creates and owns a dedicated tab. Never reuse a tab ID from a
  prompt, prior turn, memory, or another task.
- The main task reads/messages only its exact registered executor. The executor
  reads/messages only its exact registered main task. Neither inspects unrelated
  TikTok tasks. Another task using Chrome, TikTok, or the same account is not a blocker.
- Classify stale binding/browser disconnect, DNS/network `ERR_*`, proxy/TLS,
  HTTP status, `ERR_BLOCKED_BY_CLIENT`, and blank/render faults separately.
- In the same logged-in Chrome: record code+URL, bounded retry, create/rebind a
  fresh owned tab if needed, probe TikTok home and a neutral HTTPS site, then
  re-confirm account and target before continuing.
- Describe only a `可能原因` from the exact code and probes. Never clear cookies,
  switch browser, change proxy/TLS, or retry an uncertain mutation.

Ordinary technical, candidate, route, evidence, and single-lane failures are
local outcomes. Auto-recover, rotate, or checkpoint without asking the user. A
failure that ends the bounded round callbacks the exact main task with its
smallest scope. Only the main task asks the user to fix a persistent login/account
mismatch, CAPTCHA/challenge, explicit account lock/ban, credential requirement,
or unavailable sole allowed Chrome control.

## Coordinator callback and phase timer

Before external work, perform one bounded callback handshake:
`CALLBACK_PING/v1` from main to executor and `CALLBACK_ACK/v1` back to the exact
main task. No acceptance means no unattended mission claim.

The main task creates and owns one stable, self-targeted phase-timer automation
for the mission. Create it once from the user's direct mission authorization;
require exact automation ID, main-task target, current phase, one-occurrence
state, next local/UTC run, and mission cutoff readback. Update that same exact
automation in place; never create/delete a timer per round. The executor never
touches it.

Do not depend on a persisted `PAUSED` label: this runtime may normalize creates
to `ACTIVE`. Stop polling by encoding exactly one future occurrence and reading
it back. Use the tool's supported one-occurrence form; when immediate create
rejects `DTSTART` or bare `COUNT=1` has no future run, use a finite
`INTERVAL=<minutes>;UNTIL=<just after one interval>` equivalent. Never claim a
single wake merely from the request bytes. Leave at least 60 seconds between the
intended occurrence and `UNTIL` so update latency cannot erase the only run.

Use callback-first phase scheduling:

1. After sending a round, stop normal scheduler polling. Arm only one
   `ACTIVE_WATCHDOG` wake for 60 minutes after dispatch (bounded by
   `operation_stop_at`). There is no five-minute executor-active NOOP loop.
2. When the exact executor callback arrives before the watchdog, accept it,
   compute `next_dispatch_at`, and update the same automation in place to one
   `COOLDOWN_WAKE` at that exact time.
3. A valid due cooldown wake verifies executor `IDLE`, sends exactly one
   `round_assignment/v1`, marks it dispatched, and rearms the same automation as
   the next single 60-minute `ACTIVE_WATCHDOG`.
4. A watchdog wake never dispatches while the executor is active. Read only the
   exact executor's recent status: rearm once for 60 minutes when progress is
   recent; request one status/callback when idle without callback; surface a
   genuine orchestration blocker only when the registered executor is stale or
   unreachable.
5. At/after `operation_stop_at` or user stop, delete the exact timer.

The main task computes all wake times from a fresh machine clock, never from
model-estimated timestamps. A late cooldown wake dispatches once when still
before the mission cutoff; it never sends catch-up bursts. A misbound,
unreadable, or non-updatable phase timer is `SCHEDULER_CONTINUATION_FAILURE` and
cannot be claimed as unattended continuation. Timer failure never authorizes
the executor to create a substitute or fall back to five-minute polling.

Every accepted callback and coordinator progress report uses exactly three lines:

```text
本轮完成：<one sentence>
下次心跳：<verified local date, time, and timezone, or why none exists>
下轮计划：<one bounded purpose>
```

## Evidence and completion

Append and validate one JSONL record after every consumed search-origin post,
each five-card assessment, mutation attempt, For You checkpoint, round callback,
scheduler wake decision, and next-round dispatch. Store raw browsing evidence in
the executor ledger and coordinator state/cooldown decisions in the main ledger;
never put mutable evidence in the Heartbeat prompt.

At deadline, explicit stop, or objective completion: the main task stops new
dispatch, sends a stop instruction if the executor is active, deletes its exact
scheduler Heartbeat, requires executor tab-release/final-ledger callback, and
reports the final result. Never repeat an uncertain mutation.

Use Chinese for user reports while preserving exact URLs, handles, hashtags,
error codes, and UI labels.
