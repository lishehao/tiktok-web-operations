---
name: thread-supervisor
description: >-
  Create, identify, rename, pin, archive, hand off, supervise, or schedule
  persistent Codex tasks. Supports both coordinator/worker systems and one-way
  launcher-to-self-owned-executor systems; the calling domain chooses topology.
---

# Thread Supervisor

Manage persistent user-visible Codex tasks using exact IDs and an explicit
topology. Never infer a topology from old task titles or historical summaries.

## Choose topology first

The calling domain must declare one:

### `coordinator_worker`

Use only when a long-term coordinator is intentionally required. The
coordinator owns dispatch, callback handling, decisions, and any coordinator-
managed timer. Generic callback/supervision guidance below applies.

### `launcher_self_owned_executor`

Use when setup should hand one mission directly to an independent persistent
task:

```text
launcher bootstrap -> same task becomes pinned distributor
distributor -> creates one executor -> sends one canonical assignment -> reusable idle
executor -> owns user conversation, external resource, ledger, recovery,
            self-target run/round-unique one-shot wakes, and finalization
same launcher + later user command -> another fresh executor -> reusable idle
```

For this topology:

- launcher has no callback target, watchlist, pending ledger, supervisor timer,
  risk-return role, or later dispatch loop;
- executor never callbacks launcher and asks the user directly for a genuine
  human-only blocker;
- executor creates/views/consumes/retires its own unique one-shot wakes;
- no coordinator or supervisor Heartbeat exists;
- independent executors never list/read/control one another and never treat
  another task or browser owner as a blocker;
- a launcher may read the exact newly-created task once only to verify assignment
  acceptance, then becomes idle.
- idle launchers remain reusable stateless entrypoints. Each later explicit new
  operating instruction repeats fresh creation with a new run ID. The launcher
  never reads results, aggregates runs, or turns the new command into an old-run
  continuation.
- a calling domain may require the bootstrap title to transition to a pinned
  distributor title before any pre-dispatch gate or assignment. Pin/title
  failure is presentation degradation unless the domain says otherwise; it does
  not justify a second task.

The calling domain may additionally require `fresh_only_dispatch=true`. In that
topology, each setup/bootstrap/new run generates a new
`run_id`, calls `create_thread` exactly once, and recognizes only the exact new
ID returned by that call. Historical tasks are not candidates or recovery
resources.

TikTok declares `coordinator_worker`. Its setup task becomes the pinned
`TikTok 主控台`; its exact `TikTok 执行台` callbacks after every bounded round.
Do not apply launcher/self-owned-timer rules to TikTok.

## Identity and creation

- Use `create_thread` for persistent sidebar tasks; never substitute
  `spawn_agent`, Goal Mode, or an agent tree.
- Record the exact ID returned by creation before setting the presentation title.
- Title, pin, archive, list/search result, and readable summary discover a
  candidate but never prove writable ownership.
- Never guess an ID from a directory, prompt, previous run, or title.
- Treat model/reasoning/service tier/host as an opaque `execution_profile`.
  Copy explicit caller values exactly; if none are supplied, omit overrides.
- In fresh-only dispatch, never list/search/read/reuse/unarchive/revive/message/
  archive/replace a historical executor. Matching title, archive state, liveness,
  or readable summary is irrelevant and the old task remains untouched.

Read `references/canonical-registry.md` and
`references/identity-and-automation.md` before persistent assignment or timer
creation.

## One-way launcher assignment

1. Apply the domain's launcher title as the first available presentation action.
   Rename failure is presentation degradation, not a reason to duplicate tasks.
2. Run the domain preflight. If the domain declares a distributor transition,
   rename this same exact task to the distributor title, attempt to pin its exact
   ID, and read back `pinned=true` when supported. Pin failure is non-blocking
   presentation degradation; never pin the executor unless explicitly required.
3. Run every domain-declared pre-dispatch gate. A gate
   such as account-image confirmation must provide its explicit exit proof; the
   supervisor never converts a draft/proposal into confirmation.
4. Resolve one mission from the accepted gate output.
5. Generate a new run ID and call `create_thread` exactly once for one fresh
   executor with an inert bootstrap object and
   `external_work=forbidden_until_assignment_acceptance`.
6. Store the exact returned ID and set the domain title.
7. Build one canonical assignment containing exact executor ID, run ID,
   execution profile, domain refs, resource/ledger policy, and
   `launcher_contact_policy=NO_CALLBACK_NO_SUPERVISION`.
8. Send the stored bytes once to the exact executor. The executor validates and
   records `ASSIGNMENT_ACCEPTED` before external work.
9. Distributor may read that exact task once to verify acceptance, releases its
   temporary resource, records handoff, and becomes idle.

When the user later addresses the same idle launcher with another operating
instruction, repeat the domain gate and steps 3–9 with a new run ID and new executor, then return to
idle. Preserve only installed dependency configuration; inherit no historical
mission/registry/ledger/Heartbeat/tab/result/risk state.

For fresh-only dispatch, `create_thread` failure or an uncertain result without
an exact returned ID is `FRESH_TASK_CREATION_FAILED|UNKNOWN`. Report it for this
launch and stop. Do not list/search tasks, retry create, select an old title,
reuse/unarchive/revive/message/archive an old task, or create a replacement. If
the exact fresh task cannot accept assignment, report
`FRESH_TASK_ASSIGNMENT_FAILED` and stop without fallback. After handoff the
launcher never monitors or replaces the executor.

## Self-owned one-shot wake chain

For `launcher_self_owned_executor`, the executor is both manager and target:

```text
automation_manager_thread_id == targetThreadId == executor_thread_id
occurrences=1
timer_id=tiktok-wake-<run_id>-round-<round_seq>
next_wake_at < operation_stop_at
```

Do not create a timer during assignment acceptance or first-round startup. At a
completed operating-round checkpoint, the executor creates exactly one
heartbeat-kind, single-occurrence automation targeted to itself. Its ID and
display name contain the full run ID and round sequence. Immediately read back
exact automation ID, target, one-shot state, next local/UTC run, and cutoff.
Only verified readback permits yield.

A valid wake requires exact task/run/round/timer binding. Record wake
consumption, delete/retire the expired timer if still present, clear the pending
binding, and resume. Duplicate, late, misbound, or overlapping wakes perform no
external work. Never use a global timer ID or keep a repeat-on executor timer.

If a recoverable failure requires a later retry, the executor may create one
similarly unique single-occurrence recovery wake. At most one pending wake exists
per executor. Uncertain mutation remains frozen and is never retried. Explicit
stop, deadline, completion, or terminal release deletes only the exact pending
wake, if any.

Heartbeat prompts contain stable identity/resume instructions, not changing
status or raw evidence. Dynamic progress belongs in the executor ledger/task.

When the calling domain requires inter-round pacing, the round checkpoint stores
`cooldown_until`, creates/read-backs the unique one-shot wake, then yields. At
the due wake consume and clear that exact timer before resuming. The distributor
never receives a callback and never creates the executor's timer.

## Coordinator-worker rules

Apply this section only when the calling domain explicitly selects
`coordinator_worker`:

- coordinator owns user decisions, dispatch, callback acceptance, and timer;
- worker owns the external system and structured evidence;
- use callbacks at meaningful boundaries rather than polling;
- do not send unrelated work while a worker is active;
- use a low-frequency supervision Heartbeat only when the domain explicitly
  requires it;
- finalize only after worker resource-release proof.

Do not import these rules into `launcher_self_owned_executor`.

### TikTok coordinator-worker specialization

Use exactly two persistent tasks for one active mission:

```text
TikTok 启动台 --healthy same-task transition--> pinned TikTok 主控台
TikTok 主控台 --bounded round_assignment/v1--> TikTok 执行台
TikTok 执行台 --ROUND_COMPLETED|BLOCKED|RELEASED callback--> TikTok 主控台
TikTok 主控台 --one callback-armed cooldown wake--> next round
```

The main task owns profile/mission versions, strategy, exact executor registry,
callback validation, `next_dispatch_at`, one stable self-target phase timer,
user decisions, and final reporting. It never owns a TikTok operating tab or
performs TikTok mutations. The executor owns one dedicated Chrome tab, raw
evidence, within-round recovery, and one bounded 25–45-view round at a time. It
never creates, updates, views, or deletes an automation.

Before external work, prove a real callback handshake using exact task IDs and
run ID. At round completion the executor sends one canonical callback and
becomes idle. The main task accepts it only when coordinator/executor/run/round
identity and sequence match, then chooses the next three search clusters,
interaction emphasis, and a 10–20 minute cooldown.

Create the coordinator phase timer once under the user's direct mission
authorization. Read back exact automation ID, self target, current phase,
one-occurrence state, and next local/UTC run. Update that exact timer in place:

- after round dispatch, stop ordinary polling and arm one 60-minute
  `ACTIVE_WATCHDOG` wake only;
- after a valid callback, replace the pending watchdog schedule in place with
  one `COOLDOWN_WAKE` at exact `next_dispatch_at`;
- at the due cooldown wake, send one next-round assignment and rearm the same
  timer as the next 60-minute watchdog;
- delete and finalize only at user stop, mission cutoff, or terminal release.

Do not rely on a `PAUSED` create persisting. Prove stopped polling from a
read-back schedule with exactly one future occurrence. If direct creation
rejects `DTSTART` or bare `COUNT=1` yields no future run, use the tool-supported
finite `INTERVAL+UNTIL` equivalent that produces one future occurrence.

Never derive due time from model-estimated timestamps. Read machine time when
accepting the callback, compute `next_dispatch_at`, and compare epoch values on
wake. Never create/delete a timer per round, keep a five-minute active-worker
NOOP loop, or send catch-up bursts. If the timer cannot be created, updated, or
read back, do not claim unattended continuity; report
`SCHEDULER_CONTINUATION_FAILURE` in the main task while preserving completed
evidence.

## Independent-run invariant

An independent executor owns only its own task ID, run ID, ledger namespace,
automation ID, and external-resource handle/tab. It must not list/read other
domain tasks, inspect same-account activity, claim another tab, alter another
automation, or pause because another task exists.

## Presentation and lifecycle

- Naming follows the domain contract; title is not identity.
- Archive only after terminal release or when the user explicitly requests it.
- Fresh-only launchers never archive, unarchive, revive, or otherwise modify
  historical executors; the executor may finalize only its own task resources.
- A self-owned executor reports progress, hard blockers, and completion in its
  own task. The launcher has no pending-result reminders after handoff.
- A launcher is not archived/retired by a successful dispatch. It remains idle
  and user-reusable, but stateless with respect to every execution run.

## Tools

Discover the relevant persistent-task and automation tools before use:

- `create_thread`, `read_thread`, `send_message_to_thread`;
- `set_thread_title`, `set_thread_pinned`, `set_thread_archived`;
- `automation_update`.

Use exact tool readback as evidence. A tool call request or inferred schedule is
not proof of success.
