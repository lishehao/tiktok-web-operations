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

Classify recovery before changing authorization state:

- **Soft control reconnect:** the Chrome automation/control client timed out or restarted, then reattached to the same Chrome profile and TikTok storage/session; the expected account is still visible; no warning/challenge appears; and no mutation was in flight or left uncertain. Re-audit account, URL, warnings, and pending submission state, then resume the existing standing comment envelope. Do not require a new user confirmation or a new persistence test solely because the control client reinitialized.
- **Hard browser/runtime change:** the Chrome profile, TikTok account, login/cookie state, browser context, device verification state, or session identity changed or cannot be proven; or a mutation may have been interrupted. Disable standing mutation envelopes, inspect for uncertain submission, and call back for a new decision or authentication handoff.

A soft reconnect may be logged as a runtime event, but it is not a new `key_risk` unless account continuity, warning state, or submission certainty cannot be established.

If interruption happens near submit:

1. Do not retry.
2. Inspect Posts, Comments, or the public profile for the item.
3. Continue only after the prior action is confirmed present or absent.

TikTok pages often render in stages. A search or upload page may expose only a shell for roughly 1-3 seconds. Wait for a concrete result card, file input, or empty-state message before declaring the page unavailable. TikTok Studio navigation may report a navigation timeout after the destination has actually loaded; inspect the final URL, title, and DOM before retrying.

Do not treat a click, red heart, toast, or successful network response as final proof of an engagement action. Reopen or reload the item and verify the account-level state. If it does not persist, report the action as unverified or failed.

On 2026-07-10, three separate `@shehaolili` post-like tests—one photo post and two videos—changed to an active/pressed state immediately, then returned to inactive after reload. The latest test on `https://www.tiktok.com/@gideontrenary/video/7272558126740589866` moved the visible count from 5,340 to 5,341, but reload restored 5,340 and the target was absent from the account's Liked tab. A separate favorite test incremented a count, but the account exposed no saved-item proof and the control did not expose a persistent selected state. Treat post likes as failed and that favorite as unverified for this runtime. Do not enable those lanes until a fresh, separately confirmed one-action test survives both reload and an account-level ledger check.

The failed post-like control stopped its approved batch before favorite and comment were attempted. Record those later actions as `not_executed`, not failed. A batch-level stop does not establish a capability result for actions that never ran.

Current `@shehaolili` evidence snapshot for this Chrome/runtime on 2026-07-10:

| Action type | State | Evidence boundary |
|-|-|-|
| Post like | `failed` / `disabled` | Three immediate successes all rolled back after reload; latest target absent from Liked tab |
| Favorite/save | `unverified` / `disabled` | One visible count increment without persistent selected or account-level saved-item proof |
| Post repost | `untested` / `disabled_pending_gate` | User reports the control is usable, but no independent immediate/reload/account-level persistence evidence is in the current ledger |
| Proactive comment | `verified` | Multiple comments have survived post reload; still verify every later send independently |
| Comment like | `untested` | No persistence test |
| `Not interested` | `untested` | No persistence test |
| Follow | `untested` | No persistence test |

Treat this matrix as runtime evidence, not permanent account truth. Re-test only through a separately confirmed one-action packet; never re-enable a lane from elapsed time alone.

On the same account and date, one proactive comment on `@lenuww` appeared immediately as `@shehaolili` and remained present after reloading the post. Treat commenting as technically viable for this browser/account combination, while retaining exact-text action-time confirmation and post-reload verification. Do not generalize that success to likes, favorites, follows, or other action types.

## Scheduling

Verify scheduling support in the live TikTok Studio UI. Record both local time and timezone. If a Codex automation is used for a later review, validate the scheduler's actual `next_run_at`; do not assume local-hour RRULE semantics.

Heartbeats are read-only by default. They may inspect account state, comments, analytics, or a scheduled post. They must not publish, reply, edit, or delete without action-time confirmation.
