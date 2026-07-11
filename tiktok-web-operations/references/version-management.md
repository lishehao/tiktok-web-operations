# Version Management

This reference is the authoritative install/upgrade decision protocol. The repository root `README.md` is the public machine entrypoint; after downloading the archive, read this file before changing an existing installation.

## Version and source identity

The incoming Skill is valid only when all of these match:

- archive source: `https://codeload.github.com/lishehao/tiktok-web-operations/zip/refs/heads/main`
- repository root entries: exactly `README.md` and `tiktok-web-operations/`
- `manifest.json.name`: `tiktok-web-operations`
- `manifest.json.repository`: `https://github.com/lishehao/tiktok-web-operations`
- `manifest.json.repository_path`: `tiktok-web-operations`
- version format: `YYYY.MM.DD.N`, with four non-negative integer segments

Compare versions as integer tuples, never as lexical strings. Reject a malformed incoming manifest before touching the installed tree.

For equal-version comparison, compute a deterministic managed-tree fingerprint from every regular file under the Skill root, ordered by relative path. Hash each relative path plus its raw file bytes. Exclude only transport/runtime debris: `.DS_Store`, `__MACOSX/`, `.git/`, `__pycache__/`, and `*.pyc`. Do not ignore unknown Markdown, YAML, JSON, scripts, or references; local edits inside the managed tree must produce a conflict.

## Required decision record

Before mutation, record internally:

```text
local_state: ABSENT | LEGACY | MANAGED
local_version: NONE | UNKNOWN | YYYY.MM.DD.N
incoming_version: YYYY.MM.DD.N
version_relation: ABSENT | LEGACY | REMOTE_NEWER | EQUAL | REMOTE_OLDER
content_relation: UNKNOWN | IDENTICAL | DIFFERENT
active_runtime: NONE | ACTIVE:<thread_ids> | UNVERIFIED
install_action: INSTALL | UPGRADE | NOOP | DEFERRED_ACTIVE_RUNTIME | BLOCKED_RUNTIME_UNVERIFIED | BLOCKED_CONFLICT | BLOCKED_DOWNGRADE | FORCE_REINSTALL | FORCE_DOWNGRADE | ROLLED_BACK
active_version: NONE | YYYY.MM.DD.N
backup_path: NONE | absolute path
validation: PASSED | FAILED | NOT_RUN
```

Decision table:

| Local state | Comparison | Default action |
|-|-|-|
| absent | n/a | `INSTALL` |
| legacy, no manifest | n/a | back up and `UPGRADE` |
| managed | incoming newer | back up and `UPGRADE` |
| managed | equal version, identical fingerprint | `NOOP` |
| managed | equal version, different fingerprint | `BLOCKED_CONFLICT` |
| managed | incoming older | `BLOCKED_DOWNGRADE` |

Never infer permission to overwrite from the generic words `安装或升级`. `FORCE_REINSTALL` for an equal-version conflict and `FORCE_DOWNGRADE` each require explicit user direction naming that action. Explicit force still cannot bypass source validation, active-runtime safety, backup, post-install validation, or rollback.

## Active-runtime fence

Before replacing an existing Skill, inspect active TikTok tasks and their immutable registries. If a coordinator or executor is active with the installed version, do not hot-reload or modify the installed tree. Download and validate the incoming archive, then return `DEFERRED_ACTIVE_RUNTIME` with the active and incoming versions. Retry only after the executor reports `STOPPED_AND_RELEASED` and both operating tasks are idle or retired.

If task inspection is unavailable and an installed tree would be replaced, return `BLOCKED_RUNTIME_UNVERIFIED`; do not guess that no runtime is active. A first install into an absent target may continue because no task can be using that installed tree.

Publishing a newer public version while an older local runtime is active is allowed only from an isolated release staging directory. The active installed tree remains untouched and reports its original version until the later upgrade transaction.

## Transaction and rollback

Never merge individual files from old and new managed trees.

1. Acquire a single installer lock adjacent to the target. If another live/unknown lock exists, stop; do not delete it speculatively.
2. Download into a new temporary directory and reject unsafe ZIP paths, symlinks escaping the root, multiple Skill roots, or unexpected repository-root entries.
3. Validate source identity, structure, references, metadata, and the incoming manifest before the decision.
4. For a replacement, prove the active-runtime fence is clear.
5. Copy the validated incoming Skill to a sibling staging directory on the same filesystem as the target and validate that staged tree again.
6. Rename the current target to a sibling previous directory, then rename staging to the exact target path. Do not copy files into the live target.
7. Validate the exact installed target and read its active version back.
8. On success, move the previous directory to `${CODEX_HOME:-$HOME/.codex}/skill-backups/tiktok-web-operations-<old-version-or-legacy>-<timestamp>/` and release the lock.
9. On failure, move the failed target aside, rename the previous directory back to the exact target path, validate the restored version, release the lock, and report `ROLLED_BACK`. Never continue to TikTok preflight after a failed transaction.

The managed Skill must contain no cookies, credentials, Chrome profile data, ledgers, or user overrides. Custom local changes belong outside the managed tree; the timestamped backup preserves them for manual review.

## Result handling

- `INSTALL`, `UPGRADE`, `FORCE_REINSTALL`, or `FORCE_DOWNGRADE`: continue to dependency preflight only after post-install validation passes.
- `NOOP`: do not rewrite the directory; continue to dependency preflight with the existing validated copy.
- `DEFERRED_ACTIVE_RUNTIME`: do not start another runtime or claim upgrade success. Report the active and incoming versions and wait for release proof.
- `BLOCKED_RUNTIME_UNVERIFIED`, `BLOCKED_CONFLICT`, or `BLOCKED_DOWNGRADE`: make no target changes and ask for only the missing decision or repair.
- `ROLLED_BACK`: report the restored version and stop.

For release maintenance, every distributed README, Skill, reference, agent metadata, or Prompt change increments the final numeric segment. A release is complete only after local/staged validation, ZIP integrity, GitHub synchronization, and a fresh public codeload readback all agree on the same incoming version.
