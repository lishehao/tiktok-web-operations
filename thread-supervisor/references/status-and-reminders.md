# Status Queries And Supervisor Reminders

Read this reference only for multi-task research-round synthesis, on-demand
coordinator status, or proactive timed reminders. Ordinary dispatch, callback,
and durable operation timers do not require it.

## Multi-task research rounds

When the user asks to dispatch multiple tasks for one research or design round,
treat those tasks as one round, not as unrelated one-off callbacks.

At dispatch time, track:

- the round objective
- the sibling task IDs
- the acceptance criteria for the round
- which callbacks have returned
- which callbacks are still outstanding

Do not force the user to read one report per sibling task when the work was
clearly a batch research round. When the last sibling task returns, synthesize
the entire round into one cross-task report.

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
tasks mechanically unless the user asks which task produced which evidence.
Prefer the product/project conclusion over per-task summaries.

Still report immediately, before the whole round completes, when any sibling
task returns:

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

After a final round synthesis is acknowledged, remove the sibling tasks from
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

- prefer the product-native task status when it is available; `Needs input` is
  direct evidence that the task requires attention, while an unavailable or
  `notLoaded` read is only uncertainty
- report only unhandled callbacks, decisions, blocks, validation failures, key
  risks, or promised follow-ups
- include active work that is still in progress only when the user explicitly
  asks for all active task status
- avoid repeating acknowledged completed work
- do not include inactive/retired tasks
- keep ownership boundaries strict; for example, a HAOMAI coordinator should not
  include Personal Projects items unless the user explicitly asks for cross-
  coordinator status
- use task as the only reporting unit; project names are details inside a task
  entry, not separate status subjects
- group by task identity and current task state, not by individual assignments,
  callbacks, or historical project names
- never list the same task under multiple groups in one status report, even if
  it has both completed historical assignments and active current work
- group task statuses into `需要你处理`, `在运行`, and `已完成`
- these three groups are mutually exclusive: a task must appear in exactly one
  group at most in a single status response
- assign each task by priority: `需要你处理` > `在运行` > `已完成`
- when a task is running, classify it as `在运行` unless it is
  blocked or waiting for an immediate user decision; summarize completed prior
  completed prior work only as context inside that same task entry if needed
- `需要你处理` includes only items that need the user to make an immediate
  decision or provide input before the task can proceed, plus genuinely
  blocked work, validation failures requiring user choice, and key risks that
  require user direction
- do not put a task under `需要你处理` merely because it is unfinished,
  recently completed, pending acknowledgement, or useful for the user to review
  later; if the worker can continue without the user, classify it elsewhere
- `在运行` includes active delegated tasks still executing work, including
  work that has not yet reported a final result but does not require immediate
  user input
- `已完成` includes newly completed tasks or results that have not yet been
  summarized in the current status response; do not repeat old acknowledged
  completions
- if a completed result is merely available for review but does not require an
  immediate user decision to unblock work, put it under `已完成`, not
  `需要你处理`
- if a running task is also blocked or waiting for a user decision, put it
  only under `需要你处理`, not under `在运行`

If there is no actionable backlog, say that directly and include at most one
short line naming any active worker that is still running.

Recommended shape:

```text
需要你处理:
- Task:
  需要你处理:
  影响:

在运行:
- Task:
  当前状态:

已完成:
- Task:
  结果:
  验证:
```

Omit empty sections. For ordinary short questions, a concise prose answer is
acceptable.

## Supervisor reminders

Timed reminders are optional and should not be the default status mechanism.
Prefer soft-hook callbacks plus on-demand status queries. Create task-attached
scheduled work only when the user explicitly asks for proactive timed reminders
or a target task cannot reliably call back.

In current product language, this is task-attached scheduled work; the tool may
still call it a heartbeat. It returns to the same task and existing context.
Use a standalone scheduled task instead when each run should be independent.

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
未处理信息提醒 - <cadence> - <Coordinator task name> - <run_nonce>
```

Examples:

- `未处理信息提醒 - 30分钟 - Personal Projects Coordinator - a7k2`
- `未处理信息提醒 - 每小时 - HAOMAI Coordinator - p91m`

For the exact unhandled-item rules and compact reminder prompt, read
`references/hourly-reminders.md` only when creating or updating such a heartbeat.
