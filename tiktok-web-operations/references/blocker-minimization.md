# Blocker Minimization

Apply the smallest possible failure scope. Ordinary friction stays in
`TikTok 执行台`; it never returns to the launcher.

## Local outcomes, not mission blockers

| Event | Executor response |
|-|-|
| Empty/weak candidates | `no_action_checkpoint`; rotate an approved cluster next unit |
| Prohibited/ambiguous candidate | skip exact candidate/action |
| Network/DNS/proxy/TLS/render/client block | bounded recovery; if yield is required, verified self-owned one-shot recheck |
| Chrome disconnect/stale tab | reconnect same Chrome or create a new owned tab |
| Feed transition failure | mark held-out validation `partial|unavailable`; continue search |
| Missing persistence/post-action proof | record attempted; do not check; later new-post attempts remain allowed |
| Uncertain mutation | freeze exact target/action; never retry; continue independent work |
| Explicit timed rate limit | preserve retry time and auto-recheck; no confirmation |
| Malformed ledger append | bounded local repair, then checkpoint/self-resume |

Do not create a user question, callback, global pause, or task replacement for
these events. Do not alter an already verified pending one-shot wake.

## Hard blocker whitelist

Ask the user directly in `TikTok 执行台` only when current evidence proves the
user must act:

- persistent login/logout or account mismatch after bounded same-Chrome recheck;
- persistent CAPTCHA/verification challenge requiring human completion;
- explicit account lock, suspension, or ban;
- credential/code requirement;
- the sole allowed Chrome control path remains unavailable after bounded repair.

Report exact evidence, affected scope, attempts, likely cause as a possibility,
and one concrete user repair action. Use a one-shot recovery wake only when an
automatic timed recheck is appropriate; otherwise wait for the user in this
executor. Historical events never satisfy this whitelist.

User stop, deadline, and completed objective are terminal conditions, not
blockers; finalize normally.
