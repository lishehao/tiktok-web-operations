# Startup Health Check And Bootstrap

Use this reference for install, upgrade, or first launch. Phase 1 is read-only on TikTok. Phase 2 creates two persistent user-owned Threads; it never creates a subagent.

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
local_time_check: local time | timezone | UTC offset
ledger_path:
dependency_status: READY | BLOCKED
required_missing: []
repair_actions: []
```

Run checks in order:

1. Download the canonical GitHub archive, locate exactly one Skill directory, read `manifest.json`, and validate before installation.
2. Compare numeric versions. Back up and atomically replace the complete Skill directory for upgrades; block same-version conflicts and unauthorized downgrades; restore on validation failure.
3. Prove Chrome control by reading existing Chrome tabs. Retry dropped control at most twice. Do not substitute another browser tool.
4. Open/reuse TikTok, read the exact logged-in identity, and inspect warnings/challenges. Never enter credentials or verification codes.
5. Prove `list_projects`, `create_thread`, `read_thread`, `send_message_to_thread`, `set_thread_title`, and `set_thread_archived` exist.
6. Prove `create_thread` supports `model=gpt-5.6-luna` with `thinking=high`. This is a hard requirement for both operating Threads.
7. Read local time when needed and create a writable shared ledger path.
8. Initialize every mutation lane independently. Reuse prior evidence only when account and runtime continuity are proven. Do not mutate TikTok during preflight.
9. Release bootstrap Chrome control before creating the operating Threads.

Hard dependencies are the valid Skill, Chrome control, logged-in TikTok identity, required thread tools, exact Luna/High creation/dispatch support, and writable ledger. Do not silently fall back.

If blocked, return only the first repairable issue and impact, ending with `完成后回复“继续”`.

## Phase 2 — create the two persistent Threads

Follow `operating-model.md` exactly:

1. Create `TikTok 运营主任务` with `gpt-5.6-luna/high` and record its Thread ID.
2. Create `TikTok Chrome执行任务` with `gpt-5.6-luna/high`, give it the coordinator ID, and record its ID.
3. Give the coordinator the executor ID and full operating envelope.
4. Verify two-way registry plus executor `THREAD_READY` callback through `send_message_to_thread`.
5. Coordinator dispatches the first `search_heavy` block to the executor with Luna/High override.
6. Confirm the executor received the block, navigate the app to the coordinator when possible, and archive only the bootstrap task.

If any creation/handshake step fails, do not touch TikTok state. Archive only empty partial Threads created by this bootstrap and report the blocker.

If a standing proactive-comment envelope is included, it covers only top-level comments on strong `core` posts, preferably 2–12 words and never more than 30 words. On an unproven account/runtime, first use one eligible candidate for a reload-verified persistence gate. Failure disables that lane. Every other mutation stays excluded unless separately authorized.

## Healthy response

After the coordinator and executor are created, registered, and dispatched, the coordinator reports:

`状态健康。当前账号：@handle。两个 Luna/High 持久化任务已启动，第一轮定向校准正在执行。`
