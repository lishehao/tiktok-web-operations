# User Instruction Precedence

Use this contract whenever a user starts, changes, resumes, intensifies, or
narrows a TikTok mission.

## Operating precedence

Apply inputs in this order:

1. System/developer safety, platform integrity rules, and the real current tool/UI state.
2. The user's latest explicit instruction for the authorized account and actions.
3. The current run registry and active submission certainty.
4. Defaults, heuristics, recovery suggestions, and historical ledger evidence.

The latest explicit instruction replaces conflicting direction, duration,
intensity, action list, search clusters, exclusions, and other old mission
fields. Preserve only fields the user did not replace. Increment the authority
or instruction version before the next dispatch; do not ask the user to confirm
the same values again.

Defaults fill missing fields only. A conservative suggestion, recovery profile,
old capability result, or prior mission must never become a hidden authorization
gate. Ask one question only when an essential field was never supplied and
cannot be safely inferred, or when the requested action would materially expand
the user's authorization.

Thread IDs, account identity, ledger ownership, callback destination, and
submission certainty remain registry/safety facts. A user instruction may
change the operating envelope, but must not be used to guess or bypass those
facts.

Another task using Chrome, TikTok, or the same account is operating context, not
a blocker. Create/use this run's dedicated tab and continue. Concurrent activity
only forces `recommendation_attribution_contaminated=true` and prevents causal
feed claims. Pause only when the same target and action have another in-flight or
uncertain submission; pause that exact mutation, not the whole mission.

## Historical versus current state

Classify every warning, rate limit, failure, or capability result as one of:

- `historical_only` — the event ended and is no longer visible in the current
  page/runtime. Keep it in the ledger for context; do not block launch, reduce
  intensity, demand a recovery mode, or require another confirmation.
- `current_blocker` — the current page or tool explicitly shows the action is
  unavailable, including an active CAPTCHA/challenge, rate limit, lock,
  restriction, login/account mismatch, disabled control, exact tool failure, or
  unresolved submission.

Never promote an old event to `current_blocker` from memory, a previous Thread,
or a prior mission. A past lane failure may justify one fresh persistence gate
per new instruction version when the latest user instruction requests that lane;
it does not permanently disable the lane across missions or proven runtime
changes. Repeating the same instruction does not retry a failure that is still
current; wait for an observable state/runtime change.

## Current blocker handling

When a current blocker exists:

1. Pause only the affected action or lane unless account/submission certainty or
   a platform-wide challenge makes every mutation unsafe.
2. Record exact evidence, the unchanged latest instruction, affected scope, and
   the shortest observable `auto_resume_condition`.
3. Do not reinterpret the mission as a lower-intensity or recovery mission.
4. Do not ask the user to repeat or reconfirm the original instruction.
5. Recheck only through the bounded recovery or one bounded read-only executor
   probe dispatched by the verified coordinator/heartbeat. The heartbeat itself
   never touches Chrome.
6. When the condition visibly clears, account/submission certainty is restored,
   authorization is still active, and time remains, automatically resume the
   original instruction at the next safe mission boundary.

Set `decision_required=true` only when a human action/choice is actually needed:
manual login/challenge resolution, unresolved submission certainty, ambiguous or
expanded authorization, missing rights/disclosure, or another non-inferable
choice. A known wait-and-recheck condition uses `decision_required=false` and
must not be converted into a user confirmation prompt.

The user's instruction never overrides an active platform restriction, an
uncertain submission, system safety, or an action outside the authorized scope.
It controls what to do as soon as the requested action is actually executable.
