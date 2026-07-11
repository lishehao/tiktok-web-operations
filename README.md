# TikTok Web Operations

这是 `tiktok-web-operations` Codex Skill 的公开分发仓库。公开仓库只保留一个安装入口和一个完整 Skill；详细运营规则以 Skill 内 references 为准。

Protocol version: `2026.07.11.10`

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
- Skill directory: `tiktok-web-operations/`
- Install target: `${CODEX_HOME:-$HOME/.codex}/skills/tiktok-web-operations`
- Version source: `tiktok-web-operations/manifest.json`
- Version protocol: `tiktok-web-operations/references/version-management.md`

通过 HTTPS 下载并安全解压 archive。确认目标 Skill 目录唯一，并检查：

- `SKILL.md` 含有效 `name` 与 `description` frontmatter。
- `manifest.json` 的 name、version、schema 和 repository 可读。
- `agents/openai.yaml`、所有 references 及 SKILL.md 直接引用的文件存在且可读。

Git、GitHub CLI、Python、Node.js、包管理器和 API Key 都不是消费者依赖。存在 Skill validator 时可以使用；不存在时完成上述等价结构检查。

### 2. 版本决策、安装与升级

在修改本地目录前，完整读取下载包里的 `references/version-management.md`。先验证固定 repository/name/path，再把 `YYYY.MM.DD.N` 拆成四段整数比较；同版本时对完整受管树做确定性内容指纹。内部先记录 `local_version`、`incoming_version`、`version_relation`、`content_relation`、`active_runtime` 和唯一 `install_action`。

- 未安装：安装完整 Skill 目录。
- 已安装但没有 manifest：视为 legacy，先完整备份再升级。
- GitHub 版本更高：先确认没有正在使用旧版本的 TikTok 运营任务，再备份旧目录，用同文件系统 sibling staging 原子替换整个受管目录。
- 版本和内容都相同：`NOOP`。
- 同版本但内容不同：`BLOCKED_CONFLICT`，不静默覆盖；只有用户明确要求“强制重装/覆盖同版本”才允许 `FORCE_REINSTALL`。
- GitHub 版本更低：`BLOCKED_DOWNGRADE`；只有用户明确要求降级才允许 `FORCE_DOWNGRADE`。
- 旧版本仍被 active coordinator/executor 使用：只下载并校验，返回 `DEFERRED_ACTIVE_RUNTIME`；等待 executor 给出 `STOPPED_AND_RELEASED` 后再重试，绝不热覆盖。
- 无法确认是否有 active runtime 且将替换现有目录：`BLOCKED_RUNTIME_UNVERIFIED`。
- 替换后校验失败：恢复旧目录并报告 `ROLLED_BACK`，不继续 TikTok 预检。

不要逐文件混合新旧版本。取得单一 installer lock；先验证 archive，再验证同文件系统 staging；通过 whole-directory rename 切换；最后校验准确目标目录。备份放入 `${CODEX_HOME:-$HOME/.codex}/skill-backups/`。任何 explicit force 都不能绕过来源校验、active-runtime fence、备份、安装后校验或回滚。

### 3. 只读预检

安装完成后先不修改 TikTok，也不创建运营 Threads，只检查：

1. Chrome Browser control 能实际连接，并能用 `chrome.tabs.new()` 创建一个隔离的临时标签页；掉线时最多重连两次。
2. 在这个新标签页里只读打开 TikTok，确认它继承同一 Chrome profile 的登录并记录准确 `@handle`。不要输入、索取或保存密码、OTP、passkey、验证码或恢复码，也不要 claim 其他任务的标签页。
3. 当前页面没有阻塞性的 CAPTCHA、验证挑战、rate limit、warning、restriction 或账号错配。
4. Codex App 能创建、读取、命名、归档和跨任务发送消息；`create_thread` 与 `send_message_to_thread` 支持 `gpt-5.6-luna` + `high`。
5. 用 `list_threads`/`read_thread` 检查所有 active TikTok 任务；不得在旧的同账号 mutation executor、Goal Mode 或其 subagent 仍 active/uncertain 时创建新 executor。无关任务占用另一个 Chrome tab 不构成全局 blocker；若它同时只读浏览同一 TikTok 账号，只标记推荐流归因污染。若用户要求替换 mutation executor，先取得 `STOPPED_AND_RELEASED`，不能把 archive 当成 release proof。
6. 能读取真实当地时间、时区、UTC offset，并建立可写 ledger 路径。
7. 完成后只关闭/释放 bootstrap 自己创建的临时标签页。

Chrome Browser control 是 TikTok 写操作的硬依赖。Computer Use、内置 Browser、终端浏览器和普通 Web Search 不能替代。两条运营任务必须都是持久化、用户可见的 Codex Threads；不能用 subagent、agent tree、单个合并任务或其他模型替代。

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

创建并注册恰好两个持久化、用户可见的 Luna/High Threads：

```text
TikTok 运营主任务       gpt-5.6-luna / high
TikTok Chrome执行任务  gpt-5.6-luna / high
```

启动顺序：

1. 创建 `TikTok 运营主任务`。它拥有用户对话、`direction_profile`、时长、授权、能力矩阵、风险和 executor registry；绝不碰 Chrome。
2. 创建 `TikTok Chrome执行任务`。它每个 block 默认用 `chrome.tabs.new()` 创建自己的隔离标签页，是同账号 mutation 的唯一 writer 和 ledger writer；不得碰其他任务标签页、扩大授权、创建其他 Threads 或回调 bootstrap 任务。
3. 记录两条准确 Thread ID，通过 `SELF_REGISTRY` 与 `THREAD_READY` 完成双向握手；所有创建和跨任务消息都显式指定 `gpt-5.6-luna/high`。
4. 把准确账号、`direction_profile`、`operation_stop_at`、搜索簇、排除项、互动授权、能力矩阵、ledger 和停止条件交给两条任务。
5. Coordinator 先向同一 executor 派发只读 `stability_smoke_01`：一个方向搜索词观察 3 条，再进入一次连续 For You，用唯一 native next/down 控件取得 5 个可靠位置；零 reload/reset、零 mutation。
6. 在当前启动 turn 内读取 executor 的真实 proof。只有 3 条搜索结果、5 个可靠 feed identity、4 次成功 native advance、零 reset、零 mutation 才算 stability pass；页面 blocker 是证据，但不算稳定通过。
7. Smoke 通过后才可派完整 `search_heavy` 或互动 block。之后 coordinator 继续 callback 驱动的有边界 blocks，直到 `operation_stop_at`；bootstrap 任务才可归档自己。两条运营 Threads 保持未归档和持久化。

如果只创建一条、握手失败、首轮没有 proof、独立标签页创建失败或同账号 mutation writer 不明确，不得声称运营已启动，也不得进行 TikTok 写操作。

## 运营规则摘要

### 垂直校准

- 默认采用 search-heavy：三个批准搜索簇，每簇按顺序观察五条，再回到一次连续 For You checkpoint。
- For You 位置 1 后优先使用页面可见的 native next/down 控件逐条前进；不能用 reload、Home reset 或重新打开页面制造新样本。
- 每条内容标记 `core`、`adjacent`、`irrelevant` 或 `harmful_to_direction`；商品、旧内容和漂移内容都计入分母。
- 定期比较搜索结果与 For You 的 core/directional/drift shares，再调整搜索簇。

### 稳定性断路器

- 持久化只依靠两个用户可见 Threads 与 callback；禁止 `create_goal`、`update_goal`、subagent、agent tree 和自建 replacement worker。
- Executor 每个 turn 只执行一个有边界 block，完成后释放 Chrome、callback、idle。多轮运行由 coordinator 在上一轮完成后逐轮派发。
- 无人值守时只给 coordinator 配一个低频 heartbeat，作为漏回调与结束时间保险；executor 运行中保持静默，heartbeat 不能碰 Chrome、重建任务、绕过 blocker 或并发派发。
- 不硬编码 Chrome Skill 的版本缓存路径；只使用当前 runtime 与受支持的 Playwright locator。
- 只从 CAPTCHA、challenge、系统 dialog/banner/toast、账号 warning 等明确系统 UI 判断风险；caption、hashtag、comment 或搜索内容里的 `warning`/`verify` 字样不是平台警告。
- 一个失败类型最多允许一个窄 recovery；同类连续失败两次立即开断路器、释放 Chrome、callback 并 idle。改关键词、删 hashtag、换输入法或宣称“fresh audit”不能重置断路器。
- Native next/down 失败后不自动切 PageDown、ArrowDown、wheel、script scroll、reload 或 reset。Scroll-only fallback 必须由用户在收到 blocker 后重新明确授权。
- Native next/down 必须从位置 1 起锁定方向特定的精确签名；禁止使用 `button:not([disabled])` 一类宽 locator，因为第一次推进后 up/down 通常都会 enabled。每次 DOM 移动后重新解析同一 down 签名。
- 预期 UI gate 失败必须在当前判断分支直接写终态、释放 Chrome、callback；不能用 `throw` 返回 reasoning 后继续换 locator 诊断。
- Coordinator/executor ID、账号、ledger path、授权、角色、模型和 thinking 是 immutable registry；dispatch 必须逐字复制，executor 在连接 Chrome 前逐项比较，任何漂移都以 `registry_mismatch` 终止。
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

登录错配、CAPTCHA、验证挑战、rate limit、warning/restriction、账号变化、失去专属标签页控制、同账号 mutation writer 冲突、hard runtime change、uncertain submission 或持久化失败时，停止对应 mutation 并保留证据。用户说停止时，executor 只释放自己的标签页，写 final checkpoint，两个运营 Threads 保持 idle；只有用户明确要求时才归档。

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
tiktok-web-operations/
  SKILL.md
  manifest.json
  agents/
  references/
```

## Boundaries

只操作用户明确授权的账号和浏览器会话。不要保存凭据、cookies、Chrome profile、TikTok 导出或运营 ledger。不得批量养号、规避平台执法、刷量、垃圾互动、骚扰、歧视、冒充身份或伪造经验。发布内容还必须满足版权、披露和 AIGC 标记要求。

## 发布维护

Skill 的 `references/distribution-and-upgrades.md` 是维护协议。任何 material change 都必须递增版本、同步 README 与完整 Skill、重建本地 ZIP，并从新的 GitHub archive 反向验证。

## License

MIT
