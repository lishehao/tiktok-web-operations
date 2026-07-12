# Role And Stage Contract

This is the single authority for who does what and when in a persistent TikTok
run. `operating-model.md` owns transport, registry, callback, scheduler, and
finalization mechanics; content references own block-level TikTok rules. If
another file restates a role or phase, this contract wins.

## Contents

- Role transition
- Steady-state role cards
- Decision boundary
- Stage machine
- Callback events
- Mission changes
- Heartbeat meaning
- Failure routing
- Prompt shape
- Audit checklist

## Role transition

The user's first task has two sequential identities, never two simultaneous
missions:

1. `BOOTSTRAP_STARTER`: install/upgrade, run disposable read-only preflight,
   return the direction/duration handoff, then wait. No executor exists.
2. `TIKTOK_COORDINATOR`: only after the user's second message and exact
   self-registration. Before this transition, finalize the bootstrap tab and
   release browser control. From this point onward the task is `TikTok 主控台`
   and never touches Chrome/TikTok.

`BOOTSTRAP_STARTER` is a temporary stage role, not a third persistent Thread.
Steady state has exactly two user-visible Threads: one coordinator and one
executor.

## Steady-state role cards

### TikTok 主控台

```text
objective: decide the next bounded block or stop the run.
owns: user conversation; direction/authority/mission versions; canonical
identity; block selection; scheduler; callback acceptance; aggregate progress;
risk decisions; executor replacement transaction; finalization.
reads: structured callbacks, heartbeat readbacks, aggregate or targeted ledger
evidence when validation needs it.
writes: canonical control objects and mutable coordinator state; never the raw
per-item execution ledger.
outputs: one accepted dispatch, one consolidated decision/risk message, one
verified heartbeat receipt, or one final result.
never: open/control Chrome; inspect TikTok UI; classify individual videos;
draft a context-dependent comment; click an action; write raw per-item evidence;
dispatch overlapping blocks; ask the executor to choose the run strategy.
```

The coordinator answers: **what bounded outcome should happen next, under which
versioned constraints?**

### TikTok 执行台

```text
objective: finish exactly one accepted bounded block, prove it, release Chrome,
callback, and become idle.
owns: its current-session dedicated tab; live TikTok/UI judgment; candidate
qualification inside the dispatched search/query set; contextual comment draft;
authorized action execution; persistence proof; raw per-item ledger appends.
reads: accepted canonical references, one block payload, ledger tail needed to
avoid duplication, and current page/platform state.
writes: raw execution ledger and exactly one structured callback per block/event.
outputs: THREAD_READY, BLOCK_RESULT, RISK_EVENT, or EXECUTOR_RELEASED.
never: choose or change the account direction; expand search pillars or action
authority; set duration/cadence; create/update/delete Heartbeats; create Threads;
replace itself; ask the user a question; speak to another coordinator; start a
second block; continue after its terminal callback.
```

The executor answers: **which concrete items inside this block satisfy the
supplied constraints, and what actually happened?**

## Decision boundary

Use this boundary instead of letting both Threads “do strategy”:

| Decision | Owner |
|-|-|
| Persona, audience, region/language, pillars, exclusions | 主控台 |
| Which block type runs next and its search clusters/sample bounds | 主控台 |
| Whether an action lane is authorized or suspended | 主控台 from user instruction/current proof |
| Which result card/video inside the supplied cluster is strong-core | 执行台 |
| Whether live context supports a specific short comment | 执行台 |
| Exact comment text within the approved voice and 30-word ceiling | 执行台 |
| Whether persisted UI evidence passes the lane gate | 执行台 records; 主控台 accepts/rejects capability delta |
| Whether aggregate evidence warrants a new query cluster or phase | 主控台 |
| Cadence, heartbeat binding, pause, resume, and stop | 主控台 |
| Current page recovery inside the bounded budget | 执行台 |
| User decision after a true blocker | 主控台 only |

Local executor discretion is narrow. It may skip irrelevant/unsafe candidates,
use another query already listed in the block, and choose zero interactions. It
may not invent a new audience, pillar, action type, quota, or recovery method.

## Stage machine

Every run occupies exactly one stage. Each transition requires its exit proof.

| Stage | Active owner | Work | Required exit proof | Next |
|-|-|-|-|-|
| `S0_PREFLIGHT` | BOOTSTRAP_STARTER | Install/upgrade; disposable Chrome/TikTok read-only checks; tool/model/time/store checks | Healthy handoff; bootstrap tab finalized; browser authority released | `S1_MISSION` |
| `S1_MISSION` | BOOTSTRAP_STARTER + user | Resolve direction, region/language, duration, action envelope | User's second message resolved into canonical direction/authority/mission inputs | `S2_PAIR_BOOTSTRAP` |
| `S2_PAIR_BOOTSTRAP` | 主控台; 执行台 inert | Self-register coordinator; canonical bootstrap; create executor; finalize registry; SELF_REGISTRY/THREAD_READY | Exact IDs/profile/hash/callback target accepted; executor idle; zero external work | `S3_RUNTIME_SMOKE` |
| `S3_RUNTIME_SMOKE` | 执行台 executes; 主控台 accepts | One read-only stability smoke | Required search-origin proof, account/tab stability, parseable ledger, zero mutation; executor released/idle | `S4_FIRST_BLOCK` |
| `S4_FIRST_BLOCK` | 执行台 executes; 主控台 accepts | First real bounded block immediately | `BLOCK_RESULT` accepted, ledger/capability/risk reconciled, no unresolved action | `S5_SCHEDULED_RUN` or `S7_FINALIZE` |
| `S5_SCHEDULED_RUN` | 主控台 schedules; 执行台 handles one slot | Repeating bounded blocks; separate held-out validation; sparse authorized actions | Every due slot has one wake, terminal block callback, released tab, reconciled proof | remain or `S6_PAUSED`/`S7_FINALIZE` |
| `S6_PAUSED` | 主控台 owns pause; 执行台 idle | Consolidate risk; wait for user only if required, otherwise test exact auto-resume condition in an authorized recheck slot | User decision or verified external-state clearance; new version refs acknowledged if changed | `S5_SCHEDULED_RUN` or `S7_FINALIZE` |
| `S7_FINALIZE` | 主控台 requests; 执行台 releases | STOP_AND_RELEASE; no new browse/mutation; remove timers after proof | `EXECUTOR_RELEASED`, zero unresolved submission, final ledger reconciled, exact run Heartbeats retired | `S8_IDLE_COMPLETE` |
| `S8_IDLE_COMPLETE` | 主控台 | One compact user result; registered pair remains idle unless cleanup requested | Final result delivered | terminal |

No stage may be skipped by a timer. A Heartbeat firing never supplies an exit
proof. `BLOCK_RESULT` completes one block, not the run.

## Callback events

Use four semantic events; the detailed field schema remains in
`operating-model.md`:

- `THREAD_READY`: executor accepted canonical identity and is inert/idle.
- `BLOCK_RESULT`: one bounded block ended with completed/blocked/validation
  status, evidence summary, capability delta, tab release, and next-block input.
- `RISK_EVENT`: immediate terminal result for current block after bounded
  recovery; includes `decision_required` and exact resume condition.
- `EXECUTOR_RELEASED`: whole-run terminal release proof; no new external work.

The executor sends only to the canonical coordinator. After any callback it is
idle. It never asks the user to interpret the callback.

## Mission changes

The coordinator is the sole writer of new direction/authority/mission versions:

- Stop, account change, or authorization revocation interrupts safely and moves
  toward `S6_PAUSED` or `S7_FINALIZE`.
- A new direction, intensity, query plan, or expanded authority normally becomes
  a pending version for the next block. Do not mix old and new constraints in
  one block.
- If the executor is running, do not dispatch a second block. Send a mid-block
  amendment only when continuing the old block would violate the latest user
  instruction or create material waste/risk.
- The executor acknowledges the new references before acting. It does not merge
  versions or infer what changed from prose.

## Heartbeat meaning

Heartbeats are wake signals, not roles or agents:

- `operation_heartbeat` wakes only `TikTok 执行台` for one deterministic slot.
- `supervisor_heartbeat` wakes only `TikTok 主控台` to read state and verify the
  continuation chain.
- Neither Heartbeat creates a third Thread, owns strategy, or proves work.
- The executor never manages either Heartbeat. The coordinator never uses the
  supervisor wake to operate TikTok or dispatch over a running block.
- A wrong target/role produces `MISBOUND_HEARTBEAT_NO_ACTION`.

## Failure routing

| Evidence | Executor action | Coordinator action |
|-|-|-|
| Recoverable page/network transient | Recover once inside budget; record; finish block | Mention only in normal receipt if recovered |
| Feed validation transition failure | End validation lane; preserve search work; callback | Degrade only that lane; choose next search block |
| Current CAPTCHA/login/rate-limit/warning | Stop affected work; release; `RISK_EVENT` | Consolidate one user decision or exact auto-resume wait |
| Uncertain submission | Do not retry; resolve certainty if possible; release/callback | Freeze conflicting action and ask only if evidence cannot resolve it |
| Registry/target mismatch before Chrome | Zero external work; callback | One reconciliation transaction; at most one clean replacement |
| Deadline/user stop | No new work; `EXECUTOR_RELEASED` transaction | Retire exact Heartbeats after release and finalize |

All risk returns to `TikTok 主控台`. The executor's user-visible final text may
only state that it sent the result to the main console and is idle.

## Prompt shape

Keep role prompts short and stable.

Coordinator prompt:

```text
ROLE=TIKTOK_COORDINATOR
OBJECTIVE=choose the next bounded block or stop
CANONICAL_REFS=<refs>
CURRENT_STAGE=<stage>
NEVER=Chrome/TikTok/raw-ledger-write/overlapping-dispatch
```

Executor bootstrap prompt:

```text
ROLE=TIKTOK_EXECUTOR
OBJECTIVE=execute one accepted block, prove, release, callback, idle
BOOTSTRAP_REF=<exact ref>
EXTERNAL_WORK=forbidden_until_registry_ack
NEVER=strategy/user-question/scheduler/thread-creation/self-replacement
```

The detailed mission is a canonical object plus bounded block payload, not a
second role description. Do not paste the entire Skill or historical ledger into
either prompt.

## Audit checklist

- Exactly one coordinator and one executor are canonical.
- The bootstrap role ended and its disposable tab was finalized before the
  coordinator role began.
- The coordinator has no Chrome/TikTok/raw-ledger ownership.
- The executor has no strategy/scheduler/user-decision authority.
- One stage is recorded; the prior stage has exit proof.
- One accepted block is active at most.
- Candidate-level discretion remains inside supplied clusters and authority.
- Every block ends with tab release, one callback, and idle executor state.
- Operation/supervisor Heartbeats wake the correct roles and are not treated as
  agents or completion proof.
- Risks and final completion return only through `TikTok 主控台`.
