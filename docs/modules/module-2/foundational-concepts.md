---
title: 'Module 2: Foundational Concepts'
description: 'Five-chapter lesson on how LLM-based agents reason and act: the CoT/ReAct/Tree-of-Thoughts/LATS paradigms, LangChain tool integration, reasoning-trace failure analysis, prompt engineering for behavioral control, and architectural trade-offs.'
type: Lesson
tags:
- module-2
- student-facing
- lesson
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
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2:-Foundational-Concepts
  title: 'AI Automation and Agents v2 wiki: Module-2:-Foundational-Concepts'
  author: Michele Cosi; Michelle Yung; Carlos Lizárraga-Celaya
  last_modified: '2026-08-04T06:47:49-07:00'
authorship:
  created: '2026-05-10'
  updated: '2026-08-03'
  contributors:
  - C. Lizárraga
  - M. Yung
wiki_page: Module-2:-Foundational-Concepts
---
# Module 2: Foundational Concepts

![An architect's guide to agents](../../assets/images/Architects-Guide-to-Agents.png){ width="900" }

Now that we know what agents are, we move on to the next question: how do modern LLM-based agents
actually reason and act? 

The Module 2 readings introduce five interconnected frameworks that
form the technical and analytical vocabulary of contemporary LLM-based agent design.
These frameworks address:

- How agents reason (Chain-of-Thought, ReAct, Tree of Thoughts, LATS)
- How they act through tools (`create_agent` architecture)
- How their reasoning can be interpreted and critiqued (trace analysis)
- How their behavior can be shaped through language (prompt engineering)
- How competing architectural choices are evaluated for production deployment (trade-off assessment)

## Chapter 1: The Four Agent Reasoning Paradigms

### Chapter 1 Lesson

*Estimated time: ~18 min*

The four reasoning paradigms in Module 2 represent a developmental arc in the field: each
addresses specific limitations exposed by its predecessor. Understanding this arc - not merely
the techniques themselves - is the key to knowing when each paradigm is appropriate. The
progression from CoT to LATS is a progression from linear to branching, from reactive to
deliberate, and from low-cost to high-cost reasoning.

**Paradigm 1: Chain-of-Thought Prompting (Wei et al., 2022)**

Wei et al. (2022) demonstrated that prompting large language models to produce intermediate
reasoning steps - a chain of thought - substantially improves performance on complex
reasoning tasks including arithmetic, commonsense reasoning, and symbolic manipulation. The
critical finding is that this capacity is emergent: it is absent in smaller models and appears only
above a scale threshold, suggesting that chain-of-thought reasoning reflects a qualitative
capability transition rather than a continuous improvement curve.

| Dimension | Chain-of-Thought Characteristics |
| --- | --- |
| **Core mechanism** | Decompose the problem into a linear sequence of intermediate reasoning steps before producing the final answer. |
| **Prompting approach** | Few-shot examples where each example includes the reasoning chain (thought steps) followed by the answer, OR zero-shot 'Let's think step by step.' |
| **Key strength** | Dramatically improves multi-step arithmetic, commonsense reasoning, and symbolic tasks. Low computational overhead — produces one reasoning chain per query. |
| **Key limitation** | Linear: once a reasoning step is committed to, the model cannot backtrack. If an early step contains an error, subsequent reasoning inherits and compounds it. No mechanism for exploration of alternatives. |
| **When to use** | Problems with a natural linear decomposition, where intermediate steps are checkable or low-stakes, and where computational cost is a primary constraint. |

**Paradigm 2: ReAct - Synergizing Reasoning and Acting (Yao et al., 2022)**

Yao et al. (2022) introduced ReAct as a solution to the fundamental limitation that chain-of-thought
operates entirely within the model's internal knowledge - it cannot access external information
during reasoning. ReAct interleaves reasoning steps (Thought) with actions (Act) and observation
of action outputs (Observe), creating a three-phase cycle that grounds reasoning in real-world
information retrieved during the task.

| ReAct Phase | What Happens in This Phase |
| --- | --- |
| **THOUGHT** | The agent produces an internal reasoning step: what does it know, what does it need, what is its next action plan? This step is natural language — no tool is called. |
| **ACT** | The agent issues a tool call — a web search, a calculator invocation, a database query, a file read. The action is specified using a structured format that the tool interface can parse. |
| **OBSERVE** | The agent receives the tool output and incorporates it into its context. The observation becomes the input for the next Thought step, creating a closed reasoning-acting loop. |

The ReAct loop is the default reasoning architecture for production agents today. The ability to read and diagnose a ReAct trace - identifying which piece of reasoning was faulty, which tool call was incorrectly specified, or which observation was misinterpreted - is the core diagnostic skill of Module 2. Thought, Act and Observe are the paper's names for the three phases, not labels a current agent prints: the Module 2 lab prints the same three steps as `REASONING:`, `TOOL CALL:` / `ARGUMENTS:` and `OBSERVATION:` lines.

**Paradigm 3: Tree of Thoughts (Yao et al., 2023)**

Yao et al. (2023) identified a fundamental limitation of ReAct for complex, open-ended problems:
the linear thought-action-observe cycle commits to a single path and cannot recover gracefully
from dead ends. Tree of Thoughts (ToT) replaces the linear chain with a deliberate search over
a tree of coherent language sequences (thoughts), where the model generates multiple candidate
reasoning paths, evaluates them using a heuristic or the model itself, and selects the most
promising path to explore - with backtracking.

!!! note "When Tree of Thoughts is Justified"

    ToT incurs substantially higher computational cost than CoT or ReAct - it requires generating
    and evaluating multiple reasoning branches per step, which multiplies inference costs. ToT is
    justified when: (1) the problem has a large state space with many possible solution paths; (2)
    intermediate states can be meaningfully evaluated before the full solution is known; (3)
    backtracking is necessary because early commitment to a wrong path is catastrophically
    costly; and (4) computational budget and latency are not primary constraints. Canonical use
    cases include planning problems, multi-step mathematical proof construction, and creative
    generation tasks with complex constraint satisfaction.

**Paradigm 4: Language Agent Tree Search (Zhou et al., 2023)**

Zhou et al. (2023) proposed LATS (Language Agent Tree Search) as a unifying framework that
integrates the deliberate search of ToT with the grounded tool use of ReAct and a reinforcement
learning-inspired self-reflection mechanism. In LATS, each node in the search tree represents not
just a thought but a complete action-observation pair - the agent acts in the world at each search
node and uses the observation to evaluate node quality. This enables the system to ground its
deliberate search in real-world feedback rather than purely internal model judgment.
The cost of LATS is commensurate with its power: it requires many more LLM calls per task, more
complex state management, and more sophisticated evaluation logic. LATS is the current state
of the art for tasks that require both deliberate planning over a large state space AND real-world
information retrieval during search. Most production systems today use ReAct for cost reasons;
LATS represents the frontier of what is possible when cost and latency constraints permit.

**The Four-Paradigm Comparative Framework**

The following table enables side-by-side evaluation across the five dimensions that determine
architectural selection in professional practice:

| Dimension | CoT | ReAct | ToT | LATS |
| --- | --- | --- | --- | --- |
| **Reasoning structure** | Linear chain — one path, committed at each step | Interleaved Thought-Act-Observe cycles | Branching tree — multiple paths explored and pruned | Tree search with real-world tool use at each node |
| **Tool use** | None — operates on internal knowledge only | Yes — tool calls interleaved with reasoning | Not inherent — can be added but not the core architecture | Yes — tool use IS the tree expansion mechanism |
| **Backtracking** | No — errors propagate forward | No — linear like CoT, just grounded | Yes — key feature: prune and backtrack | Yes — core capability |
| **Computational cost** | Low — one reasoning pass per query | Medium — proportional to number of tool calls | High — proportional to tree breadth × depth | Very high — tree breadth × depth × tool calls |
| **Best problem type** | Structured, decomposable, linear | Grounded fact-finding, QA with external sources, multi-step task execution | Open-ended planning, constraint satisfaction, proof construction | Complex planning requiring external information at each decision point |
| **Hallucination risk** | High — no grounding in external facts | Low — observations ground each reasoning step | Medium — internal evaluation may be unreliable | Low — external observations ground evaluations |
| **Interpretability** | High — trace is a natural language argument | High — trace shows exact tool calls and outcomes | Moderate — tree structure adds complexity | Low — tree plus tool use plus self-reflection is complex |

### Learning Resources
* Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., ... & Zhou, D. (2022). [Chain-of-thought prompting elicits reasoning in large language models](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf){target=_blank}. Advances in neural information processing systems, 35, 24824-24837.
* Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). [ReAct: Synergizing reasoning and acting in language models](https://arxiv.org/pdf/2210.03629){target=_blank}. arXiv preprint arXiv:2210.03629.
* Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T., Cao, Y., & Narasimhan, K. (2023). [Tree of thoughts: Deliberate problem solving with large language models](https://proceedings.neurips.cc/paper_files/paper/2023/file/271db9922b8d1f4dd7aaef84ed5ac703-Paper-Conference.pdf){target=_blank}. Advances in neural information processing systems, 36, 11809-11822.
* Zhou, A., Yan, K., Shlapentokh-Rothman, M., Wang, H., & Wang, Y. X. (2023). [Language agent tree search unifies reasoning acting and planning in language models](https://arxiv.org/pdf/2310.04406){target=_blank}. arXiv preprint arXiv:2310.04406

**Reading 1 — Chain of Thought Prompting [~ 10 min]**

* Wei, J. et al. (2022). [Chain-of-thought prompting elicits reasoning in large language
models](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf){target=_blank}. NeurIPS 2022. 
  * Read: Abstract + Section 2 (Chain-of-Thought Prompting) and Figure 1. You may skim Section 4 (Experimental Setup) but are not required to read it in full.
  * Extract: What is a reasoning trace in the CoT sense? What does CoT add to
standard few-shot prompting? What task class shows the largest CoT benefit, and
why?

**Reading 2 — ReAct: Reason + Act [~ 12 min]**

* Yao, S. et al. (2022). [ReAct: Synergizing reasoning and acting in language models](https://arxiv.org/pdf/2210.03629){target=_blank}.
ICLR 2023. 
   * Read: Sections 1 and 2 (Introduction + ReAct: Synergizing Reasoning and Acting). 
   * Extract: How does ReAct differ structurally from CoT? What is the Thought/Action/Observation cycle? When does the loop terminate?

### Chapter 1 Quiz

[Take the Chapter 1 quiz](chapter-quizzes.md#chapter-1-quiz){ .md-button }

## Chapter 2: Tool Integration Architecture

### Chapter 2 Lesson

*Estimated time: ~14 min*

Tool use is what separates an AI agent from an LLM. An LLM without tools operates on the
knowledge encoded in its parameters during training - frozen at its training cutoff, unable to
access external systems, and capable only of text generation. An agent with tools can retrieve
live information, execute code, write to databases, send communications, and interact with APIs.
However, tool integration introduces a new class of failure modes that are distinct from LLM
reasoning failures and require different diagnostic approaches.

**The `create_agent` Factory (LangChain)**

LangChain's `create_agent` is the current production API for constructing multi-tool ReAct agents. It replaces the legacy `AgentExecutor` class with a cleaner factory function that integrates directly with LangGraph's stateful execution graph. `create_agent` accepts five primary parameters — constructor arguments, not the agent's structural components — and returns a compiled, runnable agent:

* **`model`** — a chat model instance (e.g., `ChatOpenAI`, `ChatAnthropic`) or a model identifier string. This is the LLM backbone that drives all reasoning steps.
* **`tools`** — a sequence of `BaseTool` objects, callables, or tool-specification dicts. The agent's tool registry is constructed from this sequence; tool descriptions embedded in each `BaseTool` are used for selection at inference time.
* **`system_prompt`** — an optional string or `SystemMessage` that injects persistent behavioral instructions before any user turn. This is the primary mechanism for role definition, output format constraints, and ethical boundaries.
* **`middleware`** — an optional sequence of `AgentMiddleware` objects for observability, tracing, and logging. Middleware intercepts each reasoning step without modifying agent logic, enabling production monitoring without altering behavior.
* **`response_format`** — an optional structured output specification (Pydantic model, type, or schema dict) that constrains the agent's final response to a defined schema. When set, that schema is imposed on the model's own output rather than recovered afterwards from text by an output parser. That is the general pattern in a tool-calling agent: an action comes back as a structured call — each entry in the message's `tool_calls` carries a `name` and an `args` dictionary — so there is nothing left for a parsing component to convert.

The agent returned by `create_agent` is a compiled graph that runs the ReAct loop internally: invoke it with `{"messages": [...]}` and it repeats a reasoning → tool call → observation cycle until the model returns a message that requests no tools. That message ends the run and carries the final answer, which you read from `result["messages"][-1].content`; the step cap is the `recursion_limit` config key. Unlike `AgentExecutor`, state management, loop control, and tool dispatch are handled by the underlying LangGraph execution graph — making the agent inherently compatible with checkpointing, streaming, and multi-agent orchestration. *Thought*, *Action* and *Observation* are the ReAct paper's names for the phases of that cycle, not labels the agent emits — the model's message carries structured `tool_calls`, and it is the Module 2 lab's `show_trace` helper that gives the steps printable names (`REASONING:` — only when the model narrates before calling — then `TOOL CALL:`, `ARGUMENTS:`, `OBSERVATION:` and `[final] ANSWER:`).

**The agent runtime.** Four structural components, and the loop that connects them:

```mermaid
flowchart TD
    IN["User message"] --> STATE["Memory Module"]
    STATE --> LLM["LLM Backbone"]
    LLM --> Q{"Requests a tool?"}
    Q -- no --> OUT["Final answer"]
    Q -- yes --> EXEC["Action Executor"]
    EXEC --> OBS["Observation"]
    OBS --> STATE
    REG["Tool Registry"] -- descriptions --> LLM
    REG -- callables --> EXEC
```

| Component | Role and design considerations |
| --- | --- |
| **LLM Backbone** | The reasoning core. Reads the system prompt, the message state and the tool descriptions, then produces either a tool call or a final answer. It never runs a tool itself: it names one and supplies the arguments. |
| **Tool Registry** | The registered tools, each with a description and an input schema. The model reads the descriptions to choose; for a `@tool` function the description is its docstring unless an explicit `description=` overrides it. Description quality is the single largest determinant of reliable tool use — ambiguous or incomplete descriptions produce wrong choices and invented arguments. |
| **Action Executor** | Runs the tool the model named, with the arguments it supplied, and appends the result to the state as an observation. A tool that raises propagates out and ends the run, so a production tool catches its own errors and returns them as text the model can reason about. |
| **Memory Module** | The running message state: the conversation, every tool call and every observation. Each pass of the loop sees what the previous passes produced. Pass a `checkpointer` to `create_agent` to persist it across invocations. |

**Stopping is a rule, not a component.** The loop ends when the model returns a message that requests no tools, and that message carries the final answer; the step cap is the `recursion_limit` config key. The LangChain 0.x design listed three stopping conditions instead — a "Final Answer" token, a maximum-iteration argument and a parsing-error threshold — and the current API has none of them. The first two are replaced by the rule and the config key above. The third has nothing left to act on: a tool-calling model emits the structured call directly, so no component parses text into an action.

**Older tutorials use different names.** Material written against the `AgentExecutor` that LangChain 1.0 removed calls these four *Agent (the LLM)*, *Tool Descriptions*, *Tool Executor* and *Memory / State*. Those component lists often run to five, and the extra entry is one of two things: an output parser, which a tool-calling model makes unnecessary, or stopping criteria, which is the loop rule above rather than a part of the runtime.

**Tool Description Design - The Specification Discipline**

Tool descriptions are the contract between the agent and the tool ecosystem. An effective tool
description answers five questions precisely:

* **What does this tool do?** State the tool's function in one sentence using active verbs and
concrete output types. Example: 'Searches the web and returns the top-5 result snippets for a
given query string.'

* **When should the agent use it?** Specify the conditions under which this tool is appropriate, and
explicitly note conditions where it is NOT appropriate. This prevents incorrect tool selection.

* **What arguments does it require?** List every argument with its type, format, and any
constraints. Ambiguous argument specifications produce hallucinated values, especially for
structured data types.

* **What does the output look like?** Describe the output format so the agent can parse it
correctly. If the tool returns JSON, describe the schema. If it returns plain text, describe its
structure.

* **What errors can it produce?** List the error states the tool may return and what the agent
should do on each error. Undocumented errors produce agents that silently misinterpret failure
states as data.

!!! note "THE HETEROGENEOUS TOOL ECOSYSTEM"

    Production agents rarely use a single tool type. A realistic tool set might include: a web search
    tool (retrieves live information), a Python REPL (executes code and returns output), a
    database tool (reads/writes structured data), a file tool (reads/writes documents), an email tool
    (sends communications), and a calendar tool (reads/modifies schedule data). Each tool type
    has distinct description requirements, argument schemas, error modes, and risk profiles. The
    skill of designing a cohesive, well-described heterogeneous tool set - where the agent
    reliably selects the right tool for each subtask - is the practical competency developed in
    Module 2's Guided Labs.

### Learning Resources

* LangChain Documentation - [`create_agent` API Reference](https://reference.langchain.com/python/langchain/agents/factory/create_agent){target=_blank}.
* LangChain Documentation - [Tool Creation Reference](https://docs.langchain.com/oss/python/langchain/tools){target=_blank}.
* Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). [Language models are few-shot learners](https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf){target=_blank}. Advances in neural information processing systems, 33, 1877-1901

**Reading 5 — LangChain `create_agent` [~10 min]**

* LangChain Documentation: [`create_agent` API Reference and Tool Creation
Reference](https://reference.langchain.com/python/langchain/agents/factory/create_agent){target=_blank}.
   * Read the entire `create_agent` API Reference section. Pay particular attention to: the role of the `tools` parameter in constructing the tool registry, how tool descriptions embedded in `BaseTool` objects are used for selection at inference time, and how `response_format` constrains the agent's output.

* **Video 2 — "[Understanding ReACT with LangChain](https://www.youtube.com/watch?v=Eug2clsLtFs){target=_blank}"** - Sam Witteveen (~22 min)
    * Watch focus: the conceptual distinction between CoT and ReAct and the observation integration step.
    * As you watch, map what you see in the video to the structural definitions from Reading 2. If the video uses a different term for the same concept, note both.

### Chapter 2 Quiz

[Take the Chapter 2 quiz](chapter-quizzes.md#chapter-2-quiz){ .md-button }

## Chapter 3: Reasoning Trace Interpretation and Critique

### Chapter 3 Lesson

*Estimated time: ~5 min*

A reasoning trace is the complete log of an agent's internal reasoning steps, tool calls, and tool
observations during the execution of a task. In production systems, the reasoning trace is the
primary diagnostic artifact when an agent fails to produce correct output. The ability to read a
reasoning trace analytically - identifying where reasoning deviated, why a tool call was incorrect,
and what change to the agent design would fix the failure - is a high-value professional
competency.

**The Five Classes of Reasoning Trace Failure**

Systematic trace analysis reveals that agent failures cluster into five distinguishable failure
classes, each with a different root cause and a different fix:

| Failure Class | Diagnostic Signature | Structural Fix |
| --- | --- | --- |
| **Hallucinated Tool Call** | The agent calls a tool that does not exist or calls a real tool with an argument that is not valid per the tool description. The executor returns an error or unexpected output. | Revise the tool description to make the tool's name, purpose, and argument schema unambiguous. Add negative examples if the agent confuses this tool with another. |
| **Premature Termination** | The agent produces a Final Answer token before completing the task — typically after a successful first tool call, incorrectly treating partial information as a complete answer. | Revise the system prompt to specify the termination condition explicitly. Add a rubric for what 'task complete' means in terms of observable outputs. |
| **Observation Misinterpretation** | The agent receives a valid tool output but misreads it — extracts the wrong field from a JSON response, misinterprets a numeric value, or confuses an error string with a data string. | Revise the tool description to specify the output format precisely. Add parsing instructions to the system prompt if the output format is complex. |
| **Infinite Loop** | The agent repeats the same tool call with the same or similar arguments across multiple iterations, never converging to a Final Answer. The observation does not resolve the agent's reasoning state. | Add a loop-detection stopping criterion. Revise the system prompt to specify what to do when a tool call does not resolve the current uncertainty. |
| **Logical Gap in Reasoning Chain** | The agent's Thought step contains a reasoning error — an incorrect inference, a false premise, or a misattributed observation — that propagates into subsequent tool selection or argument construction. | Add few-shot examples that demonstrate correct reasoning for this problem type. Consider switching to a more powerful base model or a more deliberate architecture (ToT or LATS) for complex reasoning problems. |

### Learning Materials

* Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). [ReAct: Synergizing reasoning and acting in language models](https://arxiv.org/pdf/2210.03629){target=_blank}. arXiv preprint arXiv:2210.03629.
* LangChain [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent){target=_blank} — the streamed step trace from `agent.stream(..., stream_mode="updates")`, which the Module 2 lab wraps in its `show_trace` helper. There is no `verbose=True` switch to turn on.
* Zhou, A., Yan, K., Shlapentokh-Rothman, M., Wang, H., & Wang, Y. X. (2023). [Language agent tree search unifies reasoning acting and planning in language models](https://arxiv.org/pdf/2310.04406){target=_blank}. arXiv preprint arXiv:2310.04406.

### Chapter 3 Quiz

[Take the Chapter 3 quiz](chapter-quizzes.md#chapter-3-quiz){ .md-button }

## Chapter 4: Prompt Engineering for Agent Behavioral Control

### Chapter 4 Lesson

*Estimated time: ~9 min*

For agents, prompt engineering is not the craft of writing better chatbot prompts. It is a design
discipline for specifying agent behavior across four dimensions: what the agent knows about its
role and constraints (system instructions), what tools the agent can use and how (tool
descriptions), what patterns of reasoning the agent should follow (few-shot CoT scaffolds), and
what format the agent's outputs must conform to (output format constraints). Each dimension is
independently configurable and independently contributes to agent reliability.

**The Four-Dimension Agent Prompt Architecture**

**Dimension 1: System Instructions**

The system prompt defines the agent's identity, role, operational domain, and constraints. Effective system instructions specify: what the agent is for (domain scope), what it is not for (negative scope — prevents the agent from attempting tasks outside its competency), what it must always do (standing behavioral requirements), and what it must never do (hard behavioral limits). Vague system instructions produce agents with unpredictable behavioral boundaries.

**Dimension 2: Tool Descriptions**

As detailed in Theme 2, tool descriptions function as the agent's mental model of its available capabilities. In the prompt architecture, tool descriptions are presented to the agent as a structured list immediately after the system instructions, before any conversation context. The order in which tools are listed can affect which tool the agent selects when multiple tools are plausible candidates for a given subtask — an empirical effect documented in LangChain's design guidance.

**Dimension 3: Few-Shot CoT Scaffolds**

Few-shot examples demonstrate correct reasoning patterns for the agent's task domain. Brown et al. (2020) established that in-context few-shot examples can elicit capabilities in LLMs that zero-shot prompting cannot. For agents, few-shot examples in the system prompt demonstrate: what a correct Thought step looks like for this problem type, how to select the right tool given a specific context, how to interpret the tool's output, and when to conclude versus continue the loop.

**Dimension 4: Output Format Constraints**

Agents must produce outputs in formats that the AgentExecutor can parse. Output format constraints in the system prompt specify: the exact JSON structure for tool call specifications, the token or string that signals task completion (Final Answer), the format of intermediate Thought steps, and any constraints on output length or content. Poorly specified output format constraints produce parsing errors that terminate the agent prematurely or cause the executor to misinterpret a reasoning step as a tool call.

!!! note "BEHAVIORAL CONTROL IS NOT A PATCH - IT IS AN ARCHITECTURE"

    A common error in agent development is to treat behavioral problems as prompting problems:
    when the agent does something unintended, the instinct is to add a sentence to the system
    prompt. This approach accumulates fragile constraints that interact unpredictably. The
    professional approach is to treat behavioral control as an architectural concern: define
    behavioral boundaries clearly at design time, test them systematically before deployment, and
    instrument the agent to detect and log behavioral violations in production. Module 2's hands-
    on project requires you to document three specific behavioral constraints and the prompting
    mechanism used to enforce each.

### Learning Materials

* Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). [Language models are few-shot learners](https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf){target=_blank}. Advances in neural information processing systems, 33, 1877-1901
* Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., ... & Zhou, D. (2022). [Chain-of-thought prompting elicits reasoning in large language models](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf){target=_blank}. Advances in neural information processing systems, 35, 24824-24837.
* LangChain [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent){target=_blank} `system_prompt` parameter design.

### Chapter 4 Quiz

[Take the Chapter 4 quiz](chapter-quizzes.md#chapter-4-quiz){ .md-button }

## Chapter 5: Architectural Trade-off Assessment for Production Deployment

### Chapter 5 Lesson

*Estimated time: ~7 min*

Selecting a reasoning architecture is not a purely technical decision. It is a multi-objective
optimization problem with six dimensions that professional practitioners must evaluate explicitly.
The Architectural Specification Brief produced in Module 2 must document your reasoning across
all six dimensions - not just the technical choice, but the evidence-based justification for that
choice given the specific problem context.

**The Six-Dimension Trade-off Assessment Framework**

| Dimension | Assessment Questions | Architecture Implications |
| --- | --- | --- |
| **Latency** | What is the acceptable response time for this use case? Is the agent operating in a real-time, near-real-time, or batch context? | CoT and ReAct have lower latency than ToT and LATS. High-latency architectures are inappropriate for real-time user-facing applications. |
| **Cost per Inference** | What is the per-query cost at the expected volume? Can the use case sustain the inference cost of multi-branch architectures? | CoT has lowest cost. ReAct cost scales with number of tool calls. ToT and LATS costs scale super linearly with tree depth and branching factor. |
| **Reliability and Error Rate** | What is the acceptable error rate? Is the problem type where linear reasoning produces frequent errors that branch-and-backtrack would prevent? | For structured, well-defined tasks, ReAct reliability is typically sufficient. For open-ended or highly constrained tasks, ToT or LATS reduce error rates at higher cost. |
| **Scalability** | What is the anticipated query volume and growth trajectory? How does the architecture scale with load? | Stateless architectures (CoT, ReAct) scale horizontally more easily. Stateful architectures (ToT, LATS) require more sophisticated state management infrastructure. |
| **Interpretability / Explainability** | Are there regulatory, organizational, or user requirements for explainability of agent decisions? Does the EU AI Act's Article 13 apply? | CoT and ReAct traces are highly interpretable. ToT and LATS traces are significantly more complex to audit. High-risk AI system deployments may require CoT or ReAct for regulatory compliance. |
| **Organizational Integration** | What are the data governance requirements? Who will maintain the system? What monitoring infrastructure is available? | Tool choices must align with data governance policies. The maintenance burden of ToT/LATS requires more sophisticated engineering capacity than CoT/ReAct. |

The European Parliament's AI Act (2024) is directly relevant to architectural choice for high-risk
AI systems. Article 13 of the Act requires that high-risk AI systems provide output that is
'sufficiently transparent' to enable the system's operators to understand and interpret the system's
outputs. For agent systems deployed in high-risk domains - healthcare decision support, legal
document processing, financial analysis - this interpretability requirement has direct implications
for architecture selection. A LATS agent operating in a high-risk domain may face regulatory
scrutiny that a ReAct agent would not, precisely because the branching trace is harder to audit.

### Learning Resources

* European Parliament (2024). [Regulation (EU) 2024/1689 — Artificial Intelligence Act](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689){target=_blank}. Read Title III, Chapter 2, Article 13 (Transparency and provision of information to deployers). The primary regulatory source cited in Chapter 5; directly governs interpretability requirements for high-risk AI systems.
* National Institute of Standards and Technology (2023). [AI Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf){target=_blank}. The U.S. federal framework for identifying, measuring, and managing AI risk across the system lifecycle — maps directly onto the safety/risk dimension of Chapter 5's six-dimension trade-off model.

### Chapter 5 Quiz

[Take the Chapter 5 quiz](chapter-quizzes.md#chapter-5-quiz){ .md-button }

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2:-Foundational-Concepts){target=_blank} (wiki page last changed 2026-08-04). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-2/foundational-concepts.md){target=_blank}.</p>
