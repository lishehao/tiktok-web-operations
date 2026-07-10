# Two Persistent Thread Operating Model

Use two separate user-owned Codex Threads. Both are persistent sidebar tasks and both run `gpt-5.6-luna` with `thinking=high`. Never use a collaboration subagent for either role.

## Topology

```text
Temporary bootstrap task
  ├─ TikTok 运营主任务 (`coordination_thread`, Luna/High)
  └─ TikTok Chrome执行任务 (`execution_thread`, Luna/High)

After registration and handshake: archive temporary bootstrap task.
```

The two operational Threads are peers connected by registered Thread IDs. The coordinator is user-facing and owns decisions. The executor is the only Chrome operator and owns raw evidence.

## Bootstrap creation contract

After read-only dependency preflight:

1. Use `list_projects` to select the current saved project when one is clearly available; otherwise create both as projectless local Threads. Use the same target type for both.
2. Create `coordination_thread` with `create_thread(model="gpt-5.6-luna", thinking="high")`. Its initial prompt must identify the Skill, role, account/audience defaults, and instruct it to wait for the executor registry without touching Chrome.
3. Record the returned coordinator Thread ID and set title `TikTok 运营主任务`; pin it when the pin tool is available.
4. Create `execution_thread` with `create_thread(model="gpt-5.6-luna", thinking="high")`. Its initial prompt must include the coordinator Thread ID, the Skill, sole Chrome ownership, ledger path, envelope, callback schema, and an instruction to send `THREAD_READY` to the coordinator with `send_message_to_thread` before doing mutations.
5. Record the returned executor Thread ID and set title `TikTok Chrome执行任务`; pin it when available.
6. Send the executor registry and full operating envelope to the coordinator with `send_message_to_thread(model="gpt-5.6-luna", thinking="high")`.
7. Read the latest turns from both Threads. Require a two-way handshake: coordinator knows the exact executor ID, executor knows the exact coordinator ID, and the coordinator received executor `THREAD_READY` through `send_message_to_thread`.
8. The coordinator sends the first bounded block to the executor using its registered ID and Luna/High override. The executor begins only after the registry matches.
9. Navigate the Codex app to the coordinator when supported. Archive the temporary bootstrap task only after both Threads, handshake, and first dispatch are verified.

The bootstrap task is not an operating Thread. If creation or handshake partially fails, do not operate TikTok. Archive only the empty Threads created by this failed bootstrap, preserve evidence, and return one repair action.

## Hard tool and model requirements

Require these Codex App thread capabilities:

- `list_projects`
- `create_thread`
- `read_thread`
- `send_message_to_thread`
- `set_thread_title`
- `set_thread_archived`

`set_thread_pinned` and `navigate_to_codex_page` are optional presentation features.

Require `gpt-5.6-luna` with `thinking=high` for both thread creation and every operational cross-thread dispatch. The user explicitly selected this combination; do not fall back silently.

## Authority split

| Concern | Coordination Thread | Execution Thread |
|-|-|-|
| User conversation and strategy | Owns | Never owns |
| Audience/search strategy | Owns | Executes current envelope |
| Authorization and decisions | Owns | Matches exact authority |
| Thread registry and lifecycle | Owns | Cannot create/replace Threads |
| Chrome and TikTok | Never touches | Sole owner |
| Raw ledger | Read-only consumer | Sole writer |
| Capability evidence | Interprets policy | Collects immediate/reload/account proof |
| Reports | User-facing | Structured callback to coordinator |

## Coordinator loop

1. Receive an executor callback; read only the latest relevant 1–3 turns when more evidence is needed.
2. Reconcile composition, query quality, capability changes, authorization, pending decisions, and risk.
3. Decide the next bounded block or safe stop.
4. If no user decision is needed, send one concrete next block to the same executor ID with `send_message_to_thread`, `model=gpt-5.6-luna`, and `thinking=high`.
5. Mark the executor `running_current_task` and end the coordinator turn. Do not poll, touch Chrome, or busy-wait.
6. Let the executor callback trigger the next coordinator turn.

Queue unrelated next work while the executor is running. Send an immediate amendment only when it corrects/overrides the current block or prevents unsafe/wasted work.

## Executor loop

For each message from the registered coordinator ID:

1. Verify sender/registry, exact account, sole Chrome ownership, capability matrix, ledger tail, and stop conditions.
2. Execute only the bounded block or exact authorized action.
3. Write raw events and persistence evidence to the sole ledger.
4. Release Chrome control at block completion or blocker.
5. Send one structured callback to the coordinator ID with Luna/High override.
6. Become idle. Never start the next block independently and never create another Thread or subagent.

Send a mid-block callback only for `blocked`, `validation_failed`, `needs_decision`, `key_risk`, authorization mismatch, hard runtime change, or uncertain submission.

## Execution envelope

Every dispatch includes:

- Coordinator and executor Thread IDs.
- Exact TikTok account and sole Chrome ownership.
- Target audience, core/adjacent/excluded ontology, language, and region.
- Approved search/hashtag/creator/sound clusters.
- Current calibration mode and sample parameters.
- Capability matrix and disabled lanes.
- Comment authorization, voice, hard 30-word maximum, exclusions, and revocation state.
- Ledger path and sole-writer rule.
- Exact action authority when applicable.
- Stop conditions and callback schema.

Never include a Skill-development or bootstrap callback ID.

## Authorization protocol

For actions outside a standing envelope:

1. Executor returns a candidate packet to the coordinator.
2. Coordinator obtains the user's exact decision.
3. Coordinator sends the approved packet to the same executor Thread.
4. Executor verifies live URL/account/text, executes once, verifies persistence, and callbacks the result.

Under `autonomous_comment_mode`, the executor may publish matching proactive top-level comments without per-item approval, must reload-verify every send, and must stop that lane on the first failure, removal, warning, throttle, challenge, uncertainty, account mismatch, or hard runtime change.

## Callback schema

```text
status: completed | blocked | validation_failed | needs_decision | key_risk
block_id:
summary:
sample_counts:
composition:
queries_used:
actions_performed:
mutations_count:
capability_matrix_delta:
risks:
ledger_path:
recommended_next_block:
```

## Persistence and recovery

- Keep both user-owned Threads idle between turns; idleness does not end persistence.
- Prefer soft-hook callbacks. Use a heartbeat only for an explicitly time-based wakeup, an unreliable callback path, or an explicit user request.
- On user stop, coordinator sends `STOP_AND_RELEASE` to the executor. Executor releases Chrome, writes a final checkpoint, callbacks `completed`, and both Threads remain idle and unarchived.
- Archive either operating Thread only when the user explicitly asks.
- If the executor disappears or becomes unusable, coordinator first checks uncertain submissions and Chrome ownership. Create a replacement persistent Luna/High executor only with explicit user authorization, update the registry, and repeat the handshake.
- If the coordinator disappears, executor stops mutation, releases Chrome, and waits. It must not redirect reports to another Thread by guesswork.

## No fallback

Do not replace this topology with a subagent, agent tree, single combined Thread, different model, or different thinking level. If a hard requirement is unavailable, report the exact blocker before TikTok operation starts.
