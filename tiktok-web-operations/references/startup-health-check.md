# Startup Health Check And Bootstrap

Use this reference for install, upgrade, or first launch. Phase 1 is read-only,
ends with a guided user handoff, and creates no executor. Phase 2 begins only
after the healthy user supplies direction/duration or accepts defaults. The
starter task itself becomes the coordinator.

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
run_registry: WRITABLE | UNAVAILABLE
executor_owner_state: NONE | CANDIDATE_ONLY | LIVE | ARCHIVED_RETIRED | LIVENESS_UNVERIFIED_TRANSIENT | STALE_OWNER_TOMBSTONE | REPLACED
executor_generation:
orphan_automation_check: NOT_RUN | CLEAR | FAILED
duplicate_canonical_owner_check: NOT_RUN | CLEAR | FAILED
model_runtime: coordinator=gpt-5.6-luna/high | executor=gpt-5.6-luna/high | UNAVAILABLE
fast_mode: ACTIVE | INACTIVE | UNVERIFIED
automation_support: AVAILABLE | UNAVAILABLE | NOT_REQUESTED
automation_manager_thread_id: NONE | exact coordinator id
operation_heartbeat_id: NONE | exact id
operation_heartbeat_target_thread_id: NONE | exact executor id
operation_heartbeat_repeat: NONE | ON | OFF
operation_heartbeat_next_tick_at: NONE | timestamp
supervisor_heartbeat_id: NONE | exact id
supervisor_heartbeat_target_thread_id: NONE | exact coordinator id
supervisor_heartbeat_repeat: NONE | ON | OFF
supervisor_heartbeat_next_tick_at: NONE | timestamp
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
   preflight evidence; persistent failure reports exact code, `可能原因`, attempted
   actions, and one user repair without clearing cookies or switching browsers.
4. Open TikTok read-only in that tab, prove the logged-in `@handle`, and inspect
   explicit platform warnings/challenges. Never enter credentials or codes.
5. Prove `list_projects`, `create_thread`, `list_threads`, `read_thread`,
   `send_message_to_thread`, `set_thread_title`, and `set_thread_archived` exist.
   Detect `set_thread_pinned` for automatic main-console pinning; absence is a
   non-blocking presentation limitation.
6. Prove the current starter task can self-rename and can later resolve its exact
   ID through unique-title `list_threads` plus `read_thread`. Phase 1 may use a
   temporary nonce/title and then restore a user-friendly bootstrap title.
7. Prove a writable private run registry can store exact task identity, owner
   liveness/generation/retirement/replacement state, automation management/
   targets, authority, ledger, slot state, and stop fields.
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

If blocked, return only the first repairable issue and impact, ending with
`完成后回复“继续”`. A blocked `继续` rechecks only that item and is not an
operation start command. Never use this blocked handoff merely because a valid
newer bundle was found; that case must have been upgraded automatically above.

## Healthy guided handoff

When Phase 1 is healthy, return only:

```text
状态健康。当前账号：@handle。
你想把这个账号运营成什么方向或人设？方向会决定后续搜索、浏览、收藏、Repost、评论，以及未来内容的主题与语气，帮助形成更一致的受众信号；但不能保证具体推荐或分发结果。
也请告诉我希望运行多久。你可以回复“北美大学生 / dorm life，运行 3 小时”；如果暂时没想法，直接回复“继续”，我会按默认方向和默认 3 小时开始。
```

Then stop and wait. Do not create the executor, dispatch work, search TikTok,
mutate TikTok, or claim startup.

## Resolve the second user message

Build `persona_name`, `target_audience`, `region_language`, `content_pillars`,
`excluded_topics`, `voice_and_comment_style`, `search_seed_clusters`,
`future_post_alignment`, `duration`, and `operation_stop_at`.

- Explicit fields override defaults.
- Missing direction defaults to North American college/dorm life.
- Default direction uses North America / English. For a custom direction with
  missing region/language, ask one necessary question when the fields cannot be
  safely inferred; never silently choose Chinese or English for a broad topic.
- Missing duration defaults to 3 hours at standard intensity.
- `继续` or `开始` after healthy handoff accepts all defaults.
- Ask one question only for a material choice that cannot be safely inferred.
- Describe direction as a coherent audience-signal hypothesis, not guaranteed
  reach.

Default pillars are roommate move-in/storytime/chaos, dorm/freshman
move-in/setup, college day-in-my-life/campus routine/GRWM, campus friends/game
day/tailgate, and finals/dorm survival failures. Exclude admissions, SAT/GPA,
application advice, pure study motivation, and generic non-campus content.

## Phase 2 — keep this task and create one executor

Follow `operating-model.md` exactly:

1. Temporarily rename this task `TikTok 主控台注册 · <run_nonce>`, resolve and verify its
   exact Thread ID, create the immutable run registry with automation manager
   equal to that coordinator ID, then set the final title to `TikTok 主控台` and pin it.
2. Create one executor with `gpt-5.6-luna/high`, record its returned ID, set its
   final title to `TikTok 执行台`, keep it unpinned, and include the
   coordinator ID and require it to wait for `SELF_REGISTRY`.
3. Send the exact returned executor ID through `SELF_REGISTRY`, then require a
   nonce-bound `THREAD_READY`/owner-liveness callback to the coordinator. A
   title, summary, list/search result, or readable cached turn is not equivalent.
4. Dispatch one Luna/High read-only `stability_smoke_01`: assess three cards from
   one direction query, open one strong-core result from search, verify direct
   post identity/playback and premise/payoff, then separately attempt up to five
   continuous For You identities through the unique native next/down control.
5. Require three assessed cards, at least one `qualified_search_view`, stable
   account/tab control, parseable incremental ledger, and zero mutation. For You
   success verifies the optional validation lane; native-feed failure alone
   degrades that lane and does not block search-led operation.
6. The first real bounded block runs immediately in this user turn and must be
   accepted from proof; do not wait for the scheduler to establish baseline
   capability.
7. If the resolved duration exceeds one bounded block, the verified coordinator
   now creates two long-running repeat-on heartbeats. The operation heartbeat
   targets the exact executor ID and has finite `UNTIL`/`operation_stop_at`; the
   lower-frequency supervisor heartbeat targets the exact coordinator ID and
   uses the same stop guard. View both exact automation IDs and verify target,
   repeat-on, next run, local/UTC schedule, and deadline. The executor never
   creates, renews, updates, or deletes either heartbeat. `COUNT=1` plus worker
   self-continuation is invalid.
8. If durable install state is `PENDING`, the supervisor heartbeat consumes the
   one-time first-hour checks near `+15/+35/+60`, capped by stop time. It reads
   only executor turns/callbacks and planned/started/completed/blocked/missed slot
   ledger state; it never touches TikTok.
9. Only after primary smoke and both required bindings verify may scheduled
   blocks begin. Keep both tasks persistent and unarchived; pin only the
   coordinator. Missing repeat/wake/proof is
   `SCHEDULER_CONTINUATION_FAILURE`, not successful persistence.

If creation, registry, callback, or smoke fails, do not create another task or
claim stable operation unless the exact failure proves
`STALE_OWNER_TOMBSTONE`; that case uses the one-attempt replacement transaction
in `operating-model.md`. A host/network/tool transient never authorizes
replacement.

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
