# TikTok Web Operations

这是 TikTok 运营 bundle 的公开分发仓库。公开仓库只保留一个安装入口、通用 `thread-supervisor` Skill 和完整 `tiktok-web-operations` Skill；详细规则以两个 Skills 内 references 为准。

Protocol version: `2026.07.12.7`

## 直接安装

把下面一句发送给普通 Codex 任务：

```text
请通过 HTTPS 打开并完整遵循 https://raw.githubusercontent.com/lishehao/tiktok-web-operations/main/README.md，按 README 安装或升级 tiktok-web-operations，并继续完成其中的预检与启动交接；不要进入目标模式，也不要开始实际运营。
```

## Codex 安装协议

如果你是执行上述 Prompt 的 Codex：当前 README 是唯一安装协议。只读取一次并直接执行，不要寻找其他 installer 文档，不要进入 Goal Mode。首次 Prompt 只完成安装、只读预检和用户交接；没有收到用户第二条方向/时长指令前，不创建运营 Threads，也不操作 TikTok。

### 1. 下载与校验

固定来源：

- Repository: `https://github.com/lishehao/tiktok-web-operations`
- Archive: `https://codeload.github.com/lishehao/tiktok-web-operations/zip/refs/heads/main`
- Skill directories: `thread-supervisor/` and `tiktok-web-operations/`
- Install targets: `${CODEX_HOME:-$HOME/.codex}/skills/thread-supervisor` and `${CODEX_HOME:-$HOME/.codex}/skills/tiktok-web-operations`
- Version sources: each Skill's `manifest.json`
- Version protocol: `tiktok-web-operations/references/version-management.md`

通过 HTTPS 下载并安全解压 archive。确认两个目标 Skill 目录各自唯一，并检查：

- 两个 `SKILL.md` 都含有效 `name` 与 `description` frontmatter。
- 两个 `manifest.json` 的 name、version、schema、repository 和 repository_path 可读。
- 两个 `agents/openai.yaml`、所有 references 及 SKILL.md 直接引用的文件存在且可读。

Git、GitHub CLI、Python、Node.js、包管理器和 API Key 都不是消费者依赖。存在 Skill validator 时可以使用；不存在时完成上述等价结构检查。

### 2. 版本决策、安装与升级

在修改本地目录前，完整读取下载包里的 `tiktok-web-operations/references/version-management.md`。先验证固定 repository/name/path 和两个 manifest 的共同 bundle 版本，再把 `YYYY.MM.DD.N` 拆成四段整数比较；同版本时分别对两个完整受管树做确定性内容指纹。内部先记录每个 Skill 的比较结果和唯一 `bundle_action`。

发现未安装、legacy 或 GitHub 版本更高时，版本处理是 installer 的内部步骤，不是用户交接点。不得只回复“发现新版本”、不得询问是否升级，也不得要求用户回复“继续”；在 active-runtime fence 清晰的前提下，直接完成备份、原子安装/升级和安装后校验，并在同一 turn 继续第 3 节只读预检。

- 未安装：安装两个完整 Skill 目录。
- 已安装但没有 manifest：视为 legacy，先完整备份再升级。
- GitHub 版本更高：先确认没有正在使用旧版本的 TikTok 运营任务，然后无需再次询问用户，自动备份旧目录，用同文件系统 sibling staging 替换两个完整受管目录；安装后校验通过即继续只读预检。
- 两个版本和内容都相同：`NOOP`。
- 同版本但内容不同：`BLOCKED_CONFLICT`，不静默覆盖；只有用户明确要求“强制重装/覆盖同版本”才允许 `FORCE_REINSTALL`。
- GitHub 版本更低：`BLOCKED_DOWNGRADE`；只有用户明确要求降级才允许 `FORCE_DOWNGRADE`。
- 旧版本仍被真正 active 的 coordinator/executor 使用：只下载并校验，返回 `DEFERRED_ACTIVE_RUNTIME`；等待 executor 给出 `STOPPED_AND_RELEASED` 后再重试，绝不热覆盖。历史任务、`notLoaded`/已完成任务、已释放 Chrome 且无 uncertain submission 的 idle executor 不算 active runtime，不能因此阻止自动升级。
- 无法确认是否有 active runtime 且将替换现有目录：`BLOCKED_RUNTIME_UNVERIFIED`。
- 任一替换后校验失败：恢复两个旧目录并报告 `ROLLED_BACK`，不继续 TikTok 预检。

不要逐文件混合新旧版本，也不要留下两个不同 bundle 版本。取得单一 installer lock；先验证 archive，再验证同文件系统 staging；通过 whole-directory rename 切换两个目录；最后校验两个准确目标目录。备份放入 `${CODEX_HOME:-$HOME/.codex}/skill-backups/`。任何 explicit force 都不能绕过来源校验、active-runtime fence、备份、安装后校验或回滚。

### 3. 只读预检

安装或自动升级并完成安装后校验后，在同一 turn 继续；先不修改 TikTok，也不创建运营 Threads，只检查：

1. Chrome Browser control 能实际连接，并能用 `chrome.tabs.new()` 创建一个隔离的临时标签页；掉线时最多重连两次。
2. 在这个新标签页里只读打开 TikTok，确认它继承同一 Chrome profile 的登录并记录准确 `@handle`。不要输入、索取或保存密码、OTP、passkey、验证码或恢复码，也不要 claim 其他任务的标签页。
3. 当前页面没有阻塞性的 CAPTCHA、验证挑战、rate limit、warning、restriction 或账号错配。
4. Codex App 能创建、列出、读取、命名、置顶/取消置顶、归档和跨任务发送消息；当前启动任务能通过唯一标题 nonce 自注册准确 Thread ID；`create_thread` 与 `send_message_to_thread` 支持 `gpt-5.6-luna` + `high`。标题/摘要/readability 只发现候选，续写前还要通过 owner-liveness gate。若只缺少置顶工具，记录为非阻塞展示限制。
5. 能写入 canonical object store：先保存 inert bootstrap，再在 executor ID 返回后冻结 identity registry；direction、authority、mission 独立版本化并按 SHA-256 引用，owner/heartbeat/slot 状态另存为 mutable runtime state。自然语言摘要不能作为 registry。
6. 若用户要求无人值守持续运行，`automation_update` 必须支持显式 `targetThreadId`、`repeat=on`、有限 `UNTIL` 或等价截止保护，以及 view readback。真实 heartbeat 只能由已验证的主控台创建和管理，执行台不得自建或续排。
7. 用 `list_threads`/`read_thread` 检查 active TikTok 任务，只用于保护标签页、标记推荐流归因污染和识别精确 mutation 冲突。同账号、同 Chrome 或另一个 TikTok executor 本身都不是 blocker；新 run 创建自己的 tab 并继续。只有同一 target/action 的提交正在进行或状态不确定时，才暂停那个精确 mutation，其他浏览与不同目标动作继续。
8. 能读取真实当地时间、时区、UTC offset，并建立可写 ledger 路径。
9. 完成后只关闭/释放 bootstrap 自己创建的临时标签页。

Chrome Browser control 是 TikTok 写操作的硬依赖。Computer Use、内置 Browser、终端浏览器和普通 Web Search 不能替代。启动任务本身必须留下来成为持久化主任务，并只创建一个用户可见的持久化执行任务；不能用 subagent、agent tree、单个合并任务或其他模型替代。

预检内部记录安装动作、Skill 版本、Chrome/TikTok 状态、准确账号、warning、thread/model 支持、当地时间和 ledger。不要把依赖表、Task ID、tab ID、模型探测、日志或时区计算展示给用户。

### 4. 向用户交接

预检健康时只回复：

```text
状态健康。当前账号：@handle。
你想把这个账号运营成什么方向或人设？也请给出目标地区/主要语言和运行多久；这些字段会决定后续搜索、实际观看、收藏、Repost、评论及未来内容语气，但不能保证具体推荐结果。你可以回复“北美大学生 / dorm life，英语，运行 3 小时”；如果暂时没想法，直接回复“继续”，我会使用默认方向、北美英语和 3 小时。
```

健康交接后立即停止本 turn，等待用户第二条消息。不要创建 Threads，不要搜索 TikTok，不要点击 Favorite/Repost，不要评论，也不要声称运营已启动。

若 Chrome control、TikTok 登录或其他硬依赖缺失，只返回一项用户能够完成的修复动作、影响以及 `完成后回复“继续”`。此时用户回复“继续”只重查缺失项，不重新安装健康 Skill，也不误当成默认运营指令。

### 5. 解析方向与时长

用户第二条消息是启动合同：

- 用户给出方向和时长：按其明确值启动。
- 只给方向：时长使用默认 `3 hours`。
- 只给时长：方向使用默认 `北美大学生 / dorm life`。
- 回复 `继续`、`开始` 或同义表达且预检已健康：使用全部默认值并立即启动。
- 自定义方向缺少地区/语言且无法安全推断时只提一个必要问题；不能把“喜欢狗”等广泛方向静默收敛成中文或英语语境。其余缺省字段直接补默认值。
- 最新明确用户指令覆盖冲突的默认强度、启发式、恢复建议、历史风险权重和旧 mission 字段；不要要求用户重复确认已经给出的方向、时长、强度或动作。
- 已结束的旧 warning、rate limit 或失败只留在 ledger，不阻止新 mission。只有当前页面/工具明确显示 active CAPTCHA/challenge/rate limit/lock/login mismatch、动作不可用、明确失败或提交不确定时，才暂停受影响动作。
- 当前阻塞清除后，在授权和时限仍有效时自动恢复用户原指令；不要求改用“恢复档”，不把建议变成授权门槛，也不扩大用户未授权的动作。

把用户描述整理成一个可执行 `direction_profile`：

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

方向用于保持搜索、消费、互动、评论口吻与未来发帖的一致性。它是运营假设和受众信号设计，不是对 TikTok 推荐算法或触达结果的保证。

默认合同：

- Persona: 北美大学生 / dorm life。
- Audience: 北美大学生、freshman、宿舍与 roommate/campus-life 兴趣人群。
- Pillars: roommate move-in/storytime/chaos、dorm/freshman move-in/setup、college day-in-my-life/campus routine/GRWM、campus friends/game day/tailgate、finals 与 dorm survival failures。
- Exclusions: admissions、SAT/GPA、申请建议、纯学习鸡血和没有校园生活语境的泛内容。
- Voice: 英文、简短、具体、玩梗；评论优先 2–12 个词，绝不超过 30 个词。
- Duration: `3 hours`，standard intensity。
- Post like: 未明确请求时默认 disabled；用户最新明确请求时进入一次 `pending_fresh_gate`，历史失败不要求二次确认。
- Favorite、TikTok Repost、proactive top-level comment: 仅在 strong-core 内容上、各自通过独立持久化 gate 后选择性使用；不设互动配额。

### 6. 用户开始运营后

用户回复方向/时长或使用默认启动词后，调用已安装的 `$tiktok-web-operations`，不要再次运行安装流程。

保留当前启动任务，并注册恰好两个持久化、用户可见的 Luna/High Threads：

```text
TikTok 主控台  gpt-5.6-luna / high  [置顶]
TikTok 执行台  gpt-5.6-luna / high  [不置顶]
```

统一命名格式为 `<平台> <职责>台`。只置顶 `TikTok 主控台`；注册中的
`TikTok 执行台` 即使 idle 也保持未置顶、未归档，以保留历史和回调身份。

完整状态机：

```text
HTTPS 安装/版本比较
  -> 两个 Skills 原子安装或 NOOP
  -> Chrome/TikTok/Thread/Automation 只读预检
  -> 询问方向和时长，等待用户第二条消息
  -> 当前任务自注册为唯一 coordinator
  -> 保存 canonical inert bootstrap
  -> 只创建一个 Luna/High executor
  -> executor ID 返回后冻结 identity registry
  -> SELF_REGISTRY bytes/hash + THREAD_READY ref 双向身份握手
  -> executor 完成只读 stability smoke
  -> 当前用户回合立即执行并验收首个真实 bounded block
  -> coordinator 创建 repeat-on executor operation heartbeat
  -> coordinator 创建低频、只读 supervisor heartbeat
  -> executor 每次 wake 只完成一个 bounded slot；callback 回主控台
  -> 到期/停止/风险 -> STOP_AND_RELEASE
  -> executor 最终结算并回传 EXECUTOR_RELEASED
  -> coordinator 验证释放/最终 ledger -> 清理两个 heartbeat
  -> RUN_COMPLETED -> 向用户返回一条简短总结果 -> idle
  -> 活跃主控/执行台保持未归档；临时诊断与已释放的退休执行台归档
```

启动顺序：

1. 当前任务生成唯一 `run_id/run_nonce`，先用一次临时 nonce 标题通过 `list_threads` 与 `read_thread` 证明自己的准确 ID，保存唯一 canonical inert bootstrap，再把最终标题固定为 `TikTok 主控台` 并置顶。它拥有用户对话、版本化 direction/authority/mission、能力矩阵和风险；绝不碰 Chrome。
2. 只创建一个最终标题为 `TikTok 执行台` 的任务，明确保持未置顶，并强制 `gpt-5.6-luna/high`。它每个 block 默认用 `chrome.tabs.new()` 创建自己的隔离标签页，是本 run 的 mutation/ledger writer；不得碰其他任务标签页、扩大授权、创建其他 Threads 或回调其他任务。同账号的其他独立 run 可以并存。
3. `create_thread` 初始提示只嵌入一次 canonical bootstrap，不重复写账号/角色/授权/方向/ledger/stop prose。准确 executor ID 返回后才冻结 identity registry，并把同一份 UTF-8 JSON bytes/hash 通过 `SELF_REGISTRY` 发送；`THREAD_READY` 必须回显准确 `registry_ref`。所有创建和跨任务消息都显式指定 `gpt-5.6-luna/high`。
   任何后续复用都必须重新证明可续写；已归档 TikTok 执行台默认 retired，不自动解除归档。
4. 把准确账号、`direction_profile`、`operation_stop_at`、搜索簇、排除项、互动授权、能力矩阵、ledger 和停止条件交给执行任务。
5. 主任务向 executor 派发只读 `stability_smoke_01`：一个方向搜索词评估 3 张结果卡，实际从搜索点开 1 条 strong-core 视频，验证直接帖子身份、播放进度和 premise/payoff；随后单独尝试最多 5 个连续 For You 身份。零 mutation。
6. 在当前启动 turn 内读取 executor 的真实 proof。主运行通过要求：3 张搜索卡已评估、至少 1 个 `qualified_search_view`、账号/tab 稳定、ledger 可解析、零 mutation。For You 成功只验证可选的推荐流验证 lane；native next/down 失败本身不阻止搜索训练启动。
7. Smoke 通过后，在当前用户回合立即执行并验收首个真实搜索训练 block，不把首轮 proof 延后到 Heartbeat。
8. 对超过一个 bounded block 的计时型运营，主控台创建两个真正长期 recurring Heartbeat：`operation_heartbeat` 显式 `targetThreadId=executor_thread_id`、`repeat=on`、带有限 `UNTIL`/`operation_stop_at`；`supervisor_heartbeat` 显式 `targetThreadId=coordinator_thread_id`、低频、只读、同样有截止保护。创建后分别 view，核对准确 ID、target、repeat、next run、本地/UTC 与截止。禁止 `COUNT=1` 后靠执行台自续；执行台永远不创建、更新、续排或删除 automation。
9. 首次 `INSTALL` 的 `+15/+35/+60` 监督复用 supervisor heartbeat，不改 operation cadence，也不创建第三个 automation。监督读取执行台真实 wake/new turn/callback/proof，以及 `planned/started/completed/blocked/missed` slot ledger；缺 wake、缺 proof、repeat 断链或 next run 丢失必须回主控台报告 `SCHEDULER_CONTINUATION_FAILURE`。
10. 到期、用户停止或目标完成时，Heartbeat 只触发终止流程，不代表完成。主控台暂停 operation heartbeat 并向准确执行台发送一次 `STOP_AND_RELEASE`；执行台不得新增浏览或互动，只解决提交确定性、释放 tab、写最终累计 checkpoint，并回传 `EXECUTOR_RELEASED`。主控台验证后才删除两个 Heartbeat、标记 `RUN_COMPLETED` 并向用户返回一条简短总结果。
11. 两个 Heartbeat 创建后及每次有效 supervisor Heartbeat 都必须向用户返回三行。先 view 两个准确 automation，确认 target/repeat/next time/截止后再报告；不能凭推算承诺时间：

```text
本轮完成：<一句话>
下次心跳：<YYYY-MM-DD HH:mm 时区>
下轮计划：<一个有边界的目标>
```

执行台仍在运行时，下轮计划只能是等待 callback，不能重叠派发；`decision_required=true` 时写等待用户决定且不执行新 TikTok 操作，`false` 时写下一次只读恢复条件检查并保留原授权；最终 Heartbeat 写 `下次心跳：无（进入终止结算）`，整体完成后写 `无（任务已完成）`。

如果主任务无法自注册、executor 创建/握手失败、首轮没有 proof、独立标签页创建失败或 scheduler binding 不明确，不得声称长期运营已启动。同账号另一个任务存在本身不构成失败。

## 运营规则摘要

### 搜索训练与推荐流验证

- 搜索训练是默认主流程；For You 是低频留出验证，不是每个 block 的后半段。
- 搜索结果卡只证明 query 质量。只有从搜索/hashtag/creator 表面实际点开 strong-core 视频、验证帖子身份和播放进度，并看懂 premise/payoff，才计入 `qualified_search_view`。
- 默认训练 block：三个不同搜索簇，各评估前五张卡并实际观看合格 core 结果，通常累计 9–15 个 qualified views。不能用缩略图、caption 或已知 direct URL 冒充消费。
- 每两个训练 block 或约 20–30 个 qualified views，再运行一次 5–10 条连续 For You 验证。搜索评估数、qualified views、For You core/directional/drift shares 分开记录。
- For You native next/down 失败只使验证 lane 成为 `partial|unavailable`；账号、tab、搜索播放和平台安全仍健康时，搜索训练继续。连续两次可停用本 runtime 的验证 lane，但不得自动换 scroll/keyboard/wheel/reload。
- 不承诺搜索观看、收藏、Repost 或评论一定改变算法；只比较连续留出样本的观察变化。

### 稳定性断路器

- 持久化只依靠两个用户可见 canonical Threads、callback，以及主控台管理的两个长期 Heartbeat；禁止 `create_goal`、`update_goal`、subagent、agent tree 和执行台自建 replacement worker。只有主控台能对已明确证实的 stale tombstone 做一次内部替换。
- Executor 每个 wake/turn 只执行一个有边界 block，完成后释放 Chrome、callback、idle；它不创建或续排 Heartbeat。
- TikTok 主控台是唯一用户决策入口。Executor 遇到 `blocked`、`validation_failed`、`needs_decision`、`key_risk`、uncertain submission 或平台风险时，必须先停止当前 block、释放自己的 Chrome、写 ledger，再只向注册的 TikTok 主控台回调并 idle；不得在 TikTok 执行台里询问用户、提出继续按钮、自行恢复或派发下一轮。
- TikTok 主控台收到上述非成功状态后必须暂停新 dispatch，把风险、影响范围、当前已停止内容、是否仍可安全只读、推荐方案和不超过三个选项合并成一次用户提示。只有用户在 TikTok 主控台明确回复继续方式，或风险被可验证的外部状态变化消除后，才可恢复。用户无需查看或回复 TikTok 执行台。
- `decision_required=false` 的当前平台等待不得被改写成用户确认：主控台保存原指令和最短可观察恢复条件，状态清除后自动恢复。只有人工登录/挑战、提交不确定、授权缺失或扩大、版权披露等真正需要用户选择的情况才询问用户。
- 每个多轮计时型 run 在首轮 proof 后由 coordinator 管理两个长期 repeat-on Heartbeat：operation 精确绑定 executor，supervisor 精确绑定 coordinator。executor 只接受 operation wake，不管理 automation；supervisor 只读核验持续性。两个都必须有截止保护并禁止一次性自续链。
- 每个普通 block 的 `completed` 只表示该轮完成；Heartbeat 到点也只表示时间到了。整场完成必须经过 `STOP_REQUESTED -> EXECUTOR_RELEASED -> RUN_COMPLETED`，并由 TikTok 主控台给用户一条最终汇总。
- TikTok supervisor Heartbeat 不静默：每次都固定报告“本轮完成 / 下次心跳 / 下轮计划”三行。下次时间必须来自两个 automation 的 readback，使用用户本地日期、时间和时区；不展示 automation ID。
- 两个 Thread 都只承担一个目标：TikTok 主控台只负责在授权和截止时间内推进下一步或停下并向用户集中决策；TikTok 执行台只负责准确执行当前唯一 block、写证据、释放 Chrome、callback、idle。方向、人设、能力矩阵和政策都是输入约束，不是额外使命。
- 首次安装监督是唯一自动例外：仅当持久化安装状态显示首次 `INSTALL` 后尚未消费，第一次运营启动才自动开启一次，检查点约为 `+15/+35/+60` 分钟。它只监督、不连续轮询；健康时也使用固定三行回执，风险仍统一回 TikTok 主控台。状态保存在受管 Skill 目录之外，不记录凭据，窗口消费后永不因升级或新任务重置。
- 不硬编码 Chrome Skill 的版本缓存路径；只使用当前 runtime 与受支持的 Playwright locator。
- 只从 CAPTCHA、challenge、系统 dialog/banner/toast、账号 warning 等明确系统 UI 判断风险；caption、hashtag、comment 或搜索内容里的 `warning`/`verify` 字样不是平台警告。
- 一个失败类型最多允许一个窄 recovery。账号、tab ownership、搜索 origin/open/playback、平台风险或写操作证据连续失败两次才打开 whole-run 断路器；For You transition 失败按验证 lane 隔离。改关键词、删 hashtag、换输入法或宣称“fresh audit”不能重置真正的断路器。
- Native next/down 失败后不自动切 PageDown、ArrowDown、wheel、script scroll、reload 或 reset；记录 partial/unavailable 并继续下一次独立搜索训练。Scroll-only 验证仍需用户另行明确授权。
- Native next/down 必须从位置 1 起锁定方向特定的精确签名；禁止使用 `button:not([disabled])` 一类宽 locator，因为第一次推进后 up/down 通常都会 enabled。每次 DOM 移动后重新解析同一 down 签名。
- 预期 UI gate 失败必须在当前判断分支直接写终态、释放 Chrome、callback；不能用 `throw` 返回 reasoning 后继续换 locator 诊断。
- Identity registry 只保存结构化 run/coordinator/executor/account/profile/ledger/writer identity；方向、授权、mission/stop time 独立版本化，owner/heartbeat/slot/next-run 属于 mutable runtime state。Dispatch/callback/heartbeat 只携带已接受的 registry/direction/authority/mission refs 与准确工具 ID，不手写同义文本。引用漂移在 Chrome 前停止并只执行一次 `REGISTRY_RECONCILIATION`。
- Heartbeat 醒来后按角色验证：operation 必须醒在 executor；supervisor 必须醒在 coordinator。任一 target/ID/repeat/run 不匹配只返回 `MISBOUND_HEARTBEAT_NO_ACTION`，不得转发、接管或操作 TikTok。
- Tab ID 不得跨 turn、prompt 或 ledger 复用。普通 block 默认直接调用 `chrome.tabs.new()`，只操作该 executor 本轮创建或已经控制的标签页；`openTabs()`/`claimTab()` 只用于用户明确要求的现有标签页交接。
- Chrome 标签页控制权不是整个 Chrome profile 或 TikTok 账号的全局锁。若某个现有 tab 属于另一个 browser session，跳过它并新建自己的 tab；不得擅自中断、归档、导航或关闭对方任务。同账号其他 run 的浏览或不同目标 mutation 允许并行，只标记推荐流归因污染。只有新建 tab/登录验证失败、本 executor 提交不确定，或相同 target/action 正在提交/不确定时，才暂停受影响范围。
- 一次页面加载失败不等于 TikTok 风控。执行台先分清 stale tab/browser disconnect、DNS/网络 `ERR_*`、代理/TLS、HTTP 429/403/5xx、`ERR_BLOCKED_BY_CLIENT` 和空白/脚本加载失败；记录错误码与 URL 后，在原登录 Chrome 内短暂等待并重试当前页，必要时从同一 browser binding 新建专属 tab，并用 TikTok 首页/中性 HTTPS 诊断全网、单域或单页范围。恢复后必须重新确认账号、目标页、系统 warning 和提交确定性才继续；不得切 Computer Use/其他浏览器、绕过 TLS/登录或重试不确定写操作。持久失败或账号/CAPTCHA/429/限流统一回 TikTok 主控台。
- 用户解释必须由 exact error code 加同域/中性页探测共同生成，并明确写成“可能原因”，不得断言根因。`ERR_NETWORK_CHANGED` 对应网络接口/VPN/代理可能切换，`ERR_CONNECTION_RESET` 对应连接可能被网络路径/VPN/服务端/安全软件重置，`ERR_NAME_NOT_RESOLVED` 对应域名/DNS 可能失败，`5xx` 对应站点服务可能异常，`ERR_BLOCKED_BY_CLIENT` 对应扩展或过滤规则可能拦截。暂态恢复后继续任务，不单独打扰用户，只在下一次三行回执的“本轮完成”中简短说明；持续失败回主控台，必须带 exact code、可能原因、已尝试动作和最小用户操作。回执永远不增加第四行。
- Coordinator 的 `send_message_to_thread` 工具目标必须等于 canonical identity registry 中的 executor ID。若失败明确来自未送达的 target typo，可记录后纠正一次；正确目标上的传输失败不得反复重试。
- 若摘要索引仍能发现 executor，但续写返回 `failed to resolve rollout path` 且底层文件不存在/`ENOENT`，把它记为 `STALE_OWNER_TOMBSTONE`，而不是账号风险：停止对旧 ID 重发，先清理指向旧 ID 的 automation，再从 registry 退休旧 ID，只创建一个替代执行台，并验证 new ID、mission dispatch、operation heartbeat binding、零 orphan automation 和唯一 canonical owner。host unavailable、timeout、网络或工具暂态错误只做有界复核，绝不立即归档或替换。

### 互动能力

- Post like 保持独立；未请求时默认 disabled，最新指令明确请求时运行一次 fresh persistence gate。旧 mission 的失败只作历史证据。
- Favorite 点击一次后，必须在即时、约 +3 秒和总计 +10 秒保持 selected，之后才刷新/重开并检查账号 Favorites exact URL。
- Repost 只指实际 `Repost`/`Undo repost` 状态。允许只读打开 Share sheet 寻找明确 Repost；禁止执行 generic Share、Copy link、Send 或其他分享目标。
- 主动顶层评论必须理解视频 setup/payoff，使用视频语言，优先 2–12 个英文词，硬上限 30 个词，并逐条刷新验证。
- 不在同一视频机械堆叠 Favorite + Repost + Comment；选择最小、真实、合适的信号。没有合格候选时零互动完全合法。
- 不宣称某种互动一定增加账号权重，也不承诺推荐或曝光结果。

### 停止条件

当前登录错配、CAPTCHA、验证挑战、rate limit、warning/restriction、账号变化、失去专属标签页控制、相同 target/action 提交冲突、Thread/automation identity mismatch、hard runtime change、uncertain submission 或持久化失败时，停止对应 mutation 并保留证据。已结束的历史事件不持续阻塞。风险统一回调 TikTok 主控台；能通过明确外部状态清除的 blocker 不要求用户二次确认，清除后按原指令自动恢复。真正需要人工处理或选择时才等待决策。用户说停止时执行同一整场终止事务：执行台最终结算并回传释放证明，主控台验证后才清理两个 Heartbeat 和宣布安全停止。两个运营 Threads 保持 idle。临时探针/诊断完成释放后归档；已被替换的退休执行台仅在确认无 heartbeat、Chrome tab 或不确定 mutation 后归档。

用户侧最终输出保持简单：

```text
运营完成。运行：<duration>；浏览：<count>；收藏：<count>；Repost：<count>；评论：<count>。风险：无｜<一句话风险>。
```

不要向用户展示 Heartbeat ID、callback ID、registry、内部状态名或释放协议；只有 finalization 被阻塞时才给一项简短修复或决策。

## Requirements

- Codex 本地 Skill 支持。
- ChatGPT Chrome Extension 提供的 Chrome Browser control。
- 用户已在同一 Chrome profile 登录 TikTok。
- Codex App 持久化 Thread 管理与跨任务消息能力。
- `gpt-5.6-luna/high` 可用于两条运营 Threads。
- 能访问 GitHub HTTPS archive。

## Repository Layout

```text
README.md
thread-supervisor/
  SKILL.md
  manifest.json
  agents/
  references/
tiktok-web-operations/
  SKILL.md
  manifest.json
  agents/
  references/
```

## Boundaries

只操作用户明确授权的账号和浏览器会话。不要保存凭据、cookies、Chrome profile、TikTok 导出或运营 ledger。不得批量养号、规避平台执法、刷量、垃圾互动、骚扰、歧视、冒充身份或伪造经验。发布内容还必须满足版权、披露和 AIGC 标记要求。

## 发布维护

TikTok Skill 的 `references/distribution-and-upgrades.md` 是 bundle 维护协议。任何 material change 都必须递增版本、同步 README 与两个完整 Skills、重建本地 ZIP，并从新的 GitHub archive 反向验证。

## License

MIT
