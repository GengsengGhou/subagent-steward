# 子智能体管家 · Subagent Steward

让 Codex 按任务需要决定是否委派，灵活选择 Luna、Sol 和推理强度；两者都适合时，考虑成本优先 Luna。为偏好 Astra 主导、控制执行成本的用户设计，也尊重你选择的其他主模型。

这是一个社区 Codex skill，不是 OpenAI 官方项目。它提供调度指导，不是独立调度服务，也不提供硬预算限制或节省费用的保证。

## 怎么分工

| 场景 | 选择参考 |
| --- | --- |
| 与用户沟通、需求澄清、总体判断、验收与交付 | 保留当前主智能体及其推理强度 |
| 范围集中的实现、调查、测试或研究，包括局部技术判断和多个模块 | 通常适合 GPT-6 Luna / high |
| 目标明确，但逻辑链长、约束相互影响或边界复杂 | Luna / xhigh 或 max 都可直接选择 |
| 需要不断调整调查方向、比较方案或综合判断的工作 | 通常适合 Sol / medium 或 high |
| 简单机械任务 | 可以降低 Luna 推理强度 |
| 任一模型需要深入推演或检查 | 按需选择 xhigh 或 max，无额外举证门槛 |

小任务直接完成。可独立推进的子任务才委派，数量由收益、依赖、编辑冲突和运行时容量决定，没有技能自设的固定并发上限。子智能体默认不继续派生。Terra 和 Astra 不进入常规子模型路线。

上表是判断参考，不是严格的准入条件。主智能体根据范围、不确定性、推理深度、验收难度、预期指挥成本和时间作合理选择。觉得 Sol 更适合就可以直接使用，无需先证明 Luna 不行，也不必先积累失败记录或成本数据。

high、xhigh、max 不是必须逐级尝试的阶梯。需要深度思考时，Luna Max 是正常选项，不因它是最高档就优先退到 xhigh；简单或追求快速响应时也可以降低强度。Sol 的推理档位同样灵活选择，任何一方都不需要额外举证或选择报告。

两者看起来都适合、没有明显实际差异时，考虑成本优先 Luna。评估总成本时包含主智能体验收、返工和交接，不要求 Astra 为了让 Luna 胜任而预先解完任务或逐步指挥。出现问题后，可按情况澄清、纠正、调整强度或换模型，不规定先重试几次。此策略不保证某个组合在所有任务上都最省钱。

## 安装

把下面这句话发给 Codex：

```text
使用 skill-installer 从 https://github.com/GengsengGhou/subagent-steward 安装 skills/subagent-steward 技能。
```

也可直接提供 [技能目录链接](https://github.com/GengsengGhou/subagent-steward/tree/main/skills/subagent-steward)。该路径包含完整的 `SKILL.md` 和 `agents/openai.yaml`。标准 skill-installer 会安装到 `$CODEX_HOME/skills/subagent-steward`；未设置 `CODEX_HOME` 时通常是 `~/.codex/skills/subagent-steward`。若同名技能已存在，先确认是否有个人修改，再决定更新，避免直接覆盖。

也可以下载仓库 ZIP，把其中的 `skills/subagent-steward` 整个文件夹复制到上述技能目录。安装后在下一轮对话中检查是否识别到技能；若客户端尚未刷新，重新打开任务后再试。

### 使用

```text
使用 $subagent-steward 完成这个任务：实现 CSV 导入，并补充错误处理和测试。
```

技能允许自动选择，但并不保证每个任务都会自动加载，也不会要求每个任务都开启子智能体。希望在复杂任务中稳定考虑这套规则，可以参考 [可选 AGENTS.md 片段](examples/AGENTS.snippet.md)，让 Codex 将它合并到你的项目或个人 `AGENTS.md`，保留已有规则。片段没有本机绝对路径。

## 运行要求与边界

- Codex 运行环境必须提供原生子智能体工具。具体可用模型和推理强度以该工具为准，主模型选择器或 API 模型列表不能代替检查。
- 默认使用 `gpt-6-luna` / `gpt-6-sol`。如果运行时不支持，可以选择它明确支持的对应 5.6 模型，或由主智能体直接完成，并说明有影响的回退。
- 派发时显式指定模型和推理强度，并传递精简、完整的任务说明，避免意外继承 Astra 或整段聊天历史。不同客户端的工具参数可能不同，以实时工具契约为准。
- 不需要额外 API key、Python、Conda 或 codebase-memory 插件。项目若已有专门的代码发现规则，仍遵守那些规则。
- 安装技能不会修改主模型、`config.toml` 或全局 `AGENTS.md`。可选的自动调用片段需要另行合并。
- 这套规则不会自动读取账单或从历史消耗中学习。评估效果需要看主智能体与子智能体的总消耗、返工和最终质量。API 单价比例不等于 Codex 套餐额度比例。

## 官方依据与本项目策略

2026-09-23 核对的 [OpenAI Codex 模型指南](https://developers.openai.com/codex/models) 建议从 **Luna High、Sol Medium** 开始。[GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) 面向范围集中、大批量的任务；[GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) 面向复杂编程和智能体工作流。

官方的起始推理档位建议不等于模型分配规则。这里的灵活分工、两者都适合时优先 Luna 和失败处理，是本项目的成本导向策略，并非官方性能或成本保证。官方对 Astra 的起始档位建议不会覆盖你已经选择的主智能体强度。

## 更新与移除

更新前保留本地定制，再安装或复制新版本。移除时删除安装目录中的 `subagent-steward` 文件夹，并移除自己添加的可选 AGENTS.md 片段。无需调整主模型配置。

## English overview

Subagent Steward is a community Codex skill for cost-aware delegation under an Astra lead. It preserves the user's primary model and effort and uses **GPT-6 Luna / high** and **GPT-6 Sol / medium** as flexible starting points. Choose model and effort using task scope, uncertainty, reasoning depth, likely supervision, time, and total cost. Favor Luna when both fit, but freely select Sol or Max without a proof requirement, prior failed attempt, or mandatory effort ladder. The skill imposes no fixed worker-count cap beyond runtime capacity. Actual savings remain unmeasured.

To install, ask Codex: "Use skill-installer to install skills/subagent-steward from https://github.com/GengsengGhou/subagent-steward." Invoke it with `$subagent-steward`. For optional recurring use, merge the portable [AGENTS.md snippet](examples/AGENTS.snippet.md) into your own instructions. No extra API key or plugin is required; native subagent tooling and supported models are required for delegation. Actual savings are unmeasured.

## License

[MIT](LICENSE).
