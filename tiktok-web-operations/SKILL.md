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

For persistent operation, use exactly two user-owned Codex Threads. The starter
task remains the coordinator and creates only one executor. Both operational
roles use `model=gpt-5.6-luna` and `thinking=high`. Use `$thread-supervisor` for
generic registry, callback, heartbeat, and lifecycle mechanics.

| Thread | Owns | Must not do |
|-|-|-|
| Current starter task, final title `TikTok 主控台` | One objective: advance or stop the authorized run at the correct time and own every user decision | Navigate or operate TikTok |
| `execution_thread` — final title `TikTok 执行台` | One objective: execute exactly the current bounded block, record evidence, release Chrome, callback, and idle | Broaden scope, infer approval, alter strategy, create other Threads, or contact the Skill-development Thread |

Direction, persona, authorization, capability matrix, risk rules, ledger, and
deadline are role inputs and constraints. They are never additional independent
objectives. Do not load either Thread with product research, Skill maintenance,
or another operating mission during an active run.

The starter task first installs the bundled Skills, runs read-only preflight,
returns the guided direction/duration prompt, and waits. After the user's second
message, it self-registers its exact Thread ID, becomes the coordinator, creates
one persistent executor, proves the callback handshake, and obtains first real
operation proof. It does not archive itself. Never use a subagent, agent tree,
or agent-path callback for this system.

Naming follows `<platform> <responsibility>台`. After exact identity proof, pin
`TikTok 主控台` and explicitly keep `TikTok 执行台` unpinned. Keep the registered
pair unarchived, including while idle. Archive only completed temporary probes or
a released, retired executor after removing its heartbeat/tab/mutation ownership.

Use `references/operating-model.md` for the exact creation, handshake, callback, lifecycle, and recovery protocol.
Before any persistent Thread or heartbeat action, also read
`$thread-supervisor/references/identity-and-automation.md`.

## Route The Request

| Request | Read |
|-|-|
| Install from GitHub, run dependency checks, or bootstrap | `references/version-management.md`, `references/startup-health-check.md`, `references/stability-and-circuit-breakers.md`, `references/runtime-and-recovery.md`, `references/operating-model.md` |
| Package, publish, upgrade, overwrite, downgrade, or distribute | `references/version-management.md`, `references/distribution-and-upgrades.md` |
| Broad operating request | all relevant references below |
| Research trends or choose content | `references/loci-content-system.md`, `references/platform-boundaries.md` |
| Browse/scroll or leave short comments | `references/feed-browsing-and-comments.md`, `references/engagement-and-analytics.md`, `references/platform-boundaries.md` |
| Persistently calibrate recommendations | `references/operating-model.md`, `references/stability-and-circuit-breakers.md`, `references/persistent-feed-operations.md`, `references/engagement-and-analytics.md`, `references/runtime-and-recovery.md` |
| Upload, publish, or schedule | `references/publishing-and-scheduling.md`, `references/platform-boundaries.md` |
| Review comments or analytics | `references/engagement-and-analytics.md`, `references/loci-content-system.md` |

## Entrypoint Contract

| User says | Execute |
|-|-|
| Installer Prompt or first `帮我运营 TikTok` before bootstrap is initialized | Automatically install or upgrade when the incoming bundle is newer, validate the installed bundle, and continue read-only preflight in the same turn. Return the guided direction/duration handoff only after preflight; do not pause merely to announce an available upgrade, create operating Threads, or touch TikTok state yet. |
| Healthy handoff followed by `继续`, `开始`, a direction, or a duration | Resolve the `direction_profile`, keep this task as coordinator, create one persistent executor, obtain first operation proof, and begin the bounded run. |
| `找热点`, `做选题`, `研究竞品` | Research only; do not mutate TikTok. |
| `刷视频`, `看看推荐`, `找能评论的视频` | Browse a bounded sample; do not infer permission for likes, favorites, reposts, follows, or comments. |
| `持续刷`, `定向刷`, `垂直刷`, `养推荐流`, `两个 Thread 运营` | Keep this task as coordinator and dispatch bounded blocks to its one persistent execution Thread with `send_message_to_thread`. |
| `刷视频并互动`, `点赞收藏评论`, `收藏并 repost`, `去发几个评论` | Find strong core candidates and use only independently verified like, favorite, repost, or proactive-comment lanes covered by the exact standing envelope. Treat Repost as distinct from generic Share. |
| `评论不用问我`, `自动发短评论` | Activate `autonomous_comment_mode` only for the exact account/audience/voice envelope; enforce the 30-word hard limit and every persistence stop rule. |
| `发视频`, `上传`, `排期` | Validate the exact asset/settings, confirm, execute one item, and verify. |
| `看数据`, `复盘` | Use account/TikTok Studio analytics read-only. |
| `现在状态`, `有什么风险` | Answer from coordinator state, execution callbacks, and the ledger. |

## Two-Phase Bootstrap

1. **Install, preflight, and ask:** use `version-management.md` to automatically
   install or upgrade a valid newer bundle, no-op, defer, block, or roll back the complete versioned
   `thread-supervisor` plus `tiktok-web-operations` bundle. Never hot-reload an
   active TikTok runtime or merge old/new files. Version availability alone is
   never a user confirmation point: after installation validation, continue in
   the same turn and prove Chrome
   control, exact TikTok login, absence of blocking warnings, required thread
   tools, starter-task self-registration, exact `gpt-5.6-luna/high` executor
   creation support, no conflicting same-account mutation executor, local time,
   and a writable ledger. Keep TikTok read-only, finalize only the bootstrap tab,
   return the guided direction/duration prompt, and wait one user turn.
2. **Resolve and operate:** after the healthy user replies, resolve the requested
   direction/persona and duration. Missing direction defaults to North American
   college/dorm life; missing duration defaults to 3 hours. Rename this task
   `TikTok 主控台` after temporary nonce-based self-registration, prove its exact
   ID, pin it, and create only one unpinned `TikTok 执行台`
   with Luna/High, exchange both IDs, prove executor-to-coordinator callback,
   dispatch the read-only first-run stability smoke, and require real page proof
   before a full calibration block or mutation. Keep both tasks persistent and
   unarchived.

A failed hard dependency stops phase 2 and returns one concrete repair action. Do not silently fall back to a subagent, a different model, a different reasoning effort, or one combined Thread.

## Direction Profile Contract

Treat direction as a product and audience decision, not merely a keyword list. Resolve `persona_name`, `target_audience`, `region_language`, `content_pillars`, `excluded_topics`, `voice_and_comment_style`, `search_seed_clusters`, `future_post_alignment`, `duration`, and `operation_stop_at`. This profile keeps searches, consumption, engagement, comment voice, and future publishing coherent. Describe it as a consistent audience signal hypothesis; never promise a particular recommendation or distribution outcome.

Region and language are required direction fields because they change queries,
consumption, and comment voice. For a custom direction, ask one necessary
question when they cannot be safely inferred; do not silently collapse a broad
topic such as `dogs` into a Chinese- or English-only audience.

When the healthy user replies `继续` or `开始` without specifics, use North American college/dorm life for 3 hours at standard intensity. If the user supplies only direction or only duration, fill the other field from that default and start without another confirmation. The coordinator owns later direction changes and must update the executor envelope before the next block.

## Execution Thread Loop

1. Read the coordinator Thread ID and operating envelope: account, objective, audience, exclusions, authorizations, stop conditions, ledger path, and result schema.
2. Confirm this exact Thread is the registered TikTok executor and sole same-account mutation writer. Create or recover only its own dedicated Chrome tab, then verify TikTok account, time context, visible warnings, and capabilities.
3. Read account health, current page state, recent relevant history, and ledger tail.
4. For recommendation work, run the search-training block in `references/persistent-feed-operations.md`; label `core`, `adjacent`, `irrelevant`, and `harmful_to_direction`. Search cards only assess query quality. Count training only after opening a strong-core result from search/bridge, verifying direct post identity/playback, and watching through its premise/payoff.
   Treat For You as a separate held-out validation block, normally 5–10 continuous items after two training blocks or 20–30 qualified search views. Preserve its native-feed invariants, but a lane-local transition failure must not erase completed search training or stop a healthy search-led run.
5. Run Check A before drafting and Check B on the exact action. Never mechanically reuse a comment, caption, hook, or asset.
6. Before any mutation, require exact action-time confirmation or a matching active standing action envelope.
7. Execute one state-changing action at a time. Gate every action type independently and verify persisted state.
8. Update the sole-writer ledger.
9. At block completion or a meaningful event, call `send_message_to_thread` to the registered coordinator ID with `model=gpt-5.6-luna`, `thinking=high`, and the structured result. Then become idle until the next message.

## Control Rules

- Use the user's existing Chrome profile and TikTok login. Never enter or store credentials.
- If TikTok is logged out, leave the page as a handoff and ask the user to log in manually.
- Each Chrome-control session owns only its own tabs. The executor normally creates a dedicated tab with `chrome.tabs.new()` and must never claim, navigate, close, or reuse a tab owned by another task. The coordinator never touches Chrome; bootstrap may use one disposable read-only tab and must finalize only that tab.
- Keep exactly two persistent operating Threads: this coordinator plus one
  executor. Do not create a second coordinator, use subagents, or create
  analyst/driver descendants.
- Pin only `TikTok 主控台`. Keep the registered `TikTok 执行台` unpinned and
  unarchived, including while idle between blocks.
- Do not use Goal Mode for persistence. Neither operating Thread may call `create_goal`, `update_goal`, `spawn_agent`, or create replacement workers.
- Before every executor creation or replacement, inspect active TikTok Threads. Block same-account mutation only when another mutation executor is active/uncertain or a submission may be in flight. An unrelated task using Chrome or another TikTok tab is not a global blocker and must not be interrupted or archived. If it browses the same account concurrently, record recommendation-attribution contamination; do not attribute feed changes to one task. Archiving alone is not release proof for an incumbent mutation executor.
- Use only registered cross-thread IDs. The executor reports solely to this
  starter task after it becomes `TikTok 主控台`; never callback to a
  Skill-development task or any other bootstrap task.
- Treat `TikTok 主控台` as the only user decision surface. On `blocked`,
  `validation_failed`, `needs_decision`, `key_risk`, uncertain submission, or a
  platform risk, the executor stops the block, releases its own Chrome, writes
  evidence, callbacks only the registered coordinator, and becomes idle. It
  never asks the user to continue inside `TikTok 执行台`, self-recovers, or dispatches
  another block. The coordinator pauses dispatch, consolidates one risk prompt,
  and resumes only after a decision in `TikTok 主控台` or a verified external-state
  change.
- Treat Thread IDs, account, ledger path, mutation authorization, role, model, and thinking as immutable registry fields. Copy them byte-for-byte into dispatches and compare them before Chrome connection; any mismatch terminates the block without page navigation. The `send_message_to_thread` tool-call target itself is part of this check and must equal the registered executor ID.
- Include `run_id`, coordinator/executor IDs, host/project identity, automation
  owner, heartbeat ID/target, authority version, ledger, stop time, exact titles,
  and pin policy in the immutable run registry. Re-read it before every dispatch,
  callback, heartbeat, stop, replacement, or archive. Titles and pin state remain
  presentation fields; IDs remain authoritative identity.
- Every `create_thread` and operational `send_message_to_thread` call must specify `gpt-5.6-luna` plus `high`. If the runtime rejects that combination, stop instead of substituting another model.
- Prefer callback-driven sequencing. Do not poll a running Thread or interrupt it with unrelated work. The coordinator sends the next block only after completion, block, validation failure, decision request, or key risk.
- Run exactly one bounded block per executor turn. For an unattended duration,
  an optional coordinator-only heartbeat may schedule the next block after a
  completed callback or enforce `operation_stop_at`. It must be created from
  the verified coordinator with explicit `targetThreadId` equal to the
  coordinator ID, then viewed and stored only after exact binding proof. The
  executor and every bootstrap, Skill-development, sibling, or historical task
  never own or manage it.
- For every timed operation expected to exceed one bounded block, make one
  verified coordinator-owned heartbeat the durable run timer. Callback drives
  event-time decisions; heartbeat drives low-frequency status checks, missed-
  callback recovery, next due time, and `operation_stop_at`. Store and reuse one
  logical automation ID for the run, never one per block. On a tick, do not
  touch Chrome or overlap a running executor; dispatch at most one block only
  when the executor is idle, no decision is pending, authorization remains, and
  time remains. At the deadline, start the terminal transaction; do not treat a
  heartbeat tick as completion. Delete the timer only after the executor returns
  verified final release evidence and the coordinator finalizes the run.
- Set `heartbeat_receipt_policy=always_three_lines`. After timer creation and
  every valid tick, first update/reuse and read back the exact owned timer, then
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
  but retain the shared durable timer until terminal executor release is
  verified. Never recreate the overlay after an upgrade, restart, or later
  operation. If automation is unavailable, mark `DEGRADED`, disclose once, use
  callbacks only, and still consume it.
- On heartbeat wakeup require
  `waking_thread_id == targetThreadId == coordinator_thread_id` and the exact
  registered automation ID. A mismatch returns
  `MISBOUND_HEARTBEAT_NO_ACTION`; it must not inspect TikTok or dispatch work.
- A `blocked` or `key_risk` callback opens the recovery circuit in `stability-and-circuit-breakers.md`. Do not self-declare a fresh audit, rebuild a worker, or hop across transition methods. Wait for a user instruction or verified external-state change after the bounded recovery budget is exhausted.
- Scope circuit breakers by lane. A For You next/down failure with healthy
  account, dedicated-tab control, and search-origin playback marks the held-out
  validation `partial|unavailable`; after two consecutive occurrences, disable
  only that validation lane for the runtime. Do not require a user decision or
  stop qualified search consumption unless the failure crosses those safety
  boundaries.
- Treat an expected gate failure as a terminal data branch, not an exception that returns to reasoning. Once `count/visible/enabled/identity` fails, write the result, release Chrome, and callback without another diagnostic.
- Prefer TikTok's visible native next/down control for feed fidelity. Use incremental scrolling only when the control is unavailable and the coordinator explicitly dispatches a scroll-only fallback block. Never switch transition methods inside one checkpoint. Do not add random delays, cursor jitter, or fake human behavior.
- Identify next/down with a direction-specific exact live signature; never use a broad enabled-button locator, because the up control normally becomes enabled after the first advance. Re-resolve the same exact down signature after every DOM movement.
- Never reuse a Chrome tab ID from a prior turn, prompt, ledger, or memory. At normal block start, use `chrome.tabs.new()` to create the executor's dedicated tab and navigate it to TikTok; use an existing current-session tab only when this executor created or already controls it. Use `user.openTabs()` plus `user.claimTab()` only for an explicit user-requested handoff or continuation of a known unclaimed tab. If an existing tab reports another browser session, leave it untouched and create a new tab; that message is not a global Chrome blocker. Stop only when new-tab creation/control fails or the dedicated tab cannot prove the expected TikTok account.
- Classify Chrome/page failures before declaring platform risk. Keep stale tab/browser disconnect, DNS/network `ERR_*`, proxy/TLS, HTTP status, `ERR_BLOCKED_BY_CLIENT`, and blank/render failures distinct. In the original logged-in Chrome only: log error+URL, retry the same URL once after a short wait, use a fresh dedicated tab from the same browser binding when needed, test same-domain home and a neutral HTTPS site in a temporary diagnostic tab, then re-confirm account/target/warnings before resuming. Never switch browser, bypass TLS/login, or retry an uncertain mutation. Persistent failure callbacks `TikTok 主控台`; a recovered transient does not end the long run or disable mutation lanes.
- A For You checkpoint is invalid if page resets are used to obtain later samples. Record exact before/after card identity for every transition. If native movement does not advance, repeats a card, loses identity, or would require a reset, record `transition_failure` or `duplicate` and stop the checkpoint; never reset to manufacture another item. Reset is allowed only for the initial entry before position 1 or a separately declared hard recovery after the block has stopped.
- Append raw evidence after every consumed search-origin post, after each
  five-card assessment, and at For You validation checkpoints. Validate each
  JSONL line immediately; a malformed append stops the block before more
  browsing.
- Keep post likes, favorites, reposts, generic shares, proactive comments, comment likes, `Not interested`, follows, replies, publishing, and profile changes as separate capability lanes.
- A standing vertical-feed envelope may authorize selective post likes, favorites, reposts, and proactive comments, but each lane must first pass its own one-action persistence gate. For Favorite/save, verify the selected state immediately, again after roughly 3 seconds, and again after a 10-second total server-settlement window before reloading; only then run reload/reopen and account-level Favorites evidence. This is a consistency wait, not simulated-human behavior. A failure disables only that lane; do not cancel unrelated authorized lanes unless a platform warning, challenge, or uncertain submission makes all mutation unsafe.
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
- Exact confirmation covers this item, or the active comment envelope matches every field.

After acting, verify persisted state. Never duplicate an uncertain send.

## Stop Conditions

Stop mutation for login mismatch, CAPTCHA, verification challenge, rate limit, warning/restriction, copyright failure, missing rights/disclosure, lost executor ownership, uncertain submission, or persistence failure. Read-only inspection may continue only when safe. Detect system warnings from explicit system UI, never from ordinary caption/hashtag/comment text. Apply the recovery circuit breaker after repeated failures.

## Thread Reporting Contract

The execution Thread returns one structured callback after every bounded block:

```text
status: completed | blocked | validation_failed | needs_decision | key_risk
callback_scope: block | run_terminal
terminal_event: NONE | EXECUTOR_RELEASED
release_state: NONE | STOPPED_AND_RELEASED | RELEASE_UNVERIFIED
run_completion_reason: NONE | deadline_reached | user_stopped | objective_complete | terminal_risk | cancelled
run_id:
coordinator_thread_id:
executor_thread_id:
block_id:
summary:
sample_counts:
search_results_assessed:
qualified_search_views:
feed_validation_status: not_run | verified | partial | unavailable | disabled
feed_validation_sample_count:
runtime_recovery_status: not_needed | recovered | failed | platform_risk
recovery_class: none | tab_binding_stale | browser_disconnected | dns_network | proxy_tls | http_status | blocked_by_client | ambiguous_render
error_code:
failure_scope: none | tab | browser | network_global | tiktok_domain | target_page | platform
recovery_attempts:
account_reverified: true | false | not_needed
composition:
queries_used:
actions_performed:
mutations_count:
capability_matrix_delta:
risks:
affected_scope: lane | current_block | whole_run
safe_to_continue_read_only: true | false
decision_required: true | false
decision_options:
ledger_path:
recommended_next_block:
```

For every non-`completed` status, set `decision_required: true`. The executor's
own final response is only a terse handoff stating that evidence was sent to
`TikTok 主控台` and the executor is idle; it must not contain a user-facing question or
invite the user to reply there.

Use `callback_scope=block`, `terminal_event=NONE`, and `release_state=NONE` for
ordinary rounds. Reserve `run_terminal/EXECUTOR_RELEASED` for the single final
release callback.

Whole-run completion is a separate transaction. At deadline, user stop, or
objective completion, the coordinator sends one terminal `STOP_AND_RELEASE` even
if the executor appears idle. The executor performs no new TikTok action; it
resolves submission certainty, releases its owned tab, writes final cumulative
evidence, and callbacks with `callback_scope=run_terminal`,
`terminal_event=EXECUTOR_RELEASED`, and
`release_state=STOPPED_AND_RELEASED`. Only then may the coordinator retire its
timer, reconcile the ledger, and mark `RUN_COMPLETED`. Missing proof becomes
`RUN_FINALIZATION_BLOCKED`, never a successful completion.

The coordinator reports meaningful checkpoints to the user with:

```text
本轮完成：
发布/处理：
下一轮：
风险：
```

For the whole run, keep the user-facing response to one compact message:

```text
运营完成。运行：<duration>；浏览：<count>；收藏：<count>；Repost：<count>；评论：<count>。风险：无｜<one short risk>。
```

Do not expose heartbeat IDs, callback IDs, registry fields, release-state names,
or the internal completion transaction unless finalization is blocked.

After timer creation and every valid nonterminal heartbeat, use exactly:

```text
本轮完成：<one sentence>
下次心跳：<YYYY-MM-DD HH:mm timezone>
下轮计划：<one bounded purpose>
```

Report the next time only after updating/viewing the exact owned automation and
verifying its target and schedule. If the executor is still running, the plan is
to wait for its callback, not dispatch overlapping work. On a risk, the plan is
to wait for the user's decision and perform no new TikTok action. At the final
tick use `下次心跳：无（进入终止结算）`; after completion use
`下次心跳：无（任务已完成）`.

Ordinary evidence stays in the ledger. See `references/operating-model.md` for cross-thread dispatch and lifecycle rules.
