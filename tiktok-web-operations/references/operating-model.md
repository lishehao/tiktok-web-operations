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
           -> handshake -> immediate first block and proof
           -> repeat-on executor operation heartbeat + read-only coordinator supervisor heartbeat
           -> bounded scheduled operating rounds
```

The starter task remains the user-facing coordinator and is never archived as
part of successful bootstrap. The executor owns only this run's dedicated Chrome
tabs and is this run's sole raw-ledger writer. Other independent runs may operate
the same account in other tabs; record attribution contamination and pause only
exact target/action submission conflicts.

## Role cards

```text
TikTok 主控台
objective: advance or stop the authorized run at the correct time and own every
user decision.
inputs: direction profile, authorization, capability matrix, callbacks, two
heartbeat readbacks, slot ledger summary, current time, operation_stop_at.
output: scheduler configuration/update, one consolidated user decision, or stop.
never: Chrome/TikTok work, raw per-item analysis, Skill development, concurrent
dispatches.

TikTok 执行台
objective: execute exactly the current bounded block, record evidence, release
Chrome, callback, and idle.
inputs: immutable registry plus one immediate dispatch or one operation-heartbeat slot.
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
   automation manager equal to the coordinator ID, and both operation/supervisor
   heartbeat fields initially `NONE`.
6. Rename the verified coordinator to the final title `TikTok 主控台`, pin it,
   and verify presentation state when the tool exposes it. Final title/pin are
   presentation only and must never replace the registered ID.
7. If zero or multiple candidates remain, stop with
   `BLOCKED_COORDINATOR_ID_UNVERIFIED`. Do not create a disposable coordinator or
   start polling as a silent fallback.

## Bootstrap creation contract

Only after preflight is healthy and the user supplies direction/duration or
accepts defaults:

1. Inspect active TikTok tasks for tab ownership, recommendation-attribution
   contamination, and exact target/action submission collision. Another Chrome
   owner or same-account executor is not a global blocker.
2. Resolve `direction_profile`, duration, `operation_stop_at`, standing action
   envelope, and a private ledger path.
3. Complete starter self-registration and keep the starter as coordinator.
4. Select the same saved project for the executor when clearly available;
   otherwise create it as a projectless local Thread.
5. Call `create_thread(model="gpt-5.6-luna", thinking="high")` exactly once for
   the executor. Its initial prompt includes the coordinator ID,
   account, envelope, ledger, dedicated-tab rule, this-run writer role, and
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
10. Execute and validate the first real bounded block immediately in the current
    user turn. Do not defer first proof to a timer.
11. For a multi-block timed run, the verified coordinator creates two recurring
    automations: `operation_heartbeat` with explicit
    `targetThreadId=executor_thread_id`, and lower-frequency
    `supervisor_heartbeat` with explicit
    `targetThreadId=coordinator_thread_id`. Both are `repeat=on`, use finite
    `UNTIL` or equivalent `operation_stop_at`, and must pass exact ID/target/
    repeat/next-run/local+UTC/deadline readback. The executor never manages them.
12. Keep both tasks unarchived. Pin only `TikTok 主控台`; keep `TikTok 执行台`
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
It must support explicit cross-thread `targetThreadId`, repeat-on recurrence,
finite stop protection, and view readback. If unavailable, mark scheduled
continuation degraded and say that multi-hour persistence is unavailable; never
fake it with `COUNT=1`, worker self-renewal, or a turn kept open.

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
| Heartbeat/automation | Creates/manages operation heartbeat targeting executor and supervisor heartbeat targeting itself | Receives operation wakes; never creates, updates, renews, pauses, or deletes |
| Chrome and TikTok | Never touches | Dedicated tabs; this-run mutation writer |
| Raw ledger | Read-only consumer | Sole writer |
| Capability evidence | Interprets | Collects immediate/reopen/account proof |
| Reporting | User-facing | Structured callback |

## Coordinator loop

1. Receive the executor callback and read at most the latest relevant 1-3 turns
   when more evidence is necessary.
2. Verify callback transport source, payload run ID, both Thread IDs, ledger,
   and current block ID against the immutable registry.
3. Reconcile search cards assessed, qualified search views, held-out For You
   validation, query quality, capability changes, pending user work,
   authorization, deadline, and risk. Never treat card relevance as consumed
   training evidence.
4. If status is `blocked`, `validation_failed`, `needs_decision`, or `key_risk`,
   pause the affected scope and inspect `decision_required`. When true,
   consolidate one user-facing decision in `TikTok 主控台`:
   risk, exact error code, evidence-bounded `可能原因`, same-domain/neutral probe
   evidence, recovery actions already attempted, affected lane/block/run, what
   has already stopped, whether read-only work remains safe, one minimal user
   action, and at most three options.
   Do not tell the user to inspect or reply in `TikTok 执行台`.
5. When `decision_required=false`, do not ask the user to reconfirm or choose a
   recovery tier. Store the latest instruction plus `auto_resume_condition` and
   update the same operation heartbeat to a bounded read-only recheck slot; the
   supervisor heartbeat never touches Chrome or dispatches TikTok work. Resume the unchanged instruction automatically after a
   verifiable external-state change clears the blocker. When
   `decision_required=true`, resume only after the user decides in `TikTok 主控台`.
   Never treat a worker-local reply or its final message as user authorization.
6. Otherwise choose the next bounded block template or stop. The default is one
   complete search-training block: three assessed five-card clusters and
   normally 9–15 qualified opened/watched core posts. Run a separate 5–10 item
   held-out For You validation only after two training blocks or roughly 20–30
   qualified views.
7. For a scheduled run, update the existing operation heartbeat's bounded block
   template only when strategy/authorization changes; never dispatch a parallel
   ad-hoc round. For a one-block/manual run, send one direct message to the exact
   executor. In either case verify registry fields, block/slot identity, and
   callback target before execution.
8. Never poll Chrome, operate TikTok, or dispatch overlapping blocks.

Routine per-video observations stay in the ledger. Callback only on completed
block, `blocked`, `validation_failed`, `needs_decision`, `key_risk`, uncertain
submission, authorization mismatch, or stop/release.

A transient Chrome/network error that fully recovers inside the bounded budget
does not create an event callback or standalone user message. Preserve it in the
ledger and ordinary completed callback; the coordinator folds one short
`<exact code> 已恢复；可能原因：...` clause into the next three-line receipt's
`本轮完成` line. Never add a fourth recovery/risk line.

A feed-validation transition failure may return `status=completed` with
`feed_validation_status=partial|unavailable`, `decision_required=false`, and a
search-training next block when account/login/warning/tab/search-playback safety
remains healthy. It is not a `validation_failed` whole-run callback. After two
consecutive lane failures, disable/defer only the feed-validation lane for the
current runtime.

Block completion is not whole-run completion. A Heartbeat tick is not a callback
and never proves release.

For every timed operation expected to exceed one bounded block, use two
coordinator-managed recurring heartbeats after first-block proof:

- the operation heartbeat wakes the exact executor and is the durable round
  scheduler;
- the lower-frequency supervisor heartbeat wakes the coordinator and is the
  read-only continuation/proof watchdog.

Callbacks remain the primary event signal. Neither heartbeat may overlap an
active slot, bypass a circuit breaker, create tasks, or create descendant
automations. Each wake must match the registered automation ID, run ID, role,
target Thread, and stop guard. A mismatch returns
`MISBOUND_HEARTBEAT_NO_ACTION` and performs no TikTok action.

## Durable operation scheduler

Create both logical heartbeats only after coordinator identity, executor
handshake, stability smoke, and one immediate real block are verified. Store
their exact IDs, manager/targets, repeat state, next runs, local/UTC schedule,
`operation_stop_at`, and `heartbeat_receipt_policy=always_three_lines`.

- Operation heartbeat: target the exact executor, `repeat=on`, fixed recurrence,
  finite `UNTIL` or equivalent cutoff. Every wake maps to one deterministic
  `slot_id` and at most one bounded block.
- Supervisor heartbeat: target the exact coordinator, `repeat=on`, lower
  frequency, same cutoff. It reads thread state, callbacks, and the slot ledger;
  it never operates TikTok or dispatches an overlapping ad-hoc block.
- The slot ledger records `planned`, `started`, `completed`, `blocked`, or
  `missed`, plus scheduled local/UTC time, observed wake turn, callback/proof,
  and mutation certainty. The executor writes execution states; the coordinator
  reconciles them read-only.
- On an operation wake, verify identity/time/slot. If the previous slot is still
  running or uncertain, record the new slot `missed` and do nothing. At or after
  stop time, perform no new TikTok action and callback for terminal handling.
- On a supervisor wake, verify that every due slot has a real executor wake/new
  turn and proof. Missing repeat state, missing wake, missing proof, or a broken
  next run is `SCHEDULER_CONTINUATION_FAILURE`; report it to the coordinator and
  pause scheduled continuation without touching Chrome.
- User mission changes are applied by the coordinator updating the same
  operation heartbeat. Stop/completion deletes or pauses both exact heartbeats
  only after terminal executor release proof.
- Never use `COUNT=1` and depend on the executor to schedule the next wake. Never
  let the executor create, update, renew, pause, or delete an automation.
- If automation support is unavailable, mark scheduled continuation `DEGRADED`,
  disclose that multi-hour timing is unavailable, and never fake persistence by
  keeping a turn open.

### Three-line heartbeat receipt

After both heartbeats are created and every valid supervisor heartbeat, provide a visible receipt
even when progress is healthy:

```text
本轮完成：<one sentence>
下次心跳：<YYYY-MM-DD HH:mm timezone>
下轮计划：<one bounded purpose>
```

Before reporting, view both registered heartbeats and verify automation IDs,
targets, repeat state, next runs, and cutoff. Report the next relevant verified
local tick, normally the earlier of operation or supervisor wake.
Only then persist/report the time. Use the user's local timezone and include the
date. Do not show an automation ID.

- Executor running: `本轮完成` states the verified progress/state; `下轮计划`
  says to wait for its callback and never dispatch overlapping work.
- Executor idle and healthy: report the one bounded block just dispatched or
  planned.
- Risk/decision pending: report the verified next safety/deadline tick when one
  remains; `本轮完成` contains exact code, `可能原因`, and attempted recovery;
  `下轮计划` contains the minimal user action and says no new TikTok action will
  run meanwhile. Do not add a fourth line.
- Schedule update/readback failure: use
  `下次心跳：未建立（调度校验失败）` and safely pause.
- Final tick: use `下次心跳：无（进入终止结算）` and plan to obtain final executor
  release proof.
- Finalized run: use `下次心跳：无（任务已完成）`; the whole-run compact result may
  follow, without internal IDs.

The first-install `+15/+35/+60` schedule is implemented by the existing
supervisor heartbeat during its first hour. It does not modify the operation
heartbeat cadence and does not create a third automation.

## First-install supervision window

Use `${CODEX_HOME:-$HOME/.codex}/state/tiktok-web-operations/install-state.json`
as private machine state outside both managed Skill trees. Store no handle,
credential, cookie, browser state, or content history.

- A true `INSTALL` writes `first_install_supervision=PENDING`. `UPGRADE`,
  `NOOP`, force reinstall, and later missions never create or reset it.
- Phase 1 does not start the clock because no executor exists. On the first real
  operation, after verified handshake and successful stability smoke, set the
  marker to `ACTIVE`, record start/end, and apply the first-hour checkpoint
  cadence to the run's existing supervisor heartbeat with exact binding proof.
- Target cumulative checkpoints are approximately `+15`, `+35`, and `+60`
  minutes from activation. Reuse/update the same exact supervisor heartbeat;
  never create a separate supervision automation. Cap the last
  checkpoint at `operation_stop_at` when the run is shorter than one hour.
- On wake, verify run/manager/target/automation identity, read the executor's
  latest 1-3 relevant turns plus callback and ledger state, and do nothing to
  Chrome/TikTok. Do not interrupt an in-progress executor.
- On ordinary healthy progress emit only the fixed three-line heartbeat receipt.
  A missed callback or non-completed state follows the main-console risk
  consolidation contract and pauses new dispatch until the user decides there.
- At the overlay's final checkpoint, early user stop, or run end, persist
  `CONSUMED`. Do not delete either run heartbeat before terminal executor
  release; retire both during whole-run
  finalization. Never recreate the window for another run, upgrade, reinstall
  over the same managed installation, or task restart.
- If automation creation/readback is unavailable, persist `DEGRADED`, disclose
  callback-only supervision once in `TikTok 主控台`, then treat the one-time window as
  consumed rather than retrying on every future mission.

## Executor loop

For each direct message from the registered coordinator ID or verified operation
heartbeat wake targeted to this executor:

1. Verify both IDs, exact account, Luna/High profile, dedicated-tab isolation,
   this-run writer authority, capability matrix, ledger tail, stop time, current
   block, automation ID, and deterministic slot ID when heartbeat-triggered.
2. Execute only that bounded block or exact authorized action.
3. Append raw evidence at the checkpoints required by the active TikTok block.
4. Release only the executor's Chrome control at completion or terminal failure.
5. Callback once to the coordinator with Luna/High and the schema below.
6. For a non-`completed` result, set `decision_required` from actual need. Use
   `false` for a known current wait-and-recheck condition with an exact
   `auto_resume_condition`; use `true` only when human action, missing/expanded
   authorization, or a non-inferable safety decision is required. Do not ask the
   user a question or propose continuation in the executor Thread. Its final
   response may only say that the result was sent to `TikTok 主控台` and it is idle.
7. Become idle. Never self-dispatch, create another Thread, spawn an agent, or
   create/update/renew/pause/delete an automation. A completed slot never
   schedules its successor.

For an ordinary block use `callback_scope=block`, `terminal_event=NONE`, and
`release_state=NONE`. For terminal `STOP_AND_RELEASE`, skip ordinary block work
and follow the whole-run completion transaction exactly once.

## Execution envelope

Every dispatch includes run ID, both Thread IDs, account, roles, Luna/High profile,
dedicated-tab and this-run writer rules, full `direction_profile`, search clusters,
content ontology, sample parameters, continuous-feed invariant, capability
matrix, lane-specific authorization, comment voice and 30-word ceiling, ledger,
stop time, latest instruction/authority version, circuit-breaker state, and callback schema.

Copy registry values byte-for-byte. Any drift before Chrome connection is a
terminal `registry_mismatch`. Never include a Skill-development task or another
bootstrap task as callback target.

## Default action envelope

- Defaults apply only to fields absent from the latest explicit user instruction.
- Post like is disabled by default when not requested. When the latest instruction
  explicitly authorizes it, set it to `pending_fresh_gate`; historical failures
  stay in the ledger and do not require another confirmation.
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
callback_scope: block | run_terminal
terminal_event: NONE | EXECUTOR_RELEASED
release_state: NONE | STOPPED_AND_RELEASED | RELEASE_UNVERIFIED
run_completion_reason: NONE | deadline_reached | user_stopped | objective_complete | terminal_risk | cancelled
run_id:
instruction_version:
coordinator_thread_id:
executor_thread_id:
block_id:
trigger: direct_first_block | direct_manual | operation_heartbeat
slot_id:
slot_scheduled_local:
slot_scheduled_utc:
slot_state: planned | started | completed | blocked | missed
summary:
sample_counts:
search_results_assessed:
qualified_search_views:
feed_validation_status: not_run | verified | partial | unavailable | disabled
feed_validation_sample_count:
runtime_recovery_status: not_needed | recovered | failed | platform_risk
recovery_class: none | tab_binding_stale | browser_disconnected | dns_network | proxy_tls | http_status | blocked_by_client | ambiguous_render
error_code:
failure_scope: none | tab | browser | network_global | tiktok_domain | target_page | platform
recovery_attempts:
account_reverified: true | false | not_needed
likely_cause:
likely_cause_basis:
recovery_actions_attempted:
user_action_required: true | false
user_action:
current_blocker:
auto_resume_condition:
composition:
queries_used:
actions_performed:
mutations_count:
concurrent_same_account_activity: true | false
recommendation_attribution_contaminated: true | false
exact_mutation_conflict: none | target/action
capability_matrix_delta:
risks:
affected_scope: lane | current_block | whole_run
safe_to_continue_read_only: true | false
decision_required: true | false
decision_options:
ledger_path:
recommended_next_block:
```

Every non-`completed` callback pauses the affected scope. Set
`decision_required=true` only when a human action/choice is needed; its
`decision_options` contains zero to three coordinator-ready choices, never a
question addressed to the executor Thread. A current platform wait with an exact
`auto_resume_condition` uses `decision_required=false`; the coordinator does not
convert it into a confirmation prompt and resumes the latest authorized
instruction after verified clearance. `completed` may also set
`decision_required=false` when it
records non-actionable observations in `risks`, including a fully recovered
transient Chrome/network event. A persistent infrastructure failure returns one
coordinator-ready `blocked`/`key_risk` callback with exact class, code, scope,
attempts, `likely_cause`, probe basis, attempted actions, minimal user action,
and ledger evidence; it is not mislabeled as account enforcement.

Only a terminal callback may use `callback_scope=run_terminal` or
`terminal_event=EXECUTOR_RELEASED`; a normal `completed` callback must not use
them.

## Stop and recovery

### Whole-run completion transaction

At `operation_stop_at`, explicit user stop, or objective completion:

1. The coordinator sets `run_terminal_state=STOP_REQUESTED`, records exactly one
   `run_completion_reason`, and stops ordinary dispatch.
2. It sends one terminal `STOP_AND_RELEASE` to the exact registered executor ID,
   even when the executor appears idle.
3. The executor performs no new browse or mutation. It stops the active block if
   any, resolves submission certainty, releases its tab, appends a final
   cumulative checkpoint, and callbacks once with
   `callback_scope=run_terminal`, `terminal_event=EXECUTOR_RELEASED`, and
   `release_state=STOPPED_AND_RELEASED`.
4. The coordinator validates callback source/payload IDs, final ledger path,
   release proof, cumulative browse/mutation counts, and zero unresolved action.
   It then sets `EXECUTOR_RELEASED`, pauses/deletes its exact operation and
   supervisor heartbeats,
   sets `operation_timer_state=COMPLETE`, and marks `RUN_COMPLETED`.
5. The coordinator gives the user one short final result. It does not callback a
   bootstrap or Skill-development task and does not expose internal state names.

If any final callback/release/certainty check fails, set
`RUN_FINALIZATION_BLOCKED`, keep the evidence, and report one concise repair or
decision. Never convert deadline arrival into successful completion.

Keep the active/idle registered pair unarchived unless the user explicitly asks
for full cleanup. When a released executor has been replaced in the registry and
owns no heartbeat, Chrome tab, or uncertain mutation, unpin and archive that
retired executor so it does not remain in the active task list.

### Simple user result

Use one line when finalization succeeds:

```text
运营完成。运行：<duration>；浏览：<count>；收藏：<count>；Repost：<count>；评论：<count>。风险：无｜<one short risk>。
```

If the user stopped early, start with `已安全停止。` instead. Do not show
Heartbeat/callback/registry/release identifiers unless finalization is blocked.

If the executor disappears, first resolve uncertain submissions and incumbent
mutation authority. Create a replacement only with explicit user authorization,
then replace the executor registry and repeat the full handshake. If the
coordinator disappears, the executor stops mutation, releases Chrome, and waits;
it never guesses a new callback destination.
