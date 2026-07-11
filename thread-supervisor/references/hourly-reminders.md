# Supervisor Reminders

Use only when creating or updating a supervisor heartbeat for unhandled items.

## Before creating

- Inspect existing automations first.
- Reuse/update a matching heartbeat for the same coordinator.
- If an existing heartbeat belongs to another project group, create a separate one.
- Use the fixed name format `未处理信息提醒 - <cadence> - <Coordinator thread name>`.
- If an older matching heartbeat uses a different name, rename it instead of
  creating a duplicate.

## Stable mechanism vs dynamic state

The heartbeat is a stable reminder mechanism. It should answer:

- which coordinator owns this reminder
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

Put those facts in the coordinator thread, management brief, or the next user
report. Update the automation only when the watchlist, cadence, ownership
boundary, notification rules, or target coordinator thread changes.

## "Unhandled" means

- completed callback not yet acknowledged
- `needs_decision`, `blocked`, `validation_failed`, or `key_risk`
- active watched thread stalled and requiring user decision
- promised follow-up dispatch not yet sent

Do not report ordinary progress, acknowledged results, inactive context hubs, or retired threads.

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

- Check only the coordinator's current active watchlist.
- Read recent callbacks or latest 1-3 turns per active target.
- Stay silent if nothing is actionable unless the user explicitly asks for all-clear messages.
- Treat `已读`, `收到`, `看到了`, or a related follow-up as acknowledgement.
- Do not treat acknowledgement as approval for external APIs, authenticated browsing, production changes, or model spend.
- Avoid embedding detailed current-state lines such as "Thread X is waiting for Y"
  unless they are stable ownership boundaries. Dynamic pending items should be
  discovered from callbacks, the management brief, or the coordinator's recent
  turns at heartbeat runtime.

Use this output shape:

```text
未处理积压:
- Thread:
  需要你处理:

本次新增:
- Thread:
  Status:
  需要你决定:
  不处理的影响:
```

If there are only old items or only new items, omit the empty section. A compact
fallback shape is also acceptable:

```text
未处理:
- Thread:
  Status:
  需要你决定:
  不处理的影响:
```
