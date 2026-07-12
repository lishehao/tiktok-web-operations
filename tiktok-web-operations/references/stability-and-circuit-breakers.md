# Stability And Circuit Breakers

Use this reference during bootstrap, first-run validation, browser recovery, and any blocked or key-risk callback.

## Concurrent-account preflight

Another task controlling Chrome, TikTok, or the same account is not a global
operating blocker. Before creating or dispatching this run's executor, query
recent TikTok-related Codex Threads only to protect tab ownership, submission
certainty, and exact-target mutations:

- keep exactly one executor inside this coordinator/run, but allow an unrelated
  run to use the same account in its own dedicated tab;
- never interrupt, archive, navigate, close, or adopt another run merely because
  it is active;
- record `concurrent_same_account_activity=true` and
  `recommendation_attribution_contaminated=true` whenever another run may change
  consumption or engagement signals; do not claim causal feed correction while
  contamination is present;
- pause only an exact mutation conflict: the same target post/comment/profile or
  asset, the same action type, and another submission currently in flight or
  still uncertain. Pause that target/action only; browsing and different-target
  authorized actions may continue;
- an uncertain submission created by this executor remains a blocker for this
  executor under the normal submission-certainty rules.

Thread archival is lifecycle cleanup, not concurrency control. Keep this run's
registered pair unarchived; archive only released temporary probes or retired
executors that own no automation, tab, or uncertain submission.

## Dedicated-tab isolation

Chrome session ownership is per controlled tab, not a global lock on the user's Chrome profile:

1. Initialize Chrome from the current Chrome plugin root's `scripts/browser-client.mjs`.
2. At normal executor block start, create a new tab with `chrome.tabs.new()` and navigate that returned tab to TikTok. Verify the expected account in this dedicated tab before any further action.
3. Reuse a tab only when it is already part of this executor's current browser-control session. Use `user.openTabs()` plus `user.claimTab()` only for an explicit user-requested handoff or continuation of a known unclaimed tab.
4. If an existing tab reports `already part of browser session <uuid>`, leave it untouched and create a new tab. Do not interrupt, archive, or wait for that unrelated task. The message is not a global Chrome blocker.
5. Stop only if `tabs.new()` or navigation/control fails, the new tab does not inherit the expected login/account, this executor has an uncertain submission, or the exact target/action has a concurrent in-flight or uncertain submission.
6. Any concurrent task on the same TikTok account is allowed, including another run's mutations on different targets. Mark `concurrent_same_account_activity=true` and `recommendation_attribution_contaminated=true`; do not claim that one task caused feed changes.
7. At block completion, finalize only tabs created or controlled by this executor session. Never close or navigate another task's tabs.

## Canonical registry contract

Use `$thread-supervisor/references/canonical-registry.md`. The create prompt has
one inert canonical bootstrap object; the identity registry is finalized only
after the executor ID exists. Direction, authorization, mission/stop time, and
mutable runtime state are separate versioned objects or ledger state.

- Persist canonical UTF-8 JSON bytes and SHA-256 once. `SELF_REGISTRY` copies the
  stored identity bytes; `THREAD_READY` echoes their exact reference.
- The coordinator constructs dispatches from accepted
  `registry_ref`/`direction_ref`/`authority_ref`/`mission_ref` values. It never
  retypes, summarizes, or normalizes a prose registry.
- The `send_message_to_thread` target must equal the coordinator's accepted
  executor ID. A proven undelivered target typo allows one corrected send;
  failure at the correct target ends the block.
- Before Chrome, the executor validates all references, exact target/source IDs,
  required Luna/High profile, and current accepted versions.
- Any unresolved mismatch stops with `registry_mismatch`, zero external work,
  and one `REGISTRY_RECONCILIATION`. Do not alternate snapshots. If create/SELF
  values were mixed, retire the contaminated executor and permit at most one
  clean replacement; failure becomes `ORCHESTRATION_REGISTRY_BLOCKER`.
- A legitimate user change creates a new direction/authority/mission version
  and acknowledgement. It never rewrites the identity registry in place.

## Persistence mechanism

Persistence comes from the starter task after it becomes coordinator plus one
user-visible executor. Neither Thread may call `create_goal`, `update_goal`,
`spawn_agent`, or create descendant workers. The coordinator never operates
Chrome. The executor never creates a replacement for itself or manages an
automation.

An idle Thread is healthy persistent state. Do not use Goal Mode or an executor-
owned one-shot timer. Treat every executor wake/message as one bounded round: it
records a slot state, executes at most one block, releases Chrome, callbacks, and
becomes idle.

For an unattended multi-round run, after the immediate first block is proven,
the verified coordinator creates and manages two distinct recurring Heartbeats:

1. `operation_heartbeat`: explicit `targetThreadId=executor_thread_id`,
   `repeat=on`, finite `UNTIL` or equivalent `operation_stop_at` guard. It wakes
   the executor for one bounded block per slot. It is never `COUNT=1` followed by
   executor self-renewal.
2. `supervisor_heartbeat`: explicit `targetThreadId=coordinator_thread_id`,
   lower frequency, `repeat=on`, and the same finite stop guard. It is read-only
   and verifies executor wakes, new turns, callbacks, and the planned/started/
   completed/blocked/missed slot ledger.

The coordinator creates, views, updates, pauses, and deletes both automations.
The executor may receive the operation heartbeat but never creates, updates,
renews, pauses, or deletes either one. After creation, require readback proof of
each exact automation ID, target, repeat state, next run, local/UTC schedule, and
deadline. A missing executor wake/proof or broken repeat chain is
`SCHEDULER_CONTINUATION_FAILURE`; the supervisor reports it to the coordinator
without touching Chrome or attempting TikTok mutation.

## First-run stability smoke

Run this read-only block before a new executor performs a full search-training block or any mutation. Search-origin video consumption is the primary runtime gate; For You is an optional validation lane.

1. Verify the registered IDs, exact account, no unresolved submission owned by this executor, no exact-target/action mutation conflict, and no system-level challenge. Create the dedicated tab and record concurrent same-account activity and recommendation-attribution contamination.
2. Open one direction-relevant search query and classify the first three visible result cards.
3. Select one strong-core result, open it from the search surface, verify the stable post URL/creator identity, confirm playback or visible watch progression, and watch enough to understand its premise/payoff. Record it as one `qualified_search_view`, then return through normal navigation.
4. If search-origin open/playback/return succeeds with zero mutation, mark `search_training_runtime=verified`.
5. Separately enter For You once and attempt up to five reliable identities through the exact native down control. Use the same direction-specific locator rules below; never switch transition method.
6. If five identities/four advances succeed, mark `feed_validation_lane=verified`. If the native gate fails while account, dedicated-tab control, and search consumption remain healthy, mark only `feed_validation_lane=degraded|unavailable`; do not fail the search-training runtime and do not request a fallback.
7. Write separate search-training and feed-validation results, validate each JSONL line, and release Chrome.

Only `completed` with three assessed search cards, at least one qualified search view, stable account/tab control, zero mutation, and parseable ledger proves the primary runtime. For You success is additional capability evidence, not a prerequisite for search-led operation. A platform warning, account mismatch, dedicated-tab failure, search-origin playback failure, or malformed ledger remains a smoke blocker.

## Risk classification

Classify platform risk from explicit system UI: CAPTCHA/challenge surfaces, login state, rate-limit or restriction dialogs, alerts/status regions, TikTok system banners/toasts, or account-level warnings. Never scan the entire page text with a broad regex and treat words inside captions, hashtags, comments, creator names, or search results as platform warnings.

If a risk locator or diagnostic API fails, mark the system-warning state `unverified`, stop the current block, release Chrome, and callback once. Do not run broader DOM scans to prove absence.

## Browser-control rules

- Resolve the currently installed Chrome Skill/runtime from the current turn's Skill catalog. Record the plugin root, and import `<plugin-root>/scripts/browser-client.mjs` exactly; do not append `skills/control-chrome/` to the runtime module path. Carrying a versioned path forward from a prompt, ledger, prior run, or memory is forbidden.
- Prefer supported Playwright locators and live element attributes.
- Do not pass DOM-CUA element objects or circular structures as coordinates.
- Do not use unavailable page globals such as `NodeFilter`, broad page-evaluate text walkers, or unbounded container scans.
- Re-resolve locators after navigation or DOM replacement.
- Never persist or reuse a Chrome tab ID across turns, prompts, ledgers, or recovery blocks. At normal block start, create a dedicated tab with `chrome.tabs.new()` and use the returned tab object. Do not inspect, claim, navigate, or close another task's tab. `openTabs()`/`claimTab()` is reserved for an explicit handoff; an ownership message on an existing tab means skip that tab, not block the entire Chrome profile.

## Recovery budget

One operation block may have at most one narrowly scoped read-only recovery
sequence for each distinct failure class. For Chrome/page-load failures, use the
classification table and exact two-attempt ceiling in
`runtime-and-recovery.md`: retry the same URL once, then, only when needed, use a
fresh dedicated tab from the same Chrome binding plus a diagnostic tab. Record
every attempt. The recovery must test one falsifiable scope hypothesis and may
not change browser/profile, authentication, proxy, TLS policy, or authorization.

Do not hop among native button, PageDown, ArrowDown, wheel, script scroll, reload, and page reset. Under the packaged default, a failed native next/down smoke stops feed sampling. A scroll-only fallback requires a new explicit user decision; the coordinator cannot self-authorize it.

Persistent `tab_binding_stale`, `browser_disconnected`, `dns_network`,
`proxy_tls`, `blocked_by_client`, or `ambiguous_render` after its bounded
sequence stops the current block and callbacks the coordinator; it does not
masquerade as TikTok/account enforcement. HTTP 429, explicit platform challenge,
account mismatch, or uncertain submission returns immediately. Two consecutive
failures with the same dedicated-tab, exact-target mutation-collision, search-origin
open/playback, rendering, or diagnostic failure class open the whole-run circuit
breaker. Feed-native transition failures are lane-local when search training
and account/browser safety remain healthy; after two consecutive failures
disable/defer only `feed_validation_lane` for the current runtime.

The callback must preserve the exact code and phrase the inferred explanation
as `可能原因`, derived from that code plus same-domain/neutral probes. Include
bounded actions already attempted and the smallest user action. A fully
recovered transient stays in the ledger/ordinary completed callback and is
mentioned only in the next receipt's `本轮完成` line; it does not page the user or
add a fourth receipt line.

1. stop the executor block;
2. release Chrome;
3. callback `blocked` or `key_risk` once;
4. keep both persistent Threads idle;
5. wait for a user decision only when `decision_required=true`; otherwise keep
   the latest instruction and let the coordinator schedule one bounded read-only
   recheck of the exact external-state condition.

Changing query wording, removing a hashtag, renaming a probe, rebuilding a subagent, or declaring a “fresh blocked audit” is not an external-state change and does not reset the circuit breaker.
An ended historical warning/failure is not an active circuit state. Once the
recorded current blocker visibly clears, close the affected circuit and resume
the still-authorized latest instruction without another confirmation.

Handle expected UI gate failures as data, not exceptions. Compute `count/visible/enabled/identity_changed`; when a required boolean fails, write the terminal block result, release Chrome, and callback. Do not `throw` an expected ambiguity back into the reasoning loop, and do not run another locator diagnostic after the terminal condition is known.

## Stop acknowledgement

`STOP_AND_RELEASE` overrides every active block. The executor must stop without another probe, confirm descendants are absent, release Chrome, record mutation/submission certainty, append one final checkpoint, callback `STOPPED_AND_RELEASED`, and remain idle without self-resuming.
