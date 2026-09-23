---
name: subagent-steward
description: "Choose whether to delegate substantial implementation, debugging, research, or review work under an Astra lead, then select Luna or Sol and reasoning effort to control total completion cost. Use for independent subtask planning or explicit cost-aware delegation; skip routine conversation and tiny edits."
---

# 子智能体管家 · Subagent Steward

Keep the user's chosen primary model and reasoning effort. The intended lead is Astra: it owns user communication, requirements, architecture, delegation, acceptance, and final delivery. Do not switch the lead to save money. When another primary model is explicitly selected, respect it.

This skill requests delegation when the conditions below are met, and explicitly instructs selection of the subagent models and reasoning efforts below. The Luna/high and Sol/medium starting points follow official Codex guidance; the task-routing and exception rules are local trial policy, not measured cost or quality guarantees. Explicit user choices take precedence.

## Decide whether to delegate

Make a brief decision, not a separate planning exercise. Complete tiny edits, short answers, and tightly coupled work directly. Spawn only for a bounded independent task when the lead has useful nonduplicative work to do alongside it and the expected execution, context isolation, or independent review benefit justifies dispatch and acceptance overhead. Do not invent parallel work to justify spawning.

Set no fixed preferred number or skill-level cap on children. Choose concurrency from the number of ready independent tasks, ownership conflicts, expected marginal benefit, dispatch/acceptance overhead, and the live runtime's available capacity. Spawn additional children when each has worthwhile independent work; do not fill slots merely because they exist. When runtime capacity is exhausted, queue remaining work and reuse available children as supported. Do not bypass runtime limits.

Children must not delegate further unless the user explicitly requests nested delegation. A child loading this skill should execute its assignment and return blockers to the lead, not become another coordinator.

Keep unresolved product decisions and high-impact tradeoffs with the lead. Give workers enough autonomy to execute an agreed technical objective without asking Astra to approve each step.

## Choose model and effort independently

Select for the actual subtask, not the size or prestige of the overall project. First choose the model for the judgment required, then choose effort for the amount of planning, analysis, and checking needed. Clear scope can still require substantial reasoning.

Use `gpt-6-luna` at `high` as the normal starting point for focused, well-specified work, including summarization, extraction, transformation, and focused coding. Luna is not restricted to mechanical tasks. Use `gpt-6-sol` at `medium` as the normal starting point for work requiring stronger autonomous judgment, including everyday implementation, complex coding, research, and agentic workflows. Sol need not be reserved for exceptional difficulty or a failed Luna attempt.

| Subtask | Model | Starting effort |
| --- | --- | --- |
| Focused investigation, summaries, extraction, or implementation with clear boundaries and objective checks | `gpt-6-luna` | `high` baseline |
| Truly mechanical work with explicit rules, few interacting constraints, and cheap reliable checks | `gpt-6-luna` | Consider `medium` or `low` as a cost-saving exception |
| Bounded work with unusually demanding combinations of constraints or edge cases and reliable acceptance checks | `gpt-6-luna` | Consider `xhigh`; `max` only when additional depth is worth the time and usage |
| Implementation, research, or tool workflows requiring autonomous technical judgment | `gpt-6-sol` | `medium` baseline |
| Cross-module debugging, subtle correctness review, or integration requiring substantial analysis | `gpt-6-sol` | `high`; consider `xhigh` for unusually demanding analysis |
| Exceptionally hard work for which deeper reasoning is worth greater time and usage | Appropriate Luna/Sol model for the judgment required | `max` only with a concrete task-specific reason |

Use these GPT-6 model IDs when the live subagent tool supports them. Select effort from that tool's supported values; API documentation and the primary-model picker do not establish subagent availability. Do not infer measured savings or quality gains from the generation change alone.

Choose the justified effort up front; the levels are not a ladder of mandatory trial runs. Do not lower Luna's effort merely because it is the cheaper model, or raise it to Max merely because it is the smaller model. Task length, many files, or having tests alone does not justify Max. Most tasks do not need Max. A Luna Max exception needs both a bounded problem it can reasonably solve and a specific need for unusually deep analysis/checking. There is no established rule that Luna Max is better or cheaper overall than Sol medium.

Use Sol directly when ambiguity, cross-cutting dependencies, weak acceptance checks, or likely rework make Luna a poor bet. Raising Luna's effort is not a substitute for the judgment needed to choose an approach. Do not force every task through a Luna attempt first. Astra retains decisions that require the user's broader intent.

Official basis, checked 2026-09-23: [Codex model guidance](https://developers.openai.com/codex/models) recommends starting with Luna High and Sol Medium; [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) emphasizes focused, high-volume tasks, and [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) emphasizes complex coding and agentic workflows. API parameter defaults are distinct from these Codex recommendations. Effort levels do not map exactly across model generations. The official Astra Light recommendation does not override this user's chosen lead effort. These references support the policy; do not re-fetch them on every delegation unless availability or guidance needs updating.

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

Before dispatch, give one brief explanation in the user's language, such as: "接口已经明确，这部分交给 Luna/high 补齐边界测试；我继续处理集成。" When departing from the Luna/high or Sol/medium baseline, include the concrete reason in that same sentence. Do not narrate an elaborate scoring system.

## Accept, repair, or escalate

Review the actual deliverable and material evidence. Run proportionate integration or acceptance checks; do not redo all of the child's exploration or automatically hire another reviewer. Independent review is useful when risk justifies it, not on every task. The lead remains responsible for the final result.

On failure, distinguish missing information, tooling/environment problems, and reasoning/implementation errors. Fix missing inputs or environment issues without automatically increasing model cost. For a localized correctable error, give one targeted correction to the same child when that is likely cheaper than replacement. If the task exceeds Luna's judgment or that correction fails, hand the unresolved work and existing evidence to Sol, or resolve it as the lead. Do not rerun the complete task through every model and effort level. When Sol is blocked, Astra should reassess the approach before spawning more workers. Do not stop an authorized task solely because a trial cost heuristic was reached.

## Keep the experiment observable and light

When children were used, add a short final accounting if useful: selected model/effort, work delegated, validation outcome, and any escalation. Do not add a routing report to routine answers. Judge savings using total lead-plus-child usage, retries, acceptance work, and result quality. API per-token price ratios do not establish Codex plan-credit ratios or total task savings. Report actual usage/cost only if the runtime or provider exposes it; do not invent token counts, savings percentages, or a hard budget guarantee. Avoid persistent logs or extra artifacts unless requested.
