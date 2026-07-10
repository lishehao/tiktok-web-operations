# TikTok Web Operations

这是 `tiktok-web-operations` Codex Skill 的公开分发仓库。仓库只保留两个顶层入口：本 README 和 `tiktok-web-operations/` Skill 目录。

Protocol version: `2026.07.10.3`

## 给用户的两句启动 Prompt

```text
请打开 https://github.com/lishehao/tiktok-web-operations，完整读取根目录 README.md，并按照其中的机器执行协议从该仓库安装或升级 tiktok-web-operations Skill；先完成 Chrome、TikTok 登录和子智能体协作能力预检，通过后立即启动“主协调器 + 唯一 Chrome 子任务”持续运营。
默认方向为北美 college/dorm life，并授权只在 strong core 视频下自动发布简短玩梗顶层评论（优先 2–12 个英文词、绝不超过 30 个词）；点赞、收藏、关注、回复、Not interested、发视频和其他外部动作均未授权。
```

下面全部内容是给执行任务读取的机器协议。用户不需要复制其余章节。

## 机器执行协议

完整读取一次本 README 后直接执行，不要递归寻找其他安装文档，不要先向用户复述技术步骤，也不要把运行结果回调给 Skill 开发任务。

### 固定分发信息

- Repository: `https://github.com/lishehao/tiktok-web-operations`
- Archive: `https://codeload.github.com/lishehao/tiktok-web-operations/zip/refs/heads/main`
- Skill path: `tiktok-web-operations/`
- Install path: `${CODEX_HOME:-$HOME/.codex}/skills/tiktok-web-operations`
- Version source: `tiktok-web-operations/manifest.json`

消费者不需要 Git、GitHub CLI、GitHub 账号、Token 或随附 ZIP。通过 HTTPS 把公开 archive 下载到临时目录，安全解压，并确认快照中只有一个目标 Skill 目录。

## 第一阶段：安装与只读预检

第一阶段不得调用运营流程，也不得进行任何 TikTok 互动。

### 安装或升级

1. 读取 incoming `manifest.json`，并在写入安装目录前校验完整 incoming Skill。
2. 有可用 `quick_validate.py` 时运行它。Python 是可选依赖；没有校验器时执行等价检查：archive 可完整解压、目标目录唯一、`SKILL.md` 有有效 `name`/`description` frontmatter、manifest 可读、`agents/openai.yaml` 和所有 references 可读、SKILL 直接引用的文件均存在。
3. 按数字段比较 `YYYY.MM.DD.N` 版本：
   - 未安装：`INSTALLED`。
   - 同名安装没有 manifest：视为 legacy，先完整备份再升级。
   - GitHub 版本更高：完整备份旧目录，再以同文件系统临时目录原子替换。
   - 版本相同且内容相同：`NOOP`。
   - 版本相同但内容不同：`BLOCKED_CONFLICT`，保留旧安装。
   - GitHub 版本更低：`BLOCKED_DOWNGRADE`，除非用户明确要求降级，否则不覆盖。
4. 替换后重新校验；失败立即恢复备份并返回 `ROLLED_BACK`。

升级必须替换整个受管 Skill 目录，不逐文件合并，也不把旧版未知文件混入新版。

### 运行依赖检查

读取已安装 Skill 的 `references/startup-health-check.md` 并依次证明：

1. Chrome control 存在并能读取用户已有 Chrome 标签页；控制连接掉线最多重连两次。
2. 只能通过 Chrome control 打开或复用 TikTok，并读取准确登录 `@handle`。Computer Use、内置 Browser、Playwright、终端浏览器和 Web Search 都不能替代。
3. 当前页面没有阻断运营的错号、CAPTCHA、验证挑战、限流、warning 或 restriction。
4. 当前任务具备 spawn、复用、消息、检查和 interrupt 一个 subordinate agent 的 collaboration 能力；第二个用户自建 Codex 任务不能代替子智能体。
5. 需要时能读取当地时间、时区和 UTC offset，并能创建可写 driver ledger。
6. 每种 mutation lane 都有独立状态。预检本身完全只读，不通过点击测试能力。

模型选择是可选项。运行时真实暴露模型/effort 选择时，主协调器请求当前最强可用模型，Chrome driver 请求 `Luna + Extra High`；接口没有模型选择时继承实际 runtime 并继续，不得声称已经成功切换。

保留内部报告，不在健康状态下向用户展开：

```text
install_action: INSTALLED | UPGRADED | NOOP | BLOCKED_CONFLICT | BLOCKED_DOWNGRADE | ROLLED_BACK
skill_version: old | incoming | active
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

阻塞时只返回第一项用户可以处理的问题、影响和 `完成后回复“继续”`，不要列出已通过项，也不要生成 Chrome driver。

- Chrome 不可用：要求用户打开 Chrome，安装或启用 ChatGPT Chrome Extension，并保持 Chrome 运行。
- TikTok 未登录：保留 TikTok 页面，要求用户手动登录和完成页面验证；不要索取密码或验证码。
- Collaboration 不可用：说明要求的主任务 + 子任务架构无法启动，TikTok 未发生任何互动；要求换到支持子智能体的 Codex 任务。

## 第二阶段：直接启动运营

当 `dependency_status=READY` 时立即调用 `$tiktok-web-operations`，不再询问技术确认：

1. 把当前用户任务设为唯一 `main_coordinator`，由它拥有用户对话、持续目标、策略、授权、风险和最终汇报。
2. 在当前 collaboration tree 内 spawn 恰好一个 subordinate `chrome_driver`。不得创建第二个用户自建任务，不得传入外部 callback Thread ID，也不得允许 child spawn 后代。
3. 把全部 Chrome/TikTok 导航与 mutation 所有权交给 child；child 存在时 parent 不得触碰 Chrome。
4. 立即派发第一个 `search_heavy` block：三个不同的批准搜索簇，每簇按顺序观察五个结果，然后回到 For You 使用原生连续滑动观察二十条。
5. Child 是 ledger 唯一写入者；每个 block 完成后向 parent 返回 Skill 定义的结构化结果并 idle。
6. Parent 评估垂直度后用 `followup_task` 复用同一个 child，不得每轮新建 agent。
7. 持续目标只属于 parent；child 每次只执行一个有边界 block。用户说停止时，parent interrupt child、确认释放 Chrome、写最终 ledger checkpoint，并结束持续目标。

依赖健康后只简短返回：

`状态健康。当前账号：@handle。已启动：主协调器 + 唯一 Chrome 子任务，第一轮定向校准正在进行。`

之后继续在 collaboration tree 内监督，不向其他 Codex 任务发送 routine callback。

## 默认垂直方向

目标是让账号保持北美大学生 / dorm-life 语境：

- roommate move-in、roommate storytime、roommate chaos。
- dorm move-in、freshman move-in day、dorm setup。
- college day in my life、campus routine、GRWM for class。
- campus friend group、college game day、tailgate。
- finals survival、dorm bathroom/cooking/laundry failures。

排除纯 admissions、SAT/GPA、申请建议、纯学习鸡血，以及没有校园生活语境的泛娱乐内容。完整搜索、采样和模式切换规则以 Skill references 为准。

## 本 Prompt 的互动授权边界

用户发送 README 顶部的两句 Prompt 时，明确激活以下 standing envelope：

- 只允许在 strong `core` 视频下发布一条主动顶层评论。
- 必须理解 setup/payoff，并确认评论区文化支持轻松玩梗。
- 使用视频语言；英文优先 2–12 个词，绝对不得超过 30 个词。
- 可以低俗、抽象、轻度损，但不得骚扰、歧视、身体羞辱、性化未成年人、针对真人恶意羞辱或复制他人评论。
- 没有合格候选就跳过；零评论是合法结果，禁止为数量硬发。

如果同一账号和浏览器 runtime 没有连续可复用的评论持久化证据，先在第一个合格 core 候选上做一次已授权 persistence gate：只提交一次，然后刷新或重新打开，验证准确 `@handle` 和精确文本仍可见。验证通过后才启用后续 autonomous comments。

第一次失败、消失、不确定提交、验证码、warning、限流、账号变化或 hard runtime 变化会立即停用 comment lane，且不得重试。

本 Prompt **不授权**点赞、收藏、评论点赞、关注、回复、`Not interested`、发视频、改 profile、分享或私信。这些 lane 保持 `disabled` 或 `untested`，直到用户以后单独授权并各自完成持久化验证。

## 硬边界

- 不输入或保存凭据，不替用户处理 CAPTCHA、OTP、passkey 或恢复码。
- 不批量注册账号、不群控、不 mass-comment、不操纵互动、不规避平台执法。
- 原生滑动用于保持 feed 顺序与播放证据，不用于模拟真人或 stealth；不添加随机停顿、鼠标抖动或伪装行为。
- 点赞、收藏、评论、评论点赞、关注、回复、`Not interested`、发帖和 profile 修改是彼此独立的能力，不能互相推断。
- 点击、按钮高亮、数字动画、toast 或网络响应都不是持久化证据。

## 维护与发布

Skill 的 `references/distribution-and-upgrades.md` 是维护协议。任何 material change 必须递增版本、同步 README 与完整 Skill、重建本地最新版 ZIP，并从新的 GitHub public archive 反向下载验证。公共仓库不得包含凭据、cookies、Chrome profile、TikTok 导出、ledger 或账号私有数据。
