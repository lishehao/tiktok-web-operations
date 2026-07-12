# Engagement And Analytics

## Dual-objective scorecard

Track two separate operational outcomes:

- `profile_alignment`: qualified strong-core views, cluster coverage, viewing
  progression/premise-payoff evidence, creator/hashtag bridges, and rolling For
  You `core_share`/`directional_share`/`drift_share`.
- `account_strength_proxy`: persisted Favorite, TikTok Repost, and proactive
  comments; later organic likes/substantive replies on those comments; profile
  visits/follows or own-post metrics only when those surfaces exist.

Never collapse these into a claimed TikTok account weight. Report the proxy's
components and evidence. Search/view can improve the profile-alignment
hypothesis, but does not substitute indefinitely for active participation in a
cultivation/growth mission. Conversely, mutations do not compensate for shallow
or off-direction viewing.

## Engagement order

1. Read account warnings and creator/account notifications.
2. Read comments on the account's own recent posts.
3. Use comment insights when available to find recurring topics, questions, suggestions, and confusion.
4. Draft replies only where the account can add a concrete answer, clarification, acknowledgment, or useful follow-up.
5. Treat proactive comments on other creators' posts as a separate authorized
   lane. A cultivation/growth/account-strength mission supplies a standing
   `pending_fresh_gate` envelope with `parallel_engagement=true` unless narrowed to read-only; other requests
   need explicit authorization. Once active, use
   `feed-browsing-and-comments.md`; do not turn it into an activity quota.

Do not set a reply quota. Do not copy-paste replies, use repetitive CTAs, insert irrelevant promotion, or reply merely to inflate activity.

Before enabling any active engagement lane for a browser/account combination, run one bounded persistence test per action type. Treat at least these as distinct types: post like, favorite/save, post repost, generic share, proactive comment, own-post reply, comment like, `Not interested`, follow, publish, and profile edit. Require:

1. Immediate UI state change.
2. The same state after reload or reopening the post.
3. Account-level evidence when TikTok exposes it.

If any required signal fails, suspend only that action type for the current
session and record a normal no-action capability checkpoint. Do not infer that a
sibling type failed, stop the mission, or ask the user. In a later mission/
runtime, a latest explicit instruction for that action may authorize one fresh
gate without another confirmation; the old result remains historical evidence
rather than a permanent blocker. Keep search/view, research, comment reading,
drafting, Studio management, analytics, and independent verified lanes available.

Comment drafting is not comment publication. Use either exact per-item confirmation or a currently active standing autonomous-comment envelope. Submit once, then reload the post and locate the account's comment before recording success.

Gate active engagement per action type, not per account. A verified comment does not re-enable likes, favorites, reposts, follows, or any action whose own persistence test failed or remains inconclusive.

## Directional feedback ladder

Treat feed signals as hypotheses rather than known algorithm weights:

| Signal | Operational use | Gate |
|-|-|-|
| Short view / early skip | Passive observation of weak fit | Read-only, but do not claim a known recommendation effect |
| Completed view / replay / creator or hashtag exploration | Stronger evidence of genuine relevance | Read-only when no outward control is changed |
| Search, open, and meaningfully watch strong-core results | Primary directional training hypothesis; card inspection alone does not count | Read-only |
| `Not interested` | Explicit negative feedback for clearly off-direction content | Exact post confirmation plus persistence check |
| Post like | Lightweight positive feedback | Independent post-like persistence gate |
| Favorite/save | Strong intent hypothesis; useful only if the account can prove persistence | Independent favorite persistence gate: selected immediately, still selected near +3s and +10s, then reload/reopen plus exact account-level Favorites evidence |
| Post repost | Public redistribution hypothesis; use only when the post genuinely fits the account voice | Independent Repost persistence gate with `Repost`/`Undo repost` state; the Share sheet may be opened read-only to reach Repost, but no generic Share/copy/send target may be executed |
| Comment like | Community-context feedback | Independent comment-like persistence gate |
| Proactive comment or reply | Social participation and voice shaping | Exact text/post confirmation plus reload visibility |

For proactive comments, the gate may instead be an active `autonomous_comment_mode` envelope. This exception does not apply to replies, comment likes, follows, favorites, reposts, post likes, `Not interested`, publishing, profile edits, or DMs.

Before enabling autonomous comments in a browser/runtime, require at least one
proactive-comment persistence test that survives reload. After activation,
verify every comment. Routine successes stay in the ledger. Persistence failure
or removal suspends only autonomous comments; timed throttle auto-waits;
submission uncertainty freezes only that exact comment. Report these in the next
normal mission checkpoint. Ask the user directly in the executor only for the
hard-blocker whitelist in `blocker-minimization.md`.

Never use all positive actions on every relevant post. Choose the smallest signal justified by the content and the current capability matrix; otherwise the operation becomes repetitive engagement manipulation rather than audience calibration.

In a cultivation/growth mission, candidate evaluation is mandatory even though
action counts are not quotas. Evaluate Like, Favorite, Repost, and proactive
comment immediately while each qualified post is open. If a qualified,
non-repetitive candidate exists and its lane is verified, use the fitting action
rather than defaulting the whole unit to read-only. When no action is taken,
record the exact no-candidate, current-gate, repetition, safety, or rights reason.

For proactive comments, record later organic likes and substantive replies when visible at normal review checkpoints. Use them to compare joke specificity, audience language, and community fit. Do not treat raw comment-like count as proof of recommendation weight, and do not rewrite comments into engagement bait merely to chase reactions.

## Comment reply packet

Record the post URL, comment text/author, relationship to the account, reason to reply, factual basis, draft, tone, disclosure risk, and whether the reply makes a product claim. Confirm the exact bounded packet before sending.

## History ledger

Track at minimum:

- Post URL/ID, publish/schedule time, language, region, pillar, format, hook, footage, sound, cover, caption, hashtags, disclosure, and rights source.
- Comment/reply URL or parent context, draft, sent time, and result.
- Views, average watch time, completion/retention when available, likes, comments, shares, saves/favorites, profile visits, follows, traffic source, audience activity, and moderation state.
- Measurement timestamp and source surface. Do not compare metrics captured at different ages without labeling the difference.

## Review windows

Use 24 hours, 72 hours, and 7 days as operational observation windows, not official TikTok thresholds. For a new or sparse account, establish a baseline before declaring a winner.

Compare content on:

- First-second and early retention when available.
- Average watch time and completion.
- Shares, saves/favorites, and substantive comments.
- Profile visits and follows relative to views.
- Comment themes, questions, confusion, and repeated audience language.

Do not optimize only for views. A smaller post that produces strong saves, shares, profile visits, or clear audience language can be more useful for Loci.
