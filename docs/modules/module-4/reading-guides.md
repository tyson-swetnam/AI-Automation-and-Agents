---
title: Module 4 Reading Guides
description: 'Five reading guides (sources, key terms, guiding questions, critical-thinking prompts) for Module 4, Multi-Agent Systems: design, coordination, and evidence-based evaluation.'
type: Reading Guide
tags:
- module-4
- student-facing
- reading-guide
- multi-agent-systems
- langgraph
- crewai
- orchestration
module: 4
status: stable
stale_after: '2027-09-01T00:00:00Z'
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-4.2-Addendum
  title: 'AI Automation and Agents v2 wiki: Module-4.2-Addendum'
  author: Carlos Lizárraga-Celaya; Michelle Yung
  last_modified: '2026-08-12T12:32:11-07:00'
authorship:
  created: '2026-07-23'
  contributors:
  - C. Lizárraga
wiki_page: Module-4.2-Addendum
---
# Module 4 Reading Guides

These reading guides accompany the assigned sources for each chapter of Module 4. Work through the guiding questions as you read — they direct your attention to the concepts the chapter lessons, labs, and quizzes assess. Complete the extraction tasks embedded in each guide; they are the direct inputs to your lab notebook, role specification template, and framework comparison report.

## Reading Guide 1 — Chapter 1: Why Multi-Agent Systems Exist { #reading-guide-1 }

**Sources covered:**
- Guo, T., et al. (2024). Large language model based multi-agents: A survey of progress and challenges. *arXiv:2402.01680*. *(Section 3 — read; Section 4 — skim)*
- Wooldridge, M., & Jennings, N. R. (1995). Intelligent agents: Theory and practice. *The Knowledge Engineering Review, 10*(2), 115–152. *(Sociability property)*
- Hutchins, E. (1995). *Cognition in the Wild*. MIT Press. *(Distributed cognition framework)*
- Stone, P., & Veloso, M. (2000). Multiagent systems: A survey from a machine learning perspective. *Autonomous Robots, 8*(3), 345–383. *(Coordination and communication taxonomy)*

**Estimated study time:** ~15 minutes (Guo et al. Section 3) + ~10 minutes (targeted sections from Wooldridge & Jennings, Hutchins, Stone & Veloso)

**Chapter connection:** These sources collectively establish why multi-agent architecture exists as a distinct engineering discipline — not as a fashionable complexity, but as a principled response to specific task properties that single agents cannot handle well. Read Guo et al. Section 3 first; use the other sources to ground its claims in foundational theory.

### Overview

Guo et al. (2024) define LLM-based multi-agent systems as networks of individual language models that perceive inputs, reason about tasks, and take coordinated actions on complex, decomposable problems. Their survey documents where these systems succeed, where they fail, and — critically — when a single well-designed agent is the better architectural choice. This last point is as important as the first two: the five conditions that justify multi-agent architecture are not generic virtues; they are specific task properties, each of which makes the coordination cost worthwhile.

The theoretical foundations come from three decades of prior work. Wooldridge and Jennings (1995) identified sociability — the capacity of agents to interact with one another — as one of the four defining properties of agency. Hutchins (1995) showed that complex cognitive work in human organizations is routinely distributed across individuals and artifacts, with no single participant holding all relevant information. Stone and Veloso (2000) formalized the coordination mechanisms and communication protocols that enable multi-agent systems to work as coherent wholes. Guo et al. translate these theoretical foundations into the engineering vocabulary of LLM-based systems.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **Multi-agent system (MAS)** | A computational architecture in which multiple autonomous AI agents, each with distinct roles and capabilities, collaborate to accomplish tasks no single agent could handle efficiently alone |
| **Sociability** | Wooldridge & Jennings' fourth agent property: the capacity of an agent to interact with other agents using defined communication protocols — the foundational prerequisite for multi-agent coordination |
| **Distributed cognition** | Hutchins' (1995) framework: complex cognitive work is distributed across multiple actors and artifacts rather than concentrated in a single mind; a theoretical antecedent to MAS design |
| **Decomposability** | The property of a task that allows it to be divided into distinct sub-tasks that can be assigned to and executed by specialized agents independently or with managed dependencies |
| **Context window limitation** | A single agent's inability to process more information simultaneously than its context window allows — one of the five conditions that justify MAS |
| **Task specialization** | The condition where sub-tasks benefit from different expertise, prompting strategies, or tool sets — requiring specialized agents rather than a generalist |
| **Parallel execution** | The condition where independent sub-tasks can run simultaneously across multiple agents, reducing total task completion time |
| **Cross-agent quality control** | The condition where one agent generates output and a separate critic agent reviews it — a structural check-and-balance that a single agent cannot apply to its own output |
| **Coordination overhead** | The additional token cost, latency, and engineering complexity introduced by inter-agent communication — the price paid for MAS capabilities |
| **Inter-agent communication** | The mechanism by which agents exchange information, results, and instructions — ranging from shared state objects (LangGraph) to conversation messages (AutoGen) |

### Guiding Questions

#### Section A — Guo et al. (2024): Section 3 — LLM-Based Multi-Agent Systems

1. Guo et al. define LLM-based multi-agent systems as networks where individual language models "perceive inputs, reason about tasks, and take actions." What is the precise technical mechanism by which one LLM-based agent communicates with another? Identify the two primary communication modes described in the survey and explain when each is appropriate.

2. Section 3 identifies the conditions under which a multi-agent architecture is justified over a single-agent design. Restate each of the five conditions in the form: "When [task property], a MAS is justified because [causal mechanism]." This restatement forces you to identify not just what the condition is but why it makes MAS the appropriate choice.

3. Guo et al. note that "coordination adds cost and complexity, so it should only be considered when the task has specific requirements." What specific empirical evidence do they cite to support the claim that a poorly designed MAS can underperform a well-designed single agent? What task properties correlate most strongly with MAS underperformance?

4. Section 4 (skim) describes applications of LLM-based MAS across domains including software engineering, scientific research, and social simulation. For each domain, identify one specific task property (from the five-condition table in the chapter lesson) that makes multi-agent architecture appropriate. Do not list generic advantages — connect each application's specific structure to a specific condition.

5. Guo et al. identify agent communication as a key design decision in MAS architecture. What is the difference between a system where agents share a centralized state object and a system where agents exchange natural language messages? What are the debugging implications of each approach?

#### Section B — Foundational Theory: Wooldridge & Jennings, Hutchins, Stone & Veloso

6. Wooldridge and Jennings (1995) define sociability as the capacity to interact with other agents "using an agent communication language." In an LLM-based MAS, what serves as the agent communication language? How does this differ from the formal ACL (Agent Communication Language) frameworks of the 1995 era?

7. Hutchins (1995) argues that complex cognitive work in organizations is routinely distributed across individuals and artifacts. Identify one specific structural parallel between Hutchins' distributed cognition framework and the architecture of a LangGraph supervisor-worker system. Be precise: which component of the MAS corresponds to which element of Hutchins' model?

8. Stone and Veloso (2000) present a taxonomy of coordination mechanisms. Identify two coordination mechanisms from their taxonomy and map each to one of the four coordination architecture patterns described in Chapter 2. This mapping demonstrates that the contemporary MAS patterns are instantiations of principles established decades earlier.

### Critical Thinking Prompts

- Guo et al. argue that "a well-designed single agent will often outperform a poorly designed multi-agent system." What does this claim imply about the relationship between architectural choice and implementation quality? Is the five-condition justification table sufficient to determine whether MAS is warranted, or is it necessary but not sufficient?

- Hutchins' distributed cognition framework was developed to describe human organizations, not computational systems. What limitations arise when applying a human-organization framework to LLM-based MAS? Which aspects of human coordination does the framework illuminate for MAS design, and which aspects does it fail to predict?

## Reading Guide 2 — Chapter 2: How Do Agents Coordinate With One Another? { #reading-guide-2 }

**Sources covered:**
- Stone, P., & Veloso, M. (2000). Multiagent systems: A survey from a machine learning perspective. *Autonomous Robots, 8*(3), 345–383. *(Section 3 — coordination mechanisms)*
- Wu, Q., et al. (2024). AutoGen: Enabling next-gen LLM applications via multi-agent conversations. *First Conference on Language Modeling*. *(Coordination model)*
- Hong, S., et al. (2024). MetaGPT: Meta programming for a multi-agent collaborative framework. *ICLR 2024*. *(Sections 1–2 — role specification and pipeline architecture)*

**Estimated study time:** ~20 minutes (Hong et al. Sections 1–2) + ~15 minutes (Stone & Veloso Section 3) + ~15 minutes (Wu et al. coordination model sections)

**Chapter connection:** Hong et al.'s MetaGPT paper is Reading 3 — the primary source for this chapter. It provides a concrete instantiation of the role-based sequential pipeline pattern that directly informs your Lab B Role Specification template. Read it first; then use Stone & Veloso to situate the four patterns in classical MAS theory.

### Overview

The four coordination architecture patterns — Hierarchical Supervisor-Worker, Peer Collaboration Network, Role-Based Sequential Pipeline, and Market-Mechanism Allocation — are not stylistic choices. Each embeds specific assumptions about task decomposability, information flow, and failure tolerance. The wrong pattern for a task structure produces coordination failures that cannot be remediated by prompt engineering; they require architectural redesign. Hong et al.'s MetaGPT provides the defining implementation of the role-based sequential pipeline: a system where agents represent structured professional roles (product manager → architect → engineer → tester), each with precisely defined input-output interfaces. This design principle — role clarity, interface specification, handoff conditions — is the operational core of your Lab B deliverable.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **Hierarchical Supervisor-Worker** | Coordination pattern where a central supervisor holds full task context, decomposes the task, delegates to specialized workers, and synthesizes their outputs; centralized authority, top-down communication |
| **Peer Collaboration Network** | Coordination pattern where agents communicate horizontally with no central coordinator; global behavior emerges from collective interaction; used in AutoGen's conversation model |
| **Role-Based Sequential Pipeline** | Coordination pattern where each agent receives the prior agent's output as input and passes its own output forward; one-directional communication; used in MetaGPT |
| **Market-Mechanism Allocation** | Coordination pattern where tasks are posted to a shared queue and worker agents claim tasks based on capability and load; a broker mediates assignment; highest coordination overhead |
| **Input-output interface** | The precise specification of what data format an agent receives as input and produces as output — the contract between adjacent pipeline stages |
| **Handoff condition** | The criterion that determines when an agent's task is complete and its output ready to pass to the next agent — must be concrete and evaluable, not subjective |
| **Bottleneck** | A structural failure point in hierarchical patterns where the supervisor's processing speed or decomposition quality limits the entire system's throughput and correctness |
| **Emergent behavior** | Behavior in peer collaboration networks that is not specified in any individual agent's design but arises from the collective interaction of agents — difficult to predict and debug |
| **Contract net protocol** | A classical MAS coordination mechanism (Stone & Veloso) in which tasks are advertised and agents bid for them — the theoretical precursor to the market-mechanism allocation pattern |
| **Role specification** | The complete definition of an agent's responsibility, input format, output format, handoff condition, and position-specific failure modes — the design artifact that MetaGPT and Lab B both require |

### Guiding Questions

#### Section A — Hong et al. (2024): MetaGPT — Sections 1–2

1. MetaGPT defines agents as representing structured professional roles. What is the precise technical mechanism by which MetaGPT enforces role boundaries — preventing, for example, the architect agent from performing the work assigned to the engineer agent? How does this enforcement mechanism differ from relying on prompt instructions alone?

2. Each MetaGPT role has a defined input format and output format (a "schema"). Why does Hong et al. argue that specifying these schemas is necessary for reliable pipeline execution? What class of coordination failure occurs when input-output schemas are left implicit?

3. MetaGPT's pipeline flows from product manager → architect → engineer → tester. Map this sequence onto the Role-Based Sequential Pipeline pattern from the chapter lesson: identify which pattern properties (one-directional communication, sequential dependency, stage-level failure propagation) are instantiated in each stage transition of MetaGPT's design.

4. Hong et al. evaluate MetaGPT on software engineering benchmarks. What specific task properties of software engineering make the role-based sequential pipeline the appropriate coordination pattern? Would a peer collaboration network be a better choice for the same task — why or why not?

5. The MetaGPT paper describes a "shared message pool" that stores all agents' outputs for cross-reference. How does this shared message pool differ from the strict one-directional pipeline described in the chapter lesson's Pattern 3 definition? Does this make MetaGPT a hybrid of two patterns?

#### Section B — Stone & Veloso (2000): Section 3 — Coordination Mechanisms

6. Stone and Veloso define coordination as "the process by which an agent reasons about its local actions and the anticipated actions of others." How does this definition apply differently to the four coordination patterns? For which pattern is coordination most implicit (agents do not need to model others' actions explicitly), and for which is it most explicit?

7. The contract net protocol (Stone & Veloso) involves task advertisement, agent bidding, and broker assignment. How does the market-mechanism allocation pattern in modern LLM-based MAS implement or depart from the classical contract net protocol? What practical constraints of LLM-based agents (token cost, latency, no formal bidding language) modify its implementation?

8. Stone and Veloso distinguish between tightly coupled and loosely coupled multi-agent systems. Map each of the four coordination patterns onto this dimension: which patterns are tightly coupled, which are loosely coupled, and what implications does coupling level have for fault tolerance and system scalability?

#### Section C — Wu et al. (2024): AutoGen's Coordination Model

9. AutoGen's coordination model uses conversational message exchange rather than a structured state schema. What coordination pattern does this most closely resemble — hierarchical, peer collaboration, sequential pipeline, or market-mechanism? Justify your answer by mapping AutoGen's architecture to the pattern's defining properties.

10. AutoGen's termination condition is defined as a function applied to incoming messages (e.g., `is_termination_msg=lambda x: 'APPROVED' in x.get('content', '')`). What coordination risk does this termination mechanism introduce if the 'APPROVED' string appears in a context that does not represent genuine task completion?

### Critical Thinking Prompts

- The chapter lesson states that choosing the wrong coordination pattern "produces coordination failures that cannot be remediated by prompt engineering." Construct a concrete scenario where a practitioner applies the Hierarchical Supervisor-Worker pattern to a task that actually requires a Peer Collaboration Network, and describe the specific coordination failure that would result and why prompt revision cannot fix it.

- MetaGPT's role-based sequential pipeline was designed for software engineering tasks. Identify a professional workflow from your own domain where the same pattern would be appropriate, and one where it would be inappropriate, explaining the specific task-structure property that makes the pattern fit or fail in each case.

## Reading Guide 3 — Chapter 3: The Three Orchestration Frameworks — LangGraph, AutoGen, and CrewAI { #reading-guide-3 }

**Sources covered:**
- LangGraph Documentation: Multi-Agent Architectures and Multi-Agent Supervisor
- Wu, Q., et al. (2024). AutoGen: Enabling next-gen LLM applications via multi-agent conversations. *First Conference on Language Modeling*. *(Sections 1–3)*
- Guo, T., et al. (2024). Large language model based multi-agents: A survey of progress and challenges. *(Framework observability and debugging critique)*
- CrewAI Documentation
- Video 1: "Fully local multi-agent systems with LangGraph" — LangChain (~13 min)

**Estimated study time:** ~20 minutes (LangGraph docs — full read) + ~15 minutes (AutoGen Sections 1–3) + ~13 minutes (Video 1)

**Chapter connection:** The LangGraph documentation is the primary implementation reference for Unit 3 Lab A. Read it before the lab, not concurrently. Construct your five-API cheat sheet (StateGraph, add_node, add_edge, add_conditional_edges, compile) while reading — it is your most practical lab resource.

### Overview

The three frameworks — LangGraph, AutoGen, and CrewAI — embody different design philosophies about the fundamental architecture of multi-agent coordination. LangGraph externalizes state into a typed, shared schema and routes agent execution through a compiled graph with explicit conditional edges. AutoGen treats coordination as a conversation between agents, with routing determined by message content and termination conditions. CrewAI abstracts coordination behind natural-language role and goal definitions, trading implementation flexibility for development speed. These are not equivalent tools with different syntax — they reflect different tradeoffs between observability, customizability, and developer accessibility.

Guo et al. (2024) provide a critical lens: high-level framework abstractions can obscure coordination dynamics and make debugging difficult when systems fail. Their recommendation — full execution logging at every agent invocation, message pass, and state transition — directly motivates the structured logging requirement in Lab A Step A3 and the execution log analysis in Unit 5.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **StateGraph** | LangGraph's primary API object; a directed graph where nodes are agent functions and edges define execution flow; state is a shared TypedDict passed through all nodes |
| **TypedDict state schema** | LangGraph's mechanism for defining the shared state object — a typed Python dictionary whose fields are explicitly declared; every node reads from and writes to this shared object |
| **add_node()** | LangGraph API call that registers an agent function as a named node in the StateGraph |
| **add_edge()** | LangGraph API call that creates a deterministic directed edge between two nodes — always routes from source to target |
| **add_conditional_edges()** | LangGraph API call that creates a routing function — a Python function that inspects the current state and returns a string key indicating the next node |
| **compile()** | LangGraph API call that validates the graph structure and returns an executable application object |
| **AssistantAgent** | AutoGen's primary agent class; an LLM-backed agent with a defined system message; communicates via natural language messages |
| **UserProxyAgent** | AutoGen's human-proxy agent class; manages termination conditions and may initiate conversations or relay human input |
| **Conversation history** | AutoGen's implicit state model; context is maintained as a growing list of message objects rather than a typed state schema |
| **Process.sequential** | CrewAI's execution mode in which agents execute in a fixed order; equivalent to the role-based sequential pipeline pattern |
| **Observability** | The degree to which a framework exposes the internal state and communication trace of a running multi-agent system — critical for debugging and audit |
| **Conditional edge routing** | A LangGraph mechanism where a Python function inspects the current state and returns a string key that maps to the next node — enabling dynamic, state-dependent control flow |

### Guiding Questions

#### Section A — LangGraph Documentation: Multi-Agent Architectures and Multi-Agent Supervisor

1. LangGraph's documentation describes the StateGraph as the central architectural unit. What is the precise role of the state schema in LangGraph's execution model — what does it enable that would be impossible without a typed, shared state object? Trace the state object's lifecycle through a two-node supervisor-worker graph from graph initialization to final response.

2. The documentation distinguishes between `add_edge()` (deterministic) and `add_conditional_edges()` (dynamic). Provide a concrete example of a routing decision in a multi-agent system that requires conditional routing rather than deterministic routing, and explain why the conditional edge is architecturally necessary rather than a convenience.

3. The Multi-Agent Supervisor documentation describes a supervisor-worker pattern. In this pattern, the supervisor node calls an LLM to determine which worker to invoke next. What is the specific risk of letting the LLM decide routing, compared to implementing routing as a deterministic Python function? Under what conditions is LLM-based routing justified despite this risk?

4. LangGraph's `compile()` step validates graph structure before execution. What categories of structural errors does compilation catch at graph-definition time that would otherwise only fail at runtime? Why does catching errors at compile time (rather than runtime) matter for production deployments?

5. Construct your five-API cheat sheet based on the documentation: for each of the five core LangGraph API calls (StateGraph, add_node, add_edge, add_conditional_edges, compile), write: the API call syntax, what it does, one parameter that requires careful attention, and one common error associated with it.

#### Section B — AutoGen (Wu et al., 2024): Sections 1–3

6. AutoGen's architecture uses AssistantAgent and UserProxyAgent as its two primary agent types. What is the functional role of the UserProxyAgent in a pure automation context (human_input_mode='NEVER')? If there is no human in the loop, what does the UserProxyAgent actually do in the coordination sequence?

7. AutoGen maintains coordination through conversation history — a growing list of message objects shared across agents. Compare this to LangGraph's typed StateGraph: what does AutoGen's conversation model make easier for the developer, and what does LangGraph's explicit state schema make easier? For which framework is debugging a mid-execution routing failure easier, and why?

8. AutoGen's termination condition is implemented as a lambda function applied to incoming messages. What is the engineering trade-off between termination-by-message-content (AutoGen's approach) and termination-by-state-field (LangGraph's approach)? Which approach is more robust to unexpected agent outputs that accidentally trigger or fail to trigger termination?

#### Section C — Guo et al. (2024): Framework Observability Critique

9. Guo et al. recommend that "production deployments instrument multi-agent systems with full execution logging — recording every agent invocation, every message passed, and every state transition." What specific class of coordination failure is invisible without this logging? Give one concrete example of a failure that a developer would not be able to diagnose from the final output alone but would be immediately identifiable in a full execution log.

10. CrewAI's abstraction model allows agent roles and goals to be specified in natural language (e.g., `role='Researcher'`, `goal='Gather and summarize relevant information'`). What does this level of abstraction make difficult to control precisely, and what does it make easier? Under what deployment context would CrewAI's natural-language specification be preferable to LangGraph's explicit Python-based routing?

### Critical Thinking Prompts

- The Framework Comparison Report requires you to compare LangGraph and your chosen alternative framework on four dimensions: implementation verbosity, observability, customization flexibility, and developer experience. Which of these four dimensions is most important for a production deployment in a regulated enterprise context (e.g., healthcare, finance), and what evidence from the documentation supports your ranking?

- LangGraph's compilation step validates graph structure but cannot validate the semantic correctness of agent behavior — it cannot check whether a supervisor LLM will actually route correctly, or whether a specialist agent will produce output in the expected format. What does this limitation imply about the adequacy of unit testing for LangGraph systems? What additional testing methodology is required?

## Reading Guide 4 — Chapter 4: Coordination Failure Taxonomy — Four Failure Modes, Four Structural Causes { #reading-guide-4 }

**Sources covered:**
- Cemri, M., et al. (2026). Why do multi-agent LLM systems fail? *Advances in Neural Information Processing Systems, 38*. *(Sections 1 and 4 — MAST taxonomy)*
- Wooldridge, M., & Jennings, N. R. (1995). Intelligent agents: Theory and practice. *(Coordination and cooperation sections)*
- Stone, P., & Veloso, M. (2000). Multiagent systems: A survey from a machine learning perspective. *(Section 3 — coordination mechanisms)*
- Wu, Q., et al. (2024). AutoGen. *(Failure analysis sections)*

**Estimated study time:** ~20 minutes (Cemri et al. Sections 1 and 4) + ~15 minutes (targeted sections from Wooldridge & Jennings, Stone & Veloso)

**Chapter connection:** Cemri et al. (2026) is Reading 5 — the primary source for this chapter. Their MAST (Multi-Agent System Failure Taxonomy) framework is the diagnostic instrument you will apply in Unit 5's coordination failure diagnosis task. Read Sections 1 and 4 carefully; the 14 failure modes and 3 categories are the vocabulary your diagnosis report must use.

### Overview

Cemri et al. (2026) introduce MAST (Multi-Agent System Failure Taxonomy) to address a systematic gap in the MAS literature: most work describes what multi-agent systems can do, but few papers systematically classify how and why they fail. MAST organizes 14 unique failure modes into three categories: (i) system design issues — failures arising from flawed architectural choices; (ii) inter-agent misalignment — failures arising from miscommunication or conflicting objectives between agents; and (iii) task verification failures — failures in the mechanisms that check whether sub-tasks were completed correctly before handoff. Crucially, coordination failures are structurally caused — they arise from mismatches between the coordination architecture and the task's actual dependency structure. This means they cannot be fixed by revising agent prompts; they require architectural intervention.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **MAST** | Multi-Agent System Failure Taxonomy (Cemri et al., 2026); a systematic classification of 14 failure modes organized into 3 categories |
| **System design issue** | MAST Category 1: failures arising from flawed architectural choices — including incorrect coordination pattern selection, malformed state schemas, and missing termination conditions |
| **Inter-agent misalignment** | MAST Category 2: failures arising from agents pursuing conflicting goals, misinterpreting handoff outputs, or communicating in incompatible formats |
| **Task verification failure** | MAST Category 3: failures in the mechanisms that validate whether a sub-task's output meets the quality standard required for handoff to the next stage |
| **Architectural cause** | The structural property of the coordination design (routing logic, state schema, termination condition, agent role boundary) that is the root cause of a coordination failure — distinct from prompt quality or model capability |
| **Structural intervention** | A remedy that changes the coordination architecture — routing logic, state schema fields, termination conditions, agent role boundaries — rather than agent prompt content |
| **Semantic drift** | An inter-agent misalignment failure where the meaning of a shared concept progressively diverges across agents' internal representations over a multi-turn interaction |
| **Cascading failure** | A failure mode in sequential pipelines where an error at one stage propagates and amplifies through all subsequent stages, producing a final output that is corrupted far beyond the original error |
| **Infinite loop** | A coordination failure where a revision cycle (e.g., critic → analyst → critic) has no termination condition, causing the system to run indefinitely or until a token budget is exhausted |
| **Role boundary violation** | An inter-agent misalignment failure where an agent performs work outside its defined role, either producing output in the wrong format or making decisions that belong to another agent |
| **Execution log** | A structured record of every agent invocation, state transition, and message exchange in a MAS execution — the primary diagnostic instrument for coordination failure analysis |

### Guiding Questions

#### Section A — Cemri et al. (2026): Sections 1 and 4 — MAST Taxonomy

1. Cemri et al. organize MAST failures into three categories: system design issues, inter-agent misalignment, and task verification failures. For each category, identify the pipeline design phase at which preventive interventions are most effective — design time, implementation time, or runtime — and justify your answer.

2. The chapter lesson emphasizes that coordination failures "require architectural intervention" and "cannot be fixed by prompt engineering." Using the MAST taxonomy's three categories, explain why this claim holds for each category. For which category is the boundary between a "prompt fix" and a "structural fix" most ambiguous, and why?

3. MAST identifies task verification failures as a distinct category. What specific mechanism is missing when a task verification failure occurs — what should the architecture provide that it does not? Design one concrete structural mechanism that would prevent a task verification failure in a sequential three-stage pipeline.

4. Section 4 of Cemri et al. describes the MAST-Data methodology — a systematic approach to classifying execution failures using the 14-mode taxonomy. What evidence does the paper provide for the claim that these 14 modes cover a comprehensive range of real-world MAS failures? What methodology was used to validate the taxonomy's coverage?

5. Cemri et al. distinguish "system design issues" from "inter-agent misalignment." A critic agent in a three-role pipeline (Researcher → Analyst → Critic) repeatedly rejects the analyst's output using inconsistent evaluation criteria. Under the MAST taxonomy, is this failure best classified as a system design issue or an inter-agent misalignment? Justify your classification using the precise MAST category definitions.

#### Section B — Classical Theory: Wooldridge & Jennings and Stone & Veloso

6. Wooldridge and Jennings (1995) define cooperation as "agents acting together to achieve a shared goal" and coordination as "managing the interdependencies among agents' activities." In a supervisor-worker LangGraph system, provide one concrete example of a cooperation failure (agents not working toward the shared goal) and one coordination failure (interdependencies not managed correctly). Are these the same failure?

7. Stone and Veloso (2000) describe the "joint intentions" problem: for agents to coordinate effectively, they must share not just goals but also a model of each other's intentions and capabilities. How does this problem manifest as an inter-agent misalignment failure in an LLM-based MAS? Specifically, what happens when two agents have different implicit assumptions about the format of the handoff output?

8. Stone and Veloso identify "coherence" — the global behavior of the system appearing consistent and coordinated from an outside observer — as a key MAS property. What specific MAST failure mode most directly threatens system coherence, and what structural mechanism (from LangGraph's API) most directly enforces it?

### Critical Thinking Prompts

- The MAST taxonomy classifies 14 failure modes, but a given execution failure may exhibit characteristics of multiple categories simultaneously. Design a concrete MAS failure scenario that implicates all three MAST categories simultaneously, and describe the minimal set of structural interventions required to address all three simultaneously.

- The chapter lesson states that diagnosing coordination failures requires reading the execution log rather than the agent prompts or configuration. What specific information in the execution log allows a practitioner to distinguish a system design issue (Category 1) from an inter-agent misalignment (Category 2) when both produce similar observable symptoms (e.g., incorrect final output)?

## Reading Guide 5 — Chapter 5: Evidence-Based Benchmarking — When Does Multi-Agent Add Value? { #reading-guide-5 }

**Sources covered:**
- Wu, Q., et al. (2024). AutoGen: Enabling next-gen LLM applications via multi-agent conversations. *(Evaluation sections)*
- Hong, S., et al. (2024). MetaGPT. *(Evaluation and benchmarking methodology)*
- Guo, T., et al. (2024). Large language model based multi-agents: A survey. *(Critical evaluation methodology)*
- Video 2: "AutoGen Tutorial" — Matthew Berman (~20 min)

**Estimated study time:** ~20 minutes (AutoGen evaluation sections + Video 2) + ~15 minutes (MetaGPT evaluation methodology)

**Chapter connection:** The benchmarking methodology in this chapter is directly operationalized in Unit 4 Task 2, which produces the Benchmark Results Table you will analyze in Unit 5 Part B. Read the evaluation sections of AutoGen and MetaGPT before Task 2 — not after — so that your experimental design is informed by published benchmarking practice.

### Overview

The central question of Chapter 5 is empirical: for a given task class, does a multi-agent system produce demonstrably better outcomes than a single advanced agent — and at what cost? This question cannot be answered by architectural reasoning alone; it requires controlled measurement across four dimensions: task accuracy, total token cost, wall-clock latency, and coordination overhead ratio. The coordination overhead ratio — (Multi-Agent Tokens − Single-Agent Tokens) / Single-Agent Tokens — is the quantitative expression of the fundamental MAS trade-off: what coordination capability costs in token terms relative to the single-agent baseline.

Wu et al.'s AutoGen paper and Hong et al.'s MetaGPT paper both provide benchmarking methodology examples. Guo et al. provide a critical perspective on these benchmarks, noting that many published MAS evaluations are conducted on tasks specifically selected to favor multi-agent architectures — making their positive conclusions less generalizable than they appear.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **Coordination overhead ratio** | (Multi-Agent Tokens − Single-Agent Tokens) / Single-Agent Tokens, expressed as a percentage; quantifies the token cost of inter-agent communication relative to the single-agent baseline |
| **Task accuracy rubric** | A defined scoring scale (1–5 in Module 4) for evaluating output quality: 1=incorrect/hallucinated; 2=partially correct; 3=correct but incomplete; 4=complete; 5=complete, well-structured, and evidence-grounded |
| **Wall-clock latency** | The elapsed time from first agent invocation to final response delivery — includes all inter-agent communication, LLM inference calls, and state transitions |
| **Single-agent ReAct baseline** | A single advanced ReAct agent using the same underlying LLM as the multi-agent pipeline — the controlled comparison condition for benchmarking MAS value |
| **Implementation verbosity** | A framework comparison dimension: the number of lines of code and configuration complexity required to implement equivalent functionality in each framework |
| **Observability** | A framework comparison dimension: the ease and completeness with which a framework exposes inter-agent communication, state transitions, and routing decisions |
| **Customization flexibility** | A framework comparison dimension: the ease of modifying routing logic, termination conditions, and agent behavior — particularly for adding conditional revision cycles |
| **Qualified recommendation** | An evidence-based conclusion that states whether MAS is warranted for the tested task class, cites specific metric values, acknowledges limiting conditions, and specifies threshold values that would change the recommendation |
| **Selection bias in benchmarks** | Guo et al.'s critique: MAS evaluations tend to be conducted on tasks specifically chosen because they decompose well into sub-tasks — producing results that overstate MAS generalizability |
| **Coordination overhead breakeven** | The task accuracy improvement at which the coordination overhead ratio is justified; if MAS accuracy > single-agent accuracy by less than [threshold], the coordination cost is not worthwhile |

### Guiding Questions

#### Section A — Wu et al. (2024): AutoGen Evaluation Sections

1. AutoGen's evaluation demonstrates performance improvements on code generation and mathematical problem-solving tasks. What specific task properties of code generation make it a favorable benchmark for multi-agent evaluation? Would the same performance advantage be expected on a task without those properties — for example, writing a single-topic essay? Justify your prediction.

2. The AutoGen paper benchmarks multi-agent performance against a single-agent baseline using the same underlying model. What is the precise purpose of holding the model constant in this comparison? What would the benchmark measure if the multi-agent system used a more powerful model than the single-agent baseline?

3. AutoGen's evaluation section reports both accuracy improvements and token cost increases. What does the ratio of accuracy improvement to token cost increase tell a practitioner about the practical value of multi-agent orchestration? If accuracy improves by 10% but token cost increases by 300%, what conditions would justify accepting this trade-off?

#### Section B — Hong et al. (2024): MetaGPT Evaluation and Benchmarking Methodology

4. MetaGPT is evaluated on HumanEval and SWE-bench — established software engineering benchmarks. Why does the choice of evaluation benchmark affect the generalizability of conclusions about MAS value? What property of HumanEval and SWE-bench specifically favors a sequential pipeline architecture?

5. MetaGPT's evaluation compares its multi-agent pipeline against single-agent GPT-4 and against other MAS frameworks (e.g., ChatDev). What is the methodological advantage of comparing against other MAS frameworks, beyond comparing only against a single-agent baseline?

#### Section C — Guo et al. (2024): Critical Evaluation Methodology

6. Guo et al. identify "selection bias" as a common problem in published MAS evaluations: benchmark tasks are chosen because they decompose well into sub-tasks, producing results that favor multi-agent architectures. Describe one concrete strategy for designing a benchmark that is resistant to this selection bias. What properties should the benchmark task set include to ensure that the evaluation is genuinely diagnostic?

7. The chapter lesson specifies that the Comparative Evaluation Report requires "a specific, evidence-based recommendation — not a 'both approaches have merits' conclusion." What is the analytical difference between a qualified recommendation and a hedge? Write one example of each for the following result: multi-agent pipeline scores 4.1/5 accuracy vs. single agent's 3.8/5 accuracy, with a coordination overhead ratio of 280%.

8. The coordination overhead ratio measures the token cost of coordination relative to the single-agent baseline. What additional cost dimensions are not captured by the coordination overhead ratio but are relevant to a production deployment decision? Name at least two and explain how they would be measured.

### Critical Thinking Prompts

- Guo et al.'s critique of selection bias implies that most published results showing MAS outperforming single agents should be interpreted with caution. Does this mean that practitioners should default to single-agent architectures unless there is overwhelming empirical evidence for MAS? Or does the five-condition justification table (Chapter 1) provide sufficient non-empirical grounds for MAS selection in certain cases?

- The Unit 4 Task 2 benchmark uses a single task instance run once for each configuration. What are the statistical limitations of a single-instance benchmark? What sample size and experimental design would be required to produce conclusions with sufficient statistical power to support a production deployment recommendation?

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-4.2-Addendum){target=_blank} (wiki page last changed 2026-08-12). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-4/reading-guides.md){target=_blank}.</p>
