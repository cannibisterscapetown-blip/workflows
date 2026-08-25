# Cannibisters Slack Agent Team — Architecture & Rollout Plan

A team of department-scoped Claude agents living in Slack, so staff in each
department can tag the right agent to handle tasks that currently bottleneck
on one person (adding new strains to Shopify, answering loyalty questions,
adjusting member discounts, pulling reports).

This folder is the source of truth:

| File | What it is | Who reads it |
|---|---|---|
| `README.md` (this file) | Architecture, model tiering, cost control, rollout | You (owner) |
| `HANDBOOK.md` | "Which agent do I tag, and how" | All staff |
| `agents/strain-agent.md` | Product/strain intake agent spec + system prompt | The agent itself |
| `agents/loyalty-agent.md` | Budbar loyalty & discounts agent spec + system prompt | The agent itself |
| `agents/marketing-agent.md` | Marketing/reporting agent spec + system prompt | The agent itself |
| `agents/ORCHESTRATOR.md` | Routing + escalation rules shared by all agents | The agents |

---

## How the agents live in Slack

Two ways to run this. Start with Option A (works today, zero code), graduate
to Option B if you outgrow it.

### Option A — Department channels + Claude in Slack (recommended start)

One Claude bot, but each **department channel gets its own agent persona**
loaded from this repo:

```
#agent-strains    ← HQ office tags @Claude here when a new strain lands
#agent-loyalty    ← budbar staff tag @Claude here for member/discount tasks
#agent-marketing  ← reports, campaign checks, email drafts
#agent-help       ← "which agent do I need?" — the dispatcher answers
```

The channel determines which spec file in `agents/` governs the
conversation. Each channel gets a pinned Slack canvas that is a copy of the
relevant section of `HANDBOOK.md`, so staff always see what the agent in
that channel can and can't do.

Why channels instead of one do-everything bot:
- **Scoping is safety.** The loyalty agent's channel is private to budbar
  staff + managers; the strain agent never touches customer data.
- **The channel is the audit log.** Every discount change lives in a thread
  a manager can review.
- **Cheaper.** A narrow agent with a short spec burns far fewer tokens than
  a mega-prompt covering every department.

### Option B — Named bots via the Claude Agent SDK (later, if needed)

Separate Slack apps (`@Strainy`, `@LoyalT`, `@Marko`…) each running the
Agent SDK with its spec file as the system prompt and only the MCP tools it
needs (strain agent: Shopify only; loyalty agent: Shopify customers +
discounts only). This gives per-agent model selection, hard tool
allowlists, and real usage metering per agent — but it's infrastructure you
have to host. Don't build this until Option A is creaking.

---

## Model tiering (the usage-burn plan)

The principle: **expensive models plan and judge; cheap models execute
templates.** Almost everything these agents do daily is template execution.

| Task | Model | Why |
|---|---|---|
| Designing/changing the agent team, new workflows, this plan | Fable 5 | Rare, high-leverage, happens in sessions like this one |
| Routing "which agent handles this?" | Sonnet 5 | Trivial classification — never spend big-model tokens on it |
| Strain writeup (metafields, description, tags) | Sonnet 5 | Fully templated by `shopify_product_template.md`; Sonnet follows templates excellently |
| Loyalty lookups (fetch member info, explain a discount) | Sonnet 5 | Read-only, structured |
| Discount **changes** within policy limits | Sonnet 5 | Policy in the spec does the thinking; the model just applies it |
| Discount changes **outside** policy / disputes / judgment calls | Opus 5 (or escalate to a human) | Genuine judgment |
| Monthly performance reports, campaign analysis | Opus 5 | Multi-source synthesis benefits from the bigger model |

Practical notes:
- In Option A, model choice is a workspace/agent setting rather than
  per-message — set the Slack agents' default to Sonnet 5 and reserve
  Opus/Fable for sessions you run yourself (like this planning session).
- In Option B you set the model per bot, and the specs' escalation rules
  (`ORCHESTRATOR.md`) decide when a worker hands a task up.
- Never use Fable as a live router. Routing is the cheapest task in the
  system; the specs make it a lookup, not a decision.

## Cost-control rules baked into the specs

1. **Templates over reasoning.** Every recurring task has a template in this
   repo; agents fill templates, they don't reinvent structure.
2. **One-shot answers.** Specs instruct agents to gather everything needed
   and reply once, not to think out loud across ten messages.
3. **Scoped tools.** Fewer available tools = smaller prompts = cheaper calls.
4. **Escalation is explicit.** Workers escalate by *stopping and tagging a
   human or a bigger-model session* — not by retry-looping.

---

## Guardrails (non-negotiable, encoded in each spec)

- **Loyalty agent** may change a member's discount only within the policy
  table in its spec (tier caps + max single change). Anything outside → it
  drafts the change and tags a manager for a ✅ reaction before applying.
- **Every write action gets receipted** in-thread: what changed, old → new
  value, link to the Shopify record.
- **No customer PII leaves the private loyalty channel.** The agent shares
  loyalty status with staff so *they* relay it to the member.
- **Strain agent publishes nothing.** It fills drafts; a human flips the
  product to Active (matches the current `draft → review → publish` flow in
  this repo's scripts).

## Rollout

1. **Week 1 — Strain agent only, HQ channel.** Lowest risk, highest rep
   count, the template already exists. Martine's Slack ping becomes the
   trigger, same as today's workflow doc.
2. **Week 2 — Loyalty agent, read-only.** Budbar staff can fetch loyalty
   info but the agent can't change discounts yet. Confirm the policy table
   (`agents/loyalty-agent.md` → `TO CONFIRM` markers) with real numbers.
3. **Week 3 — Loyalty writes within policy + marketing agent.**
4. **Ongoing —** review agent threads weekly; anything the agents got wrong
   becomes a line in their spec file (specs are living documents — PR the
   fix, don't re-explain in Slack each time).
