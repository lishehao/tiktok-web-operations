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
  keywords, like/favorite/comment, operate, grow, audit, publish, schedule, or
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

The short-lived installer/bootstrap task creates both persistent Threads through Codex App thread tools, registers their IDs, proves a two-way `send_message_to_thread` handshake, dispatches the first block, then archives itself. Never use a subagent, agent tree, or agent-path callback for this system.

Use `references/operating-model.md` for the exact creation, handshake, callback, lifecycle, and recovery protocol.

## Route The Request

| Request | Read |
|-|-|
| Install from GitHub, run dependency checks, or bootstrap | `references/startup-health-check.md`, `references/runtime-and-recovery.md`, `references/operating-model.md` |
| Package, publish, upgrade, or distribute | `references/distribution-and-upgrades.md` |
| Broad operating request | all relevant references below |
| Research trends or choose content | `references/loci-content-system.md`, `references/platform-boundaries.md` |
| Browse/scroll or leave short comments | `references/feed-browsing-and-comments.md`, `references/engagement-and-analytics.md`, `references/platform-boundaries.md` |
| Persistently calibrate recommendations | `references/operating-model.md`, `references/persistent-feed-operations.md`, `references/engagement-and-analytics.md`, `references/runtime-and-recovery.md` |
| Upload, publish, or schedule | `references/publishing-and-scheduling.md`, `references/platform-boundaries.md` |
| Review comments or analytics | `references/engagement-and-analytics.md`, `references/loci-content-system.md` |

## Entrypoint Contract

| User says | Execute |
|-|-|
| `帮我运营 TikTok`, `开始运营` | Run read-only preflight, then build the smallest useful operating batch. Outward actions still require exact confirmation unless a matching standing envelope is active. |
| `找热点`, `做选题`, `研究竞品` | Research only; do not mutate TikTok. |
| `刷视频`, `看看推荐`, `找能评论的视频` | Browse a bounded sample; do not infer permission for likes, favorites, follows, or comments. |
| `持续刷`, `定向刷`, `垂直刷`, `养推荐流`, `两个 Thread 运营` | Use the two persistent user-owned Threads. The coordinator dispatches bounded blocks to the same execution Thread with `send_message_to_thread`. |
| `刷视频并互动`, `点赞收藏评论`, `去发几个评论` | Find strong core candidates and use only independently verified like, favorite, or proactive-comment lanes covered by the exact standing envelope. |
| `评论不用问我`, `自动发短评论` | Activate `autonomous_comment_mode` only for the exact account/audience/voice envelope; enforce the 30-word hard limit and every persistence stop rule. |
| `发视频`, `上传`, `排期` | Validate the exact asset/settings, confirm, execute one item, and verify. |
| `看数据`, `复盘` | Use account/TikTok Studio analytics read-only. |
| `现在状态`, `有什么风险` | Answer from coordinator state, execution callbacks, and the ledger. |

## Two-Phase Bootstrap

1. **Install and preflight:** install or upgrade the complete versioned Skill, validate it, prove Chrome control, exact TikTok login, absence of blocking warnings, required thread tools, exact `gpt-5.6-luna/high` thread creation support, time when needed, and a writable ledger. Keep TikTok read-only.
2. **Create and operate:** create `TikTok 运营主任务` and `TikTok Chrome执行任务` as two separate persistent user-owned Threads with Luna/High; exchange both Thread IDs; prove executor-to-coordinator callback; transfer Chrome ownership to the executor; dispatch the first vertical-calibration block; archive only the bootstrap task.

A failed hard dependency stops phase 2 and returns one concrete repair action. Do not silently fall back to a subagent, a different model, a different reasoning effort, or one combined Thread.

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
- Use only registered cross-thread IDs. The executor reports solely to `TikTok 运营主任务`; never callback to a Skill-development or bootstrap task.
- Every `create_thread` and operational `send_message_to_thread` call must specify `gpt-5.6-luna` plus `high`. If the runtime rejects that combination, stop instead of substituting another model.
- Prefer callback-driven sequencing. Do not poll a running Thread or interrupt it with unrelated work. The coordinator sends the next block only after completion, block, validation failure, decision request, or key risk.
- Prefer TikTok's visible native next/down control for feed fidelity. Use incremental scrolling only when the control is unavailable and the coordinator explicitly dispatches a scroll-only fallback block. Never switch transition methods inside one checkpoint. Do not add random delays, cursor jitter, or fake human behavior.
- A For You checkpoint is invalid if page resets are used to obtain later samples. Record exact before/after card identity for every transition. If native movement does not advance, repeats a card, loses identity, or would require a reset, record `transition_failure` or `duplicate` and stop the checkpoint; never reset to manufacture another item. Reset is allowed only for the initial entry before position 1 or a separately declared hard recovery after the block has stopped.
- Append raw evidence incrementally: after each five-result search cluster and at For You positions 1, 5, 10, 15, and 20 (or the final position of a shorter block). Do not wait until the entire block ends to persist all observations.
- Keep post likes, favorites, proactive comments, comment likes, `Not interested`, follows, replies, publishing, and profile changes as separate capability lanes.
- A standing vertical-feed envelope may authorize selective post likes, favorites, and proactive comments, but each lane must first pass its own one-action persistence gate. A failure disables only that lane; do not cancel unrelated authorized lanes unless a platform warning, challenge, or uncertain submission makes all mutation unsafe.
- Use distinct strong-core posts for first like, favorite, and comment gates so one action does not contaminate another lane's evidence. After verification, choose the smallest genuine signal rather than stacking all three actions on each post.
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

Stop mutation for login mismatch, CAPTCHA, verification challenge, rate limit, warning/restriction, copyright failure, missing rights/disclosure, lost executor ownership, uncertain submission, or persistence failure. Read-only inspection may continue only when safe.

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
