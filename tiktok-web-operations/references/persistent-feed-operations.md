# Persistent Feed Operations

Use this reference for long-running feed calibration, keyword/community seeding, or user-requested multi-task operation.

Assume the persistent `execution_thread` role defined in `operating-model.md`. This file defines browsing and recommendation-calibration behavior only; it does not grant authority or change the two-Thread ownership model.

Before the first continuous mission segment of a new executor/runtime, pass the
read-only `stability_smoke_01` in `stability-and-circuit-breakers.md`. Do not
combine the smoke with mutation gates.

## Continuous mission loop

Run until the canonical `operation_stop_at`, explicit user stop, authorized
objective completion, or a current safety boundary. Do not use estimated model,
video, or Chrome-loading time as a control condition. Time estimates are
observability metrics only.

Use evidence counts and content state to advance:

```text
search-training unit
  -> next approved cluster when the current query is exhausted/repetitive/drifting
  -> sparse opportunity-triggered feedback
  -> held-out For You checkpoint after the sample threshold
  -> reconcile cluster weights and continue immediately
```

One search-training unit normally reaches 9–15 qualified search views across
distinct approved clusters, or ends honestly when suitable results are exhausted,
repetitive, or visibly drifting. Trigger a 5–10 item held-out For You checkpoint
after roughly 20–30 new qualified views or two distinct completed training units.
Then continue immediately with the adjusted cluster mix. These are logical
content boundaries, not Codex turns, Heartbeat slots, or fixed-minute promises.

Before starting a new query, opening the next post, submitting any mutation,
starting a held-out checkpoint, and after recovery, compare current time with
`operation_stop_at`. At/after cutoff, start no new action and enter the terminal
release transaction.

If a query or full unit produces zero qualified candidates, record
`no_action_checkpoint` with the assessed denominator and rejection reasons,
rotate to another approved cluster on the next cycle, and continue. Empty
discovery is not `blocked`, `validation_failed`, or a reason to ask the user. A
rule-prohibited candidate, community, route, or action is simply skipped; do not
request permission to bypass the rule.

## Search-training state machine

Treat search-led consumption as the default training surface and For You as a
held-out validation surface. Neither surface proves a known TikTok ranking
weight.

1. **Audit** — Verify account identity, warnings, driver ownership, region/language, and per-action capability state.
2. **Baseline validation** — When the feed-validation lane is available, take one small continuous For You sample to measure the starting mix. Do not train on it.
3. **Search assessment** — Search one approved cluster and classify the first five result cards in order. This measures query quality only.
4. **Qualified consumption** — From those results, open strong `core` posts individually from the search surface, verify the direct post identity/playback, and watch through the premise/payoff or completion when reasonably short. Returning without opening the post is not consumption.
5. **Bridge consumption** — From a consumed core post, optionally open one relevant creator, hashtag, sound, or related-search path and consume another core post when it adds audience context.
6. **Sparse explicit feedback** — For cultivation/growth/account-strength
   missions, post Like, Favorite, TikTok Repost, and proactive comment are four
   standing `pending_fresh_gate` lanes with `parallel_engagement=true` unless the
   user narrows the run to read-only. Run
   each fresh gate on a distinct strong-core post, then choose the smallest
   genuine verified signal. Every unit must evaluate opportunities; zero
   outward actions requires an explicit no-candidate/current-lane/repetition/
   safety reason, not a blanket `mutation_allowed=false` dispatch.
7. **Held-out validation** — After the sample threshold, enter For You once and sample a small continuous sequence. Measure composition; do not claim causal attribution.
8. **Reconcile and continue** — Update qualified-consumption counts, feed-validation state, capability matrix, cluster weights, and exclusions, then immediately start the next approved unit while before the cutoff.

Search cards are candidate discovery, not recommendation training evidence.
Record `search_results_assessed` separately from `qualified_search_views`. A
qualified search view requires all of: opened from a search/bridge surface,
stable post URL/creator identity, playback or visible watch progression, and
premise/payoff understanding. Directly opening an already-known URL does not
replace the search-origin proof.

## Operating round and search-training units

An operating round targets 35 qualified watched videos with an allowed range of
25–45. Normally use 25–35 qualified search-origin views plus 5–10 sequential For
You validation views. If the Feed lane is unavailable, use search-origin views
for the whole round. Thumbnails, duplicates, clear drift, failed loads, and
unverified playback do not count.

After 25 qualified views the executor may end at the next natural boundary when
inventory quality, runtime yield, or cutoff makes that sensible. At 45 it must
checkpoint before more browsing. A round may contain multiple training units;
unit completion never triggers a launcher message, task switch, or wait. After
checkpoint the executor directly starts the next round when safe and before
cutoff; Heartbeat is only recovery/resume.

## Default search-training unit

Use one logical training unit for a new, sparse, or visibly off-direction account.
Spend most operating effort here; do not append a For You checkpoint to every
unit and do not yield merely because one unit completed.

1. Lock the audience ontology before browsing: current core clusters, adjacent boundary, exclusions, language/region, and active capability matrix.
2. Select three distinct approved search clusters. Do not use three near-duplicate queries from the same microtopic.
3. For each cluster, classify the first five result cards in order. Count product/storefront, stale, adjacent, and irrelevant results in the assessment denominator.
4. Open and consume every suitable strong-core result among those five, normally three to five per cluster. Verify the exact post page, observe playback progression, and watch enough to understand the premise/payoff. Record observed/total time when exposed, without inventing a universal dwell rule.
5. Return through normal page navigation to the same search context; do not substitute a direct URL list or merely inspect thumbnails/captions.
6. Record two separate denominators: all assessed result cards and the number of qualified consumed core posts. A complete unit normally contains 9–15 qualified search views; if fewer or zero exist, write an honest completed/no-action unit and rotate weak clusters rather than opening irrelevant posts to fill a quota or escalating.
7. When `autonomous_comment_mode` is active, comment only on a strong core post
   after it has become a qualified view. Zero comments remains valid only when
   no contextually strong, non-repetitive candidate exists or the lane is
   currently unavailable; record the reason.
8. Append and validate one JSONL record after each consumed post and one cluster summary after each five-card assessment. A malformed line suspends further mutation until the executor repairs the ledger; it does not retire the self Heartbeat.
9. Run held-out For You validation only after two distinct training units or roughly 20–30 qualified search views, unless the user directly requests an earlier diagnostic in the executor task.

The default unit success metric is qualified search consumption, not search-card relevance and not For You composition.

## Held-out For You validation checkpoint

Use For You to measure whether the recommendation mix is moving, not as the main training surface:

1. Enter For You once and sample 5–10 sequential items through the verified native next/down control. Do not watch irrelevant posts longer merely to complete a research sample; classify as soon as the premise is clear and advance normally.
2. Keep the same continuous-page invariants: no reload, Home reset, direct-post replacement, mixed transition method, or cherry-picking.
3. Record exact before/after identities and composition. A five-item sample is directional only; compare rolling checkpoints rather than one small sample.
4. If native transition fails after at least five reliable identities, mark `feed_validation_status=partial` and finish the checkpoint normally. This does not invalidate completed search training.
5. If fewer than five reliable identities are available, mark `feed_validation_status=unavailable`. When account/login/warning/Chrome ownership remain healthy, disable or defer only the feed-validation lane and continue future search-training blocks.
6. Two consecutive feed-transition failures may disable the validation lane for
   the current runtime. They never open the whole-run circuit. Search-origin
   failures rotate route/query or yield an automatic-resume checkpoint; only the
   hard-blocker whitelist can stop the mission.

Never use For You validation failure as permission for scroll/keyboard/wheel/reload fallback. It remains a lane-local evidence result.

## Verticality metrics and mode switch

For each For You checkpoint record:

```text
core_share = core / sampled
directional_share = (core + adjacent) / sampled
drift_share = (irrelevant + harmful_to_direction) / sampled
```

Use these operating heuristics, not as claims about TikTok's official algorithm:

| Observed For You composition | Next training plan |
|-|-|
| `core_share < 20%` | Remain search-training-led; run two training units before the next 5–10 item validation. |
| `core_share 20–50%` | Remain search-led but validate after each one or two training units. |
| `core_share > 50%` in two consecutive checkpoints | Permit mixed mode; retain at least one qualified search-consumption cluster per cycle. |

Do not switch to feed-led mode from one favorable checkpoint. If `core_share` stays below 10% across three validation checkpoints despite at least 60 qualified search views, change query/cluster mix and recheck account, region, and language context; do not compensate by posting more comments.

## Packaged default college/dorm block

Rotate among these families so the account stays vertically coherent without collapsing into one narrow microtopic:

- `roommate move in`, `college roommate storytime`, roommate chaos.
- `dorm move in`, `freshman move in day`, `dorm room setup`.
- `college day in my life`, campus routine, `grwm for class`.
- `college friend group`, `college game day`, campus social life.
- `finals week vlog`, dorm survival, campus-life failures.

Prefer recent posts from roughly the last 30 days when suitable current results exist. Older evergreen posts may be research evidence, but avoid relying on old viral inventory to represent the current audience language.

## Native browsing versus imitation

Prefer the visible native next/down control when it preserves playback, ordered feed context, and visible watch state. Before position 1, record a direction-specific exact signature through accessible name/title/test id/data-e2e or the verified live down-chevron SVG. Never use all enabled buttons as the locator: after position 1, both up and down may be enabled. Re-resolve the exact down signature after each DOM movement, click it exactly once per transition, and verify the before/after identity packet before continuing.

Incremental scroll/wheel gestures are not an automatic fallback. Under the
packaged default, failure of the visible native next/down control ends only the
current feed-validation sample and records `partial|unavailable`; do not ask the
user. If scroll was not already authorized/configured, abandon that
method for the runtime and continue search-led training. Never mix button,
keyboard, wheel, script scroll, reload, or reset transitions in one checkpoint
or recovery sequence. Direct URLs remain appropriate for exact verification and
revisiting candidates, but they are not a replacement for feed sampling.

For You sampling is one continuous-session invariant. Initial entry before position 1 may use the normal TikTok navigation link. After position 1, remain on the same page and preserve feed order. Do not use reload, `goto`, Home reopening, direct-post navigation, or a second For You entry as an ordinary transition. A reset is permitted only after the current block is explicitly stopped and reported as a separate hard recovery; recovered items belong to a new checkpoint, never the old denominator.

For every transition store `position_before`, `identity_before`, `action`, `position_after`, `identity_after`, and `advanced=true|false`. A repeated identity stays in the raw denominator and is labeled `duplicate`; a control that does not advance or destroys stable identity is `transition_failure`. Stop rather than disguising either condition.

The purpose is interface fidelity, not stealth. Never randomize timing, move the pointer artificially, insert fake indecision, or claim to be human. Respect CAPTCHA, verification, warnings, and rate limits. Detect platform warnings only from explicit system UI; never treat ordinary caption, hashtag, comment, or search-result words as system warnings.

For search training, watch long enough to understand the content and record actual progression when exposed. Do not encode a universal dwell-time formula: video length, clarity, replay need, and the research objective vary. Record whether the premise/payoff was understood, not a fabricated human-behavior score.

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

Do not stack like + favorite + repost + comment on every good post. During each
qualified view, evaluate all four lanes before leaving the post and execute the
justified verified action(s) immediately. Normally Like may accompany at most one
higher-intent action; use distinct posts for first capability gates, then the smallest justified signal. A natural
operating profile includes many read-only decisions, a few strong candidates,
and sparse verified mutations. For a cultivation/growth mission, an executor
must not silently downgrade the whole run to read-only or postpone interaction
until after viewing: it records all-lane candidate evaluation on every qualified
video and uses each eligible verified lane at least once per operating round
when a genuine candidate exists. Missing candidates require an exact logged
reason, not a fabricated quota fill.

An ended warning, rate limit, or failed gate from an older mission is historical
evidence, not a continuing blocker. When the latest explicit instruction requests
that lane and the current page/runtime is clean, run one fresh gate without
asking for the same authorization again. Pause only from current evidence.

## Ledger and capability matrix

For each viewed item record timestamp, source surface, ordered position when available, URL, freshness, creator, topic cluster, relevance label, premise/payoff understood, action candidate, and risk. For search-origin posts also record `opened_from_search=true`, stable post identity, playback progression evidence, and `qualified_search_view=true|false`. Keep `search_results_assessed`, `qualified_search_views`, and For You composition separate. Persist incrementally and validate each JSONL line immediately so a runtime failure or malformed append cannot erase/corrupt the block.

Track each action type as `untested`, `verified`, `failed`, `unverified`, or `disabled`, with account, browser/runtime, test URL, timestamp, immediate state, reload state, account-level state, and stop reason. `not_executed` is a batch result, not a capability result.

Never report success from a click, count animation, pressed control, toast, or network response alone. Require the action-specific persisted evidence defined in `engagement-and-analytics.md`.

## Stop and handoff

Stop mutation immediately for login mismatch, lost driver ownership, CAPTCHA, verification challenge, rate limit, warning/restriction, uncertain submission, or persistence failure. Keep read-only analysis available if the page and account remain safe to inspect.

At handoff report: account, driver owner, current surface/URL, sample composition, active seed cluster, candidate packet, capability matrix deltas, mutation count, ledger path, and exact next safe action.
