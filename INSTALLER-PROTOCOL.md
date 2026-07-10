# TikTok Web Operations Installer Protocol

Machine execution protocol. Follow it directly after the user-facing bootstrap Prompt fetches this file. Do not ask the user to read or copy this protocol.

Protocol version: `2026.07.10.1`

## Canonical distribution

- Repository: `https://github.com/lishehao/tiktok-web-operations`
- Installer protocol: `https://raw.githubusercontent.com/lishehao/tiktok-web-operations/main/INSTALLER-PROTOCOL.md`
- Archive: `https://codeload.github.com/lishehao/tiktok-web-operations/zip/refs/heads/main`
- Skill path inside repository: `tiktok-web-operations/`
- Install path: `${CODEX_HOME:-$HOME/.codex}/skills/tiktok-web-operations`

Use ordinary task mode. Do not use Git, GitHub CLI, an attached ZIP, or a private token. Download the public archive through HTTPS into a temporary directory and locate exactly one target Skill directory.

## Phase 1 — install and dependency preflight

Do not invoke the Skill or mutate TikTok until this phase finishes.

### Install or upgrade

1. Read the incoming `manifest.json` and validate the complete incoming Skill folder.
2. Use the available `quick_validate.py` when possible. Python is optional: when no validator is available, verify archive integrity, unique target directory, valid `name` and `description` frontmatter, readable `manifest.json`, `agents/openai.yaml`, every reference, and every file directly referenced by `SKILL.md`.
3. Compare versions numerically as `YYYY.MM.DD.N`:
   - Missing install: `INSTALLED`.
   - Installed same name without a manifest: treat as legacy; back it up and upgrade.
   - Incoming newer: back up the complete installed directory, then atomically replace the complete directory.
   - Same version and same content: `NOOP`.
   - Same version but different content: `BLOCKED_CONFLICT`; preserve the installation.
   - Incoming older: `BLOCKED_DOWNGRADE`; preserve the installation unless the user explicitly requests downgrade.
4. Revalidate after replacement. On failure restore the backup and return `ROLLED_BACK`.

Do not merge individual files and do not copy unknown files from an old install into the new version.

### Runtime checks

Run the installed Skill's `references/startup-health-check.md` contract. At minimum prove:

1. Chrome control is present and can read the user's existing Chrome tabs. A dropped control connection may be reconnected at most twice.
2. Chrome control—not Computer Use, the in-app Browser, Playwright, terminal browsing, or Web Search—can open/reuse TikTok and read the exact logged-in `@handle`.
3. No visible login mismatch, CAPTCHA, verification challenge, rate limit, warning, or restriction blocks operation.
4. The current task exposes collaboration tools sufficient to spawn, reuse, message, inspect, and interrupt one subordinate agent. A second user-owned Codex task is not an acceptable substitute.
5. Local time, timezone, and UTC offset are readable when duration or scheduling matters.
6. A driver ledger path is writable.
7. Every mutation lane has an explicit capability state. Preflight itself is read-only.

Model selection is optional. If the runtime exposes model/effort selection, request the strongest available coordinator model and `Luna + Extra High` for the Chrome driver. Record the actual model. If the collaboration interface has no model selector, inherit the actual runtime and continue; do not claim the request was applied.

Keep this internal report:

```text
install_action: INSTALLED | UPGRADED | NOOP | BLOCKED_CONFLICT | BLOCKED_DOWNGRADE | ROLLED_BACK
github_source: AVAILABLE | UNAVAILABLE
skill_version: old | incoming | active
skill_validation: PASSED | FAILED
chrome_control: AVAILABLE | RECONNECTED | UNAVAILABLE
tiktok_session: LOGGED_IN:@handle | LOGGED_OUT | UNVERIFIED
account_warning: NONE_VISIBLE | PRESENT | UNVERIFIED
collaboration_support: SPAWN_REUSE_INTERRUPT | UNAVAILABLE
model_runtime: requested | actual | fallback
local_time_check: local time | timezone | UTC offset
ledger_path:
dependency_status: READY | BLOCKED
required_missing: []
repair_actions: []
```

When blocked, return only the first user-repairable issue, its impact, and `完成后回复“继续”`. Do not list successful checks or create the driver.

Preferred repair messages:

- Chrome unavailable: `需要你处理：请打开 Chrome，安装或启用 ChatGPT Chrome Extension，并保持 Chrome 运行。影响：Skill 已安装，但 TikTok 运营尚未开始。完成后回复“继续”。`
- TikTok logged out: `需要你处理：请在当前 Chrome 手动打开 tiktok.com 并登录，完成页面要求的验证。不要把密码或验证码发给 Codex。影响：Skill 已安装，但 TikTok 运营尚未开始。完成后回复“继续”。`
- Collaboration unavailable: `需要你处理：当前任务没有可用的子智能体协作能力，无法启动要求的主任务 + Chrome 子任务架构。影响：依赖检查已停止，TikTok 未发生任何互动。请换到支持 collaboration 的 Codex 任务后回复“继续”。`

## Phase 2 — start operation

When `dependency_status=READY`, use `$tiktok-web-operations` and the exact runtime envelope in the user's bootstrap Prompt. Do not ask another technical confirmation.

1. Make the current user-owned task `main_coordinator`. It is the only user-facing operating task and owns the continuing objective.
2. Spawn exactly one subordinate `chrome_driver` inside the collaboration tree. Do not create a second user-owned task, do not pass an external callback Thread ID, and do not let the child spawn descendants.
3. Transfer all Chrome/TikTok navigation and mutation ownership to the child. The parent must not touch Chrome while the child exists.
4. Immediately dispatch one bounded `search_heavy` block: three distinct approved search clusters × five ordered results, followed by twenty sequential native For You observations.
5. The child writes raw evidence to the sole ledger, returns the Skill's structured block result to its parent, and becomes idle.
6. The parent evaluates verticality and reuses the same child with `followup_task`. Do not spawn a new child per block.
7. If the bootstrap Prompt requests continuing operation, keep that objective only on the parent. The child performs bounded blocks and never owns an independent persistent goal.

For the default North American college/dorm-life envelope, rotate among roommate move-in/storytime, dorm move-in/setup, campus routines, friend groups/game day, and finals/dorm-survival chaos. Exclude pure admissions, SAT/GPA, application advice, and study-grind motivation.

If the user's bootstrap Prompt explicitly activates autonomous proactive comments, first run one authorized reload-verified persistence gate on an eligible strong `core` post unless the same account/runtime already has continuous verified evidence. After it passes, comments may proceed without per-item questions only inside the exact envelope. Prefer 2–12 words and never exceed 30 words. Stop the comment lane on the first failed/uncertain persistence check, removal, warning, throttle, CAPTCHA, account mismatch, or hard runtime change. No other mutation lane is implied.

After healthy startup, only return a short status such as:

`状态健康。当前账号：@handle。已启动：主协调器 + 唯一 Chrome 子任务，第一轮定向校准正在进行。`

Then continue supervising through the collaboration tree. Never send routine callbacks to the Skill-development task.

## Operating boundaries

- Respect the actual TikTok account, UI, warnings, and platform rules.
- Never enter credentials or handle CAPTCHA/OTP for the user.
- Never bulk-create accounts, mass-comment, manipulate engagement, imitate human timing to evade detection, or bypass enforcement.
- Use native scrolling for feed fidelity, not stealth; do not add cursor jitter or random delays.
- Keep likes, favorites, comments, comment likes, follows, replies, `Not interested`, posting, and profile changes as separate independently verified lanes.
- A click, pressed control, count animation, toast, or network response is not persistence proof.
- Zero comments in a block is valid when no strong core candidate survives the checks.
