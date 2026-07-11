# Version Management

This reference is the authoritative install/upgrade protocol for the bundled
`thread-supervisor` and `tiktok-web-operations` Skills.

## Source and bundle identity

Accept incoming content only when all conditions hold:

- archive source is `https://codeload.github.com/lishehao/tiktok-web-operations/zip/refs/heads/main`;
- repository root entries are exactly `README.md`, `thread-supervisor/`, and
  `tiktok-web-operations/`;
- both directories contain valid `SKILL.md`, `manifest.json`, and
  `agents/openai.yaml`;
- manifest names and repository paths match their directories;
- both manifests name `https://github.com/lishehao/tiktok-web-operations`;
- both versions equal the README protocol version and match `YYYY.MM.DD.N`.

Compare versions as four integer segments, never lexical strings. For equal
versions, fingerprint every managed regular file by ordered relative path plus
raw bytes. Exclude only `.DS_Store`, `__MACOSX/`, `.git/`, `__pycache__/`, and
`*.pyc`.

## Required decision record

Record one row for each Skill plus one bundle action:

```text
skill: thread-supervisor | tiktok-web-operations
local_state: ABSENT | LEGACY | MANAGED
local_version: NONE | UNKNOWN | YYYY.MM.DD.N
incoming_version: YYYY.MM.DD.N
version_relation: ABSENT | LEGACY | REMOTE_NEWER | EQUAL | REMOTE_OLDER
content_relation: UNKNOWN | IDENTICAL | DIFFERENT
active_runtime: NONE | ACTIVE:<thread_ids> | UNVERIFIED
skill_action: INSTALL | UPGRADE | NOOP | BLOCKED_CONFLICT | BLOCKED_DOWNGRADE

bundle_action: INSTALL | UPGRADE | NOOP | DEFERRED_ACTIVE_RUNTIME |
  BLOCKED_RUNTIME_UNVERIFIED | BLOCKED_CONFLICT | BLOCKED_DOWNGRADE |
  FORCE_REINSTALL | FORCE_DOWNGRADE | ROLLED_BACK
validation: PASSED | FAILED | NOT_RUN
```

Use `NOOP` only when both installed trees match the incoming bundle. An absent or
older component makes the bundle an install/upgrade. Equal-version content
drift blocks the bundle unless the user explicitly requests force reinstall.
An incoming older version blocks unless the user explicitly requests downgrade.
Explicit force never bypasses source validation, runtime fencing, backup,
post-install validation, or rollback.

`INSTALL` and `UPGRADE` are non-interactive installer actions. Do not stop after
comparison, report only that an upgrade is available, ask whether to upgrade,
or require a user `continue`. When source validation and the active-runtime
fence pass, execute the transaction immediately, validate the exact installed
trees, and continue dependency preflight in the same turn.

## Active-runtime fence

Before replacing either Skill, inspect active TikTok tasks and registries. Do
not hot-reload a coordinator or executor using an installed version. Download
and validate the incoming bundle, then return `DEFERRED_ACTIVE_RUNTIME`. Retry
only after the executor reports `STOPPED_AND_RELEASED` and the coordinator is
idle or retired. If runtime state cannot be inspected, return
`BLOCKED_RUNTIME_UNVERIFIED`.

Treat a task as active only with current evidence that it is running, owns a
TikTok/Chrome mutation session, has an uncertain submission, or has not released
its executor. Historical, completed, archived, `notLoaded`, or otherwise idle
tasks with released Chrome and no uncertain submission do not trigger the
fence. Do not turn stale task history into an upgrade prompt.

Publishing from an isolated release directory while an older installed runtime
is active is allowed. Do not imply the installed version changed.

## Bundle transaction and rollback

Never merge files or leave the two Skills on different bundle versions.

1. Acquire one installer lock adjacent to `${CODEX_HOME:-$HOME/.codex}/skills`.
2. Download to a fresh temporary directory and reject unsafe paths, symlinks,
   duplicate Skill roots, or unexpected root entries.
3. Validate source identity, both manifests, references, metadata, and bundle
   version before selecting an action.
4. Prove the active-runtime fence is clear for a replacement.
5. Stage both complete Skill directories as siblings on the target filesystem
   and validate both staged trees.
6. Rename any current targets to temporary previous directories, then rename
   both staged directories into their exact target paths.
7. Validate both exact installed targets and read both versions back.
8. On success, move previous trees into timestamped
   `${CODEX_HOME:-$HOME/.codex}/skill-backups/` directories and release the lock.
9. If either target fails, move both new targets aside, restore every previous
   target, validate the restored state, release the lock, report `ROLLED_BACK`,
   and stop before TikTok preflight.

Do not store credentials, browser state, ledgers, or user overrides in either
managed tree.

## Result handling

- Successful install/upgrade/force action continues automatically to dependency
  preflight in the same turn, only after both installed targets validate.
- `NOOP` rewrites neither directory and continues with the validated trees.
- Deferred or blocked actions make no target changes and start no runtime.
- A release is complete only after staged validation, ZIP integrity, GitHub
  synchronization, and fresh public codeload readback agree on the same bundle
  version and contents.
