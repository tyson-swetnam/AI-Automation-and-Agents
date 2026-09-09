---
title: Module 2 Self-Assessment Quizzes (Retired)
description: Five ungraded five-question self-assessment quizzes with answer keys for the Module 2 chapters; retired in favor of the chapter quizzes.
type: Assessment
tags:
- module-2
- student-facing
- quiz
- reasoning-paradigms
- react
- langchain
- tool-use
- prompt-engineering
- answer-key
- superseded
module: 2
status: deprecated
stale_after: '2027-09-01T00:00:00Z'
superseded_by: ../../modules/module-2/chapter-quizzes.md
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2.2-Addendum-%E2%80%90-OLD
  title: 'AI Automation and Agents v2 wiki: Module-2.2-Addendum-‐-OLD'
  author: Michelle Yung; Carlos Lizárraga-Celaya
  last_modified: '2026-08-06T06:28:19-07:00'
authorship:
  created: '2026-08-03'
  contributors:
  - C. Lizárraga
wiki_page: Module-2.2-Addendum-‐-OLD
---
# Module 2 Self-Assessment Quizzes (Retired)

!!! warning "Superseded"

    This page is kept for history. The current version is [Module 2 Chapter Quizzes](../../modules/module-2/chapter-quizzes.md).

Five quizzes of five questions each, one per chapter. Questions are multiple-choice with a single correct answer. Answer keys appear at the end of each quiz. These assessments are not graded; their purpose is to verify comprehension of the lesson content and assigned readings before proceeding to the chapter quiz.

## Quiz 1 — Chapter 1: The Four Agent Reasoning Paradigms

**Q1.** According to Wei et al. (2022), chain-of-thought reasoning in large language models is best characterized as:

- A) A fine-tuning technique that improves arithmetic accuracy by providing labeled solution steps during training
- B) An emergent capability that is absent in smaller models and appears only above a scale threshold
- C) A retrieval-augmented generation strategy that grounds model outputs in external document corpora
- D) A structured output format enforced through system-level prompt constraints at inference time

**Q2.** The primary structural innovation of ReAct (Yao et al., 2022) over chain-of-thought prompting is:

- A) The use of few-shot demonstrations to elicit longer and more detailed reasoning chains
- B) The interleaving of reasoning steps (Thought) with external tool actions (Act) and observed outcomes (Observe)
- C) The application of Monte Carlo Tree Search to steer autoregressive language model inference
- D) The replacement of greedy decoding with constrained beam search over a predefined action vocabulary

**Q3.** Tree of Thoughts (Yao et al., 2023) is most justified when which of the following conditions holds?

- A) The task requires sub-second inference latency in a high-throughput production environment
- B) The problem has a single, well-defined solution path that can be confirmed in one reasoning step
- C) Intermediate reasoning states can be meaningfully evaluated before the complete solution is known, and backtracking from dead ends is necessary
- D) The agent must integrate live external information at each reasoning step using tool invocation

**Q4.** In LATS (Zhou et al., 2023), each node in the search tree represents:

- A) A candidate system prompt variant evaluated by a separate critic model
- B) A complete action-observation pair in which the agent acts in the world and uses the resulting observation to assess node quality
- C) A discrete internal reasoning step generated without any external tool invocation
- D) A memory retrieval event from a vector database queried during deliberate search

**Q5.** Which of the following correctly ranks the four reasoning paradigms from lowest to highest computational cost per task?

- A) CoT < LATS < ReAct < ToT
- B) ReAct < CoT < ToT < LATS
- C) CoT < ReAct < ToT < LATS
- D) ToT < CoT < LATS < ReAct

??? note "Answer key — Quiz 1"

| Question | Answer | Rationale |
| :-- | :-- | :-- |
| Q1 | B | Wei et al. explicitly identify CoT as an emergent property absent below a scale threshold — not a fine-tuning or retrieval technique. |
| Q2 | B | ReAct's defining contribution is the Thought/Act/Observe cycle that grounds reasoning in real-world tool feedback unavailable to CoT. |
| Q3 | C | Chapter 1 states ToT is justified when intermediate states can be evaluated before the full solution is known and backtracking is necessary. Options A and D describe conditions favoring ReAct; B favors CoT. |
| Q4 | B | LATS nodes represent action-observation pairs, enabling real-world grounding of deliberate search — the mechanism that distinguishes LATS from ToT. |
| Q5 | C | CoT has no tool calls (lowest cost); ReAct adds one tool call per reasoning loop; ToT multiplies candidate branches; LATS adds real-world tool calls at every search node (highest cost). |

## Quiz 2 — Chapter 2: Tool Integration Architecture

**Q1.** In LangChain's `create_agent` factory, the `tools` parameter serves which primary architectural function?

- A) It defines the system-level behavioral constraints and ethical boundaries passed to the language model
- B) It constructs the tool registry from which the agent selects actions based on embedded tool descriptions at inference time
- C) It specifies the structured output schema that constrains the agent's final response format
- D) It configures the middleware pipeline for production-level observability and tracing

**Q2.** Which `create_agent` parameter is the primary mechanism for enforcing role definition, output format requirements, and ethical boundaries?

- A) `response_format`
- B) `middleware`
- C) `system_prompt`
- D) `state_schema`

**Q3.** An agent is equipped with a web search tool and a Python REPL. After the REPL's description is changed to the vague phrase "Use for advanced tasks," which failure mode is most likely to occur?

- A) The agent invokes the web search tool for arithmetic and computation tasks that should be handled by the REPL
- B) The agent exits the ReAct loop prematurely before producing a Final Answer
- C) The agent produces a hallucinated tool output without invoking either tool
- D) The `middleware` pipeline intercepts all REPL calls and silently reroutes them to the web search tool

**Q4.** According to the Tool Description Design framework in Chapter 2, which component is specifically designed to prevent over-invocation of a tool in a heterogeneous multi-tool setting?

- A) The purpose statement (one-sentence functional description using active verbs and concrete output types)
- B) The failure conditions listing (error states and recommended agent responses)
- C) The scope boundary clause ("Do not use this tool for...")
- D) The output type specification (format and schema of the tool's return value)

**Q5.** The key architectural distinction between `create_agent` and the legacy `AgentExecutor` is:

- A) `create_agent` natively supports a broader class of tool types, including database, email, and calendar tools
- B) `create_agent` returns a LangGraph-backed agent in which state management, loop control, and tool dispatch are handled by the underlying execution graph rather than manually orchestrated
- C) `create_agent` requires the developer to explicitly specify the ReAct loop termination condition and maximum iteration count
- D) `create_agent` eliminates the need for tool descriptions by using embedding-based similarity to match queries to tools at runtime

??? note "Answer key — Quiz 2"

| Question | Answer | Rationale |
| :-- | :-- | :-- |
| Q1 | B | The `tools` parameter populates the tool registry; tool descriptions embedded in each `BaseTool` are the mechanism for inference-time selection. |
| Q2 | C | `system_prompt` injects persistent behavioral instructions before any user turn — it is the primary behavioral control lever. |
| Q3 | A | Vague tool descriptions cause incorrect tool selection. An underspecified REPL description allows the agent to default to web search even for computation tasks. |
| Q4 | C | The scope boundary clause is explicitly identified in Chapter 2 as the mechanism that prevents over-invocation by excluding specific use cases. |
| Q5 | B | Chapter 2 states that unlike `AgentExecutor`, `create_agent` delegates state management and loop control to LangGraph's execution graph, enabling native compatibility with checkpointing, streaming, and multi-agent orchestration. |

## Quiz 3 — Chapter 3: Reasoning Trace Interpretation and Critique

**Q1.** In the context of production LLM-based agent systems, a reasoning trace is defined as:

- A) The sequence of token-level probability distributions produced by the language model at each generation step
- B) The complete sequential log of an agent's internal reasoning steps, tool calls, and tool observations during task execution
- C) The scalar difference between the agent's predicted output and a ground-truth reference answer
- D) The set of prompt templates applied to the language model across an entire user session

**Q2.** An agent given the query "What is the current price of AAPL stock?" produces the Thought: "I know the current stock price from my training data" and returns a Final Answer without invoking the web search tool. Which failure class does this best illustrate?

- A) Incorrect tool argument specification — the agent selected the right tool but passed a malformed query
- B) Observation misinterpretation — the agent correctly retrieved data but drew a wrong conclusion from it
- C) Reasoning-action decoupling — the agent formulated a plausible-sounding rationale that bypassed required tool invocation
- D) Spurious tool invocation — the agent called a tool unnecessarily when the answer was already available

**Q3.** In a ReAct trace, an agent correctly identifies that web search is the appropriate tool, but submits the query "AAPL stock price today cheap source" instead of a clean, targeted query. The observation returned is an advertisement page rather than price data. This failure is best classified as:

- A) Incorrect tool selection — the agent chose web search when a financial data API should have been used
- B) Tool argument specification error — the agent selected the correct tool but provided a malformed or imprecise argument
- C) Observation misinterpretation — the agent received valid data but drew incorrect conclusions from it
- D) Premature loop termination — the agent produced a Final Answer before completing sufficient reasoning steps

**Q4.** Why is the reasoning trace the primary diagnostic artifact in production agent systems, rather than the Final Answer alone?

- A) Because the trace contains raw model logits that reveal which alternative tokens were considered at each reasoning step
- B) Because the trace provides a complete sequential record of every decision point where reasoning, tool selection, or observation processing can be inspected and corrected
- C) Because the trace encodes the precise API calls made to external services, enabling cost attribution and billing reconciliation
- D) Because the trace serves as the online reinforcement learning signal for continuously improving the agent policy in production

**Q5.** An agent correctly invokes the web search tool and receives an observation containing the correct answer. In its subsequent Thought step, it states "the search result was inconclusive" and re-invokes the same tool with an identical query. This failure is best classified as:

- A) Tool argument specification error — the agent should have refined the query before re-invoking
- B) Incorrect tool selection — the agent should have switched to a different tool after the first search
- C) Observation misinterpretation — the agent received a valid observation but incorrectly characterized it as inconclusive
- D) Premature loop termination — the agent exited the reasoning loop before satisfying the task requirements

??? note "Answer key — Quiz 3"

| Question | Answer | Rationale |
| :-- | :-- | :-- |
| Q1 | B | Chapter 3 defines the reasoning trace as the complete log of reasoning steps, tool calls, and observations — the primary production diagnostic artifact. |
| Q2 | C | The agent produced a reasoning step that justified bypassing tool invocation. This is reasoning-action decoupling: the thought and the required action are misaligned. |
| Q3 | B | The tool selected (web search) was appropriate; the failure was in the argument passed to it. Malformed arguments are tool argument specification errors. |
| Q4 | B | The Final Answer reveals only the outcome; the trace reveals every decision point where a failure could have been introduced, making it the actionable diagnostic artifact. |
| Q5 | C | The observation contained the correct answer; the agent's Thought incorrectly assessed it as inconclusive. This is observation misinterpretation, not an argument or tool selection error. |

## Quiz 4 — Chapter 4: Prompt Engineering for Agent Behavioral Control

**Q1.** Chapter 4 defines prompt engineering for agents as operating across four independently configurable dimensions. Which of the following enumerates all four correctly?

- A) Model selection, inference temperature, tool count limit, and maximum output length
- B) System instructions, tool descriptions, few-shot CoT scaffolds, and output format constraints
- C) Role definition, chain-of-thought exemplars, context window configuration, and retrieval pipeline design
- D) Instruction fine-tuning, preference alignment, tool registry construction, and memory module design

**Q2.** Chapter 4 treats agent prompt control as four components: system instructions, tool descriptions, few-shot demonstrations, and output format constraints. Which option maps these components most directly to `create_agent` configuration?

- A) `model`, `tools`, `middleware`, and `checkpointer`
- B) `system_prompt`, tool descriptions, few-shot demonstrations, and `response_format`
- C) `state_schema`, `context_schema`, `interrupt_before`, and `interrupt_after`
- D) `name`, `debug`, `cache`, and `store`

**Q3.** A developer adds the instruction "Always cite your sources" to the system prompt to address citation omissions. Three weeks later, citation behavior degrades when queries are phrased as imperatives. A second instruction is added. Over time, the agent begins exhibiting unpredictable behavior as the instructions interact. This scenario illustrates which anti-pattern described in Chapter 4?

- A) Treating behavioral control as an architectural concern rather than as a patch applied after deployment
- B) Accumulating fragile prompt constraints that interact unpredictably, because behavioral problems are addressed with ad hoc sentence-level additions rather than systematic design
- C) Over-specifying the output format at the expense of reasoning quality in the Thought steps
- D) Using few-shot demonstrations formatted incorrectly as plain text rather than as structured turn pairs

**Q4.** A few-shot demonstration is embedded in the system instruction as a plain-text paragraph rather than formatted as a `Human:`/`AI:` turn pair containing all six ReAct trace labels. What is the most likely consequence?

- A) The agent will produce outputs that strictly conform to the format shown in the plain-text demonstration
- B) The demonstration will function as a behavioral constraint equivalent to an explicit instruction
- C) The demonstration will have no visible effect on the agent's output format
- D) The agent will invoke additional tools to validate its outputs against the example provided

**Q5.** Which of the following best characterizes the professional approach to agent behavioral control described in Chapter 4?

- A) Iteratively add sentence-level constraints to the system prompt until each undesired behavior is suppressed
- B) Define behavioral boundaries at design time, test them systematically before deployment, and instrument the agent to detect and log behavioral violations in production
- C) Rely on the language model's alignment training to enforce ethical and format constraints, reserving the system prompt for role definition only
- D) Delegate all behavioral constraints to the tool description layer and treat the system prompt as a concise role identifier

??? note "Answer key — Quiz 4"

| Question | Answer | Rationale |
| :-- | :-- | :-- |
| Q1 | B | Chapter 4 explicitly enumerates system instructions, tool descriptions, few-shot CoT scaffolds, and output format constraints as the four independently configurable dimensions. |
| Q2 | B | Chapter 4 maps the four control components directly to agent configuration: system instructions → `system_prompt`, tool descriptions → tool definitions, few-shot demonstrations → structured example turns, and output constraints → `response_format`. |
| Q3 | B | Chapter 4 explicitly warns against treating behavioral problems as prompting problems that are fixed by appending sentences — this accumulates fragile, unpredictably interacting constraints. |
| Q4 | C | Chapter 4 states that plain-text examples placed in the system instruction are ignored. The demonstration must be formatted as a `Human:`/`AI:` turn pair with all six trace labels to influence output format. |
| Q5 | B | Chapter 4 defines the professional approach as: define boundaries at design time, test systematically, and instrument in production — behavioral control as architecture, not as a post-hoc patch. |

## Quiz 5 — Chapter 5: Architectural Trade-off Assessment for Production Deployment

**Q1.** Article 13 of the EU AI Act (2024) requires that high-risk AI systems produce output that is "sufficiently transparent." For agent systems, this requirement most directly constrains which architectural property?

- A) Token throughput and end-to-end inference latency per query
- B) The interpretability and auditability of the agent's reasoning trace
- C) The maximum number of tool invocations permitted per task execution
- D) The context window size allocated to each reasoning episode

**Q2.** A healthcare decision support agent must be deployed under the EU AI Act's Article 13 transparency requirement. The engineering team is choosing between ReAct and LATS. Which consideration most strongly favors selecting ReAct?

- A) ReAct consistently achieves higher accuracy than LATS on medical question-answering benchmarks
- B) ReAct's linear Thought/Action/Observation trace is substantially easier to audit than LATS's branching search tree
- C) ReAct requires fewer tool calls per task, reducing API cost in a clinical deployment context
- D) ReAct is natively compatible with LangGraph's checkpointing mechanism, enabling state recovery after interruption

**Q3.** Chapter 5 characterizes the selection of a reasoning architecture for production deployment as:

- A) A purely technical decision resolved by running benchmark evaluations on held-out test sets and selecting the highest-scoring system
- B) A single-objective optimization problem in which accuracy is the dominant selection criterion
- C) A multi-objective optimization problem across six explicitly evaluated dimensions requiring evidence-based professional justification
- D) A compliance exercise whose outcome is fully determined by applicable regulatory frameworks such as the EU AI Act

**Q4.** An agent system must process thousands of financial analysis queries per hour within a fixed inference budget. A junior engineer proposes LATS because it achieves higher reasoning accuracy on multi-step tasks. Which of the following best articulates the correct trade-off justification for selecting ReAct instead?

- A) "ReAct is selected because its linear trace satisfies Article 13 transparency requirements that LATS cannot meet."
- B) "ReAct is selected because it achieves higher accuracy than LATS on standard financial reasoning benchmarks."
- C) "ReAct is selected because its linear reasoning structure minimizes per-query LLM call count, satisfying the inference budget constraint, at the accepted cost of reduced reasoning depth for multi-hypothesis tasks."
- D) "ReAct is selected because it is the default architecture returned by LangChain's `create_agent` factory, minimizing implementation complexity."

**Q5.** Which of the following deployment scenarios would most strongly justify selecting LATS over ReAct, despite its substantially higher computational cost?

- A) A customer service routing agent that must classify incoming support tickets into one of ten predefined categories within a 500 ms latency constraint
- B) A scientific hypothesis generation agent that must explore multiple competing mechanistic explanations for an experimental result, where early commitment to an incorrect hypothesis invalidates subsequent reasoning and requires full restart
- C) A document summarization agent that must condense 50-page legal briefs into 200-word abstracts under a strict per-document cost ceiling
- D) A web monitoring agent that must retrieve and aggregate current news headlines on a fixed set of topics every 15 minutes

??? note "Answer key — Quiz 5"

| Question | Answer | Rationale |
| :-- | :-- | :-- |
| Q1 | B | Article 13 requires operators to be able to understand and interpret system outputs — for agent systems this directly targets the interpretability and auditability of the reasoning trace, not latency, tool count, or context size. |
| Q2 | B | Chapter 5 states that a LATS agent's branching trace is harder to audit than a ReAct agent's linear trace — this is the primary regulatory consideration under Article 13 for high-risk domains. |
| Q3 | C | Chapter 5 explicitly frames architectural selection as a multi-objective optimization across six dimensions requiring documented, evidence-based justification — not a benchmark race or a pure compliance exercise. |
| Q4 | C | A valid trade-off statement names both competing properties (inference cost vs. reasoning depth) and the contextual constraint (fixed budget in high-volume deployment) that resolves the trade-off in favor of ReAct. Options A and B are partially correct but miss the cost-depth trade-off structure. |
| Q5 | B | LATS is justified when: the state space is large with many possible solution paths; intermediate states can be evaluated; early commitment to a wrong path is catastrophically costly; and latency is not the primary constraint. Scenario B satisfies all four conditions; the others require low latency or involve linear tasks. |

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2.2-Addendum-%E2%80%90-OLD){target=_blank} (wiki page last changed 2026-08-06). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/archive/module-2/self-assessment-quizzes.md){target=_blank}.</p>
