# Startup Health Check And Bootstrap

Use this reference for install, upgrade, or first launch. On a setup/install
request, the first available presentation action is immediately renaming this
same task `TikTok 启动台`. Phase 1 is read-only, ends with a guided user handoff,
and creates no executor. After healthy preflight the same task is promoted in
place to coordinator and immediately renamed `TikTok 主控台`; Phase 2 executor
creation begins only after direction/duration is resolved.

Use `role-and-stage-contract.md` for the `BOOTSTRAP_STARTER` to
`TIKTOK_COORDINATOR` transition and stage exit gates. This file owns preflight
checks and handoff content only.

## Contents

- Phase 1 install and preflight
- Healthy guided handoff
- Resolve the second user message
- Phase 2 pair creation handoff
- Default action envelope
- Healthy started response

## Phase 1 — install and preflight

Record internally:

```text
install_action:
bundle_version:
thread_supervisor_version:
tiktok_skill_version:
github_source: AVAILABLE | UNAVAILABLE
skill_validation: PASSED | FAILED
chrome_control: AVAILABLE | RECONNECTED | UNAVAILABLE
tiktok_session: LOGGED_IN:@handle | LOGGED_OUT | UNVERIFIED
account_warning: NONE_VISIBLE | PRESENT | UNVERIFIED
thread_support: READY | UNAVAILABLE
coordinator_self_registration: PROVABLE | UNAVAILABLE
bootstrap_title: TIKTOK_STARTUP_CONSOLE | DEGRADED_PRESENTATION
role_state: BOOTSTRAP_STARTER | TIKTOK_COORDINATOR
canonical_object_store: WRITABLE | UNAVAILABLE
bootstrap_ref: NONE | exact ref
registry_ref: NONE | exact ref
direction_ref: NONE | exact ref
authority_ref: NONE | exact ref
mission_ref: NONE | exact ref
executor_owner_state: NONE | CANDIDATE_ONLY | LIVE | ARCHIVED_RETIRED | LIVENESS_UNVERIFIED_TRANSIENT | STALE_OWNER_TOMBSTONE | REPLACED
executor_generation:
orphan_automation_check: NOT_RUN | CLEAR | FAILED
duplicate_canonical_owner_check: NOT_RUN | CLEAR | FAILED
model_runtime: coordinator=gpt-5.6-luna/high | executor=gpt-5.6-luna/high | UNAVAILABLE
fast_mode: ACTIVE | INACTIVE | UNVERIFIED
automation_support: AVAILABLE | UNAVAILABLE | NOT_REQUESTED
automation_manager_thread_id: NONE | exact coordinator id
coordinator_heartbeat_id: NONE | exact id
coordinator_heartbeat_target_thread_id: NONE | exact coordinator id
coordinator_heartbeat_repeat: NONE | ON | OFF
coordinator_heartbeat_next_tick_at: NONE | timestamp
operation_timer_state: NONE | ACTIVE | DEGRADED | COMPLETE
operation_timer_stop_at: NONE | timestamp
durable_install_state_path: ${CODEX_HOME:-$HOME/.codex}/state/tiktok-web-operations/install-state.json
first_install_supervision: NOT_APPLICABLE | PENDING | ACTIVE | CONSUMED | DEGRADED
first_install_supervision_checkpoints: NONE | timestamps
dedicated_tab_creation: AVAILABLE | UNAVAILABLE
concurrent_same_account_activity: true | false
recommendation_attribution_contaminated: true | false
exact_mutation_conflict: none | target/action
local_time_check:
ledger_path:
dependency_status: READY | BLOCKED
required_missing: []
repair_actions: []
bootstrap_state: PREFLIGHT_HEALTHY_WAITING_FOR_DIRECTION | BLOCKED
```

Run checks in order:

0. Immediately call the available self-title operation to set
   `TikTok 启动台`. If rename is unavailable, record
   `bootstrap_title=DEGRADED_PRESENTATION` and continue; repair the title at the
   next safe point. Do not create another task to obtain the title.
1. Download the canonical GitHub archive. Require exactly `README.md`,
   `thread-supervisor/`, and `tiktok-web-operations/`; validate both manifests,
   source identity, Skills, agents metadata, and directly referenced files.
2. Follow `version-management.md`: compare numeric versions and managed-tree
   fingerprints, fence genuinely active runtimes, and automatically install or
   upgrade without asking when the incoming bundle is newer. Stage both Skills
   on the target filesystem, replace whole directories, validate both exact
   targets, and roll both back if either replacement fails. Never mix old/new
   files. Upgrade discovery is not a stopping point; after successful installed-
   tree validation continue with step 3 in this same turn.
   On a true first `INSTALL`, create the private installation-state record with
   `first_install_supervision=PENDING`; never place it in either managed Skill
   tree. Upgrade/NOOP/reinstall must preserve an existing consumed state.
3. Prove Chrome control with one disposable `chrome.tabs.new()` tab. Apply the
   exact-code/likely-cause and bounded same-session recovery contract in
   `runtime-and-recovery.md`; retry a dropped control connection at most twice
   and never claim another task's tab. A recovered transient remains internal
   preflight evidence. A temporary failure remains `auto_retry_pending` and does
   not ask the user. Only failure of the sole allowed Chrome control path after
   bounded reconnect enters the hard-blocker whitelist.
4. Open TikTok read-only in that tab, prove the logged-in `@handle`, and inspect
   explicit platform warnings/challenges. Never enter credentials or codes.
5. Prove `list_projects`, `create_thread`, `list_threads`, `read_thread`,
   `send_message_to_thread`, `set_thread_title`, and `set_thread_archived` exist.
   Detect `set_thread_pinned` for automatic main-console pinning; absence is a
   non-blocking presentation limitation.
6. Prove the current starter task can resolve its exact ID through the current
   `TikTok 启动台` identity plus unique nonce `list_threads`/`read_thread` when
   needed. A temporary registration suffix is allowed only for ID proof and must
   return to the lifecycle title immediately.
7. Prove a writable private canonical-object store can persist exact UTF-8 bytes
   and SHA-256 references for bootstrap, identity registry, direction,
   authority, and mission objects. Prove mutable owner/automation/progress/resume state is
   stored separately. Do not use natural-language summaries as canonical data.
8. Prove executor creation and operational dispatch support
   `model=gpt-5.6-luna` with `thinking=high`. This TikTok profile is mandatory.
   Record Fast Mode only when independently visible; it is not a creation gate.
9. When unattended/timed continuation is requested, prove `automation_update`
   can create and view repeat-on heartbeats with explicit `targetThreadId`, a
   finite `UNTIL` or equivalent stop guard, next-run readback, and local/UTC
   schedule evidence. Do not create real operating heartbeats during Phase 1.
10. Inspect active TikTok tasks only to detect tab ownership, attribution
   contamination, and exact-target/action submission collisions. Other Chrome
   tabs and other same-account runs are allowed, including different-target
   mutations. Record concurrent activity and contamination; block only this
   executor's unresolved submission or the exact colliding target/action.
11. Read local time and create a writable private ledger path. Initialize every
   mutation lane independently without modifying TikTok.
12. Finalize only the disposable bootstrap tab and release its control session.
    Record browser authority revoked, promote the same exact task ID from
    `BOOTSTRAP_STARTER` to `TIKTOK_COORDINATOR`, immediately rename it
    `TikTok 主控台`, and preserve its history/pin. Rename failure is presentation-
    only degradation; do not create a replacement main task or block handoff.

Do not use `blocked` for missing preferences, temporary tool transport, another
Chrome owner, route/page failure, or a capability lane. Retry/degrade internally
and keep the handoff moving. If a required orchestration capability remains
unavailable, report `auto_retry_pending` or one concrete capability limitation,
not a confirmation request. Ask the user and end with `完成后回复“继续”` only for
the live hard-blocker whitelist in `blocker-minimization.md`. Never use this
handoff merely because a valid newer bundle was found; that case must have been
upgraded automatically above.

## Healthy guided handoff

When Phase 1 is healthy, first promote the same task in place to
`TIKTOK_COORDINATOR` and apply the final title `TikTok 主控台`; then return only:

```text
状态健康。当前账号：@handle。
你想把这个账号运营成什么方向或人设？方向会决定后续搜索、浏览、收藏、Repost、评论，以及未来内容的主题与语气，帮助形成更一致的受众信号；但不能保证具体推荐或分发结果。
也请告诉我希望运行多久。你可以回复“北美大学生 / dorm life，运行 3 小时”；如果暂时没想法，直接回复“继续”，我会按默认方向和默认 3 小时开始。
```

Then stop and wait. Do not create the executor, dispatch work, search TikTok,
mutate TikTok, or claim startup.

If the bundle is already installed and the incoming user message already
contains a clear operating direction/duration or accepts defaults, use the
direct-mission fast path: immediately title/promote this same task as
`TikTok 主控台`, run only reusable quick health checks, resolve the mission, and
continue to Phase 2 in the same turn. Do not repeat the full setup handoff. A
rename-tool failure remains non-blocking presentation degradation.

## Resolve the second user message

Build `persona_name`, `target_audience`, `region_language`, `content_pillars`,
`excluded_topics`, `voice_and_comment_style`, `search_seed_clusters`,
`future_post_alignment`, `duration`, and `operation_stop_at`.

- Explicit fields override defaults.
- Missing direction defaults to North American college/dorm life.
- Default direction uses North America / English. A supplied universal direction
  with missing region/language defaults to `global English with North American
  bias`; record this reversible assumption and start. Match proactive comments
  to the qualified video's language.
- Missing duration defaults to 3 hours at standard intensity.
- Missing intensity, sub-pillar mix, tone detail, or future format uses safe
  documented defaults and never blocks pair creation.
- `继续` or `开始` after healthy handoff accepts all defaults.
- Ask one question only when the missing value changes an irreversible action,
  expands authorization, selects a materially different account/audience, or
  requires human-only platform work. Otherwise disclose the assumption once and
  start.
- Describe direction as a coherent audience-signal hypothesis, not guaranteed
  reach.

Default pillars are roommate move-in/storytime/chaos, dorm/freshman
move-in/setup, college day-in-my-life/campus routine/GRWM, campus friends/game
day/tailgate, and finals/dorm survival failures. Exclude admissions, SAT/GPA,
application advice, pure study motivation, and generic non-campus content.

## Phase 2 — keep the promoted coordinator and create one executor

Follow `role-and-stage-contract.md` for ownership/stages and
`operating-model.md` for mechanics:

1. Reuse the exact same task ID already promoted from `TikTok 启动台` to
   `TikTok 主控台`; never create another main task. Resolve/verify its ID, persist
   one canonical inert bootstrap envelope, and pin it. If the final title could
   not be applied earlier, retry it now without blocking operation.
2. Create one executor with `gpt-5.6-luna/high`. Its initial prompt embeds only
   the stored bootstrap JSON once and requires it to wait for `SELF_REGISTRY`;
   it must not contain a second prose copy of account/role/authorization/
   direction/ledger/stop fields. Record the returned ID, set its final title to
   `TikTok 执行台`, and keep it unpinned.
3. Only now finalize the canonical identity-registry generation plus versioned
   direction/authority/mission objects. Copy the stored identity bytes through
   `SELF_REGISTRY`, then require a nonce-bound `THREAD_READY` that echoes the
   exact `registry_ref`. A title, summary, paraphrase, list/search result, or
   readable cached turn is not equivalent.
4. Dispatch one Luna/High read-only `stability_smoke_01`: assess three cards from
   one direction query, open one strong-core result from search, verify direct
   post identity/playback and premise/payoff, then separately attempt up to five
   continuous For You identities through the unique native next/down control.
5. Require three assessed cards, at least one `qualified_search_view`, stable
   account/tab control, parseable incremental ledger, and zero mutation. For You
   success verifies the optional validation lane; native-feed failure alone
   degrades that lane and does not block search-led operation.
6. The real continuous mission starts immediately in this user turn and must
   produce accepted first search-training proof; do not wait for a timer to
   establish baseline capability.
7. If the resolved duration may span more than one model/runtime turn, the
   verified coordinator creates one long-running repeat-on
   `coordinator_heartbeat`, normally hourly, targeting its exact coordinator ID
   with finite cutoff protection. View it and verify exact ID, target, repeat-on,
   next run, local/UTC schedule, and deadline. Normal continuation remains
   executor callback -> immediate coordinator resume. The executor never manages
   the timer; an executor-targeted operation Heartbeat is invalid.
8. If durable install state is `PENDING`, the coordinator Heartbeat consumes the
   one-time first-hour checks near `+15/+35/+60`, capped by stop time. It reads
   only executor turns/callbacks, recent ledger progress, resume state, and
   deadline; it never touches TikTok.
9. Only after primary smoke and the required binding verifies may unattended
   continuation begin. Keep both tasks persistent and unarchived; pin only the
   coordinator. Missing repeat/wake/proof is
   `SCHEDULER_CONTINUATION_FAILURE`, not successful persistence. Page, network,
   Chrome, route, client-block, or lane failure must leave the correctly bound
   coordinator Heartbeat repeat-on for a later automatic recovery wake.

If creation, registry, callback, or smoke fails, do not casually create another
task or claim stable operation. A definitive `STALE_OWNER_TOMBSTONE` uses its
one-attempt replacement transaction. A pre-Chrome create/SELF/hash conflict uses
one `REGISTRY_RECONCILIATION`; if the executor accepted mixed snapshots, the
verified coordinator may retire it and create exactly one clean replacement.
Host/network/tool transients never authorize replacement.

## Default action envelope

- Defaults fill only fields absent from the latest explicit user instruction.
- Post like is disabled when not requested. An explicit latest request moves it
  to `pending_fresh_gate`; an old mission failure is historical evidence only.
- Favorite, TikTok Repost, and proactive comments may be selectively used on
  strong-core posts only after their own persistence gates pass.
- Favorite requires immediate, +3 second, +10 second, reopen, and account proof.
- Repost means only TikTok's explicit Repost control, never generic Share.
- Comments are contextual, preferably 2-12 words, never over 30 words, and each
  must survive reload verification.
- Never set engagement quotas or infer ranking effects.

## Healthy started response

Only after first proof, report:

```text
已启动。当前账号：@handle。
方向：resolved persona / audience。
时长：duration；预计结束：local date and time。
搜索训练：已验证从搜索实际点开并观看 strong-core 视频。
For You 验证：verified | degraded | unavailable（仅作为留出验证）。
互动：当前已启用的独立 lanes；未通过持久化 gate 的仍关闭。
```

Do not say only `已启动` when the primary search-origin consumption proof is
missing. Do not imply For You alignment merely because search cards are core.
