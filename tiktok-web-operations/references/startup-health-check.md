# Startup Health Check And Bootstrap

Use this reference for install, upgrade, or first launch. Phase 1 is read-only, ends with a guided user handoff, and creates no operating Threads. Phase 2 begins only after the healthy user supplies direction/duration or accepts defaults.

## Phase 1 — install and preflight

Record internally:

```text
install_action: INSTALLED | UPGRADED | NOOP | BLOCKED_CONFLICT | BLOCKED_DOWNGRADE | ROLLED_BACK
skill_version: old | incoming | active
github_source: AVAILABLE | UNAVAILABLE
skill_validation: PASSED | FAILED
chrome_control: AVAILABLE | RECONNECTED | UNAVAILABLE
tiktok_session: LOGGED_IN:@handle | LOGGED_OUT | UNVERIFIED
account_warning: NONE_VISIBLE | PRESENT | UNVERIFIED
thread_support: CREATE_READ_SEND_TITLE_ARCHIVE | UNAVAILABLE
model_runtime: coordinator=gpt-5.6-luna/high | executor=gpt-5.6-luna/high | UNAVAILABLE
incumbent_executor: NONE | SAME_REGISTERED_EXECUTOR | RETIRED_AND_RELEASED | ACTIVE_OR_UNCERTAIN
local_time_check: local time | timezone | UTC offset
ledger_path:
dependency_status: READY | BLOCKED
required_missing: []
repair_actions: []
bootstrap_state: PREFLIGHT_HEALTHY_WAITING_FOR_DIRECTION | BLOCKED
```

Run checks in order:

1. Download the canonical GitHub archive, locate exactly one Skill directory, read `manifest.json`, and validate before installation.
2. Compare numeric versions. Back up and atomically replace the complete Skill directory for upgrades; block same-version conflicts and unauthorized downgrades; restore on validation failure.
3. Prove Chrome control by reading existing Chrome tabs. Retry dropped control at most twice. Do not substitute another browser tool.
4. Open/reuse TikTok read-only, read the exact logged-in identity, and inspect warnings/challenges. Never enter credentials or verification codes.
5. Prove `list_projects`, `create_thread`, `read_thread`, `send_message_to_thread`, `set_thread_title`, and `set_thread_archived` exist.
6. Prove `create_thread` and `send_message_to_thread` support `model=gpt-5.6-luna` with `thinking=high`. This is a hard requirement for both operating Threads.
7. Query recent TikTok-related Threads. Inspect every active/in-progress candidate and prove no other Chrome executor or descendant agent owns the session. If the user explicitly asked to replace an incumbent, require its `STOPPED_AND_RELEASED` checkpoint before continuing; archiving alone is insufficient.
8. Read local time and create a writable shared ledger path.
9. Initialize every mutation lane independently. Reuse prior evidence only when the same account and runtime continuity are proven. Do not mutate TikTok during preflight.
10. Release bootstrap Chrome control.

Hard dependencies are the valid Skill, Chrome control, logged-in TikTok identity, required thread tools, exact Luna/High creation/dispatch support, exclusive executor ownership, local time, and writable ledger. Do not silently fall back.

If blocked, return only the first repairable issue and impact, ending with `完成后回复“继续”`. A blocked `继续` rechecks only the missing item; it is not an operation start word.

## Healthy guided handoff

When Phase 1 is healthy, return only:

```text
状态健康。当前账号：@handle。
你想把这个账号运营成什么方向或人设？方向会决定后续搜索、浏览、收藏、Repost、评论，以及未来内容的主题与语气，帮助形成更一致的受众信号；但不能保证具体推荐或分发结果。
也请告诉我希望运行多久。你可以回复“北美大学生 / dorm life，运行 3 小时”；如果暂时没想法，直接回复“继续”，我会按默认方向和默认 3 小时开始。
```

Then stop and wait. Do not create Threads, dispatch work, search TikTok, mutate TikTok, or claim startup.

## Resolve the second user message

Build this contract:

```text
persona_name:
target_audience:
region_language:
content_pillars:
excluded_topics:
voice_and_comment_style:
search_seed_clusters:
future_post_alignment:
duration:
operation_stop_at:
```

Rules:

- Explicit user fields override defaults.
- Missing direction defaults to North American college/dorm life.
- Missing duration defaults to 3 hours at standard intensity.
- `继续` or `开始` after a healthy handoff accepts all defaults.
- Ask one question only when a material persona/risk choice cannot be safely inferred. Otherwise fill missing fields and start in the same turn.
- Explain direction as a coherence and audience-signal hypothesis, not a guarantee of reach.

Default pillars are roommate move-in/storytime/chaos, dorm/freshman move-in/setup, college day-in-my-life/campus routine/GRWM, campus friends/game day/tailgate, and finals/dorm survival failures. Exclude admissions, SAT/GPA, application advice, pure study motivation, and generic content without campus-life context.

## Phase 2 — create the two persistent Threads and start

Follow `operating-model.md` exactly:

1. Create `TikTok 运营主任务` with `gpt-5.6-luna/high`; include the resolved profile, duration, exact account, authorization, and stop time.
2. Create `TikTok Chrome执行任务` with `gpt-5.6-luna/high`, give it the coordinator ID, require it to wait for `SELF_REGISTRY`, and record the returned executor ID. It must not infer its own ID or touch Chrome yet.
3. Send `SELF_REGISTRY` containing the exact returned executor ID to that executor; then give the coordinator the same executor ID and full operating envelope.
4. Verify two-way registry plus executor `THREAD_READY` callback through `send_message_to_thread`; reject any payload ID that conflicts with callback `source_thread_id` or the bootstrap registry.
5. Coordinator dispatches `stability_smoke_01` from `stability-and-circuit-breakers.md` with Luna/High override. It is read-only: one search query × three results, then one continuous five-position For You native-down sample.
6. Require first-operation proof in the same startup turn. A completed smoke needs three observed search results, five reliable For You identities, four verified native-control advances, zero reset, and zero mutation. A concrete page-based blocker is real evidence but does not count as a stability pass.
7. Only after the smoke passes may the coordinator dispatch a full `search_heavy` block or any mutation. Navigate the app to the coordinator when possible and archive only the bootstrap task. Keep both operating Threads unarchived and persistent.

If creation, handshake, or the stability smoke fails, do not claim stable operation. Apply the circuit breaker; do not create a subagent or another executor. Do not touch TikTok state unless the registered executor owns Chrome and the active envelope permits it. Archive only empty partial Threads created by this failed bootstrap.

## Default action envelope

- Post like is disabled.
- Favorite/save, TikTok Repost, and proactive top-level comments may be selectively authorized on strong-core content after each lane passes its own independent gate.
- Favorite must remain selected immediately, near +3 seconds, and after a 10-second total settlement window before reload/reopen and exact account-level Favorites evidence.
- Repost must expose actual `Repost`/`Undo repost`. Opening Share sheet is read-only navigation; generic Share, copy-link, send, and other targets remain excluded.
- Comments are context-specific and funny, preferably 2–12 words and never more than 30 words; every comment is reload-verified.
- Never set engagement quotas or infer ranking effects from a successful action.

## Healthy started response

Only after first proof, report compactly:

```text
已启动。当前账号：@handle。
方向：resolved persona / audience。
时长：duration；预计结束：local date and time。
两个 Luna/High 持久化任务已接管，第一轮已产生真实浏览或操作 proof。
```
