# Supervisor Reminders

Use only when creating or updating task-attached scheduled work (called a
heartbeat by the current tool) for unhandled supervisor items.

## Before creating

- Read `identity-and-automation.md` and prove the current task is the exact
  registered coordinator and automation owner.
- Inspect existing automations first.
- Reuse/update a matching heartbeat only when its viewed `targetThreadId`, run
  ID, purpose, coordinator, and accepted canonical reference match the current
  run state.
- If an existing heartbeat belongs to another project group, create a separate one.
- Pass explicit `targetThreadId=coordinator_thread_id`, view the returned
  automation ID, and verify the stored binding before treating creation as
  successful.
- Use the fixed name format `未处理信息提醒 - <cadence> - <Coordinator task name> - <run_nonce>`.
- If an older matching heartbeat uses a different name, rename it instead of
  creating a duplicate.

Never create or update a heartbeat from an executor, installer,
Skill-development task, sibling coordinator, or any task that cannot prove it
is the registered owner. Never retarget another task's automation.

## Stable mechanism vs dynamic state

The heartbeat is a stable reminder mechanism. It should answer:

- which coordinator, task ID, automation ID, and run ID own this reminder
- which active watchlist it may inspect
- what events are worth interrupting the user for
- when it should stay silent

It should not become the live project brief. Do not update the automation merely
because:

- a worker completed
- a callback was acknowledged
- a decision list changed
- a management brief changed
- a current project status line became stale

Put those facts in the coordinator task, management brief, or the next user
report. Update the automation only when the watchlist, cadence, ownership
boundary, notification rules, or target coordinator task changes.

## "Unhandled" means

- completed callback not yet acknowledged
- `needs_decision`, `blocked`, `validation_failed`, or `key_risk`
- active watched task stalled and requiring user decision
- promised follow-up dispatch not yet sent

Do not report ordinary progress, acknowledged results, inactive context hubs, or retired tasks.

## Pending ledger behavior

Unhandled items accumulate. A callback is not considered handled just because it
was shown to the user once.

On every hook-triggered report or hourly reminder:

- include still-unhandled older items first
- include the newly arrived callback or decision second
- remove an item only after the user acknowledges, decides, or gives a related
  follow-up instruction

Keep the ledger in coordinator state, a management brief, or a short ledger file
if one already exists. Do not mirror the live ledger into the automation prompt.

## Heartbeat prompt requirements

- Include immutable `run_id`, coordinator ID, executor/watchlist IDs,
  automation ID when available, and a no-action rule for identity mismatch.
- Check only the coordinator's current active watchlist.
- Read recent callbacks or latest 1-3 turns per active target.
- Stay silent if nothing is actionable unless the user explicitly asks for all-clear messages.
- Treat `已读`, `收到`, `看到了`, or a related follow-up as acknowledgement.
- Do not treat acknowledgement as approval for external APIs, authenticated browsing, production changes, or model spend.
- Avoid embedding detailed current-state lines such as "Task X is waiting for Y"
  unless they are stable ownership boundaries. Dynamic pending items should be
  discovered from callbacks, the management brief, or the coordinator's recent
  turns at heartbeat runtime.

On wakeup, first verify
`waking_thread_id == targetThreadId == coordinator_thread_id` and the exact
registered automation ID. A misbound wakeup returns
`MISBOUND_HEARTBEAT_NO_ACTION`; it must not forward itself, inspect unrelated
work, or dispatch an executor.

Use this output shape:

```text
未处理积压:
- Task:
  需要你处理:

本次新增:
- Task:
  Status:
  需要你决定:
  不处理的影响:
```

If there are only old items or only new items, omit the empty section. A compact
fallback shape is also acceptable:

```text
未处理:
- Task:
  Status:
  需要你决定:
  不处理的影响:
```
