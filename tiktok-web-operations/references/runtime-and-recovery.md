# Runtime And Recovery

Recover inside the executor's bounded round, owned Chrome tab, and ledger. When
the round ends or user action is required, callback the exact registered main
task. Never contact an unrelated TikTok task.

## Error classes

| Class | Evidence examples | Possible cause wording |
|-|-|-|
| binding/browser | stale tab, browser disconnected | Chrome control binding changed |
| DNS/network | `ERR_NAME_NOT_RESOLVED`, `ERR_INTERNET_DISCONNECTED`, `ERR_NETWORK_CHANGED`, `ERR_CONNECTION_TIMED_OUT/RESET/CLOSED` | DNS, connectivity, VPN/proxy, or local security interruption |
| proxy/TLS | `ERR_PROXY_CONNECTION_FAILED`, `ERR_TUNNEL_CONNECTION_FAILED`, `ERR_CERT_*` | proxy tunnel or certificate path |
| HTTP | 429, 403, 5xx | platform limit/access/service response |
| client block | `ERR_BLOCKED_BY_CLIENT` | extension or local filtering rule |
| render | blank/loading/script error without code | page rendering or script failure |

Never assert a root cause from one symptom. Report `likely_cause` as `可能原因`
only after exact code and same-domain/neutral probes.

## Bounded same-Chrome recovery

1. Record exact code/status, URL, time, stage, and whether a mutation was
   submitted or uncertain.
2. If submission is uncertain, freeze that exact target/action and never retry.
3. Wait briefly and retry the current page once.
4. If binding is stale/disconnected, reconnect the same Chrome and create a new
   dedicated owned tab when needed. Never claim another task's tab.
5. Probe TikTok home and one neutral HTTPS site in temporary owned tabs.
6. Reconfirm exact account, target, warnings, and lane state before continuing.
7. If recovered, continue the bounded round. If still transient and the round
   must yield, checkpoint `auto_resume_condition`, callback the exact main task,
   and become idle. The executor never creates a recovery timer.

Never switch browser, clear cookies, enter credentials/codes, change proxy/TLS,
bypass login, or repeat an uncertain mutation.

## Recovery routing

- Candidate/page/route faults: skip or rotate.
- Network/Chrome/render faults: bounded retry then callback checkpoint when the round must yield.
- Feed movement failure: end only held-out validation.
- Missing persistence/post-action proof: record attempted and continue; do not
  run verification or suspend future new-post attempts.
- Timed 429/rate limit: preserve expiry and auto-recheck.
- Current human-only blocker: preserve/release the owned tab safely, callback
  exact evidence, and let the main task ask the user.

No ordinary recovery creates a replacement task, asks the user, or alters the
main scheduler.

## Scheduler and resumption

Only the main mission recurring Heartbeat wakes for scheduled resumption. It
validates exact automation, main/run IDs, current machine time, accepted
callback-IDLE proof, pending round, and cutoff. It sends one new assignment when
due. A live executor task read is diagnostic and cannot negate accepted IDLE
proof merely by being unavailable, empty, or `notLoaded`. A wrong, early,
duplicate, active-executor, or overlapping tick performs no dispatch and leaves
the same repeat-on schedule intact. Before cutoff every scheduler turn reads
back a future next run plus cleanup `UNTIL`; it never depends on `COUNT=1` or
self-rearming after the current wake.
