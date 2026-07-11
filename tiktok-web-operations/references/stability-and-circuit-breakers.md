# Stability And Circuit Breakers

Use this reference during bootstrap, first-run validation, browser recovery, and any blocked or key-risk callback.

## Same-account mutation-writer preflight

Before creating or dispatching an executor, query recent TikTok-related Codex Threads and inspect any active or in-progress result. Require one of these states:

- no other TikTok Chrome executor is active;
- the exact incumbent was explicitly retired by the user, returned `STOPPED_AND_RELEASED`, released Chrome, and has no mutation or submission in flight; or
- the incumbent is the same registered executor being resumed.

Do not create a second same-account mutation executor while write authority is active, ambiguous, or delegated to a collaboration agent. Do not infer that archiving stops an active turn. Stop/release first, verify, then archive only when the user requested archival.

## Dedicated-tab isolation

Chrome session ownership is per controlled tab, not a global lock on the user's Chrome profile:

1. Initialize Chrome from the current Chrome plugin root's `scripts/browser-client.mjs`.
2. At normal executor block start, create a new tab with `chrome.tabs.new()` and navigate that returned tab to TikTok. Verify the expected account in this dedicated tab before any further action.
3. Reuse a tab only when it is already part of this executor's current browser-control session. Use `user.openTabs()` plus `user.claimTab()` only for an explicit user-requested handoff or continuation of a known unclaimed tab.
4. If an existing tab reports `already part of browser session <uuid>`, leave it untouched and create a new tab. Do not interrupt, archive, or wait for that unrelated task. The message is not a global Chrome blocker.
5. Stop only if `tabs.new()` or navigation/control fails, the new tab does not inherit the expected login/account, another same-account mutation executor is active/uncertain, or a submission is uncertain.
6. A concurrent read-only task on the same TikTok account does not block a mechanical smoke, but mark `recommendation_attribution_contaminated`; do not claim that one task caused feed changes.
7. At block completion, finalize only tabs created or controlled by this executor session. Never close or navigate another task's tabs.

## Immutable registry contract

Treat these fields as byte-for-byte immutable after `SELF_REGISTRY`: coordinator Thread ID, executor Thread ID, account handle, ledger path, mutation authorization, role, model, and thinking level.

- The coordinator must construct every dispatch by copying the registered values; it must not retype, shorten, normalize, relocate, or regenerate them.
- The `send_message_to_thread` tool-call target is an immutable field too. Set it from the registry and compare the actual target before sending. If a failed call proves the target was mistyped and nothing was delivered, one corrected send to the registered ID is allowed and must be logged; a failure at the correct target is terminal for that block.
- Before connecting to Chrome, the executor must compare every dispatch field with its local registry snapshot.
- Any mismatch is a terminal `registry_mismatch`: do not connect/navigate Chrome, do not create a second ledger, and callback once with both values.
- A bootstrap correction may replace the dispatch only before Chrome navigation and only when it repeats the original authoritative registry exactly. It does not change the registry itself.

## Persistence mechanism

Persistence comes from the starter task after it becomes coordinator plus one
user-visible executor, connected by callback-driven bounded blocks. Neither
Thread may call `create_goal`, `update_goal`, `spawn_agent`, or create descendant
workers. The coordinator never operates Chrome. The executor never creates a
replacement for itself.

An idle Thread is healthy persistent state. Do not manufacture activity through polling, Goal Mode continuation, or self-dispatch.

Treat every executor message as one bounded round. The executor completes that block, releases Chrome, callbacks, and becomes idle. The coordinator dispatches at most one next block after reconciling the callback.

For an unattended multi-round run, attach an optional low-frequency heartbeat to the coordinator only. Use it as a watchdog and round scheduler, not as a Chrome operator:

- read the coordinator/executor latest state;
- stay silent and dispatch nothing while the executor is running;
- dispatch one next bounded block only when the prior callback is complete, the executor is idle, the circuit is closed, and `operation_stop_at` has not passed;
- never create/replace Threads, bypass a blocker, or touch Chrome from the heartbeat;
- at or after `operation_stop_at`, send one `STOP_AND_RELEASE`, confirm the final callback, and remove the heartbeat.

Soft callbacks remain the primary sequencing signal. The heartbeat is a missed-callback/time-bound safety net and must never overlap executor turns.

## First-run stability smoke

Run this read-only block before a new executor performs a full calibration block or any mutation:

1. Verify the registered IDs, exact account, no incumbent same-account mutation writer, no submission in flight, and no system-level challenge. Create the dedicated tab and record whether concurrent same-account browsing contaminates recommendation attribution.
2. Open one direction-relevant search query and classify the first three visible results without opening interaction controls.
3. Enter For You once.
4. Enumerate the navigation controls once and identify the down control by a direction-specific signature: prefer an accessible name/title/test id/data-e2e that specifically means next/down; otherwise use the unique down-chevron SVG signature observed in the current live UI. The currently verified fallback signature is `button:has(svg path[d^="m24 28.75"])`, but use it only after confirming it is the visible down control. Never use a broad locator such as `button:not([disabled])`, because the up and down controls can both become enabled after position 1.
5. Require the exact down signature to have count `1`, visible, and enabled. Record that signature with the position-1 identity packet, then re-resolve that same exact signature after every DOM movement for four single-click transitions to positions 2–5. Do not retain a stale element or ordinal.
6. Require five reliable identities, four verified advances, zero reset/reload/Home re-entry, and zero mutation.
7. Write the smoke result and release Chrome.

Only `completed` with those acceptance criteria proves feed-control stability. A page-based blocker is useful startup evidence but is not a stability pass. Up-control enablement after the first advance is expected and must not make the exact down-control locator ambiguous.

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

One operation block may have at most one narrowly scoped read-only recovery block for its distinct failure class. The recovery must keep the same accepted transition method and test one falsifiable hypothesis.

Do not hop among native button, PageDown, ArrowDown, wheel, script scroll, reload, and page reset. Under the packaged default, a failed native next/down smoke stops feed sampling. A scroll-only fallback requires a new explicit user decision; the coordinator cannot self-authorize it.

Two consecutive failures with the same dedicated-tab, mutation-writer, transition, rendering, or diagnostic failure class open the circuit breaker:

1. stop the executor block;
2. release Chrome;
3. callback `blocked` or `key_risk` once;
4. keep both persistent Threads idle;
5. wait for a user instruction or a verifiable external-state change.

Changing query wording, removing a hashtag, renaming a probe, rebuilding a subagent, or declaring a “fresh blocked audit” is not an external-state change and does not reset the circuit breaker.

Handle expected UI gate failures as data, not exceptions. Compute `count/visible/enabled/identity_changed`; when a required boolean fails, write the terminal block result, release Chrome, and callback. Do not `throw` an expected ambiguity back into the reasoning loop, and do not run another locator diagnostic after the terminal condition is known.

## Stop acknowledgement

`STOP_AND_RELEASE` overrides every active block. The executor must stop without another probe, confirm descendants are absent, release Chrome, record mutation/submission certainty, append one final checkpoint, callback `STOPPED_AND_RELEASED`, and remain idle without self-resuming.
