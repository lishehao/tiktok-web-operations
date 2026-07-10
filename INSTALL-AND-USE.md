# TikTok Web Operations 固定启动 Prompt

打开一个支持 Chrome control 与子智能体协作的普通 Codex 任务，复制并发送下面整段 Prompt。不需要同时发送 ZIP。

```text
请直接执行，不要先解释安装步骤，也不要把工作回调给其他 Codex 任务。

1. 通过 HTTPS 读取并完整遵循这个 canonical machine protocol，只读取一次，不要递归抓取：
   https://raw.githubusercontent.com/lishehao/tiktok-web-operations/main/INSTALLER-PROTOCOL.md
2. 从公开 GitHub archive 安装或升级 $tiktok-web-operations。不要调用 git、git clone、git pull 或 GitHub CLI，也不要求 Python；不要使用 Computer Use、内置 Browser、Playwright 或 Web Search 替代 Chrome control。
3. 严格分两阶段连续执行：
   - 第一阶段只做 Skill、Chrome control、TikTok 登录/账号/警告、collaboration 子智能体能力、当地时间和 ledger 的依赖检查；不得进行任何 TikTok 互动。
   - 全部健康后立即进入第二阶段，不再询问技术确认：把当前任务设为唯一 main_coordinator，并由它 spawn 恰好一个 subordinate chrome_driver。主任务不碰 Chrome，子任务独占 Chrome，也不能再 spawn 后代。
4. 第二阶段立即开始第一轮 search_heavy 定向校准：3 个不同搜索簇，每簇按顺序看 5 个结果，然后回到 For You 原生连续滑动采样 20 条；同一个 chrome_driver 后续用 followup_task 复用，不得每轮新建任务，也不得把结果发回 Skill 开发任务。
5. 默认受众方向是北美大学生 / dorm life：roommate move-in/storytime、dorm move-in/setup、campus routine、friend group/game day、finals/dorm-survival chaos。排除纯 admissions、SAT/GPA、申请建议和纯学习鸡血。
6. 这条消息同时明确授权 autonomous_comment_mode：仅在 strong core 视频下发布一条主动顶层评论；必须理解 setup/payoff 与评论区文化，文案要简短、玩梗、贴语境，优先 2–12 个英文词，绝对不得超过 30 个词。可以低俗、抽象、轻度损，但不得骚扰、歧视、身体羞辱、性化未成年人、针对真人做恶意羞辱或复制别人的评论。没有合格候选就跳过，绝不能为了数量硬发。
7. 如果当前账号/浏览器运行时没有连续可复用的评论持久化证据，先在第一个合格 core 候选上做一次已授权的评论 gate：只提交一次，并在刷新/重新打开后验证 @handle 与精确文本仍可见。验证通过才启用后续自动评论；失败、消失、不确定、验证码、警告、限流、账号变化或硬 runtime 变化时立即停掉评论 lane，不得重试。
8. 本 Prompt 不授权点赞、收藏、评论点赞、关注、回复、Not interested、发视频、改 profile、分享或私信；这些 lane 保持 disabled/untested，除非我以后单独授权并各自完成持久化验证。
9. 依赖健康时只简短告诉我当前 @handle，以及“主协调器 + 唯一 Chrome 子任务”已启动，然后继续工作。若有阻塞，只告诉我第一项需要亲自完成的修复动作和影响，结尾写“完成后回复‘继续’”，不要展示内部字段、日志、agent path 或技术堆栈。
10. 这是持续运营请求：持续目标只属于 main_coordinator；chrome_driver 每次只执行一个有边界 block、回传结构化结果并 idle。用户说停止时，主任务 interrupt 子任务、确认释放 Chrome、写最终 ledger checkpoint，并结束持续目标。
```
