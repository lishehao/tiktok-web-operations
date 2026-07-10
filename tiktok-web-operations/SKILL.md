---
name: tiktok-web-operations
description: >-
  Run authorized TikTok web operations through the user's logged-in Chrome
  session, including account audits, TikTok Studio analytics, trend research,
  persistent feed calibration, search-first vertical browsing, native feed
  scrolling, search/hashtag seeding,
  positive and negative preference feedback, Loci content planning, short
  meme-aware comments with optional standing autonomous-comment authorization,
  video upload and scheduling, comment follow-up, post verification, and a
  main-thread-plus-subordinate-driver operating system. Use when the user asks to
  browse or scroll TikTok videos, train or calibrate recommendations, search
  communities or keywords, like/favorite/comment, operate, grow, audit, publish,
  schedule, or maintain a TikTok account from the web, or asks to package or
  explain this workflow.
---

# TikTok Web Operations

Use TikTok's web surfaces as an evidence-led operating system. Keep planning, publishing, engagement, and analytics separate; do not turn activity volume into the objective.

## System Topology

For long-running operation, use exactly one user-owned main Thread and one subordinate agent spawned by that main Thread. Each active agent declares one role:

| Role | Owns | Must not do |
|-|-|-|
| `main_coordinator` | User conversation, goal, audience direction, authorization envelope, child supervision, strategy, risk, and final reporting | Navigate or operate TikTok while its child driver exists |
| `chrome_driver` | The logged-in Chrome session, ordered browsing, searches, authorized actions, verification, and raw evidence logging | Broaden scope, infer approval, alter strategy, spawn agents, or contact unrelated Codex Threads |

The main Thread must spawn exactly one `chrome_driver` through the collaboration/subagent tools and reuse that child for sequential calibration blocks. Do not create a second user-owned Codex Thread for the driver. Do not use `send_message_to_thread` to report to a Skill-development Thread or any external coordinator. Use a single-agent fallback only when the user explicitly declines the two-agent system.

## Route The Request

| Request | Read |
|-|-|
| Inspect, explain, install, or troubleshoot | `references/runtime-and-recovery.md` |
| Install from GitHub, run dependency checks, or bootstrap a fresh operating Thread | `references/startup-health-check.md`, `references/runtime-and-recovery.md`, and `references/operating-model.md` |
| Package, publish, upgrade, or distribute this Skill | `references/distribution-and-upgrades.md` |
| Broad request such as `帮我运营 TikTok` | all references except load only the relevant sections |
| Research trends or choose content | `references/loci-content-system.md` and `references/platform-boundaries.md` |
| Browse/scroll videos or leave short comments | `references/feed-browsing-and-comments.md`, `references/engagement-and-analytics.md`, and `references/platform-boundaries.md` |
| Persistently browse, calibrate recommendations, use search seeds, or coordinate the main/child system | `references/operating-model.md`, `references/persistent-feed-operations.md`, `references/engagement-and-analytics.md`, and `references/runtime-and-recovery.md` |
| Upload, publish, or schedule | `references/publishing-and-scheduling.md` and `references/platform-boundaries.md` |
| Check comments, reply, or maintain community | `references/engagement-and-analytics.md` and `references/platform-boundaries.md` |
| Review performance or decide the next post | `references/engagement-and-analytics.md` and `references/loci-content-system.md` |
| Coordinate lanes or multi-round work | `references/operating-model.md` and `references/runtime-and-recovery.md` |

## Entrypoint Contract

| User says | Execute |
|-|-|
| `帮我运营 TikTok`, `开始运营`, or similarly broad wording | Run a read-only account/capability audit, build the smallest useful batch, and reach a verified plan or blocker. Do not mutate TikTok until the exact outward batch is confirmed at action time. |
| `找热点`, `做选题`, `研究竞品` | Research only. Return content opportunities with live evidence; do not like, follow, comment, or publish. |
| `刷视频`, `看看推荐`, `找能评论的视频` | Browse a bounded feed sample and return or prepare relevant candidates. Do not infer permission to comment, like, favorite, or follow. |
| `持续刷`, `定向刷`, `垂直刷`, `养推荐流`, `搜索关键词引导`, `两个 agent 一起运营` | Make the current user-owned Thread the `main_coordinator`; have it spawn exactly one subordinate `chrome_driver`. Run bounded vertical calibration blocks and reuse the same child through follow-up tasks. Never route callbacks to an external Skill-development Thread. |
| `刷视频并评论`, `去发几个评论` | Browse for context-fit candidates, draft short meme-aware comments, confirm the exact post/comment batch, submit one at a time, and verify each after reload. |
| `评论不用问我`, `直接评论`, `自动发短评论` | Activate `autonomous_comment_mode` only for the explicitly authorized account, audience envelope, language, and voice. Publish eligible proactive comments without per-comment confirmation; enforce the 30-word hard limit and all comment-lane verification/stop rules. |
| `发视频`, `上传`, `排期` | Validate the asset and post settings, present the exact batch for confirmation, then upload or schedule one item at a time and verify it. |
| `看评论`, `回复评论` | Read own-post comments first. Draft a bounded reply batch, confirm it, send one by one, and verify. |
| `看数据`, `复盘` | Use TikTok Studio/account analytics; make no outward changes. |
| `现在状态`, `有什么风险`, `下一步是什么` | Answer from the coordinator ledger and current TikTok state; do not invent missing metrics. |

## Two-Phase Bootstrap

When invoked by the public installer Prompt, complete these phases in order:

1. **Install and preflight:** install or upgrade the complete versioned Skill from the canonical GitHub archive, validate it, prove Chrome control is callable, verify an existing TikTok login and exact account, prove collaboration tools can create and reuse one subordinate agent, read local time/timezone, initialize a ledger, and inspect warnings plus the live capability matrix. Keep TikTok read-only throughout this phase.
2. **Operate:** only when every hard dependency is ready, make the current user-owned Thread the `main_coordinator`, spawn exactly one subordinate `chrome_driver`, transfer Chrome ownership to it, and immediately dispatch the first bounded vertical-calibration block. Do not send results to the Skill-development Thread or create another user-owned operating Thread.

Use `references/startup-health-check.md` as the machine contract. A failed hard dependency stops phase 2 and returns one concrete repair action. Optional model selection never blocks startup and must not be reported as active unless the runtime proves it.

## Chrome Driver Loop

1. Read the parent main coordinator's operating envelope: account, objective, language/region, allowed topics, exclusions, authorizations, stop conditions, ledger path, and parent agent path.
2. Connect to Chrome automatically. Confirm TikTok login, exact account, local time/timezone, and the web features actually visible for that account.
3. Read account health, recent posts, recent comments, analytics, and any visible warnings before proposing activity.
4. Build or refresh the history ledger described in `references/engagement-and-analytics.md`.
5. For recommendation calibration, run the vertical calibration block in `references/persistent-feed-operations.md`; label core, adjacent, irrelevant, and harmful-to-direction content. Do not assume passive views or searches have a known ranking weight.
6. Choose the smallest driver work slot: feed calibration, live trend/context evidence, candidate collection, one confirmed publish/schedule execution, comment follow-up execution, or Studio evidence capture. Leave strategy and content decisions to the coordinator.
7. Run Check A before drafting and Check B on the final exact action. Never reuse a caption, comment, asset, or hook mechanically.
8. Immediately before any upload, video post, schedule, reply, post-like, comment-like, favorite, `Not interested`, follow, profile edit, privacy change, or deletion, request confirmation for the exact bounded batch. For proactive comments only, an active `autonomous_comment_mode` envelope may replace per-comment confirmation when every envelope rule matches.
9. Execute one state-changing action at a time through the sole Chrome driver. Gate and verify each action type independently before continuing.
10. Update the driver-owned ledger and capability evidence, then continue read-only work or send an event callback. Do not redefine the objective. A later state-changing continuation requires confirmation when it reaches the action.

## Control Rules

- Use the user's existing Chrome profile and TikTok login. Never enter or store credentials.
- If no TikTok session is logged in, keep the TikTok tab as a handoff and ask the user to log in. Do not substitute another browser or account.
- Treat Chrome as a single-driver resource, not merely a single-writer resource. Only one task may navigate, scroll, search, or mutate TikTok in that Chrome profile at a time. Other tasks may analyze the ledger, plan queries, classify candidates, or draft comments without touching Chrome.
- In the two-agent system, the main coordinator never touches Chrome and the child driver never spawns another agent. Keep exactly two active agents unless the user explicitly changes the architecture.
- Keep all operational communication inside the main Thread's collaboration tree. Do not call Codex App thread messaging tools from the child and do not report to a separate Skill-development Thread.
- Prefer TikTok's native next/previous controls, wheel/trackpad-style incremental scrolling, and normal search result navigation when they preserve the real feed context. Use them for behavioral fidelity and observable playback state, never to imitate a human or evade automation detection. Do not add random delays, cursor jitter, or stealth patterns.
- Prefer TikTok Studio for account analytics, post management, comment management, uploads, and scheduling when those features are visible.
- Web capability varies by account, region, and eligibility. Verify the live UI instead of assuming a documented feature is enabled.
- A broad operating request authorizes read-only preparation, not an unspecified stream of posts or comments. Require action-time confirmation for the exact outward batch unless the user explicitly activates the narrowly scoped `autonomous_comment_mode` described in `references/feed-browsing-and-comments.md` and `references/operating-model.md`.
- Keep post likes, favorites, proactive comments, comment likes, `Not interested`, follows, replies, and publishing as separate capability lanes. Success or failure in one lane proves nothing about another.
- Do not set comment, follow, like, or post quotas. Quality, audience fit, rights, account health, persisted state, and either an exact confirmed batch or a matching standing comment envelope gate every action.
- Never automate account creation, operate accounts in bulk, distribute high-volume commercial content, manipulate engagement signals, evade enforcement, or imitate human timing to avoid detection.
- Favor original, account-native content. Record asset provenance, music rights, commercial disclosure, and AI disclosure before publishing.
- If the content promotes Loci or another business, verify the required TikTok content disclosure setting before publishing.
- Label realistic AI-generated or significantly edited people/scenes when TikTok requires it. Do not generate deceptive personas, testimonials, product use, or results.
- Use Chinese for user reports by default; retain necessary identifiers, URLs, creator names, hashtags, and exact TikTok UI text.

## Checks

### Check A — before drafting

- Correct account and clean-enough account state.
- Clear audience, content pillar, and intended viewer action.
- Live trend/context evidence rather than a copied trend label.
- Recent-history comparison for hook, footage, sound, caption, hashtag set, and format.
- Rights and disclosure path for footage, faces, music, brands, location, and AIGC.
- Web feature and asset-format eligibility.

### Check B — before acting

- Exact account, asset, cover, caption, hashtags, mentions, links, audience, privacy, comments, Duet/Stitch, disclosure, and schedule time.
- Copyright check result when available.
- No accidental private information, fake claim, duplicate post, copied comment, or unsupported metric.
- Explicit action-time confirmation covers this exact item, or an active standing comment envelope covers this proactive comment and every envelope field matches.

After acting, verify the post/comment/schedule in TikTok or TikTok Studio. If submission state is uncertain, inspect before retrying; never duplicate an uncertain send.

## Stop Conditions

Stop state-changing work for login mismatch, CAPTCHA, verification challenge, rate limit, account warning/restriction, copyright failure, missing rights, missing required disclosure, or an uncertain submission. Ask the user to handle CAPTCHA or authentication challenges.

Skip a candidate for weak fit, stale trend evidence, repetitive creative, inadequate source material, unsafe comments, or missing analytics. A skipped candidate is not a reason to fill the slot with lower-quality activity.

## Reporting Contract

The Chrome driver keeps ordinary read-only events in the ledger. At the end of each bounded calibration block, return one structured result to its parent main coordinator through the collaboration channel and become idle. The parent may dispatch the next block with `followup_task`. For a mid-block blocker, key risk, or decision, message the parent agent path. Never call `send_message_to_thread` from the child.

The main coordinator reports to the user with four short fields when a decision, status answer, or meaningful checkpoint is due:

```text
本轮完成：做了什么；实际完成多少项。
发布/处理：TikTok 位置 + 动作 + 链接；未发布时写原因。
下一轮：本地日期、时间、时区，以及准备做什么；结束时写“已结束，不再调度”。
风险：无；或当前具体风险与影响。
```

Keep candidate scoring, loaded references, browser recovery, Check A/B details, scheduler conversion, and internal ledger fields out of the default report unless they caused a decision or risk. See `references/operating-model.md` for parent/child dispatch, authorization, result, and ownership protocols.
