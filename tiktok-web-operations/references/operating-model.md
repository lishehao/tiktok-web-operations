# Main Thread And Subordinate Driver Model

Use one user-owned TikTok main Thread and exactly one subordinate Chrome driver agent spawned inside that Thread. The main Thread owns the system; no Skill-development or external coordinator Thread participates in runtime operations.

## Topology

```text
User
  └─ TikTok main Thread (`main_coordinator`)
       └─ spawned subordinate agent (`chrome_driver`)
```

The main coordinator is the only user-facing operational agent. The subordinate is the only Chrome operator. Do not create another user-owned Codex Thread for the driver, do not keep a third analyst agent, and do not let the child spawn descendants.

## Startup contract

When the user asks the main Thread to start persistent TikTok operation:

1. Declare `main_coordinator` and read the relevant Skill references.
2. Create a long-running goal only when the user explicitly requested persistent or continuing operation.
3. Establish account, audience ontology, search clusters, exclusions, calibration mode, capability matrix, autonomous-comment envelope, ledger path, and stop conditions.
4. Spawn exactly one subordinate agent named for the Chrome-driver role. Pass only the execution envelope and the parent agent path; do not pass an external Codex Thread callback ID.
5. Record the child agent path and keep it as the sole driver. Reuse it with `followup_task`; do not spawn a new child for every block.

If the collaboration/subagent tools are unavailable, report that the two-agent system cannot start. Do not silently replace the child with a second user-owned background Thread.

## Authority split

| Concern | Main coordinator | Subordinate Chrome driver |
|-|-|-|
| User conversation and goal | Owns | Never owns |
| Audience ontology and query strategy | Owns | Follows the current envelope |
| Standing authorization and exact decisions | Owns | Executes only matching authority |
| Child lifecycle and next-block dispatch | Owns | Cannot spawn or replace agents |
| Chrome and TikTok UI | Must not touch while child exists | Sole owner |
| Raw event/action ledger | Read-only consumer | Sole writer |
| Capability evidence | Interprets and changes policy | Collects immediate, reload, and account-level proof |
| Final reporting | Owns | Returns structured block results to parent |

## Main coordinator loop

1. Read the last child result and ledger checkpoint.
2. Reconcile core/directional/drift shares, query quality, capability changes, authorization state, and risks.
3. Decide the next bounded block: `search_heavy`, `mixed`, `feed_led`, capability verification, publishing execution, or safe stop.
4. Send one concrete follow-up task to the existing child with acceptance criteria and the current envelope.
5. Wait for the child result or a collaboration message. Do not operate Chrome locally and do not poll unrelated Codex Threads.
6. Report to the user only when requested, when a decision is genuinely needed, or when a meaningful checkpoint/risk occurs.

The main coordinator may continue this loop under its own goal. The child does not need its own persistent goal; it performs bounded blocks and returns control.

## Subordinate driver loop

For each assigned block:

1. Confirm it is the sole Chrome driver and verify the logged-in account.
2. Read the execution envelope, current mode, capability matrix, ledger tail, and stop conditions.
3. Execute only the bounded block described in `persistent-feed-operations.md` or the exact authorized action.
4. Write raw events and verification evidence to the driver-owned ledger.
5. Release or safely hand off Chrome ownership when the block finishes or stops.
6. Return one structured result to the parent and become idle. Wait for `followup_task`; do not start another block independently after returning.

The child may message the parent mid-block only for a new blocker, key risk, authorization mismatch, hard runtime change, or uncertain submission. Use the collaboration parent path, never Codex App thread messaging.

## Execution envelope

Each child dispatch includes:

- Parent agent path.
- Exact TikTok account and Chrome ownership rule.
- Target audience, core/adjacent/excluded ontology, language, and region.
- Approved search/hashtag/creator/sound clusters.
- Current calibration mode, block parameters, and latest core/directional/drift shares.
- Capability matrix and disabled lanes.
- Comment authorization mode, voice, hard 30-word maximum, exclusions, and revocation state.
- Ledger path and sole-writer rule.
- Exact action authority when applicable.
- Hard stop conditions and expected result schema.

Do not include a Skill-development Thread ID or instructions to call `send_message_to_thread`.

## Authorization protocol

The main coordinator owns all authorization. For actions outside a standing envelope:

1. Child returns a candidate packet to the parent.
2. Main coordinator reviews it and obtains the user's exact decision when needed.
3. Main sends the exact approved packet to the existing child with `followup_task`.
4. Child verifies the live URL/account/text, executes once, verifies persistence, and returns the result.

For `autonomous_comment_mode`, the main sends the complete standing envelope once and keeps it in coordinator state. The child may publish matching proactive top-level comments without per-item approval, must reload-verify every send, and must stop that lane on the first new persistence failure, removal, warning, throttle, challenge, uncertain submission, account mismatch, or hard browser/runtime change. A proven soft control reconnect preserves the envelope.

## Result protocol

Return one object or clearly structured report after every bounded block:

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

Routine successful comments and read-only events stay in the ledger during the block. The block result aggregates them for the parent; it is not sent to another Codex Thread.

## Lifecycle and recovery

- Keep exactly one subordinate driver alive or idle at a time.
- Use `followup_task` to reuse an idle child. Use `send_message` only for tightly related mid-run corrections or risk prevention.
- Use `interrupt_agent` when the user stops operation or the child must release Chrome immediately.
- If the child disappears, confirm Chrome ownership and uncertain submissions before spawning a replacement.
- On user stop, main interrupts the child, requires Chrome release and a final ledger checkpoint, then ends its own operating goal. The Skill-development Thread remains uninvolved.
- Archive or retire a user-owned main Thread only at the user's request; subordinate-agent cleanup belongs to that main Thread.

## Single-agent fallback

Use a single Thread that combines coordinator and driver roles only when the user explicitly asks not to use the two-agent architecture or collaboration tools are unavailable and the user accepts the fallback. Keep Chrome serialization, authorization, verification, and ledger rules unchanged.
