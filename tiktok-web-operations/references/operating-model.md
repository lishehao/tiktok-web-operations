# Starter Coordinator And Persistent Executor

Use exactly two user-visible persistent Codex Threads. The starter/install task
becomes the coordinator; it creates one execution Thread. Both TikTok roles use
`gpt-5.6-luna` with `thinking=high`. Never use a collaboration subagent, Goal
Mode, or an agent tree for either role.

Use `$thread-supervisor` for generic registration, callback, work-state,
heartbeat fallback, stop/release, and archival mechanics. Read its
`references/identity-and-automation.md` before creating either the executor or
an automation. This reference owns the TikTok-specific authority split and
evidence contract.

## Topology

```text
Starter task
  phase 1: install/upgrade -> read-only preflight -> ask direction/duration -> wait
  phase 2: temporary nonce title -> prove own ID -> final title TikTok 主控台 [pinned]
           -> create one executor -> final title TikTok 执行台 [unpinned]
           -> handshake -> smoke
           -> one durable run timer with optional first-install overlay
           -> bounded operating rounds
```

The starter task remains the user-facing coordinator and is never archived as
part of successful bootstrap. The executor owns its dedicated Chrome tab, is the
sole same-account mutation writer, and is the sole raw-ledger writer.

## Role cards

```text
TikTok 主控台
objective: advance or stop the authorized run at the correct time and own every
user decision.
inputs: direction profile, authorization, capability matrix, callback, timer,
ledger summary, current time, operation_stop_at.
output: one next bounded dispatch, one consolidated user decision, or stop.
never: Chrome/TikTok work, raw per-item analysis, Skill development, concurrent
dispatches.

TikTok 执行台
objective: execute exactly the current bounded block, record evidence, release
Chrome, callback, and idle.
inputs: immutable registry plus one bounded dispatch.
output: ledger checkpoints plus one structured callback.
never: long-term strategy, user questions, self-recovery beyond the explicit
budget, scheduling, another block, another Thread, Skill development.
```

Persona, target audience, search clusters, interaction policy, and validation
rules are constraints carried in the dispatch. Do not restate them as parallel
goals in either role prompt.

## Starter self-registration

The coordinator must know its exact Thread ID before creating the executor:

1. Generate a short unique `run_nonce` and temporarily rename the current task,
   using the self-targeting title operation, to
   `TikTok 主控台注册 · <run_nonce>`.
2. Use `list_threads` with that exact title and require one matching current
   local task in the expected project/directory context.
3. Use `read_thread` on the returned ID and confirm the current bootstrap state,
   account, direction handoff, and `run_nonce` are consistent.
4. Record that returned ID as `coordinator_thread_id`. Never derive an ID from a
   directory name, old prompt, previous run, or another task's callback.
5. Create the run registry with `run_id`, `run_nonce`, coordinator ID/host,
   `coordinator_title=TikTok 主控台`, `coordinator_pinned=true`, executor ID
   initially `NONE`, `executor_title=TikTok 执行台`, `executor_pinned=false`,
   account, Luna/High profile, ledger, authority envelope version, stop time,
   automation owner equal to the coordinator ID, and heartbeat fields initially
   `NONE`.
6. Rename the verified coordinator to the final title `TikTok 主控台`, pin it,
   and verify presentation state when the tool exposes it. Final title/pin are
   presentation only and must never replace the registered ID.
7. If zero or multiple candidates remain, stop with
   `BLOCKED_COORDINATOR_ID_UNVERIFIED`. Do not create a disposable coordinator or
   start polling as a silent fallback.

## Bootstrap creation contract

Only after preflight is healthy and the user supplies direction/duration or
accepts defaults:

1. Inspect active TikTok tasks and apply the same-account mutation-writer fence.
   An unrelated Chrome task or other-tab owner is not a global blocker.
2. Resolve `direction_profile`, duration, `operation_stop_at`, standing action
   envelope, and a private ledger path.
3. Complete starter self-registration and keep the starter as coordinator.
4. Select the same saved project for the executor when clearly available;
   otherwise create it as a projectless local Thread.
5. Call `create_thread(model="gpt-5.6-luna", thinking="high")` exactly once for
   the executor. Its initial prompt includes the coordinator ID,
   account, envelope, ledger, dedicated-tab rule, sole mutation-writer role, and
   callback schema, and says to wait for `SELF_REGISTRY` without touching Chrome.
6. Record the returned executor ID, set its final title to `TikTok 执行台`, and
   explicitly keep it unpinned.
7. Send `SELF_REGISTRY` to the exact returned executor ID with Luna/High. Include
   both IDs, account, ledger, authority, role, and stop time byte-for-byte.
8. Require the executor to callback `THREAD_READY` to the registered coordinator
   ID. Verify callback source and payload IDs against the registry.
9. Dispatch one read-only `stability_smoke_01` to the exact executor ID. Require
   the acceptance criteria in `stability-and-circuit-breakers.md` before any
   full calibration block or mutation.
10. If unattended continuation needs a heartbeat, create it only now from this
    verified coordinator. Pass explicit `targetThreadId=coordinator_thread_id`,
    include `run_id` in its name/prompt, view the returned automation ID, require
    exact binding readback, and store it in the run registry. The executor never
    creates an automation.
11. Keep both tasks unarchived. Pin only `TikTok 主控台`; keep `TikTok 执行台`
    unpinned. Navigate the app to the coordinator when useful.

If self-registration, creation, handshake, or smoke fails, do not claim stable
operation. Do not create a second executor or another coordinator. Archive an
empty executor only when the user requests cleanup; otherwise preserve evidence.

## Hard tool and model requirements

Require `list_projects`, `create_thread`, `list_threads`, `read_thread`,
`send_message_to_thread`, `set_thread_title`, and `set_thread_archived`.
Use `set_thread_pinned` when available to pin the coordinator and unpin the
executor. Missing presentation-only pin/navigation tools do not block operation;
record the unavailable action internally.
Require `automation_update` when the resolved run is timed and expected to span
more than one bounded block, or when the user requests unattended continuation.
If unavailable, mark the timer degraded, keep callback-driven manual
continuation, and say that deadline/watchdog timing is unavailable; never attach
a substitute automation to another task.

TikTok operations explicitly require `gpt-5.6-luna` plus `thinking=high` for the
starter coordinator, executor creation, and operational dispatches. This is a
TikTok domain requirement, not a default supplied by Thread Supervisor. If the
runtime rejects it, stop rather than substitute another model or effort.

Fast Mode is a separate runtime/service-tier capability. Record it only when the
current task or runtime proves it; never claim that `create_thread` propagated
Fast Mode unless the tool surface exposes and confirms that field.

## Authority split

| Concern | Starter coordinator | Execution Thread |
|-|-|-|
| User conversation and strategy | Owns | Never owns |
| Direction and next block | Owns | Executes current envelope |
| Authorization and lifecycle | Owns | Matches exact authority |
| Heartbeat/automation | May own one bound to its exact ID | Never creates or owns |
| Chrome and TikTok | Never touches | Dedicated tab; sole mutation writer |
| Raw ledger | Read-only consumer | Sole writer |
| Capability evidence | Interprets | Collects immediate/reopen/account proof |
| Reporting | User-facing | Structured callback |

## Coordinator loop

1. Receive the executor callback and read at most the latest relevant 1-3 turns
   when more evidence is necessary.
2. Verify callback transport source, payload run ID, both Thread IDs, ledger,
   and current block ID against the immutable registry.
3. Reconcile composition, query quality, capability changes, pending user work,
   authorization, deadline, and risk.
4. If status is `blocked`, `validation_failed`, `needs_decision`, or `key_risk`,
   pause all new dispatches. Consolidate one user-facing decision in `TikTok 主控台`:
   risk, evidence, affected lane/block/run, what has already stopped, whether
   read-only work remains safe, one recommendation, and at most three options.
   Do not tell the user to inspect or reply in `TikTok 执行台`.
5. Resume only after the user decides in `TikTok 主控台` or a verifiable external-state
   change clears the blocker. Never treat a worker-local reply or its final
   message as user authorization.
6. Otherwise choose one next bounded block or stop. A normal block should amortize callback
   overhead: normally 10-20 minutes, 20-40 feed items, or one complete search
   cluster plus a For You checkpoint.
7. If no user decision is required and the standing duration authorizes
   continuation, send exactly one next block to the registered executor ID with
   Luna/High, mark it `running_current_task`, and end the turn.
8. Never poll Chrome, operate TikTok, or dispatch overlapping blocks.

Routine per-video observations stay in the ledger. Callback only on completed
block, `blocked`, `validation_failed`, `needs_decision`, `key_risk`, uncertain
submission, authorization mismatch, or stop/release.

For every timed operation expected to exceed one bounded block, one coordinator-
only heartbeat acts as the durable run timer, missed-callback watchdog, and
round scheduler. Callback remains the primary event signal; heartbeat is the
time signal.
The heartbeat must not touch Chrome, overlap a running executor turn, bypass a
circuit breaker, create tasks, or rewrite dynamic operating state. On every
wakeup, require
`waking_thread_id == heartbeat_target_thread_id == coordinator_thread_id` and
the registered automation ID. A mismatch returns
`MISBOUND_HEARTBEAT_NO_ACTION` and dispatches nothing.

## Durable operation timer

Create one logical timer only after coordinator identity, executor handshake,
and stability smoke are verified. Store its exact automation ID, owner/target,
`operation_stop_at`, and next tick in the immutable registry.

- Use a low-frequency recurring timer or successive one-shot updates according
  to the available scheduler, but preserve the same logical timer identity and
  never create a timer per block.
- Set the next tick to the earlier of the next useful watch time and
  `operation_stop_at`. Normal cadence is about 15-30 minutes; callbacks may
  advance work sooner without waiting for a tick.
- On wake, verify identity and time first. At or after stop time, dispatch no new
  work; send `STOP_AND_RELEASE` when needed, verify release, finalize the run,
  and delete the timer.
- Before stop time, reconcile any missed callback. If the executor is running,
  do nothing and schedule the next tick. If it is idle, healthy, authorized,
  and no user decision is pending, dispatch at most one next block.
- A risk or decision pauses dispatch but does not move the deadline. Keep or
  reschedule the same timer only to enforce stop and surface unhandled state.
- If automation is unavailable, mark `operation_timer_state=DEGRADED`, disclose
  that long-term timing is callback-only, and never fake persistence by keeping
  a turn open.

The first-install `+15/+35/+60` schedule uses this same durable timer during its
first hour. It is a supervision cadence overlay, not a second automation.

## First-install supervision window

Use `${CODEX_HOME:-$HOME/.codex}/state/tiktok-web-operations/install-state.json`
as private machine state outside both managed Skill trees. Store no handle,
credential, cookie, browser state, or content history.

- A true `INSTALL` writes `first_install_supervision=PENDING`. `UPGRADE`,
  `NOOP`, force reinstall, and later missions never create or reset it.
- Phase 1 does not start the clock because no executor exists. On the first real
  operation, after verified handshake and successful stability smoke, set the
  marker to `ACTIVE`, record start/end, and apply the first-hour checkpoint
  overlay to the run's existing durable timer with exact binding proof.
- Target cumulative checkpoints are approximately `+15`, `+35`, and `+60`
  minutes from activation. Reuse/update the same exact run timer for the next
  checkpoint; never create a separate supervision automation. Cap the last
  checkpoint at `operation_stop_at` when the run is shorter than one hour.
- On wake, verify run/owner/target/automation identity, read the executor's
  latest 1-3 relevant turns plus callback and ledger state, and do nothing to
  Chrome/TikTok. Do not interrupt an in-progress executor.
- Stay silent on ordinary healthy progress. A missed callback or non-completed
  state follows the main-console risk consolidation contract and pauses new
  dispatch until the user decides there.
- At final checkpoint, early user stop, or run end, delete/pause the exact owned
  watch heartbeat and persist `CONSUMED`. Never recreate the window for another
  run, upgrade, reinstall over the same managed installation, or task restart.
- If automation creation/readback is unavailable, persist `DEGRADED`, disclose
  callback-only supervision once in `TikTok 主控台`, then treat the one-time window as
  consumed rather than retrying on every future mission.

## Executor loop

For each message from the registered coordinator ID:

1. Verify both IDs, exact account, Luna/High profile, dedicated-tab isolation,
   sole mutation-writer authority, capability matrix, ledger tail, stop time, and
   current block.
2. Execute only that bounded block or exact authorized action.
3. Append raw evidence at the checkpoints required by the active TikTok block.
4. Release only the executor's Chrome control at completion or terminal failure.
5. Callback once to the coordinator with Luna/High and the schema below.
6. For any non-`completed` result, set `decision_required: true`; do not ask the
   user a question or propose continuation in the executor Thread. Its final
   response may only say that the result was sent to `TikTok 主控台` and it is idle.
7. Become idle. Never self-dispatch, create another Thread, spawn an agent, or
   create/update/delete an automation.

## Execution envelope

Every dispatch includes run ID, both Thread IDs, account, roles, Luna/High profile,
dedicated-tab and sole-writer rules, full `direction_profile`, search clusters,
content ontology, sample parameters, continuous-feed invariant, capability
matrix, lane-specific authorization, comment voice and 30-word ceiling, ledger,
stop time, circuit-breaker state, and callback schema.

Copy registry values byte-for-byte. Any drift before Chrome connection is a
terminal `registry_mismatch`. Never include a Skill-development task or another
bootstrap task as callback target.

## Default action envelope

- Post like remains disabled.
- Favorite, TikTok Repost, and proactive top-level comments may be used only on
  strong-core posts after each lane passes its independent persistence gate.
- Favorite requires immediate, near +3 seconds, total +10 seconds, reload/reopen,
  and account-level evidence when exposed.
- Repost permits opening Share sheet read-only, then only the explicit TikTok
  Repost control; generic Share, copy-link, send, and other targets are excluded.
- Comments are contextual, preferably 2-12 words, never over 30 words, and must
  survive reload verification.
- Never set engagement quotas or infer ranking effects.

## Callback schema

```text
status: completed | blocked | validation_failed | needs_decision | key_risk
run_id:
coordinator_thread_id:
executor_thread_id:
block_id:
summary:
sample_counts:
composition:
queries_used:
actions_performed:
mutations_count:
capability_matrix_delta:
risks:
affected_scope: lane | current_block | whole_run
safe_to_continue_read_only: true | false
decision_required: true | false
decision_options:
ledger_path:
recommended_next_block:
```

Every `blocked`, `validation_failed`, `needs_decision`, and `key_risk` callback
sets `decision_required: true` and prevents another dispatch. `decision_options`
contains zero to three coordinator-ready choices, never a question addressed to
the executor Thread. `completed` may set `decision_required: false` even when it
records non-actionable observations in `risks`.

## Stop and recovery

`STOP_AND_RELEASE` overrides an active block. The executor stops without another
probe, releases its tab, records submission certainty, appends a final
checkpoint, callbacks `STOPPED_AND_RELEASED`, and remains idle. The coordinator
then verifies and pauses/deletes only its own registered heartbeat. Keep the
active/idle registered pair unarchived unless the user explicitly asks for full
cleanup. When a released executor has been replaced in the registry and owns no
heartbeat, Chrome tab, or uncertain mutation, unpin and archive that retired
executor so it does not remain in the active task list.

If the executor disappears, first resolve uncertain submissions and incumbent
mutation authority. Create a replacement only with explicit user authorization,
then replace the executor registry and repeat the full handshake. If the
coordinator disappears, the executor stops mutation, releases Chrome, and waits;
it never guesses a new callback destination.
