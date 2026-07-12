# TikTok Web Operations

Protocol version: `2026.07.12.16`

This repository distributes two version-locked Codex Skills:

- `tiktok-web-operations/` — TikTok strategy, Chrome operation, evidence,
  engagement lanes, recovery, and lifecycle.
- `thread-supervisor/` — persistent task identity, one-way assignment, and
  self-owned Heartbeat mechanics.

The system uses the user's existing logged-in Chrome. It does not create
accounts, enter credentials, bypass challenges, imitate a human with random
input, promise reach, or claim access to TikTok's private ranking weights.

## Minimal user prompt

Send this to a new Codex task:

```text
请通过 HTTPS 打开并完整遵循 https://raw.githubusercontent.com/lishehao/tiktok-web-operations/main/README.md，按 README 安装或升级 TikTok Web Operations，并继续完成其中的预检与启动交接。
```

The agent automatically validates version/source, installs or upgrades both
Skills atomically, runs read-only preflight, and continues. It does not stop just
because an update exists.

## Installation contract

1. Download only:
   `https://codeload.github.com/lishehao/tiktok-web-operations/zip/refs/heads/main`.
2. Require repository root entries exactly `README.md`, `thread-supervisor/`,
   and `tiktok-web-operations/`.
3. Reject unsafe ZIP paths, symlinks, duplicates, unexpected roots, manifest
   mismatch, missing references, or unequal bundle versions.
4. Validate both `SKILL.md`, both manifests, both `agents/openai.yaml`, all
   relative references, and every packaged validator.
5. Compare numeric four-part versions and complete managed-tree fingerprints.
6. Install/upgrade by staging both complete directories and atomically replacing
   `${CODEX_HOME:-$HOME/.codex}/skills/thread-supervisor` and
   `${CODEX_HOME:-$HOME/.codex}/skills/tiktok-web-operations` together.
7. If a managed older TikTok runtime is currently active, validate the new
   bundle but mark local replacement `DEFERRED_ACTIVE_RUNTIME`; never hot-mix
   versions. The next clean install invocation upgrades automatically.
8. Roll back both directories if either installed Skill fails validation.

## User-visible lifecycle

```text
TikTok 启动台
  install/upgrade -> read-only preflight -> resolve initial mission
  -> fresh-create/assign one new TikTok 执行台 -> verify acceptance
  -> reusable stateless idle -> later command creates another fresh executor

TikTok 执行台
  read-only smoke -> create self-target recurring Heartbeat
  -> search-led operation -> held-out Feed checks -> verified interactions
  -> self-recovery/checkpoints -> final release
```

There is no long-term `TikTok 主控台`, executor-to-launcher callback,
coordinator/supervisor Heartbeat, centralized monitoring, or cross-run lock.
Every execution task is independent and uses its own task ID, Chrome tab,
ledger, and Heartbeat. Future user changes and true hard blockers are handled
directly in `TikTok 执行台`.

Every setup/bootstrap/new operating start is fresh-only. The launcher generates
a new run ID and calls `create_thread` exactly once. It recognizes only that
call's exact newly returned task ID. It never lists/searches/reads/reuses/
unarchives/revives/messages/archives/replaces a historical executor, including
same-title, archived, completed, or live tasks; those remain untouched history.
If fresh creation fails or its result is uncertain, this launch reports the
fresh-task creation failure and stops without retry, replacement, or fallback.

The same `TikTok 启动台` may be used repeatedly. Every later operating command
starts another independent fresh-only dispatch and then returns the launcher to
idle. The launcher retains installation capability but no old executor result,
mission, registry, ledger, Heartbeat, tab, risk, or progress. Workers never
callback, return, or message the launcher.

The launcher uses `gpt-5.6-luna`/high for the executor exactly as required by the
TikTok Skill. It never substitutes a subagent or Goal Mode.

## Mission defaults

If the user has not supplied values:

- direction: North American college/dorm life;
- duration: 3 hours, standard intensity;
- universal lifestyle language/region: global English with North American bias;
- cultivation lanes: post Like, Favorite, TikTok Repost, and proactive comment
  are four independent `pending_fresh_gate` lanes with
  `parallel_engagement=true`;

`继续` accepts defaults. Explicit direction, duration, intensity, and action
instructions override the corresponding defaults without repeat confirmation.

## Operating method

The primary training path is directed search, not Feed browsing:

1. Three distinct approved search clusters.
2. Five result cards assessed per cluster.
3. Each operating round targets 35 qualified views, with an allowed 25–45
   range: normally 25–35 search-origin views plus 5–10 For You validation views.
   For You failure may be replaced by search views. Duplicates, drift, failed
   loads, and thumbnails do not count.
4. While every qualified video is still open, evaluate Like, Favorite, Repost,
   and Comment together and immediately execute justified actions through their
   independently verified persistence lanes. Do not postpone interaction until
   after the viewing round; comments never exceed 30 words.
5. After two units or roughly 20–30 qualified views, 5–10 continuous For You
   items are sampled as held-out validation.
6. Search clusters are adjusted from rolling evidence and the loop continues
   until stop/cutoff.

For You movement uses one continuous native feed without reload/reset between
items. Feed failure disables only validation; healthy search training continues.
Page/network/Chrome/lane failures are scoped, auto-recovered, and never delete
the executor's valid Heartbeat.

## Heartbeat receipt

The executor owns one repeat-on, finite-cutoff Heartbeat targeted to itself.
Every timed receipt has exactly three lines:

```text
本轮完成：<one sentence>
下次心跳：<verified local date, time, and timezone, or why none exists>
下轮计划：<one bounded purpose>
```

No launcher callback or supervisor timer is created.

## Validation

From the repository root, run both Skill structural validators and all TikTok
scenario validators. Required scenarios include:

- setup immediate launcher rename;
- old matching title ignored and untouched;
- archived and live old runs ignored and untouched;
- a fresh create is required for every new launch;
- create failure produces no reuse, retry, or replacement;
- each launcher command performs one fresh dispatch then returns idle;
- same launcher second command creates another fresh executor;
- launcher remains reusable stateless idle after every dispatch;
- no worker-to-launcher return/message/result path;
- executor self-owned recurring Heartbeat;
- no callback to launcher;
- no coordinator/supervisor Heartbeat;
- independent lanes and independent runs;
- network/Chrome recovery and Heartbeat survival;
- separate Like/Favorite/Repost/Comment gates with concurrent eligibility during
  viewing and lane-local failure isolation.

The release is complete only when local source, GitHub main/codeload, and the ZIP
artifact are byte-identical for managed files.
