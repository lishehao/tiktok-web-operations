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
`$thread-supervisor`: one reusable stateless launcher and one newly created,
independent execution task per operating instruction.

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

### TikTok 启动台 → TikTok 分发台 (`TIKTOK_LAUNCHER`)

Its first available presentation action is renaming the current task
`TikTok 启动台`. That title is temporary and covers only install/upgrade,
validation, read-only Chrome/TikTok preflight, and a user repair that prevents
health proof. Immediately after every required preflight passes, rename the same
exact task `TikTok 分发台`, attempt to pin that exact task, and verify
`pinned=true` when readback exists. Rename/pin failure is presentation
degradation and never blocks dispatch.

The pinned distributor has one objective: resolve the initial mission using
explicit values plus safe defaults, complete the profile gate only when needed,
fresh-create exactly one unpinned `TikTok 执行台`, send one canonical assignment,
verify acceptance, release its disposable tab, then become idle.

The launcher never becomes `TikTok 主控台`, never creates or owns a Heartbeat,
never supervises the execution task, never receives callbacks, and never acts as
a later risk or decision surface. A rename-tool failure is
`DEGRADED_RENAME_UNAVAILABLE`; it does not block setup.

Idle is reusable, not retired. Whenever the user later sends another new
operating instruction in this same `TikTok 分发台`, run a quick current health
check, resolve only that instruction, generate a new `run_id`, fresh-create one
new executor only after its profile proposal is confirmed, send the one-way
assignment, and return to idle. Keep no watchlist
or cross-run result state and never aggregate previous executor output.

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
recovery, user reports, and at most one pending self-targeted one-shot wake. Future user
changes and hard-blocker repair happen directly in this task.

The executor never calls back the launcher, never reads or supervises other
TikTok tasks, never claims another task's tab, never creates descendants, and
never treats another Chrome/TikTok owner as a blocker. Independent runs use
independent task IDs, ledgers, run/round-unique wake IDs, and Chrome tabs.

Read `references/role-and-stage-contract.md` and
`references/operating-model.md` before creating an execution task or Heartbeat.

## Entrypoints

| User request | Behavior |
|-|-|
| Installer/setup prompt | Rename to `TikTok 启动台`, automatically install/upgrade, validate, and run preflight; on health rename the same task `TikTok 分发台` and pin it. |
| Clear mission with a healthy installation | Rename/pin as distributor first. Treat a sufficiently explicit start instruction as canonical profile confirmation and fresh-create/assign without another question. Never reuse an operating task. |
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

Every later fresh dispatch through the reusable launcher repeats this profile
lock for that new run. Stateless launchers never inherit a prior profile; the
user must restate it or confirm the newly displayed proposal.

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
- a normal 35-view round may contain multiple search units and never returns to
  the launcher between units or rounds.

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
6. At the end of every completed 25–45-view operating round, persist a durable
   checkpoint and set `cooldown_until` 10–20 minutes ahead. Use 15 minutes by
   default, 10 for read-only/low-yield work, and 20 for mutation- or
   recovery-heavy work. This is workload pacing, never randomized stealth.
   During cooldown perform no TikTok navigation, viewing, or mutation. Before
   yielding, create and read back exactly one self-target, single-occurrence
   Heartbeat with ID `tiktok-wake-<run_id>-round-<round_seq>`. Verify exact ID,
   target task, run ID, round sequence, one-shot state, next local/UTC wake, and
   mission cutoff. Resume only from that wake; record it consumed, delete or
   retire the expired timer if it remains visible, clear the binding, and begin
   the next round.
7. Adjust search clusters from rolling evidence and repeat until
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
local outcomes. Auto-recover, rotate, or checkpoint without asking the user. If
a later retry requires yielding, create one run/sequence-unique self-target
single-occurrence recovery wake and validate it before yield. Ask directly in the executor only when the
user must fix a current persistent login/account mismatch, CAPTCHA/challenge,
explicit account lock/ban, credential requirement, or unavailable sole allowed
Chrome control.

## Self-owned one-shot wake

Do not create a timer at assignment acceptance. The first round starts
immediately. At each completed round checkpoint, if `cooldown_until` is before
`operation_stop_at`, create exactly one heartbeat-kind automation with one
occurrence (`COUNT=1` or the tool's equivalent), targeted to this exact executor.
Use a unique ID and display name containing full `run_id` plus `round_seq`; never
use a global ID such as `executor-heartbeat`.

Read back and verify automation ID, `targetThreadId`, run ID, round sequence,
single-occurrence state, next local/UTC run, and cutoff before yielding. A
misbound or uncertain timer is not continuation proof: delete it when identity
is certain, create no duplicate in the same checkpoint, and report the
continuation failure in this executor task.

On wake, require exact task/run/round/timer binding and a still-open mission.
Record `ONE_SHOT_WAKE_CONSUMED`; if the expired automation remains visible,
delete/retire it; clear `pending_wake_id`; then resume. A duplicate/late wake or
an already-running executor performs no TikTok work. Never callback the
distributor and never ask it to schedule a timer.

For a recoverable fault that truly requires a later retry, use the same pattern
with ID `tiktok-recovery-<run_id>-<recovery_seq>` and one occurrence. Never keep
a standing repeat-on Heartbeat. At most one pending self-owned wake exists per
executor. At user stop, deadline, completion, or terminal release, delete only
the executor's exact pending wake if one exists.

No launcher/coordinator/supervisor timer exists. The executor alone creates,
views, consumes, and retires its own one-shot automation. Every valid wake and
normal progress report uses exactly three lines:

```text
本轮完成：<one sentence>
下次心跳：<verified local date, time, and timezone, or why none exists>
下轮计划：<one bounded purpose>
```

## Evidence and completion

Append and validate one JSONL record after every consumed search-origin post,
each five-card assessment, mutation attempt, For You checkpoint, one-shot create
readback, and wake consumption. Store raw evidence and resume cursor in the
executor's ledger; never in the wake prompt.

At deadline, explicit stop, or objective completion: stop new external work,
resolve no uncertain mutation by repetition, release only owned tabs, reconcile
the final ledger, delete the exact pending one-shot wake if present, and report in the executor
task. The launcher remains idle and is not contacted.

Use Chinese for user reports while preserving exact URLs, handles, hashtags,
error codes, and UI labels.
