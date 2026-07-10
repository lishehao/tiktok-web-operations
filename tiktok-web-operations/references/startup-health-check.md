# Startup Health Check And Bootstrap

Use this reference for a fresh install, upgrade, or first launch from the public installer Prompt. Keep phase 1 read-only on TikTok. Start phase 2 automatically only after all hard dependencies pass.

## Phase 1 — install and preflight

Record this internal report:

```text
install_action: INSTALLED | UPGRADED | NOOP | BLOCKED_CONFLICT | BLOCKED_DOWNGRADE | ROLLED_BACK
skill_version: old | incoming | active
github_source: AVAILABLE | UNAVAILABLE
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

Run checks in this order:

1. Download the canonical public GitHub archive over HTTPS into a temporary directory. Locate exactly one `tiktok-web-operations/` Skill directory, read `manifest.json`, and validate the whole incoming folder before installation.
2. Compare numeric `YYYY.MM.DD.N` versions. For an upgrade, back up the complete installed directory and atomically replace it with the complete incoming directory. Do not merge files. On validation failure, restore the backup. Block same-version content conflicts and downgrades unless the user explicitly authorizes them.
3. Prove Chrome control exists by listing or reading the user's existing Chrome tabs. Retry a dropped control connection at most twice. Do not replace Chrome control with Computer Use, the in-app Browser, Playwright, or Web Search.
4. Through Chrome control, open or reuse `https://www.tiktok.com/`, read the exact logged-in profile identity, and inspect visible warnings, verification challenges, or restrictions. Never enter credentials, OTPs, passkeys, or recovery codes.
5. Prove the current Thread can spawn one subordinate agent and later reuse, message, interrupt, and inspect that agent through collaboration tools. Do not create a second user-owned Codex Thread as a substitute.
6. Read actual local time, timezone, and UTC offset. Create a writable ledger path for the driver. Do not require a database.
7. Initialize each mutation lane independently as `untested`, `verified`, `failed`, `unverified`, or `disabled`. Reuse prior evidence only when account and browser/runtime continuity are proven. Do not perform a TikTok mutation during preflight.
8. If the runtime exposes model selection, request the strongest coordinator model available and `Luna + Extra High` for the subordinate driver. Record the actual model. If selection is absent, inherit the actual runtime and continue; never claim the requested model was applied without proof.

Hard dependencies are the valid installed Skill, callable Chrome control, logged-in TikTok identity, collaboration support, and a writable ledger. GitHub is required for install/upgrade but not for a later already-installed offline run when the user explicitly requests offline use. Local time becomes hard only for scheduled or duration-bounded work.

If Chrome control is missing, ask the user to open Chrome and enable the ChatGPT Chrome Extension. If TikTok is logged out, keep the TikTok tab open and ask the user to log in manually. If collaboration support is missing, report that the required two-agent topology cannot start. Return only the first user-repairable blocker and its impact; re-run the full preflight after the user replies `继续`.

## Phase 2 — immediate operation

When `dependency_status=READY`:

1. Declare the current Thread `main_coordinator` and keep it as the only user-facing operating Thread.
2. Establish account, North American college/dorm-life audience ontology unless the user supplied another direction, exclusions, search clusters, current capability matrix, comment authorization, ledger path, and hard stops.
3. Spawn exactly one subordinate named `chrome_driver`. Do not pass any external Thread ID or callback target. Pass the parent agent path, full execution envelope, and a rule forbidding descendants.
4. Transfer all Chrome ownership to the child. The parent must not inspect or navigate TikTok while the child exists.
5. Dispatch one `search_heavy` block: three distinct approved query clusters × five ordered results, then twenty sequential For You items. The child writes every observation to the sole ledger and returns one structured block result to the parent.
6. Reuse the same child with `followup_task` for later blocks. The child becomes idle after each bounded result; it does not start unbounded work on its own.

If the bootstrap Prompt explicitly grants a standing proactive-comment envelope, it covers only top-level comments on strong `core` posts, in the video's language, with context-specific meme-aware voice, preferably 2–12 words and never more than 30 words. Before autonomous comments begin on an unproven account/runtime, use the first eligible core candidate for one reload-verified persistence gate. A failed or uncertain gate disables the lane. Likes, favorites, comment likes, follows, replies, `Not interested`, publishing, profile changes, shares, and DMs remain excluded unless separately authorized.

## Healthy and blocked responses

After a healthy preflight, do not dump the dependency report. Return one short line stating the account and that the first calibration block has started. Continue supervising through the collaboration tree.

When blocked, do not create the driver or touch TikTok state. Return one direct repair action, the paused scope, and `完成后回复“继续”`.
