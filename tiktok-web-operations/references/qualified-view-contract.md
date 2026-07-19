# Strict Qualified View Contract

Use this contract for every search-origin and For You video record. Keep three
states separate:

- `opened_only`: a stable post page opened, but consumption is unproven;
- `classified_sample`: stable identity and enough context exist to classify the
  item, but one or more qualification gates are missing; for search/bridge this
  is only a diagnostic record, while a sequential For You identity may also
  enter the validation sample denominator;
- `qualified_view`: relevance, continuous playback, and comprehension evidence
  all pass the gate below.

## Required evidence

A `qualified_view` requires all of:

1. one unique stable post URL/video ID and creator identity;
2. `core` relevance to the current cluster (`adjacent`, `irrelevant`, and
   `harmful_to_direction` never count as training views);
3. the exact source proof: search query plus result position or bridge parent
   for search-origin posts, or ordered native-feed position for For You;
4. at least two playback observations from the active owned tab, with forward
   progression after the first observation; page-open position alone is zero
   watch evidence;
5. continuous observed watch time meeting the duration floor below;
6. one concrete premise note and one concrete payoff/outcome note. For long
   videos, a resolved segment outcome is sufficient; a caption paraphrase or
   generic topic label is not;
7. no duplicate, failed/incomplete load, fabricated time, seek/scrub shortcut,
   background-tab assumption, or unresolved identity mismatch.

Apply the states in this order:

1. Use `opened_only` when identity/source/playback is unstable or the item is
   not yet reliably classifiable.
2. Use `classified_sample` when identity is stable and relevance can be
   classified but any watch-floor, observation, relevance, premise, or payoff
   gate fails. It never counts as a qualified view.
3. Use `qualified_view` only when every required gate passes.

A search/bridge `classified_sample` counts in neither search qualified views nor
the For You sample denominator. A For You `classified_sample` counts only in the
For You sampled denominator when its sequential identity is reliable.

Use the following minimum continuous observed watch floor. Round fractional
seconds upward:

| Video duration | Minimum evidence |
|-|-|
| `<=15s` | at least 80% of duration |
| `16–60s` | at least 40% of duration and at least 10 seconds |
| `>60s` | at least 25% of duration and at least 20 seconds, capped at 45 seconds |
| unknown/unreadable | at least 15 seconds plus two visible content-state changes |

The floor is necessary, not sufficient. If the premise/payoff is still unclear,
continue watching or record `classified_sample|opened_only`; never qualify it by
time alone. Completion before the floor may qualify only when the player exposes
a reliable total duration and the complete video actually ended.

Count only continuous playback observed after the first timestamp. Do not use
the absolute progress value as watched time, and do not seek, scrub, reload,
open a direct timestamp, or let an already-playing page retroactively satisfy
the floor. A natural loop/replay may add observed watch time but the unique
video still counts once per round.

## Ledger schema

Write these fields for every opened video before any qualified-view count:

```json
{
  "view_status":"opened_only|classified_sample|qualified_view",
  "relevance":"core|adjacent|irrelevant|harmful_to_direction",
  "source_proof":{"surface":"search|bridge|for_you","query":null,"position":1,"parent_url":null},
  "stable_post_id":"...",
  "duration_seconds":45,
  "progress_start_seconds":1,
  "progress_end_seconds":20,
  "continuous_watch_seconds":19,
  "required_watch_seconds":18,
  "playback_observations":2,
  "premise_evidence":"one concrete observed setup",
  "payoff_evidence":"one concrete observed outcome",
  "qualified_view":true,
  "rejection_reason":null
}
```

If a field is unavailable, store `null` and fail closed unless the explicit
unknown-duration path passes. Validate that round callback qualified counts equal
the number of unique ledger rows with `qualified_view=true`. An action attempt
does not make a view qualified, and a mutation issued before qualification is a
contract violation that must be reported rather than hidden.

For You validation keeps a separate denominator: every reliable sequential
identity may count as `sampled`, including an early-skipped drift item. Only a
`core` item passing this strict contract enters `qualified_views.for_you`.
