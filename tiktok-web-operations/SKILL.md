---
name: tiktok-web-operations
description: >-
  Run authorized TikTok web operations through the user's logged-in Chrome
  session, including account audits, TikTok Studio analytics, persistent feed
  calibration, search-first vertical browsing, native feed scrolling,
  search/hashtag seeding, short meme-aware comments with optional standing
  authorization, publishing, comment follow-up, verification, and a
  starter-as-coordinator plus one persistent executor system. Use when the user asks to
  browse or scroll TikTok, train recommendations, search communities or
  keywords, like/favorite/repost/comment, operate, grow, audit, publish,
  schedule, or
  maintain a TikTok account from the web, or package this workflow.
---

# TikTok Web Operations

Use TikTok's web surfaces as an evidence-led operating system. Keep strategy, Chrome execution, publishing, engagement, and analytics separate.

## System Topology

For persistent operation, use exactly two live canonical user-owned Codex Threads. The starter
task remains the coordinator and keeps only one canonical executor at a time. Both operational
roles use `model=gpt-5.6-luna` and `thinking=high`. Use `$thread-supervisor` for
generic registry, callback, heartbeat, and lifecycle mechanics.

| Thread | Owns | Must not do |
|-|-|-|
| Current starter task, final title `TikTok 主控台` | One objective: keep the authorized mission advancing until stop/completion and own every user decision | Navigate or operate TikTok |
| `execution_thread` — final title `TikTok 执行台` | One objective: continuously advance the accepted mission, checkpoint recoverably, and release/callback on yield, blocker, or stop | Broaden scope, infer approval, alter strategy, create other Threads, or contact the Skill-development Thread |

Direction, persona, authorization, capability matrix, risk rules, ledger, and
deadline are role inputs and constraints. They are never additional independent
objectives. Do not load either Thread with product research, Skill maintenance,
or another operating mission during an active run.

On a setup/install request, the starter task's first available presentation
action is renaming itself `TikTok 启动台`. In that bootstrap role it installs the
bundled Skills, runs read-only preflight, probes capabilities/defaults, and never
starts a mission or creates an executor. After healthy preflight and bootstrap-
tab release, the same exact task ID/history is promoted in place and immediately
renamed `TikTok 主控台`; it may then return the direction/duration handoff and
wait. A rename-tool failure is non-blocking presentation degradation and is
repaired later. Never create a second main task, use a subagent, agent tree, or
agent-path callback for this system.

Naming follows `<platform> <responsibility>台`. After exact identity proof, pin
`TikTok 主控台` and explicitly keep `TikTok 执行台` unpinned. Keep the registered
pair unarchived, including while idle. An already archived TikTok executor is
retired and is never automatically unarchived for reuse. Archive only completed temporary probes or
a released, retired executor after removing its heartbeat/tab/mutation ownership.

Use `references/role-and-stage-contract.md` for the authoritative role cards,
decision boundary, stage machine, and phase exit gates. Use
`references/operating-model.md` for creation, registry, callback, scheduler,
finalization, and recovery mechanics.
Before any persistent Thread or heartbeat action, also read
`$thread-supervisor/references/canonical-registry.md` and
`$thread-supervisor/references/identity-and-automation.md`.

## Route The Request

| Request | Read |
|-|-|
| Install from GitHub, run dependency checks, or bootstrap | `references/version-management.md`, `references/startup-health-check.md`, `references/blocker-minimization.md`, `references/stability-and-circuit-breakers.md`, `references/runtime-and-recovery.md`, `references/operating-model.md` |
| Package, publish, upgrade, overwrite, downgrade, or distribute | `references/version-management.md`, `references/distribution-and-upgrades.md` |
| Broad operating request | all relevant references below |
| Research trends or choose content | `references/loci-content-system.md`, `references/platform-boundaries.md` |
| Browse/scroll or leave short comments | `references/feed-browsing-and-comments.md`, `references/engagement-and-analytics.md`, `references/platform-boundaries.md` |
| Persistently calibrate recommendations | `references/role-and-stage-contract.md`, `references/operating-model.md`, `references/blocker-minimization.md`, `references/stability-and-circuit-breakers.md`, `references/persistent-feed-operations.md`, `references/engagement-and-analytics.md`, `references/runtime-and-recovery.md` |
| Upload, publish, or schedule | `references/publishing-and-scheduling.md`, `references/platform-boundaries.md` |
| Review comments or analytics | `references/engagement-and-analytics.md`, `references/loci-content-system.md` |

Before starting, changing, resuming, or recovering any operating mission, read
`references/instruction-precedence.md` and `references/blocker-minimization.md`.

## Entrypoint Contract

| User says | Execute |
|-|-|
| Installer Prompt or first `帮我运营 TikTok` before bootstrap is initialized | Automatically install or upgrade when the incoming bundle is newer, validate the installed bundle, and continue read-only preflight in the same turn. Return the guided direction/duration handoff only after preflight; do not pause merely to announce an available upgrade, create operating Threads, or touch TikTok state yet. |
| Healthy handoff followed by `继续`, `开始`, a direction, duration, intensity, or action list | Resolve the latest explicit fields, keep this task as coordinator, create one persistent executor, obtain first operation proof, and begin without reconfirming supplied values. |
| `找热点`, `做选题`, `研究竞品` | Research only; do not mutate TikTok. |
| `刷视频`, `看看推荐`, `找能评论的视频` | Browse a bounded sample; do not infer permission for likes, favorites, reposts, follows, or comments. |
| `持续刷`, `定向刷`, `垂直刷`, `养推荐流`, `两个 Thread 运营` | Keep this task as coordinator and run one continuous, resumable, deadline-bounded mission in its persistent execution Thread. |
| `刷视频并互动`, `点赞收藏评论`, `收藏并 repost`, `去发几个评论` | Find strong core candidates and use only independently verified like, favorite, repost, or proactive-comment lanes covered by the exact standing envelope. Treat Repost as distinct from generic Share. |
| `评论不用问我`, `自动发短评论` | Activate `autonomous_comment_mode` only for the exact account/audience/voice envelope; enforce the 30-word hard limit and every persistence stop rule. |
| `发视频`, `上传`, `排期` | Validate the exact asset/settings, confirm, execute one item, and verify. |
| `看数据`, `复盘` | Use account/TikTok Studio analytics read-only. |
| `现在状态`, `有什么风险` | Answer from coordinator state, execution callbacks, and the ledger. |

## User Instruction Precedence

Treat the user's latest explicit instruction as the highest operating input
inside system safety, the authorized account/action scope, immutable Thread
identity, submission certainty, and real current platform capability. It replaces
conflicting defaults, heuristics, recovery suggestions, historical risk weight,
and old mission fields. Defaults fill only fields the user did not supply.

Historical ended warnings, rate limits, and failures remain ledger evidence; they
do not block a new mission or force a recovery tier. Pause an action only from
current page/tool evidence that it cannot run. Preserve the user's instruction
and resume it automatically after the observable blocker clears. Ask again only
for genuinely missing/expanded authorization, a human-only login/challenge,
uncertain submission, or another non-inferable safety decision.

## Two-Phase Bootstrap

1. **Install, preflight, and ask:** immediately rename this same task
   `TikTok 启动台`, then use `version-management.md` to automatically
   install or upgrade a valid newer bundle, no-op, defer, block, or roll back the complete versioned
   `thread-supervisor` plus `tiktok-web-operations` bundle. Never hot-reload an
   active TikTok runtime or merge old/new files. Version availability alone is
   never a user confirmation point: after installation validation, continue in
   the same turn and prove Chrome
   control, exact TikTok login, absence of blocking warnings, required thread
   tools, starter-task self-registration, exact `gpt-5.6-luna/high` executor
   creation support, dedicated-tab isolation, exact-target mutation-conflict
   detection, local time,
   and a writable ledger. Keep TikTok read-only, finalize only the bootstrap tab,
   promote the same task in place to coordinator, rename it `TikTok 主控台`,
   return the guided direction/duration prompt, and wait one user turn. If a
   human-only repair remains, stay `TikTok 启动台` until recheck succeeds.
2. **Resolve and operate:** after the healthy user replies, resolve the requested
   direction/persona and duration. Missing direction defaults to North American
   college/dorm life; missing duration defaults to 3 hours. Reuse and prove the
   exact already-promoted `TikTok 主控台` ID, pin it, and create only one unpinned `TikTok 执行台`
   with Luna/High, exchange both IDs, prove executor-to-coordinator callback,
   dispatch the read-only first-run stability smoke, and require real page proof
   before a full calibration block or mutation. Keep both tasks persistent and
   unarchived. If the Skill was already installed and the first user message is
   already a clear mission, use quick health reuse, promote/rename the same task,
   and begin in that same turn without repeating the full setup handoff.

A failed hard dependency stops phase 2 and returns one concrete repair action. Do not silently fall back to a subagent, a different model, a different reasoning effort, or one combined Thread.

## Direction Profile Contract

Treat direction as a product and audience decision, not merely a keyword list. Resolve `persona_name`, `target_audience`, `region_language`, `content_pillars`, `excluded_topics`, `voice_and_comment_style`, `search_seed_clusters`, `future_post_alignment`, `duration`, and `operation_stop_at`. This profile keeps searches, consumption, engagement, comment voice, and future publishing coherent. Describe it as a consistent audience signal hypothesis; never promise a particular recommendation or distribution outcome.

`region_language` must have a mission value, but it is not normally a user-input
gate. Apply explicit values first; otherwise infer from intended future content
when clear. For a universal consumer/lifestyle direction such as dogs, pets,
food, travel, or humor, default non-blockingly to `global English with North
American bias`, let comments match the qualified video's language, record the
assumption, and start. The user may override it at the next safe item boundary.
Ask only when location/language changes an irreversible or materially different
authorized action, such as local services/regulations, a location-specific
publication, or an ambiguous reply. Never stop generic search-led calibration
merely to ask for region or language.

Apply the same low-blocking rule to optional intensity, sub-pillar mix, comment
tone detail, and future-post format. Fill safe defaults, disclose them once, and
start. Preferences are not authorization boundaries.

When the healthy user replies `继续` or `开始` without specifics, use North American college/dorm life for 3 hours at standard intensity. If the user supplies only direction or only duration, fill the other field from that default and start without another confirmation. Any later explicit direction, duration, intensity, or action change supersedes the corresponding old mission fields and updates the executor authority envelope at the next safe item boundary without a second confirmation.

## Operating Stage Gate

Before either Thread acts, read `references/role-and-stage-contract.md`, record
exactly one current stage, and require the previous stage's exit proof. The main
console chooses the next bounded outcome; the executor makes only candidate-
level judgments inside that accepted mission. One executor activation may finish
multiple logical training units and Feed checkpoints. It yields only at a natural
runtime boundary, current blocker, or cutoff, with a durable checkpoint, owned-
tab release, and callback. A timer never defines unit duration, changes a stage,
or proves completion by itself.

## Control Rules

- Use the user's existing Chrome profile and TikTok login. Never enter or store credentials.
- If TikTok still proves logged out or account-mismatched after the bounded
  same-Chrome account recheck, leave the page as a handoff and ask the user to
  restore the expected login manually.
- Each Chrome-control session owns only its own tabs. The executor normally creates a dedicated tab with `chrome.tabs.new()` and must never claim, navigate, close, or reuse a tab owned by another task. The coordinator never touches Chrome; bootstrap may use one disposable read-only tab and must finalize only that tab.
- Keep exactly two persistent operating Threads: this coordinator plus one
  executor. Do not create a second coordinator, use subagents, or create
  analyst/driver descendants.
- Pin only `TikTok 主控台`. Keep the registered `TikTok 执行台` unpinned and
  unarchived, including while idle between blocks.
- Do not use Goal Mode for persistence. Neither operating Thread may call `create_goal`, `update_goal`, or `spawn_agent`. The executor never creates a replacement. The coordinator may create at most one replacement only through the definitive `STALE_OWNER_TOMBSTONE` transaction in `references/operating-model.md`.
- Before executor creation or any mutation, inspect active TikTok Threads only for tab ownership, concurrent-account attribution, and exact target/action submission conflicts. Another task using Chrome, TikTok, or the same account is never by itself a blocker and must not be interrupted or archived. Create this run's own tab and continue. Record `concurrent_same_account_activity=true` plus `recommendation_attribution_contaminated=true`, and make no causal feed claims. Pause only the exact target/action whose same-type submission is concurrently in flight or uncertain; other browsing and different-target authorized actions continue.
- Use only registered cross-thread IDs. The executor reports solely to this
  starter task after it becomes `TikTok 主控台`; never callback to a
  Skill-development task or any other bootstrap task.
- Treat `TikTok 主控台` as the only user decision surface, but do not elevate
  routine operating friction into a decision. Empty candidates, prohibited or
  ambiguous candidates/routes, page faults, recovered network/Chrome faults,
  missing evidence, and single-action/lane failures are ledger outcomes; skip or
  suspend only that exact scope while other safe work continues. Ordinary
  recovery does not callback or wait for the user. At a natural yield or hard
  blocker, release owned Chrome, checkpoint, and callback only the registered
  coordinator. Ask the user only for the live hard-blocker whitelist in
  `references/blocker-minimization.md`; otherwise store the shortest
  `auto_resume_condition` and let a later Heartbeat continue the unchanged
  mission. Uncertain mutation freezes only its exact target/action and is never
  resubmitted.
- Use the canonical two-phase registry contract. The create prompt carries one
  inert canonical bootstrap envelope; after `create_thread` returns its exact ID,
  `SELF_REGISTRY` carries one stored canonical identity object. Dispatches,
  callbacks, and heartbeat prompts use exact registry/direction/authority/mission
  references and never retype those values as natural-language snapshots.
- Keep immutable identity separate from versioned direction/authority/mission
  objects and mutable owner/heartbeat/progress/resume/finalization state. Re-read their
  accepted hashes plus exact tool target IDs before every dispatch, callback,
  heartbeat, stop, replacement, or archive. Any unresolved reference mismatch
  stops before Chrome and enters one bounded `REGISTRY_RECONCILIATION`; it never
  triggers repeated prompt rewriting.
- Every `create_thread` and operational `send_message_to_thread` call must specify `gpt-5.6-luna` plus `high`. If the runtime rejects that combination, stop instead of substituting another model.
- Start the real continuous mission immediately in the current user turn and
  accept its first search-training proof from real evidence. Normal persistence
  is callback-driven: one executor activation may finish multiple logical units;
  after a natural yield the executor callbacks the coordinator, which validates
  the checkpoint and immediately resumes the same mission without waiting for a
  timer. For a timed run, create exactly one long-running repeat-on
  `coordinator_heartbeat` targeting the exact coordinator, normally hourly,
  with finite cutoff protection and verified next-run local/UTC readback.
- The coordinator Heartbeat is read-only until it proves a broken callback
  chain. It verifies executor liveness, new turn/proof, recent ledger progress,
  resume state, binding, next run, and cutoff. If the executor is running, it
  does nothing. If the executor is unexpectedly idle/yielded before cutoff, it
  resumes the same mission through the coordinator from the validated
  checkpoint. It never touches Chrome or performs mutation.
- The executor never creates, updates, renews, pauses, or deletes an automation.
  Do not create an executor-targeted operation Heartbeat, use `COUNT=1`
  self-renewal, or make a timer the normal boundary between logical units.
  `SCHEDULER_CONTINUATION_FAILURE` means the callback chain failed and the
  coordinator Heartbeat must repair the same run without overlapping work.
- Keep the correctly bound coordinator Heartbeat repeat-on through ordinary page,
  network, Chrome, route/client-block, rendering, Feed-transition, and lane
  failures. A later wake automatically retries the safe failed surface and
  continues unaffected work. Never ask whether to retry a normal technical
  failure. Uncertain mutation freezes only that exact action/lane and is never
  retried; it does not retire any Heartbeat.
- Retire the coordinator Heartbeat only after explicit user stop, `operation_stop_at`, objective
  completion plus terminal executor release, or verified no-gap replacement of
  a misbound/duplicate/misconfigured timer. Create/read back the replacement,
  switch the registry binding, then retire the old timer.
- Set `heartbeat_receipt_policy=always_three_lines`. After the coordinator Heartbeat is created and
  every valid tick, first view/read back the exact registered automation, then
  tell the user in exactly three lines what finished, the verified next local
  heartbeat time, and one next bounded plan. Never expose an inferred schedule.
- On a true first install, persist
  `first_install_supervision=PENDING` outside the managed Skill tree. After the
  user's first real run completes identity handshake and stability smoke, the
  verified `TikTok 主控台` consumes that marker and owns one first-hour read-only watch
  window with cumulative checkpoints near `+15`, `+35`, and `+60` minutes,
  capped by `operation_stop_at`. Each checkpoint reads only the registered
  executor's status/callback/ledger, emits only the fixed three-line receipt when
  healthy, and centralizes risk in `TikTok 主控台`. Persist `CONSUMED` at one hour, early stop, or run end,
  but retain the durable coordinator Heartbeat until terminal executor release is
  verified. Never recreate the overlay after an upgrade, restart, or later
  operation. If automation is unavailable, mark `DEGRADED`, disclose once, use
  callbacks only, and still consume it.
- On heartbeat wakeup require exact automation/run/role binding:
  `waking_thread_id == targetThreadId == coordinator_thread_id`. A mismatch
  returns `MISBOUND_HEARTBEAT_NO_ACTION`; it must not inspect TikTok or dispatch
  work.
- Only a live hard blocker from `blocker-minimization.md` may open the whole-run
  recovery circuit. Candidate, route, page, technical, evidence, action, and lane
  failures never do. After bounded recovery, continue another safe scope or wait
  for the exact automatic resume condition. Historical ended events never keep a
  circuit open.
- Scope circuit breakers by lane. A For You next/down failure with healthy
  account, dedicated-tab control, and search-origin playback marks the held-out
  validation `partial|unavailable`; after two consecutive occurrences, disable
  only that validation lane for the runtime. Do not require a user decision or
  stop qualified search consumption unless the failure crosses those safety
  boundaries.
- Treat an expected gate failure as a terminal data branch, not an exception that returns to reasoning. Once `count/visible/enabled/identity` fails, write the result, release Chrome, and callback without another diagnostic.
- Prefer TikTok's visible native next/down control for feed fidelity. Use incremental scrolling only when the control is unavailable and the coordinator explicitly dispatches a scroll-only fallback block. Never switch transition methods inside one checkpoint. Do not add random delays, cursor jitter, or fake human behavior.
- Identify next/down with a direction-specific exact live signature; never use a broad enabled-button locator, because the up control normally becomes enabled after the first advance. Re-resolve the same exact down signature after every DOM movement.
- Never reuse a Chrome tab ID from a prior turn, prompt, ledger, or memory. At
  normal activation/resume, use `chrome.tabs.new()` to create the executor's
  dedicated tab and navigate it to TikTok; use an existing current-session tab
  only when this executor created or already controls it. Use `user.openTabs()`
  plus `user.claimTab()` only for an explicit user-requested handoff or
  continuation of a known unclaimed tab. If an existing tab reports another
  browser session, leave it untouched and create a new tab. Stop the mission only
  when the sole allowed Chrome control remains unavailable after bounded
  reconnect/rebind or the expected account requires user restoration.
- Classify Chrome/page failures before declaring platform risk. Keep stale tab/browser disconnect, DNS/network `ERR_*`, proxy/TLS, HTTP status, `ERR_BLOCKED_BY_CLIENT`, and blank/render failures distinct. In the original logged-in Chrome only: log error+URL, retry the same URL once after a short wait, use a fresh dedicated tab from the same browser binding when needed, test same-domain home and a neutral HTTPS site in a temporary diagnostic tab, then re-confirm account/target/warnings before resuming. Generate `likely_cause` only from the exact code plus those probes and present it as `可能原因`, never a confirmed root cause. Never switch browser, clear cookies, change proxy/TLS, bypass login, or retry an uncertain mutation. Persistent failure callbacks `TikTok 主控台`; a recovered transient does not end the long run, disable mutation lanes, or create a standalone user interruption.
- A For You checkpoint is invalid if page resets are used to obtain later samples. Record exact before/after card identity for every transition. If native movement does not advance, repeats a card, loses identity, or would require a reset, record `transition_failure` or `duplicate` and stop the checkpoint; never reset to manufacture another item. Reset is allowed only for the initial entry before position 1 or a separately declared hard recovery after the block has stopped.
- Append raw evidence after every consumed search-origin post, after each
  five-card assessment, and at For You validation checkpoints. Validate each
  JSONL line immediately; a malformed append suspends further mutation, runs one
  bounded local repair, and otherwise yields an automatic-resume checkpoint. It
  is not a user decision or whole-mission blocker.
- Keep post likes, favorites, reposts, generic shares, proactive comments, comment likes, `Not interested`, follows, replies, publishing, and profile changes as separate capability lanes.
- A standing vertical-feed envelope may authorize selective post likes, favorites, reposts, and proactive comments, but each lane must first pass its own one-action persistence gate in the current account/runtime. For Favorite/save, verify the selected state immediately, again after roughly 3 seconds, and again after a 10-second total server-settlement window before reloading; only then run reload/reopen and account-level Favorites evidence. This is a consistency wait, not simulated-human behavior. A current failure pauses only that lane for the current runtime; a later explicit mission may run one fresh gate without another authorization prompt. Do not cancel unrelated authorized lanes unless a current platform warning, challenge, or uncertain submission makes all mutation unsafe.
- Repost means TikTok's actual `Repost`/`Undo repost` state. Opening the visible Share action sheet is allowed as a read-only navigation step when TikTok nests Repost there; opening the sheet is not itself a successful Repost. Inside it, click only an explicit `Repost` control. Never click or substitute generic Share, copy-link, send-to-recipient, or another share target, and never infer persistence from the sheet merely opening.
- Use distinct strong-core posts for first like, favorite, repost, and comment gates so one action does not contaminate another lane's evidence. After verification, choose the smallest genuine signal rather than stacking multiple actions on each post.
- Do not set engagement quotas. Zero outward actions is valid when quality, audience fit, rights, or persistence gates fail.
- Never automate account creation, operate accounts in bulk, manipulate engagement, evade enforcement, or distribute high-volume repetitive content.
- Optimize comments for contextual wit and organic community response, not a claimed ranking formula. Record later comment likes/replies when visible, but never promise that they increase account weight and never use engagement bait.
- Record content rights, disclosures, and AIGC labeling before publishing.
- Use Chinese for user reports; retain exact URLs, handles, hashtags, and UI labels.

## Checks

### Check A — before drafting

- Correct account and clean-enough account state.
- Clear audience, content pillar, and intended viewer action.
- Live context evidence rather than copied labels.
- Recent-history comparison and non-repetitive creative.
- Rights/disclosure path and visible web eligibility.

### Check B — before acting

- Exact account, URL/asset, text/settings, privacy, disclosure, and schedule time.
- No private information, fake claim, copied comment, unsupported metric, or uncertain prior submission.
- The latest instruction already covers this item, or the active standing envelope matches every field. Never reconfirm a field the user already supplied.

After acting, verify persisted state. Never duplicate an uncertain send.

## Stop Conditions

Stop only the exact affected mutation/lane for a current login mismatch,
CAPTCHA, verification challenge, rate limit, warning/restriction, copyright
failure, missing rights/disclosure, lost executor ownership, uncertain
submission, or persistence failure. Timed waits auto-resume; uncertain
submission is never retried; search/view and independent safe lanes continue.
Detect system warnings from explicit current system UI, never from ordinary
caption/hashtag/comment text or historical ledger entries. Stop the whole mission
and ask the user only for `references/blocker-minimization.md`'s hard whitelist.

## Thread Reporting Contract

For any persistent two-Thread run, read and use the authoritative
`Callback schema`, `Three-line heartbeat receipt`, `Whole-run completion
transaction`, and `Simple user result` sections in
`references/operating-model.md`. Do not copy or locally reconstruct those
schemas in dispatch prompts.

Core invariants remain: every natural yield, blocker, or terminal event gets a
durable checkpoint/callback; every non-`completed` result requires coordinator
handling without deleting Heartbeats; the executor asks no user question;
ordinary progress is not whole-run completion; terminal completion requires
verified executor release. Ordinary evidence stays in the ledger, and user-
facing timed receipts never add a fourth line.
