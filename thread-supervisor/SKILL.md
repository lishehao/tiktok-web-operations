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
user-visible execution task over multiple bounded rounds:

```text
starter task becomes coordinator
  -> creates one persistent executor with create_thread
  -> executor completes one bounded round
  -> executor callbacks coordinator
  -> coordinator reconciles and dispatches at most one next round
```

- Keep the starter task as coordinator when it can prove its own exact Thread ID.
  Use the temporary nonce registration title in
  `references/identity-and-automation.md`, resolve the exact matching task with
  `list_threads`, confirm it with `read_thread`, record the returned ID, then set
  the final title to `主控台`. Record the executor ID returned by `create_thread`
  before setting its final title to `执行器`. Do not guess an ID from a final
  title, directory name, stale prompt, or previous run.
- Create the executor with `create_thread`; never substitute `spawn_agent`, a
  collaboration subagent, Goal Mode, or an agent tree when the contract requires
  a persistent sidebar task.
- Pass the exact coordinator ID, returned executor ID, execution profile,
  authority envelope, ledger, stop conditions, and callback schema through a
  `SELF_REGISTRY` handshake before the executor performs external work.
- Treat self-registration failure as a bootstrap blocker. Do not create a second
  coordinator merely to work around an unknown starter-task ID unless the user
  explicitly selects that alternate topology.
- Let the coordinator own user conversation, strategy, pending work, and
  lifecycle. Let the executor own the external system and raw evidence. Never
  let both operate the same mutable surface.
- Make the coordinator the only user-facing decision surface. A worker that
  encounters a block, validation failure, decision need, key risk, uncertain
  external action, or terminal event must callback the coordinator, stop its
  current work, and become idle. It must not ask the user to decide inside the
  worker Thread, self-authorize recovery, or scatter risk handling across tasks.
- Amortize callback overhead with meaningful bounded rounds. Routine per-item
  progress stays in the ledger; callback only at round completion or on a
  terminal event.

The calling domain Skill owns what a round means, which actions are authorized,
and how evidence is validated. Thread Supervisor owns only registration,
dispatch, callback, work state, heartbeat fallback, stop/release, and archival.
Before creating a persistent pair or any heartbeat, read
`references/identity-and-automation.md` and enforce its immutable run registry.

Callback shape:

```text
Project:
Status: completed | blocked | validation_failed | needs_decision | key_risk
Changed:
Validation:
Risks:
Decision needed:
Decision owner: coordinator
```

After a callback:

- read the callback first
- optionally read the target thread's latest 1-3 turns
- for `completed` with no user decision, report or dispatch the next authorized
  step normally
- for `blocked`, `validation_failed`, `needs_decision`, or `key_risk`, do not
  dispatch again; consolidate the risk, affected scope, safe stopped state,
  recommendation, and at most three choices into one coordinator message
- resume only after the user decides in the coordinator or a verifiable
  external-state change clears the blocker
- remove completed threads from the active watchlist

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

## Heartbeat fallback

Use heartbeat automation only when soft hooks are unavailable, unreliable, or the user wants proactive reminders.

Create, update, fire, pause, or delete a heartbeat only from its verified owner
coordinator. Require
`automation_owner_thread_id == targetThreadId == coordinator_thread_id`, pass
the exact `targetThreadId` when supported, then view the returned automation ID
and verify its binding. The executor and unrelated bootstrap, Skill-development,
or sibling Threads never own or manage the coordinator's heartbeat. On any
mismatch, follow `references/identity-and-automation.md` and take no external
action.

Heartbeat automations are stable mechanisms, not project status documents.
Do not update a heartbeat just because a worker completed, a decision list changed,
or a brief was refreshed. Put dynamic state in the coordinator thread, a management
brief, or the user-facing report.

Update an existing heartbeat only when one of these changes:

- active watchlist membership
- reminder cadence
- ownership boundary
- notification rules
- target coordinator thread

On heartbeat:

- read only active target threads, usually latest 1-3 turns
- notify only for completion, block, validation pass/fail, user decision, key risk, or major scope change
- stay silent for ordinary progress
- adjust cadence by expected usefulness:
  - 5-7 minutes for validation or near-completion
  - 15-30 minutes for normal implementation
  - 30-60 minutes for long-running or low-risk tracking
- delete the automation when no active thread or unacknowledged result remains

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

## Multi-thread research rounds

When the user asks to dispatch multiple threads for one research or design
round, treat those threads as one round, not as unrelated one-off callbacks.

At dispatch time, track:

- the round objective
- the sibling thread ids
- the acceptance criteria for the round
- which callbacks have returned
- which callbacks are still outstanding

Do not force the user to read one report per sibling thread when the task was
clearly a batch research round. When the last sibling thread returns, synthesize
the entire round into one cross-thread report.

Default final round report:

```text
这轮最终结论:
- 

被验证的判断:
- 

被推翻或需要降级的判断:
- 

可以沉淀进 PRD / artifact 的内容:
- 

还需要用户拍板:
- 

建议下一步:
- 
```

Use the final round report to reconcile conflicts between workers. Do not list
threads mechanically unless the user asks which thread produced which evidence.
Prefer the product/project conclusion over per-thread summaries.

Still report immediately, before the whole round completes, when any sibling
thread returns:

- `blocked`
- `validation_failed`
- `needs_decision`
- `key_risk`
- a finding that would make the remaining sibling work materially wasteful

If a user asks for status while a round is incomplete, report the round state
compactly:

- returned count / total count
- any urgent blockers or decisions
- whether the coordinator is still waiting for the final synthesis

After a final round synthesis is acknowledged, remove the sibling threads from
the active watchlist unless the user explicitly asks to continue them.

## On-demand status queries

When the user asks for coordinator status, treat it as a pending-ledger query by
default, not as a broad project summary.

Trigger phrases include:

- `告诉我下状态`
- `现在什么状态`
- `还有什么积压`
- `有哪些未处理`
- `哪些需要我处理`
- `status`

Default answer:

- report only unhandled callbacks, decisions, blocks, validation failures, key
  risks, or promised follow-ups
- include active work that is still in progress only when the user explicitly
  asks for all active thread status
- avoid repeating acknowledged completed work
- do not include inactive/retired threads
- keep ownership boundaries strict; for example, a HAOMAI coordinator should not
  include Personal Projects items unless the user explicitly asks for cross-
  coordinator status
- use thread as the only reporting unit; task/project names are details inside
  a thread entry, not separate status subjects
- group by thread identity and current thread state, not by individual tasks,
  callbacks, or historical project names
- never list the same thread under multiple groups in one status report, even
  if that thread has both completed historical tasks and an active current task
- group thread statuses into `需要你处理`, `在运行`, and `已完成`
- these three groups are mutually exclusive: a thread must appear in exactly one
  group at most in a single status response
- assign each thread by priority: `需要你处理` > `在运行` > `已完成`
- when a thread has a running task, classify the thread as `在运行` unless it is
  blocked or waiting for an immediate user decision; summarize completed prior
  tasks only as context inside that same thread entry if needed
- `需要你处理` includes only items that need the user to make an immediate
  decision or provide input before the thread can proceed, plus genuinely
  blocked work, validation failures requiring user choice, and key risks that
  require user direction
- do not put a thread under `需要你处理` merely because it is unfinished,
  recently completed, pending acknowledgement, or useful for the user to review
  later; if the worker can continue without the user, classify it elsewhere
- `在运行` includes active delegated threads still executing work, including
  work that has not yet reported a final result but does not require immediate
  user input
- `已完成` includes newly completed threads or results that have not yet been
  summarized in the current status response; do not repeat old acknowledged
  completions
- if a completed result is merely available for review but does not require an
  immediate user decision to unblock work, put it under `已完成`, not
  `需要你处理`
- if a running thread is also blocked or waiting for a user decision, put it
  only under `需要你处理`, not under `在运行`

If there is no actionable backlog, say that directly and include at most one
short line naming any active worker that is still running.

Recommended shape:

```text
需要你处理:
- Thread:
  需要你处理:
  影响:

在运行:
- Thread:
  当前状态:

已完成:
- Thread:
  结果:
  验证:
```

Omit empty sections. For ordinary short questions, a concise prose answer is
acceptable.

## Supervisor reminders

Timed reminders are optional and should not be the default status mechanism.
Prefer soft-hook callbacks plus on-demand status queries. Create a thread
heartbeat only when the user explicitly asks for proactive timed reminders or a
target thread cannot reliably call back.

When the user wants an active coordinator to stay useful while they are present,
the heartbeat checks on the requested cadence for unhandled callbacks,
decisions, blocks, validation failures, and key risks. Use 30 minutes for
long-running goal-mode delegation when the user asks for a half-hour heartbeat;
use one hour for lower-touch reminder loops. Keep it scoped to the current
active watchlist, stay silent when there is nothing actionable, and update an
existing matching heartbeat instead of creating duplicates only when the
heartbeat mechanism itself must change. Do not rewrite the heartbeat prompt to
mirror each new callback or current decision list.

Name reminder automations consistently and include the owning run nonce:

```text
未处理信息提醒 - <cadence> - <Coordinator thread name> - <run_nonce>
```

Examples:

- `未处理信息提醒 - 30分钟 - Personal Projects Coordinator - a7k2`
- `未处理信息提醒 - 每小时 - HAOMAI Coordinator - p91m`

For the exact unhandled-item rules and compact reminder prompt, read
`references/hourly-reminders.md` only when creating or updating such a heartbeat.

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
