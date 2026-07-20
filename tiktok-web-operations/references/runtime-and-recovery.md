# Runtime And Recovery

Use this reference for every Chrome, tab, navigation, page-read, playback, and
tool timeout. Recover inside the executor's owned Chrome surface; callback only
the exact registered main task. Never contact an unrelated TikTok task.

## Contents

- Recovery invariant
- Error classes and edge cases
- Required recovery record
- One bounded same-Chrome recovery pass
- Persistent retry across Heartbeats
- Callback and task-tool uncertainty

## Recovery invariant

Use **one bounded recovery pass per active executor turn, then a durable
cross-wake retry**. A transient failure never becomes permanent merely because
one pass failed:

```text
observe -> local retry -> same-Chrome rebind -> scope probes -> restore
        -> recovered: continue the same round
        -> unresolved: ROUND_YIELDED + RECOVERY_PENDING + IDLE
main recurring Heartbeat -> RECOVERY_FIRST for the same round/cursor/budgets
```

The main-owned Heartbeat remains repeat-on until mission cutoff or explicit
terminal release. The executor never creates a recovery timer. Repeated recovery
wakes continue until health proof, user stop, cutoff, or a live human-repair
condition. Do not loop indefinitely inside one model turn or send catch-up work.

## Error classes and edge cases

| Class | Evidence examples | Immediate interpretation |
|-|-|-|
| tab binding | stale/closed/missing tab; empty tab list | discard only the tab binding; an empty list after cleanup does not invalidate the browser binding |
| browser control | explicit browser disconnected; browser-client/tool unavailable | reconnect the same Chrome extension/runtime; never switch browser |
| read-only tool timeout | navigation, DOM, screenshot, or playback read timed out before mutation | safe to run the bounded recovery pass; no mutation freeze |
| mutation tool timeout | click/send was issued or may have been issued and the return is unknown | `SUBMISSION_UNCERTAIN`; freeze exact `action_key` forever |
| DNS/network | `ERR_NAME_NOT_RESOLVED`, `ERR_INTERNET_DISCONNECTED`, `ERR_NETWORK_CHANGED`, `ERR_CONNECTION_TIMED_OUT/RESET/CLOSED` | DNS, connectivity, VPN/proxy, or local security interruption may be involved |
| proxy/TLS | `ERR_PROXY_CONNECTION_FAILED`, `ERR_TUNNEL_CONNECTION_FAILED`, `ERR_CERT_*` | proxy tunnel or certificate path may be involved; never change either automatically |
| HTTP 403 | exact route denied | probe scope; do not infer account lock from one response |
| HTTP 429 | explicit rate limit, optionally `Retry-After`/expiry | store exact earliest retry time; no busy-wait or alternate-account bypass |
| HTTP 5xx | platform service response | retry once locally, then later wake if domain remains unhealthy |
| client block | `ERR_BLOCKED_BY_CLIENT` | extension or local filtering may affect this route; fresh owned tab/route probe once |
| render/hydration | blank/loading shell, missing stable identity, script error without code | one hydration wait plus one alternate supported read surface; do not treat a video canvas or sparse DOM as blank when stable identity/controls exist |
| media stall | play state never advances on two observations | click a visible Play control once; otherwise reject the view and rotate; repeated independent stalls become render/domain evidence |
| search empty shell | search chrome exists but results never hydrate | distinguish from genuine zero results; retry native search once, then rotate query/route |
| dismissible overlay | app-open prompt, signup promo, or ordinary modal with an explicit close control | close once without accepting terms, installing/opening an app, entering data, or changing consent; then re-read identity |
| consent or terms choice | cookie/privacy/terms prompt requires accepting, rejecting, or changing a durable preference | use an already-present neutral close/continue-only path if available; otherwise skip that route and never choose consent for the user |
| gated content | age/sensitive-content warning or access acknowledgment | skip that candidate; never bypass or infer an account restriction from one gate |
| unavailable content | private, deleted, creator-unavailable, region-blocked, or removed post | terminal candidate skip; do not recover/reload the same URL repeatedly |
| session | login redirect, handle unavailable, account mismatch | `UNVERIFIED` is not mismatch; recheck exact handle in a fresh owned TikTok tab |

Never assert a root cause from one symptom. Record `likely_cause` as `可能原因`
only after exact code plus same-domain and neutral probes.

## Required recovery record

Append one `browser_recovery/v1` record before retrying:

```json
{
  "schema":"browser_recovery/v1",
  "run_id":"...",
  "round_id":"...",
  "round_seq":1,
  "boundary_seq":1,
  "retry_epoch":1,
  "phase":"OBSERVED|LOCAL_RETRY|REBOUND|PROBED|RESTORED|RECOVERY_PENDING|HUMAN_REPAIR_PENDING",
  "error_class":"...",
  "exact_code":null,
  "failed_url":"...",
  "failure_stage":"PRE_NAVIGATION|READ_ONLY|PRE_MUTATION|MUTATION_CALL|POST_ATTEMPT|CALLBACK|RELEASE",
  "submission_certainty":"NOT_APPLICABLE|NOT_SUBMITTED|CALL_RETURNED|UNKNOWN_AFTER_TIMEOUT",
  "action_key":null,
  "tiktok_probe":"NOT_RUN|HEALTHY|FAILED|UNKNOWN",
  "neutral_probe":"NOT_RUN|HEALTHY|FAILED|UNKNOWN",
  "account_probe":"NOT_RUN|MATCH|MISMATCH|LOGGED_OUT|CHALLENGE|UNKNOWN",
  "expected_account_handle":"@...",
  "observed_account_handle":null,
  "account_proof_surface":"profile_link|profile_heading|account_menu|none",
  "resume_cursor_ref":null,
  "next_retry_not_before_utc":null
}
```

Increment `retry_epoch` across recovery wakes. Reset it only after Chrome
control, TikTok page identity, exact account, and one target surface are all
healthy. A superficial tab creation or title load is not health proof.

## One bounded same-Chrome recovery pass

1. Record exact code/status, URL, fresh time, stage, last stable video/query,
   and whether any mutation call may have been issued.
2. Before every mutation, append a unique `MUTATION_INTENT` with an `action_key`
   derived from run ID, stable video ID, lane, and comment parent/top-level
   identity. If that key already exists without a known-safe pre-call abort, do
   not issue it again.
3. For `UNKNOWN_AFTER_TIMEOUT`, append `MUTATION_UNKNOWN`, freeze that exact
   `action_key`, and never reopen the target merely to finish or verify it.
   Independent lanes remain eligible on new posts.
4. Retry the current page/read once after one brief bounded hydration wait.
   Do not immediately repeat the identical failed step on identical evidence.
5. For a stale/closed/missing tab, keep the existing browser binding and create
   a fresh dedicated owned tab. Only an explicit browser-disconnected error
   invalidates the browser binding; reconnect the same Chrome runtime then.
6. Probe TikTok home and one neutral HTTPS site in temporary owned tabs, then
   close those probe tabs. Interpret scope:
   - target failed + TikTok home healthy -> target/route fault; skip or rotate;
   - TikTok failed + neutral healthy -> TikTok/domain/client-filter fault;
   - both failed -> browser/network/proxy/TLS fault;
   - probes themselves unavailable -> browser-control fault.
7. Restore in a fresh owned TikTok tab, re-confirm exact account plus absence of
   a current challenge/warning, and re-read the target identity before work.
   Store expected and observed handles plus the exact proof surface; `UNKNOWN`
   never authorizes a mutation, while one mismatch triggers a fresh-tab recheck
   before `HUMAN_REPAIR_PENDING`.
8. If a read-only interruption broke a watch window, do not add pre-failure and
   post-recovery time. Restart the qualified-view observation window from zero
   and deduplicate the video ID.

Use `schema=mutation_action/v1` with
`event=MUTATION_INTENT|MUTATION_ATTEMPTED|MUTATION_UNKNOWN|MUTATION_HARD_BLOCKED`.
Every result row references its earlier intent through the same `action_key`.

Never claim another task's tab, clear cookies, enter credentials/codes, change
proxy/TLS, bypass login, switch account/browser, or retry an uncertain action.

## Persistent retry across Heartbeats

If one pass does not restore health, the executor writes a valid recovery
record, sends one `round_callback/v1` with `status=ROUND_YIELDED`,
`executor_state=IDLE`, and `recovery_state=RECOVERY_PENDING`, then stops TikTok
work. Preserve the same `round_id`, `round_seq`, accumulated qualified-view
counts, comment/mutation budgets, dedup set, frozen action keys, and resume
cursor. `next_retry_not_before_utc` must be a non-null exact UTC timestamp for
every pending checkpoint.

The main task accepts that callback without treating it as a completed round.
It leaves the same recurring Heartbeat unchanged and the next eligible tick
sends one `resume_mode=RECOVERY_FIRST` assignment for the same round. Use the
stored `next_retry_not_before_utc`; for 429, honor explicit `Retry-After` or
expiry. If 429 has no retry timestamp, scope it to the displayed lane/route,
set the next retry to no earlier than the next 15-minute Heartbeat, and make at
most one probe per due wake; unrelated safe lanes may continue. Early ticks perform no dispatch. Do not create a new executor, new
round, new timer, or reset any budget.

If a persistent login/account mismatch, CAPTCHA/challenge, explicit lock/ban,
credential need, or sole Chrome-control failure proves user action is required,
use `HUMAN_REPAIR_PENDING`. The main asks once with exact evidence and one
repair action. The Heartbeat survives and may dispatch read-only recovery probes
on later due ticks; it never retries mutations while the condition remains.
Repeated unchanged probes stay quiet.

At `operation_stop_at`, send no new TikTok work. Request executor release and
keep the already-configured cleanup wake until `RUN_RELEASED` is proven or the
finite cleanup `UNTIL` arrives. At cleanup expiry, record `RELEASE_UNCERTAIN`,
delete/read back the scheduler, and do not archive or claim tab release without
proof.

## Callback and task-tool uncertainty

- `CALLBACK_DELIVERY_UNKNOWN`: executor stays IDLE, writes the callback bytes and
  hash locally, and does not resend blindly. The next main wake reads canonical
  state or requests status once.
- `DISPATCH_UNCERTAIN`: main does not resend the assignment or consume another
  idle proof until exact acceptance/callback evidence resolves it.
- A transient task read, `notLoaded`, empty result, host error, or tool timeout
  never proves owner absence and never triggers executor replacement.

Ordinary recovery never deletes/pauses the mission Heartbeat, asks the user,
or changes task ownership. Only terminal stop/cutoff cleanup or strict owner/
scheduler repair may alter those resources.
