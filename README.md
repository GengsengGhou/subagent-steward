# 子智能体管家 / Subagent Steward

**v3.1.0 · 统一自适应维护版**

子智能体管家根据根主智能体当前所选主模型、任务适配度和实时原生工具支持，决定直接完成或分工。执行者负责适合任务的完整结果，主智能体保留关键决策、审查实际产物和可复现证据，并完成最终交付。这是社区维护的 Codex skill，不是 OpenAI 官方项目或独立调度服务。

- [v3.1.0 正式发布页](https://github.com/GengsengGhou/subagent-steward/releases/tag/v3.1.0)
- [下载技能 ZIP](https://github.com/GengsengGhou/subagent-steward/releases/download/v3.1.0/subagent-steward-v3.1.0.zip)

技能在 Codex 中显示为 **Subagent Steward**，副标题为 **Delegate tasks to Luna, Terra, and Sol**。

## 按主模型适配分工

| 根主智能体主模型 | 常规子模型族 | 通常的分工倾向 |
| --- | --- | --- |
| Astra | Luna、Terra、Sol | 原生条件允许时，主动委派适合的常规执行；有用时可串行或并行拆分，直接完成仍可选。 |
| Sol | Luna、Terra、Sol | 可直接完成适合的完整任务；也可为成本、并行、任务适配、上下文隔离或复核而委派。 |
| Terra | Terra、Luna | 可直接完成适合的完整任务；也可在这两个模型族内分工。 |
| Luna | Luna | 可直接完成适合的工作；有益时可在同族内并行、隔离上下文或复核。 |

这些模型族边界是项目路由政策，体现用户的能力与成本选择，不是客观能力排名或硬预算。边界限制常规子模型族，不限制是否委派、任务规模、人数或并行协作。只有用户明确指示或已有明确授权时，根主智能体才扩大模型族范围；没有合适且实时工具支持的候选时，直接完成。

Luna、Terra、Sol 都可在合适且受允许时负责实现、调查、写作、检查与复核等完整结果。选择时综合任务适配、工具支持、时间和总完成成本；适配相当且其他候选没有实际优势时偏好 Luna。范围清楚本身不决定选 Luna，Terra 也适合有边界的执行和代码修复。

| 子模型 | 适用倾向 | 实用强度起点 |
| --- | --- | --- |
| `gpt-6-luna` | 集中执行、局部技术判断、边界清楚的问题求解及重复工作 | `high` |
| `gpt-6.1-terra` | 基于材料写作、视觉理解、目标明确的电脑操作及局部代码修复 | `medium` |
| `gpt-6.2-sol` | 复杂编程、不确定调查、相互依赖的交付与整合、冲突证据判断 | `medium` |

强度起点只是参考；按任务选择实时支持的强度，需要深度时可直接选择 `xhigh` 或 `max`。模型族首选及同族回退为 Luna `gpt-6-luna` → `gpt-5.6-luna`、Terra `gpt-6.1-terra` → `gpt-5.6-terra`、Sol `gpt-6.2-sol` → `gpt-6.1-sol` → `gpt-6-sol` → `gpt-5.6-sol`。不更换用户选择的主模型或主推理强度。

## 角色、授权与验收

执行者仍是执行者：按获派范围完成连贯结果，不因继承技能而成为根主智能体。只有父任务明确授予有边界的拆分权限时，执行者才可继续委派；权限不自动向后传播。交办时传递根主控允许的模型族、范围、授权、验收要求和整合责任，后代继续遵守原根的模型族边界。

执行者按任务需要负责准备、调查、设计、实现、整合、必要检查和证据；多人协作需明确整合负责人。主智能体保留用户沟通、关键决策、实际产物验收与最终交付，并审查相关实际产物和可复现证据。未完成部分通常交原负责人定向续做；按风险深入复核或直接接管。依实时工具采用完成通知或有界等待，不设固定人数、嵌套深度或 token 配额，也不要求先用较低成本模型试错。

## 当前主模型读取

只使用明确、新鲜的 **CURRENT-TURN** 主模型身份。若本轮首次需要决定委派策略但没有可用身份，按优先顺序读取：

1. 用户已指定或当前上下文已有的 Python 3.9+ 运行时，直接运行随附 Python reader。
2. Windows 使用 PowerShell 启动器，POSIX 系统使用 `sh` 启动器；启动器只查找 PATH 中的 `python3` 或 `python`，验证 Python 3.9+ 和所需标准库后调用 reader 一次。
3. 如果启动器报告 `runtime_unavailable`，且当前客户端确实提供 bundled dependency discovery 工具，可调用一次发现现有 Python 路径，再把该绝对路径传给启动器。

若仍不可用，按 Sol 的分工政策回退，不声称实际主模型是 Sol，也不改变模型或推理强度。metadata fallback 是本轮读取的最终结果，不因其再尝试其他解释器。reader 只查询当前会话的本地状态与有界日志，不扫描其他聊天、不输出正文。启动器不安装、下载、激活或改配置；本机日志格式是实现细节，不是稳定公开 API。启动器本身仍要求可用的 PowerShell/POSIX `sh` 和 Python 运行时，不提供零运行时的跨平台执行。详见[读取说明](skills/subagent-steward/references/primary-model.md)。

## 安装

### Codex skill-installer

在 Codex 中请求安装 GitHub 技能并固定使用 v3.1.0：

```text
使用 $skill-installer 从 GitHub 仓库 GengsengGhou/subagent-steward 安装 skills/subagent-steward，指定 --ref v3.1.0。
```

### 手动安装

从[正式发布页](https://github.com/GengsengGhou/subagent-steward/releases/tag/v3.1.0)下载 [v3.1.0 ZIP](https://github.com/GengsengGhou/subagent-steward/releases/download/v3.1.0/subagent-steward-v3.1.0.zip)，解压后将 ZIP 中的 `subagent-steward/` 文件夹放入 `$CODEX_HOME/skills/`；若未设置 `CODEX_HOME`，通常使用 `~/.codex/skills/`。保留完整目录结构，包括 reader、PowerShell/sh 启动器和 references。安装后下一轮即可使用 `$subagent-steward`。

从旧默认版或经济版更新前，备份个人修改，再替换同名技能目录。若个人或项目 `AGENTS.md` 有可选的 `subagent-steward` 标记块，同步换成 v3.1.0 的[可选配置片段](examples/AGENTS.snippet.md)；只替换该标记块，保留其他指令和配置。安装不会更改主模型、推理强度或其他设置。

## 参考

- [技能正文](skills/subagent-steward/SKILL.md)：模型路由、工作角色和授权规则。
- [可选 AGENTS 片段](examples/AGENTS.snippet.md)：简短调用入口。
- [模型依据](skills/subagent-steward/references/model-guidance.md)：官方说明与项目策略的区别。
- [主模型读取说明](skills/subagent-steward/references/primary-model.md)：运行时选择、入口和回退行为。

## English

Subagent Steward v3.1.0 is one unified adaptive Codex skill. It adapts work to the root lead's fresh current primary model, task fit, and live native-tool support. Workers can own complete outcomes; the lead retains key decisions, evidence-based acceptance, and final delivery. Its Codex UI name is **Subagent Steward**, with the subtitle **Delegate tasks to Luna, Terra, and Sol**. This is a community-maintained skill, not an official OpenAI project or standalone scheduler.

| Root primary | Regular child families | Usual tendency |
| --- | --- | --- |
| Astra | Luna, Terra, Sol | Proactively delegate suitable routine work when native conditions permit; split serially or in parallel when useful. Direct work remains available. |
| Sol | Luna, Terra, Sol | Complete suitable work directly or delegate for cost, parallelism, task fit, context isolation, or review. |
| Terra | Terra, Luna | Complete suitable work directly or delegate within these families. |
| Luna | Luna | Work directly or use same-family delegation for useful parallel work, context isolation, or review. |

These family limits are local policy reflecting the user's capability and cost choice, not an objective ranking or hard budget. They constrain regular child families, not delegation, task size, worker count, or parallelism. Only explicit user direction or existing authorization widens the root's family set. If no suitable live-supported candidate is available within it, work directly.

Luna, Terra, and Sol can each own complete implementation, investigation, writing, checks, or review when suitable and permitted. Choose by task and tool fit, time, total completion cost, and user preference. Favor Luna only when candidates are equally suitable and another permitted family has no practical advantage. Practical effort starting points are Luna/high, Terra/medium, and Sol/medium; they are guidance, not requirements. Use a supported effort directly, including `xhigh` or `max` when depth helps. Preferred same-family routes are Luna `gpt-6-luna` to `gpt-5.6-luna`, Terra `gpt-6.1-terra` to `gpt-5.6-terra`, and Sol `gpt-6.2-sol` to `gpt-6.1-sol`, then `gpt-6-sol` and `gpt-5.6-sol`. Never change the selected primary or its effort.

An assigned worker remains a worker and executes its assigned scope. Further delegation requires explicit bounded permission from its parent; permission does not propagate automatically. Handoffs carry the original root's allowed families, scope, authorization, acceptance needs, and integration responsibility. The lead reviews relevant artifacts and reproducible evidence; incomplete work normally returns to its original owner for targeted continuation. Native completion notifications or bounded waits follow the live tool. There are no fixed worker, nesting, or token quotas and no cheaper-model trial requirement.

Use only fresh, explicit **CURRENT-TURN** primary metadata. If a root first needs routing and no current identity is available, use a known Python 3.9+ runtime to run the bundled reader directly. Otherwise use `read_primary_model.ps1` on Windows or `read_primary_model.sh` through POSIX `sh`. These launchers search PATH for `python3` and `python`, verify Python 3.9+ and the required standard library, then invoke the reader once. They accept an explicit absolute path to an existing Python runtime, including paths with spaces. If a launcher returns `runtime_unavailable` and the current client provides bundled dependency discovery, use it once and pass the returned path to the launcher. Do not assume this tool exists or hard-code a machine path. A metadata fallback is conclusive: use Sol routing policy without claiming the primary is Sol, changing the model or effort, or retrying another interpreter. Workers inherit root limits and never run a root lookup.

The reader inspects only the exact local session through read-only state lookup and bounded metadata. It does not scan other chats or emit conversation text. Launchers do not install, download, activate, or change runtime configuration. Running them still requires a PowerShell or POSIX `sh` shell and a compatible Python runtime; they are not zero-runtime cross-platform execution. The local storage format is not a stable public API. See the [primary-model reader reference](skills/subagent-steward/references/primary-model.md).

Install with Codex by asking `$skill-installer` to install `GengsengGhou/subagent-steward`, path `skills/subagent-steward`, at ref `v3.1.0`. For manual installation, download the [release ZIP](https://github.com/GengsengGhou/subagent-steward/releases/download/v3.1.0/subagent-steward-v3.1.0.zip) and place its `subagent-steward/` directory under `$CODEX_HOME/skills/` (usually `~/.codex/skills/` when unset). The skill is available next turn. When updating from an earlier default or economy edition, back up personal edits, replace the skill directory, and replace only the optional `subagent-steward` marker block in `AGENTS.md` with the [v3.1.0 snippet](examples/AGENTS.snippet.md); preserve all other instructions and settings.

See the [skill](skills/subagent-steward/SKILL.md), [optional AGENTS snippet](examples/AGENTS.snippet.md), [model guidance](skills/subagent-steward/references/model-guidance.md), and [reader reference](skills/subagent-steward/references/primary-model.md).

## License

[MIT](LICENSE).
