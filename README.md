# 子智能体管家 · 经济版（开发中） / Subagent Steward · Economy (Development)

本仓库有两个同名技能变体，一次只安装一个：

- `main` / `v1.0.0`：通用版，按任务判断是否委派。
- `economy`：成本导向开发分支，尚未正式发布；原生委派条件允许时，由 Luna／Sol **默认负责**实质性常规执行。节省效果与交付质量变化尚未测量，也无保证。

先通过分支提交持续开发和实际试用，不为每次修改创建 Release。早期经济版 Release 已转为草稿，标签和代码历史保留；达到预期后再考虑以 `economy-v1.0.0` 等独立标签发布。此次整理不修改调度策略。

这是社区 Codex skill，不是 OpenAI 官方项目或独立调度服务。

## 经济版怎么分工

- Astra 保留与你沟通、需求澄清、关键产品或架构决策、针对性验收和交付；通常只做准确交办所需的调查，需要时可深入调查，不需要手动切换主模型。
- 原生工具条件允许时，Luna／Sol 默认完整承担有界调查、约定范围内的技术设计、实现、有意义的测试、局部修复和技术跟进。Astra 不常规地预先解题、重复广泛调查、并行实现相同范围或接管局部修复；同一负责人优先处理后续问题。
- 沿用默认版的灵活选择：两者都适合时偏好 Luna；Luna/high、Sol/medium 是参考起点，xhigh/max 可按需直接选，Sol 不需要额外举证或先让 Luna 失败。
- Astra 可以直接调用任一模型；有实际收益且运行时支持时，执行者也可继续委派独立部分，并负责整合和验证。没有必经的 Sol 中间层或技能自设的并发、深度上限。
- 小任务可以直接完成。Astra 检查实际产物和证据，遇到歧义、风险或疑点可随时深入调查、重复检查或亲自接管；独立复核按风险使用，不是每项工作必备。不设 token 占比或工作量配额。

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

需要原生子智能体工具，模型、推理强度、并发和嵌套能力以实时工具为准。若工具要求父智能体同时有独立的有用工作，经济版也遵守；不会为了委派制造工作或绕过限制。因此它不能保证 Astra 只沟通、不执行。

默认子模型为 `gpt-6-luna` / `gpt-6-sol`；不可用时可使用工具明确支持的对应 5.6 模型，或由主智能体处理，并说明有影响的回退。无需额外 API key 或插件。安装技能本身不修改主模型、`config.toml` 或全局 `AGENTS.md`；可选片段另行合并。

这套规则不自动读取账单或学习历史消耗。试用时应比较相近任务的主智能体绝对消耗、总费用、返工和交付质量；API 单价比例不等于 Codex 套餐额度比例。官方模型依据及本项目策略的区分见 [SKILL.md](skills/subagent-steward/SKILL.md)。

## English overview

The default stable edition is `main` / `v1.0.0`. The `economy` branch is under development and real-task evaluation, with no current public release. Capable Luna/Sol workers own substantial routine execution when native delegation conditions allow. Savings and quality effects remain unmeasured. Earlier economy releases are drafts; their tags and history remain available. Routine edits stay on the branch; a future independent release may use `economy-v1.0.0`. This publishing cleanup does not change the delegation policy. Install only one variant at a time.

Keep Astra as the lead for scope, key product or architecture decisions, targeted acceptance, communication, and delivery. Workers own coherent discovery, technical design within agreed scope, implementation, meaningful testing, local repair, and technical follow-ups. The lead does the discovery needed for accurate dispatch, inspects real artifacts and evidence, and can investigate or take over whenever useful. Model and effort selection stays flexible, with Luna favored when both fit. Independent review is driven by material risk. Useful nested delegation respects native tool conditions, including genuine concurrent parent work where required; there is no fixed hierarchy or token quota.

Ask Codex: "Use skill-installer to install skills/subagent-steward from https://github.com/GengsengGhou/subagent-steward with ref economy. Back up existing customizations before replacing the installed variant, and update its optional marked AGENTS block if present."

To try the development edition, use the [`economy` branch skill directory](https://github.com/GengsengGhou/subagent-steward/tree/economy/skills/subagent-steward) or its [branch ZIP](https://github.com/GengsengGhou/subagent-steward/archive/refs/heads/economy.zip). For reproducible trials, record and install a full commit SHA instead of a moving branch. Back up personal customizations before replacing the skill folder and optional marked AGENTS block. Preserve other instructions. To return to the default edition, explicitly install ref `v1.0.0` and its corresponding optional AGENTS snippet.

Invoke the skill with `$subagent-steward`. Automatic invocation remains enabled but is not guaranteed for every task. For consistent use, merge the optional [AGENTS snippet](examples/AGENTS.snippet.md) into your project or personal instructions.

## License

[MIT](LICENSE).
