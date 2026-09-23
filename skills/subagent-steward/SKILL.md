---
name: subagent-steward
description: "Choose whether to delegate substantial implementation, debugging, research, or review under an Astra lead. Balance Luna, Sol, and reasoning effort by task needs and total cost, favoring Luna when both fit. Use for independent subtask planning or explicit cost-aware delegation; skip routine conversation and tiny edits."
---

# 子智能体管家 · Subagent Steward

Keep the user's chosen primary model and reasoning effort. The intended lead is Astra: it owns user communication, requirements, architecture, delegation, acceptance, and final delivery. Do not switch the lead to save money. When another primary model is explicitly selected, respect it.

This skill requests delegation when the conditions below are met, and explicitly instructs selection of the subagent models and reasoning efforts below. The Luna/high and Sol/medium starting points follow official Codex guidance; the task-routing suggestions are local trial policy, not measured cost or quality guarantees. Explicit user choices take precedence.

## Decide whether to delegate

Make a brief decision, not a separate planning exercise. Complete tiny edits, short answers, and tightly coupled work directly. Spawn only for a bounded independent task when the lead has useful nonduplicative work to do alongside it and the expected execution, context isolation, or independent review benefit justifies dispatch and acceptance overhead. Do not invent parallel work to justify spawning.

Set no fixed preferred number or skill-level cap on children. Choose concurrency from the number of ready independent tasks, ownership conflicts, expected marginal benefit, dispatch/acceptance overhead, and the live runtime's available capacity. Spawn additional children when each has worthwhile independent work; do not fill slots merely because they exist. When runtime capacity is exhausted, queue remaining work and reuse available children as supported. Do not bypass runtime limits.

Children must not delegate further unless the user explicitly requests nested delegation. A child loading this skill should execute its assignment and return blockers to the lead, not become another coordinator.

Keep unresolved product decisions and high-impact tradeoffs with the lead. Give workers enough autonomy to execute an agreed technical objective without asking Astra to approve each step. Do not make Astra pre-solve the implementation or micromanage a worker merely to keep it on Luna; count that extra lead work against the expected savings.

## Choose model and effort for total completion cost

Choose a model-and-effort combination using ordinary task judgment: scope, uncertainty, reasoning depth, ability to check the result, likely supervision, time, and total cost. When both models look suitable with no clear practical advantage, favor `gpt-6-luna` for its lower cost. This is a preference, not a requirement to prove Luna inadequate before selecting `gpt-6-sol`.

Luna/high and Sol/medium are useful starting points, not compulsory defaults or a trial sequence. Give either worker clear goals, relevant context, and enough autonomy to investigate and make local technical decisions. Use the tendencies below as guidance, not eligibility tests.

| Subtask | Model | Starting effort |
| --- | --- | --- |
| Focused implementation, investigation, tests, summaries, or research, including local technical judgment and multiple modules | Usually `gpt-6-luna` | `high` is a useful starting point |
| Simple extraction, transformations, or repetitive edits | Usually `gpt-6-luna` | `low` or `medium` can be sufficient |
| Clear goals with long reasoning chains, interacting constraints, or many edge cases | Often `gpt-6-luna` | Freely choose `xhigh` or `max` for deeper reasoning |
| Open-ended investigation, changing hypotheses, competing approaches, or integration needing broader judgment | Often `gpt-6-sol` | `medium` or `high`, adjusted to the task |
| Deep analysis or extensive checking for either model | Whichever fits the work | `xhigh` or `max` when useful |

Use these GPT-6 model IDs when the live subagent tool supports them. Select effort from that tool's supported values; API documentation and the primary-model picker do not establish subagent availability. Do not infer measured savings or quality gains from the generation change alone.

Select the effort that seems useful up front. There is no required progression through high, xhigh, and max, and no preference for xhigh solely because Max is the highest setting. If deeper thought is likely to help, Luna Max is a normal option; if the work is straightforward or latency matters more, use a lighter setting. The same flexibility applies to Sol. Neither Sol nor Max needs extra proof, a benchmark, a prior failure, or a special approval beyond ordinary task judgment. Do not manufacture certainty or collect evidence solely to authorize a model choice.

Task labels are hints, not automatic routing rules: multi-module work can fit Luna, and focused work can fit Sol when its judgment is likely to make execution easier. Choose Sol directly when it seems better suited to the investigation or expected supervision needs; Luna does not have to fail first. Likewise, do not choose Sol just because it is generally stronger or reject Luna merely because the task takes many steps. Keep the user's product and architectural decisions with Astra.

Aim for acceptable quality at reasonable total completion cost, including lead supervision, retries, acceptance, and elapsed time when relevant. Luna's lower per-token cost can make extra reasoning worthwhile; Sol can avoid costly guidance or rework. Use available experience when helpful without requiring measurements, inventing success probabilities, or assuming either model always wins.

Official basis, checked 2026-09-23: [Codex model guidance](https://developers.openai.com/codex/models) recommends starting with Luna High and Sol Medium; [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) emphasizes focused, high-volume tasks, and [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol) emphasizes complex coding and agentic workflows. These starting efforts do not establish which model is cheapest for a task. Favoring Luna when both fit is this skill's cost preference, not an official comparative performance claim. API parameter defaults are distinct from Codex recommendations, and effort levels do not map exactly across generations. Preserve the user's chosen Astra effort. Do not re-fetch these references on every delegation unless availability or guidance needs updating.

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

Before dispatch, briefly state the assignment, model, and effort in the user's language, such as: "这部分交给 Luna/max 补齐状态机边界测试；我继续处理集成。" A short rationale can help when the choice matters, but do not produce a model-selection report or extra justification for Sol or Max.

## Accept, repair, or escalate

Review the actual deliverable and material evidence. Run proportionate integration or acceptance checks; do not redo all of the child's exploration or automatically hire another reviewer. Independent review is useful when risk justifies it, not on every task. The lead remains responsible for the final result.

On failure, distinguish missing information, tooling/environment problems, and reasoning/implementation errors. Fix missing inputs or environmental problems rather than assuming a stronger model will resolve them. Choose the useful next step: clarify the assignment, give a targeted correction, adjust effort, switch models, or handle the unresolved part as the lead. No fixed number of corrections or demonstrated capability gap is required before changing course. Preserve existing artifacts, failed checks, and useful findings when handing work over. Avoid automatic upgrades after every failed check, repeated dead-end retries, and restarting completed work. Do not stop an authorized task solely because a trial cost heuristic was reached.

## Keep the experiment observable and light

When children were used, add a short final accounting if useful: selected model/effort, work delegated, validation outcome, and any escalation. Do not add a routing report to routine answers. Judge savings using total lead-plus-child usage, retries, acceptance work, and result quality. API per-token price ratios do not establish Codex plan-credit ratios or total task savings. Report actual usage/cost only if the runtime or provider exposes it; do not invent token counts, savings percentages, or a hard budget guarantee. Avoid persistent logs or extra artifacts unless requested.
