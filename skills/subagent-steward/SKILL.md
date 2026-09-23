---
name: subagent-steward
description: "Choose whether to delegate substantial implementation, debugging, research, or review under an Astra lead. Prefer Luna with task-appropriate reasoning; choose Sol on concrete evidence to control total completion cost. Use for independent subtask planning or explicit cost-aware delegation; skip routine conversation and tiny edits."
---

# 子智能体管家 · Subagent Steward

Keep the user's chosen primary model and reasoning effort. The intended lead is Astra: it owns user communication, requirements, architecture, delegation, acceptance, and final delivery. Do not switch the lead to save money. When another primary model is explicitly selected, respect it.

This skill requests delegation when the conditions below are met, and explicitly instructs selection of the subagent models and reasoning efforts below. The Luna/high and Sol/medium starting points follow official Codex guidance; the task-routing and exception rules are local trial policy, not measured cost or quality guarantees. Explicit user choices take precedence.

## Decide whether to delegate

Make a brief decision, not a separate planning exercise. Complete tiny edits, short answers, and tightly coupled work directly. Spawn only for a bounded independent task when the lead has useful nonduplicative work to do alongside it and the expected execution, context isolation, or independent review benefit justifies dispatch and acceptance overhead. Do not invent parallel work to justify spawning.

Set no fixed preferred number or skill-level cap on children. Choose concurrency from the number of ready independent tasks, ownership conflicts, expected marginal benefit, dispatch/acceptance overhead, and the live runtime's available capacity. Spawn additional children when each has worthwhile independent work; do not fill slots merely because they exist. When runtime capacity is exhausted, queue remaining work and reuse available children as supported. Do not bypass runtime limits.

Children must not delegate further unless the user explicitly requests nested delegation. A child loading this skill should execute its assignment and return blockers to the lead, not become another coordinator.

Keep unresolved product decisions and high-impact tradeoffs with the lead. Give workers enough autonomy to execute an agreed technical objective without asking Astra to approve each step. Do not make Astra pre-solve the implementation or micromanage a worker merely to keep it on Luna; count that extra lead work against the expected savings.

## Choose model and effort for total completion cost

Default eligible delegated work to `gpt-6-luna` at `high`. Give Luna clear goals, boundaries, relevant context, and acceptance criteria, with autonomy to investigate and make local technical decisions. This includes implementation, debugging, tests, research, and work spanning multiple files or modules when the interfaces and intended behavior are sufficiently bounded.

Compare plausible model-and-effort combinations rather than treating task difficulty as an automatic model upgrade. For a bounded but demanding task, seriously consider Luna at `xhigh` or `max` before choosing Sol. Higher effort is a candidate, not a mandatory trial. When the evidence below justifies Sol, use `gpt-6-sol` at `medium` as its starting effort and adjust to the analysis required.

| Subtask | Model | Starting effort |
| --- | --- | --- |
| Investigation, implementation, debugging, tests, or research with bounded objectives and checkable outcomes, including local technical judgment and multiple modules | `gpt-6-luna` | `high` baseline |
| Truly mechanical work with explicit rules, few interacting constraints, and cheap reliable checks | `gpt-6-luna` | Consider `medium` or `low` as a cost-saving exception |
| Bounded work with long reasoning chains, interacting constraints, or difficult edge cases, with reliable acceptance checks | `gpt-6-luna` | Consider `xhigh` or `max` when the specific reasoning burden warrants it |
| Work meeting a concrete Sol selection reason below | `gpt-6-sol` | `medium` baseline; `high` or `xhigh` for demonstrably deeper analysis |
| Exceptionally demanding analysis for either selected model | Luna or justified Sol | `max` when the additional depth is worth its time and usage |

Use these GPT-6 model IDs when the live subagent tool supports them. Select effort from that tool's supported values; API documentation and the primary-model picker do not establish subagent availability. Do not infer measured savings or quality gains from the generation change alone.

Choose the justified effort up front; the levels are not a ladder of mandatory trial runs. Neither Sol nor Max is justified merely by the words "complex", "autonomous", "cross-module", a file count, or task length. Luna Max needs a concrete reasoning burden, such as interacting boundary conditions in a specified state machine. It does not require a failed lower-effort attempt first. Do not lower Luna's effort merely because it is cheaper or default it to Max merely because it is smaller.

### Require a concrete reason for Sol

Before choosing Sol, identify why a suitably supported, higher-effort Luna is a poor fit for this particular task. A sufficient reason can be:

- Available evidence or relevant prior results show a capability gap on this kind of task; name the missing capability or failed invariant.
- The task requires unresolved global design or correctness judgment, errors would have material consequences and be difficult to detect, and proportionate scoping or checks cannot sufficiently reduce that risk. Missing tests alone is not sufficient; consider an affordable focused check first.
- A Luna attempt reveals substantive reasoning or implementation failure after adequate context and, when worthwhile, one targeted correction. Missing tools, environmental errors, or a failing test alone do not establish a model capability gap.
- Task-specific evidence indicates Sol is likely to reduce total lead-plus-child cost or meet an explicit time constraint better, including dispatch, retries, acceptance, and recovery. Generic expectations that Sol is "safer" or Luna "might need rework" are not evidence.

Explicit user model choices and unavailable Luna tooling can also justify Sol; disclose the reason. When a sufficient reason is already known, choose Sol directly without an unnecessary Luna trial. When both choices seem plausible and there is no concrete counterevidence, prefer Luna with an appropriate effort and bounded acceptance checks. Do not invent success probabilities or cost estimates to rationalize either choice.

Optimize expected total completion cost at acceptable quality. Luna's lower per-token cost can make extra reasoning and a recoverable failed attempt economical; do not optimize only for first-pass success. Conversely, expensive Astra handholding, hard-to-detect errors, or costly recovery can erase the benefit. Keep the user's product and architectural decisions with Astra.

Official basis, checked 2026-09-23: [Codex model guidance](https://developers.openai.com/codex/models) recommends starting with Luna High and Sol Medium; [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) emphasizes focused, high-volume tasks, and [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) emphasizes complex coding and agentic workflows. These starting efforts apply after choosing a model; they do not establish which model is cheapest for a task. Luna-first routing is this skill's cost-oriented policy, not an official comparative performance claim. API parameter defaults are distinct from Codex recommendations, and effort levels do not map exactly across generations. Preserve the user's chosen Astra effort. Do not re-fetch these references on every delegation unless availability or guidance needs updating.

Exclude Terra and Astra from the default child route. Use Terra only when explicitly requested or when task-specific measured results support it. Use an Astra child only when explicitly requested or when a bounded independent high-stakes judgment clearly warrants it; explain that exception briefly. Usually the existing Astra lead handles the hardest judgment itself. Do not default children to `ultra`; GPT-6 Luna does not support Ultra.

## Dispatch without accidental Astra inheritance

Use native subagent tools, not new user-owned tasks or a second CLI/API process as a workaround. Check the live tool's supported models, efforts, and role behavior. Set BOTH model and reasoning effort explicitly on every spawn. Where `collaboration.spawn_agent` is available, use `model`, `reasoning_effort`, and `fork_turns: "none"`; supply a self-contained task message. Do not combine a model override with a full-history fork, which may be unsupported or inherit the primary model. Reuse an existing child for related follow-up work when its model remains suitable.

Prefer the default role unless the user requests another role or the tool contract allows choosing one. Custom role configuration may override spawn settings: avoid roles with incompatible fixed models. If the desired model or effort is unavailable, use a supported Luna/Sol combination appropriate to the task, or do the work locally. When a GPT-6 model is unavailable, its `gpt-5.6-luna` or `gpt-5.6-sol` predecessor is an eligible fallback only if the live subagent tool lists it; check its supported effort separately. Disclose material fallback; do not silently spawn an inherited Astra or claim a requested model was used without evidence.

Provide only the necessary handoff:

- Objective, relevant decisions, scope, and objective acceptance criteria.
- Exact inputs, paths or symbols, constraints, and required tools. Include applicable project instructions that a fresh child would otherwise miss. Do not assume it has the parent's tools or history.
- For code discovery, follow applicable project discovery instructions and pass the evidence already collected. If the project uses codebase-memory, include project/freshness, relevant graph and coverage evidence, source fallbacks, and unresolved gaps. This skill does not require that plugin; use available source tools when it is absent. Do not create or index unrelated projects merely to delegate non-code work.
- For edits, assign file/module ownership. State that others share the codebase, that their changes must not be reverted, and that the child should accommodate concurrent changes. Avoid overlapping writers.
- Ask for the result or artifact, exact evidence locations, checks actually run and their outcomes, and remaining uncertainty. Request a concise summary, not a transcript. Do not request private chain-of-thought.
- State: execute only this assignment, do not spawn children, and report concrete blockers instead of repeatedly exploring the same dead end.

Before dispatch, give one brief explanation in the user's language, such as: "接口已经明确，这部分交给 Luna/high 补齐边界测试；我继续处理集成。" For higher-effort Luna, name the reasoning burden; for any Sol child, including Sol/medium, name the concrete Sol selection reason. Include the selected effort. Keep this to a short decision summary, not a scoring exercise.

## Accept, repair, or escalate

Review the actual deliverable and material evidence. Run proportionate integration or acceptance checks; do not redo all of the child's exploration or automatically hire another reviewer. Independent review is useful when risk justifies it, not on every task. The lead remains responsible for the final result.

On failure, distinguish missing information, tooling/environment problems, and substantive reasoning/implementation errors. Fix missing inputs or environment issues without automatically increasing model cost. For a localized correctable error, give one targeted correction to the same child when that is likely cheaper than replacement. If a substantive capability gap remains, apply the Sol selection criteria and hand over existing artifacts, exact failed checks, and unresolved work, or resolve it as the lead. Do not automatically upgrade after any failed check, repeatedly retry the same dead end, or restart completed work through every model and effort level. When Sol is blocked, Astra should reassess the approach before spawning more workers. Do not stop an authorized task solely because a trial cost heuristic was reached.

## Keep the experiment observable and light

When children were used, add a short final accounting if useful: selected model/effort, work delegated, validation outcome, and any escalation. Do not add a routing report to routine answers. Judge savings using total lead-plus-child usage, retries, acceptance work, and result quality. API per-token price ratios do not establish Codex plan-credit ratios or total task savings. Report actual usage/cost only if the runtime or provider exposes it; do not invent token counts, savings percentages, or a hard budget guarantee. Avoid persistent logs or extra artifacts unless requested.
