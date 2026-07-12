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
launcher -> creates one executor -> sends one canonical assignment -> reusable idle
executor -> owns user conversation, external resource, ledger, recovery,
            self-target recurring Heartbeat, and finalization
same launcher + later user command -> another fresh executor -> reusable idle
```

For this topology:

- launcher has no callback target, watchlist, pending ledger, supervisor timer,
  risk-return role, or later dispatch loop;
- executor never callbacks launcher and asks the user directly for a genuine
  human-only blocker;
- executor creates/views/updates/replaces/retires its own recurring Heartbeat;
- no coordinator or supervisor Heartbeat exists;
- independent executors never list/read/control one another and never treat
  another task or browser owner as a blocker;
- a launcher may read the exact newly-created task once only to verify assignment
  acceptance, then becomes idle.
- idle launchers remain reusable stateless entrypoints. Each later explicit new
  operating instruction repeats fresh creation with a new run ID. The launcher
  never reads results, aggregates runs, or turns the new command into an old-run
  continuation.

The calling domain may additionally require `fresh_only_dispatch=true`. TikTok
does. In fresh-only dispatch, each setup/bootstrap/new run generates a new
`run_id`, calls `create_thread` exactly once, and recognizes only the exact new
ID returned by that call. Historical tasks are not candidates or recovery
resources.

TikTok declares `launcher_self_owned_executor`; do not apply coordinator rules
to it.

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
2. Run the domain preflight and resolve one mission.
3. Generate a new run ID and call `create_thread` exactly once for one fresh
   executor with an inert bootstrap object and
   `external_work=forbidden_until_assignment_acceptance`.
4. Store the exact returned ID and set the domain title.
5. Build one canonical assignment containing exact executor ID, run ID,
   execution profile, domain refs, resource/ledger policy, and
   `launcher_contact_policy=NO_CALLBACK_NO_SUPERVISION`.
6. Send the stored bytes once to the exact executor. The executor validates and
   records `ASSIGNMENT_ACCEPTED` before external work.
7. Launcher may read that exact task once to verify acceptance, releases its
   temporary resource, records handoff, and becomes idle.

When the user later addresses the same idle launcher with another operating
instruction, repeat steps 2–7 with a new run ID and new executor, then return to
idle. Preserve only installed dependency configuration; inherit no historical
mission/registry/ledger/Heartbeat/tab/result/risk state.

For fresh-only dispatch, `create_thread` failure or an uncertain result without
an exact returned ID is `FRESH_TASK_CREATION_FAILED|UNKNOWN`. Report it for this
launch and stop. Do not list/search tasks, retry create, select an old title,
reuse/unarchive/revive/message/archive an old task, or create a replacement. If
the exact fresh task cannot accept assignment, report
`FRESH_TASK_ASSIGNMENT_FAILED` and stop without fallback. After handoff the
launcher never monitors or replaces the executor.

## Self-owned recurring Heartbeat

For `launcher_self_owned_executor`, the executor is both manager and target:

```text
automation_manager_thread_id == targetThreadId == executor_thread_id
repeat=on
finite UNTIL or operation_stop_at
```

The executor immediately reads back exact automation ID, target, role, repeat
state, next local/UTC run, and cutoff. A valid wake requires exact task/run/timer
binding. If already running, do no overlap; if idle before cutoff, resume the
same mission from the last durable checkpoint.

Ordinary page/network/browser/route/render/candidate/lane failure never pauses
or deletes the timer. An uncertain mutation freezes only its exact submission
and is never retried. For a bad timer, create/read back the replacement, switch
the stored binding, then retire the old timer. Retire only after explicit stop,
deadline, objective completion, or terminal resource release.

Heartbeat prompts contain stable identity/resume instructions, not changing
status or raw evidence. Dynamic progress belongs in the executor ledger/task.

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
