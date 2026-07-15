# TikTok Web Operations

Protocol version: `2026.07.15.3`

This repository distributes two version-locked Codex Skills:

- `tiktok-web-operations/` — TikTok strategy, Chrome operation, evidence,
  engagement lanes, recovery, and lifecycle.
- `thread-supervisor/` — persistent task identity, exact callback routing, and
  coordinator-owned scheduler mechanics.

The system uses the user's existing logged-in Chrome. It does not create
accounts, enter credentials, bypass challenges, imitate a human with random
input, promise reach, or claim access to TikTok's private ranking weights.

## Minimal user prompt

Send this to a new Codex task:

```text
请通过 HTTPS 打开并完整遵循 https://raw.githubusercontent.com/lishehao/tiktok-web-operations/main/README.md，按 README 安装或升级 TikTok Web Operations，并继续完成其中的预检、主控台就绪与任务交接。
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
  install/upgrade -> read-only preflight
  -> same task renames to pinned TikTok 主控台

TikTok 主控台
  -> resolve explicit mission or confirm a missing account image
  -> fresh-create/assign one TikTok 执行台 -> callback handshake
  -> create/read-back one stable main-target phase timer
  -> dispatch bounded round -> accept callback -> choose cooldown/direction
  -> callback supplies canonical IDLE proof and arms one cooldown wake
  -> due wake dispatches one next round without a second mandatory task read

TikTok 执行台
  read-only smoke -> search-led operation -> held-out Feed checks
  -> verified interactions -> checkpoint
  -> callback main task and become idle
  -> next bounded assignment after main-controlled cooldown
  -> within-round recovery/checkpoints -> final release callback
```

The pinned `TikTok 主控台` owns mission strategy, exact executor registry,
callback acceptance, 10–20 minute cooldown decisions, one callback-first phase
timer, user communication, and finalization. It never operates
TikTok. `TikTok 执行台` owns only its dedicated Chrome tab, raw ledger,
within-round recovery, and one bounded round at a time; it owns no timer.

Every new mission initially fresh-creates exactly one executor and recognizes
only that create call's returned ID. The same active mission then reuses that
exact registered executor across every round and every continuation instruction
sent in `TikTok 主控台`; a round callback is not a reason to create another task.
Historical same-title tasks remain untouched and are never fallback owners.

Only an absent registered ID or an exact registered executor proven
`STALE_OWNER_TOMBSTONE`, retired, archived, or released while the mission is
still active permits one same-run replacement. `notLoaded`, transient task-read,
host, network, or tool failures do not. Replacement keeps the run ID, increments
`executor_generation`, records old/new exact IDs and reason, repeats assignment
acceptance plus callback handshake, and resumes from the last accepted cursor.
An uncertain replacement create never authorizes a second create. A truly
terminal/released mission starts a new run and a fresh executor instead.

The main task creates the executor with `gpt-5.6-luna`/high exactly as required
by the TikTok Skill. It never substitutes a subagent or Goal Mode.

## Mission defaults

The main task uses a profile lock before every fresh mission. Preflight may finish,
but it must not create an executor, search, watch, or interact until
`profile_status=confirmed`.

Use at most two user-facing rounds:

1. Ask what identity the account should represent, which audience it serves,
   and what it will eventually publish. Skip this question when already clear.
2. Present one structured proposal containing persona, target audience,
   region/language, 3–5 pillars, exclusions, comment voice, future-post
   alignment, duration/intensity, and interaction policy. The user confirms or
   supplies final replacement values once; supplied corrections count as
   confirmation unless the user explicitly asks to review another draft.

A clear operating instruction that already defines a usable direction and asks
to start is canonical confirmation; after health, rename/pin first and dispatch
without another question. A bare `继续` confirms only a proposal already displayed. Without a visible
proposal, it asks the main task to show the default proposal and does not start.
Every later new mission repeats this lock; a historical completed profile never
silently becomes the new mission.

After setup, use this novice handoff and nothing more:

```text
TikTok 已准备好，当前账号：@handle。
下一步只要告诉我：想把账号做成什么方向，以及运营多久。
例如：“做北美宠物账号，持续 10 小时。”不确定就回复：“用默认设置开始。”
```

A direction/duration reply to this handoff is an operating instruction and
dispatches without another confirmation round. `用默认设置开始` confirms the
packaged defaults and dispatches directly.

If the user has not supplied values:

- direction: North American college/dorm life;
- duration: 3 hours, standard intensity;
- universal lifestyle language/region: global English with North American bias;
- cultivation lanes: post Like, Favorite, TikTok Repost, and proactive comment
  are four independent `best_effort_attempt` lanes with
  `parallel_engagement=true`;

After a proposal is visible, `确认`, `继续`, `开始`, or an explicit “按此开始”
confirms it. Explicit final corrections produce the confirmed revised version
before dispatch.

## Operating method

The primary training path is directed search, not Feed browsing:

1. Three distinct approved search clusters.
2. Five result cards assessed per cluster.
3. Each operating round targets 35 qualified views, with an allowed 25–45
   range: normally 25–35 search-origin views plus 5–10 For You validation views.
   For You failure may be replaced by search views. Duplicates, drift, failed
   loads, and thumbnails do not count.
4. While every qualified video is still open, evaluate Like, Favorite, Repost,
   and Comment together and immediately issue justified native actions once. Do
   not postpone interaction until after the viewing round and do not wait/reload/
   reopen/account-check afterward; comments never exceed 30 words.
5. Comment is the highest-priority lane: target 10 total comment attempts per
   round, flexible range 7–12, hard ceiling 15. On an unusually strong video,
   this may be one top-level joke plus replies to at most two distinct existing
   comments; never post two or three separate top-level comments on one video.
   If live context does not yield a strong joke,
   permit at most two focused Web searches per round for current meme/slang
   context, then write an original line rather than copying a result.
   The budget resets every round. A prior target hit or drifted For You sample
   cannot set the next assignment's Comment values to zero; `new cluster match`
   is judged per opened search video, and candidate scarcity becomes an honest
   checkpoint shortfall rather than a pre-emptive lane freeze.
6. After two units or roughly 20–30 qualified views, 5–10 continuous For You
   items are sampled as held-out validation.
7. At every completed 25–45-view round, persist a checkpoint and callback the
   main task. The main task chooses a real 10–20 minute no-TikTok cooldown from
   evidence, machine-calculates `next_dispatch_at`, adjusts search clusters, and
   lets its scheduler send one next-round assignment when due.
8. The loop continues until stop/cutoff; no catch-up bursts are dispatched.

For You movement uses one continuous native feed without reload/reset between
items. Feed failure disables only validation; healthy search training continues.
Page/network/Chrome/lane failures are scoped and auto-recovered inside the
round. A round-ending or human-only blocker callbacks the exact main task.

## Callback-first resume receipt

The main task creates one stable self-targeted phase timer under direct user
authorization. It does not poll every five minutes. After dispatch, normal
scheduler polling is paused and the same timer holds only one low-frequency
60-minute watchdog wake. A valid executor callback updates that exact timer in
place to one cooldown wake at `next_dispatch_at`; the due wake sends exactly one
assignment and rearms the one watchdog. The executor never creates or modifies
a Heartbeat, and the main task never creates/deletes a timer per round.

Every wake before cutoff must read back exactly one future occurrence unless it
has just terminally deleted the timer. A transient task-state read cannot erase
accepted callback-IDLE proof. If required orchestration proof is missing, the
same timer keeps the pending round and rearms a five-minute state retry; after
three failures it retains a 15-minute degraded-recovery wake and notifies once.
`ACTIVE` with no future occurrence is an expired orphan, not continuity.

Every accepted callback/coordinator receipt has exactly three lines:

```text
本轮完成：<one sentence>
下次心跳：<verified local date, time, and timezone, or why none exists>
下轮计划：<one bounded purpose>
```

At stop/cutoff, the main task deletes its exact scheduler after requesting
executor release and reconciling the final callback.

## Validation

From the repository root, run both Skill structural validators and all TikTok
scenario validators. Required scenarios include:

- setup immediate `TikTok 启动台` rename;
- successful setup shows exactly the three-line novice handoff;
- direction/duration and `用默认设置开始` replies dispatch without another question;
- healthy preflight same-task rename to pinned `TikTok 主控台`;
- pin failure is non-blocking presentation degradation and executors remain unpinned;
- profile proposal required before executor creation;
- bare continue without a visible proposal cannot start;
- confirmed profile version is the only assignment direction reference;
- old matching title ignored and untouched;
- archived and live old runs ignored and untouched;
- a fresh create is required at every new-mission boundary;
- same active-mission continuation and later rounds reuse the exact registered
  executor rather than creating duplicate tasks;
- `notLoaded` and transient task/tool/network failures never trigger replacement;
- an absent exact registered ID or proven stale/retired owner permits at most one
  same-run replacement with incremented generation and fresh handshake;
- initial or replacement create uncertainty produces no duplicate create;
- exact callback ping/ack before any TikTok work;
- one registered executor and one canonical callback path per active mission;
- executor returns one structured callback after every bounded round;
- main task selects next clusters, interaction emphasis, and cooldown;
- one coordinator-owned callback-first phase timer with exact in-place readback;
- executor owns zero Heartbeats and cannot substitute a timer;
- no five-minute polling while the executor is active;
- one cooldown wake after callback plus one 60-minute active-round watchdog;
- accepted callback-IDLE proof survives unavailable/empty/`notLoaded` task read;
- every nonterminal wake leaves exactly one future occurrence;
- missing proof produces bounded state retry and degraded recovery, never naked
  NOOP or silent scheduler death;
- independent lanes and independent runs;
- network/Chrome recovery with callback only at a bounded-round boundary;
- 10–20 minute inter-round cooldown with machine-clock `next_dispatch_at`;
- concurrent Like/Favorite/Repost/Comment attempt coverage during viewing, with
  `attempted|unavailable|hard_blocked` reporting and no persistence checks.
- comment-priority 7–12 target range, at most three comment mutations on one
  exceptional video, selective Web meme research, and no-copy originality/
  safety checks.
- comment-lane continuity across rounds: Feed drift and callback advice cannot
  erase current cultivation authority or zero the per-round `10/7/12/15`
  Comment policy.

The release is complete only when local source, GitHub main/codeload, and the ZIP
artifact are byte-identical for managed files.
