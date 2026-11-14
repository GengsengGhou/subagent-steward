---
name: subagent-steward
description: "Adapt delegation to the chosen primary model for substantial implementation, debugging, research, or review. Give capable workers complete outcomes, select model and effort flexibly, preserve assigned roles, and retain meaningful lead acceptance. Skip tiny edits and routine conversation."
---

# 子智能体管家 · Subagent Steward

Preserve the user's chosen primary model and reasoning effort, scope, authorization, key choices, quality requirements, and scientific correctness. Explicit user preferences for cost, speed, quality, or direct work override the tendencies below. Do not change the model picker or primary effort. The lead retains decisions, communication, meaningful acceptance, and final delivery; it may always investigate, implement, test, review, or take over when useful, without extra proof or a failed-worker trial.

## Role first, then primary model

**An assigned worker remains that worker.** Inheriting this skill does not make it the root lead or authorize whole-task delegation. Execute the assigned scope and return its outcome. The root normally dispatches peer workers directly; peers may cooperate within their ownership, authorization, and visibility to the assigning parent. No mandatory Sol manager or successive coordinator chain is needed.

A worker may subdivide only when its parent's assignment explicitly grants bounded permission. A grant can be given up front without repeated approval for each child or user confirmation. State the original boundaries, constraints, acceptance needs, integration owner, and useful report-back. The worker retains integration and verification responsibility and keeps the root informed of meaningful subdivision or changes. Permission does not propagate implicitly: a worker may grant further subdivision authority only if its own grant explicitly permits that, within the original authorized bounds. Do not forward the whole assignment through coordinators. Without nesting permission, execute directly or flag a real need; do not stop for routine approvals. Runtime limits always prevail; these instructions are not hard enforcement of permissions or depth.

For the **root lead**, use explicit current-turn primary metadata when already supplied. Otherwise, when a delegation policy is first needed in a root turn, run the bundled [primary-model reader](scripts/read_primary_model.py) once with available Python 3, respecting the user's environment: `python -B "<skill-directory>/scripts/read_primary_model.py"`. It resolves `CODEX_THREAD_ID` through read-only local state and reads the latest `turn_context` model and effort from a bounded tail of that session's log. Reuse the result within that turn; refresh next root turn when needed so model changes are respected. Workers inherit the root's model-family limits and do not run this lookup for routing. See [reader details](references/primary-model.md) for the output and compatibility limits.

If the reader cannot run or resolve the model, apply Sol's delegation policy and child-family set only; do not claim the primary is Sol or change the selected primary or effort. Do not install a runtime solely for this lookup, broaden it into a config/history scan, repeatedly probe, ask the user for a model, or add a separate routing-analysis step.

| Current primary | Regular child families | Delegation tendency |
| --- | --- | --- |
| Astra | Luna, Terra, Sol | Proactively delegate substantial coherent routine outcomes when native conditions permit, including useful serial delegation for cost and parallel work. Direct work remains available when useful. |
| Sol | Luna, Terra, Sol | Complete suitable coherent work directly, including substantial tasks. Delegate for useful cost, time, parallelism, task fit, context isolation, or review. |
| Terra | Terra, Luna | Complete suitable coherent work directly, including substantial tasks. Delegate within these families for useful cost, task fit, parallelism, context isolation, or review. |
| Luna | Luna | Complete suitable coherent work directly, including substantial tasks. Use same-family delegation for useful independent parallel work, context isolation, or review. |

Treat the chosen primary as the user's intended capability and cost choice. These family boundaries are project policy, not an objective capability ranking or hard budget guarantee. They constrain regular child selection, not delegation, worker count, parallel work, or whether a child can own a complete outcome. When useful independent work exists, the root may split it across suitable permitted families and work concurrently; no cost or capability proof is required. If a suitable live-supported child is unavailable within the permitted families, work directly. A genuine blocker can be reported normally, without silently widening the family set. Explicit user instruction or existing explicit authorization can widen it; preserve explicit model choices without asking again. Do not change the model picker or primary effort.

## Choose model and effort flexibly

Choose practically for quality, total completion cost including lead work and retries, time, and tool fit. Every family can own coherent outcomes through implementation, investigation, writing, and checks or review when suitable and permitted by the root. Clear scope alone does not prescribe Luna: Terra overlaps with both Luna and Sol, including bounded execution and code fixes. These are soft overlapping advantages, not exclusive jobs, eligibility gates, or a universal model ranking:

| Worker model | Useful fit | Practical starting effort |
| --- | --- | --- |
| `gpt-6-luna` | Cost-efficient focused execution, local technical judgment, and bounded problem-solving, including deeper reasoning with clear constraints; also repeatable or high-volume work | `high`; lighter effort may suffice |
| `gpt-6.1-terra` | Writing and content adaptation from supplied material, visual reasoning, computer use with a defined outcome, and scoped code fixes | `medium` |
| `gpt-6.1-sol` | Complex coding and professional projects, uncertain investigation, coordinating interdependent deliverables, integration, and judgment from conflicting evidence | `medium` |

Use task fit and the user's priorities to choose among permitted families. Favor Luna when candidates are equally suitable and another permitted family has no practical advantage; this is a tie-breaker, not a cheaper-first trial. No failure or other proof gate is required before choosing any suitable permitted family. The effort examples are local starting points, not official or mandatory defaults. Choose `xhigh` or `max` normally when depth helps, without a progression or extra proof, and lighter effort when appropriate. Do not default to `ultra`.

Select only models and efforts supported by the **live native tool**. Preferred family routes are Luna `gpt-6-luna` to `gpt-5.6-luna`, Terra `gpt-6.1-terra` to `gpt-5.6-terra`, and Sol `gpt-6.1-sol` to `gpt-6-sol`, then `gpt-5.6-sol`. Check task/tool fit and supported effort separately. A fallback or custom role cannot widen the root's permitted families. If no suitable permitted candidate is available, execute directly rather than silently crossing families. Disclose meaningful fallbacks and retain suitable active owners. An Astra child may be used under an Astra root for useful bounded consequential judgment, or with explicit user authorization; never use it as an automatic escalation from a known Sol, Terra, or Luna root.

For the official basis and the distinction from this project's policy, consult [model guidance](references/model-guidance.md) when evaluating or updating routing. API model documentation does not establish availability in the current subagent tool or measured quality and savings.

## Give workers complete outcomes

Hand over a coherent result, with task-appropriate discovery, technical design, authorized environment or tool setup, implementation through interface integration, meaningful checks and acceptance-harness creation and execution, in-scope repair, remote commands and log follow-up, related docs, verification records, and artifact references ready for acceptance. These are responsibilities as needed, not a universal checklist. Respect project rules reserving integration or checks for the lead. Keep unresolved user intent, key scientific or product choices, consequential out-of-scope tradeoffs, and permissions with the lead; workers make ordinary local decisions within the assignment without step-by-step approval.

Discover enough to hand off accurately and satisfy project discovery rules without routinely pre-solving the work. Do not duplicate broad exploration, implement the same scope in parallel, or habitually take over local repairs. For multiple workers, name a useful execution or integration owner for interfaces, combined verification, and evidence; an extra manager is not required. Reuse suitable owners for related follow-ups. Pass relevant changed constraints or responsibilities to older workers rather than assuming they know revised instructions, resending the entire skill, or replacing active owners just to refresh guidance.

## Dispatch and coordinate

Use native subagent tools, not user-owned chats, CLI, or API processes to evade limits. Set **both model and reasoning effort explicitly** on every spawn. With `collaboration.spawn_agent`, use `model`, `reasoning_effort`, and `fork_turns: "none"` plus a self-contained assignment; a full-history fork does not accept those overrides. Prefer the default role unless another is requested or appropriate under the live contract. Account for fixed role settings before spawning; choose a compatible role and settings that stay within the root's family boundary, and do not claim an effective model or effort without available evidence.

Include the objective, decisions already made, bounded ownership, inputs and paths or symbols, acceptance needs, constraints, applicable project instructions, permitted root families, and whether bounded subdivision is permitted. Descendants keep the original root's family boundary; a worker does not become a new root or apply the Sol identity fallback. Do not assume a fresh worker shares tools or history. For edits, assign non-overlapping file or module ownership, say others share the workspace, and require accommodating rather than reverting their changes. Ask for concise results, accessible actual artifacts and evidence, checks actually run and outcomes, remaining uncertainty, and prompt notice of material blockers or changes; do not request private reasoning.

Reuse fully read, still-available applicable rules and evidence. Reread for truncation, possible changes, lost context, required freshness, or higher-priority instructions; do not add routine hashes or logs. Pass project discovery evidence already collected. Where codebase-memory applies, include project and generation/freshness, graph and coverage findings, source fallbacks, and unresolved gaps. It is optional to this skill: use available source tools when absent and do not index unrelated projects for non-code work.

Before dispatch, briefly state the assignment, model, and effort in the user's language. Concurrent independent parent work is required only if the live tool actually requires it, including for nesting. If required, use real independent work; if none exists, execute directly and revisit delegation when useful. Otherwise waiting for the owner is valid. Do not manufacture busywork.

Use stage-appropriate native completion events or bounded waits within runtime and user-update rules. Avoid unjustified short probes, busy polling, repeated inspection, and redundant execution. Combine nonurgent feedback to the same owner; promptly relay meaningful findings, blockers, changed requirements, and urgent messages. At full capacity, reuse a suitable owner or queue work. Direct work remains available when useful; do not terminate active work to free a slot or evade limits. Choose worker count and subdivision for useful independent work and live capacity; this skill imposes no worker-count, depth, or token-share quotas.

## Accept, repair, and deliver

Review relevant **actual artifacts and reproducible evidence** against the user's goal; a summary alone is insufficient. Use the owner's checks without routinely repeating them, writing replacement harnesses, or patching integration glue yourself. Incomplete integration, checks, or docs ordinarily receive a targeted continuation to the same owner. Independent review, deeper investigation, additional checks, or direct takeover remain available whenever useful for quality, uncertainty, risk, inconsistent evidence, or project requirements. Meaningful verification and scientific correctness remain required.

Distinguish missing inputs or environment problems from reasoning or implementation errors before changing models. Choose a useful correction, effort or model adjustment, review, or direct work without a fixed retry ladder. Preserve useful artifacts, failed checks, and findings; avoid repeated dead ends or restarting completed work. Do not stop authorized work solely because a cost heuristic was reached.

Report model/effort, validation, and material changes when useful to the user. Do not invent usage, savings, quality equivalence, or hard budget guarantees. API price ratios are not Codex plan-credit ratios or total completion costs. Avoid persistent routing logs or extra artifacts unless requested.
