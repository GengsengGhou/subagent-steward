# 子智能体管家 · 经济版（开发中） / Subagent Steward · Economy (Development)

本仓库有两个同名技能变体，一次只安装一个：

- `main` / `v1.0.0`：通用版，按任务判断是否委派。
- `economy`：成本导向开发分支，尚未正式发布；原生委派条件允许时，由 Luna／Sol **默认负责**实质性常规执行。节省效果与交付质量变化尚未测量，也无保证。

先通过分支提交持续开发和实际试用，不为每次修改创建 Release。早期经济版 Release 已转为草稿，标签和代码历史保留；达到预期后再考虑以 `economy-v1.0.0` 等独立标签发布。

这是社区 Codex skill，不是 OpenAI 官方项目或独立调度服务。

## 经济版怎么分工

- Astra 保留与你沟通、需求澄清、关键产品或架构决策、针对性验收和交付；通常只做准确交办所需的调查，需要时可深入调查，不需要手动切换主模型。
- 按实际工具条件，Luna／Sol 默认负责完整结果：按任务需要承担授权内的环境和工具准备、调查与技术设计、实现及接口整合、测试和验收脚本的创建与执行、范围内修复、远程命令与日志跟进、相关文档和交付证据。多人分工时明确有用的执行或整合负责人；不强制增加管理层。项目明确要求主智能体亲自整合或检查时仍遵守。
- 沿用默认版的灵活选择：两者都适合时偏好 Luna；Luna/high、Sol/medium 是参考起点，xhigh/max 可按需直接选，Sol 不需要额外举证或先让 Luna 失败。
- Astra 可以直接调用任一模型；有实际收益且运行时支持时，执行者也可继续委派独立部分，并负责整合和验证。没有必经的 Sol 中间层或技能自设的并发、深度上限。
- Astra 依据目标检查实际产物和可复现证据；验收不默认变成主智能体编写测试脚本、补接口代码或重跑全部测试。整合、测试或文档未完成时，通常交原负责人定向续做；存在实质风险、疑点或直接处理更合适时，可深入检查或接管。小任务直接完成，独立复核按风险使用，不设 token 占比或工作量配额。
- 连贯执行阶段优先使用原生完成通知或有界等待，遵守运行时和用户进度沟通要求；不为保持忙碌反复检查、催问或循环调用工具。非紧急修正合并交办，及时传达改变决策的发现和阻塞。

## 试用开发分支或切换

把下面这句话发给 Codex：

```text
使用 skill-installer 从 https://github.com/GengsengGhou/subagent-steward 安装 skills/subagent-steward，指定 ref 为 economy。若已安装同名技能，先备份个人修改，再替换为经济版；若有本技能的 AGENTS.md 标记块，同步替换为该版本片段，保留其他指令。
```

试用入口是 [`economy` 分支技能目录](https://github.com/GengsengGhou/subagent-steward/tree/economy/skills/subagent-steward)。分支会变化；需要可复现的版本时，记录所安装的完整提交 SHA，并将其作为 ref。也可下载 [开发分支 ZIP](https://github.com/GengsengGhou/subagent-steward/archive/refs/heads/economy.zip)，把其中的 `skills/subagent-steward` 放入 `$CODEX_HOME/skills/subagent-steward`（未设置时通常为 `~/.codex/skills/subagent-steward`）。

安装或切换前备份个人定制。两个变体使用相同技能名和安装目录，应先替换该目录中的旧版本；若曾添加可选 AGENTS 片段，也请替换 `subagent-steward` 标记块中的内容，同时保留块外定制。回退通用版时，安装 [v1.0.0 ZIP](https://github.com/GengsengGhou/subagent-steward/archive/refs/tags/v1.0.0.zip) 中的技能目录，并按需恢复对应的 AGENTS 片段。

安装后可用 `$subagent-steward` 调用。自动选择仍开启，但不保证每个任务都会加载技能。需要在项目或个人 `AGENTS.md` 中稳定采用规则时，可合并[可选片段](examples/AGENTS.snippet.md)。

开发期后续更新继续明确指定 `economy` 分支或完整提交 SHA；省略 ref 可能装回默认 `main`。安装的技能将在下一轮对话可用；客户端尚未刷新时，重新打开任务后检查。

## 运行边界

需要原生子智能体工具，模型、推理强度、并发和嵌套能力以实时工具为准。只有工具实际要求时，父智能体才必须同时有独立的有用工作；没有这一要求时，可以等待负责人完成，不制造并行工作。嵌套同样依据实际条件。容量满时先复用合适的现有执行者或排队等待，不默认把全部执行转回 Astra；紧急、阻塞或直接处理更合适时仍可亲自执行，不终止活跃任务来腾出名额。因此它不能保证 Astra 只沟通、不执行。

默认子模型为 `gpt-6-luna` / `gpt-6-sol`；不可用时可使用工具明确支持的对应 5.6 模型，或由主智能体处理，并说明有影响的回退。无需额外 API key 或插件。安装技能本身不修改主模型、`config.toml` 或全局 `AGENTS.md`；可选片段另行合并。

这套规则不自动读取账单或学习历史消耗。试用时应比较相近任务的主智能体绝对消耗、总费用、返工和交付质量；API 单价比例不等于 Codex 套餐额度比例。官方模型依据及本项目策略的区分见 [SKILL.md](skills/subagent-steward/SKILL.md)。

## English overview

The default stable edition is `main` / `v1.0.0`. The `economy` branch is under development and real-task evaluation, with no current public release. Capable Luna/Sol workers own substantial routine execution when native delegation conditions allow. Savings and quality effects remain unmeasured. Earlier economy releases are drafts; their tags and history remain available. Routine edits stay on the branch; a future independent release may use `economy-v1.0.0`. Install only one variant at a time.

Keep Astra as the lead for scope, key scientific, product or architecture decisions, permissions, targeted acceptance, communication, and delivery. Workers own complete outcomes, including task-relevant authorized setup, implementation through interface integration, test and acceptance-harness creation and execution, in-scope repair, remote command and log monitoring, related docs, and delivery evidence. With multiple workers, name a useful execution or integration owner; no manager layer is required. Respect project rules that reserve integration or checks for the lead.

Acceptance reviews actual artifacts and reproducible evidence. It does not default to the lead building harnesses, patching glue, or repeating all tests. Ordinarily return unfinished integration, checks, or docs to the same owner, while retaining direct intervention for material uncertainty, risk, or practical need. Use native completion events or bounded waits and meaningful user updates instead of busy status loops. Concurrent independent parent work is required only when the live tool actually says so, including for nesting; otherwise awaiting the owner is valid. At full capacity, first reuse a suitable worker or queue work, without terminating active tasks to free slots. Model and effort selection stays flexible, with Luna favored when both fit; there is no fixed hierarchy, quota, or measured savings guarantee.

Ask Codex: "Use skill-installer to install skills/subagent-steward from https://github.com/GengsengGhou/subagent-steward with ref economy. Back up existing customizations before replacing the installed variant, and update its optional marked AGENTS block if present."

To try the development edition, use the [`economy` branch skill directory](https://github.com/GengsengGhou/subagent-steward/tree/economy/skills/subagent-steward) or its [branch ZIP](https://github.com/GengsengGhou/subagent-steward/archive/refs/heads/economy.zip). For reproducible trials, record and install a full commit SHA instead of a moving branch. Back up personal customizations before replacing the skill folder and optional marked AGENTS block. Preserve other instructions. To return to the default edition, explicitly install ref `v1.0.0` and its corresponding optional AGENTS snippet.

Invoke the skill with `$subagent-steward`. Automatic invocation remains enabled but is not guaranteed for every task. For consistent use, merge the optional [AGENTS snippet](examples/AGENTS.snippet.md) into your project or personal instructions.

## License

[MIT](LICENSE).
