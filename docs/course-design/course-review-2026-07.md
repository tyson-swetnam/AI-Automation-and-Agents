---
title: Course Review Analysis (July 2026)
description: Internal pedagogical review of the five-module course written from a graduate student's perspective, flagging overview/content mismatches, prerequisite escalation, and writing-load imbalance as of July 2026.
type: Course Design
tags:
- course
- instructor-facing
- course-design
- review
status: deprecated
superseded_by: development-plan.md
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Course-Review-Analysis-v1
  title: 'AI Automation and Agents v2 wiki: Course-Review-Analysis-v1'
  author: Michelle Yung
  last_modified: '2026-08-19T16:35:14-07:00'
wiki_page: Course-Review-Analysis-v1
---
# Course Review Analysis (July 2026)

!!! warning "Historical document"

    This review reflects the course as of 2026-07-31. Several findings (overview rewrites, Module 2 alternative frameworks) have since been addressed; see the development plan for current status.

## Executive Summary

This document presents a structured review of the five-module graduate course "AI Automation and Agents v2," written from the perspective of a diligent graduate student working through the course sequentially. Each module carries an 8-hour time budget and targets non-CS graduate students seeking practical AI automation competency.

The course demonstrates strong conceptual scaffolding in its early modules and ambitious technical scope throughout. However, several critical coherence issues emerge: Overview pages frequently promise different content than what the Foundational Concepts and Activities deliver (Modules 2-4), the stated "no programming required" accessibility goal conflicts with actual lab requirements as early as Module 2, and the writing load in Modules 3-5 may crowd out the hands-on learning that should dominate an automation course.

**Overall Assessment:** The course has excellent bones — the conceptual frameworks are well-chosen, the progression from individual agents to multi-agent systems to production deployment is logical, and the responsible AI thread is woven throughout. The primary work needed is alignment: making Overviews match content, ensuring activities match the stated audience, and rebalancing the doing/reading/writing ratio in later modules.

---

## Module 1: "From Prompts to Pipelines: Thinking Like an Automation Designer"

**Time Budget:** 8 hours | **Status:** Nearly finalized | **Review Depth:** Polish-level

### Strengths

1. **Strong conceptual foundation.** The five foundational chapters build logically from "what is an agent" through paradigms, literacy, workflow thinking, and responsible AI. A student finishing this module has genuine vocabulary and mental models for the rest of the course.

2. **Excellent activity design.** The Workflow Audit Project (2.5 hrs) is the right flagship activity — it forces students to apply decomposition frameworks to their own professional context, creating immediate personal relevance. The time allocation (doing-heavy) matches the 60/25/15 ideal.

3. **Accessible entry point.** Lab A (Ollama setup) and Lab B (Openwork agent) provide tangible "I built something" moments without requiring programming. The 45-minute time boxes are realistic.

4. **The 2D automation assessment framework** (rule-based specification + consequence severity) is a genuinely useful heuristic that students will carry beyond the course. It gives them a principled way to say "this should NOT be automated" — rare in AI courses.

5. **Responsible AI is introduced early** rather than bolted on at the end. Integrating NIST RMF and AI4People principles in Module 1 means students encounter every subsequent module through an ethics-aware lens.

### Areas for Improvement

1. **Self-check prompts (10 min) feel vestigial.** At 10 minutes, they cannot provide meaningful reflection. Consider either expanding them to 20 minutes with a brief written response, or folding them into the lab introductions as warm-up questions.

2. **"Blast radius" concept needs more scaffolding.** This is introduced in Chapter 5 (Responsible AI) but would benefit from a concrete example matrix showing blast radius assessments for 3-4 common automation scenarios. Students from non-technical backgrounds may struggle to calibrate "severity" without anchoring examples.

3. **Discussion post timing.** The 30-minute allocation for post + reply is tight if students are expected to reference their Workflow Audit findings. Consider whether the discussion should come after the audit (as synthesis) or before (as ideation). Currently the sequencing is ambiguous.

### Time Budget Assessment

| Activity | Allocated | Realistic | Notes |
|----------|-----------|-----------|-------|
| Self-check prompts | 10 min | 10 min | Adequate for current scope |
| Lab A (Ollama) | 45 min | 45-60 min | Installation issues could extend this |
| Lab B (Openwork) | 45 min | 45 min | Reasonable |
| Workflow Audit Project | 2.5 hrs | 2.5-3 hrs | Depends on professional context complexity |
| Discussion Post + Reply | 30 min | 30-45 min | Tight if substantive replies expected |
| Readings (5 chapters) | ~3 hrs | 3 hrs | Dense but manageable |
| **Total** | **~8 hrs** | **8-9 hrs** | **Slightly tight but acceptable** |

### Recommendations (Priority Order)

1. **(Low effort)** Add 2-3 blast radius calibration examples to Chapter 5 — a table showing "automation scenario / rule-based spec score / consequence severity / recommended approach."
2. **(Low effort)** Clarify discussion post sequencing relative to the Workflow Audit.
3. **(Optional)** Consider making self-check prompts slightly more substantial or merging them into lab pre-work.

## Module 2: "No-Code Automation: Agent Reasoning Architectures and Tool Integration"

**Time Budget:** 8 hours | **Status:** Nearly finalized but has significant coherence issues | **Review Depth:** Polish-level with coherence flags

### Critical Issue: Overview vs. Content Mismatch

The module title says "No-Code Automation" and the Overview describes building pipelines with Claude Cowork and n8n. The actual Foundational Concepts and Activities teach:

- Four reasoning paradigms (CoT, ReAct, ToT, LATS)
- AgentExecutor architecture in LangChain
- Prompt engineering for agent control
- A guided lab building a ReAct agent in Google Colab (Python)

**This is not no-code content.** A student arriving from Module 1 (which required zero programming) expecting to build automations in Cowork and n8n will instead encounter Python code, LangChain imports, and Colab notebooks. The cognitive whiplash is significant.

### Additional Issue: Legacy Architecture

The content itself marks AgentExecutor as LEGACY within LangChain. Teaching students a deprecated architecture creates a shelf-life problem — by the time students apply this knowledge professionally, the recommended approach (LangGraph) will have fully superseded AgentExecutor. Module 4 then teaches LangGraph, making Module 2's AgentExecutor content feel like throwaway scaffolding.

### Strengths

1. **The reasoning paradigm taxonomy (CoT, ReAct, ToT, LATS) is excellent.** This is genuinely valuable conceptual content that helps students understand why agents reason differently in different contexts. The progression from simple (CoT) to complex (LATS) is well-structured.

2. **Reasoning Trace Interpretation** is a practical skill with real-world applicability. Being able to read and debug an agent's reasoning chain is useful regardless of framework.

3. **The Prompt Engineering Suite project** (2 hrs) is well-designed as a doing-oriented activity that builds transferable skills.

4. **Discussion post structure** (project proposal + peer review) is pedagogically sound — it creates accountability and exposes students to diverse application domains.

### Areas for Improvement

1. **The Overview must be rewritten to match the actual content,** OR the content must be rewritten to match the Overview. These are two different courses:
   - **Option A (Rewrite Overview):** Rename to something like "Agent Reasoning: How AI Systems Think and Act." Remove Cowork/n8n promises. Be transparent that this module introduces Python-in-Colab as a learning tool.
   - **Option B (Rewrite Content):** Actually deliver no-code automation with Cowork and n8n. Move reasoning paradigms to conceptual readings only. Make the lab a Cowork pipeline build. This would be a major rewrite but would honor the course's accessibility promise.

2. **Programming prerequisite gap.** The course states "no prior programming experience" for Modules 1-3, but Module 2's guided lab requires students to work in Google Colab with Python/LangChain code. Even if the notebook is pre-written, students need to understand imports, function calls, and output interpretation. This needs either:
   - Explicit acknowledgment that Module 2 introduces code-reading (not code-writing) as a skill
   - A "Python for Non-Programmers" primer (30-min pre-lab resource)
   - Redesign to actually be no-code

3. **AgentExecutor deprecation.** Either update to current LangChain patterns (langgraph prebuilt agents) or frame the content explicitly as "historical architecture study" with a forward pointer to Module 4's LangGraph content.

4. **Time budget for non-programmers.** The 2-hour Colab lab allocation assumes students can navigate a notebook environment. For genuinely non-technical students, environment setup alone could consume 30+ minutes.

### Time Budget Assessment

| Activity | Allocated | Realistic (CS student) | Realistic (Non-CS) | Notes |
|----------|-----------|----------------------|-------------------|-------|
| Self-check prompts | 15 min | 15 min | 15 min | Fine |
| Guided Lab (Colab ReAct) | 2 hrs | 1.5-2 hrs | 2.5-3 hrs | Non-CS students will struggle |
| Prompt Engineering Suite | 2 hrs | 2 hrs | 2 hrs | More accessible — text-based |
| Discussion (Proposal + Peer Review) | 1 hr | 1 hr | 1 hr | Reasonable |
| Readings (5 chapters) | ~3 hrs | 2.5 hrs | 3.5 hrs | Dense theoretical content |
| **Total** | **~8 hrs** | **7-8 hrs** | **9-10 hrs** | **Over budget for target audience** |

### Recommendations (Priority Order)

1. **(Critical)** Resolve the Overview vs. Content mismatch. Recommend Option A (rewrite the Overview) as the lower-effort path that preserves valuable content.
2. **(High)** Add a "Colab and Python Basics" 20-minute orientation resource for non-CS students. Frame it as "reading code, not writing code."
3. **(Medium)** Either update AgentExecutor references to current LangChain or add a prominent note: "This architecture pattern is being superseded by LangGraph (Module 4). We study it here for its clear illustration of the ReAct loop."
4. **(Low)** Consider whether the Prompt Engineering Suite project could partially replace the Colab lab for non-CS students (offering a "choose your depth" track).

## Module 3: "AI with Memory & Integrations: MCP, LangChain Tools & Agent Memory"

**Time Budget:** 8 hours | **Status:** Needs deep review | **Review Depth:** Full analysis with concrete recommendations

### Critical Issue: Overview vs. Content Mismatch (Again)

The Overview promises:

- Model Context Protocol (MCP) for desktop extensions
- Web connectors and integrations
- Building a Research Assistant Workflow with Claude Cowork

The actual content delivers:

- RAG pipeline architecture (six stages)
- Vector database concepts and chunking strategies
- Four LangChain memory types (ConversationBuffer, Summary, WindowBuffer, EntityMemory)
- RAGAS evaluation framework
- Retrieval optimization and context window management

MCP receives at most a passing mention in the actual lesson content. A student who read the Overview expecting to wire up Cowork with web connectors will instead spend 8 hours learning embedding models, chunk overlap parameters, and RAGAS faithfulness scores.

**The disconnect is arguably worse than Module 2** because at least Module 2's content (reasoning paradigms) is universally applicable. Module 3's Overview promises a completely different learning experience than what is delivered.

### Strengths

1. **The RAG pipeline content is genuinely excellent.** The six-stage pipeline (Ingest, Chunk, Embed, Index, Retrieve, Generate) provides a clear mental model. The progression from "why parametric memory isn't enough" to "how to evaluate retrieval quality" is well-structured.

2. **RAGAS evaluation framework** is a strong choice — it gives students quantitative tools (faithfulness, answer relevancy, context precision, context recall) to assess RAG system quality rather than relying on vibes.

3. **Memory type taxonomy** (the four LangChain memory types) helps students understand that "memory" is not monolithic — different conversation patterns need different memory architectures.

4. **The assessment structure is well-designed.** The three deliverables (RAGAS Interpretation Worksheet 25%, RAG Failure Diagnosis Report 20%, Memory Architecture Specification Brief 30%) target different cognitive levels: interpretation, diagnosis, and design.

5. **Context window management** is a practical constraint that every AI practitioner encounters. Teaching students to think about token budgets is immediately applicable.

### Areas for Improvement

1. **Overview must be rewritten** to reflect actual content. Suggested title adjustment: "AI Memory Systems: RAG, Vector Databases, and Evaluation." Remove MCP and Cowork promises unless corresponding activities are created.

2. **Where does MCP actually get taught?** If MCP is a course-level learning objective, it needs a home. Options:
   - Add a 45-min MCP lab to Module 3 (requires cutting something else)
   - Move MCP to Module 4 where it could complement the multi-agent discussion
   - Create a dedicated MCP mini-module or integrate it into Module 1's Cowork/Openwork labs
   - Remove MCP from course objectives entirely

3. **Writing load is heavy.** Three substantial deliverables in one module:
   - RAGAS Interpretation Worksheet (likely 400-500 words of analysis)
   - RAG Failure Diagnosis Report (likely 500-700 words)
   - Memory Architecture Specification Brief (likely 600-800 words)

   Combined, students may write 1,500-2,000 words of technical analysis in a single module. For a course targeting 15% writing, this skews heavily toward written output at the expense of hands-on time.

4. **The guided lab (RAG + memory, 2 hrs) requires Python/LangChain fluency** that Module 2 may not adequately develop, especially for non-CS students who struggled with Module 2's Colab lab. There is no explicit bridge acknowledging increased complexity.

5. **Chunking strategies section** needs grounding in student-relevant examples. Abstract discussion of "chunk overlap" and "recursive character splitting" means little without concrete demonstrations showing how different chunking approaches affect retrieval quality on the same document.

6. **Unit structure (6 units) feels fragmented** compared to Module 1-2's cleaner activity flow. Having readings, quiz, lab, project, case study, and discussion as separate "units" creates navigation overhead without clear pedagogical benefit over a simpler sequence.

### Time Budget Assessment

| Activity | Allocated | Realistic | Notes |
|----------|-----------|-----------|-------|
| Unit 1: Readings + Videos | 1.5 hrs | 1.5-2 hrs | Dense conceptual content |
| Unit 2: Quiz | 0.5 hrs | 0.5 hrs | Reasonable |
| Unit 3: Guided Lab (RAG + Memory) | 2 hrs | 2-3 hrs | High variance by student background |
| Unit 4: Optimization Project | 2.5 hrs | 2.5-3 hrs | Ambitious scope |
| Unit 5: RAGAS Case Study | 1 hr | 1-1.5 hrs | Requires careful metric interpretation |
| Unit 6: Discussion + Capstone Brief | 0.5 hrs | 0.5-1 hr | Brief is substantial for 30 min |
| **Total** | **8 hrs** | **8.5-11 hrs** | **Over budget, especially for non-CS** |

### Concrete Recommendations

1. **(Critical) Rewrite the Overview** to accurately describe RAG/Memory content. Remove or drastically reduce MCP promises.

2. **(Critical) Reduce writing load.** Recommendation: Merge the RAGAS Interpretation Worksheet into the Case Study activity (Unit 5) as an embedded component rather than a standalone deliverable. This eliminates one grading artifact while preserving the learning. Revised weighting:
   - RAG Failure Diagnosis Report: 30% (absorbs some RAGAS interpretation)
   - Memory Architecture Specification Brief: 35%
   - Lab Completion + Reflection: 20%
   - Discussion Participation: 15%

3. **(High) Add a "Module 2 Lab Skills Check" bridge** at the start of Unit 3. A 15-minute orientation that says: "You'll need these Colab skills from Module 2. If you struggled there, review [specific resources] before proceeding."

4. **(High) Add concrete chunking demonstrations.** Take one 3-page document and show students: "Here's what retrieval looks like with 200-token chunks vs. 500-token chunks vs. 1000-token chunks. Notice how the answer quality changes." This makes abstract concepts tangible. Time cost: ~20 min. Cut from: Unit 1 readings (trim one video).

5. **(Medium) Simplify unit structure.** Consider collapsing Units 1-2 (readings + quiz) into a single "Prepare" phase and Units 5-6 (case study + discussion) into a single "Synthesize" phase. This gives students a clearer three-act structure: Prepare (2 hrs) -> Build (4.5 hrs) -> Synthesize (1.5 hrs).

6. **(Medium) Scope the Memory Architecture Specification Brief more tightly.** Currently it carries 30% weight, which implies substantial length. Provide a template with specific sections and word limits per section (e.g., "System Context: 100 words, Memory Type Selection + Justification: 200 words, Retrieval Strategy: 150 words, Evaluation Plan: 150 words"). Total: 600 words maximum.

7. **(Low) Decide MCP's course-level home.** If MCP is a genuine course objective, recommend adding a 45-minute guided MCP walkthrough to Module 1's Lab B (Openwork agent setup) since MCP is a protocol for tool connectivity — it fits naturally alongside the "agent connects to tools" framing of Module 1.

## Module 4: "Building AI Agents: Multi-Agent Systems and Orchestration"

**Time Budget:** 8 hours | **Status:** Needs deep review | **Review Depth:** Full analysis with concrete recommendations

### Critical Issue: Missing Track A (Claude Code)

The Overview describes a dual-track approach:

- **Track A:** Claude Code for multi-agent orchestration
- **Track B:** Open-source frameworks (LangGraph, CrewAI)

The actual Activities are **entirely Track B.** There are no Claude Code activities, no Claude Code lab, and no Claude Code integration in any deliverable. Track A exists only as a promise in the Overview.

This is the third consecutive module (2, 3, 4) where the Overview promises content involving Claude/Anthropic tools that the actual activities do not deliver. The pattern suggests the Overviews were written to a different course design than the one that was ultimately implemented.

### Strengths

1. **The coordination architecture taxonomy is genuinely valuable.** The four patterns (hierarchical, peer-to-peer, pipeline, market-based) give students a vocabulary for describing multi-agent systems they encounter in industry. The taxonomy is well-chosen — it covers the major coordination patterns without being exhaustive to the point of confusion.

2. **Coordination failure taxonomy** (four failure modes) is an unusually mature pedagogical choice. Teaching students to diagnose failures — not just build systems — reflects real-world practice where most time is spent debugging, not building.

3. **The comparative evaluation requirement** (LangGraph vs. AutoGen/CrewAI) forces students to develop framework-agnostic thinking. Rather than becoming partisans of one tool, they learn to assess trade-offs.

4. **Evidence-based benchmarking** (Chapter 5) teaches measurement discipline. Students learn that "it works" is not an evaluation — you need metrics, baselines, and controlled comparisons.

5. **LangGraph as the primary framework** is a good choice given Module 2's (deprecated) AgentExecutor content. Students see the evolution: "This is what replaced what you learned before, and here's why."

### Areas for Improvement

1. **Track A (Claude Code) must either be implemented or removed from the Overview.** Options:
   - **(Recommended) Add a Track A alternative lab** (Unit 3 variant) where students use Claude Code to orchestrate a multi-agent workflow. This would require creating new lab content but would honor the dual-track promise and serve non-CS students who struggled with Colab.
   - **Remove Track A from the Overview** and acknowledge this is a code-first module. Less work, but further erodes the course's accessibility claims.
   - **Make Track A the primary and Track B the alternative.** This inverts the current design but better serves non-CS students.

2. **Prerequisite escalation is steep.** Module 4 expects students to:
   - Build state graphs in LangGraph (requires understanding nodes, edges, state management)
   - Compare across frameworks (requires running both LangGraph and CrewAI/AutoGen)
   - Diagnose coordination failures (requires understanding distributed systems concepts)

   A non-CS student who struggled through Modules 2-3's Colab labs will face even greater difficulty here. The jump from "run a pre-built notebook" to "build a state graph" is significant.

3. **Three major deliverables (30% + 25% + 20% = 75% of grade from written reports) continue the writing-heavy pattern.** The Coordination Failure Diagnosis Report, Comparative Evaluation Report, and MAS Architecture Specification collectively require 1,500-2,000+ words of technical writing. This leaves only 25% for demonstration of actual building skills.

4. **The 2.5-hour "hands-on alternative framework + benchmark" (Unit 4)** assumes students can set up, learn, and evaluate a new framework in that time. For CrewAI or AutoGen, just understanding the abstraction model and running a basic example could take 2 hours, leaving 30 minutes for meaningful benchmarking. The time estimate is aggressive.

5. **Distributed Cognition framing (Chapter 1)** may over-intellectualize the "why MAS" question for practical learners. Students need to understand "when should I use multiple agents instead of one?" — the answer is more about task decomposition and specialization than cognitive science metaphors.

### Time Budget Assessment

| Activity | Allocated | Realistic (CS student) | Realistic (Non-CS) | Notes |
|----------|-----------|----------------------|-------------------|-------|
| Unit 1: Readings + Videos | 1.5 hrs | 1.5 hrs | 2 hrs | MAS concepts are abstract |
| Unit 2: Quiz | 0.5 hrs | 0.5 hrs | 0.5 hrs | Fine |
| Unit 3: Guided Lab (LangGraph) | 2 hrs | 2 hrs | 3+ hrs | State graphs are complex |
| Unit 4: Alt Framework + Benchmark | 2.5 hrs | 2.5-3 hrs | 3.5-4 hrs | New framework setup alone is 1hr+ |
| Unit 5: Failure Diagnosis + Eval | 1 hr | 1 hr | 1.5 hrs | Requires completed lab work |
| Unit 6: Discussion + MAS Spec | 0.5 hrs | 0.5-1 hr | 1 hr | Spec is non-trivial |
| **Total** | **8 hrs** | **8-9.5 hrs** | **11.5-13 hrs** | **Significantly over budget for non-CS** |

### Concrete Recommendations

1. **(Critical) Resolve the Track A absence.** Recommended approach: Create a simplified Track A lab using Claude Code (or Claude Projects with multiple specialized system prompts simulating agents) that achieves the same learning objectives (coordination, specialization, communication) without requiring LangGraph proficiency. Offer it as the default path; make Track B the "advanced/CS-background" path.

2. **(Critical) Reduce scope of Unit 4.** The "learn a new framework AND benchmark it in 2.5 hours" requirement is unrealistic. Recommendation: Provide a pre-configured CrewAI notebook with a working multi-agent system. Students analyze and modify it rather than building from scratch. The benchmark becomes "compare this pre-built CrewAI system against your LangGraph lab" rather than "build two systems and compare." Time savings: ~1 hour.

3. **(High) Consolidate written deliverables.** Merge the Comparative Evaluation Report and Coordination Failure Diagnosis into a single "Multi-Agent System Analysis Report" with sections for:
   - Architecture comparison (LangGraph vs. alternative): 300 words
   - Failure mode identification and diagnosis: 300 words  
   - Performance benchmarking results: 200 words
   - Architectural recommendation: 200 words

   Total: 1,000 words, one report, covering both evaluation and failure diagnosis. Weight: 45%. This frees up time currently spent on report formatting and transitions.

4. **(High) Add explicit scaffolding for the LangGraph lab.** Before students touch code, provide a visual state graph diagram of what they are building. Non-CS students need the conceptual picture before the implementation details. Include: "Here is the system you will build. It has 3 agent nodes, 2 conditional edges, and a shared state. In the next 2 hours, you will implement each piece."

5. **(Medium) Simplify the Distributed Cognition framing.** Replace or supplement the cognitive science angle with a practical decision framework: "Use multiple agents when: (1) tasks require different expertise, (2) tasks can be parallelized, (3) you need checks and balances, (4) scale demands it." Keep the academic framing in readings but lead with practical heuristics.

6. **(Medium) Provide framework comparison table upfront.** Before students encounter AutoGen, CrewAI, or LangGraph in detail, provide a one-page comparison: "LangGraph = explicit state graphs, AutoGen = conversation-based coordination, CrewAI = role-based delegation." This orients students before they dive into implementation details.

7. **(Low) Consider making the MAS Architecture Specification (Unit 6) a capstone prep document** rather than a standalone graded artifact. If students are building toward the Module 5 capstone proposal, the MAS Spec could be framed as "draft the multi-agent section of your capstone" — reducing total unique deliverables while maintaining rigor.

## Module 5: "Responsible Agentic AI: Production Deployment, Evaluation, and Responsible AI"

**Time Budget:** 8 hours | **Status:** Needs deep review | **Review Depth:** Full analysis with concrete recommendations

### Critical Issue: Technical Complexity Mismatch with Audience

Module 5 covers:

- Docker containerization and Kubernetes orchestration
- API gateway patterns and autoscaling
- LangSmith and LangFuse observability platforms
- OpenTelemetry instrumentation
- CI/CD evaluation pipelines
- HELM benchmarking
- EU AI Act compliance mapping
- NIST Risk Management Framework

This is a DevOps/MLOps/Compliance survey course compressed into 8 hours. Each of these topics could be a module unto itself. For non-CS graduate students who have been building competency over 4 modules, this represents a dramatic escalation in both breadth and technical depth.

**The core tension:** Production deployment knowledge IS essential for responsible AI (you cannot govern what you cannot observe), but the depth required to meaningfully engage with Docker, Kubernetes, and OpenTelemetry far exceeds what 8 hours allows for non-technical students.

### Strengths

1. **Sculley's "Hidden Technical Debt" framing (Chapter 1)** is an excellent opening. It contextualizes everything that follows: production AI systems accumulate debt in monitoring, data pipelines, configuration, and serving infrastructure. Students understand WHY deployment matters, not just HOW.

2. **Multi-dimensional evaluation (Chapter 3)** is well-conceived. Moving beyond "accuracy" to encompass robustness, fairness, efficiency, and calibration gives students a mature evaluation vocabulary.

3. **The responsible AI thread reaches its culmination here.** EU AI Act and NIST RMF, introduced briefly in Module 1, receive full treatment. Students complete a risk register and gap analysis — genuine governance artifacts they could produce professionally.

4. **The capstone proposal (1,000 words)** provides satisfying course closure. Students synthesize across all five modules into a single coherent system proposal. The scope (1,000 words) is appropriately bounded.

5. **LLM-as-judge evaluation** is a timely and practical technique. Teaching students to use one LLM to evaluate another's output is immediately applicable to any AI deployment.

### Areas for Improvement

1. **Docker and Kubernetes depth is inappropriate for this audience.** Non-CS students do not need to understand container orchestration to be responsible AI practitioners. They need to understand THAT containerization exists and WHY it matters for reproducibility and isolation — not HOW to write Dockerfiles or configure Kubernetes deployments. Recommendation: Reduce from "production infrastructure" to "production infrastructure concepts" — a conceptual overview (30 min reading) rather than a hands-on engagement.

2. **OpenTelemetry is too low-level.** Students should understand observability as a concept and be able to interpret traces/metrics. They should NOT need to instrument code with OpenTelemetry spans. LangSmith provides a higher-level abstraction that is more appropriate for this audience. Recommendation: Focus on LangSmith as the primary observability tool; mention OpenTelemetry as "what LangSmith is built on" for context.

3. **The Lab A + Lab B structure (LangSmith observability + CI/CD pipeline) assumes functional Python environments** from Modules 2-4. If students struggled with earlier labs, they will be underwater here. There is no acknowledgment of accumulated technical debt in student experience.

4. **The 6-Dimension Evaluation Report (25%)** requires students to evaluate a system across six dimensions. If those dimensions are from HELM (accuracy, calibration, robustness, fairness, bias, toxicity), students need access to evaluation tooling or pre-computed results. The logistics are unclear — do students evaluate their own Module 4 systems? A provided system? The scope needs tightening.

5. **EU AI Act content will date quickly.** The Act is still being implemented with delegated acts and standards emerging through 2025-2027. Content should be framed as "the EU AI Act framework and compliance methodology" rather than specific article-level requirements that may shift.

6. **Writing load peaks here.** Three major deliverables plus the capstone:
   - 6-Dimension Evaluation Report (25%)
   - EU AI Act Governance Analysis (20%)  
   - Comprehensive Proposal / Capstone (30%)

   Students are producing their most sophisticated written work while simultaneously learning the most technically complex material. This is a peak-load problem.

7. **Time budget is impossible for the stated scope.** Even a senior DevOps engineer would find "Docker + Kubernetes + API gateways + autoscaling + LangSmith + LangFuse + OpenTelemetry + HELM + LLM-as-judge + CI/CD + EU AI Act + NIST RMF + capstone proposal" in 8 hours to be absurd. Something must be cut.

### Time Budget Assessment

| Activity | Allocated | Realistic (CS student) | Realistic (Non-CS) | Notes |
|----------|-----------|----------------------|-------------------|-------|
| Unit 1: Readings + Videos | 1.5 hrs | 2 hrs | 3 hrs | 5 dense technical chapters |
| Unit 2: Quiz | 0.5 hrs | 0.5 hrs | 0.5 hrs | Fine |
| Unit 3: Lab A (LangSmith) | ~1.5 hrs | 1.5 hrs | 2.5 hrs | Platform onboarding overhead |
| Unit 3: Lab B (CI/CD pipeline) | ~1.5 hrs | 1.5-2 hrs | 3+ hrs | CI/CD is alien to non-CS |
| Unit 4: NIST + EU AI Act Project | ~1.5 hrs | 1.5 hrs | 2 hrs | Research-heavy |
| Unit 5: 6-Dimension Evaluation | 1 hr | 1.5 hrs | 2 hrs | Complex analytical task |
| Unit 6: Discussion + Capstone | 0.5 hrs | 1-2 hrs | 2-3 hrs | 1000-word proposal needs time |
| **Total** | **8 hrs** | **10-11 hrs** | **15-17 hrs** | **Massively over budget for non-CS** |

### Concrete Recommendations

1. **(Critical) Radically reduce infrastructure scope.** Replace Chapters 2 (Production Infrastructure) with "Production Deployment Concepts for AI Practitioners" — a 45-minute reading that covers:
   - Why containerization matters (reproducibility, isolation) — conceptual only, no Dockerfiles
   - What orchestration does (scaling, fault tolerance) — conceptual only, no K8s YAML
   - API gateway patterns (rate limiting, authentication) — as a consumer, not implementer
   - The deployment spectrum: "Here's what your DevOps team handles; here's what you need to specify"

   **Time savings: ~2 hours** (eliminating hands-on infrastructure work students will never do without DevOps support).

2. **(Critical) Eliminate Lab B (CI/CD pipeline) or replace with conceptual exercise.** Non-CS students will not build CI/CD pipelines. Instead, provide a pre-built pipeline and have students:
   - Read and interpret the pipeline configuration (15 min)
   - Identify what each stage evaluates (15 min)
   - Propose one additional evaluation stage with justification (15 min)

   **Time savings: ~1 hour** while preserving the learning objective ("understand how evaluation integrates into deployment").

3. **(Critical) Reallocate saved time to the capstone proposal.** The current 30-minute allocation for a 1,000-word comprehensive proposal is fiction. Realistic time: 2-3 hours for research, outlining, drafting, and revision. With time savings from recommendations 1-2, allocate 2 hours explicitly to capstone development.

4. **(High) Focus observability on LangSmith only.** Remove OpenTelemetry and LangFuse from required content. Frame them as "additional resources for students with DevOps backgrounds." Lab A becomes purely LangSmith-focused: "Trace an agent's execution, identify a performance bottleneck, propose a fix." This is achievable for non-CS students using LangSmith's UI.

5. **(High) Restructure the 6-Dimension Evaluation Report.** Provide students with:
   - A pre-evaluated system with metrics across 6 dimensions
   - 3 of the 6 dimensions already analyzed (as examples)
   - Students complete the remaining 3 dimensions

   This reduces scope while maintaining analytical rigor. The scaffolding helps non-CS students understand the evaluation methodology before applying it independently.

6. **(Medium) Frame EU AI Act content as methodology, not memorization.** Rather than requiring students to map specific articles, teach them the COMPLIANCE METHODOLOGY:
   - How to determine an AI system's risk category
   - What documentation is required at each category
   - How to conduct a gap analysis (the process, not the specific gaps)

   This survives regulatory updates and teaches transferable governance skills.

7. **(Medium) Make the capstone proposal a living document that evolves from Module 3 onward.** If the MAS Architecture Specification (Module 4) and Memory Architecture Brief (Module 3) are framed as "sections of your capstone," students build the proposal incrementally rather than writing 1,000 words from scratch in Module 5. The Module 5 capstone becomes: "Integrate your previous work, add the evaluation and governance sections, write the executive summary." Time required drops from 3 hours to 1.5 hours.

8. **(Low) Add a "Production Readiness Checklist" template** that students complete for their capstone system. This is a practical artifact (1-page checklist: monitoring in place? Evaluation pipeline defined? Risk register completed? Rollback plan?) that synthesizes the module's learning without requiring deep technical implementation.

## Cross-Cutting Issues and Recommendations

### Issue 1: Overview vs. Content Misalignment (Modules 2, 3, 4)

**Pattern:** Module Overviews were apparently written to a course design centered on Claude Cowork, MCP, n8n, and Claude Code. The actual content was developed around LangChain, LangGraph, CrewAI, and Python/Colab. These are fundamentally different courses for different audiences.

**Root Cause Hypothesis:** The course was initially designed around Anthropic's tool ecosystem (Cowork, Claude Code, MCP) for a non-technical audience, then pivoted to open-source frameworks (LangChain/LangGraph) for technical depth, but the Overviews were never updated to reflect the pivot.

**Recommendation:** Conduct a systematic Overview rewrite for Modules 2-4. Each Overview should accurately describe:

- What students will learn (concepts)
- What students will build (activities)
- What tools they will use (technologies)
- What prerequisites are assumed (skills)

The Overviews should be written LAST, after content is finalized, to ensure alignment.

### Issue 2: Programming Prerequisite Escalation

**The stated promise:** No prior programming experience required for Modules 1-3; guided notebooks for Modules 4-5.

**The reality:**

- Module 1: No programming. Promise kept.
- Module 2: Python/LangChain in Colab. Promise broken.
- Module 3: RAG pipeline implementation in Python. Promise broken.
- Module 4: LangGraph state graphs. "Guided" but requires code comprehension.
- Module 5: LangSmith instrumentation, CI/CD pipelines. Deep technical engagement.

**Recommendation:** Either:

- **(Option A) Acknowledge the escalation honestly.** State upfront: "This course uses Python in Google Colab starting in Module 2. You will read and modify code, not write it from scratch. No prior experience is required, but comfort with structured text and logical thinking is essential." Add a 30-minute "Colab + Python Reading" orientation before Module 2.
- **(Option B) Create genuine no-code tracks.** For Modules 2-4, offer a Claude Cowork/Claude Code track that achieves the same conceptual learning objectives without Python. This is more work but honors the accessibility promise.

### Issue 3: Writing Load Imbalance

**Target ratio:** 60% doing / 25% reading / 15% writing

**Approximate actual ratios for Modules 3-5:**

- Module 3: 35% doing / 30% reading / 35% writing
- Module 4: 35% doing / 25% reading / 40% writing
- Module 5: 25% doing / 30% reading / 45% writing

The writing load escalates precisely as technical complexity increases, creating a compounding difficulty problem.

**Recommendation:** Apply a "one major deliverable per module" rule for Modules 3-5:

- Module 3: Memory Architecture Specification Brief (merge RAGAS interpretation into lab reflection)
- Module 4: Multi-Agent System Analysis Report (merge failure diagnosis and comparative evaluation)
- Module 5: Comprehensive Capstone Proposal (merge evaluation and governance into capstone sections)

Each module retains one substantial written deliverable plus lightweight lab reflections. Total unique graded writing artifacts per module drops from 3 to 1+reflections.

### Issue 4: Time Budget Realism

**Stated budget:** 8 hours per module

**Estimated realistic time for target audience (non-CS graduate students):**

- Module 1: 8-9 hours (acceptable)
- Module 2: 9-10 hours (slightly over)
- Module 3: 8.5-11 hours (problematic)
- Module 4: 11.5-13 hours (critically over)
- Module 5: 15-17 hours (impossible)

**Total course as designed:** 52-60 hours for non-CS students vs. 40 hours stated.

**Recommendation:** The cuts recommended in each module section above should bring totals closer to budget:

- Module 3: Reduce to ~8-9 hrs (consolidate deliverables, simplify unit structure)
- Module 4: Reduce to ~9-10 hrs (provide pre-built alternatives, consolidate deliverables, add Track A)
- Module 5: Reduce to ~9-10 hrs (eliminate infrastructure hands-on, simplify CI/CD, expand capstone time)

Accept that Modules 4-5 will run slightly over 8 hours for non-CS students. This is acceptable if students are warned and if the overage is in doing (lab work) rather than writing.

### Issue 5: Discussion Post Design Drift

**Module 1 design:** Traditional discussion post + reply. Clean, achievable in 30 minutes.

**Modules 3-5 design:** "Discussion posts" that are actually architecture brief presentations requiring peer review of technical specifications. These are not discussions — they are mini-deliverables dressed as discussions.

**Recommendation:** Decide what discussions are FOR in this course:

- **(Option A) Community building and reflection.** Keep them short (200 words), focused on experience sharing ("What surprised you about RAG evaluation?"), and separate from graded technical work.
- **(Option B) Peer review of technical work.** Rename them "Peer Review Exchanges," allocate appropriate time (45-60 min rather than 30 min), and grade on review quality rather than post quality.

Do not pretend technical peer review is a "discussion post" — the mismatch confuses time expectations.

### Issue 6: Tool Ecosystem Coherence

The course references these tools: Ollama, Openwork, Claude Cowork, Claude Code, n8n, Google Colab, LangChain, LangGraph, CrewAI, AutoGen, LangSmith, LangFuse, OpenTelemetry, Docker, Kubernetes, RAGAS, HELM.

**That is 16 distinct tools/platforms across 5 modules.** For non-CS students, each new tool carries onboarding overhead (account creation, UI learning, troubleshooting). The cognitive load of tool-switching may exceed the cognitive load of the actual content.

**Recommendation:** Establish a "core tool stack" and an "extended tool stack":

- **Core (all students):** Ollama, Claude Cowork, Google Colab, LangSmith
- **Extended (CS-background students):** LangChain, LangGraph, CrewAI, Docker, RAGAS
- **Reference only (conceptual understanding):** Kubernetes, OpenTelemetry, HELM, AutoGen, LangFuse, n8n

Students interact hands-on with 4 core tools. They use 5 extended tools in guided contexts. They learn ABOUT 6 additional tools conceptually. This tiering manages cognitive load while maintaining technical breadth.

## Summary of Priority Recommendations

### Must-Fix (Before Course Launch)

| # | Issue | Modules Affected | Effort |
|---|-------|-----------------|--------|
| 1 | Rewrite Overviews to match actual content | 2, 3, 4 | Medium (writing only) |
| 2 | Resolve programming prerequisite gap | 2, 3, 4, 5 | Medium (add orientation + acknowledge escalation) |
| 3 | Reduce Module 5 infrastructure scope | 5 | Medium (cut content, replace with conceptual overview) |
| 4 | Add Track A (Claude Code) activities or remove from Overview | 4 | High (create new lab) OR Low (edit Overview) |

### Should-Fix (Significantly Improves Quality)

| # | Issue | Modules Affected | Effort |
|---|-------|-----------------|--------|
| 5 | Consolidate writing deliverables (one major per module) | 3, 4, 5 | Medium (restructure assessments) |
| 6 | Add scaffolding for technical labs (visual diagrams, skill checks) | 3, 4, 5 | Low-Medium |
| 7 | Make capstone proposal incremental (built across Modules 3-5) | 3, 4, 5 | Medium (reframe existing deliverables) |
| 8 | Reduce Module 4 Unit 4 scope (pre-built alternative framework) | 4 | Medium (create notebook) |

### Nice-to-Have (Polish)

| # | Issue | Modules Affected | Effort |
|---|-------|-----------------|--------|
| 9 | Simplify unit structures in Modules 3-5 | 3, 4, 5 | Low |
| 10 | Add blast radius calibration examples | 1 | Low |
| 11 | Establish core/extended/reference tool tiering | All | Low (documentation) |
| 12 | Frame EU AI Act as methodology, not memorization | 5 | Low |

## Appendix: Ideal Module Structure Template

Based on the analysis above, the following structure best serves non-CS graduate students within an 8-hour budget:

```text
PHASE 1: PREPARE (2 hours)
- Readings: Conceptual chapters with clear learning objectives (1.5 hrs)
- Self-check: Brief comprehension verification (0.5 hrs)

PHASE 2: BUILD (4 hours)  
- Guided Lab: Step-by-step hands-on with clear deliverable (2 hrs)
- Independent Project: Apply lab skills to new context (2 hrs)

PHASE 3: SYNTHESIZE (2 hours)
- Written Deliverable: One substantial analytical artifact (1.5 hrs)
- Discussion/Peer Exchange: Community reflection or peer review (0.5 hrs)
```

**Ratio achieved:** 50% doing (Build phase) / 25% reading (Prepare phase) / 25% writing+discussion (Synthesize phase). This slightly exceeds the 15% writing target but is realistic given graduate-level expectations.

---

*Document prepared: 2026-07-31*
*Review scope: All Overview, Foundational Concepts, and Activities pages across 5 modules*
*Perspective: Sequential graduate student experience, non-CS background*

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Course-Review-Analysis-v1){target=_blank} (wiki page last changed 2026-08-19). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/course-design/course-review-2026-07.md){target=_blank}.</p>
