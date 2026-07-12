---
name: thread-supervisor
description: Use when Codex needs to coordinate, supervise, rename, pin, archive, continue, or collect results from background Codex threads. Applies to multi-thread project management, soft-hook callbacks with send_message_to_thread, heartbeat fallbacks, pending-result reminders, and deciding when to stop monitoring.
---

# Thread Supervisor

Coordinate background Codex threads from the current thread.

## Operating model

- Treat the current thread as the user's coordinator.
- Watch only threads the user explicitly dispatched or asked to supervise.
- Stop watching a thread when it completes, becomes irrelevant, or its result is acknowledged.
- Do not monitor historical threads just because they contain useful context.
- Do not modify project files from a supervisor heartbeat.
- Do not send new work to a target thread unless the current user explicitly asks
  or an active standing operation envelope explicitly authorizes another bounded
  round. Never broaden that envelope from a worker result.

## Prefer soft hooks

Use a callback instead of polling whenever practical.

## Dispatch contract

Every delegated task should include a completion callback instruction whenever
`send_message_to_thread` is available to the target thread. The callback should
return to the coordinator thread, not just finish in the worker thread.

Before relying on a target thread for callbacks, run a short callback capability
check unless that exact thread has already proven it can call back in the
current management session.

Before reusing any persistent worker, apply the owner-liveness gate in
`references/identity-and-automation.md`. List/search/title/summary/readability
only discovers a candidate; it does not prove a writable rollout.

Include these fields in the dispatch prompt:

- the coordinator thread id
- the target project or task name
- the expected final report shape
- the instruction to call `send_message_to_thread` when the task is completed,
  blocked, validation fails, a user decision is needed, or a key risk appears

If the target thread cannot call `send_message_to_thread`, say so in the
coordinator thread, mark that target as polling-only, and use the heartbeat
fallback below. Do not keep asking a polling-only target to call back unless a
new tool surface becomes available or the thread is recreated.

When dispatching work, give the target thread:

- the coordinator thread id
- the expected final report shape
- the instruction to call `send_message_to_thread` only for completion, block, validation failure, user decision, or key risk

Treat model, reasoning effort, service tier, and host as an opaque
`execution_profile`. This Skill has no default model or reasoning effort. If the
user or calling domain Skill supplied an explicit profile, copy supported fields
exactly into thread creation and operational dispatches. If no profile was
supplied, omit overrides and preserve the target's configured settings. Never
invent a fallback or silently strengthen, weaken, or substitute a model.

## Persistent coordinator/executor pair

Use this reusable topology when one user-visible task must supervise one
user-visible execution task over bounded rounds or one continuous resumable
mission, as declared by the calling domain:

```text
starter task becomes coordinator
  -> creates one persistent executor with create_thread
  -> first real work runs immediately and is proven
  -> executor checkpoints/callbacks at the calling domain's declared boundaries
  -> continuation follows the calling domain's declared scheduler topology
```

Keep each role single-purpose:

```text
Coordinator objective: advance or stop the authorized run at the correct time,
and own every user decision.

Executor objective: execute exactly one accepted mission. A bounded-round domain
ends after one round; a continuous domain keeps advancing until a natural
runtime yield, blocker, or cutoff, then checkpoints, releases the external
resource, callbacks, and becomes resumable.
```

Treat strategy, policy, account, direction, capability matrix, deadline, and
reporting schema as inputs or constraints, not additional worker missions. If a
prompt gives either role multiple independent goals, rewrite it into this role
card plus a bounded input contract before dispatch.

Require the calling domain to declare one authoritative role-and-stage contract:
each role has one objective plus explicit `owns`, `reads`, `writes`, `outputs`,
and `never` fields; each stage has one active owner, entry condition, exit proof,
and next state. A bootstrap role may transition into the coordinator only after
releasing any external resource the coordinator is forbidden to own. Heartbeats
are wake signals, never extra roles or stage-completion proof. Thread Supervisor
enforces that contract but does not restate or broaden it.

- Keep the starter task as coordinator when it can prove its own exact Thread ID.
  Use the temporary nonce registration title in
  `references/identity-and-automation.md`, resolve the exact matching task with
  `list_threads`, confirm it with `read_thread`, record the returned ID, then set
  the caller-supplied `coordinator_title` (generic default `主控台`). Record the
  executor ID returned by `create_thread` before setting the caller-supplied
  `executor_title` (generic default `执行器`). Do not guess an ID from a final
  title, directory name, stale prompt, or previous run.
- Treat title, pin, and archive as presentation/lifecycle fields in the registry.
  Apply the calling domain's policy only after exact task identity is verified;
  none of these fields proves ownership.
- Create the executor with `create_thread`; never substitute `spawn_agent`, a
  collaboration subagent, Goal Mode, or an agent tree when the contract requires
  a persistent sidebar task.
- Use the two-phase canonical protocol in
  `references/canonical-registry.md`: one inert bootstrap envelope before
  creation, then one finalized identity registry after the executor ID exists.
  `SELF_REGISTRY` sends the stored canonical bytes once; later dispatches and
  callbacks carry hashes/references rather than retyped registry prose.
- Treat self-registration failure as a bootstrap blocker. Do not create a second
  coordinator merely to work around an unknown starter-task ID unless the user
  explicitly selects that alternate topology.
- Let the coordinator own user conversation, strategy, pending work, and
  lifecycle. Let the executor own the external system and raw evidence. Never
  let both operate the same mutable surface.
- Make the coordinator the only user-facing decision surface. A worker that
  encounters a block, validation failure, decision need, key risk, uncertain
  external action, or terminal event must checkpoint and callback the
  coordinator. Stop the affected scope; a continuous domain may keep explicitly
  independent safe lanes running under its accepted policy. It must not ask the
  user to decide inside the worker Thread, expand recovery authority, or scatter
  risk handling across tasks.
- Amortize callback overhead with meaningful boundaries. Routine per-item
  progress stays in the ledger. For a continuous domain, logical content units
  do not force a callback; callback at a natural turn/runtime yield, blocker,
  material checkpoint required by the domain, or terminal event.
- Distinguish round completion, resource release, and whole-run completion.
  When the overall run ends, require one terminal executor callback proving
  release and final evidence before the coordinator marks `RUN_COMPLETED`.
  Heartbeat completion alone is never run completion.

The calling domain Skill owns what a round means, which actions are authorized,
how evidence is validated, and whether timed continuation uses coordinator ticks
or coordinator-managed worker ticks. Thread Supervisor owns only registration,
dispatch, callback, work state, heartbeat mechanics, stop/release, and archival.
Before creating a persistent pair or any heartbeat, read
`references/canonical-registry.md` and
`references/identity-and-automation.md`; enforce canonical identity separately
from versioned direction/authority/mission objects and mutable runtime state.

Callback shape:

```text
Project:
Status: completed | blocked | validation_failed | needs_decision | key_risk
Callback scope: block | run_terminal
Terminal event: none | executor_released
Release state: none | stopped_and_released | release_unverified
Changed:
Validation:
Risks:
Decision needed:
Decision owner: coordinator
```

After a callback:

- read the callback first
- optionally read the target thread's latest 1-3 turns
- apply the calling domain's scope-minimization policy before accepting a
  worker's status label. Reclassify empty candidates, prohibited/local routes,
  recovered technical faults, missing optional evidence, and single-action/lane
  failures as normal local outcomes when the domain says safe work continues;
  do not manufacture a global block or user decision from an over-elevated
  worker callback
- for `completed` with no user decision, report or dispatch the next authorized
  step normally
- for `blocked`, `validation_failed`, `needs_decision`, or `key_risk`, pause the
  smallest affected scope and respect the calling domain's `decision_required` field. If
  true, consolidate the risk, affected scope, safe stopped state,
  recommendation, and at most three choices into one coordinator message. If
  false, keep the original authorization and exact external resume condition;
  do not manufacture a user confirmation or recovery-tier choice
- resume only after the user decides in the coordinator or a verifiable
  external-state change clears the blocker
- remove a target from the active watchlist only when its whole run is terminal
  or the calling domain retires it. A bounded-round completion or continuous-
  mission checkpoint does not remove the persistent executor.

For a persistent coordinator/executor run, ordinary `completed` or a mission
checkpoint means only that recoverable progress was recorded. At deadline,
user stop, or objective completion,
follow the whole-run transaction in `references/identity-and-automation.md`:
stop dispatch, obtain `EXECUTOR_RELEASED`, retire the exact managed heartbeat(s), reconcile
the final ledger, then mark `RUN_COMPLETED`. If release proof is missing, use
`RUN_FINALIZATION_BLOCKED` and do not tell the user the run completed.

## Dispatch pacing

Do not interrupt a worker thread with unrelated new work while it is actively
executing. Prefer callback-driven sequencing:

- if the worker is in progress, queue the next unrelated task in the
  coordinator's plan or pending ledger instead of sending it immediately
- send a new task after the worker calls back, completes, blocks, or asks for a
  decision
- mid-run follow-up is allowed only when it is highly related to the current
  task, overrides the current task, fixes acceptance criteria, or prevents
  wasted work
- if sending a mid-run follow-up, state explicitly that it is an amendment to
  the current task, not a new unrelated task
- avoid using thread messages as a to-do list while the target is busy; keep
  coordinator-side pending tasks until the target is ready

If the target cannot call back, say so and use a low-frequency heartbeat fallback.

## Work-state control

As supervisor, maintain a lightweight working-state ledger for each active
target thread before deciding whether to send a new instruction:

- `idle_or_done`: no active work is known, or the latest callback completed.
- `running_current_task`: a worker is executing the latest dispatched task and
  has not called back.
- `blocked_or_waiting`: the worker reported blocked, validation failed, key
  risk, or needs a decision.
- `pending_next`: the user requested a next task that should wait for the
  worker's current callback.

When the user gives a follow-up while a worker is running, classify it before
sending anything:

- **Interrupt/amend immediately** when the follow-up changes, corrects, narrows,
  or overrides the worker's current task or acceptance criteria. Send it as an
  explicit amendment to the current task so the worker can avoid wasted work.
- **Queue until callback** when the follow-up is a next direction, extra polish,
  broader continuation, or a new task that can start after the current work is
  complete. Do not interrupt the worker just to add this to-do item; record it
  in the coordinator state and dispatch it after the callback.
- **Ask or state the tradeoff** only when it is genuinely ambiguous whether the
  user means to alter the active run or start a later task, and the wrong choice
  would waste material work.

Default rule: corrections to the active work interrupt; extensions after the
active work wait. This protects worker output quality by avoiding unrelated
mid-run context changes.

## Long-running goal-mode dispatch

When the current coordinator thread is inside a long-running goal-mode loop and
the next useful work belongs in a delegated target thread, dispatch the work and
then stop active waiting in the coordinator. Do not keep spending coordinator
turns polling, re-summarizing, or trying to complete the delegated work locally.

Use this pattern when all of these are true:

- the user wants a multi-iteration objective or "goal mode" supervision
- a target thread can do the next concrete step
- the target thread has a soft-hook callback path, or a heartbeat fallback is
  configured
- no immediate user decision is needed before the worker can proceed

Coordinator behavior:

- send one clear dispatch with acceptance criteria, callback shape, and model /
  thinking overrides when requested
- mark the target as `running_current_task` in the coordinator state or pending
  ledger
- create or update a heartbeat fallback if the user requested one, if callbacks
  are unproven, or if the goal loop is expected to run unattended
- then stop the coordinator turn with a short report saying the task was
  dispatched and the next action will be driven by callback or heartbeat
- do not mark the goal complete merely because the dispatch was sent
- do not mark the goal blocked while the worker is still expected to call back

The worker callback, a user interruption, or a heartbeat should drive the next
iteration. This is intentional: a coordinator in goal mode should supervise the
loop, not busy-wait inside it.

For iterative design/review loops, define the loop contract up front:

- target iteration count or stopping criteria
- worker role for production work
- reviewer/playtester roles for acceptance feedback
- minimum evidence per loop
- which failures require user decision vs automatic next-iteration dispatch
- rule that each next iteration starts only after the previous callback or
  review result is received

## Heartbeat and durable timer

Use heartbeat automation when soft hooks are unavailable or unreliable, the
user wants proactive reminders, or a domain Skill defines a multi-round timed
operation that needs a durable clock.

For a time-bounded operation, use the topology declared by the calling domain:

- `coordinator_tick`: one coordinator-target durable timer;
- `coordinator_managed_worker_tick`: one repeat-on operation heartbeat targeting
  the executor plus one lower-frequency repeat-on supervisor heartbeat targeting
  the coordinator.

Callbacks mean “an event arrived”; a heartbeat means “a continuation/recovery or
supervision time arrived.” Keep one logical automation per declared role, never
one per content unit or block. A recurring worker operation must have `repeat=on`
plus finite `UNTIL` or equivalent `operation_stop_at`; `COUNT=1` followed by
worker self-renewal is invalid.

Create, update, pause, or delete every run heartbeat only from the verified
coordinator/manager. The target may be the coordinator or exact executor as
declared, but the executor never manages an automation. Immediately view every
created automation and verify exact ID, target, repeat state, next run, local/UTC
schedule, and cutoff. On mismatch follow
`references/identity-and-automation.md` and take no external action.

Heartbeat automations are stable mechanisms and recovery carriers, not project
status documents.
Do not update a heartbeat just because a worker completed, a decision list changed,
or a brief was refreshed. Put dynamic state in the coordinator thread, a management
brief, or the user-facing report.

Update an existing heartbeat only when one of these changes:

- active watchlist membership
- reminder cadence
- management or target boundary
- notification rules
- target Thread or bounded operation template

On a coordinator/supervisor heartbeat:

- read only active target threads, usually latest 1-3 turns
- notify only for completion, block, validation pass/fail, user decision, key risk, or major scope change
- stay silent for ordinary progress
- adjust cadence by expected usefulness:
  - 5-7 minutes for validation or near-completion
  - 15-30 minutes for normal implementation
  - 30-60 minutes for long-running or low-risk tracking
- retire a run automation only when its domain declares the run terminal and
  verifies external-resource release; ordinary reminder-only automations may be
  deleted when no active thread or unacknowledged result remains

A calling domain may set `heartbeat_receipt_policy=always_three_lines`. In that
case, do not stay silent on healthy ticks. First update/reuse and read back the
exact managed run heartbeat(s), then report exactly:

```text
本轮完成：<one sentence>
下次心跳：<verified local date, time, and timezone>
下轮计划：<one bounded purpose>
```

If no next tick exists, say why in the second line. Never announce an inferred
schedule before automation readback. Keep generic reminder heartbeats on the
default `silent_unless_event` policy unless the user/domain explicitly opts in.

For durable timed operation:

- verify manager, target, role, run ID, automation ID, repeat state, current
  time, next run, and stop time;
- in bounded-round topology, the executor-target wake executes at most one
  deterministic round; in continuous-resumable topology, it resumes the same
  accepted mission from the latest durable checkpoint when idle/yielded and does
  no overlapping work when already running;
- the coordinator-target supervisor wake reads the executor's new turn,
  callback, proof, and either bounded-round slot state or continuous-mission
  progress/resume state; it never operates the external system;
- if the executor is already running, do not overlap it. If one mutation is
  uncertain, freeze that exact action/lane but preserve unaffected work as the
  domain permits;
- missing repeat state, missing wake/new turn, missing proof, or broken next run
  is `SCHEDULER_CONTINUATION_FAILURE` and must be surfaced by the coordinator;
- ordinary page/network/Chrome/route/client-block/lane failures never pause or
  delete a correctly bound Heartbeat. Preserve repeat-on state and let a later
  wake recheck the exact auto-resume condition without asking whether to retry;
- user mission changes update canonical state and the same operation Heartbeat
  only when its stable template/cadence/target/cutoff changes. Stop/completion
  retires all exact run Heartbeats only after terminal executor release proof.

Reaching the final scheduled tick starts the stop/release transaction; it does
not complete it.

### One-time first-run supervision window

When a calling domain Skill explicitly requires first-install monitoring, let
the verified coordinator own one low-frequency, time-bounded watch window. This
is not a recurring default:

- require a durable state marker outside the managed Skill tree with
  `PENDING | ACTIVE | CONSUMED | DEGRADED`;
- activate only on the first real run after a true first install, after the
  coordinator/executor identity handshake and initial proof;
- use sparse checkpoints such as cumulative `+15`, `+35`, and `+60` minutes,
  capped by the operation stop time, rather than keeping a turn open or polling;
- at each checkpoint read only the registered worker's latest relevant turns,
  callbacks, and ledger state; never touch the external system or interrupt a
  running worker;
- stay silent when healthy; centralize any block, validation failure, decision,
  or key risk in the coordinator;
- persist the supervision overlay as `CONSUMED` at its final checkpoint, early
  user stop, or run end. When a domain uses a dedicated supervisor heartbeat,
  reuse that heartbeat for this overlay and keep all run heartbeats through
  terminal executor release; retire them only in whole-run
  finalization; never recreate the first-run overlay on later missions.

If automation support is unavailable, mark the one-time window `DEGRADED`, keep
callback-only supervision, disclose the limitation once in the coordinator,
and still consume the marker. Do not retry it on every later mission.

## Result reminders

- If an important result has not been acknowledged, keep a reminder.
- Stop reminding when the user replies with an acknowledgement or follow-up instruction.
- `已读`, `收到`, `看到了`, or a new related task counts as acknowledgement.
- Acknowledgement is not permission for external API calls; ask explicitly before external data/model use.

## Pending ledger

Maintain an accumulating pending ledger for unhandled callbacks and decisions.

When any hook/callback wakes the coordinator:

- first check whether older pending items are still unhandled
- report older pending items before the new callback
- then report the new callback or decision
- keep all unhandled items in the ledger until the user acknowledges, decides, or gives a related follow-up

Do not treat a callback as handled merely because it was reported once. If the
user ignores it, keep reminding on later hook-triggered reports or hourly
reminders.

Store dynamic pending state in the coordinator thread, a management brief, or a
short ledger file if the coordinator already uses one. Do not store the live
pending list in the heartbeat automation prompt.

Recommended report shape when both old and new items exist:

```text
未处理积压:
- Thread:
  需要你处理:

本次新增:
- Thread:
  Status:
  需要你处理:
```

## Advanced reporting and reminders

Read `references/status-and-reminders.md` only when the user asks for an
on-demand coordinator status report, multi-thread research-round synthesis, or
proactive timed reminders. Ordinary dispatch/callback supervision and durable
operation timers do not require that reference.

## Useful tools

Discover tools first when they are not already available:

- `read_thread`: inspect a target thread
- `send_message_to_thread`: dispatch work or request a soft-hook callback
- `list_threads`: find a thread when id/title is unknown
- `set_thread_title`: rename a thread
- `set_thread_pinned`: pin or unpin
- `set_thread_archived`: archive or unarchive
- `automation_update`: create, update, or delete heartbeat fallbacks

## Reporting

Keep user reports short and segmented:

```text
Thread name - status
Completed:
Validation:
Risk:
Next:
```

For completed work, include slightly more detail: what changed, what was verified, remaining risk, and what decision is needed.
