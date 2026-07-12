# Starter Coordinator And Persistent Executor

Use exactly two user-visible persistent Codex Threads. The starter/install task
becomes the coordinator; it creates one execution Thread. Both TikTok roles use
`gpt-5.6-luna` with `thinking=high`. Never use a collaboration subagent, Goal
Mode, or an agent tree for either role.

Use `$thread-supervisor` for generic registration, callback, work-state,
heartbeat fallback, stop/release, and archival mechanics. Read
`$thread-supervisor/references/canonical-registry.md` and
`$thread-supervisor/references/identity-and-automation.md` before creating either
the executor or an automation. The canonical reference owns serialization,
versioned envelopes, and reconciliation; this reference owns the TikTok-specific
authority split and evidence contract.

Role ownership, the bootstrap-to-coordinator transition, decision boundaries,
and stage exit gates live only in `role-and-stage-contract.md`. Read it before
this reference. This file does not redefine either role; it implements the
registry, scheduler, callback, and finalization mechanics required by that
contract.

## Contents

- Starter self-registration and bootstrap creation
- Stale-owner recovery
- Hard tool and model requirements
- Runtime responsibility handoff
- Durable scheduler and first-install supervision
- Execution envelope and default actions
- Callback schema
- Stop, release, and finalization

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
5. Create and persist the canonical `thread_bootstrap/v1` envelope. It contains
   only run/coordinator identity, the exact Luna/High profile, and
   `external_work=forbidden_until_registry_ack`. Do not create an incomplete
   identity registry with `executor_id=NONE`, and do not duplicate bootstrap
   fields in prose.
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
   the initial executor. Its prompt embeds the stored canonical bootstrap JSON
   once, tells the executor to verify its hash, and says to wait for
   `SELF_REGISTRY` without touching Chrome, TikTok, a ledger, or automations. Do
   not independently restate account, authorization, role prose, direction,
   ledger, or stop time in that prompt.
6. Record the returned executor ID, set its final title to `TikTok 执行台`, and
   explicitly keep it unpinned. Now finalize and persist one
   `thread_identity_registry/v1` generation with structured role codes,
   Luna/High profile, account, ledger, callback target, and writer/tab policies.
   Create separate canonical direction, authority, and mission objects.
7. Send `SELF_REGISTRY` to the exact returned executor ID with Luna/High by
   copying the stored identity-registry bytes. Include its schema, ID,
   generation, byte length, and SHA-256; do not render a prose equivalent.
8. Require the executor to hash the received bytes, store them unchanged, and
   callback `THREAD_READY` with the exact `registry_ref` to the registered
   coordinator ID. Verify callback source, payload IDs, profile, and hash.
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
operation. Do not create another coordinator or casually create another
executor. A definitive stale owner may use the stale-owner replacement below;
pre-Chrome mixed create/SELF snapshots may use exactly one
`REGISTRY_RECONCILIATION` clean replacement. Both require automation cleanup,
old/new ID evidence, one canonical owner, and no second retry. Preserve the
failure evidence.

## TikTok stale-owner recovery

Apply `$thread-supervisor/references/identity-and-automation.md` before reusing
or dispatching any registered executor:

- title, role, search result, preview, readable summary, and `read_thread` cache
  are candidate evidence only; require current-session owner-liveness proof;
- an archived TikTok executor is retired and must not be automatically
  unarchived for reuse;
- `failed to resolve rollout path` plus `file does not exist`/`ENOENT` is
  `STALE_OWNER_TOMBSTONE`, not a TikTok account/platform risk;
- host unavailable, timeout, network, or tool transport errors are
  `LIVENESS_UNVERIFIED_TRANSIENT`; retain the owner and do not replace it from
  that evidence;
- for a tombstone, run the generic stale executor replacement transaction once:
  remove old-target automations, retire the old ID, create one replacement,
  verify exact new ID and mission acknowledgement, bind/read back the new
  operation heartbeat, and prove no orphan automation or duplicate canonical
  owner remains;
- successful same-envelope replacement is internal self-healing. Only a failed
  replacement/handshake/dispatch/binding becomes an orchestration blocker in
  `TikTok 主控台`.

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

## Runtime responsibility handoff

Follow `role-and-stage-contract.md` for the coordinator loop, executor
discretion, risk routing, and mission-change boundary. This mechanics reference
only enforces the accepted canonical references, one active block, callback
identity, exact automation binding, and terminal release proof.

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

## Execution envelope

Every dispatch is a canonical `block_dispatch/v1` object with exact
`registry_ref`, `direction_ref`, `authority_ref`, and `mission_ref`, plus the
bounded block/slot ID, trigger, search clusters, sample parameters, capability
snapshot reference, circuit state, and callback schema version. Full structured
objects are retrieved from their accepted artifacts; do not duplicate them as
hand-written prose in the dispatch.

Before Chrome, reject an unknown or mismatched reference as
`registry_mismatch` and run at most one `REGISTRY_RECONCILIATION`. A legitimate
user change creates and acknowledges a new direction/authority/mission version;
it never edits the identity registry or masquerades as a repair. Never include
a Skill-development/bootstrap task as callback target.

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
registry_ref:
direction_ref:
authority_ref:
mission_ref:
coordinator_thread_id:
executor_thread_id:
executor_generation:
executor_owner_state:
replacement_old_executor_thread_id:
replacement_new_executor_thread_id:
orphan_automation_check: NOT_RUN | CLEAR | FAILED
duplicate_canonical_owner_check: NOT_RUN | CLEAR | FAILED
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

If the executor becomes unreachable, first classify it with the owner-liveness
gate and resolve uncertain submissions. A definitive stale tombstone uses the
single internal replacement transaction without user confirmation. A transient
host/network/tool failure never creates a replacement. If replacement fails,
report an orchestration blocker and stop. If the coordinator disappears, the
executor stops mutation, releases Chrome, and waits; it never guesses a new
callback destination.
