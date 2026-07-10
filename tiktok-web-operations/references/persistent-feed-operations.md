# Persistent Feed Operations

Use this reference for long-running feed calibration, keyword/community seeding, or user-requested multi-task operation.

Assume the persistent `execution_thread` role defined in `operating-model.md`. This file defines browsing and recommendation-calibration behavior only; it does not grant authority or change the two-Thread ownership model.

## Calibration state machine

1. **Audit** — Verify account identity, warnings, current feature visibility, driver ownership, and per-action capability state.
2. **Baseline** — Sample the native For You feed in order. Record core/adjacent/irrelevant/harmful labels without outward actions.
3. **Seed** — Search one approved topic cluster. Open results from the search surface and watch enough to classify the setup and payoff.
4. **Bridge** — Explore a relevant hashtag, creator, sound, or related-search path when it adds audience context rather than pure virality.
5. **Re-sample** — Return to For You and measure whether the visible mix moved toward the target. Report composition, not causal certainty.
6. **Prepare feedback** — Build an exact packet for actions requiring confirmation, or select an eligible proactive comment when a matching autonomous-comment envelope is active.
7. **Authorize and execute** — Use exact action-time confirmation or the matching standing comment envelope, run one action once, and apply its independent persistence gate.
8. **Reconcile** — Update the ledger, capability matrix, search seeds, exclusions, and next read-only calibration phase.

Loop through Baseline → Seed → Bridge → Re-sample. Do not stay indefinitely in For You when the feed is off-direction, and do not stay indefinitely in search because that prevents measuring the actual recommendation mix.

## Default vertical calibration block

Use one block as the repeatable unit for a new, sparse, or visibly off-direction account:

1. Lock the audience ontology before browsing: current core clusters, adjacent boundary, exclusions, language/region, and active capability matrix.
2. Select three distinct approved search clusters. Do not use three near-duplicate queries from the same microtopic.
3. For each cluster, inspect five results in order. Count product/storefront, stale, adjacent, and irrelevant results in the denominator instead of silently cherry-picking only good posts.
4. For each result, record source query, URL, freshness, creator, relevance label, whether the setup/payoff was understood, and whether the comment culture supports participation.
5. When `autonomous_comment_mode` is active, comment only on a strong `core` result. Expect roughly zero or one qualifying comment per five results, but never treat that as a quota; zero is valid.
6. After 15 search-result observations, return to For You and sample 20 sequential items through native scrolling. Do not open only attractive cards or replace bad results.
7. Compute the block composition and choose the next mode with the heuristic below.

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

## Current college/dorm block

Rotate among these families so the account stays vertically coherent without collapsing into one narrow microtopic:

- `roommate move in`, `college roommate storytime`, roommate chaos.
- `dorm move in`, `freshman move in day`, `dorm room setup`.
- `college day in my life`, campus routine, `grwm for class`.
- `college friend group`, `college game day`, campus social life.
- `finals week vlog`, dorm survival, campus-life failures.

Prefer recent posts from roughly the last 30 days when suitable current results exist. Older evergreen posts may be research evidence, but avoid relying on old viral inventory to represent the current audience language.

## Native browsing versus imitation

Prefer native next/previous controls or incremental scroll/wheel gestures when they preserve playback, ordered feed context, and visible watch state. Direct URLs are appropriate for exact verification and revisiting candidates, but they are not a complete replacement for feed sampling.

The purpose is interface fidelity, not stealth. Never randomize timing, move the pointer artificially, insert fake indecision, or claim to be human. Respect CAPTCHA, verification, warnings, and rate limits.

Watch long enough to understand the content. Do not encode a universal dwell-time formula: video length, clarity, replay need, and the research objective vary. Record whether the premise/payoff was understood, not a fabricated human-behavior score.

## Search-seed policy

Organize queries into clusters with a reason and an exclusion boundary. For the current North American college/dorm-life direction:

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
- **Explicit positive:** post like or favorite only when context-fit, confirmed, and independently proven persistent for this account/runtime.
- **Community feedback:** comment like is its own capability type. Use it only for a comment that genuinely represents the desired community voice; do not mass-like comment sections.
- **Social participation:** proactive comments require either exact confirmation or a matching active autonomous-comment envelope; replies still require exact confirmation. Submit once and require post-reload visibility.

Do not stack like + favorite + comment on every good post. Use the smallest justified signal. A natural operating profile includes many read-only decisions, a few prepared candidates, and sparse confirmed mutations.

## Ledger and capability matrix

For each viewed item record timestamp, source surface, ordered position when available, URL, freshness, creator, topic cluster, relevance label, premise/payoff understood, action candidate, and risk. For each block, summarize search denominators plus For You core/directional/drift shares.

Track each action type as `untested`, `verified`, `failed`, `unverified`, or `disabled`, with account, browser/runtime, test URL, timestamp, immediate state, reload state, account-level state, and stop reason. `not_executed` is a batch result, not a capability result.

Never report success from a click, count animation, pressed control, toast, or network response alone. Require the action-specific persisted evidence defined in `engagement-and-analytics.md`.

## Stop and handoff

Stop mutation immediately for login mismatch, lost driver ownership, CAPTCHA, verification challenge, rate limit, warning/restriction, uncertain submission, or persistence failure. Keep read-only analysis available if the page and account remain safe to inspect.

At handoff report: account, driver owner, current surface/URL, sample composition, active seed cluster, candidate packet, capability matrix deltas, mutation count, ledger path, and exact next safe action.
