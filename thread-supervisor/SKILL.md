---
name: thread-supervisor
description: >-
  Manage persistent user-visible Codex tasks: identify, open, inspect, continue,
  create, fork, hand off between local/worktree/connected hosts, rename, pin,
  archive, schedule follow-ups, query status, and coordinate callback-based
  workers. Use when the user asks about Codex tasks, threads, chats,
  conversations, background tasks, task supervision, or scheduled continuation.
---

# Thread Supervisor

Manage Codex tasks with the smallest operation that matches the user's intent.
In user-facing text say **task**; tool names may still say **thread**.

## Core contract

1. Choose the operation before choosing an orchestration topology.
2. Treat an exact task ID, plus `hostId` when applicable, as identity. Titles,
   directories, previews, branches, and search results are labels or discovery
   evidence only.
3. Mutate another task only when the user explicitly asks to create, continue,
   steer, fork, hand off, rename, pin, archive, schedule, or supervise it.
4. Use persistent tasks for user-owned work that belongs in the sidebar. Use
   subagents for internal subtasks of the current request.
5. Prefer event-driven callbacks and product status over polling.
6. Treat a tool request as intent, not proof. Preserve the returned identifier
   and read back state when the tool supports verification.
7. Omit model and reasoning overrides unless the user explicitly supplied them.
   Do not silently upgrade or copy a previous task's execution profile.

## Operation map

| User intent | Primary operation | Key rule |
|---|---|---|
| Show or open a task | `navigate_to_codex_page` | Requires an exact task ID. |
| Find or inspect status | `list_threads`, then `read_thread` | Search only when the ID is unknown. |
| Continue or steer an existing task | `send_message_to_thread` | Do not message an unrelated or merely similar task. |
| Start a separate/background task | `list_projects`, then `create_thread` | Creation requires an explicit user request. |
| Branch from existing context | `fork_thread` | Forks copy completed history only. |
| Move a task and Git state | `handoff_thread`, then `get_handoff_status` | Handoff is a move, not a copy. |
| Rename, pin, or archive | `set_thread_title`, `set_thread_pinned`, `set_thread_archived` | Presentation never proves identity or ownership. |
| Continue later or monitor | `automation_update` | Choose task-attached continuation vs standalone runs. |
| Coordinate several persistent tasks | Composite workflow below | Use only when coordination adds real value. |

Discover the current tool schemas before acting. Product features roll out by
surface and host; if a listed operation is absent, report the runtime limit
instead of simulating it with another mechanism.

## Resolve identity

- If the user supplied an exact `codex://threads/<id>` link or task ID, use it
  directly.
- If the ID is unknown, search with the narrowest useful title, phrase, branch,
  or project query. Read the candidate before mutation.
- When `list_threads` returns a `hostId`, pass it to subsequent read/message
  calls that accept it.
- If multiple candidates remain plausible, do not choose by recency alone.
- After creation or fork, record the exact returned identifier type:
  `threadId` is usable immediately; `clientThreadId` means worktree setup is
  queued and must not be presented as a ready task ID.
- A successful rename, pin, search hit, or readable summary does not prove the
  task can be steered or can call back.

## Execute one task operation

### Create

- Call `create_thread` only when the user explicitly asks for a new,
  separate, or background task.
- For repo-scoped work, call `list_projects`, select the exact saved project,
  and choose `local` or `worktree` deliberately. Prefer a worktree when parallel
  coding tasks could touch the same checkout.
- Use `projectless` for general work without shared project files.
- Set a worktree `startingState` only when the user explicitly requests an
  existing branch/ref or the current working tree. Do not use it to name a new
  branch.
- Put the actual mission and completion criteria in the initial prompt. Avoid
  creating an inert task that needs a second message unless a domain protocol
  explicitly requires assignment acceptance.
- After success, preserve the returned ID and expose the product's created-task
  directive in the final response when required by the host UI.

### Fork

- Fork when the user wants an alternative based on the existing task's
  completed history, not merely another unrelated task.
- Choose `same-directory` for a conversational branch sharing the checkout;
  choose `worktree` for isolated code changes.
- If the source task is running, the active turn and unfinished response are
  not copied. State that limitation when it matters.
- Send a follow-up to the child only when work must continue there. A fork can
  be useful as a snapshot without immediate execution.

### Read, continue, or steer

- Read the latest 1-3 turns first. Follow older cursors only when the request
  needs deeper history. Include command/tool outputs only for a concrete
  diagnostic need.
- Treat `read_thread` as observation, not a liveness or write-capability proof.
- Send a correction to active work immediately when it changes scope,
  acceptance criteria, or prevents wasted work. Label it as an amendment.
- Queue an unrelated next task until the current work completes or asks for a
  decision. Do not use task messages as a growing to-do list while work runs.
- Omit model/reasoning fields to preserve the target's current settings unless
  the user explicitly requests an override.
- If delivery is uncertain, do not send duplicates blindly. Read the target or
  report unconfirmed delivery first.

### Hand off

- Handoff moves another task and its Git state between its checkout, a Codex
  worktree, or a matching saved project on a connected host.
- The calling task cannot hand itself off. Cloud handoff is unsupported on the
  current product path.
- A running task is interrupted before transfer. Warn when that interruption is
  material.
- Cross-host handoff requires a matching saved project for the same repository
  and subdirectory on the destination host.
- Preserve the returned `operationId` and `revision`. Poll once, then use
  `get_handoff_status(afterRevision, waitMs)` with backoff. Do not narrate or
  repeatedly poll unchanged state; the UI already shows progress.
- Use `followUpPrompt` only when work should resume automatically after a
  successful transfer.

### Presentation and lifecycle

- Use short outcome-oriented titles.
- Pin only for frequent return or durable control surfaces. Pinning changes
  sidebar placement, not context, authority, or ownership.
- Archive when the work is terminal or when the user explicitly requests it.
  Do not archive an active task merely to declutter a status report.
- Restore an archived task only when the user asks to resume that exact task.

## Schedule continuation

Use `automation_update` only when the user asks to continue later, monitor,
remind, or schedule work.

Choose one destination:

- **Task-attached scheduled work / heartbeat:** return to the same task with its
  existing context. Prefer for active follow-up loops, near-term continuation,
  or monitoring whose result belongs in the current task.
- **Standalone scheduled task:** start an independent run from a durable prompt.
  Prefer when runs should be separate or span one or more projects.

Rules:

- Test the workflow manually before scheduling when practical.
- Write a durable prompt with scope, report threshold, stop condition, and what
  requires user input.
- Inspect existing automations and update the exact matching ID instead of
  creating a duplicate. Preserve fields the user did not ask to change.
- Use the tool schema; never emit raw automation directives as a substitute for
  a successful tool call.
- Read back exact target, status, next run, and schedule when supported.
- Keep dynamic project status in the task or ledger, not in the automation
  prompt.
- Delete or retire task-attached monitoring when the terminal condition is met.

Read `references/status-and-reminders.md` for multi-task status reporting and
`references/hourly-reminders.md` only when creating a proactive supervisor
reminder.

## Choose orchestration only when needed

Default to **direct task management**. Use one of the following only when the
user's workflow actually needs multiple persistent tasks.

### One-way executor handoff

Use when a launcher should create one independent user-owned task and then
become idle.

- Create one fresh task, record its exact ID, send one canonical mission, and
  verify assignment acceptance once.
- The executor owns its user conversation, external resources, recovery,
  scheduled continuation, and finalization.
- The launcher has no callback target, watchlist, pending ledger, result
  aggregation, or supervisor timer after verified handoff.
- If the domain requires `fresh_only`, never reuse, revive, or replace a
  historical same-title task after an uncertain create/assignment result.

### Coordinator-worker

Use only when a long-lived coordinator is intentionally responsible for worker
dispatch, decisions, callback acceptance, synthesis, or a coordinator-owned
timer.

Maintain a minimal registry:

```text
coordinator: <exact task id + host>
workers: <exact task ids + hosts>
objective: <one round/outcome>
state per worker: idle | running | needs_input | completed | unknown
pending_next: <none or one queued assignment>
automation: <none or exact id>
```

Before dispatch:

1. Record exact IDs and ownership boundaries.
2. If callbacks are required, run one bounded real handshake. Outbound message
   success or a readable task does not prove the worker can call back.
3. Send objective, scope, definition of done, validation, exact callback target,
   and the events that justify an early return.

Default callback shape:

```text
Project:
Status: completed | blocked | validation_failed | needs_decision | key_risk
Changed:
Validation:
Risks:
Decision needed:
```

During execution:

- Prefer callbacks at meaningful boundaries. Poll only when callbacks are
  unavailable or the user explicitly asks for active monitoring.
- A worker that can continue autonomously is `running`, not `needs_input`.
- Product-native `Needs input` status is direct evidence and should be surfaced
  promptly.
- Corrections to active work interrupt; unrelated extensions wait in
  `pending_next` until completion/callback.
- Read only registered workers, usually the latest 1-3 turns.
- Synthesize a multi-worker round once all required results arrive; do not make
  the user read one mechanical report per worker.
- Remove completed workers from the active watchlist after their results are
  acknowledged.

For research-round synthesis and status grouping, read
`references/status-and-reminders.md`.

## Domain protocols

Keep domain-specific state machines out of this generic workflow.

- For the TikTok two-task coordinator/worker protocol, read all three:
  `references/tiktok-coordinator-worker.md`,
  `references/canonical-registry.md`, and
  `references/identity-and-automation.md`.
- Do not apply TikTok assignment envelopes, callback hashes, round counts, tab
  ownership, or scheduler phases to other projects unless their own contract
  explicitly adopts them.

## Completion and failure semantics

- `unknown`, `notLoaded`, an empty read, or a transient host/tool error is not
  proof of completion, blockage, or owner absence.
- Task creation is complete only when the exact returned identifier is recorded.
- Assignment is complete only when the target accepts the mission or equivalent
  target-side evidence exists.
- Handoff is complete only when the handoff operation reports success.
- Scheduled continuity is complete only when the exact automation and future run
  are readable.
- Worker completion is accepted only when required validation/evidence exists;
  a polished final message alone is insufficient.
- Report bounded uncertainty instead of guessing or creating duplicate tasks.

## Verification checklist

- Correct operation chosen before topology.
- Exact task ID and `hostId` recorded where applicable.
- User authorized every persistent-task mutation.
- Local vs worktree vs projectless vs remote destination chosen deliberately.
- Returned `threadId`, `clientThreadId`, `operationId`, or automation ID preserved
  without substitution.
- Callback capability proven only when the workflow depends on it.
- Polling is bounded and lower frequency than event-driven updates.
- Presentation state is not confused with identity or execution state.
- Completion, handoff, schedule, and release claims have readback evidence.
