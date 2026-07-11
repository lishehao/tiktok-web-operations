# TikTok Web Operations

这是 TikTok 运营 bundle 的公开分发仓库。公开仓库只保留一个安装入口、通用 `thread-supervisor` Skill 和完整 `tiktok-web-operations` Skill；详细规则以两个 Skills 内 references 为准。

Protocol version: `2026.07.11.19`

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
4. Codex App 能创建、列出、读取、命名、置顶/取消置顶、归档和跨任务发送消息；当前启动任务能通过唯一标题 nonce 自注册准确 Thread ID；`create_thread` 与 `send_message_to_thread` 支持 `gpt-5.6-luna` + `high`。若只缺少置顶工具，记录为非阻塞展示限制。
5. 能建立 immutable run registry，保存 run ID、主/执行 Thread ID、host/project、授权、ledger、stop time，以及 automation owner/ID/target。
6. 若用户要求无人值守持续运行，`automation_update` 必须支持显式 `targetThreadId` 与 view readback。真实 heartbeat 只能在主任务自注册后由主任务自己创建，不能预先挂到 installer、Skill-development 或其他任务。
7. 用 `list_threads`/`read_thread` 检查所有 active TikTok 任务；不得在旧的同账号 mutation executor、Goal Mode 或其 subagent 仍 active/uncertain 时创建新 executor。无关任务占用另一个 Chrome tab 不构成全局 blocker；若它同时只读浏览同一 TikTok 账号，只标记推荐流归因污染。若用户要求替换 mutation executor，先取得 `STOPPED_AND_RELEASED`，不能把 archive 当成 release proof。
8. 能读取真实当地时间、时区、UTC offset，并建立可写 ledger 路径。
9. 完成后只关闭/释放 bootstrap 自己创建的临时标签页。

Chrome Browser control 是 TikTok 写操作的硬依赖。Computer Use、内置 Browser、终端浏览器和普通 Web Search 不能替代。启动任务本身必须留下来成为持久化主任务，并只创建一个用户可见的持久化执行任务；不能用 subagent、agent tree、单个合并任务或其他模型替代。

预检内部记录安装动作、Skill 版本、Chrome/TikTok 状态、准确账号、warning、thread/model 支持、当地时间和 ledger。不要把依赖表、Task ID、tab ID、模型探测、日志或时区计算展示给用户。

### 4. 向用户交接

预检健康时只回复：

```text
状态健康。当前账号：@handle。
你想把这个账号运营成什么方向或人设？方向会决定后续搜索、浏览、收藏、Repost、评论，以及未来内容的主题与语气，帮助形成更一致的受众信号；但不能保证具体推荐或分发结果。
也请告诉我希望运行多久。你可以回复“北美大学生 / dorm life，运行 3 小时”；如果暂时没想法，直接回复“继续”，我会按默认方向和默认 3 小时开始。
```

健康交接后立即停止本 turn，等待用户第二条消息。不要创建 Threads，不要搜索 TikTok，不要点击 Favorite/Repost，不要评论，也不要声称运营已启动。

若 Chrome control、TikTok 登录或其他硬依赖缺失，只返回一项用户能够完成的修复动作、影响以及 `完成后回复“继续”`。此时用户回复“继续”只重查缺失项，不重新安装健康 Skill，也不误当成默认运营指令。

### 5. 解析方向与时长

用户第二条消息是启动合同：

- 用户给出方向和时长：按其明确值启动。
- 只给方向：时长使用默认 `3 hours`。
- 只给时长：方向使用默认 `北美大学生 / dorm life`。
- 回复 `继续`、`开始` 或同义表达且预检已健康：使用全部默认值并立即启动。
- 方向或时长会实质改变账号定位时才提一个必要问题；其余缺省字段直接补默认值，不再要求确认。

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
- Post like: disabled。
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
  -> 建立 immutable run registry
  -> 只创建一个 Luna/High executor
  -> SELF_REGISTRY + THREAD_READY 双向身份握手
  -> executor 完成只读 stability smoke
  -> coordinator 创建并回读本 run 唯一 durable timer heartbeat
  -> 首次 INSTALL 的第一次运营：同一 timer 使用首小时监督日程
  -> callback -> coordinator 决策 -> 一个下一 bounded block
  -> 到期/停止/风险 -> STOP_AND_RELEASE
  -> executor 释放 Chrome -> coordinator 清理自己的 heartbeat -> idle
  -> 活跃主控/执行台保持未归档；临时诊断与已释放的退休执行台归档
```

启动顺序：

1. 当前任务生成唯一 `run_id/run_nonce`，先用一次临时 nonce 标题通过 `list_threads` 与 `read_thread` 证明自己的准确 ID，写入 immutable run registry，再把最终标题固定为 `TikTok 主控台` 并置顶。它拥有用户对话、`direction_profile`、时长、授权、能力矩阵、风险和 executor registry；绝不碰 Chrome。
2. 只创建一个最终标题为 `TikTok 执行台` 的任务，明确保持未置顶，并强制 `gpt-5.6-luna/high`。它每个 block 默认用 `chrome.tabs.new()` 创建自己的隔离标签页，是同账号 mutation 和 ledger 的唯一 writer；不得碰其他任务标签页、扩大授权、创建其他 Threads 或回调其他任务。
3. 记录主任务与执行任务的准确 ID、host/project、run ID、授权版本、ledger 和停止时间，通过 `SELF_REGISTRY` 与 `THREAD_READY` 完成双向握手；所有创建和跨任务消息都显式指定 `gpt-5.6-luna/high`。
4. 把准确账号、`direction_profile`、`operation_stop_at`、搜索簇、排除项、互动授权、能力矩阵、ledger 和停止条件交给执行任务。
5. 主任务向 executor 派发只读 `stability_smoke_01`：一个方向搜索词观察 3 条，再进入一次连续 For You，用唯一 native next/down 控件取得 5 个可靠位置；零 reload/reset、零 mutation。
6. 在当前启动 turn 内读取 executor 的真实 proof。只有 3 条搜索结果、5 个可靠 feed identity、4 次成功 native advance、零 reset、零 mutation才算 stability pass；页面 blocker 是证据，但不算稳定通过。
7. 对超过一个 bounded block 的计时型运营，只有现在才由已验证的主任务创建本 run 唯一 durable timer heartbeat：显式设置 `targetThreadId=coordinator_thread_id`，名称和 prompt 包含 run ID 与 `operation_stop_at`；创建后 view 同一 automation ID，并要求 `automation_owner_thread_id == targetThreadId == coordinator_thread_id`。执行任务永远不创建 automation。Callback 负责事件到达，timer 负责下一次检查和最终截止；整个 run 复用同一个 timer，不为每个 block 新建。
8. 若本机安装状态是首次 `INSTALL` 且 `first_install_supervision=PENDING`，Smoke 通过后由 TikTok 主控台把它消费为一次性的首小时监督窗口。默认在启动后约 `+15`、`+35`、`+60` 分钟只读检查 TikTok 执行台最新状态、callback 和 ledger；健康时静默，风险只在 TikTok 主控台汇总。窗口不得超过 `operation_stop_at`，结束或用户提前停止时删除自己的监督 heartbeat，并写 `CONSUMED`。升级、后续运营任务、重启和新 run 都不得再次创建该窗口。
9. Smoke 及 heartbeat binding（若需要）都通过后，才可派完整 `search_heavy` 或互动 block。之后当前主任务继续 callback 驱动的有边界 blocks，直到 `operation_stop_at`；它不归档自己，两条运营 Threads 都保持未归档和持久化，且只置顶 TikTok 主控台。

如果主任务无法自注册、executor 创建/握手失败、首轮没有 proof、独立标签页创建失败或同账号 mutation writer 不明确，不得声称运营已启动，也不得进行 TikTok 写操作。

## 运营规则摘要

### 垂直校准

- 默认采用 search-heavy：三个批准搜索簇，每簇按顺序观察五条，再回到一次连续 For You checkpoint。
- For You 位置 1 后优先使用页面可见的 native next/down 控件逐条前进；不能用 reload、Home reset 或重新打开页面制造新样本。
- 每条内容标记 `core`、`adjacent`、`irrelevant` 或 `harmful_to_direction`；商品、旧内容和漂移内容都计入分母。
- 定期比较搜索结果与 For You 的 core/directional/drift shares，再调整搜索簇。

### 稳定性断路器

- 持久化只依靠两个用户可见 Threads 与 callback；禁止 `create_goal`、`update_goal`、subagent、agent tree 和自建 replacement worker。
- Executor 每个 turn 只执行一个有边界 block，完成后释放 Chrome、callback、idle。多轮运行由 coordinator 在上一轮完成后逐轮派发。
- TikTok 主控台是唯一用户决策入口。Executor 遇到 `blocked`、`validation_failed`、`needs_decision`、`key_risk`、uncertain submission 或平台风险时，必须先停止当前 block、释放自己的 Chrome、写 ledger，再只向注册的 TikTok 主控台回调并 idle；不得在 TikTok 执行台里询问用户、提出继续按钮、自行恢复或派发下一轮。
- TikTok 主控台收到上述非成功状态后必须暂停新 dispatch，把风险、影响范围、当前已停止内容、是否仍可安全只读、推荐方案和不超过三个选项合并成一次用户提示。只有用户在 TikTok 主控台明确回复继续方式，或风险被可验证的外部状态变化消除后，才可恢复。用户无需查看或回复 TikTok 执行台。
- 每个多轮计时型 run 默认只给 coordinator 配一个长期 timer heartbeat，作为低频状态检查、漏回调保险和 `operation_stop_at` 截止时钟。它必须由 coordinator 自己创建并显式绑定/回读自己的准确 Thread ID；executor、installer、Skill-development 和其他 coordinator 都不能代建或接管。executor 运行中保持静默，heartbeat 不能碰 Chrome、重建任务、绕过 blocker 或并发派发。
- 两个 Thread 都只承担一个目标：TikTok 主控台只负责在授权和截止时间内推进下一步或停下并向用户集中决策；TikTok 执行台只负责准确执行当前唯一 block、写证据、释放 Chrome、callback、idle。方向、人设、能力矩阵和政策都是输入约束，不是额外使命。
- 首次安装监督是唯一自动例外：仅当持久化安装状态显示首次 `INSTALL` 后尚未消费，第一次运营启动才自动开启一次，检查点约为 `+15/+35/+60` 分钟。它只监督、不连续轮询；健康静默，风险仍统一回 TikTok 主控台。状态保存在受管 Skill 目录之外，不记录凭据，窗口消费后永不因升级或新任务重置。
- 不硬编码 Chrome Skill 的版本缓存路径；只使用当前 runtime 与受支持的 Playwright locator。
- 只从 CAPTCHA、challenge、系统 dialog/banner/toast、账号 warning 等明确系统 UI 判断风险；caption、hashtag、comment 或搜索内容里的 `warning`/`verify` 字样不是平台警告。
- 一个失败类型最多允许一个窄 recovery；同类连续失败两次立即开断路器、释放 Chrome、callback 并 idle。改关键词、删 hashtag、换输入法或宣称“fresh audit”不能重置断路器。
- Native next/down 失败后不自动切 PageDown、ArrowDown、wheel、script scroll、reload 或 reset。Scroll-only fallback 必须由用户在收到 blocker 后重新明确授权。
- Native next/down 必须从位置 1 起锁定方向特定的精确签名；禁止使用 `button:not([disabled])` 一类宽 locator，因为第一次推进后 up/down 通常都会 enabled。每次 DOM 移动后重新解析同一 down 签名。
- 预期 UI gate 失败必须在当前判断分支直接写终态、释放 Chrome、callback；不能用 `throw` 返回 reasoning 后继续换 locator 诊断。
- Run ID、Coordinator/executor ID、host/project、账号、ledger path、授权、角色、模型、thinking、automation owner/ID/target 和 stop time 都是 immutable registry；dispatch、callback 和 heartbeat 必须逐字比较，任何漂移都以 `registry_mismatch` 或 `AUTOMATION_OWNERSHIP_MISMATCH` 终止。
- Heartbeat 醒来后先验证 `waking_thread_id == targetThreadId == coordinator_thread_id` 和准确 automation ID；若被挂到别的 Thread，只返回 `MISBOUND_HEARTBEAT_NO_ACTION`，不得转发、接管或操作 TikTok。
- Tab ID 不得跨 turn、prompt 或 ledger 复用。普通 block 默认直接调用 `chrome.tabs.new()`，只操作该 executor 本轮创建或已经控制的标签页；`openTabs()`/`claimTab()` 只用于用户明确要求的现有标签页交接。
- Chrome 标签页控制权不是整个 Chrome profile 的全局锁。若某个现有 tab 属于另一个 browser session，跳过它并新建自己的 tab；不得擅自中断、归档、导航或关闭对方任务。只有新建 tab 失败、账号继承/登录验证失败、同账号 mutation writer 冲突或 uncertain submission 才阻塞。并发只读浏览同一账号时必须标记推荐流归因污染。
- Coordinator 的 `send_message_to_thread` 工具目标本身也属于 immutable registry。若失败明确来自未送达的 target typo，可记录后纠正一次；正确目标上的传输失败不得反复重试。

### 互动能力

- Post like 保持独立且默认 disabled。
- Favorite 点击一次后，必须在即时、约 +3 秒和总计 +10 秒保持 selected，之后才刷新/重开并检查账号 Favorites exact URL。
- Repost 只指实际 `Repost`/`Undo repost` 状态。允许只读打开 Share sheet 寻找明确 Repost；禁止执行 generic Share、Copy link、Send 或其他分享目标。
- 主动顶层评论必须理解视频 setup/payoff，使用视频语言，优先 2–12 个英文词，硬上限 30 个词，并逐条刷新验证。
- 不在同一视频机械堆叠 Favorite + Repost + Comment；选择最小、真实、合适的信号。没有合格候选时零互动完全合法。
- 不宣称某种互动一定增加账号权重，也不承诺推荐或曝光结果。

### 停止条件

登录错配、CAPTCHA、验证挑战、rate limit、warning/restriction、账号变化、失去专属标签页控制、同账号 mutation writer 冲突、Thread/automation identity mismatch、hard runtime change、uncertain submission 或持久化失败时，停止对应 mutation 并保留证据，风险统一回调 TikTok 主控台等待决策。用户说停止时，executor 只释放自己的标签页并写 final checkpoint，主任务只暂停/删除自己 registry 中的 heartbeat；两个运营 Threads 保持 idle。临时探针/诊断完成释放后归档；已被替换的退休执行台仅在确认无 heartbeat、Chrome tab 或不确定 mutation 后归档。

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
