# 子智能体管家 · 经济版 / Subagent Steward · Economy

经济版让 Luna／Sol 在适合委派的任务中默认负责完整的常规执行，包括调查、实现、整合、测试和相关文档。Astra 负责与你沟通、关键决策和针对性验收。它适合希望减少主智能体执行工作、同时保留必要判断的用户。

这是社区 Codex skill，不是 OpenAI 官方项目或独立调度服务。两版使用相同技能名 `$subagent-steward`，一次只安装一种：

- [通用版 `v1.0.0`](https://github.com/GengsengGhou/subagent-steward/releases/tag/v1.0.0)：按任务收益判断是否委派，适合偏好灵活分工的用户。
- [经济版 `economy-v1.0.0`](https://github.com/GengsengGhou/subagent-steward/releases/tag/economy-v1.0.0)：原生工具允许时，默认将大部分常规执行交给 Luna／Sol，适合更重视控制 Astra 用量的用户。

GitHub 的默认最新版是通用版。经济版请明确指定 `economy-v1.0.0`；本 `economy` 分支的 GPT-6.1 Sol 路由更新尚未发布，固定标签 `economy-v1.0.0` 不包含该更新；指定正式标签才能安装上面介绍的正式版。分工偏好不等于预算上限，也不保证总费用或交付质量与其他版本相同。

## 经济版怎么分工

- Astra 保留与你沟通、需求澄清、关键产品或架构决策、针对性验收和交付；通常只做准确交办所需的调查，需要时可深入调查，不需要手动切换主模型。
- 按实际工具条件，Luna／Sol 默认负责完整结果：按任务需要承担授权内的环境和工具准备、调查与技术设计、实现及接口整合、测试和验收脚本的创建与执行、范围内修复、远程命令与日志跟进，并交齐相关文档、验证记录和产物引用供验收。多人分工时明确有用的执行或整合负责人；不强制增加管理层。项目明确要求主智能体亲自整合或检查时仍遵守。
- 灵活选择模型和推理强度：两者都适合时偏好 Luna；Luna/high、Sol/medium 是参考起点，xhigh/max 可按需直接选，Sol 不需要额外举证或先让 Luna 失败。
- Astra 可以直接调用任一模型；有实际收益且运行时支持时，执行者也可继续委派独立部分，并负责整合和验证。没有必经的 Sol 中间层或技能自设的并发、深度上限。
- Astra 依据目标检查实际产物和可复现证据；验收不默认变成主智能体编写测试脚本、补接口代码或重跑全部测试。整合、测试或文档未完成时，通常交原负责人定向续做；存在实质风险、疑点或直接处理更合适时，可深入检查或接管。小任务直接完成，独立复核按风险使用，不设 token 占比或工作量配额。
- 连贯执行阶段使用适合当前阶段的原生完成通知或有界等待；没有即将完成等理由时，不先用短超时反复探测。遵守运行时和用户进度沟通要求，不许诺超出限制的长等待；非紧急反馈合并交给同一负责人，及时传达重要发现、阻塞和紧急消息。
- 完整读过、仍在上下文且适用的规则与证据可复用；输出截断、内容可能更新、压缩后丢失、需要确认新鲜度或上位指令要求时仍重读。复用旧负责人时按需补充改变的约束和职责，不假设它已知道新版，也不默认重发整套技能或替换活跃负责人。

## 安装正式版或切换

把下面这句话发给 Codex：

```text
使用 skill-installer 从 https://github.com/GengsengGhou/subagent-steward 安装 skills/subagent-steward，指定 ref 为 economy-v1.0.0。若已安装同名技能，先备份个人修改，再替换为经济版；若有本技能的 AGENTS.md 标记块，同步替换为该版本片段，保留其他指令。
```

正式版入口是 [`economy-v1.0.0` 技能目录](https://github.com/GengsengGhou/subagent-steward/tree/economy-v1.0.0/skills/subagent-steward)。也可从[发布页](https://github.com/GengsengGhou/subagent-steward/releases/tag/economy-v1.0.0)下载附件 `subagent-steward-economy-v1.0.0.zip`，把其中的 `subagent-steward` 文件夹放入 `$CODEX_HOME/skills`（未设置时通常为 `~/.codex/skills`）。自动生成的 Source code ZIP 包含完整仓库，技能位于 `skills/subagent-steward`。

安装或切换前备份个人定制。两个变体使用相同技能名和安装目录，应先替换该目录中的旧版本；若曾添加可选 AGENTS 片段，也请替换 `subagent-steward` 标记块中的内容，同时保留块外定制。回退通用版时，安装 [v1.0.0 ZIP](https://github.com/GengsengGhou/subagent-steward/archive/refs/tags/v1.0.0.zip) 中的技能目录，并按需恢复对应的 AGENTS 片段。

安装后可用 `$subagent-steward` 调用。自动选择仍开启，但不保证每个任务都会加载技能。需要在项目或个人 `AGENTS.md` 中稳定采用规则时，可合并[可选片段](examples/AGENTS.snippet.md)。

明确要试用未发布修改时，指定 [`economy` 分支](https://github.com/GengsengGhou/subagent-steward/tree/economy/skills/subagent-steward)或完整提交 SHA；分支会变化。省略 ref 可能装回默认 `main`。安装的技能将在下一轮对话可用；客户端尚未刷新时，重新打开任务后检查。

## 运行边界

需要原生子智能体工具，模型、推理强度、并发和嵌套能力以实时工具为准。只有工具实际要求时，父智能体才必须同时有独立的有用工作；没有这一要求时，可以等待负责人完成，不制造并行工作。嵌套同样依据实际条件。容量满时先复用合适的现有执行者或排队等待，不默认把全部执行转回 Astra；紧急、阻塞或直接处理更合适时仍可亲自执行，不终止活跃任务来腾出名额。因此它不能保证 Astra 只沟通、不执行。

本分支优先子模型为 `gpt-6-luna` / `gpt-6.1-sol`。Luna 回退为 `gpt-5.6-luna`；Sol 依次回退为 `gpt-6-sol`、`gpt-5.6-sol`，且只选实时工具明确支持的模型和推理强度。无法委派时由主智能体处理，并说明有影响的回退；不因新型号替换合适的活跃负责人。无需额外 API key 或插件。安装技能本身不修改主模型、`config.toml` 或全局 `AGENTS.md`；可选片段另行合并。

这套规则不自动读取账单或学习消耗。评估时应比较相近任务的主智能体绝对消耗、总费用、返工和交付质量；API 单价比例不等于 Codex 套餐额度比例。2026-10-01 核对的 [Codex 模型指南](https://developers.openai.com/codex/models) 建议复杂编程和智能体工作流在可用时选择 [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)，Luna 用于范围集中、可重复的任务。6.1 Sol 推理强度从客户端默认开始；Luna 建议 High。本技能的 Sol/medium 是实用参考起点，API 默认值不代表原生工具默认，跨代 effort 不能直接等同。官方模型依据及本项目策略的区分见 [SKILL.md](skills/subagent-steward/SKILL.md)。

## English overview

The [default edition `v1.0.0`](https://github.com/GengsengGhou/subagent-steward/releases/tag/v1.0.0) delegates when the task warrants it. The [economy edition `economy-v1.0.0`](https://github.com/GengsengGhou/subagent-steward/releases/tag/economy-v1.0.0) defaults to giving capable Luna/Sol workers substantial routine execution under an Astra lead. Choose the default edition for flexible delegation or the economy edition when reducing Astra execution is a stronger priority. Both use the same skill name, so install only one at a time. GitHub's Latest release is the default edition; pin `economy-v1.0.0` to install the stable economy edition. This `economy` branch contains unpublished GPT-6.1 Sol routing changes; the fixed `economy-v1.0.0` tag does not include them. No savings or quality outcome is guaranteed.

Keep Astra as the lead for scope, key scientific, product or architecture decisions, permissions, targeted acceptance, communication, and delivery. Workers own complete outcomes, including task-relevant authorized setup, implementation through interface integration, test and acceptance-harness creation and execution, in-scope repair, remote command and log monitoring, related docs, verification records, and artifact references ready for acceptance. With multiple workers, name a useful execution or integration owner; no manager layer is required. Respect project rules that reserve integration or checks for the lead.

Acceptance reviews actual artifacts and reproducible evidence. Ordinarily return unfinished delivery to the same owner rather than rebuilding harnesses, patching glue, or repeating all tests, while retaining direct intervention for material uncertainty, risk, or practical need. Use stage-appropriate native waits within runtime and user-update rules; avoid unjustified short probes, combine nonurgent feedback, and relay meaningful findings or urgent messages. Reuse fully read, still-available relevant rules and evidence, rereading for truncation, possible changes, lost context, required freshness, or higher-priority instructions. Pass relevant changed constraints or responsibilities when reusing older workers without routinely resending the full skill or replacing active owners. Concurrent independent parent work is required only when the live tool actually says so, including for nesting. At full capacity, first reuse a suitable worker or queue work without terminating active tasks. This branch prefers `gpt-6-luna` and `gpt-6.1-sol`. Sol falls back to `gpt-6-sol`, then `gpt-5.6-sol`; Luna falls back to `gpt-5.6-luna`, only with live-tool-supported efforts. Retain suitable active owners. Codex recommends the client default for 6.1 Sol and High for Luna; Sol/medium is this skill's practical starting point, not a native-tool default. Model and effort selection stays flexible, with Luna favored when both fit; no fixed hierarchy, quota, or savings guarantee applies.

Ask Codex: "Use skill-installer to install skills/subagent-steward from https://github.com/GengsengGhou/subagent-steward with ref economy-v1.0.0. Back up existing customizations before replacing the installed variant, and update its optional marked AGENTS block if present."

Install the [`economy-v1.0.0` skill directory](https://github.com/GengsengGhou/subagent-steward/tree/economy-v1.0.0/skills/subagent-steward) or the tag-exact skill ZIP attached to its [release](https://github.com/GengsengGhou/subagent-steward/releases/tag/economy-v1.0.0). Explicitly choose the [`economy` branch](https://github.com/GengsengGhou/subagent-steward/tree/economy/skills/subagent-steward) or a full commit SHA only to try subsequent development. Back up personal customizations before replacing the skill folder and optional marked AGENTS block. Preserve other instructions. To return to the default edition, explicitly install ref `v1.0.0` and its corresponding optional AGENTS snippet.

Invoke the skill with `$subagent-steward`. Automatic invocation remains enabled but is not guaranteed for every task. For consistent use, merge the optional [AGENTS snippet](examples/AGENTS.snippet.md) into your project or personal instructions.

## License

[MIT](LICENSE).
