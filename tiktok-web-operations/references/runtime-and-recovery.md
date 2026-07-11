# Runtime And Recovery

## Dependencies

- Codex skill support.
- Chrome control connected to the user's existing Chrome profile.
- A TikTok account already logged in by the user.
- Local date, time, timezone, and UTC offset.
- TikTok web and TikTok Studio features visible for the account.
- Automation support only for multi-round or scheduled follow-up work.
- Local video files only when publishing or scheduling.

Do not require TikTok API keys, passwords, Playwright outside the Chrome skill, Computer Use, Python, Node.js, or a database for ordinary operation.

## Login audit

Open `https://www.tiktok.com/` and verify an actual profile identity. A visible `Log in` button together with an empty `/@` profile route means the session is not ready.

When login is missing:

1. Keep the TikTok page open as a handoff.
2. Ask the user to log in manually.
3. Resume by reading the exact profile identity and TikTok Studio availability.
4. Never enter credentials, OTPs, passkeys, or recovery codes.

## Chrome recovery

For a stale tab or dropped connection, reconnect to Chrome, obtain a fresh tab if needed, and re-read the page state. Do not switch browser surfaces merely because Chrome needs reconnection.

Resolve the current Chrome Skill/runtime from the current turn's Skill catalog and record that source path. The runtime call may import that exact current path; never reuse a versioned cache path copied from a prior prompt, ledger, run, or memory. Prefer supported Playwright locators; do not pass DOM-CUA objects/circular structures as coordinates, use unavailable page globals such as `NodeFilter`, or run broad text walkers to diagnose state.

Classify recovery before changing authorization state:

- **Soft control reconnect:** the Chrome automation/control client timed out or restarted, then reattached to the same Chrome profile and TikTok storage/session; the expected account is still visible; no warning/challenge appears; and no mutation was in flight or left uncertain. Re-audit account, URL, warnings, and pending submission state, then resume the existing standing comment envelope. Do not require a new user confirmation or a new persistence test solely because the control client reinitialized.
- **Hard browser/runtime change:** the Chrome profile, TikTok account, login/cookie state, browser context, device verification state, or session identity changed or cannot be proven; or a mutation may have been interrupted. Disable standing mutation envelopes, inspect for uncertain submission, and call back for a new decision or authentication handoff.

A soft reconnect may be logged as a runtime event, but it is not a new `key_risk` unless account continuity, warning state, or submission certainty cannot be established.

Classify warnings only from explicit system UI such as CAPTCHA/challenge, login, rate-limit/restriction dialogs, alerts/status regions, TikTok banners/toasts, or account warnings. Caption, hashtag, comment, creator, and search-result text containing words such as `warning` or `verify` is content, not a platform warning. If the diagnostic locator/API fails, stop with warning state `unverified`; do not broaden the scan or repeatedly probe.

If interruption happens near submit:

1. Do not retry.
2. Inspect Posts, Comments, or the public profile for the item.
3. Continue only after the prior action is confirmed present or absent.

TikTok pages often render in stages. A search or upload page may expose only a shell for roughly 1-3 seconds. Wait for a concrete result card, file input, or empty-state message before declaring the page unavailable. TikTok Studio navigation may report a navigation timeout after the destination has actually loaded; inspect the final URL, title, and DOM before retrying.

Do not treat a click, red heart, toast, count animation, or successful network response as final proof of an engagement action. Verify each lane with the action-specific settlement and persistence checks in `engagement-and-analytics.md`.

Apply the bounded recovery budget in `stability-and-circuit-breakers.md`. One narrow recovery is allowed per distinct failure class; two consecutive same-class failures open the circuit and require idle wait for user or external-state change.

## Capability evidence isolation

Every live account and browser/runtime combination starts with its own capability matrix. Never reuse another account's successful or failed test as proof for the current account.

| Action type | Packaged startup state | Enablement gate |
|-|-|-|
| Post like | `disabled` | Explicit user authorization plus a fresh independent immediate/reopen/account-level persistence test |
| Favorite/save | `unverified` / `disabled_pending_gate` | One strong-core post; selected state immediately, near +3 seconds, and after a 10-second total settlement window; then reopen/reload and account-level proof when exposed |
| TikTok Repost | `unverified` / `disabled_pending_gate` | One strong-core post; click only the explicit TikTok Repost control, then verify immediate, reopen/reload, and account-level evidence when available |
| Proactive comment | `unverified` / `disabled_pending_gate` | One eligible strong-core post, one submission, exact author/text visible after reload |
| Comment like | `untested` / `disabled` | Separate one-comment persistence gate |
| `Not interested` | `untested` / `disabled` | Separate exact-post gate and user authorization |
| Follow | `untested` / `disabled` | Separate exact-creator gate and user authorization |

A failed lane does not prove that another lane fails. A stopped batch makes later unattempted actions `not_executed`, not failed. Disable only the failed lane unless a warning, throttle, challenge, uncertain submission, account mismatch, or hard runtime change makes every mutation unsafe.

Store account handles, test URLs, timestamps, and raw persistence evidence only in that run's private ledger. Do not publish account-specific evidence in the reusable Skill or its public README.

## Scheduling

Verify scheduling support in the live TikTok Studio UI. Record both local time and timezone. If a Codex automation is used for a later review, validate the scheduler's actual `next_run_at`; do not assume local-hour RRULE semantics.

Heartbeats are read-only by default. They may inspect account state, comments, analytics, or a scheduled post. They must not publish, reply, edit, or delete without action-time confirmation.
