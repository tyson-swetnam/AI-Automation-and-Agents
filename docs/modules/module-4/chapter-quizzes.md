---
title: Module 4 Chapter Quizzes
description: Five self-evaluating five-question chapter quizzes with collapsed answer keys and per-option feedback for Module 4, Multi-Agent Systems.
type: Assessment
tags:
- module-4
- student-facing
- quiz
- multi-agent-systems
- langgraph
- crewai
- orchestration
- self-assessment
- answer-key
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
# Module 4 Chapter Quizzes

These quizzes are self-evaluating. For each question, select your answer, then read the feedback section immediately below. Feedback is provided for every option so you can diagnose your reasoning, not just verify your answer. Each quiz counts 20% of the Module 4 grade.

Each quiz has **5 questions**. Two attempts are permitted; your best score is retained.

## Chapter 1 Quiz — Why Multi-Agent Systems Exist { #chapter-1-quiz }

*Based on Reading Guide 1: Guo et al. (2024), Wooldridge & Jennings (1995), Hutchins (1995), Stone & Veloso (2000)*

### Question 1

Guo et al. (2024) define LLM-based multi-agent systems as networks of agents that "perceive inputs, reason about tasks, and take actions" on complex, decomposable problems. A project manager asks whether to use a multi-agent system for drafting a one-page executive briefing. Which analysis most correctly applies Guo et al.'s framework?

A. A multi-agent system is appropriate because LLMs work best when their roles are divided — a researcher, a writer, and an editor are always better than a single generalist.

B. A multi-agent system is likely not justified for this task: a one-page briefing does not exceed a single agent's context window, does not require parallel execution, and can be drafted and critiqued within a single advanced agent's ReAct loop — coordination overhead would add latency and token cost with no measurable quality benefit.

C. A multi-agent system is appropriate because the briefing involves multiple domains of knowledge, which justifies task specialization even for short documents.

D. The decision cannot be made without knowing the underlying LLM's context window size, since context window capacity is the primary criterion for MAS selection.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Guo et al. are explicit that MAS "should only be considered when the task has specific requirements that a single agent cannot handle well." A one-page executive briefing satisfies none of the five justification conditions: (1) it does not exceed any modern LLM's context window; (2) while writing involves multiple skills, a capable LLM can handle drafting and self-critique in a single pass; (3) there are no independent sub-tasks that would benefit from parallelization; (4) cross-agent quality control adds value only when the single-agent critique mechanism is demonstrably insufficient; and (5) the scale does not exceed single-agent capability. Adding a MAS for this task introduces coordination overhead — additional token cost, latency, and engineering complexity — for no measurable quality return.

    ❌ **A is incorrect.** The claim that "specialized agents are always better than a single generalist" directly contradicts Guo et al.'s position. The paper explicitly states that "a well-designed single agent will often outperform a poorly designed multi-agent system." Role division is beneficial only when the task structure makes specialization necessary — not as a default architectural preference.

    ❌ **C is incorrect.** Involving multiple knowledge domains is not itself a justification for MAS. A capable LLM integrates knowledge across domains by design. Task specialization is justified when sub-tasks require "different expertise, prompting strategies, or tool sets" that a generalist cannot handle reliably — not merely when a task involves more than one topic.

    ❌ **D is incorrect.** While context window capacity is one of the five justification conditions, it is neither the only condition nor the "primary" criterion. Many tasks that exceed a single agent's context window are still better handled by document chunking within a single agent than by a MAS. The full five-condition analysis is required, and this task fails all five conditions regardless of context window size.

### Question 2

Wooldridge and Jennings (1995) identify sociability as one of the four defining properties of an intelligent agent. In an LLM-based multi-agent system, which mechanism most directly implements sociability?

A. The agent's ability to generate fluent natural language responses to user queries — a prerequisite for communicating with humans and other agents.

B. The agent's capacity to exchange structured messages, shared state updates, or tool call results with other agents in the system, enabling coordinated action toward a shared objective.

C. The agent's access to the internet and external APIs, which allows it to gather information on behalf of the multi-agent system.

D. The agent's instruction-following capability — the ability to execute tasks specified by a supervisor agent without requiring clarification.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Wooldridge and Jennings define sociability as the capacity to interact with other agents "using an agent communication language" — a formal or structured mechanism that enables agents to exchange information, coordinate actions, and work toward shared goals. In LLM-based MAS, sociability is implemented through: shared state schemas (LangGraph, where agents read from and write to a typed state object), natural language message exchange (AutoGen, where agents communicate via conversational messages), or structured role handoffs (MetaGPT and CrewAI, where agents pass structured outputs to the next stage). The defining feature is not the communication medium but the capacity for inter-agent coordination toward shared objectives.

    ❌ **A is incorrect.** Generating fluent natural language is a property of the underlying LLM — it is present in any LLM-based system, including single-agent systems, regardless of whether the system is multi-agent. Sociability is specifically about inter-agent communication, not communication with human users, and is not reducible to language generation capability.

    ❌ **C is incorrect.** External API access is a tool-use capability — it relates to what Wooldridge and Jennings call "pro-activeness" (taking initiative to gather information) or the agent's action repertoire. It is not sociability. An agent can have extensive tool access without any capacity for inter-agent communication, and vice versa.

    ❌ **D is incorrect.** Instruction-following describes the agent's responsiveness to a supervisor's directives — a property that partially overlaps with reactivity (responding to environmental inputs) but is not sociability. Sociability requires bidirectional communication and coordination capability, not merely the ability to follow instructions received from above.

### Question 3

A research team needs to analyze 500 scientific papers to produce a comprehensive literature review. Each paper must be read, summarized, and its key claims extracted before cross-paper synthesis can begin. Which condition from Guo et al.'s five-condition table most precisely justifies a multi-agent architecture for this task?

A. Task specialization — because no single model can both summarize individual papers and synthesize across them, so each sub-task needs its own specialist agent.

B. Context window limitation — because 500 papers cannot be loaded simultaneously into a single agent's context window, requiring multiple agents to process distinct paper subsets in parallel before synthesis.

C. Cross-agent quality control — because the task specification requires a separate critic agent to verify each paper summary before synthesis.

D. Scale beyond single-agent capability — because 500 papers is a high-volume task that no single agent can complete in a reasonable time.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The most precise and necessary justification is context window limitation: even the longest-context LLMs available cannot process 500 full scientific papers simultaneously. This is a hard architectural constraint — no amount of prompt engineering or model capability resolves it within a single-agent architecture. Multiple agents must process distinct paper subsets, and their outputs must be aggregated. This is the condition that makes MAS not merely preferable but structurally necessary for this task. The condition is both necessary (the task cannot be done single-agent) and sufficient (it directly motivates parallel agent execution across document subsets).

    ❌ **A is incorrect.** Its premise is false: one capable model can summarize a paper and also synthesize across papers; the two sub-tasks call for different prompts, not different models. Task specialization can improve quality, but it does not make a multi-agent design necessary here. What does is the hard limit in B: 500 full papers cannot fit into any single agent's context window.

    ❌ **C is incorrect.** The task as described asks for no verification step, so a critic cannot be what justifies the architecture. A critic agent might well improve the summaries, but that would make a multi-agent design better, not necessary. The constraint the task does impose — all 500 papers read and summarized before synthesis — is one no single context window can hold.

    ❌ **D is incorrect as the primary justification.** "Scale beyond single-agent capability" is a real condition in the table, but its most precise meaning is workload volume that requires distribution, not just time. For 500 papers, context window limitation is the more precise and structurally primary constraint — the task literally cannot fit in one context window, which is a more fundamental constraint than execution speed alone.

### Question 4

Hutchins (1995) argues in *Cognition in the Wild* that complex cognitive work in human organizations is routinely distributed across individuals and artifacts, with no single participant holding all relevant information. Which structural property of a LangGraph supervisor-worker system most directly instantiates Hutchins' distributed cognition model?

A. The supervisor agent uses an LLM to reason, which distributes cognition across the LLM's billions of parameters — a form of distributed representation analogous to distributed organizational knowledge.

B. The shared state schema distributes information across all agents — no single agent holds the full task context simultaneously; the supervisor holds decomposition results, each worker holds only its sub-task, and the final response is assembled from all agents' contributions.

C. The LangGraph framework itself distributes computation across multiple CPU cores during graph compilation, paralleling how human organizations distribute physical labor.

D. The conditional edge routing function distributes decision-making between the supervisor agent and the Python runtime — a form of human-machine cognitive distribution.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Hutchins' key insight is that cognition is distributed across participants and artifacts — no single participant holds all the information needed for the task; knowledge is partitioned across roles, documents, and tools. In a LangGraph supervisor-worker system, this maps precisely to the state schema: the supervisor holds the decomposed task structure but not the specialist knowledge; each worker holds deep knowledge in its domain but not the global task context; the final response is synthesized from all agents' contributions. No single agent holds the complete picture at any point — the "intelligence" of the system is distributed across the state object and the agents that read from and write to it. This structural parallel is why Hutchins' 30-year-old organizational theory remains analytically relevant to contemporary MAS design.

    ❌ **A is incorrect.** Hutchins' distributed cognition refers to knowledge distributed across distinct cognitive actors and artifacts in a social system — not to internal distributed representation within a single computational device. The distribution of information across LLM parameters is a model architecture property, not an instantiation of distributed cognition in Hutchins' sense.

    ❌ **C is incorrect.** Parallel CPU execution is a hardware-level computational property, not a cognitive or organizational distribution in Hutchins' sense. Hutchins is analyzing how knowledge and cognitive work are divided across socially distinct agents — not how computation is parallelized within a single machine.

    ❌ **D is incorrect.** The conditional edge routing function distributes control flow between the supervisor's LLM output and the Python runtime's routing logic — this is a software architecture property, not a cognitive distribution in Hutchins' sense. The division of decision-making between an LLM and a Python function is not analogous to the organizational distribution of knowledge across individuals with distinct roles and information access.

### Question 5

Guo et al. (2024) state that "coordination adds cost and complexity, so it should only be considered when the task has specific requirements that a single agent cannot handle well." A practitioner implements a four-agent system for a task that a single ReAct agent handles with 92% accuracy. The multi-agent system achieves 94% accuracy but requires 340% more tokens. Which response most correctly applies Guo et al.'s framework to this result?

A. The multi-agent system is clearly superior because it achieves higher accuracy, and accuracy is the primary criterion for production deployment.

B. The result is ambiguous and requires additional context: the 2-percentage-point accuracy gain must be evaluated against the deployment context's cost sensitivity, latency requirements, and whether the accuracy gain exceeds the threshold that justifies 340% coordination overhead in this specific use case.

C. The multi-agent system should be rejected because any coordination overhead ratio above 100% is economically unjustifiable in professional deployment.

D. The multi-agent system is clearly inferior because the 340% token increase exceeds the 2-point accuracy gain on any reasonable cost-benefit metric.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Guo et al.'s framework does not provide a universal threshold at which coordination overhead is or is not justified — it requires contextual analysis. A 2-point accuracy improvement (92% → 94%) with 340% coordination overhead might be justified in a high-stakes domain where every accuracy point has significant monetary or safety value (e.g., medical diagnosis, legal document review), but unjustified in a low-stakes context where the token cost directly translates to prohibitive API expense. The qualified recommendation the module requires must state the conditions under which the conclusion holds and the threshold values that would shift it — not simply compare raw numbers. This is what Guo et al. mean by evidence-based evaluation: context determines value, not absolute metric values.

    ❌ **A is incorrect.** Treating accuracy as the sole criterion ignores the coordination overhead ratio entirely. Guo et al. explicitly frame MAS evaluation as a cost-benefit analysis where token cost, latency, and engineering complexity are legitimate production constraints that must be weighed against accuracy gains.

    ❌ **C is incorrect.** There is no universal coordination overhead threshold in Guo et al.'s framework. A 340% overhead might be completely acceptable in a use case where the task runs once per week and the single-agent cost is trivially small. The threshold for acceptability is deployment-context-specific, not architecturally universal. The Chapter 5 lesson's 40% rule of thumb does not contradict this. It applies to a different number, the coordination share — the fraction of a multi-agent system's own tokens that go to coordination — and it tells you where to look for waste, not whether the system is justified.

    ❌ **D is incorrect** as a categorical claim. Declaring the system "clearly inferior" requires a cost-benefit conclusion that is necessarily context-dependent. In a domain where a 2-point accuracy gain prevents costly errors — a medical screening system, a fraud detection pipeline — the economics may clearly favor the multi-agent approach. "Clearly inferior" is the kind of unqualified conclusion that Guo et al.'s critical evaluation framework is designed to prevent.

## Chapter 2 Quiz — How Do Agents Coordinate With One Another? { #chapter-2-quiz }

*Based on Reading Guide 2: Hong et al. (2024) MetaGPT, Stone & Veloso (2000), Wu et al. (2024) AutoGen*

### Question 1

A software development team implements a multi-agent system using the Role-Based Sequential Pipeline pattern (Researcher → Analyst → Critic). During a production run, the researcher agent produces a well-structured output, but the analyst agent fails to parse it correctly and produces a malformed analysis. The critic agent then approves the malformed analysis because its evaluation criteria do not check structural validity. Which MAST-aligned failure mode does this scenario most precisely represent?

A. A system design issue — the pipeline lacks a structural validation mechanism (an input schema check) between the researcher and analyst stages, allowing a parsing failure to propagate unchecked through all subsequent stages.

B. An inter-agent misalignment — the analyst agent lacks sufficient intelligence to parse complex researcher outputs, indicating that a more capable LLM should be used at the analyst stage.

C. A task verification failure at the researcher stage — the researcher agent should have verified that its output was parseable before passing it forward.

D. A coordination pattern mismatch — a sequential pipeline is the wrong architecture for this task, which should use a Hierarchical Supervisor-Worker pattern to provide centralized quality control.

??? success "Show answer and feedback"

    **Correct Answer: A**

    ✅ **A is correct.** This is a system design issue in the MAST taxonomy: the architecture lacks a structural mechanism — a schema validation step or a typed input-output interface between stages — that would catch the parsing failure before it propagates. In a correctly designed sequential pipeline, each stage transition includes a handoff condition check (the criterion that determines readiness to pass forward). The absence of this check is an architectural gap, not a prompt engineering problem or a model capability problem. The structural fix is to add an explicit validation node between the researcher and analyst stages — a lightweight node that applies the analyst's expected input schema to the researcher's output and routes to an error handler if validation fails. This is a structural intervention, not a prompt revision.

    ❌ **B is incorrect.** Attributing the failure to insufficient model intelligence is the wrong diagnostic category. The parsing failure occurred because the system has no mechanism to detect or handle it — not necessarily because the analyst LLM is incapable of parsing the output. Even a highly capable LLM will misinterpret an unexpectedly formatted input without explicit parsing guidance. The failure is structural (no validation step), not capability-based.

    ❌ **C is incorrect.** Requiring the researcher to verify that its output is parseable by the analyst conflates two agents' responsibilities. The researcher's role is to produce well-structured research output; verifying parseability from the analyst's perspective requires the researcher to model the analyst's input schema — a role boundary violation that adds complexity without addressing the root structural gap. The correct fix is an inter-stage validation node, not expansion of the researcher's responsibility.

    ❌ **D is incorrect.** Switching to a Hierarchical Supervisor-Worker pattern would address the failure only if the supervisor were responsible for validating each stage's output before passing it forward — which the description does not guarantee. More importantly, this option proposes an architectural overhaul when a targeted structural fix (adding a validation step) would address the specific failure without discarding the sequential pipeline's advantages for this task structure.

### Question 2

Hong et al. (2024) describe MetaGPT's design principle of defining explicit input-output schemas for each agent role. A practitioner argues: "If we use capable LLMs, we don't need to specify schemas — the agents will figure out the format from context." Which response most precisely refutes this argument using Hong et al.'s framework?

A. Capable LLMs are inconsistent in their output formats across runs, making implicit schemas unreliable regardless of model capability.

B. Schema specification is not about LLM capability — it is about making inter-agent interfaces explicit and deterministic so that structural failures (parsing errors, format mismatches) are detectable at design time rather than discovered as silent runtime failures that corrupt downstream stages.

C. Schemas are required by the LangGraph API — add_conditional_edges() cannot route correctly without typed schema fields to inspect.

D. The practitioner is correct — with GPT-4 class models, implicit schemas are sufficient for most production use cases; explicit schemas are only necessary for smaller, less capable models.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Hong et al.'s schema specification principle is not a compensation for LLM capability limitations — it is an architectural discipline that provides determinism and detectability. Even a highly capable LLM will produce format variations across runs (especially for complex structured outputs), and those variations propagate silently through a pipeline without explicit validation. More importantly, explicit schemas make inter-agent interfaces a contractual design artifact: when a schema mismatch occurs, the system can detect and report it rather than passing malformed data forward. This is analogous to function signatures in software engineering — strongly typed interfaces catch errors at design time, not after they have corrupted production data. The principle applies regardless of model capability.

    ❌ **A is incorrect** as the primary argument. While LLM output inconsistency is real, framing the schema argument primarily around model unreliability is weaker than the architectural argument. Even a perfectly consistent LLM that always produces valid output would benefit from explicit schemas because they make inter-agent contracts explicit, auditable, and verifiable — not because the LLM might fail.

    ❌ **C is incorrect.** LangGraph's `add_conditional_edges()` does not require typed schema fields in a strict API sense — it routes based on the return value of a Python routing function that can inspect any state field. The argument for schema specification is architectural (Hong et al.'s design principle), not a framework API requirement.

    ❌ **D is incorrect.** This option contradicts Hong et al.'s design philosophy and mischaracterizes the purpose of schemas. Schema specification is a professional discipline for reliable systems engineering — it is more important, not less important, in production deployments with high-capability models, where the costs of silent failures are higher. The practitioner's argument is the kind of "we'll handle it with better prompting" reasoning that the chapter lesson explicitly identifies as insufficient for structural problems.

### Question 3

Stone and Veloso (2000) describe the contract net protocol as a coordination mechanism where tasks are advertised, agents bid for them, and a broker assigns them. The Market-Mechanism Allocation pattern in modern LLM-based MAS is described as "inspired by the contract net protocol." Which statement correctly identifies the most significant departure of modern LLM-based market-mechanism systems from the classical contract net protocol?

A. Modern systems use LLMs instead of rule-based agents, so the bidding logic is now probabilistic rather than deterministic — LLMs cannot provide formal bid values.

B. Modern systems typically lack a formal bidding language and structured bid evaluation mechanism; instead, task assignment is often based on capability declarations (system prompts) rather than dynamic, per-task competitive bids — eliminating the competitive allocation property that defines the classical protocol.

C. Modern systems run on cloud infrastructure rather than distributed robotics systems, which changes the latency profile but not the fundamental coordination mechanism.

D. Modern systems do not use a broker — the task queue is managed by the orchestration framework's scheduler, which assigns tasks randomly rather than based on agent capabilities.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The defining feature of the contract net protocol is dynamic, per-task competitive bidding: for each task, agents evaluate it, determine their capability and availability, submit a bid, and the broker selects the best-fit agent. Modern LLM-based systems that implement market-mechanism allocation typically do not support this dynamic bidding process — LLMs cannot reliably evaluate a task specification and produce a structured, comparable bid. Instead, capability declaration is done at system initialization through system prompts that describe each agent's specialization, and assignment is based on matching task type to declared capability rather than competitive per-task evaluation. This departures from the classical protocol in a way that reduces dynamic adaptability — a key property of the contract net — while retaining the queue-based task distribution structure.

    ❌ **A is incorrect.** The distinction between probabilistic and deterministic reasoning is a real property of LLM-based systems, but it is not the most significant departure from the contract net protocol. Probabilistic reasoning affects bid quality; the more fundamental departure is the absence of structured bidding altogether — without formal bids, there is nothing to evaluate probabilistically.

    ❌ **C is incorrect.** Infrastructure (cloud vs. distributed robotics) affects latency and deployment context but does not change the coordination mechanism. The contract net protocol could, in principle, be implemented on cloud infrastructure with the same competitive bidding properties. The departure is in the protocol design, not the deployment environment.

    ❌ **D is incorrect.** Modern market-mechanism systems do use a broker (or equivalent task dispatcher) — the departure from the classical protocol is in the bidding process, not the broker's role. The chapter lesson explicitly describes the broker as "assigning tasks to the appropriate agent" in the modern pattern; the departure is that assignment is based on static capability declarations rather than dynamic per-task competitive bids.

### Question 4

The chapter lesson states that the Peer Collaboration Network pattern is appropriate for "tasks where interdependencies are complex, non-linear, or not fully known at design time." A practitioner is designing a system to coordinate three LLM agents working on an open-ended strategic planning problem where the agents' conclusions may influence each other's reasoning. Which specific failure risk of the Peer Collaboration Network pattern must the practitioner address before deployment?

A. Sequential bottleneck — if one agent produces output faster than others, the pipeline will be rate-limited by the slowest agent, requiring load balancing.

B. Supervisor overload — without a central coordinator, no agent can decompose the task effectively, producing agents that work on overlapping sub-problems.

C. Emergent contradictory outputs — without explicit conflict resolution mechanisms, agents in a peer network may reach conclusions that contradict each other, and no architectural component exists to arbitrate; the system may present conflicting recommendations without a synthesis mechanism.

D. Context window saturation — peer collaboration networks share all messages across all agents, rapidly filling each agent's context window and degrading performance.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** The chapter lesson explicitly identifies "contradictory outputs arising without explicit conflict resolution" as the key failure point of the Peer Collaboration Network pattern. When agents communicate horizontally without a central arbiter, each agent may develop reasoning that logically contradicts another agent's conclusions — and the peer network provides no architectural mechanism to detect, arbitrate, or synthesize these contradictions. The practitioner must either: (1) add an explicit synthesis agent whose role is to identify and resolve contradictions across peer outputs before producing a final recommendation; (2) define conflict resolution rules in each agent's system prompt (though this is a partial fix, not a structural one); or (3) consider whether a hierarchical pattern with a supervisor responsible for synthesis is more appropriate for a task where conclusions must be integrated into a coherent final output.

    ❌ **A is incorrect.** Sequential bottleneck is a failure mode of the Role-Based Sequential Pipeline pattern — not the Peer Collaboration Network. In a peer network, agents communicate in all directions and do not have a strict sequential execution order; there is no pipeline stage to bottleneck.

    ❌ **B is incorrect.** Supervisor overload is a failure mode of the Hierarchical Supervisor-Worker pattern, where the central supervisor becomes a processing bottleneck. The Peer Collaboration Network has no supervisor; its failure modes arise from the absence of centralized coordination, not from overloading a coordinator.

    ❌ **D is incorrect.** While context window management is a real concern in any multi-agent system, it is not the defining structural failure risk of the peer collaboration pattern. Message flooding can be managed architecturally through selective message routing. The more fundamental and architecturally distinctive failure risk is contradictory outputs without resolution — which is inherent to the pattern's distributed, non-hierarchical structure and cannot be managed through context window optimization.

### Question 5

Hong et al.'s MetaGPT evaluation shows that the role-based sequential pipeline produces higher-quality software artifacts than single-agent GPT-4 on HumanEval benchmarks. The chapter lesson warns that the sequential pipeline's specific failure point is "a failure at any stage propagates forward and may corrupt all subsequent stages." Which structural mechanism does Hong et al.'s MetaGPT implement to mitigate this propagation risk, and what is its limitation?

A. MetaGPT uses LLM self-correction at each stage — before passing output to the next agent, each agent is instructed to verify its own output for errors; the limitation is that self-correction is unreliable for logical errors that the generating agent cannot detect in its own reasoning.

B. MetaGPT uses a shared message pool that stores all agents' outputs, allowing downstream agents to reference any prior stage's output directly — mitigating some propagation failures by giving downstream agents access to the original upstream output, not only the immediately preceding stage's processed output; the limitation is that this creates a departure from strict sequential pipeline architecture and introduces the need to manage message pool growth.

C. MetaGPT uses human-in-the-loop checkpoints at each stage transition — a human reviewer approves each stage's output before it is passed forward; the limitation is that this eliminates the automation benefit that makes MAS valuable.

D. MetaGPT enforces a maximum revision count (like Lab B's `revision_count >= 2` check) to prevent infinite propagation loops; the limitation is that the maximum count may terminate the pipeline before a genuinely correctable error is fixed.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** MetaGPT's shared message pool is the specific architectural mechanism that partially mitigates linear propagation risk. In a strict sequential pipeline, the analyst only receives the researcher's output — if the researcher's output is flawed, the analyst has no access to the original task specification or earlier context. MetaGPT's shared pool makes all prior stages' outputs available to all subsequent agents, allowing a downstream agent to reference the original specification and detect divergence from it even if the intermediate stage corrupted its output. The limitation is structural: the shared message pool introduces cross-stage dependencies that are not explicit in the pipeline's directed graph, making the system's behavior harder to reason about, and the pool grows with each message, consuming context window space.

    ❌ **A is incorrect.** MetaGPT does not implement LLM self-correction as its primary propagation mitigation — self-correction is an optional prompting strategy, not a structural mechanism of the MetaGPT architecture. While self-correction can be added to any pipeline, it is not the specific mechanism Hong et al. describe as addressing propagation risk.

    ❌ **C is incorrect.** MetaGPT is designed as an automated system — it does not implement mandatory human-in-the-loop stage checkpoints as its primary reliability mechanism. Human review is available as an optional override but is not the architectural mechanism that addresses propagation.

    ❌ **D is incorrect.** The maximum revision count mechanism (as in Lab B's `revision_count >= 2` check) addresses the infinite loop failure of a critic-revision cycle, not the propagation of errors through a linear pipeline. These are distinct failure modes: propagation occurs when a stage's error corrupts the next stage's input; infinite loops occur when a revision cycle has no termination condition. Cemri et al.'s MAST taxonomy would classify these in different categories.

## Chapter 3 Quiz — The Three Orchestration Frameworks: LangGraph, AutoGen, and CrewAI { #chapter-3-quiz }

*Based on Reading Guide 3: LangGraph Documentation, Wu et al. (2024) AutoGen, Guo et al. (2024), CrewAI Documentation, LangChain Video*

### Question 1

A developer implements a LangGraph supervisor-worker system. The supervisor node calls an LLM to decompose the user query and writes the sub-task to `state['subtask']`. The specialist node reads `state['subtask']` and writes its result to `state['specialist_output']`. After two test runs, the developer discovers that the specialist node sometimes receives `None` in `state['subtask']` and fails silently. What is the most likely architectural cause, and what is the correct structural fix?

A. The specialist node's LLM prompt is not instructing it to handle None values gracefully; the fix is to add a None-handling instruction to the specialist's system prompt.

B. The `state['subtask']` field is missing from the TypedDict state schema declaration, so LangGraph initializes it as None rather than raising an error; the fix is to declare the field explicitly in the AgentState TypedDict with an appropriate type annotation.

C. The LangGraph `compile()` step has a bug that occasionally fails to propagate state updates between nodes; the fix is to add a validation call after `compile()` to verify state field propagation.

D. The conditional edge routing function is routing to the specialist node before the supervisor node has completed its LLM call; the fix is to add a `time.sleep()` delay between the supervisor and specialist nodes.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The Lab A hint explicitly warns: "if a field is missing or misnamed, every downstream node fails silently (it receives None rather than an error)." LangGraph's TypedDict state schema is the architectural contract that all nodes depend on. If `state['subtask']` is not declared in the AgentState TypedDict, Python's TypedDict machinery does not raise a KeyError when the field is absent — the field resolves to None, and the specialist node receives None as its subtask input. This is a state schema declaration failure (MAST Category 1: system design issue). The structural fix is to declare the field in the TypedDict: `class AgentState(TypedDict): subtask: Optional[str]`. This is not a prompt fix — it is an architectural fix to the state schema definition.

    ❌ **A is incorrect.** Adding None-handling instructions to the specialist's prompt treats the symptom (the specialist receives None) rather than the root cause (the state schema does not declare the field). Even with graceful None handling, the specialist still receives no subtask — it would produce a meaningless output rather than the correct output. The correct fix eliminates the None by declaring the field, not by teaching the specialist to work around it.

    ❌ **C is incorrect.** LangGraph's state propagation is deterministic and not subject to intermittent bugs in the compile step. If state propagation were non-deterministic, the failure would not be consistent with the symptom (sometimes None — which is consistent with a missing field declaration that always initializes to None, not with intermittent propagation bugs).

    ❌ **D is incorrect.** LangGraph's graph execution is sequential within a single execution thread — the specialist node does not begin executing until the supervisor node has completed and returned its updated state. Adding a sleep would not fix a missing field declaration and would introduce unnecessary latency. Race conditions are not a failure mode of LangGraph's node execution model.

### Question 2

The LangGraph documentation distinguishes between `add_edge()` (deterministic routing) and `add_conditional_edges()` (dynamic routing). A practitioner building the Lab A system must route to either the specialist node or END depending on whether the specialist has completed its task. Which statement correctly explains why `add_conditional_edges()` is architecturally necessary rather than merely convenient for this routing decision?

A. `add_conditional_edges()` is required by the LangGraph API whenever a graph has more than two nodes — it is a structural requirement, not a design choice.

B. The routing decision depends on the runtime value of a state field (`state['specialist_output']`) that is only known after the supervisor node has executed — a deterministic edge cannot inspect runtime state, so conditional routing is architecturally required for any decision that depends on state values produced during execution.

C. `add_conditional_edges()` is more efficient than `add_edge()` because it avoids unnecessary node invocations — a deterministic edge would always invoke both the specialist and END nodes, doubling the execution cost.

D. The LangGraph compiler cannot validate `add_edge()` routing for graphs with cycles, so `add_conditional_edges()` must be used whenever the graph contains a loop back to an earlier node.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The routing decision — whether to proceed to the specialist or terminate — depends on whether `state['specialist_output']` has been populated. This value is only known at runtime, after the supervisor node has executed and the specialist has (or has not) produced output. `add_edge()` creates a static, compile-time routing rule: "always go from node A to node B." It cannot inspect runtime state. `add_conditional_edges()` creates a runtime routing function: "call this Python function with the current state and use its return value to determine the next node." For any routing decision that depends on what happened during execution — the content of a state field, the output of an LLM call, the count of prior revisions — conditional routing is architecturally required, not merely preferable.

    ❌ **A is incorrect.** The LangGraph API does not require `add_conditional_edges()` for graphs with more than two nodes. Graphs with deterministic linear flow can use `add_edge()` throughout, regardless of node count. The distinction is about routing logic, not graph size.

    ❌ **C is incorrect.** `add_conditional_edges()` does not improve efficiency by avoiding node invocations — it routes to exactly one node per invocation (the one returned by the routing function). It does not execute multiple nodes or avoid any execution that `add_edge()` would have triggered. The efficiency argument is factually incorrect.

    ❌ **D is incorrect.** LangGraph can validate `add_edge()` routing in graphs with cycles — it checks for reachability and termination conditions at compile time. The choice between `add_edge()` and `add_conditional_edges()` is driven by whether routing logic depends on runtime state, not by whether the graph contains cycles.

### Question 3

Guo et al. (2024) recommend that "production deployments instrument multi-agent systems with full execution logging — recording every agent invocation, every message passed, and every state transition." A developer argues that logging adds latency and storage overhead that is not justified for a well-tested system. Which counter-argument most precisely applies Guo et al.'s recommendation?

A. Logging is required by enterprise compliance standards, making it a regulatory requirement rather than an optional engineering choice.

B. Even a well-tested system will encounter input distributions at runtime that differ from its test cases; execution logs are the only mechanism that allows a developer to diagnose whether an observed output failure arose from a coordination failure (an architectural issue) or a generation failure (a model capability issue) — without logs, these two failure types are indistinguishable from the final output alone.

C. Logging overhead is negligible for LLM-based systems because LLM inference latency dominates total execution time; the marginal cost of writing log entries is imperceptible relative to the inference calls.

D. Guo et al. recommend logging because multi-agent systems are inherently unreliable, so practitioners should always expect failures and treat logging as a mandatory incident response mechanism.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Guo et al.'s recommendation is grounded in a specific diagnostic necessity: coordination failures and generation failures produce similar observable symptoms (incorrect final output) but require fundamentally different remediation. A coordination failure (e.g., an agent receiving a malformed handoff) requires architectural intervention; a generation failure (e.g., an LLM producing an incorrect answer despite correct input) requires prompt or model-level intervention. Without execution logs showing what each agent received as input and produced as output, it is impossible to determine which type of failure occurred. This diagnostic necessity applies to well-tested systems encountering novel inputs, not only to unreliable systems. The argument is analytical — about the information needed for correct diagnosis — not regulatory or performance-based.

    ❌ **A is incorrect.** While compliance requirements may mandate logging in some regulated industries, Guo et al.'s argument is architectural and diagnostic — it is not primarily a regulatory compliance argument. The recommendation applies to all production MAS deployments regardless of regulatory context.

    ❌ **C is incorrect.** The latency argument may be empirically true for many systems, but it does not address the developer's core concern about storage overhead and is not Guo et al.'s argument for logging. Even if logging had significant overhead, the diagnostic necessity (B) would still apply. Dismissing the overhead concern empirically without addressing the analytical reason for logging misses the more important argument.

    ❌ **D is incorrect.** Guo et al. do not characterize multi-agent systems as "inherently unreliable" — they characterize them as systems whose failures require specific diagnostic capabilities that final-output inspection cannot provide. The recommendation is about diagnostic precision, not about pessimistic reliability assumptions.

### Question 4

AutoGen's coordination model uses natural language message exchange, while LangGraph uses a typed state schema. A practitioner building a system that requires auditable decision trails for regulatory compliance must choose between these frameworks. Which analysis most precisely applies the observability dimension from the Framework Comparison Report?

A. AutoGen is more observable because its natural language messages are human-readable, enabling regulators to inspect agent communication without specialized tooling.

B. LangGraph's typed state schema provides superior auditability for regulatory compliance: each state transition is a structured, typed object that can be logged, compared against expected values, and replicated deterministically — satisfying interpretability requirements that unstructured natural language message trails cannot reliably meet.

C. Both frameworks are equally observable — Python's `logging` module can be applied to either framework to capture full execution traces, regardless of whether state is typed or conversational.

D. AutoGen is superior for compliance contexts because its conversation history model mirrors how human teams document decisions — as a sequence of natural language communications — making it more interpretable to non-technical auditors.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** For regulatory compliance, observability has a specific technical meaning beyond human readability: the execution trace must be structured, deterministic, and verifiable. LangGraph's typed state schema provides this: at each state transition, the full typed state object is logged, and the log entry can be programmatically compared against expected schemas, replicated in a test environment, and traced to the specific node and routing function that produced it. AutoGen's natural language message trail is human-readable but is not structured or verifiable in the same technical sense — message content is untyped text that may vary across runs for the same input, making programmatic verification difficult. The LangGraph state schema's explicitness — the same property that the LangGraph documentation highlights and that Reading Guide 3 connects to EU AI Act Article 13 requirements — directly addresses regulatory auditability requirements.

    ❌ **A is incorrect.** Human readability and regulatory auditability are not equivalent. A regulatory audit typically requires deterministic, structured evidence that the system made specific decisions based on specific inputs — properties that human-readable natural language messages do not reliably provide. A natural language message saying "the analyst reviewed the research and found it satisfactory" does not provide the same audit evidence as a structured state log showing `analysis_output: [exact content]` and `critic_verdict: APPROVED` at a specific timestamp.

    ❌ **C is incorrect.** While Python's `logging` module can be applied to both frameworks, it captures different granularities of information depending on the underlying data structure. Logging LangGraph's typed state objects produces structured, parseable log entries. Logging AutoGen's conversation history produces unstructured text. The observability difference is in the structure of what is logged, not in whether logging can be applied.

    ❌ **D is incorrect.** The argument that AutoGen mirrors human documentation practices is a user experience argument, not an observability argument. Regulatory compliance requires technical verifiability, not mimicry of human documentation conventions. An unstructured conversation log that resembles human email exchanges is not more auditable than a structured state log — it is less auditable, because it lacks the typed, schema-validated structure needed for programmatic verification.

### Question 5

The LangChain video demonstrates two multi-agent architectures — swarm and supervisor — using LangGraph with Ollama. The supervisor architecture uses a routing LLM call to decide which specialist to invoke next. What is the specific architectural risk of using an LLM to make routing decisions, and what is the most robust structural mitigation?

A. LLM-based routing is slow because it requires an additional inference call per routing decision; the mitigation is to cache routing decisions for repeated queries to avoid redundant inference.

B. LLM-based routing is non-deterministic: the same state may produce different routing decisions across runs depending on the LLM's sampling behavior, making system behavior difficult to reproduce, test, and audit; the most robust mitigation is to implement routing as a deterministic Python function that inspects typed state fields rather than delegating the decision to an LLM — or to constrain the routing LLM to structured output (e.g., a JSON object with a `next_agent` field) and validate its output before acting on it.

C. LLM-based routing may route to agents that do not exist in the StateGraph, causing a KeyError at runtime; the mitigation is to add a try-except block around the routing function call.

D. LLM-based routing requires a more capable and expensive model than the specialist agents, increasing the cost of the supervisor node disproportionately; the mitigation is to use a smaller, faster model for routing decisions only.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The Reading Guide identifies LLM-based routing non-determinism as the specific risk: the supervisor LLM inspects the current state and produces a routing decision as natural language output (e.g., "route to the research specialist"), but this output may vary across runs for identical inputs due to the LLM's temperature setting and sampling stochasticity. In a system where routing correctness is a reliability requirement, non-deterministic routing makes the system behavior difficult to test (test results may not reproduce), audit (the execution trace may differ from previous runs for the same input), and debug (a routing failure may not reproduce in a debug run). The mitigations are: (1) implement routing as a deterministic Python function that inspects state fields (e.g., `if state['subtask_type'] == 'research': return 'researcher'`); or (2) constrain the routing LLM to structured output and validate the output against the set of valid node names before acting on it — a partial mitigation that retains LLM flexibility while reducing the risk of invalid or inconsistent routing decisions.

    ❌ **A is incorrect.** Routing latency from an additional LLM inference call is a real cost, but caching routing decisions is not the appropriate mitigation — routing decisions are state-dependent, and the same query state may legitimately require different routing at different points in a conversation or task. Caching a routing decision from a prior run and applying it to a different state is architecturally incorrect.

    ❌ **C is incorrect.** A KeyError from routing to a non-existent node is a real implementation risk, but it is not the primary architectural risk of LLM-based routing. This error would occur only if the routing LLM produces a node name not registered in the StateGraph — a specific implementation failure that would manifest on the first test run and is easily caught. The more significant and persistent risk is non-determinism, which may not be obvious from initial testing.

    ❌ **D is incorrect.** Model cost differential is a valid engineering consideration for production deployments, but it is a resource optimization concern, not the primary architectural risk of LLM-based routing. The primary architectural risk — non-determinism and its implications for reproducibility and auditability — exists regardless of whether the routing model is expensive or cheap.

## Chapter 4 Quiz — Coordination Failure Taxonomy { #chapter-4-quiz }

*Based on Reading Guide 4: Cemri et al. (2026) MAST, Wooldridge & Jennings (1995), Stone & Veloso (2000)*

### Question 1

In a three-role pipeline (Researcher → Analyst → Critic), the critic approves analyst outputs even when they contain factual errors contradicting the research. Which MAST failure mode is this, and what is the correct mitigation?

A. "Ignored Other Agent's Input" — require the critic to explicitly reference the researcher's output in its evaluation.

B. "Incorrect Verification" — use multiple independent verifiers and require verification against a structured checklist that cross-references analyst claims against the research output.

C. "Disobey Task Specification" — use structured output schemas that enforce the required verification format.

D. "Reasoning-Action Mismatch" — add a step comparing the critic's stated plan to its executed action.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** This is "Incorrect Verification" (9.1%) — the verifier accepts flawed output as correct. The critic performs its evaluation but produces a wrong judgment because its criteria don't include factual consistency. The mitigation: use multiple independent verifiers and verify against all criteria in a structured checklist cross-referencing the research output.

    ❌ **A is incorrect.** "Ignored Other Agent's Input" describes an agent disregarding another's information during execution. Here the critic evaluates the analyst's work — it isn't ignoring input, it's verifying incorrectly.

    ❌ **C is incorrect.** "Disobey Task Specification" means the agent deviates from its instructions. The critic may be following its instructions — the instructions themselves are incomplete (missing a factual check criterion).

    ❌ **D is incorrect.** "Reasoning-Action Mismatch" means an agent says one thing but does another. The scenario describes incorrect judgment, not a disconnect between plan and action.

### Question 2

A practitioner's pipeline enters an infinite revision loop — the critic never approves the analyst's output. They propose fixing it by telling the critic to "be less strict" in its system prompt. Why is this wrong?

A. System prompts have character limits that prevent adding detailed strictness instructions.

B. The infinite loop is an architectural failure: the pipeline lacks a termination condition. A prompt change may reduce rejection probability but does not guarantee termination. The fix is to add a `revision_count` state field and a hard stop in routing logic (`if revision_count >= 2: return 'end'`).

C. LLMs ignore system prompt instructions in multi-turn conversations.

D. Strictness is determined by the LLM's training data, not system prompts — only fine-tuning would change it.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The infinite loop maps to "Step Repetition" (15.7%) — the most prevalent system design failure. The routing function has no exit condition other than critic approval, so if the critic ever rejects, the loop continues indefinitely. "Be less strict" is a probabilistic nudge, not a structural guarantee. The mitigation: track executed actions in a state log and add a hard stop after N iterations.

    ❌ **A is incorrect.** Prompt length is not the issue — the distinction is between probabilistic behavior change and deterministic structural guarantee.

    ❌ **C is incorrect.** LLMs do process system prompt instructions. The argument is that a prompt change doesn't guarantee termination, not that prompts don't work.

    ❌ **D is incorrect.** System prompts demonstrably influence LLM behavior. The problem is that no behavioral nudge provides the same guarantee as an architectural termination condition.

### Question 3

Cemri et al. (2026) studied 150 interaction traces across six frameworks. Which statement best describes the MAST taxonomy's scope?

A. MAST covers all possible MAS failure modes exhaustively.

B. MAST's 14 failure modes were derived from systematic analysis of observed failures across multiple frameworks; the taxonomy is validated for coverage within that dataset but may not capture failure modes in future architectures.

C. MAST applies only to LangGraph-based systems.

D. MAST's three categories map one-to-one to the three frameworks (LangGraph, AutoGen, CrewAI).

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** MAST is empirically grounded — derived from coding real failures, validated for inter-rater reliability, and scoped to the observed dataset. The authors do not claim exhaustiveness for all future systems.

    ❌ **A is incorrect.** Proving a taxonomy is exhaustive would require demonstrating no other failure modes exist — the paper does not claim this.

    ❌ **C is incorrect.** MAST is framework-agnostic, analyzing failures across six different frameworks.

    ❌ **D is incorrect.** The three categories are failure types, not framework labels. Any framework can exhibit any failure category.

### Question 4

An analyst agent states in its reasoning trace: "I will focus on the three key findings from the research." It then produces output covering five unrelated topics. Under MAST, which failure mode is this, and what mitigation addresses it?

A. "Task Derailment" — insert periodic objective-check gates that compare output against the original task goal.

B. "Reasoning-Action Mismatch" — add a verification step that compares the agent's stated plan to its executed action and flags discrepancies before passing output downstream.

C. "Disobey Task Specification" — use structured output schemas that enforce the required format.

D. "Information Withholding" — design agents with explicit output schemas that mandate passing all relevant context forward.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** "Reasoning-Action Mismatch" (13.2%) — the second most prevalent failure mode overall — describes exactly this: the agent's stated reasoning ("focus on three findings") does not match its action (covers five unrelated topics). The mitigation: add a verification step comparing plan to output before handoff.

    ❌ **A is incorrect.** "Task Derailment" is collective drift away from the objective across multiple agents. This scenario is a single agent's internal disconnect between plan and action.

    ❌ **C is incorrect.** "Disobey Task Specification" means deviating from assigned instructions. Here the agent's own reasoning is correct — it's the action that diverges from its own plan, not from external instructions.

    ❌ **D is incorrect.** "Information Withholding" is about failing to share relevant information with other agents, not about internal plan-action inconsistency.

### Question 5

A pipeline completes a research task successfully, but the researcher agent continues executing — generating additional summaries, re-querying sources, and appending redundant content to the output. Which MAST failure mode is this, and what is the correct mitigation?

A. "Step Repetition" — track executed actions in a state log and halt after N identical steps.

B. "Premature Termination" — add a high-level objective verifier that checks whether the goal is satisfied.

C. "Unaware of Termination Conditions" — define explicit completion criteria in the task prompt and add a post-step check that evaluates whether those criteria have been met.

D. "Task Derailment" — insert objective-check gates to prevent drift from the original goal.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** "Unaware of Termination Conditions" (12.4%) — the third most prevalent failure mode — describes an agent continuing after the task is complete because it lacks explicit criteria for recognizing when to stop. The mitigation: define completion criteria and add a post-step evaluation gate.

    ❌ **A is incorrect.** "Step Repetition" is repeating the same action without progress. This agent is doing different things (summaries, re-queries, appending) — it's not stuck in a loop, it simply doesn't know when to stop.

    ❌ **B is incorrect.** "Premature Termination" is the opposite problem — stopping too early. This agent stops too late.

    ❌ **D is incorrect.** "Task Derailment" is collective drift from the objective. This agent stays on-topic (still doing research) — it just doesn't recognize the task is already done.

## Chapter 5 Quiz — Evidence-Based Benchmarking: When Does Multi-Agent Add Value? { #chapter-5-quiz }

*Based on Reading Guide 5: Wu et al. (2024) AutoGen, Hong et al. (2024) MetaGPT*

### Question 1

A benchmark produces: Multi-agent pipeline — accuracy 4.2/5, tokens 18,400, latency 47s. Single ReAct agent — accuracy 3.9/5, tokens 4,200, latency 12s. What is the coordination overhead ratio, and how should it be interpreted?

A. (18,400 − 4,200) / 4,200 = 338%. The pipeline used 338% more tokens for a 7.7% accuracy gain. Whether this is justified depends on the deployment context — how much accuracy is worth relative to cost.

B. 18,400 / 4,200 = 438%. The pipeline used 4.38× more tokens, so it is always too expensive unless accuracy is the only criterion.

C. (4.2 − 3.9) / 4.2 = 7.1%. This measures accuracy improvement, not token overhead.

D. 47 / 12 = 3.9. Latency ratio is the correct metric because users care about speed more than cost.

??? success "Show answer and feedback"

    **Correct Answer: A**

    ✅ **A is correct.** Coordination overhead = (MAS tokens − single-agent tokens) / single-agent tokens = 338%. Whether 338% overhead is worth a 0.3-point accuracy gain depends on context: in high-stakes domains (medical, legal), that gain may prevent costly errors; in high-volume cost-sensitive pipelines, it may not be worthwhile.

    ❌ **B is incorrect.** The formula is wrong (must subtract before dividing), and "always too expensive" is the kind of unqualified claim the module rejects. Context determines whether overhead is justified.

    ❌ **C is incorrect.** This formula calculates accuracy improvement, not coordination overhead. They are separate metrics.

    ❌ **D is incorrect.** Latency is a separate evaluation dimension, not the coordination overhead ratio. The overhead ratio specifically measures token cost.

### Question 2

Wu et al.'s AutoGen paper shows MAS outperforms single-agent GPT-4 on code generation. What is the main limitation when generalizing these results to other tasks?

A. The results are invalid because Microsoft published the paper, creating a conflict of interest.

B. Code generation naturally decomposes into stages (spec → design → code → test) with clean handoffs between stages. Tasks that require holistic reasoning rather than decomposition may not show the same MAS advantage.

C. The evaluation is biased because single-agent GPT-4 is weaker than the multi-agent ensemble.

D. All published MAS benchmarks are unreliable, so practitioners must always run their own evaluations.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Code generation is a favorable MAS benchmark because it decomposes naturally into stages with well-defined outputs. Results may not generalize to tasks requiring holistic integration (e.g., analytical writing, complex causal reasoning) where decomposition is unclear or loses coherence.

    ❌ **A is incorrect.** Selection bias is about task selection, not author affiliation. The critique is that the chosen task happens to favor MAS, not that the authors are biased.

    ❌ **C is incorrect.** Wu et al. use the same underlying model for both conditions, so the comparison is fair. Performance differences are attributable to architecture, not model capability.

    ❌ **D is incorrect.** The critique is more targeted: results from easily decomposable tasks should not be assumed to generalize to all tasks. Published results are still informative within their scope.

### Question 3

A student's evaluation report concludes: "The multi-agent pipeline scored 4.1 vs. 3.8 for single-agent, but used more tokens and time. Both approaches have trade-offs depending on context." What is wrong with this as a formal recommendation?

A. Nothing — acknowledging trade-offs is a balanced, professional recommendation.

B. It describes trade-offs but never makes a decision. A formal recommendation must commit to a position (e.g., "MAS is warranted for this task class when [conditions]"), specify the boundary conditions under which that position holds, and state what would change it.

C. The only thing missing is the coordination overhead ratio; adding that number would turn the paragraph into a formal recommendation.

D. It needs to be longer — at least 300 words of analysis.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** A formal recommendation requires three things: (1) a clear position — is MAS warranted or not; (2) the conditions under which that position holds (e.g., "when accuracy gain > 0.3 points AND cost per query < $X"); (3) what would change the recommendation. "Both have trade-offs" delivers none of these — it is a description of results, not a recommendation a decision-maker can act on.

    ❌ **A is incorrect.** Acknowledging trade-offs is necessary context, but a recommendation must go further and commit to a course of action with stated conditions.

    ❌ **C is incorrect.** The coordination overhead ratio is useful evidence — it tells a decision-maker what the extra agents cost compared with a single agent — but adding it would not fix this paragraph. It would still describe trade-offs without choosing between them. What makes a recommendation formal is a committed position with stated conditions, and no additional metric supplies that.

    ❌ **D is incorrect.** Quality is defined by analytical rigor, not word count. A concise recommendation with clear boundary conditions is better than a long description without a conclusion.

### Question 4

MetaGPT benchmarks against both single-agent GPT-4 and another MAS framework (ChatDev). Why is comparing against another MAS framework valuable?

A. Conference reviewers require at least two baselines for publication.

B. It distinguishes "MAS is better than single-agent" from "this specific MAS design is better than other MAS designs." If MetaGPT outperforms ChatDev, the advantage is attributable to MetaGPT's specific architectural choices, not just multi-agent coordination in general.

C. It validates that the benchmark task is suitable for multi-agent systems.

D. More experimental conditions increase statistical power.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Comparing against a single agent only shows that MAS helps. Comparing against another MAS shows that MetaGPT's specific choices (role specification, shared message pool, sequential pipeline) are better than alternative MAS designs — a more precise and useful conclusion.

    ❌ **A is incorrect.** The advantage is analytical insight, not compliance with publication requirements.

    ❌ **C is incorrect.** Comparing two MAS on the same task doesn't address selection bias, which is about task choice.

    ❌ **D is incorrect.** Statistical power comes from more trials per condition, not more conditions.

### Question 5

A practitioner benchmarks a document classification system (10,000 docs/day): single-agent 91% accuracy, multi-agent 93%, coordination overhead ratio 180% against the single-agent baseline. Which recommendation is most appropriate?

A. MAS is warranted — 2-point accuracy gain always justifies overhead for enterprise use.

B. MAS is not warranted — 180% overhead exceeds the 40% threshold, so the architecture should be simplified.

C. MAS may be warranted if the 2-point accuracy gain translates to enough business value to justify the token cost at 10,000 docs/day. Calculate cost-per-classification, check latency requirements, and test whether single-agent prompt optimization could close the accuracy gap before committing to MAS.

D. The benchmark is insufficient — at least 30 trials are needed before any recommendation is possible.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** This is a qualified recommendation: it takes a conditional position, specifies what evidence would confirm it, and identifies a prerequisite (test prompt optimization first). At scale, 180% overhead is a specific dollar amount that must be weighed against what 2% more accurate classification is worth to the business.

    ❌ **A is incorrect.** "Always justifies" is an unqualified claim. A 2-point gain may matter little in low-stakes routing but matter greatly in high-stakes classification. Context determines value.

    ❌ **B is incorrect**, twice over. The 40% rule of thumb applies to the coordination share — the fraction of a multi-agent system's own tokens spent on coordination — not to the 180% overhead ratio, which compares the system with the single-agent baseline. And even on its own measure, 40% is a signal to investigate simplification, not a ceiling that vetoes a deployment. At this scale, the relevant question is whether the accuracy gain's business value exceeds the additional cost.

    ❌ **D is incorrect.** Statistical limitations should be noted as a qualifying condition, but "no recommendation possible" is too strong. A qualified recommendation can be made while acknowledging limited sample size.

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-4.2-Addendum){target=_blank} (wiki page last changed 2026-08-12). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-4/chapter-quizzes.md){target=_blank}.</p>
