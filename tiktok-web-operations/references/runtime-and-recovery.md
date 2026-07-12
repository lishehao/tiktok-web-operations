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

When login is still missing or mismatched after one bounded same-Chrome account
recheck:

1. Keep the TikTok page open as a handoff.
2. Ask the user to log in manually.
3. Resume by reading the exact profile identity and TikTok Studio availability.
4. Never enter credentials, OTPs, passkeys, or recovery codes.

## Chrome and page-load recovery

A page-load failure is not, by itself, TikTok enforcement or account risk. Keep
transport/control evidence separate from explicit platform UI. Recovery stays
inside the user's original logged-in Chrome profile: do not switch to Computer
Use, another browser, a clean context, or a login bypass.

### Error classification

| Class | Exact evidence or examples | Initial interpretation | Allowed recovery |
|-|-|-|-|
| `tab_binding_stale` | missing, stale, or closed tab; tab no longer belongs to the current browser session | tab-level control loss, not an account or network verdict | discard only the stale tab binding and create a fresh dedicated tab from the existing Chrome browser binding |
| `browser_disconnected` | explicit browser-disconnected or Chrome-extension communication error | browser binding is invalid; ordinary empty tab results do not prove this | reconnect the same running Chrome/profile through the supported Chrome extension, then create a fresh dedicated tab |
| `dns_network` | `ERR_NAME_NOT_RESOLVED`, `ERR_INTERNET_DISCONNECTED`, `ERR_NETWORK_CHANGED`, `ERR_CONNECTION_TIMED_OUT`, `ERR_CONNECTION_RESET`, `ERR_CONNECTION_CLOSED` | DNS, interface, or transport failure; not TikTok risk | bounded wait/retry, then same-Chrome diagnostic tab to distinguish global network, TikTok domain, and target-page scope |
| `proxy_tls` | `ERR_PROXY_CONNECTION_FAILED`, `ERR_TUNNEL_CONNECTION_FAILED`, any `ERR_CERT_*` | proxy, tunnel, certificate, clock, or TLS path failure | bounded diagnostic only; never disable certificate checks, replace the user's proxy, or bypass the warning |
| `http_status` | HTTP `429`, `403`, or `5xx` | `429` is a platform-rate-limit signal; `403` may be auth, WAF, or policy and needs visible-page evidence; `5xx` is normally server-side | preserve status/body evidence; do not retry mutations; bounded retry only for `5xx`; for `429`, record displayed retry/cooldown and let Heartbeat recheck automatically; persistent explicit account lock/ban follows the hard-blocker whitelist |
| `blocked_by_client` | `ERR_BLOCKED_BY_CLIENT` | local extension/content policy or request blocking; not account risk by itself | retry once in a fresh dedicated tab in the same Chrome; do not disable the user's extensions automatically |
| `ambiguous_render` | blank page, perpetual loading shell, script error, missing content, or navigation timeout with no explicit code | renderer/page ambiguity | allow the normal 1–3 second staged-render wait, inspect final URL/title/DOM, then use the same bounded recovery sequence |

### Likely-cause inference

Generate `likely_cause` only from the exact error/status plus same-domain and
neutral-page probe results. It is an evidence-bounded hypothesis, never a root-
cause diagnosis. In user-facing Chinese, always begin with `可能原因：`; never
say `根因是`, `确定是`, or claim that TikTok restricted the account without
explicit platform UI.

| Exact evidence | Required likely-cause wording |
|-|-|
| `ERR_NETWORK_CHANGED` | 网络接口、VPN 或代理连接可能刚发生切换 |
| `ERR_CONNECTION_RESET` | 连接可能被网络链路、VPN、服务端或安全软件中途重置 |
| `ERR_CONNECTION_TIMED_OUT` | 网络路径、代理/VPN 或站点响应可能超时 |
| `ERR_CONNECTION_CLOSED` | 对端或中间网络路径可能提前关闭连接 |
| `ERR_INTERNET_DISCONNECTED` | 当前设备可能暂时失去互联网连接 |
| `ERR_NAME_NOT_RESOLVED` | 目标域名或当前 DNS 解析可能失败 |
| `ERR_PROXY_CONNECTION_FAILED` / `ERR_TUNNEL_CONNECTION_FAILED` | 当前代理或隧道连接可能不可达 |
| `ERR_CERT_*` | 系统时间、证书链或代理/TLS 检查路径可能异常；不得绕过证书警告 |
| HTTP `5xx` | TikTok 或其上游服务可能暂时异常 |
| HTTP `403` | 当前请求可能被登录、权限、WAF 或站点策略拒绝；需结合可见页面判断 |
| HTTP `429` | TikTok 当前可能正在限流 |
| `ERR_BLOCKED_BY_CLIENT` | Chrome 扩展、内容过滤器或本地规则可能拦截了请求 |
| no exact code / blank or script failure | 页面脚本、渲染、单路由或暂态加载可能异常 |

Refine that phrase with probes, without overstating certainty:

- neutral HTTPS fails too: local/global network, DNS, proxy, TLS, or security
  path is more likely than a TikTok-only problem;
- neutral succeeds but TikTok home fails: TikTok domain/CDN/path is more likely;
- TikTok home succeeds but the exact target fails: target route/page/script is
  more likely;
- probes are unavailable: keep the cause broad and set
  `likely_cause_basis=<exact code>; probes=unavailable`.

Store the exact code separately from the hypothesis. `likely_cause` must never
replace `error_code`, and a probe outcome must not overwrite the original code.

Do not infer `browser_disconnected` from an empty tab list. Tab binding and
browser binding are separate: only an explicit browser-disconnected result
invalidates the browser binding. Never call browser-discovery APIs to recover a
lost tab; reuse the existing Chrome browser binding and create a new tab.

### Bounded recovery sequence

Before recovery, append one ledger event with timestamp, exact URL, exact error
code/message, classification, expected account, tab/browser binding state,
whether a mutation was in flight, submission certainty, `likely_cause`,
`likely_cause_basis`, and `user_action_required`. Then:

1. If a mutation may have been submitted, do not retry it as ordinary recovery.
   Freeze that exact target/action, record the uncertainty, and continue only
   independent safe search/view/action scopes. Resolve it later through the
   normal evidence check; do not ask the user merely to authorize a retry.
2. Wait briefly, then retry the exact current URL once. A staged-render wait is
   normally 1–3 seconds; a transport retry may use one additional short backoff
   no longer than about 10 seconds.
3. If the tab is stale or the page still cannot be inspected, discard only that
   tab object and create a fresh dedicated tab with `chrome.tabs.new()` from the
   same Chrome browser binding. If Chrome explicitly disconnected, reconnect
   that same Chrome/profile first.
4. In a separate temporary diagnostic tab, check the same-domain home
   `https://www.tiktok.com/`. When scope remains ambiguous, also check one
   neutral HTTPS site. Close only the executor-created diagnostic tab. Interpret
   neutral failure as global network/path scope, neutral success plus TikTok
   failure as TikTok-domain scope, and TikTok home success plus target failure as
   target-page scope.
5. Reopen the exact target URL and re-confirm the expected TikTok account,
   login state, explicit warning/challenge state, and submission certainty.
6. Resume the active mission from its durable checkpoint only after those checks pass. Record
   `recovered=true`, `account_reverified=true`, and the final scope. A recovered
   transient error does not disable a mutation lane or terminate a long run.

When recovery succeeds, do not send a standalone user interruption. Keep the
event in the ledger and ordinary completed callback. At the next scheduled
three-line receipt, append one short clause to `本轮完成`, for example:
`期间 ERR_NETWORK_CHANGED 已在原 Chrome 会话内恢复；可能原因：网络或代理连接切换。`
Do not add a fourth line.

The sequence permits at most two page attempts after the first failure: one
same-URL retry and, when necessary, one fresh-tab retry/diagnostic sequence.
Never loop, reload repeatedly, alter proxy/TLS settings, or use another browser.
If the same failure remains after this sequence, yield only when the current
runtime turn must end, release owned tabs, and preserve the ledger plus exact
auto-resume condition. Do not send a standalone risk callback or ask the user.
Keep the correctly bound coordinator Heartbeat repeat-on so a later wake can retry
automatically. Continue another approved route/scope when possible. A timed HTTP
429 waits and rechecks automatically. Persistent human CAPTCHA/challenge,
unrecoverable login/account mismatch, explicit account lock/ban, or unavailable
sole allowed Chrome control follows `blocker-minimization.md`. Uncertain
submission freezes only that exact mutation.

A persistent technical checkpoint includes the exact code, `likely_cause` as a
possibility, probe evidence, every attempted recovery action, and the automatic
resume condition. Do not ask the user to diagnose ordinary connectivity, VPN,
proxy, extension, route, renderer, `5xx`, or timed `429` states. Only the hard-
blocker whitelist produces a user action. The executor never clears cookies,
changes proxy/DNS/TLS, disables extensions, switches browsers, or repeats an
uncertain mutation.

Never carry a tab ID across turns. At normal executor activation/resume, create a tab with `chrome.tabs.new()` and use that returned object. Reuse a tab only when it is already part of this executor's current control session. `user.openTabs()` plus `user.claimTab()` is allowed only for an explicit user-requested handoff or continuation of a known unclaimed tab; never guess or touch another app task's tab.

Resolve the current Chrome Skill/runtime from the current turn's Skill catalog and record the plugin root. Import `<plugin-root>/scripts/browser-client.mjs`; the Skill file lives below `<plugin-root>/skills/control-chrome/`, but the runtime module does not. Never reuse a versioned cache path copied from a prior prompt, ledger, run, or memory. Prefer supported Playwright locators; do not pass DOM-CUA objects/circular structures as coordinates, use unavailable page globals such as `NodeFilter`, or run broad text walkers to diagnose state.

When an explicit handoff `claimTab()` reports `already part of browser session <uuid>`, leave that tab untouched and create a new dedicated tab. An active unrelated owner is not a global Chrome scheduling conflict. Stop only if new-tab creation/control fails or the dedicated tab cannot prove expected login/account. Do not count an existing-tab ownership message as a Feed transition failure or disable TikTok mutation lanes.

Classify runtime continuity before changing authorization state:

- **Soft control reconnect:** the Chrome automation/control client timed out or restarted, then reattached to the same Chrome profile and TikTok storage/session; the expected account is still visible; no warning/challenge appears; and no mutation was in flight or left uncertain. Re-audit account, URL, warnings, and pending submission state, then resume the existing standing comment envelope. Do not require a new user confirmation or a new persistence test solely because the control client reinitialized.
- **Hard browser/runtime change:** the Chrome profile, TikTok account, login/cookie state, browser context, device verification state, or session identity changed or cannot be proven; or a mutation may have been interrupted. Pause standing mutation envelopes and inspect for uncertain submission. Require a decision only for manual authentication, unresolved submission, account ambiguity, or expanded scope. If the same account and submission certainty are later proven, restore the unchanged latest user envelope automatically without asking for another confirmation.

A soft reconnect may be logged as a runtime event, but it is not a new `key_risk` unless account continuity, warning state, or submission certainty cannot be established. A recovered `dns_network`, `proxy_tls`, `blocked_by_client`, `ambiguous_render`, or tab-binding event is likewise infrastructure evidence, not a TikTok warning.

Classify warnings only from explicit system UI such as CAPTCHA/challenge, login,
rate-limit/restriction dialogs, alerts/status regions, TikTok banners/toasts, or
account warnings. Caption, hashtag, comment, creator, and search-result text
containing words such as `warning` or `verify` is content, not a platform
warning. If the diagnostic locator/API fails, mark that diagnostic route
`unverified`, use the bounded native recovery once, and continue another safe
scope or later Heartbeat recheck; do not infer platform risk or broaden the scan.

If interruption happens near submit:

1. Do not retry.
2. Inspect Posts, Comments, or the public profile for the item.
3. Continue only after the prior action is confirmed present or absent.

TikTok pages often render in stages. A search or upload page may expose only a shell for roughly 1-3 seconds. Wait for a concrete result card, file input, or empty-state message before declaring the page unavailable. TikTok Studio navigation may report a navigation timeout after the destination has actually loaded; inspect the final URL, title, and DOM before retrying.

Do not treat a click, red heart, toast, count animation, or successful network response as final proof of an engagement action. Verify each lane with the action-specific settlement and persistence checks in `engagement-and-analytics.md`.

Apply the bounded recovery budget in `stability-and-circuit-breakers.md`. One
bounded recovery sequence is allowed per distinct failure class per activation.
Persistent same-class failure after the sequence checkpoints and callbacks the
coordinator; the executor never deletes a Heartbeat, silently abandons the
mission, self-restarts, or asks whether to retry an ordinary technical failure.

## Capability evidence isolation

Every live account and browser/runtime combination starts with its own capability matrix. Never reuse another account's successful or failed test as proof for the current account.

| Action type | Packaged startup state | Enablement gate |
|-|-|-|
| Post like | `disabled_by_default` or `pending_fresh_gate` when explicitly requested | Latest explicit user authorization plus one fresh independent immediate/reopen/account-level persistence test; old mission failures are historical only |
| Favorite/save | `unverified` / `disabled_pending_gate` | One strong-core post; selected state immediately, near +3 seconds, and after a 10-second total settlement window; then reopen/reload and account-level proof when exposed |
| TikTok Repost | `unverified` / `disabled_pending_gate` | One strong-core post; click only the explicit TikTok Repost control, then verify immediate, reopen/reload, and account-level evidence when available |
| Proactive comment | `unverified` / `disabled_pending_gate` | One eligible strong-core post, one submission, exact author/text visible after reload |
| Comment like | `untested` / `disabled` | Separate one-comment persistence gate |
| `Not interested` | `untested` / `disabled` | Separate exact-post gate and user authorization |
| Follow | `untested` / `disabled` | Separate exact-creator gate and user authorization |

A current failed lane does not prove that another lane fails. A stopped batch
makes later unattempted actions `not_executed`, not failed. Suspend only the
failed lane. A timed throttle auto-waits; uncertain submission freezes its exact
target/action; warning/challenge/account ambiguity may suspend all mutations but
not safe search/view. Stop the mission only for `blocker-minimization.md`'s hard
whitelist. When a later explicit mission requests that lane and no current
blocker is visible, move it to `pending_fresh_gate` and test once without asking
the user to reconfirm; keep the earlier failure as historical ledger evidence.

Store account handles, test URLs, timestamps, and raw persistence evidence only in that run's private ledger. Do not publish account-specific evidence in the reusable Skill or its public README.

## Scheduling

Verify scheduling support in the live TikTok Studio UI. Record both local time and timezone. If a Codex automation is used for a later review, validate the scheduler's actual `next_run_at`; do not assume local-hour RRULE semantics.

The coordinator Heartbeat is always read-only toward TikTok. If it proves the
callback chain broke, it may cause the coordinator to resume the already
authorized continuous mission from its validated checkpoint; it never expands
action authority or retries an uncertain submission. The Heartbeat is not
retired for an ordinary technical or lane failure.
