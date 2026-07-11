# TikTok Web Operations

这是 `tiktok-web-operations` Codex Skill 的公开分发仓库。公开仓库只保留一个安装入口和一个完整 Skill；详细运营规则以 Skill 内 references 为准。

Protocol version: `2026.07.11.4`

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

通过 HTTPS 下载并安全解压 archive。确认目标 Skill 目录唯一，并检查：

- `SKILL.md` 含有效 `name` 与 `description` frontmatter。
- `manifest.json` 的 name、version、schema 和 repository 可读。
- `agents/openai.yaml`、所有 references 及 SKILL.md 直接引用的文件存在且可读。

Git、GitHub CLI、Python、Node.js、包管理器和 API Key 都不是消费者依赖。存在 Skill validator 时可以使用；不存在时完成上述等价结构检查。

### 2. 安装与升级

按 `manifest.json` 数字段比较 `YYYY.MM.DD.N`：

- 未安装：安装完整 Skill 目录。
- 已安装但没有 manifest：视为 legacy，先完整备份再升级。
- GitHub 版本更高：备份旧目录后，用同文件系统临时目录原子替换整个受管目录。
- 版本和内容都相同：`NOOP`。
- 同版本但内容不同：停止为冲突，不静默覆盖。
- GitHub 版本更低：默认不降级。
- 替换后校验失败：恢复旧目录。

不要逐文件混合新旧版本。备份放入 `${CODEX_HOME:-$HOME/.codex}/skill-backups/`。

### 3. 只读预检

安装完成后先不修改 TikTok，也不创建运营 Threads，只检查：

1. Chrome Browser control 能实际连接；掉线时最多重连两次。
2. 通过 Chrome 只读打开或复用 TikTok，确认用户已登录并记录准确 `@handle`。不要输入、索取或保存密码、OTP、passkey、验证码或恢复码。
3. 当前页面没有阻塞性的 CAPTCHA、验证挑战、rate limit、warning、restriction 或账号错配。
4. Codex App 能创建、读取、命名、归档和跨任务发送消息；`create_thread` 与 `send_message_to_thread` 支持 `gpt-5.6-luna` + `high`。
5. 能读取真实当地时间、时区、UTC offset，并建立可写 ledger 路径。
6. 完成后释放 bootstrap 对 Chrome 的控制。

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
2. 创建 `TikTok Chrome执行任务`。它是唯一 Chrome/TikTok 执行者和 ledger writer；不得扩大授权、创建其他 Threads 或回调 bootstrap 任务。
3. 记录两条准确 Thread ID，通过 `SELF_REGISTRY` 与 `THREAD_READY` 完成双向握手；所有创建和跨任务消息都显式指定 `gpt-5.6-luna/high`。
4. 把准确账号、`direction_profile`、`operation_stop_at`、搜索簇、排除项、互动授权、能力矩阵、ledger 和停止条件交给两条任务。
5. Coordinator 向同一 executor 派发第一个 `search_heavy` 垂直校准 block。
6. 在当前启动 turn 内读取 executor 的第一个真实 proof：至少完成并记录一个请求相关的搜索/浏览微轮次，或者给出基于实际页面检查的具体无动作/阻塞证据。仅创建 Threads、握手、派发、做计划或回复“已启动”不算开始。
7. 取得 proof 后，coordinator 继续 callback 驱动的有边界 blocks，直到 `operation_stop_at`；bootstrap 任务才可归档自己。两条运营 Threads 保持未归档和持久化。

如果只创建一条、握手失败、首轮没有 proof 或 Chrome 所有权不明确，不得声称运营已启动，也不得进行 TikTok 写操作。

## 运营规则摘要

### 垂直校准

- 默认采用 search-heavy：三个批准搜索簇，每簇按顺序观察五条，再回到一次连续 For You checkpoint。
- For You 位置 1 后优先使用页面可见的 native next/down 控件逐条前进；不能用 reload、Home reset 或重新打开页面制造新样本。
- 每条内容标记 `core`、`adjacent`、`irrelevant` 或 `harmful_to_direction`；商品、旧内容和漂移内容都计入分母。
- 定期比较搜索结果与 For You 的 core/directional/drift shares，再调整搜索簇。

### 互动能力

- Post like 保持独立且默认 disabled。
- Favorite 点击一次后，必须在即时、约 +3 秒和总计 +10 秒保持 selected，之后才刷新/重开并检查账号 Favorites exact URL。
- Repost 只指实际 `Repost`/`Undo repost` 状态。允许只读打开 Share sheet 寻找明确 Repost；禁止执行 generic Share、Copy link、Send 或其他分享目标。
- 主动顶层评论必须理解视频 setup/payoff，使用视频语言，优先 2–12 个英文词，硬上限 30 个词，并逐条刷新验证。
- 不在同一视频机械堆叠 Favorite + Repost + Comment；选择最小、真实、合适的信号。没有合格候选时零互动完全合法。
- 不宣称某种互动一定增加账号权重，也不承诺推荐或曝光结果。

### 停止条件

登录错配、CAPTCHA、验证挑战、rate limit、warning/restriction、账号变化、失去 Chrome 所有权、hard runtime change、uncertain submission 或持久化失败时，停止对应 mutation 并保留证据。用户说停止时，executor 释放 Chrome，写 final checkpoint，两个运营 Threads 保持 idle；只有用户明确要求时才归档。

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
