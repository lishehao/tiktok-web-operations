# Runtime And Recovery

Recover inside the executor's own task, Chrome tab, ledger, and self Heartbeat.
Do not contact the launcher or another TikTok task.

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
7. If recovered, continue and mention it only in the next normal three-line
   receipt. If still transient, checkpoint `auto_resume_condition` and let the
   self Heartbeat retry later.

Never switch browser, clear cookies, enter credentials/codes, change proxy/TLS,
bypass login, or repeat an uncertain mutation.

## Recovery routing

- Candidate/page/route faults: skip or rotate.
- Network/Chrome/render faults: bounded retry then self-resume checkpoint.
- Feed movement failure: end only held-out validation.
- Missing persistence/post-action proof: record attempted and continue; do not
  run verification or suspend future new-post attempts.
- Timed 429/rate limit: preserve expiry and auto-recheck.
- Current human-only blocker: release owned tab and ask directly in executor.

No ordinary recovery deletes the Heartbeat, changes the launcher, creates a
replacement task, or waits for user confirmation.

## Executor wake

Validate exact automation ID, run ID, executor ID, target, repeat state, next
run, and cutoff. If already running, do no overlapping work. If idle before
cutoff, resume from the last valid JSONL checkpoint. If the timer is wrong,
replace it without a gap as specified in `stability-and-circuit-breakers.md`.
