---
title: "Course syllabus"
description: "Course information, description, learning outcomes and the five-module overview for AI Automation and Agents, with the official syllabus PDF (v2.0) to read online or download."
type: Reference
tags: [course, student-facing, syllabus, learning-outcomes, certificate]
status: stable
generated:
  by: "claude/fable-5-1"
  at: "2026-09-08T00:00:00Z"
sources:
  - id: syllabus-v2
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/assets/files/AI_Automation_Agents_Syllabus_v2.pdf"
    title: "AI Automation & Agents — Course Syllabus v2.0 (revised April 2026)"
    author: "University of Arizona Online; Arizona Institute for Artificial Intelligence (AI2S)"
  - id: wiki-home
    resource: "https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki"
    title: "AI Automation and Agents v2 wiki: Home (course description, learning outcomes, course overview table)"
    author: "Carlos Lizárraga-Celaya; Michelle Yung"
    last_modified: "2026-08-28T19:24:31-07:00"
---

# Course syllabus

*AI Automation & Agents - Build Workflows. Deploy Agents. Work Smarter.*
Course 2 of the AI Education Series, University of Arizona Online. Non-credit
professional development, 40 hours. Syllabus version 2.0, revised April 2026.

[:material-file-pdf-box: Download the syllabus (PDF)](../assets/files/AI_Automation_Agents_Syllabus_v2.pdf){ .md-button .md-button--primary target=_blank }
[:material-map-marker-path: How this course works](how-this-course-works.md){ .md-button }

## Course information

| Parameter | Details |
| :-- | :-- |
| Format | 5 modules, self-paced online with optional instructor-led cohort sessions |
| Total hours | 40 hours (8 hours per module) |
| Level | Intermediate; requires completion of Course 1 (Introduction to Generative AI) |
| Audience | Workforce professionals and graduate students seeking applied AI skills |
| Time commitment | About 8 hours per module |
| Tools used | Claude Desktop (Cowork + Code), n8n, LangChain, LangGraph, CrewAI, Ollama, Google Colab |
| Assessment | Concept quizzes, guided lab exercises, one hands-on project per module, case study analyses, peer reviews, and a capstone deployment policy |
| Prerequisites | Basic Python knowledge |
| Free-tier path | A no-cost alternative track is available using Ollama, n8n Community Edition, and Google Colab |

## Course description

This course moves beyond individual AI prompts into the world of AI agents and
automated workflows: systems that can take actions, use tools, manage files,
and complete multi-step tasks on your behalf. Learners progress from
foundational agent theory through to structured agent frameworks used in
industry, gaining transferable skills applicable to any organization or
platform.

The course follows a layered progression. Module 1 builds the conceptual
foundation: defining what agents are, surveying the no-code, low-code and
code-first automation spectrum, and introducing Claude Desktop for hands-on
agent interaction. Subsequent modules introduce the leading open-source agent
frameworks (LangChain, LangGraph and CrewAI) through guided Jupyter Notebook
labs on Google Colab, covering reasoning architectures, tool integration,
memory, retrieval-augmented generation, and multi-agent coordination.
Throughout, the emphasis remains practical and workforce-relevant.

The course closes with a dedicated module on responsible agentic AI, covering
production deployment, evaluation, observability, security (the OWASP Top 10
for LLM Applications), and governance grounded in the EU AI Act and the NIST
AI Risk Management Framework (AI RMF 1.0).

## Course learning outcomes

Upon successful completion of this course, learners will be able to:

1. **Design** an AI agent system specification that selects and justifies the
   reasoning architecture, memory configuration, retrieval pipeline, and
   multi-agent coordination pattern for a given task and deployment context.
2. **Implement** end-to-end AI agent pipelines integrating tool use, vector
   retrieval, conversational memory, multi-agent workflows, and observability
   instrumentation using current industry frameworks.
3. **Diagnose** failures in AI agent systems by analyzing reasoning traces,
   RAGAS evaluations, coordination logs, and observability data, attributing
   deficiencies to specific architectural causes.
4. **Evaluate** an AI agent system's production readiness across accuracy,
   cost, latency, safety, and coordination efficiency, and determine when
   multi-agent complexity is warranted.
5. **Apply** responsible AI governance frameworks (EU AI Act, NIST AI RMF) to
   classify risk, specify mitigations and human oversight checkpoints, and
   produce accountability documentation.

## Course overview

| # | Module | Key topics | Hours |
| :--: | :-- | :-- | :--: |
| 1 | [**From Prompts to Pipelines:** Thinking Like an Automation Designer](../modules/module-1/overview.md) | Agent loop; no-code/low-code/code-first spectrum; workflow decomposition; Claude Desktop; key vocabulary | 8 |
| 2 | [**Agent Reasoning Architectures and Tool Integration**](../modules/module-2/overview.md) | Chain-of-Thought, ReAct, Tree of Thoughts, LATS; tool integration with LangChain; prompt engineering; trace evaluation; architectural trade-offs | 8 |
| 3 | [**Total Recall:** Memory Architectures and Retrieval-Augmented Generation](../modules/module-3/overview.md) | Parametric vs. non-parametric memory; six-stage RAG pipeline; conversational memory types; retrieval optimization; RAGAS evaluation | 8 |
| 4 | [**Multi-Agent Systems**](../modules/module-4/overview.md) | Coordination architectures; LangGraph multi-agent implementation; three-role pipeline design; CrewAI vs. LangGraph comparison; coordination failure diagnosis | 8 |
| 5 | [**Responsible Agentic AI:** Production Deployment, Evaluation, and Responsible AI](../modules/module-5/overview.md) | Technical debt and production infrastructure; multi-dimensional evaluation and CI/CD; observability with LangSmith; OWASP Top 10; EU AI Act, NIST AI RMF, human-in-the-loop | 8 |

??? note "How the PDF differs from the current module pages"

    The syllabus PDF (v2.0, April 2026) predates the current course content.
    Its titles for Modules 2-4 describe an earlier design centred on Claude
    Cowork, n8n, MCP and Claude Code (*No-Code Automation: Claude Cowork, n8n
    & Connected Apps*; *AI with Memory & Integrations: MCP, LangChain Tools &
    Agent Memory*; *Building AI Agents: Claude Code, LangChain, LangGraph &
    CrewAI*), and Module 5 as *Responsible Agentic AI: Trust, Control & Safe
    Deployment*. The module pages on this site are the current course. Where
    the two disagree, the module pages and your LMS take precedence; the PDF
    remains the reference for the course information table, the free-tier
    path and the certificate rules. The PDF itself notes that it "is subject
    to change as AI tools evolve".

## Completion and certification

From the syllabus:

- Complete all five module projects and pass all five concept quizzes (70% or
  above) to earn a digital certificate of completion.
- Learners who complete both Course 1 (Introduction to Generative AI) and
  Course 2 (AI Automation & Agents) receive the University AI Education Series
  professional badge.
- A free-tier completion path is supported: learners who complete all
  activities using Ollama, n8n, and Google Colab in lieu of paid Claude tools
  are eligible for the same certificate.
- Bring your own work: apply course projects to real tasks from your job or
  studies. The Workflow Audit and the capstone deployment plan are
  portfolio-quality artifacts.

Grade weights for each module are stated in that module's overview; see
[How this course works](how-this-course-works.md) for the pattern.

## Read the syllabus online

<iframe class="course-pdf" src="../assets/files/AI_Automation_Agents_Syllabus_v2.pdf" title="AI Automation and Agents course syllabus (PDF)" loading="lazy"></iframe>

If your browser cannot display the PDF above,
[download the syllabus (PDF, 19 pages)](../assets/files/AI_Automation_Agents_Syllabus_v2.pdf){target=_blank} instead.
