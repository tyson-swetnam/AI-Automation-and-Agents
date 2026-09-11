---
title: Module 2 Reading Guides
description: 'Read-extract-synthesize reading guides for the five Module 2 chapters: CoT, ReAct, Tree of Thoughts, LATS, tool integration, reasoning-trace critique, agent prompt engineering, and architectural trade-offs.'
type: Reading Guide
tags:
- module-2
- student-facing
- reading-guide
- reasoning-paradigms
- react
- langchain
- tool-use
- prompt-engineering
module: 2
status: stable
stale_after: '2027-09-01T00:00:00Z'
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2.2-Addendum
  title: 'AI Automation and Agents v2 wiki: Module-2.2-Addendum'
  author: Michelle Yung; Carlos Lizárraga-Celaya
  last_modified: '2026-08-06T07:02:00-07:00'
authorship:
  created: '2026-08-06'
  contributors:
  - C. Lizárraga
wiki_page: Module-2.2-Addendum
---
# Module 2 Reading Guides

These guides structure your engagement with the assigned readings. For each guide, complete the tasks in sequence: **read → extract → synthesize**. The extraction tasks map directly to quiz and project rubric items. Do not proceed to a chapter quiz until you can complete the synthesis task without re-reading.

**Note on reading numbering:** Readings are numbered according to the course reading assignment sequence (Readings 1, 2, 3, 5, 7). Readings 4 and 6 are reserved for other course materials. Chapter 3 and Chapter 5 draw on previously assigned readings plus lesson content rather than new numbered readings.

## Reading Guide 1 — Chapter 1: The Four Agent Reasoning Paradigms { #reading-guide-1 }

**Assigned Readings:**

- Reading 1: Wei, J., et al. (2022). *Chain-of-thought prompting elicits reasoning in large language models.* NeurIPS 2022. Read: Abstract + Section 2 + Figure 1.
- Reading 2: Yao, S., et al. (2022). *ReAct: Synergizing reasoning and acting in language models.* ICLR 2023. Read: Sections 1–2.
- Reading 3: Yao, S., et al. (2023). *Tree of thoughts: Deliberate problem solving with large language models.* NeurIPS 2023. Read: Sections 1–2.

*(Zhou et al. 2023 — LATS — is introduced in the Chapter 1 lesson. No separate full reading is assigned; master LATS from the lesson content and the four-paradigm comparative table.)*

### Part A: Chain-of-Thought Prompting (Wei et al., 2022)

**Scope:** Abstract + Section 2 (Chain-of-Thought Prompting) + Figure 1. Skim Section 4 only.

**Reading Focus Questions**

1. Wei et al. define a "chain of thought" as a series of intermediate natural language reasoning steps that lead to a final output. In standard few-shot prompting, what is absent from the exemplars, and what does CoT add to each exemplar?

2. The paper identifies emergent capability as a defining property of CoT: the effect is absent in smaller models and appears above a scale threshold. What does this imply about deploying CoT with sub-threshold models — models that have not crossed the emergent capability boundary?

3. Which task class shows the largest absolute performance gain from CoT prompting, and what property of that task class explains why intermediate reasoning steps help more than they do for, for example, simple factual retrieval?

**Key Concepts to Extract**

- **Reasoning trace (CoT sense):** The sequence of intermediate natural language steps produced by the model between the question and the final answer, serving as explicit intermediate computation.
- **Few-shot prompting vs. CoT few-shot prompting:** Standard few-shot provides (input, output) pairs as exemplars; CoT few-shot provides (input, reasoning-chain, output) triples, demonstrating the desired intermediate steps.
- **Emergent capability:** A qualitative capability transition that is absent below a model-scale threshold and appears above it — not a gradual improvement curve.
- **Task classes benefiting most from CoT:** Multi-step arithmetic, commonsense reasoning requiring compositional inference, and symbolic manipulation tasks — tasks where intermediate steps reduce the cognitive load on the final generation step.

**Synthesis Task**

Write two sentences in your notes: (1) What CoT adds to standard few-shot prompting in one sentence using the terms *reasoning trace* and *intermediate steps*. (2) Why an emergent capability finding matters for a practitioner choosing whether to use CoT with a 7B-parameter model.

### Part B: ReAct — Reason + Act (Yao et al., 2022)

**Scope:** Sections 1–2 (Introduction + ReAct: Synergizing Reasoning and Acting).

**Reading Focus Questions**

1. Yao et al. describe CoT as operating "entirely within the model's internal knowledge." What specific capability gap does this create for tasks that require current or external information — information not present in the model's training data?

2. The ReAct loop has three named phases: **Thought**, **Action**, and **Observation**. Define each phase precisely: what is generated in each, and by what component (LLM or external system)?

3. What terminates a ReAct reasoning loop? Identify both the agent-side condition (what the agent generates) and any external termination conditions described in the paper.

**Key Concepts to Extract**

- **Structural difference from CoT:** CoT is linear text generation with no external information retrieval; ReAct interleaves reasoning (Thought) with tool invocations (Action) and incorporates their outputs (Observation) before the next reasoning step.
- **Thought phase:** Generated by the LLM — a natural language statement of what the agent knows, what it needs, and what it intends to do next.
- **Action phase:** Generated by the LLM — a structured specification of a tool call (tool name + arguments).
- **Observation phase:** Generated by the external tool — the raw output returned after executing the Action. The LLM does not generate this; it reads it.
- **Loop termination:** The loop terminates when the LLM produces an answer instead of another action (agent-side), or when a step limit is reached (framework-side hard stop). In the paper's prompt format the agent signals completion with a finish action written as text; a modern tool-calling model signals it structurally, by returning a message that requests no tools, and the step limit is set by the `recursion_limit` config key rather than a `max_iterations` argument.

**Synthesis Task**

Draw a single-loop diagram in your notes showing the Thought → Action → Observation cycle. Label: (a) which component generates each phase, (b) the direction of information flow, and (c) the termination condition. If your diagram requires more than six labeled elements, simplify until it fits — clarity is the diagnostic criterion.

### Part C: Tree of Thoughts (Yao et al., 2023)

**Scope:** Sections 1–2 (Introduction + Tree of Thoughts Framework).

**Reading Focus Questions**

1. Yao et al. state that ReAct's linear Thought-Action-Observation cycle "cannot recover gracefully from dead ends." Describe a concrete scenario in which a ReAct agent commits to an incorrect reasoning path and cannot backtrack — and explain why the linear architecture prevents recovery.

2. ToT replaces the single reasoning chain with a tree of "coherent language sequences." What is the node structure of this tree — what does each node represent, and what determines which path is explored next?

3. The chapter lesson lists four conditions that justify choosing ToT over ReAct. State all four. Then identify the condition that is most often overlooked in practice (hint: it involves evaluation of intermediate states before the full solution is known).

**Key Concepts to Extract**

- **Problem ToT solves:** Linear commitment to a single reasoning path without backtracking; inability to explore alternative hypotheses in parallel.
- **Deliberate problem solving:** Generating multiple candidate reasoning paths, evaluating them before committing, and selecting or backtracking based on evaluated quality.
- **Tree node structure:** Each node represents a coherent partial solution (a "thought" — a language sequence that serves as an intermediate step); children are generated by expanding that thought into alternatives.
- **Evaluation mechanism:** A heuristic or the LLM itself evaluates each node's promise (e.g., assigning a score or a vote) before deciding which branch to extend.
- **Four ToT justification conditions:** (1) large state space with many possible solution paths; (2) intermediate states can be evaluated before the full solution is known; (3) backtracking is necessary because early wrong commitment is catastrophically costly; (4) computational budget and latency are not primary constraints.
- **Cost:** ToT requires generating and evaluating multiple branches per step — inference cost multiplies with branching factor; substantially more expensive than CoT or ReAct.

**Synthesis Task**

Construct a four-row reference table in your notes with columns: **Paradigm | External Tool Access | Backtracking | Relative Inference Cost | Primary Use Case**. Fill in all cells for CoT, ReAct, ToT, and LATS (use the Chapter 1 lesson for LATS). This table is the primary study artifact for Chapter 1 quiz preparation.

## Reading Guide 2 — Chapter 2: Tool Integration Architecture { #reading-guide-2 }

**Assigned Reading:**

- Reading 5: LangChain Documentation — *[Agents](https://docs.langchain.com/oss/python/langchain/agents){target=_blank} and [Tools](https://docs.langchain.com/oss/python/langchain/tools){target=_blank}.* Read the complete Agents guide; use the Tools reference for Part B. Focus: tool registry role, tool description use for tool selection, and how a tool-calling model returns a structured call — a `name` and an `args` dictionary — instead of text that an output parser has to convert.
- Video 2: Sam Witteveen — *"Understanding ReACT with LangChain"* (~22 min). Watch focus: conceptual distinction between CoT and ReAct; the observation integration step. The video was recorded against LangChain 0.x, whose `AgentExecutor` class was removed in LangChain 1.0 — take the reasoning-loop explanation from the video and the API from Reading 5.

*(Reference: Brown, T., et al. (2020). Language models are few-shot learners. NeurIPS 2020. — cited in lesson context; no full reading assigned.)*

### Part A: The Agent Runtime Architecture

**Scope:** LangChain Agents guide — complete.

**Reading Focus Questions**

1. The agent runtime has four structural components. Name all four and describe the specific function of each in one sentence. Pay particular attention to the **tool registry**: what does it store, where does each tool's description come from, and how does the model use it during a reasoning loop?

2. Older agent runtimes asked the model to *write* its action as text and then ran an **output parser** over that text; a tool-calling model instead returns the call as structured data (a `name` and an `args` dictionary) that the runtime executes directly. Which class of failure does that design remove? Then work through a failure it does not remove: the correct tool is called but raises an exception while it runs. What happens to the rest of the run, and what must the tool's author do instead?

3. The chapter lesson emphasizes that tool use is "what separates an AI agent from an LLM." Using the agent runtime as a reference, explain exactly what structural capability the agent adds that a standalone LLM call does not have.

**Key Concepts to Extract**

- **Four structural components of the agent runtime:**
    1. *LLM backbone* — the central reasoning engine; it reads the conversation so far and decides which action to take next, or that the question can now be answered.
    2. *Tool registry* — the registered tools with their descriptions and input schemas; it is the whole set of actions the model may choose from, and the agent reads it to know what capabilities are available.
    3. *Action executor* — the runtime that actually runs the chosen tool with the arguments the model supplied, and returns the result as the observation.
    4. *Memory module* — carries conversation history, tool outputs and observations forward, so each turn of the loop sees what the previous turns produced.
- **The fifth component that no longer exists:** older LangChain listed a fifth, an *output parser*, whose job was to convert the model's raw text Action into a structured tool call. A tool-calling model emits that structure directly — each entry in the message's `tool_calls` carries a `name` and an `args` dictionary — so there is no text left to parse and the component has no work to do. Four is the current count; if an older component list hands you five, the extra one is the parser. A figure that shows stopping criteria as a fifth row is counting something else again — the rule that ends the loop, not a part of the runtime.
- **Tool registry function:** Maps tool names (as strings) to tool objects (description + callable); the model reads those descriptions — for a `@tool` function the description is its docstring, unless an explicit `description=` overrides it — and selects a tool by naming it in a tool call.
- **Tool failure handling:** Structured tool calls remove the text-parsing failure mode, but not tool failure. A tool that raises lets the exception propagate out of the agent and end the run, so the user gets a traceback and no answer. A production tool catches its own errors and returns a description of the failure, which reaches the model as an ordinary observation it can reason about — retrying with different arguments, switching tools, or reporting the limitation.

### Part B: Tool Description Design

**Reading Focus Questions**

1. The chapter lesson identifies five questions that an effective tool description must answer. State all five. For each, explain the failure mode that results from omitting it.

2. A tool description includes the clause: "Do not use this tool for math calculations." What class of failure does this scope boundary clause prevent, and what would a ReAct agent do without it?

3. The lesson states that "ambiguous argument specifications produce hallucinated values, especially for structured data types." Construct a concrete example: write an ambiguous argument specification for a date parameter, and explain what the agent would likely hallucinate.

**Key Concepts to Extract**

- **Five tool description questions and their omission failure modes:**
    1. *What does it do?* — Omission: agent cannot determine whether this tool is relevant to the current sub-task.
    2. *When should the agent use it?* — Omission: agent selects the tool in inappropriate contexts (over-invocation or under-invocation).
    3. *What arguments does it require?* — Omission: agent hallucinates argument values, especially for structured types (dates, IDs, JSON schemas).
    4. *What does the output look like?* — Omission: agent misparses the tool's response and uses incorrect values in subsequent reasoning.
    5. *What errors can it produce?* — Omission: agent silently misinterprets error responses as valid data, propagating errors into the final answer.
- **Scope boundary clause:** Prevents over-invocation — the agent selecting a tool for a task within its superficial domain but outside its intended scope.
- **Hallucinated argument value:** An agent-generated value for a parameter that is formally valid (passes type checking) but semantically incorrect because the specification was ambiguous.

**Synthesis Task**

Write a complete tool description for a hypothetical "company database lookup" tool, answering all five questions. Then write a deliberately degraded version that omits the scope boundary clause and has an ambiguous argument specification. In one paragraph, predict what failure behaviors the degraded description would produce in a live ReAct agent.

## Reading Guide 3 — Chapter 3: Reasoning Trace Interpretation and Critique { #reading-guide-3 }

**Sources (no new numbered reading assigned — draws on previously assigned readings and lesson content):**

- Yao, S., et al. (2022). ReAct. Sections 1–2 (already read in Guide 1B).
- The streamed agent trace printed by the `show_trace` helper in Lab Exercise Step 1 (`REASONING`, `TOOL CALL`, `ARGUMENTS`, `OBSERVATION`, `ANSWER` lines).
- Zhou, A., et al. (2023). LATS. Section 1 (accessible from Chapter 1 lesson).
- Chapter 3 lesson content: Five Classes of Reasoning Trace Failure (reference the lesson table directly).

### Part A: What Is a Reasoning Trace?

**Reading Focus Questions**

1. The chapter lesson defines a reasoning trace as "the complete log of an agent's internal reasoning steps, tool calls, and tool observations during the execution of a task." In the streamed trace the lab's `show_trace` helper prints, which specific labeled lines constitute the reasoning trace? List them in order, and say which one may legitimately be missing from a correct run that did call a tool.

2. The lesson states that in production systems "the reasoning trace is the primary diagnostic artifact when an agent fails to produce correct output." What does this mean for system design — specifically, what must be true about logging configuration for a production deployment to be diagnosable?

3. Re-read the ReAct paper's description of the Thought-Action-Observation cycle (already read in Guide 1B). How does the trace structure map to this cycle — that is, where in a real streamed trace would you locate each of the three phases, given that a model calling tools natively never writes the words "Thought:", "Action:" or "Observation:"?

**Key Concepts to Extract**

- **Reasoning trace elements (in order):** `REASONING:` (the model's own text, printed only when it chooses to narrate — frequently absent, and its absence is not a fault) → `TOOL CALL:` (the tool name) → `ARGUMENTS:` (the argument dictionary) → `OBSERVATION:` (the content the tool returned), repeated per loop iteration → `ANSWER:` (the last model message, the one that requests no tools).
- **Production diagnostic requirement:** There is no `verbose=True` switch to turn on any more. The agent must be streamed (`agent.stream(..., stream_mode="updates")`) or otherwise instrumented so that every tool call, its arguments and the content the tool returned are recorded; a deployment that logs only the final answer cannot be diagnosed post-failure.
- **Trace-to-cycle mapping:** Thought phase = the model message's own `content` (the `REASONING:` line), which the model may omit entirely; Action phase = `tool_call["name"]` plus `tool_call["args"]` (the `TOOL CALL:` and `ARGUMENTS:` lines); Observation phase = the tool message's `content` (the `OBSERVATION:` line).

### Part B: The Five Classes of Reasoning Trace Failure

**Reading Focus Questions**

1. The chapter lesson identifies five distinguishable failure classes. For each class, state: (a) the class name, (b) where in the trace the failure manifests, (c) the root cause, and (d) the corrective intervention.

2. Two failure classes involve incorrect tool invocation but have different root causes. Identify both classes and explain how a trace analyst distinguishes between them — that is, what specific evidence in the trace indicates which class applies.

3. One failure class produces a trace that appears complete and correctly structured — all phases are present, no errors are logged — yet the final answer is wrong. Identify this class and explain why a trace that looks correct can produce an incorrect output.

**Key Concepts to Extract**

- **Five failure classes (derived from Chapter 3 lesson):**
    1. *Incorrect tool selection* — The `TOOL CALL` line names the wrong tool for the sub-task. Root cause: tool description ambiguity or missing scope boundary. Fix: revise tool description.
    2. *Malformed tool call* — `TOOL CALL` names the correct tool but `ARGUMENTS` carries incorrect or malformed values. Root cause: ambiguous argument specification. Fix: clarify argument format and constraints in tool description.
    3. *Observation misinterpretation* — Correct tool is called with correct arguments and the `OBSERVATION` line shows a correct result, but the model's next message misreads it and draws an incorrect inference. Root cause: output format not described or agent not instructed on how to parse it. Fix: add output format description and parsing instructions.
    4. *Premature termination* — Agent returns an answer message with no tool calls before the reasoning task is complete (e.g., after the first tool call, regardless of whether sufficient information has been retrieved). Root cause: stopping condition is triggered too early; the demonstrations do not show multi-step loops. Fix: add demonstrations of multi-loop reasoning. Separately, check whether the run was cut short by the `recursion_limit` config key, which replaced the old `max_iterations` argument.
    5. *Hallucination in Thought* — The agent asserts a false fact in its own text — the `REASONING:` line, or the answer itself — as though a tool had returned it, when no `OBSERVATION` line contains it. Root cause: parametric memory override — the LLM inserts training knowledge as if it were a retrieved fact. Fix: strengthen tool use instructions; require grounding of all factual claims in an Observation.
- **Distinguishing incorrect tool selection vs. malformed tool call:** Incorrect tool selection is visible on the `TOOL CALL` line (wrong tool name); a malformed tool call shows the correct name on `TOOL CALL` but wrong content on `ARGUMENTS`.
- **Trace-complete failure class:** Hallucination in Thought — every step of the trace is well formed and no error is logged, but the model's text contains an asserted fact that no `OBSERVATION` line ever returned.

**Synthesis Task**

Given the following abbreviated trace, classify the failure, identify its root cause, and prescribe a structural fix:

```text
[1] REASONING:  I need to find the current GDP of Brazil.
[1] TOOL CALL:  web_search
[1] ARGUMENTS:  {'query': 'Brazil GDP'}
[1] OBSERVATION: Brazil GDP 2023: $2.08 trillion (World Bank)
[final] ANSWER:  Brazil's GDP is $2.08 trillion. From what I know, its inflation rate in 2023 was 4.6%.
```

??? success "Answer"

    Hallucination in Thought — the only `OBSERVATION` in the trace returned a GDP figure and nothing else, so the 4.6% inflation rate came from the model's parametric memory, which the answer all but admits with "From what I know". It is not premature termination: the agent did not stop short, it answered in full and sourced part of that answer from memory instead of a tool — premature termination means stopping before enough was gathered, hallucination means asserting what was never gathered. The trace is otherwise well formed: one tool call, one observation, one answer, no error. Fix: add a system instruction requiring that every numerical claim be grounded in a tool result, and read traces by checking each figure in the answer against the observations above it.

## Reading Guide 4 — Chapter 4: Prompt Engineering for Agent Behavioral Control { #reading-guide-4 }

**Assigned Reading:**

- Reading 7: Liu, P., et al. (2023). *Pre-train, prompt, and predict: A systematic survey of prompting methods in NLP.* ACM Computing Surveys, 55(9). Read: Section 3 (A Formal Description of Prompting) + Section 4 (Prompt Engineering). Focus: four-component prompt architecture and cross-mapping to the four agent prompt engineering dimensions of Part B (system instructions, tool descriptions, few-shot CoT scaffolds, output format constraints).

*(Reference readings: Brown et al. 2020, Wei et al. 2022 — revisit as needed for few-shot context; the LangChain [Agents guide](https://docs.langchain.com/oss/python/langchain/agents){target=_blank} on the `system_prompt` argument to `create_agent`.)*

### Part A: Liu et al.'s Four-Component Prompt Taxonomy

**Scope:** Section 3 (Formal Description) + Section 4 (Prompt Engineering).

**Reading Focus Questions**

1. Liu et al. describe four components of a complete prompt: **instruction**, **context**, **input indicator**, and **output indicator**. Define each component precisely using Liu et al.'s language. What does each component contribute to the model's behavior?

2. Liu et al. distinguish between "hard prompts" (fixed token sequences) and "soft prompts" (learnable continuous embeddings). For the purposes of agent system design, which category applies to system instructions and few-shot demonstrations, and why does this distinction matter for deployment?

3. The chapter lesson assigns a cross-mapping task: map Liu et al.'s four-component taxonomy to the four agent prompt engineering dimensions (system instructions, tool descriptions, few-shot CoT scaffolds, output format constraints). Complete this mapping explicitly, justifying each correspondence.

**Key Concepts to Extract**

- **Four Liu et al. components:**
    - *Instruction:* The directive that specifies what the model should do — the task specification component.
    - *Context:* Background information provided to the model to ground its response — retrieved documents, prior conversation, domain knowledge.
    - *Input indicator:* The marker or framing that identifies where the model's input begins (the query or task instance to be solved in this call).
    - *Output indicator:* The specification of the desired output format, structure, or type.
- **Hard prompts in agent design:** System instructions and few-shot demonstrations are hard prompts — fixed token sequences in the model's context. This means they consume context window tokens and must be concise.
- **Cross-mapping (Liu et al. → Agent dimensions):**
    - *Instruction → System instructions:* The agent's role, behavioral constraints, and task scope.
    - *Context → Tool descriptions + few-shot CoT scaffolds:* Tool descriptions provide the agent's operational context; few-shot examples provide reasoning-pattern context.
    - *Input indicator → User query / task input:* The specific task the agent must solve in this invocation.
    - *Output indicator → Output format constraints:* The required structure of the agent's final answer message (section headers, citation format, word count, confidence levels).

### Part B: Four Dimensions of Agent Prompt Engineering

**Reading Focus Questions**

1. The chapter lesson identifies four independently configurable dimensions of agent prompt engineering. List all four. For each, give one concrete example of what specifying that dimension correctly achieves, and one example of what omitting or mis-specifying it produces.

2. The lesson contains the note: "A common error in agent development is to treat behavioral problems as prompting problems — adding a sentence to the system prompt when the agent does something unintended." Why is this approach described as accumulating "fragile constraints"? What structural property of LLM prompts makes this fragility predictable?

3. The Hands-On Project requires a system instruction of minimum 150 words covering: agent role, behavioral constraints (at least two prohibitions), output format, and ethical boundary. How does this four-part structure map to Liu et al.'s taxonomy? Which component of Liu et al.'s taxonomy is most represented by the ethical boundary specification?

**Key Concepts to Extract**

- **Four agent prompt engineering dimensions:**
    1. *System instructions:* Role identity, professional framing, behavioral constraints, ethical boundaries — what the agent knows about itself and its limits.
    2. *Tool descriptions:* Operational specification of each available tool — the agent's action vocabulary.
    3. *Few-shot CoT scaffolds:* Worked exchanges placed in the message list ahead of the real question — a user turn, the assistant's tool call, the tool's result, and the answer that followed — which the model reads as precedent for its own loop.
    4. *Output format constraints:* Required structure, length, citation format, or confidence framing for the final answer.
- **Fragility of accumulated constraints:** LLMs do not apply prompt constraints with equal weight across all tokens; constraints added later in a long system prompt may be overshadowed by earlier instructions or by strong in-context patterns. Accumulated constraints interact unpredictably — a new prohibition may inadvertently suppress a behavior that was previously working correctly.
- **Behavioral control as architecture:** Behavioral boundaries defined at design time, tested systematically, and instrumented in production are more reliable than reactive prompt patches.

**Synthesis Task**

Write the complete cross-mapping table in your notes:

| Liu et al. Component | Agent Prompt Dimension | Example in Agent Context |
|---|---|---|
| Instruction | System instructions | "You are a senior legal analyst. Do not provide legal advice." |
| Context | Tool descriptions + few-shot scaffolds | Web search tool docstring + a worked tool call → tool result → answer exchange |
| Input indicator | User query | "Review this contract for non-compete clauses." |
| Output indicator | Output format constraints | "Your final answer must contain: Summary (≤100 words), Risk Level (High/Med/Low), Citations." |

Verify that every cell is filled from Liu et al.'s text and the lesson content — not from your prior knowledge.

## Reading Guide 5 — Chapter 5: Architectural Trade-off Assessment for Production Deployment { #reading-guide-5 }

**Sources (no new numbered reading assigned — draws on lesson content + prior readings and EU AI Act reference):**

- Chapter 5 lesson: Six-Dimensions Trade-Off Assessment framework + EU AI Act (2024) Article 13.
- Synthesize from all four prior paradigm readings (Wei et al. 2022, Yao et al. 2022 — ReAct, Yao et al. 2023 — ToT, Zhou et al. 2023 — LATS) and the four-paradigm comparative table from Chapter 1.

### Part A: The Six Dimensions of Trade-Off Assessment

**Reading Focus Questions**

1. The chapter lesson introduces a six-dimension framework for architectural selection in professional practice. Identify all six dimensions. For each dimension, describe what a practitioner must specify or evaluate to complete the assessment for that dimension.

2. The lesson states that architectural selection "is a multi-objective optimization problem." What makes it a multi-objective problem rather than a single-objective one — that is, why can no single paradigm be declared "best" independent of context?

3. Apply the six-dimension framework to a concrete scenario: an agent deployed as a customer support tool for a high-volume SaaS product, answering billing and subscription questions 24/7. Which paradigm would the framework most likely support, and across which two dimensions would the evidence be most decisive?

**Key Concepts to Extract**

- **Six assessment dimensions (from the lesson's table and text):**
    1. *Task complexity* — Number and interdependency of sub-tasks; whether backtracking capability is needed.
    2. *Inference cost* — Total token budget per query; whether per-query cost constraints are strict.
    3. *Latency requirements* — Time-to-response constraint; whether branching search latency is acceptable.
    4. *External information needs* — Whether the task requires real-time retrieval during reasoning (rules out CoT).
    5. *Interpretability requirements* — Whether the reasoning trace must be auditable by operators or regulators.
    6. *Deployment risk profile* — Whether the domain is high-risk (triggering regulatory requirements such as EU AI Act Article 13).
- **Multi-objective nature:** Different deployment contexts impose conflicting constraints — a high-accuracy medical reasoning task may require LATS (high cost, high interpretability requirement), while a high-volume customer service task requires ReAct (low cost, low latency, good enough accuracy). No paradigm dominates across all six dimensions simultaneously.

### Part B: EU AI Act Article 13 and Interpretability Requirements

**Reading Focus Questions**

1. The chapter lesson cites EU AI Act (2024) Article 13, which requires that high-risk AI systems provide output that is "sufficiently transparent" to enable operators to understand and interpret the system's outputs. What constitutes a "high-risk AI system" in the Act's scope, and give three examples of agent deployment domains that would trigger this classification.

2. The lesson states that "a LATS agent operating in a high-risk domain may face regulatory scrutiny that a ReAct agent would not, precisely because the branching trace is harder to audit." What property of the LATS trace makes it harder to audit than a ReAct trace, and what would a practitioner need to add to a LATS deployment to meet Article 13's transparency requirement?

3. A practitioner argues: "We should always use ReAct because it is more interpretable and therefore safer under the AI Act." What is the flaw in this reasoning, and what would a correct application of the six-dimension framework say in response?

**Key Concepts to Extract**

- **High-risk AI systems (EU AI Act scope):** Systems deployed in domains including healthcare decision support, legal document processing, financial analysis, employment screening, biometric identification — domains where incorrect outputs cause significant harm to individuals.
- **LATS trace auditability challenge:** A LATS trace contains multiple branching paths, evaluation scores at each node, and backtracking decisions — an operator must understand the tree structure, not just a linear chain, to audit the reasoning. This is substantially more complex than a linear ReAct trace.
- **Article 13 compliance for LATS:** Requires structured trace logging that records the full tree (not just the selected path), evaluation scores, and the reason each branch was or was not selected.
- **Flaw in "always ReAct":** Interpretability is one of six dimensions. A task that requires deliberate planning over a large state space may produce systematically wrong answers with ReAct — and a wrong answer from a more interpretable system is not safer than a correct answer from a less interpretable one. The six-dimension framework requires evaluating all dimensions, not optimizing a single dimension in isolation.

**Synthesis Task**

Complete a six-row Architectural Specification Brief in your notes:

| Dimension | Scenario A: Customer Support Bot | Scenario B: Medical Literature Synthesis Agent |
|---|---|---|
| Task complexity | Low — FAQ-style, no backtracking | High — multi-hypothesis, requires backtracking |
| Inference cost | Strict — millions of queries/day | Flexible — low query volume, high value per query |
| Latency | Strict — &lt;2s response required | Flexible — minutes acceptable |
| External info needs | Yes — live account data | Yes — live medical literature |
| Interpretability | Low — no regulatory requirement | High — EU AI Act Article 13 applicable |
| Deployment risk profile | Low | High |
| **Recommended paradigm** | **ReAct** | **LATS (with structured trace logging)** |

Use this table as your primary study artifact for Chapter 5 quiz preparation. Verify that your paradigm recommendations are consistent with the four-paradigm comparative table from Reading Guide 1.

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2.2-Addendum){target=_blank} (wiki page last changed 2026-08-06). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-2/reading-guides.md){target=_blank}.</p>
