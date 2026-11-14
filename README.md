# 子智能体管家 / Subagent Steward

**v2.0.0 · 统一自适应维护版**

子智能体管家会按根主智能体当前选择的主模型、任务适配度和实时工具支持来安排工作。它既支持直接完成，也支持把连贯的完整结果交给合适的子智能体，并由主智能体验收实际产物。旧正式版仍可使用；v2.0.0 是一个统一自适应维护版。它是社区维护的 Codex skill，不是 OpenAI 官方项目或独立调度服务。

- [v2.0.0 正式发布页](https://github.com/GengsengGhou/subagent-steward/releases/tag/v2.0.0)
- [下载技能 ZIP](https://github.com/GengsengGhou/subagent-steward/releases/download/v2.0.0/subagent-steward-v2.0.0.zip)

## 按主模型适配分工

| 根主智能体主模型 | 常规子模型族 | 通常的分工倾向 |
| --- | --- | --- |
| Astra | Luna、Terra、Sol | 原生条件允许时，主动委派适合的常规执行；有用时可串行或并行拆分。直接完成仍可选。 |
| Sol | Luna、Terra、Sol | 可直接完成适合的完整任务；也可为成本、并行、任务适配、上下文隔离或复核而委派。 |
| Terra | Terra、Luna | 可直接完成适合的完整任务；也可在这两个模型族内分工。 |
| Luna | Luna | 可直接完成适合的工作；有益时可在同族内并行、隔离上下文或复核。 |

这些模型族边界是项目路由政策，体现用户的能力与成本选择，不是客观能力排名或硬预算。边界限制常规子模型族，不限制是否委派、任务规模、人数或并行协作。只有用户明确指示或已有明确授权时，根主智能体才扩大模型族范围；没有合适且实时工具支持的候选时，直接完成。

主模型识别只使用明确的新鲜 **CURRENT-TURN** 元数据。若当前轮主控需要决定委派而没有可用的本轮身份信息，可用随附 Python 3 标准库脚本只读查询当前会话一次；不扫描其他聊天，不把数据库中的旧模型字段当作当前身份，也不输出聊天正文。结果在该根主控轮复用，下一轮需要委派时重新确认。子智能体继承根主控的模型族范围，不自行查询并套用根主控回退。

脚本不可用、环境不支持或本地元数据缺失时，仅回退到 Sol 分工政策；这不表示实际主模型是 Sol，也不会更改主模型或推理强度。此读取方式依赖本地实现格式，不是稳定的公开 API。小任务直接完成，无需为了读取主模型运行脚本。详见[主模型读取说明](skills/subagent-steward/references/primary-model.md)。

## 灵活选模型与强度

Luna、Terra、Sol 都可在合适且受允许的情况下负责实现、调查、写作、检查或复核等完整结果。选择时综合任务适配、工具支持、时间与总完成成本，并尊重用户偏好；适配相当且其他候选没有实际优势时偏好 Luna。范围清楚本身不决定选择 Luna，Terra 也适合有边界的执行和代码修复。

| 子模型 | 适用倾向 | 实用强度起点 |
| --- | --- | --- |
| `gpt-6-luna` | 集中执行、局部技术判断、边界清楚的问题求解及重复工作 | `high` |
| `gpt-6.1-terra` | 基于材料写作、视觉理解、目标明确的电脑操作及局部代码修复 | `medium` |
| `gpt-6.1-sol` | 复杂编程、不确定调查、相互依赖的交付与整合、冲突证据判断 | `medium` |

强度起点只是参考；按任务选择支持的强度，需要深度时可直接选择 `xhigh` 或 `max`。模型族首选及同族回退为 Luna `gpt-6-luna` → `gpt-5.6-luna`、Terra `gpt-6.1-terra` → `gpt-5.6-terra`、Sol `gpt-6.1-sol` → `gpt-6-sol` → `gpt-5.6-sol`。只使用实时原生工具支持且属于根主控允许范围的候选。不更换主模型或主推理强度。

## 角色与交付

执行者仍是执行者：按获派范围交付完整结果，不因继承本技能而成为根主智能体。只有父任务明确授予有边界的拆分权限时，执行者才可继续委派；权限不自动向后传播。交办时传递根主控允许的模型族、范围、授权、验收要求和整合责任，后代继续遵守原根的模型族边界。

执行者按任务需要负责准备、调查、设计、实现、整合、必要检查和证据；多人协作需明确整合负责人。主智能体保留用户沟通、关键决策、实际产物验收与最终交付，并审查相关实际产物和可复现证据。未完成部分通常交原负责人定向续做；按风险深入复核或直接接管。依实时工具采用完成通知或有界等待，不设固定人数、嵌套深度或 token 配额，也不要求先用较低成本模型试错。

## 安装

### 使用 Codex skill-installer

在 Codex 中请求安装以下 GitHub 技能，并指定发布 ref：

```text
使用 $skill-installer 从 GitHub 仓库 GengsengGhou/subagent-steward 安装 skills/subagent-steward，指定 --ref v2.0.0。
```

### 手动安装

从[发布页](https://github.com/GengsengGhou/subagent-steward/releases/tag/v2.0.0)下载 [v2.0.0 ZIP](https://github.com/GengsengGhou/subagent-steward/releases/download/v2.0.0/subagent-steward-v2.0.0.zip)，解压后将其中的 `subagent-steward/` 文件夹放入 `$CODEX_HOME/skills/`；若未设置 `CODEX_HOME`，通常使用 `~/.codex/skills/`。保留技能目录结构，包括 `scripts/` 和 `references/`。安装后下一轮即可使用 `$subagent-steward`。

从旧默认版或经济版更新前，备份对技能的个人修改，再替换同名技能目录。若个人或项目 `AGENTS.md` 中有可选的 `subagent-steward` 标记块，同步换成 v2.0.0 的[可选配置片段](examples/AGENTS.snippet.md)；只替换该标记块，保留文件中的其他指令与配置。安装不会更改主模型、推理强度或其他设置。

## 功能与依据

- [技能正文](skills/subagent-steward/SKILL.md)：完整策略、模型选择及角色规则。
- [可选 AGENTS 片段](examples/AGENTS.snippet.md)：项目或个人指令中的简短调用入口。
- [模型依据](skills/subagent-steward/references/model-guidance.md)：官方资料与项目路由政策的区别。
- [主模型读取说明](skills/subagent-steward/references/primary-model.md)：本地只读查找、输出及失败回退。

Python 读取器只用标准库；若 Python、本地状态库或会话格式不可用，技能按 Sol 路由政策继续工作，不会为此安装运行环境或依赖。本地读取格式可能变化。实际节省、质量等效或硬预算结果未经量化保证。

## English

Subagent Steward v2.0.0 is one unified adaptive Codex skill; earlier official editions remain usable. It adapts delegation to the root lead's freshly identified current primary model, task fit, and live native-tool support. The lead may work directly or assign a coherent end-to-end outcome, then accepts the actual artifact. This is a community-maintained skill, not an official OpenAI project or standalone scheduler.

| Root primary | Regular child families | Usual tendency |
| --- | --- | --- |
| Astra | Luna, Terra, Sol | Proactively delegate suitable routine execution when native conditions permit; split serially or in parallel when useful. Direct work remains available. |
| Sol | Luna, Terra, Sol | Complete suitable work directly or delegate for cost, parallelism, task fit, context isolation, or review. |
| Terra | Terra, Luna | Complete suitable work directly or delegate within these families. |
| Luna | Luna | Work directly or use same-family delegation for useful parallel work, context isolation, or review. |

These family limits are local routing policy that reflects the user's capability and cost choice, not an objective ranking or hard budget. They constrain regular child-family selection, not delegation, task size, worker count, or parallelism. Only explicit user direction or existing authorization widens the root's family set. If no suitable live-supported candidate is available within it, work directly.

Use only fresh, explicit **CURRENT-TURN** primary metadata. If a root needs a delegation policy and no current identity is available, the bundled Python 3 standard-library reader can inspect the exact current session locally and read-only. It does not scan other chats or expose conversation text. Reuse its result within that root turn; refresh on a later delegation turn. Workers inherit root limits and do not run a root lookup. If the runtime or local format is unavailable, use Sol's routing policy as a fallback without claiming the actual primary is Sol or changing the primary or effort. This local storage format is not a stable public API. See the [reader reference](skills/subagent-steward/references/primary-model.md).

Luna, Terra, and Sol can each own complete implementation, investigation, writing, checks, or review when suitable and permitted. Choose by task and tool fit, total completion cost, time, and user preference; favor Luna only when candidates are equally suitable and another permitted family has no practical advantage. Practical effort starting points are Luna/high, Terra/medium, and Sol/medium. They are not mandatory defaults; choose a supported effort directly, including `xhigh` or `max` when depth helps. Preferred same-family routes are Luna `gpt-6-luna` to `gpt-5.6-luna`, Terra `gpt-6.1-terra` to `gpt-5.6-terra`, and Sol `gpt-6.1-sol` to `gpt-6-sol`, then `gpt-5.6-sol`. Never change the selected primary or its effort.

An assigned worker remains a worker and completes its assigned scope. It may delegate further only with explicit bounded permission from its parent; permission does not propagate automatically. Handoffs carry the original root's permitted families, scope, authorization, acceptance needs, and integration responsibility. Workers own a complete result as appropriate; the lead retains key decisions, meaningful acceptance, and final delivery.

Install with Codex by asking `$skill-installer` to install `GengsengGhou/subagent-steward`, path `skills/subagent-steward`, at ref `v2.0.0`. For manual installation, download the [release ZIP](https://github.com/GengsengGhou/subagent-steward/releases/download/v2.0.0/subagent-steward-v2.0.0.zip), then place the ZIP's `subagent-steward/` directory under `$CODEX_HOME/skills/` (usually `~/.codex/skills/` when unset). The skill is available next turn. When updating from an earlier default or economy edition, back up personal edits, replace the skill directory, and replace only the optional `subagent-steward` marker block in `AGENTS.md` with the [v2.0.0 snippet](examples/AGENTS.snippet.md); preserve all other instructions and settings.

See the [skill](skills/subagent-steward/SKILL.md), [optional AGENTS snippet](examples/AGENTS.snippet.md), [model guidance](skills/subagent-steward/references/model-guidance.md), and [primary-model reader reference](skills/subagent-steward/references/primary-model.md). The reader uses Python's standard library only. If Python or the local metadata format is unavailable, routing falls back to Sol without changing the primary or effort. No runtime or dependency is installed for the lookup, and no savings, quality equivalence, or hard budget is guaranteed.

## License

[MIT](LICENSE).
