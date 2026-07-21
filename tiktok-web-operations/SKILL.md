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

The pinned main task has one objective: decide **what the next bounded round is,
when it starts, or whether the mission ends**. Its inputs are the latest user
instruction, canonical mission/authority, one accepted executor callback, and a
fresh machine clock. Its outputs are exactly one next-round assignment, one
timer update, one hard-repair request, or terminal finalization. It owns profile
and mission versions, strategy, executor registry, callback acceptance,
inter-round cooldown, scheduler Heartbeat, user reports, and finalization.

It never operates TikTok, owns a Chrome operating tab, selects an exact video,
writes a comment, decides whether a specific post deserves an action, or edits
the executor's raw evidence. It may change clusters and emphasis, but not
silently narrow user authority.

Treat an accepted exact `round_callback/v1` with `executor_state=IDLE` as the
canonical idle proof until the main task sends the next round. A later
`read_thread` is diagnostic only: its temporary failure, empty result, or
`notLoaded` presentation state cannot invalidate the accepted callback or block
a due dispatch. Only explicit newer contradictory evidence requires
reconciliation.

After profile confirmation for a new mission, fresh-create exactly one unpinned `TikTok 执行台`,
record its exact returned ID, immediately set that exact task title to
`TikTok 执行台`, and verify same-ID title readback when supported. Do not select
or repair an executor by title. If title mutation is unavailable, record
`DEGRADED_EXECUTOR_TITLE_UNAVAILABLE`, continue, and make at most one exact-ID
repair attempt at the first safe executor-IDLE boundary. Prove a callback
handshake, create/read-back one
coordinator-targeted mission recurring Heartbeat under the user's direct mission
authorization, then dispatch bounded rounds. A rename/pin failure is
`DEGRADED_RENAME_UNAVAILABLE|PIN_UNAVAILABLE`; it does not block setup.

Every new mission generates a new `run_id` and calls `create_thread` once. The
main task accepts only that call's exact new executor ID. It never selects,
unarchives, revives, or reuses a historical same-title executor. During the
mission it may read/message only the registered executor for assignment,
callback, dispatch, stop, and release. If fresh creation fails or is uncertain,
report `FRESH_TASK_CREATION_FAILED|UNKNOWN`; never fall back to an old task.
Never fallback to a historical owner by title, archive state, or readable summary.

Within that active mission, every later round and every user continuation or
direction adjustment in `TikTok 主控台` reuses the same exact registered
executor. Update versioned direction/authority/mission refs for the next bounded
assignment; do not create a task merely because a round ended, the executor is
IDLE, or the user said `继续`.

Create at most one same-run replacement only when the registry has no exact
executor ID or that exact registered task is proven `STALE_OWNER_TOMBSTONE`,
retired, archived, or released before the active mission ends. Temporary
`notLoaded`, empty/unavailable `read_thread`, host/network unavailability, or a
transient tool error is not absence and never triggers replacement. A valid
replacement keeps `run_id`, increments `executor_generation`, records old/new
IDs, reason, and timestamp, sends a new canonical `executor_assignment/v2` with
the last accepted resume cursor, repeats `CALLBACK_PING/ACK`, and atomically
updates the registry before dispatch. If replacement creation or assignment is
failed/uncertain, do not try again; report one orchestration blocker. After a
terminal release/cutoff, a later instruction is a new mission with a new run.

At stop, cutoff, or completion, stop new dispatch, obtain exact executor
`RUN_RELEASED` plus owned-tab release proof, delete/read back the exact mission
Heartbeat, and reconcile both ledgers. Only then archive the exact registered
executor task and verify same-ID archive readback when supported. Never archive
an ACTIVE, IDLE-but-live, STOP_REQUESTED, unreleased, or newly bound replacement
executor. Archive unavailability is
`DEGRADED_EXECUTOR_ARCHIVE_UNAVAILABLE`: report it without blocking terminal
mission truth or pretending the task was archived.

### TikTok 执行台 (`TIKTOK_EXECUTOR`)

It has one objective: complete **the currently assigned bounded Chrome round and
return observed facts**. Its inputs are one exact accepted assignment, its own
ledger/resume cursor, and live Chrome/TikTok state. It chooses exact queries
within assigned clusters, exact videos, watch progression, candidate fit,
comment wording, and justified authorized actions. Its only boundary output is
one structured callback with evidence, counts, blockers, and optional
non-binding next-round suggestions; then it becomes idle.

It owns its dedicated Chrome tab, raw evidence ledger, within-round recovery,
candidate decisions, and authorized TikTok actions. It never creates, updates,
views, or deletes a Heartbeat.

The executor never chooses or dispatches the next round, cooldown, scheduler,
mission direction, authority, or user-facing resolution; never reads or
supervises unrelated TikTok tasks; never claims another task's tab; never
creates descendants; and never treats another Chrome/TikTok owner as a blocker.
It accepts work only from its registered main task and exact run ID.

Read `references/role-and-stage-contract.md` and
`references/operating-model.md` before creating an execution task or Heartbeat.
Every executor must also read `references/qualified-view-contract.md` before its
first browsing round and apply that contract to every opened video. Read
`references/runtime-and-recovery.md` before Chrome setup and after any browser,
tab, navigation, render, playback, or tool timeout.

## Entrypoints

| User request | Behavior |
|-|-|
| Installer/setup prompt | Rename to `TikTok 启动台`, automatically install/upgrade, validate, and run preflight; on health rename the same task `TikTok 主控台` and pin it. |
| Clear mission with a healthy installation | Rename/pin as main task first. Treat a sufficiently explicit start instruction as canonical profile confirmation and fresh-create one executor without another question. |
| Continuation or adjustment while the current mission is active | Keep the current `run_id`; reuse the exact registered executor, version changed refs, and apply them to the next non-overlapping bounded assignment. |
| New instruction after terminal release/cutoff | Start a new profile/mission boundary with a new `run_id` and fresh executor. |
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
`direction_ref` and may enter `executor_assignment/v2`.

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
- if For You is unavailable or sampled items fail the qualified-view gate,
  search-origin views may fill the whole round;
- thumbnails, duplicates, adjacent/drift content, failed loads, and
  `opened_only|classified_sample` records do not count;
- after 25 qualified views, finish at the next natural boundary when quality or
  runtime conditions justify it; never exceed 45 before a durable checkpoint;
- a normal 35-view round may contain multiple search units and makes exactly one
  callback to the main task at its checkpoint.

1. Search three distinct approved clusters.
2. Assess the first five results per cluster and open every suitable strong-core
   result. A normal unit contains 9–15 qualified search-origin views; fewer is an
   honest no-action unit, not a blocker.
3. Apply `STRICT_QUALIFIED_VIEW_V2`: record two or more playback observations,
   continuous watch time after the first observation, duration-based watch
   floor, and concrete premise/payoff evidence. A page-open progress value,
   action click, caption paraphrase, or one-second autoplay does not qualify a
   view. Search cards and direct-known URLs do not count as search-origin proof.
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
   exact machine-clock `next_dispatch_at`, and adjusts the next three search
   clusters and action emphasis. Its stable 15-minute recurring Heartbeat
   dispatches the next bounded round once on the first tick at or after that due
   time. Use 15 minutes by default, 10 for
   read-only/low-yield work, and 20 for mutation- or recovery-heavy work. During
   cooldown the executor performs no TikTok work. Repeat until
   `operation_stop_at` or user stop; do not promise fixed hourly throughput.

For You is validation, not the primary training surface. Use one continuous
native feed; no reload/reset/goto-home between sampled items. Prefer the visible
native next/down control. If it fails, mark only the validation lane
`partial|unavailable` and continue healthy search training. Do not add random
delays, cursor jitter, or fake human behavior.

Feed drift never zeroes Comment. Feed composition may change the next search
clusters or validation frequency, but never narrows mutation authority. A drifted For You checkpoint cannot pause
Comment, set its next-round target/min/max to zero, or remove it from an
authorized cultivation assignment. Evaluate `new cluster match` per opened
search-origin video; it is not a whole-round prerequisite.

## Mutation lanes

Keep Like, Favorite, Repost, proactive comment, cultivation reply, comment Like,
Not interested, follow, generic Share, publishing, and profile changes as
separate capability sub-lanes. A cultivation reply can share the active comment
authorization and round budget while retaining its own candidate and parent-
context checks. Each authorized lane uses attempt evidence rather than a
persistence gate.

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

The main task must copy the current authority into every round assignment. For
an authorized cultivation mission without a current exact-lane hard block,
write all four lanes as `best_effort_attempt` and keep Comment `ACTIVE`; a prior
callback recommendation is strategy advice, not authority. Only a newer user
revocation, browse-only mission, or current explicit Comment hard block may
disable it. Prior-round attempt counts, Feed drift, quality shortfall, or a
request to rotate clusters may never become a round-wide Comment freeze.

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
`comment_attempt_target=10`, `comment_attempt_min=7`,
`comment_attempt_max=12`, with an absolute safety ceiling of 15. Count both
top-level proactive comments and replies in this total. This is a quality range:
if fewer than seven genuinely strong conversational openings exist, record the
shortfall and do not publish generic filler.

Reset this budget at the start of every cultivation round. Include the four
values explicitly in each `round_assignment/v1`; never carry forward
`comment_mode=PAUSED_UNTIL_NEW_CLUSTER_MATCH` or zero values merely because the
previous round reached target or its For You sample drifted. A round can finish
with zero actual comment attempts only as a reported current-round quality,
availability, safety, or hard-block shortfall—not because the assignment erased
the authorized lane in advance.

Most qualifying videos receive zero or one top-level comment. On an exceptional
strong-core video, inspect the live discussion more deeply and allow up to three
total comment mutations: at most one proactive top-level comment plus at most
two replies to distinct existing comments. Each reply must add a different,
post-specific joke or observation. Never post multiple top-level comments,
self-reply, repeat a template, or use replies merely to reach the round target.

Generate comments in this order:

1. understand the video's exact setup/payoff;
2. inspect visible live comment culture; on a deep candidate, read roughly
   8–20 relevant visible comments when readily available;
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
  store, or bypass credentials, switch browsers, clear cookies, or change
  proxy/TLS.
- Every executor creates and owns a dedicated tab. Never reuse a tab ID from a
  prompt, prior turn, memory, or another task.
- The main task reads/messages only its exact registered executor. The executor
  reads/messages only its exact registered main task. Neither inspects unrelated
  TikTok tasks. Another task using Chrome, TikTok, or the same account is not a blocker.
- `references/runtime-and-recovery.md` is the only detailed Chrome/runtime
  authority. Load it before Chrome setup and after any browser, tab, navigation,
  content, React-control, playback, or tool timeout.
- Metadata health is not content health. If `openTabs`/`list`, `claimTab`, URL,
  and title work but `goto`, DOM, screenshot, locator, or evaluate time out,
  classify `CHROME_CONTENT_CHANNEL_TIMEOUT`, not Chrome disconnect, target-tab
  loss, TikTok account risk, or route failure without stronger probe evidence.
- Browser actions are atomic: one boundary call performs only one potentially
  blocking browser action, and navigation timeouts require URL/title/page-state
  readback before any repeat navigation.
- Write pre-action `MUTATION_INTENT`/`action_key`; a mutation-call timeout becomes
  `SUBMISSION_UNCERTAIN`/`MUTATION_UNKNOWN`, freezing that exact key without
  repeat or verification while independent posts and lanes may continue.

Ordinary technical, candidate, route, evidence, and single-lane failures are
local outcomes. Auto-recover, rotate, or checkpoint without asking the user. A
transient failure that exhausts one pass yields `ROUND_YIELDED` with
`RECOVERY_PENDING`, preserves the same round/cursor/counts/budgets, and returns
IDLE. The unchanged main Heartbeat later dispatches one `RECOVERY_FIRST` resume;
retries continue across wakes until health, stop, cutoff, or current human-only
repair. Only the main task asks once for a persistent login/account mismatch,
CAPTCHA/challenge, explicit account lock/ban, credential requirement, or
unavailable sole allowed Chrome control; the Heartbeat remains the quiet recheck
carrier.

## Coordinator callback and mission scheduler

Before external work, perform one bounded callback handshake:
`CALLBACK_PING/v1` from main to executor and `CALLBACK_ACK/v1` back to the exact
main task. No acceptance means no unattended mission claim.

The main task creates and owns one stable, self-targeted mission scheduler
Heartbeat. Create it once from the user's direct mission authorization before
round 1. Configure it as repeat-on every 15 minutes, with a finite `UNTIL` that
extends at least one full interval beyond `operation_stop_at` so one cleanup
wake can finalize after the exact no-new-work cutoff. Do not use `COUNT=1`, a
one-occurrence schedule, a self-rearmed watchdog, or a per-round timer.
Prefer the tool-supported encoding
`RRULE:FREQ=MINUTELY;INTERVAL=15;UNTIL=<operation_stop_at plus 15 minutes in UTC>`
and omit `COUNT` entirely; if the tool requires an equivalent finite repeat-on
form, preserve the same cadence and cleanup guarantee.

Require readback of the exact automation ID, main-task target, `ACTIVE` status,
15-minute interval, repeat-on schedule, next local/UTC run, mission cutoff, and
cleanup `UNTIL`. A rendered suggestion or request bytes are not proof. The
executor never creates, views, updates, or deletes this Heartbeat.

For each wake, compare fresh actual machine time with the scheduled occurrence.
If `abs(actual_wake - scheduled_wake) <= 5 minutes`, record
`ON_TIME_WITH_TOLERANCE` and continue the normal gate without scheduler repair,
missed-slot handling, catch-up, or user notification. Larger absolute drift is
`WAKE_TIME_DRIFT`: diagnose the scheduler/host once while preserving the same
recurrence, pending work, and dedup state. Wake tolerance is not deadline
tolerance; evaluate actual time against `operation_stop_at` first and never
dispatch new TikTok work at/after cutoff.

The recurring schedule is a liveness carrier, not a dispatch instruction. On
every wake the main task reads a fresh machine clock and applies this gate:

1. At/after `operation_stop_at`, send no new TikTok work and request executor
   release. Keep the preconfigured cleanup wake until `RUN_RELEASED` or finite
   cleanup `UNTIL`; only then delete/read back the exact Heartbeat. Never archive
   when release or tab proof is uncertain.
2. If an accepted exact callback provides unconsumed `executor_state=IDLE`, a
   pending round exists, and `now >= next_dispatch_at`, dispatch exactly one
   round and consume that idle proof.
3. If the cooldown is not yet due, keep the pending round and recurrence. The
   first tick at or after `next_dispatch_at` may add less than one 15-minute
   interval to the chosen cooldown.
4. If the executor is active, do not dispatch or create another timer. Record a
   quiet scheduler checkpoint, verify the recurrence, and use `DONT_NOTIFY` so
   a no-change tick does not spam the user.
5. If the executor is idle without an accepted callback, request one status or
   callback at most once per expected `boundary_seq`; later ticks keep waiting without
   duplicate messages. Transient unreadable task/tool/network state keeps the
   registered owner and the recurring Heartbeat.
6. Strict stale/missing-owner proof may enter the one-attempt same-run owner
   replacement path. Ordinary callback, Chrome, route, candidate, or mutation
   failure never deletes or pauses the Heartbeat.
7. An accepted `ROUND_YIELDED` callback preserves the same round, cursor,
   counters, remaining budgets, and frozen action keys. At/after its
   `next_retry_not_before`, dispatch exactly one `RECOVERY_FIRST` resume rather
   than a new round, using the next `boundary_seq`.
Callback arrival may wake the main task early. Accept and persist the callback. For
`ROUND_COMPLETED`, choose clusters/cooldown and advance the logical round;
for `ROUND_YIELDED`, keep the same round and increment only `boundary_seq` for
`RECOVERY_FIRST`. Do not rewrite the recurring schedule. The next periodic tick is the independent recovery path if
callback delivery or an earlier main-task turn does not continue.

Before every nonterminal scheduler turn returns, read back the same exact
repeat-on automation with a future next run and `UNTIL` beyond the mission
cutoff. `ACTIVE` with no future occurrence before cutoff is
`MISSION_SCHEDULER_EXPIRED`; repair that same automation in place to the
mission recurring schedule before dispatching. A misbound, duplicate,
unreadable, or non-updatable scheduler is `SCHEDULER_CONTINUATION_FAILURE` and
cannot be claimed as unattended continuation. Never create a substitute timer
before a corrected replacement is read back, and never send catch-up bursts.
`DONT_NOTIFY` is valid only after this recurring readback and only for a
no-change tick; accepted callbacks, dispatches, hard repair, and finalization use
the user-facing receipt below.

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

Before a round callback, validate that every claimed qualified view has the
required `qualified-view-contract.md` fields and that the unique qualifying
ledger-row count exactly equals `qualified_views.total`. Keep `opened`,
`classified_sample`, For You `sampled`, and `qualified` counts separate. Fail
closed on missing or contradictory watch evidence; do not fill a round by
upgrading partial views.

At deadline, explicit stop, or objective completion: the main task stops new
TikTok dispatch, sends a stop instruction if the executor is active, and uses
the finite cleanup wake to obtain executor tab-release/final-ledger callback.
After `RUN_RELEASED`, delete/read back the exact scheduler, reconcile both
ledgers, and then archive the exact registered executor task. If cleanup `UNTIL`
arrives without release proof, record `RELEASE_UNCERTAIN`, delete/read back the
scheduler, and do not archive or claim tab release. Archive unavailability after
proven release is an explicit presentation degradation, not false success.
Never repeat an uncertain mutation.

Use Chinese for user reports while preserving exact URLs, handles, hashtags,
error codes, and UI labels.
