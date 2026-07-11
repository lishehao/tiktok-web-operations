# Persistent Feed Operations

Use this reference for long-running feed calibration, keyword/community seeding, or user-requested multi-task operation.

Assume the persistent `execution_thread` role defined in `operating-model.md`. This file defines browsing and recommendation-calibration behavior only; it does not grant authority or change the two-Thread ownership model.

Before the first full block of a new executor/runtime, pass the read-only `stability_smoke_01` in `stability-and-circuit-breakers.md`. Do not combine the smoke with mutation gates.

## Calibration state machine

1. **Audit** — Verify account identity, warnings, current feature visibility, driver ownership, and per-action capability state.
2. **Baseline** — Enter native For You once, then sample one continuous feed in order. Record core/adjacent/irrelevant/harmful labels without outward actions or page resets.
3. **Seed** — Search one approved topic cluster. Open results from the search surface and watch enough to classify the setup and payoff.
4. **Bridge** — Explore a relevant hashtag, creator, sound, or related-search path when it adds audience context rather than pure virality.
5. **Re-sample** — After all search/bridge work is finished, enter For You once and measure one continuous native sequence. Report composition, not causal certainty.
6. **Prepare feedback** — Build an exact packet for actions requiring confirmation, or select an eligible post like, favorite, repost, or proactive comment when a matching standing envelope is active.
7. **Authorize and execute** — Use exact action-time confirmation or the matching standing envelope, run one action once, and apply its independent persistence gate.
8. **Reconcile** — Update the ledger, capability matrix, search seeds, exclusions, and next read-only calibration phase.

Loop through Baseline → Seed → Bridge → Re-sample. Do not stay indefinitely in For You when the feed is off-direction, and do not stay indefinitely in search because that prevents measuring the actual recommendation mix.

## Default vertical calibration block

Use one block as the repeatable unit for a new, sparse, or visibly off-direction account:

1. Lock the audience ontology before browsing: current core clusters, adjacent boundary, exclusions, language/region, and active capability matrix.
2. Select three distinct approved search clusters. Do not use three near-duplicate queries from the same microtopic.
3. For each cluster, inspect five results in order. Count product/storefront, stale, adjacent, and irrelevant results in the denominator instead of silently cherry-picking only good posts.
4. For each result, record source query, URL, freshness, creator, relevance label, whether the setup/payoff was understood, and whether the comment culture supports participation.
5. When `autonomous_comment_mode` is active, comment only on a strong `core` result. Expect roughly zero or one qualifying comment per five results, but never treat that as a quota; zero is valid.
6. After 15 search-result observations, enter For You once and sample 20 sequential items on that same page through the visible native next/down control. Do not open only attractive cards, replace bad results, reload, reopen Home, call `goto` on the home route, or navigate away between positions. If no unambiguous down/next control exists, stop; a coordinator may later declare a separate scroll-only fallback checkpoint, but methods must not be mixed.
7. Record the exact before/after creator, URL, or stable card identity plus the transition action for every advance. If the feed does not advance, repeats unexpectedly, loses identity, or would require a reset, record `transition_failure`/`duplicate` and stop the checkpoint. Never reset to manufacture a sample.
8. Append ledger checkpoints after each five-result search cluster and after For You positions 1, 5, 10, 15, and 20. A shorter or failed checkpoint is appended at its final observed position.
9. Compute the block composition and choose the next mode with the heuristic below.

Five items are an exploration unit for one search cluster, not enough to judge the recommendation feed. Twenty sequential For You items are the minimum default checkpoint; retain larger rolling samples when available.

## Verticality metrics and mode switch

For each For You checkpoint record:

```text
core_share = core / sampled
directional_share = (core + adjacent) / sampled
drift_share = (irrelevant + harmful_to_direction) / sampled
```

Use these operating heuristics, not as claims about TikTok's official algorithm:

| Observed For You composition | Next block |
|-|-|
| `core_share < 20%` | `search_heavy`: three search clusters × five results, then 20-item For You checkpoint |
| `core_share 20–50%` | `mixed`: two search clusters × five results, then 20-item For You checkpoint |
| `core_share > 50%` in two consecutive checkpoints | `feed_led`: primarily browse For You; retain one five-result search cluster per block to prevent drift and discover fresh language |

Do not switch to feed-led mode from one favorable checkpoint. If `core_share` stays below 10% for three complete blocks, change query wording or cluster mix and recheck account/region context; do not compensate by posting more comments.

## Packaged default college/dorm block

Rotate among these families so the account stays vertically coherent without collapsing into one narrow microtopic:

- `roommate move in`, `college roommate storytime`, roommate chaos.
- `dorm move in`, `freshman move in day`, `dorm room setup`.
- `college day in my life`, campus routine, `grwm for class`.
- `college friend group`, `college game day`, campus social life.
- `finals week vlog`, dorm survival, campus-life failures.

Prefer recent posts from roughly the last 30 days when suitable current results exist. Older evergreen posts may be research evidence, but avoid relying on old viral inventory to represent the current audience language.

## Native browsing versus imitation

Prefer the visible native next/down control when it preserves playback, ordered feed context, and visible watch state. Before position 1, record how the control was identified through accessible name, role, stable UI placement, or another unambiguous locator. Click it exactly once per transition and verify the before/after identity packet before continuing.

Incremental scroll/wheel gestures are not an automatic fallback. Under the packaged default, failure of the visible native next/down control stops feed sampling and callbacks once. A scroll-only checkpoint requires a new explicit user decision after the stopped block. Never mix button, keyboard, wheel, script scroll, reload, or reset transitions in one checkpoint or recovery sequence. Direct URLs remain appropriate for exact verification and revisiting candidates, but they are not a replacement for feed sampling.

For You sampling is one continuous-session invariant. Initial entry before position 1 may use the normal TikTok navigation link. After position 1, remain on the same page and preserve feed order. Do not use reload, `goto`, Home reopening, direct-post navigation, or a second For You entry as an ordinary transition. A reset is permitted only after the current block is explicitly stopped and reported as a separate hard recovery; recovered items belong to a new checkpoint, never the old denominator.

For every transition store `position_before`, `identity_before`, `action`, `position_after`, `identity_after`, and `advanced=true|false`. A repeated identity stays in the raw denominator and is labeled `duplicate`; a control that does not advance or destroys stable identity is `transition_failure`. Stop rather than disguising either condition.

The purpose is interface fidelity, not stealth. Never randomize timing, move the pointer artificially, insert fake indecision, or claim to be human. Respect CAPTCHA, verification, warnings, and rate limits. Detect platform warnings only from explicit system UI; never treat ordinary caption, hashtag, comment, or search-result words as system warnings.

Watch long enough to understand the content. Do not encode a universal dwell-time formula: video length, clarity, replay need, and the research objective vary. Record whether the premise/payoff was understood, not a fabricated human-behavior score.

## Search-seed policy

Organize queries into clusters with a reason and an exclusion boundary. Build the live clusters from the resolved `direction_profile`. For the packaged North American college/dorm-life default:

| Cluster | Examples | Keep distinct from |
|-|-|-|
| Move-in and setup | `college move in vlog`, `freshman move in day`, `dorm room setup`, `dorm essentials` | Product-only shopping hauls with no campus context |
| Roommate life | `college roommate`, `roommate move in`, `college roommate storytime` | Generic dating or family-roommate content |
| Campus routine | `college day in my life`, `campus life vlog`, `grwm for class`, `college night routine` | Pure productivity or study-motivation content |
| Social moments | `college game day`, `college tailgate`, `college friends vlog`, `first week of college` | Professional sports fandom without student life |
| Survival/chaos | `finals week vlog`, `things I wish I knew before college`, dorm bathroom/cooking/laundry failures | Admissions, SAT, GPA, application advice |

Useful hashtag bridges include `#collegemovein`, `#dormlife`, `#freshmanyear`, `#collegelife`, `#roommate`, `#dormroom`, `#campuslife`, and `#collegegameday`. Recheck live results; a label alone is not evidence of audience fit.

Rotate seed clusters when new results become repetitive or the For You sample remains unchanged. Preserve exclusions so the task does not repeatedly rediscover that pure admissions or study-grind content is off-direction.

## Feedback policy

Keep these feedback lanes separate:

- **Passive consumption:** view, completion, replay, early skip, opening creator/hashtag/sound. Observe directionally; do not claim a known ranking weight.
- **Explicit negative:** `Not interested` only for clearly harmful-to-direction content. Require exact-post confirmation and a one-action capability test before using it as a lane.
- **Explicit positive:** post like, favorite, or TikTok Repost only on strong-core content under exact or standing authorization. Use one separately authorized test per lane and enable continued use only after independent persistence proof. Favorite/save requires immediate, about +3-second, and +10-second stable-selected checks before reload/reopen and account-level proof; do not create a false failure by reloading immediately after the click. Repost is not generic Share, copy-link, or send-to-recipient. Opening the Share sheet is allowed read-only when needed to reveal an explicit Repost control; every other target in the sheet remains excluded.
- **Community feedback:** comment like is its own capability type. Use it only for a comment that genuinely represents the desired community voice; do not mass-like comment sections.
- **Social participation:** proactive comments require either exact confirmation or a matching active autonomous-comment envelope; replies still require exact confirmation. Submit once and require post-reload visibility.

Do not stack like + favorite + repost + comment on every good post. Use distinct posts for first capability gates, then the smallest justified signal. A natural operating profile includes many read-only decisions, a few strong candidates, and sparse verified mutations.

## Ledger and capability matrix

For each viewed item record timestamp, source surface, ordered position when available, URL, freshness, creator, topic cluster, relevance label, premise/payoff understood, action candidate, and risk. For each block, summarize search denominators plus For You core/directional/drift shares. Persist incrementally after every search cluster and every five For You positions, including the first and final/failed positions, so a runtime failure cannot erase the whole block.

Track each action type as `untested`, `verified`, `failed`, `unverified`, or `disabled`, with account, browser/runtime, test URL, timestamp, immediate state, reload state, account-level state, and stop reason. `not_executed` is a batch result, not a capability result.

Never report success from a click, count animation, pressed control, toast, or network response alone. Require the action-specific persisted evidence defined in `engagement-and-analytics.md`.

## Stop and handoff

Stop mutation immediately for login mismatch, lost driver ownership, CAPTCHA, verification challenge, rate limit, warning/restriction, uncertain submission, or persistence failure. Keep read-only analysis available if the page and account remain safe to inspect.

At handoff report: account, driver owner, current surface/URL, sample composition, active seed cluster, candidate packet, capability matrix deltas, mutation count, ledger path, and exact next safe action.
