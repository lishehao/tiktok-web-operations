# Blocker Minimization

This reference is the single authority for TikTok scope reduction, escalation,
and user-decision routing. Prefer continued safe work over global pause. A
`blocked` status is exceptional; most failures are `no_action`, `skipped`,
`lane_suspended`, or `auto_resume_wait` inside an active mission.

## Decision order

1. Preserve submission certainty and the latest user authorization.
2. Reduce the problem to the smallest exact scope: candidate, page/route,
   action, lane, Chrome activation, or whole account.
3. Try the bounded native recovery allowed by the owning reference.
4. Skip/rotate the exact failed scope and continue all independent safe work.
5. Record a durable checkpoint and `auto_resume_condition`; let a later
   Heartbeat recheck ordinary technical conditions.
6. Escalate to the user only when the user must personally repair the current
   state.

## Non-blocking outcomes

| Evidence | Required result |
|-|-|
| No qualified candidate in the current query | `no_action_checkpoint`; rotate an approved query next cycle |
| Candidate is stale, unsafe, ambiguous, prohibited, or lacks an action control | Skip that candidate/action; do not ask and do not substitute a prohibited route |
| Exact page/route fails while TikTok home or another approved route works | Mark route unavailable; continue through another native approved discovery route |
| Network/DNS/proxy/TLS/renderer/client-block transient | Bounded recovery, then `auto_resume_wait`; keep Heartbeats active and do not ask |
| Chrome control disconnects but the same allowed Chrome can reconnect | Reconnect/bind the same Chrome, create a fresh owned tab, and continue |
| Tool feature is temporarily unavailable but core search/view remains possible | Degrade that feature/lane; continue core mission |
| One persistence gate fails or evidence is temporarily unavailable | Suspend only that action lane; continue search/view and independent verified lanes |
| One mutation is uncertain | Freeze that exact target/action, never resubmit, continue search/view and independent actions |
| Explicit timed rate limit/429 | Preserve displayed retry time, wait through Heartbeat, recheck automatically; no confirmation |
| Rule forbids a route/community/candidate/action | Abandon only that scope; prohibition is not a mission blocker |
| Missing reversible preference such as region/language | Apply documented default, report assumption once, start |

Ordinary recovery success stays in the ledger and next normal three-line receipt.
Do not emit a standalone risk callback, user prompt, or `needs_decision` for it.
An executor may checkpoint at a natural runtime boundary, but this is not a
blocker and does not stop the mission.

## Hard blocker whitelist

Only these current states may stop the whole operating mission and require the
coordinator to ask the user for repair:

1. TikTok is logged out, or the account is mismatched/ambiguous, and the expected
   account cannot be restored without the user.
2. Credentials, OTP, passkey, recovery code, or another user-secret interaction
   is required.
3. A persistent CAPTCHA or verification challenge requires human completion.
4. TikTok explicitly shows the account locked, banned, or unavailable with no
   timed automatic recovery path.
5. The only allowed Chrome control path remains unavailable after its bounded
   reconnect/rebind attempt, so no authorized TikTok read-only work can run.

Explicit user stop, `operation_stop_at`, and objective completion are terminal
conditions, not blockers. They enter the normal release transaction.

Missing mutation permission does not stop the mission: do not perform that
action and continue read-only/authorized lanes. Rights/disclosure ambiguity
stops only the affected publication. An uncertain mutation is not a global hard
blocker unless it also makes account identity or all submission certainty
unrecoverable.

## Callback and reporting policy

- Do not callback for each empty query, skipped candidate, recovered page,
  lane-local failure, or timed wait. Keep these in the ledger.
- Use a coordinator callback when a natural executor yield needs continuation,
  aggregate strategy evidence materially changes, or a hard blocker occurs.
- `decision_required=true` is valid only for the hard whitelist or a materially
  different irreversible action that the user explicitly requested.
- For timed rate limits and other observable waits use
  `decision_required=false` plus the exact retry condition/time.
- Keep the run's coordinator Heartbeat repeat-on. Follow the no-gap replacement contract for
  a genuinely invalid timer.

## Audit checks

- No candidate/route/action/lane event opens a whole-run circuit.
- Empty discovery produces `no_action_checkpoint`, never `blocked`.
- A prohibited method is skipped rather than elevated into a fallback question.
- Technical retry exhaustion yields and auto-resumes; it does not request the
  user to diagnose ordinary networking.
- Hard blockers match the whitelist exactly and contain live evidence.
- Historical failures and conservative suggestions never affect current launch.
