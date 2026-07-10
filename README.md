# TikTok Web Operations

这是 `tiktok-web-operations` Codex Skill 的公开分发仓库。仓库顶层只保留本 README 和 `tiktok-web-operations/` Skill 目录。

Protocol version: `2026.07.10.6`

## 给用户的两句启动 Prompt

```text
请打开 https://github.com/lishehao/tiktok-web-operations，完整读取根目录 README.md，并按机器协议安装或升级 Skill、只读检查 Chrome/TikTok/thread 依赖，然后创建两个持久化用户 Threads——“TikTok 运营主任务”和“TikTok Chrome执行任务”——两者都强制使用 gpt-5.6-luna + high；完成双向回调握手后直接开始运营并归档当前 bootstrap 任务，绝不使用 subagent。
默认方向为北美 college/dorm life，并授权在 strong core 视频上选择性点赞、收藏或发布简短玩梗顶层评论；点赞与收藏必须各自在不同视频上先通过一次刷新及账号级持久化 gate，评论优先 2–12 个英文词且绝不超过 30 个词，其他外部动作均未授权。
```

下面内容是执行任务必须完整读取一次的机器协议。用户不需要复制其余章节。

## 固定分发信息

- Repository: `https://github.com/lishehao/tiktok-web-operations`
- Archive: `https://codeload.github.com/lishehao/tiktok-web-operations/zip/refs/heads/main`
- Skill path: `tiktok-web-operations/`
- Install path: `${CODEX_HOME:-$HOME/.codex}/skills/tiktok-web-operations`
- Version source: `tiktok-web-operations/manifest.json`

完整读取本 README 后直接执行。不要递归寻找其他安装文档，不要先复述技术步骤，不要使用 Git、GitHub CLI、GitHub Token 或随附 ZIP。消费者只需通过 HTTPS 下载公开 archive。

## 第一阶段：安装与只读预检

第一阶段不得进行任何 TikTok 互动，也不得创建运营 Thread。

### 安装或升级

1. 下载 archive 到临时目录，安全解压，并确认快照中只有一个目标 Skill 目录。
2. 读取 incoming `manifest.json`，在写入安装目录前校验完整 Skill。有 `quick_validate.py` 时运行；没有 Python/校验器时检查 archive 完整性、目录唯一性、有效 frontmatter、manifest、`agents/openai.yaml`、references 和 SKILL 直接引用。
3. 按数字段比较 `YYYY.MM.DD.N`：
   - 未安装：`INSTALLED`。
   - 同名安装无 manifest：视为 legacy，完整备份后升级。
   - Incoming 更新：完整备份旧目录，再原子替换整个目录。
   - 同版本同内容：`NOOP`。
   - 同版本不同内容：`BLOCKED_CONFLICT`。
   - Incoming 更旧：`BLOCKED_DOWNGRADE`，除非用户明确要求降级。
4. 替换后重新校验；失败恢复备份并返回 `ROLLED_BACK`。

不逐文件合并，也不把旧版未知文件混入新版本。

### Chrome 与 TikTok

1. 必须存在 Chrome control，并能读取用户现有 Chrome 标签页；掉线最多重连两次。
2. 只能通过 Chrome control 打开或复用 TikTok，读取准确 `@handle`。Computer Use、内置 Browser、Playwright、终端浏览器和 Web Search 不能替代。
3. 检查错号、CAPTCHA、验证挑战、限流、warning 和 restriction。
4. 不输入密码、OTP、passkey、验证码或恢复码。
5. 建立可写的共享 ledger 路径，并初始化每个 mutation lane 的独立状态。预检不能通过点击来测试能力。
6. 完成后释放 bootstrap 对 Chrome 的控制；后续只有执行 Thread 能碰 Chrome。

### Thread 与模型硬依赖

必须证明下面工具真实存在：

- `list_projects`
- `create_thread`
- `read_thread`
- `send_message_to_thread`
- `set_thread_title`
- `set_thread_archived`

`set_thread_pinned` 与 `navigate_to_codex_page` 是可选展示能力。

必须证明 `create_thread` 和 `send_message_to_thread` 接受：

```text
model: gpt-5.6-luna
thinking: high
```

这是用户明确指定的硬要求。任一运营 Thread 不能使用该组合时停止，不替换为其他模型或 effort，也不降级成单 Thread 或 subagent。

内部保留：

```text
install_action: INSTALLED | UPGRADED | NOOP | BLOCKED_CONFLICT | BLOCKED_DOWNGRADE | ROLLED_BACK
skill_version: old | incoming | active
skill_validation: PASSED | FAILED
chrome_control: AVAILABLE | RECONNECTED | UNAVAILABLE
tiktok_session: LOGGED_IN:@handle | LOGGED_OUT | UNVERIFIED
account_warning: NONE_VISIBLE | PRESENT | UNVERIFIED
thread_support: CREATE_READ_SEND_TITLE_ARCHIVE | UNAVAILABLE
model_runtime: coordinator=gpt-5.6-luna/high | executor=gpt-5.6-luna/high | UNAVAILABLE
ledger_path:
dependency_status: READY | BLOCKED
required_missing: []
repair_actions: []
```

阻塞时只返回第一项可修复问题、影响和 `完成后回复“继续”`。不要列出成功项。

## 第二阶段：创建两个持久化运营 Threads

Bootstrap 任务只是安装器，不属于最终运营拓扑。依赖健康后按顺序执行：

1. 调用 `list_projects`。当前 saved project 明确可用时，两条 Thread 使用同一 local project target；否则两条都使用 projectless local target。
2. 创建 `coordination_thread`：
   - `create_thread(model="gpt-5.6-luna", thinking="high")`
   - 标题设为 `TikTok 运营主任务`
   - 初始 Prompt 要求读取 `$tiktok-web-operations`，声明只负责用户对话、方向、授权、executor 管理与风险，等待 executor registry，绝不碰 Chrome。
3. 记录 coordinator Thread ID；可用时 pin。
4. 创建 `execution_thread`：
   - `create_thread(model="gpt-5.6-luna", thinking="high")`
   - 标题设为 `TikTok Chrome执行任务`
   - 初始 Prompt 包含准确 coordinator Thread ID、Skill、唯一 Chrome 所有权、ledger、默认 envelope 和 callback schema；同时要求等待 `SELF_REGISTRY`，不得猜测自己的 Thread ID、不得提前发送 `THREAD_READY`、不得触碰 Chrome。
5. 记录 executor Thread ID；可用时 pin。
6. 用 `send_message_to_thread(model="gpt-5.6-luna", thinking="high")` 向刚返回的 executor ID 发送 `SELF_REGISTRY`，包含准确 executor ID、coordinator ID、账号、ledger 与唯一 Chrome owner 身份。Executor 只能逐字回显这组已提供 ID，再向 coordinator 发送 `THREAD_READY`。
7. 用同样的 Luna/High 参数把 executor ID 与完整运营 envelope 发给 coordinator。
8. 读取两条 Thread 最新 turns，验证双向注册：coordinator 知道准确 executor ID；executor 从 `SELF_REGISTRY` 获得自己的准确 ID；coordinator 已收到 executor 通过 `send_message_to_thread` 发来的 `THREAD_READY`。Callback 的 `source_thread_id` 与 bootstrap registry 是身份权威，payload 冲突时停止派发并修正。
9. Coordinator 用 Luna/High 向该 executor ID 派发第一个 `search_heavy` block。
10. 确认 executor 收到；可用时把 Codex UI 导航到 coordinator；然后归档当前 bootstrap 任务。

如果只创建出一条或握手失败，不得开始 TikTok 操作。只归档本次 bootstrap 创建且尚未执行任何外部动作的空 Thread，并报告阻塞。

最终运营面严格只有：

```text
TikTok 运营主任务       gpt-5.6-luna / high
TikTok Chrome执行任务  gpt-5.6-luna / high
```

两者都是持久化、用户可见、可在侧边栏独立打开的 Codex Threads，不是 subagent。

## Thread-to-Thread 运行协议

### 运营主任务

1. 只与用户沟通并维护方向、授权、能力矩阵、pending decisions 和 executor registry。
2. 收到 executor callback 后，必要时只读最新 1–3 turns。
3. 决定下一有边界 block；不需要用户决策时，用 `send_message_to_thread` 向同一 executor ID 派发，显式指定 Luna/High。
4. 标记 executor 为 `running_current_task` 后结束 turn，不轮询、不 busy-wait、不碰 Chrome。
5. 由下一次 executor callback 唤醒并继续。

### Chrome 执行任务

1. 只接受已注册 coordinator ID 的消息。
2. 独占 Chrome/TikTok，执行一个有边界 block 或一个精确授权动作。
3. 写入 sole-writer ledger，完成即时/刷新/账号级验证。
4. 完成或阻塞时释放 Chrome control。
5. 用 `send_message_to_thread(model="gpt-5.6-luna", thinking="high")` 把结构化结果发给 coordinator，然后 idle。
6. 不自行开始下一轮、不创建 Thread、不使用 subagent、不回调 Skill 开发或 bootstrap 任务。

普通顺序依赖 soft-hook callback，不持续轮询。只有用户明确要求定时唤醒、callback 不可靠或任务确实依赖未来时刻时才使用 heartbeat。

## 第一轮垂直校准

立即从 `search_heavy` 开始：

1. 选择三个不同的批准搜索簇。
2. 每簇按顺序观察五条结果，合计十五条；商品、陈旧、adjacent 和 irrelevant 都计入分母。
3. 记录 query、URL、creator、freshness、relevance、setup/payoff 和评论区文化。
4. 完成全部搜索后只进入一次 For You，把它当作同一条连续自然流；位置 1 之后只能使用页面上可见的 next/down 控件或一次增量滚动前进。
5. 每次前进记录准确的 before/after creator、URL 或稳定卡片身份。禁止中途 reload、重新打开 Home、`goto` 首页、离开页面后重进；不能前进、重复或身份丢失时记录 `transition_failure`/`duplicate` 并停止，绝不重置页面补样本。
6. 每个五条搜索簇结束后，以及 For You 的 1、5、10、15、20（或提前停止的最终位置）增量写入 ledger。
7. 计算 core/directional/drift shares，并按 Skill 的 `persistent-feed-operations.md` 选择下一模式。
8. Executor callback 完整 block；coordinator 再派下一轮。

## 默认方向

- Roommate move-in、storytime、roommate chaos。
- Dorm/freshman move-in、dorm setup。
- College day in my life、campus routine、GRWM for class。
- Campus friend group、game day、tailgate。
- Finals survival、dorm bathroom/cooking/laundry failures。

排除 admissions、SAT/GPA、申请建议、纯学习鸡血和无校园生活语境的泛内容。

## 点赞、收藏与自动评论授权

用户发送顶部两句 Prompt 时，明确激活三个彼此独立的 lane：post like、favorite/save、proactive top-level comment。

- 三个 lane 都只用于 strong `core` 视频。
- 点赞和收藏分别选择不同视频做一次 one-action persistence gate：只点击一次，检查即时状态、刷新/重开状态，以及 TikTok 可提供的账号级证据。
- Gate 通过后才允许该 lane 后续选择性使用；失败或证据不足只停用该 lane，不推断另外两个 lane 失败。
- 不在同一个视频机械堆叠 like + favorite + comment；根据真实内容选择最小的合适信号。
- 历史 `@shehaolili` post-like 失败和 favorite 未验证证据仍有效，除非本 Prompt 明确授权的新 gate 产生更强的持久化证据。

- 必须理解 setup/payoff，且评论区支持轻松玩梗。
- 使用视频语言；英文优先 2–12 个词，绝不超过 30 个词。
- 可以低俗、抽象、轻度损，但不得骚扰、歧视、身体羞辱、性化未成年人、针对真人恶意羞辱或复制他人评论。
- 没有合格候选就跳过，零评论合法，不为数量硬发。
- 评论要具体、有趣、能获得自然点赞或回复；禁止索赞、钓回复、制造争议或模仿热门评论。后续评论点赞/回复只用于评价语气和受众契合，不宣称是 TikTok 账号权重公式。

没有连续可复用的评论持久化证据时，先做一次已授权 persistence gate：只提交一次，刷新或重新打开后确认准确 `@handle` 与精确文本仍可见。验证通过才启用后续自动评论。

任一 lane 第一次失败、消失或证据不足时停用该 lane，不重试。验证码、warning、限流、账号变化、hard runtime 变化或 uncertain submission 会停止所有 mutation，直到重新审计。

本 Prompt不授权评论点赞、关注、回复、`Not interested`、发视频、改 profile、分享或私信。

## 停止与生命周期

- 用户说停止时，coordinator 向 executor 发送 `STOP_AND_RELEASE`。Executor 释放 Chrome、写 final checkpoint、callback `completed`，两条 Thread 都保留为 idle、unarchived。
- 只有用户明确要求归档时才归档运营 Threads。
- Executor 消失时，先检查 Chrome 所有权与 uncertain submission；只有用户明确授权后才创建新的 Luna/High 持久化 executor 并重新握手。
- Coordinator 消失时，executor 停止 mutation、释放 Chrome 并等待，不猜测新的 callback 目标。

## 发布维护

Skill 的 `references/distribution-and-upgrades.md` 是维护协议。任何 material change 都必须递增版本、同步 README 与完整 Skill、重建本地 ZIP，并从新的 GitHub archive 反向验证。公共仓库不得包含凭据、cookies、Chrome profile、TikTok 导出、ledger 或账号私有数据。
