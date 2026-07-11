---
name: tiktok-web-operations
description: >-
  Run authorized TikTok web operations through the user's logged-in Chrome
  session, including account audits, TikTok Studio analytics, persistent feed
  calibration, search-first vertical browsing, native feed scrolling,
  search/hashtag seeding, short meme-aware comments with optional standing
  authorization, publishing, comment follow-up, verification, and a
  two-persistent-thread coordinator/executor system. Use when the user asks to
  browse or scroll TikTok, train recommendations, search communities or
  keywords, like/favorite/repost/comment, operate, grow, audit, publish,
  schedule, or
  maintain a TikTok account from the web, or package this workflow.
---

# TikTok Web Operations

Use TikTok's web surfaces as an evidence-led operating system. Keep strategy, Chrome execution, publishing, engagement, and analytics separate.

## System Topology

For persistent operation, use exactly two user-owned Codex Threads. Both must be created with `model=gpt-5.6-luna` and `thinking=high`:

| Thread | Owns | Must not do |
|-|-|-|
| `coordination_thread` — title `TikTok 运营主任务` | User conversation, direction, standing authorization, executor supervision, decisions, risk, and final reporting | Navigate or operate TikTok |
| `execution_thread` — title `TikTok Chrome执行任务` | The logged-in Chrome session, ordered browsing, searches, authorized actions, verification, and raw evidence ledger | Broaden scope, infer approval, alter strategy, create other Threads, or contact the Skill-development Thread |

The short-lived installer/bootstrap task first installs and runs read-only preflight, returns the guided direction/duration prompt, and waits. Only after the user replies with a direction/duration or the default start word does it create both persistent Threads, register their IDs, prove a two-way `send_message_to_thread` handshake, obtain first real operation proof, then archive itself. Never use a subagent, agent tree, or agent-path callback for this system.

Use `references/operating-model.md` for the exact creation, handshake, callback, lifecycle, and recovery protocol.

## Route The Request

| Request | Read |
|-|-|
| Install from GitHub, run dependency checks, or bootstrap | `references/startup-health-check.md`, `references/stability-and-circuit-breakers.md`, `references/runtime-and-recovery.md`, `references/operating-model.md` |
| Package, publish, upgrade, or distribute | `references/distribution-and-upgrades.md` |
| Broad operating request | all relevant references below |
| Research trends or choose content | `references/loci-content-system.md`, `references/platform-boundaries.md` |
| Browse/scroll or leave short comments | `references/feed-browsing-and-comments.md`, `references/engagement-and-analytics.md`, `references/platform-boundaries.md` |
| Persistently calibrate recommendations | `references/operating-model.md`, `references/stability-and-circuit-breakers.md`, `references/persistent-feed-operations.md`, `references/engagement-and-analytics.md`, `references/runtime-and-recovery.md` |
| Upload, publish, or schedule | `references/publishing-and-scheduling.md`, `references/platform-boundaries.md` |
| Review comments or analytics | `references/engagement-and-analytics.md`, `references/loci-content-system.md` |

## Entrypoint Contract

| User says | Execute |
|-|-|
| Installer Prompt or first `帮我运营 TikTok` before bootstrap is initialized | Install/upgrade and run read-only preflight, return the guided direction/duration handoff, and wait. Do not create operating Threads or touch TikTok state yet. |
| Healthy handoff followed by `继续`, `开始`, a direction, or a duration | Resolve the `direction_profile`, fill missing fields from defaults, create the two persistent Threads, obtain first operation proof, and begin the bounded run. |
| `找热点`, `做选题`, `研究竞品` | Research only; do not mutate TikTok. |
| `刷视频`, `看看推荐`, `找能评论的视频` | Browse a bounded sample; do not infer permission for likes, favorites, reposts, follows, or comments. |
| `持续刷`, `定向刷`, `垂直刷`, `养推荐流`, `两个 Thread 运营` | Use the two persistent user-owned Threads. The coordinator dispatches bounded blocks to the same execution Thread with `send_message_to_thread`. |
| `刷视频并互动`, `点赞收藏评论`, `收藏并 repost`, `去发几个评论` | Find strong core candidates and use only independently verified like, favorite, repost, or proactive-comment lanes covered by the exact standing envelope. Treat Repost as distinct from generic Share. |
| `评论不用问我`, `自动发短评论` | Activate `autonomous_comment_mode` only for the exact account/audience/voice envelope; enforce the 30-word hard limit and every persistence stop rule. |
| `发视频`, `上传`, `排期` | Validate the exact asset/settings, confirm, execute one item, and verify. |
| `看数据`, `复盘` | Use account/TikTok Studio analytics read-only. |
| `现在状态`, `有什么风险` | Answer from coordinator state, execution callbacks, and the ledger. |

## Two-Phase Bootstrap

1. **Install, preflight, and ask:** install or upgrade the complete versioned Skill, validate it, prove Chrome control, exact TikTok login, absence of blocking warnings, required thread tools, exact `gpt-5.6-luna/high` thread creation support, no conflicting active TikTok executor, local time, and a writable ledger. Keep TikTok read-only, release Chrome, return the exact guided direction/duration prompt from `startup-health-check.md`, and wait one user turn.
2. **Resolve and operate:** after the healthy user replies, resolve the requested direction/persona and duration. Missing direction defaults to North American college/dorm life; missing duration defaults to 3 hours. Create `TikTok 运营主任务` and `TikTok Chrome执行任务` as two separate persistent user-owned Threads with Luna/High; exchange both Thread IDs; prove executor-to-coordinator callback; transfer Chrome ownership to the executor; dispatch the read-only first-run stability smoke in `stability-and-circuit-breakers.md`; require its real page proof before a full calibration block or mutation; then archive only the bootstrap task.

A failed hard dependency stops phase 2 and returns one concrete repair action. Do not silently fall back to a subagent, a different model, a different reasoning effort, or one combined Thread.

## Direction Profile Contract

Treat direction as a product and audience decision, not merely a keyword list. Resolve `persona_name`, `target_audience`, `region_language`, `content_pillars`, `excluded_topics`, `voice_and_comment_style`, `search_seed_clusters`, `future_post_alignment`, `duration`, and `operation_stop_at`. This profile keeps searches, consumption, engagement, comment voice, and future publishing coherent. Describe it as a consistent audience signal hypothesis; never promise a particular recommendation or distribution outcome.

When the healthy user replies `继续` or `开始` without specifics, use North American college/dorm life for 3 hours at standard intensity. If the user supplies only direction or only duration, fill the other field from that default and start without another confirmation. The coordinator owns later direction changes and must update the executor envelope before the next block.

## Execution Thread Loop

1. Read the coordinator Thread ID and operating envelope: account, objective, audience, exclusions, authorizations, stop conditions, ledger path, and result schema.
2. Confirm this exact Thread is the registered sole Chrome executor. Verify TikTok account, time context, visible warnings, and capabilities.
3. Read account health, current page state, recent relevant history, and ledger tail.
4. For recommendation work, run the bounded block in `references/persistent-feed-operations.md`; label `core`, `adjacent`, `irrelevant`, and `harmful_to_direction`.
   Treat each For You checkpoint as one continuous native feed: enter once, then use the visible TikTok next/down control as the default transition. An incremental scroll is allowed only in a separately declared fallback block when no unambiguous visible control exists; never mix button and scroll transitions inside one checkpoint. Never reload, reopen Home, call `goto` on the home route, or navigate away between sampled positions.
5. Run Check A before drafting and Check B on the exact action. Never mechanically reuse a comment, caption, hook, or asset.
6. Before any mutation, require exact action-time confirmation or a matching active standing action envelope.
7. Execute one state-changing action at a time. Gate every action type independently and verify persisted state.
8. Update the sole-writer ledger.
9. At block completion or a meaningful event, call `send_message_to_thread` to the registered coordinator ID with `model=gpt-5.6-luna`, `thinking=high`, and the structured result. Then become idle until the next message.

## Control Rules

- Use the user's existing Chrome profile and TikTok login. Never enter or store credentials.
- If TikTok is logged out, leave the page as a handoff and ask the user to log in manually.
- Chrome is a single-driver resource. Only the execution Thread may navigate, scroll, search, or mutate TikTok. The coordinator and bootstrap task must release Chrome after preflight.
- Keep exactly two persistent operating Threads. Do not use subagents or create analyst/driver descendants.
- Do not use Goal Mode for persistence. Neither operating Thread may call `create_goal`, `update_goal`, `spawn_agent`, or create replacement workers.
- Before every executor creation or replacement, inspect active TikTok Threads and prove the prior Chrome owner returned `STOPPED_AND_RELEASED` with no uncertain submission. Archiving alone is not release proof.
- Use only registered cross-thread IDs. The executor reports solely to `TikTok 运营主任务`; never callback to a Skill-development or bootstrap task.
- Treat Thread IDs, account, ledger path, mutation authorization, role, model, and thinking as immutable registry fields. Copy them byte-for-byte into dispatches and compare them before Chrome connection; any mismatch terminates the block without page navigation.
- Every `create_thread` and operational `send_message_to_thread` call must specify `gpt-5.6-luna` plus `high`. If the runtime rejects that combination, stop instead of substituting another model.
- Prefer callback-driven sequencing. Do not poll a running Thread or interrupt it with unrelated work. The coordinator sends the next block only after completion, block, validation failure, decision request, or key risk.
- Run exactly one bounded block per executor turn. For an unattended duration, an optional coordinator-only heartbeat may schedule the next block after a completed callback or enforce `operation_stop_at`; it never touches Chrome, overlaps a running turn, or bypasses a blocker.
- A `blocked` or `key_risk` callback opens the recovery circuit in `stability-and-circuit-breakers.md`. Do not self-declare a fresh audit, rebuild a worker, or hop across transition methods. Wait for a user instruction or verified external-state change after the bounded recovery budget is exhausted.
- Treat an expected gate failure as a terminal data branch, not an exception that returns to reasoning. Once `count/visible/enabled/identity` fails, write the result, release Chrome, and callback without another diagnostic.
- Prefer TikTok's visible native next/down control for feed fidelity. Use incremental scrolling only when the control is unavailable and the coordinator explicitly dispatches a scroll-only fallback block. Never switch transition methods inside one checkpoint. Do not add random delays, cursor jitter, or fake human behavior.
- Identify next/down with a direction-specific exact live signature; never use a broad enabled-button locator, because the up control normally becomes enabled after the first advance. Re-resolve the same exact down signature after every DOM movement.
- Never reuse a Chrome tab ID from a prior turn, prompt, ledger, or memory. Choose a live TikTok tab only from the current turn's `openTabs()` result by current URL/title/account context; absent or ambiguous selection is a terminal data gate, not an exception or guessing opportunity.
- A For You checkpoint is invalid if page resets are used to obtain later samples. Record exact before/after card identity for every transition. If native movement does not advance, repeats a card, loses identity, or would require a reset, record `transition_failure` or `duplicate` and stop the checkpoint; never reset to manufacture another item. Reset is allowed only for the initial entry before position 1 or a separately declared hard recovery after the block has stopped.
- Append raw evidence incrementally: after each five-result search cluster and at For You positions 1, 5, 10, 15, and 20 (or the final position of a shorter block). Do not wait until the entire block ends to persist all observations.
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
block_id:
summary:
sample_counts:
composition:
queries_used:
actions_performed:
mutations_count:
capability_matrix_delta:
risks:
ledger_path:
recommended_next_block:
```

The coordinator reports meaningful checkpoints to the user with:

```text
本轮完成：
发布/处理：
下一轮：
风险：
```

Ordinary evidence stays in the ledger. See `references/operating-model.md` for cross-thread dispatch and lifecycle rules.
