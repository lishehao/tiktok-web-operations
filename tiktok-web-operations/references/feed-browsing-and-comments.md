# Feed Browsing And Short Comments

## Browsing loop

Treat `刷视频` as read-only browsing unless the user separately authorizes an outward action.

1. Confirm the logged-in account and the intended feed, search, hashtag, creator, sound, or topic.
2. Choose the surface deliberately: use native feed scrolling to measure current recommendations; use search/hashtag/creator navigation to seed a missing direction. Do not substitute a list of direct video URLs for all scrolling because that loses feed-order and playback evidence.
3. Inspect one post at a time: creator, caption/on-screen premise, language, sound, visible context, comment culture, engagement signals, and account relevance.
4. Watch enough to understand the setup and payoff. Use native next/previous or incremental scrolling after the relevant evidence is captured. Skip without forcing a comment when the context is unclear, stale, unsafe, or irrelevant.
5. Label the post `core`, `adjacent`, `irrelevant`, or `harmful_to_direction`; keep the post URL and a one-line reason. Stop when the sample is sufficient for the objective or the user-supplied time limit ends.
6. Rotate back to a small search-seeded cluster when the feed drifts, then re-sample For You to see whether the composition changes. Treat any change as observed correlation, not proof of TikTok's ranking mechanism.
7. Do not like, favorite, use `Not interested`, follow, share, like a comment, or publish a comment merely because the video was viewed. Each action type keeps its own confirmation and persistence gate.

Do not manufacture human-like pauses or scrolling patterns to evade detection. Respect CAPTCHA, rate limits, warnings, and feature restrictions as hard stops.

Use `Not interested` sparingly and only for content that is clearly harmful to the approved direction. Do not use it on merely adjacent content: an overly aggressive negative signal can narrow discovery before the target audience model is understood.

## Short-comment voice

Prefer a fragment or one short sentence. Aim for roughly 2-12 words in English or 4-24 Chinese characters when the joke still lands.

**Hard red line:** never submit a proactive comment longer than 30 words. For English, count whitespace-separated tokens after trimming; a contraction, hashtag, mention, number, or emoji group counts as one token. If the count is above 30, rewrite below the limit or skip. Do not treat 30 as a target: shorter is better.

Use the video's language and comment culture. Favor:

- Deadpan understatement or fake seriousness.
- Self-roast, friend-group chaos, awkward dating, relatable failure, or mild non-graphic adult innuendo when everyone involved is clearly an adult.
- Current slang or meme structure supported by the live post/comment context.
- One sharp observation instead of an explanation, CTA, product mention, or generic praise.

Aim for a comment that a real college/dorm-life viewer might genuinely like or reply to because it notices the video's specific payoff. Treat later likes and replies as evidence about voice quality, not as a promised TikTok account-weight mechanism. Do not ask for likes, bait replies, manufacture controversy, or imitate a top comment.

The user may request `恶俗`, `损`, or `抽象`. Interpret that as lowbrow, chaotic, slightly rude humor—not unrestricted abuse. Allow shitposting, embarrassment, absurd exaggeration, and consensual-feeling friend-roast energy. Do not produce:

- Targeted harassment, threats, dogpiling, humiliation, dehumanization, or body shaming.
- Slurs or attacks based on protected traits.
- Sexualization of minors, graphic sexual content, or sexual comments directed at an identifiable person.
- Encouragement of self-harm, dangerous acts, illegal conduct, or evasion of TikTok enforcement.
- Copy-pasted comments, irrelevant promotion, engagement bait, or repeated wording across posts.

If the joke depends on insulting a real person rather than the situation, rewrite it as self-roast or observational humor. If no context-fit safe joke survives, skip the post.

## Comment authorization modes

Use one mode:

- `per_item_confirmation` — default. Present the exact URL and text before every proactive comment.
- `autonomous_comment_mode` — use only after the user explicitly grants standing authorization for the exact account and operating envelope. Do not ask about each eligible comment.

The standing envelope must record:

- Account and language.
- Allowed audience/topic clusters and exclusions.
- Voice: short, meme-aware, context-specific, non-promotional.
- Hard maximum: 30 words; prefer 2-12.
- Eligible action: one proactive top-level comment on a qualifying post.
- Excluded actions: replies, comment likes, post likes, favorites, follows, shares, `Not interested`, video posts, profile edits, and DMs unless separately authorized.
- Start time, revocation state, capability state, and hard stops.

In autonomous mode, comment only when the post is `core` to the active audience direction, the setup/payoff is understood, the visible comment culture supports playful participation, and a strong original joke survives the safety checks. Skip rather than ask when the fit is merely adjacent, emotionally sensitive, politically charged, directed at a vulnerable person, unclear, stale, repetitive, or dependent on insulting a real person.

Record the URL and exact final text in the ledger before submitting. Never reuse wording mechanically across posts. Do not optimize for comment volume or stack multiple account actions on the same post.

## Draft and send

For each candidate, prepare up to three materially different short options only when choice would help. Prefer the strongest single option when it is obvious. Never copy another comment verbatim.

In `per_item_confirmation`, present the exact creator/post URL and exact final text and confirm the bounded batch at action time. In `autonomous_comment_mode`, verify that every standing-envelope field matches; do not request per-comment confirmation. Then:

1. Submit one comment once.
2. Verify the immediate posted state and author identity.
3. Reload or reopen the post and locate the exact comment again.
4. Record success, failure, removal, warning, or uncertainty before moving on.

A successful comment does not prove that likes, favorites, follows, or later comments will persist. Verify every send after reload even in autonomous mode. Stop the comment lane on CAPTCHA, warning, throttling, removal, an uncertain submission, account mismatch, or a failed persistence check. Do not retry and do not substitute another candidate to fill the slot.
