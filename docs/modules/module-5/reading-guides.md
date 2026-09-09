---
title: Module 5 Reading Guides
description: Chapter-by-chapter reading guides (focus points and active reading tasks) for the Module 5 chapters on production deployment, evaluation, observability, LLM security, and responsible AI.
type: Reading Guide
tags:
- module-5
- student-facing
- reading-guide
- production
- evaluation
- langsmith
- owasp
- eu-ai-act
- nist-ai-rmf
module: 5
status: stable
stale_after: '2027-09-01T00:00:00Z'
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-5.2-Addendum
  title: 'AI Automation and Agents v2 wiki: Module-5.2-Addendum'
  author: Carlos Lizárraga-Celaya; Michelle Yung
  last_modified: '2026-09-03T07:53:58-07:00'
authorship:
  created: '2026-08-13'
  updated: '2026-08-28'
  contributors:
  - C. Lizárraga
  - M. Yung
wiki_page: Module-5.2-Addendum
---
# Module 5 Reading Guides

## Chapter 1 Reading Guide: From Prototype to Production { #reading-guide-1 }

**Assigned Reading:** [The Agent Development Lifecycle](https://www.langchain.com/blog/the-agent-development-lifecycle){target=_blank} (LangChain)
**Estimated time:** 30 minutes

### What to Focus On

**Hidden Technical Debt (Sculley et al., 2015)**

The chapter introduces five categories of technical debt that are invisible in prototypes but costly in production. For each one, understand what it is, how it shows up in agent systems, and how to prevent it:

| Category | Core idea |
|---|---|
| Entanglement | Changing one component breaks another unexpectedly |
| Unstable data dependencies | Upstream data changes silently degrade behavior |
| Feedback loops | The system's outputs influence its future inputs |
| Configuration debt | Parameters scattered with no versioning or documentation |
| Undeclared consumers | Downstream systems depend on your output format without anyone tracking it |

**The Production Stack**

The chapter presents five infrastructure layers (containerization, orchestration, API gateway, secrets management, autoscaling). For each, know what it does and why it matters specifically for agents.

**The Assigned Reading** covers the agent development lifecycle from LangChain's perspective. Focus on what changes between prototype and production and how teams decide when an agent is ready.

### Active Reading Tasks

**Task A:** For each of the five debt categories, write one sentence describing how it could appear in an agent system you built or proposed in this course.

**Task B:** Pick two layers from the production stack table. For each, describe what would go wrong in a production agent deployment if that layer were missing.

## Chapter 2 Reading Guide: Evaluating AI Agents { #reading-guide-2 }

**Estimated time:** 20 minutes (chapter content only)

### What to Focus On

**No Single Metric Is Enough**

The chapter's central argument: accuracy alone is insufficient. Models that rank highly on accuracy often rank poorly on robustness or efficiency (Liang et al., 2022). Know all six evaluation dimensions and be able to give an example failure for each:

| Dimension | What it measures |
|---|---|
| Task accuracy | Correct outputs |
| Safety & alignment | Refuses harmful requests, stays in bounds |
| Resource efficiency | Token cost, latency, API calls |
| Robustness | Performance under unexpected inputs |
| Fairness & bias | Consistent across demographic groups |
| Observability | Diagnosable when failures happen |

**LLM-as-Judge**

Understand when this is needed (no single correct answer to compare against), what it requires (judge prompt design, explicit rubrics, human-label validation), and its limits (judge model bias).

**CI/CD for Agents**

Every prompt change, tool update, or model swap triggers the evaluation suite. Failures block deployment. Prompt changes are code changes.

### Active Reading Tasks

**Task A:** Name a change to an agent that improves one evaluation dimension while degrading another. Identify which dimension you would gate on in CI/CD and what threshold blocks a deploy.

**Task B:** A team wants to evaluate whether their agent's reasoning traces are logically coherent. Explain in 2-3 sentences why reference-based metrics (like exact match) won't work and what approach the chapter recommends instead.

## Chapter 3 Reading Guide: Observability { #reading-guide-3 }

**Assigned Reading:** [LangSmith Observability Quickstart](https://docs.langchain.com/langsmith/observability-quickstart){target=_blank}
**Estimated time:** 30 minutes

### What to Focus On

**Classical Signals + Agent-Specific Signals**

Know the three classical signal types (logs, metrics, traces) and what each captures. Then know what additional signals agent systems require: prompt content/length, reasoning traces and tool calls, inter-agent messages, token consumption, and retrieval relevance scores.

**LangSmith vs. LangFuse**

LangSmith integrates natively with LangChain/LangGraph (minimal config). LangFuse is open-source and self-hostable (matters for data sovereignty). Both capture full agent execution traces.

**OpenTelemetry (OTel)**

Vendor-neutral instrumentation. Instrument once, route to any backend. Understand why this matters: switching platforms later requires only a config change, not a code rewrite.

**What to Monitor**

Six signals that indicate production problems:
1. Error rate spike
2. Token cost anomaly (often runaway loops or unbounded context)
3. Retrieval quality degradation
4. Safety/guardrail violations
5. Tool call failure rate
6. Latency above target

**The Assigned Reading** walks through setting up tracing in LangSmith. Focus on how traces appear in the dashboard and what information they expose about agent execution.

### Active Reading Tasks

**Task A:** Classify each of the following as a log, metric, or trace: (1) the sequence of tool calls during one user query, (2) average tokens per request over 24 hours, (3) a timestamped record that the agent called `web_search` with a specific query.

**Task B:** Your agent's token consumption spikes 5x with no code changes. Which monitoring signal is this, and what two causes does the chapter suggest?

## Chapter 4 Reading Guide: Security Risks for LLM Applications { #reading-guide-4 }

**Assigned Video:** [OWASP's Top 10 Ways to Attack LLMs: AI Vulnerabilities Exposed](https://www.youtube.com/watch?v=gUNXZMcd2jU){target=_blank} (IBM Technologies)
**Estimated time:** 30 minutes (chapter) + 20 minutes (video)

### What to Focus On

**OWASP Top 10 for LLM Applications (2026)**

These are the ten most critical risks for any LLM-powered system. For each, know the risk name, what it means in plain terms, and one example of how it applies to an agent:

Key entries to internalize:
- **LLM01 Prompt Injection:** Input alters the model's behavior in unintended ways
- **LLM02 Sensitive Information Disclosure:** System exposes data through unauthorized channels
- **LLM03 Excessive Agency:** Agent has too much functionality, too many permissions, or too much autonomy
- **LLM09 Vector and Embedding Weaknesses:** Attackers manipulate what the model sees via retrieval, not via instructions

**OWASP Top 10 for Agentic Applications (2026)**

These extend the LLM Top 10 to autonomous agents. The Agentic list focuses on how autonomy, delegation, and multi-step execution amplify risks:

Key entries to internalize:
- **ASI01 Agent Goal Hijack:** Attacker redirects what the agent is trying to do
- **ASI06 Memory & Context Poisoning:** False data planted in memory corrupts future reasoning
- **ASI07 Insecure Inter-Agent Communication:** Messages between agents lack authentication
- **ASI08 Cascading Failures:** One fault propagates across a multi-agent system

**The Assigned Video** covers the LLM Top 10 from a 2025 perspective. The ordering differs slightly from 2026 but the threats are the same.

### Active Reading Tasks

**Task A:** Pick an agent system you built or proposed in this course. Identify the three LLM Top 10 risks most relevant to it and explain why in one sentence each.

**Task B:** For each of the following scenarios, identify which Agentic Top 10 entry applies: (1) An attacker poisons a shared memory store so a downstream agent makes biased decisions. (2) Agent A sends a forged message to Agent B, and Agent B acts on it without verifying the source. (3) A malicious MCP server is loaded at runtime.

## Chapter 5 Reading Guide: Responsible AI: Governance, Compliance, and Accountability { #reading-guide-5 }

**Assigned Video:** [AI Governance and the EU AI Act: What Developers Need to Know](https://www.youtube.com/watch?v=GELAXU9XReI){target=_blank} (~15 minutes)
**Estimated time:** 25 minutes (chapter) + 15 minutes (video)

### What to Focus On

**NIST AI Risk Management Framework**

NIST (the U.S. National Institute of Standards and Technology) provides guidance for managing AI risks. Know the four functions and what each does:

| Function | Purpose |
|---|---|
| **Govern** | Establish policies, roles, and accountability |
| **Map** | Identify uses, affected populations, and risks |
| **Measure** | Develop metrics and testing to produce evidence about the risk profile |
| **Manage** | Implement mitigations and review effectiveness |

The chapter illustrates all four using a claims-processing agent example. Understand how one agent scenario threads through all four functions.

**EU AI Act: Four-Tier Classification**

Know the four tiers (Unacceptable, High Risk, Limited Risk, Minimal Risk), what compliance obligations each carries, and one agent example per tier. Key points:
- Classification depends on deployment context, not architecture
- The same agent could be minimal or high risk depending on what decisions it informs
- Non-compliance with high-risk obligations carries fines up to 3% of global annual revenue
- Other jurisdictions are drafting similar frameworks, so this matters globally

**Classifying Your Agent**

The chapter gives four questions to determine classification. The most common mistake is placing credit, employment, or education agents in Limited Risk because a human reviews the output. Human review does not change the tier.

**Human-in-the-Loop (HITL)**

Both the EU AI Act and NIST RMF require defining where human authority is needed. For the chapter, focus on the three design questions: which actions need a gate, what does the reviewer need to see, and what happens on rejection.

**Governance Artifacts**

Four documentation types: model cards, system cards, risk registers, and incident response plans. Know what each documents and why they exist (demonstrating accountability).

**The Assigned Video** covers the EU AI Act's four tiers and practical compliance obligations for developers.

### Active Reading Tasks

**Task A:** Apply the four-question classification process to an agent you built or proposed in this course. Which tier does it fall in? Justify in 2-3 sentences.

**Task B:** For the same agent, write one sentence for each NIST RMF function describing what it would look like in practice (using the claims-agent example in the chapter as a model).

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-5.2-Addendum){target=_blank} (wiki page last changed 2026-09-03). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-5/reading-guides.md){target=_blank}.</p>
