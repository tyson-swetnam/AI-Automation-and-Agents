---
title: Module 1 Reading Guides
description: Reading guides (sources, key terms, guiding questions, critical-thinking prompts) for the five chapters of Module 1, From Prompts to Pipelines.
type: Reading Guide
tags:
- module-1
- student-facing
- reading-guide
- ai-agents
- agent-loop
- automation-paradigms
- workflow-audit
module: 1
status: stable
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1.2-Addendum
  title: 'AI Automation and Agents v2 wiki: Module-1.2-Addendum'
  author: Carlos Lizárraga-Celaya
  last_modified: '2026-08-05T17:04:48-07:00'
authorship:
  created: '2026-07-23'
  contributors:
  - C. Lizárraga
wiki_page: Module-1.2-Addendum
---
# Module 1 Reading Guides

These reading guides are designed to accompany the assigned sources for each chapter of Module 1. Work through the guiding questions as you read — they focus your attention on the concepts the chapter lesson and quizzes will assess.

## Reading Guide 1 — Chapter 1: Redefining Intelligence — What AI Agents Actually Are { #reading-guide-1 }

**Sources covered:**

- Wooldridge, M., & Jennings, N. R. (1995). Intelligent agents: Theory and practice. *The Knowledge Engineering Review, 10*(2), 115–152.
- LangChain Conceptual Guide: What are Agents?
- Video: "What are Agents?" — IBM Technology

**Estimated study time:** ~40 minutes (readings) + ~15 minutes (video)

**Chapter connection:** These three sources together bridge the foundational theoretical definition of an agent (Wooldridge & Jennings) with its contemporary engineering implementation (LangChain) and a practitioner-accessible overview (IBM video). Read them in the order listed: theory first, then practice.

### Overview

Wooldridge and Jennings (1995) is the canonical theoretical treatment of intelligent agents. Written before the modern deep-learning era, it nonetheless defines properties — autonomy, reactivity, pro-activeness, and social ability — that remain the standard analytical vocabulary for evaluating whether a system qualifies as a "true" agent. The LangChain Conceptual Guide operationalizes these properties for contemporary LLM-based agent systems, grounding them in the four-stage agent loop (perceive → plan → act → observe) that every automation framework in this course implements. The IBM Technology video serves as a visual synthesis of both sources, suitable for review after reading.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **Intelligent agent** | A computer system capable of autonomous action in an environment to meet its design objectives (Wooldridge & Jennings, 1995) |
| **Autonomy** | The agent operates without continuous human direction, making decisions from its own internal state |
| **Reactivity** | The agent perceives its environment and responds to changes in a timely fashion — it is not executing a fixed script |
| **Pro-activeness** | The agent exhibits goal-directed behavior, taking initiative rather than merely reacting to stimuli |
| **Social ability** | The agent can interact with other agents and humans using defined communication protocols |
| **Agent loop** | The four-stage cycle: Perceive → Plan → Act → Observe, which underlies every automated agent system |
| **ReAct pattern** | Reasoning and Acting — a prompting pattern in which the agent alternates between Thought, Action, and Observation steps |
| **Tool** | An external capability (API, database query, file operation) that an agent can invoke during the Act stage |
| **Environment** | The external context an agent perceives and acts upon — includes files, databases, APIs, and other agents |
| **BDI model** | Beliefs–Desires–Intentions — a theoretical model for reasoning about agent internal states (Wooldridge & Jennings) |

### Guiding Questions

#### Section A — Wooldridge & Jennings (1995)

1. Wooldridge and Jennings distinguish between a "weak notion" and a "strong notion" of agency. What additional properties characterize the strong notion, and why does the course adopt the weak notion as its working definition?

2. The paper defines reactivity as responding to changes "in a timely fashion." Why is the phrase "in a timely fashion" analytically significant? What would distinguish a reactive agent from one that is simply reading from a static input?

3. Pro-activeness requires that the agent take initiative to meet its design objectives, not merely respond to stimuli. Identify one scenario in an organizational workflow where this distinction would matter practically.

4. Social ability is defined as the capacity to interact using "agent communication languages." Why does this property become especially important in multi-agent systems (a topic introduced in Module 4)?

5. The authors argue that the term "agent" is overloaded — applied to systems that do not meet all four weak-notion properties. Identify two examples of systems that are commonly called "agents" in commercial contexts but would fail Wooldridge and Jennings' weak-notion criteria.

#### Section B — LangChain Conceptual Guide: What are Agents?

6. The LangChain guide describes the agent loop as: Perceive → Plan → Act → Observe. Map each stage onto one of Wooldridge and Jennings' four agent properties. Where does the mapping break down or require nuance?

7. In the LangChain framework, what distinguishes a "tool call" from an ordinary function call in a conventional program? What property of the agent determines when and whether a tool is invoked?

8. The Conceptual Guide describes the LLM as the "reasoning engine" of the agent. What specific capability of the LLM enables the Plan stage of the loop? What does this imply about the role of prompt design in agent behavior?

9. The ReAct pattern structures agent reasoning as alternating Thought → Action → Observation cycles. What would happen if the Observation stage were omitted — that is, if the agent acted but received no feedback on the result?

#### Section C — IBM Technology Video: "What are Agents?"

10. After watching the video, identify one concept from Wooldridge & Jennings that the video explains accurately and one concept it simplifies in a way that could mislead a practitioner. Justify your assessment by citing the original paper.

11. The video distinguishes agents from chatbots and from APIs. Summarize the video's explanation of each distinction in one sentence each. Then evaluate: are these distinctions sufficient for a professional making architectural decisions, or do they omit critical nuance?

### Critical Thinking Prompts

- The agent loop (perceive → plan → act → observe) is structurally similar to the Plan-Do-Check-Act (PDCA) cycle used in organizational quality management. What does this structural parallel suggest about the generalizability of agent-based thinking beyond AI systems?

- A large language model without tool access cannot take actions in the world — it can only produce text. What does this imply about the relationship between LLMs and agents? Is a standalone LLM an agent by Wooldridge and Jennings' definition?

## Reading Guide 2 — Chapter 4: Workflow Thinking as a Professional Competency { #reading-guide-2 }

> **Note on sequence:** Reading Guide 2 accompanies Chapter 4 content because its primary source — Wooldridge & Jennings (1995) — is shared with Chapter 1. Reading Guide 2 focuses on how that foundational theory connects to workflow decomposition and computational thinking, which are the analytical tools you will apply in the Workflow Audit Project.

**Sources covered:**

- Wing, J. M. (2006). Computational thinking. *Communications of the ACM, 49*(3), 33–35.
- Wooldridge, M., & Jennings, N. R. (1995). *(Re-read: Sections on agent environment and agent architecture)* — Reading 2

**Estimated study time:** ~20 minutes (Wing) + ~20 minutes (targeted Wooldridge & Jennings re-read)

**Chapter connection:** Wing's essay provides the intellectual foundation for why systematic workflow decomposition is a generalizable cognitive skill, not merely a software engineering technique. The targeted Wooldridge & Jennings re-read anchors the theoretical notion of agent environment to the practical concept of workflow trigger and output.

### Overview

Jeannette Wing's 2006 essay is one of the most cited papers in computing education, arguing that computational thinking — decomposing problems, recognizing patterns, and abstracting processes into clear specifications — is a fundamental intellectual skill applicable well beyond programming. The essay's central claim directly motivates the Workflow Decomposition Framework used in Module 1: if you can specify a workflow with sufficient precision that another agent (human or AI) could execute it without ambiguity, you have demonstrated computational thinking. The Wooldridge & Jennings re-read focuses on agent environment structure, which maps directly onto the "trigger" and "output" fields of the Workflow Mapping Template.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **Computational thinking** | The thought processes involved in formulating problems and their solutions so that the solutions are representable in a form that can be effectively carried out by an information-processing agent (Wing, 2006) |
| **Decomposition** | Breaking a complex process into smaller, independently specifiable steps |
| **Abstraction** | Suppressing irrelevant detail to expose the essential structure of a problem |
| **Pattern recognition** | Identifying recurring structures across problem instances that can be generalized into reusable rules |
| **Trigger** | The event or condition that initiates a workflow — maps to the agent's initial Perceive stage |
| **Conditional branch** | A workflow step where the next action depends on the evaluation of a condition — maps to the Plan stage |
| **Blast radius** | The scope of downstream consequences if an automated step produces an incorrect output |
| **Rule-based specification** | A workflow step that can be executed by applying a deterministic rule consistently across all inputs |
| **Reversibility** | The degree to which the output of a workflow step can be undone or corrected after execution |
| **Automation potential** | A two-dimensional assessment of how fully a workflow can be automated given its rule-based specification score and consequence severity score |

### Guiding Questions

#### Section A — Wing (2006): Computational Thinking

1. Wing defines computational thinking as "the thought processes involved in formulating problems and their solutions so that the solutions are representable in a form that can be effectively carried out by an information-processing agent." Why is the phrase "information-processing agent" significant for this course? What does it imply about the relationship between workflow documentation and agent design?

2. Wing argues that computational thinking is "a fundamental skill for everyone, not just computer scientists." What specific habits of mind does she claim constitute computational thinking? Identify three of them and explain how each applies to the task of documenting a professional workflow.

3. Wing distinguishes abstraction — "the one skill that makes computer scientists tick" — from simplification. What is the difference? Give one example of inappropriate simplification in a workflow specification and one example of appropriate abstraction.

4. The essay was written in 2006, before modern LLMs. Which of Wing's claims about computational thinking appear most durable in an era where LLMs can generate code and automate reasoning tasks? Which claims require revision in light of current AI capabilities?

5. Wing states that computational thinking involves "thinking recursively." What would a recursive workflow structure look like, and what challenges would it pose for the Workflow Decomposition Framework used in Module 1?

#### Section B — Wooldridge & Jennings (1995): Agent Environment (re-read)

6. Wooldridge and Jennings classify agent environments along four dimensions: accessible vs. inaccessible, deterministic vs. non-deterministic, episodic vs. non-episodic, and static vs. dynamic. Map each dimension onto a property of a professional workflow. Which dimension most directly determines whether a workflow is rule-based in the Module 1 two-dimensional assessment?

7. The paper argues that the hardest environments for agents are those that are inaccessible, non-deterministic, non-episodic, and dynamic simultaneously. Identify one professional workflow that exhibits all four properties and explain why it would score low on the rule-based dimension of the two-dimensional assessment.

8. The "trigger" field of the Workflow Mapping Template corresponds to what Wooldridge and Jennings call the agent's initial perception of its environment. Why is it important to specify the trigger precisely rather than loosely? What happens to automation reliability if the trigger condition is ambiguous?

### Critical Thinking Prompts

- The Workflow Decomposition Framework requires that a workflow be specified so completely that "another person who has never done your job could follow your workflow map as a procedure and produce the same output without asking a single clarifying question." How does this requirement relate to Wing's concept of abstraction? What level of abstraction is too high, and what level is too low?

- Wing argues that computational thinking precedes and enables automation. If this is true, what does it imply about the order in which a professional should approach a new automation project? What should come before the first tool is touched?

## Reading Guide 3 — Chapter 3: AI Literacy as a New Professional Imperative { #reading-guide-3 }

**Sources covered:**

- Ng, D. T. K., Leung, J. K. L., Chu, S. K. W., & Qiao, M. S. (2021). Conceptualizing AI literacy: An exploratory review. *Computers and Education: Artificial Intelligence, 2*, 100041.
- Long, D., & Magerko, B. (2020, April). What is AI literacy? Competencies and design considerations. *Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems* (pp. 1–16).

**Estimated study time:** ~35 minutes (Ng et al.) + ~30 minutes (Long & Magerko)

**Chapter connection:** These two papers together construct the professional competency model that underlies this course's learning objectives. Ng et al. (2021) provides the four-pillar framework; Long and Magerko (2020) provides the 21-competency taxonomy. Both papers inform the course's argument that AI literacy is a multi-domain professional imperative, not a purely technical credential.

### Overview

Ng et al. (2021) conducted a systematic review of the AI literacy literature and synthesized a four-pillar model: (1) Know and understand AI, (2) Use and apply AI, (3) Evaluate and create AI, and (4) AI ethics. This hierarchical structure — from foundational knowledge to ethical practice — maps directly onto the five-module arc of this course. Long and Magerko (2020) complement this with twenty-one specific competencies organized into five families, grounded in empirical research and design practice. Together, these frameworks answer the question: what does it mean to be professionally literate in AI, as distinct from merely being able to use AI tools?

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **AI literacy** | A set of competencies that enables individuals to critically evaluate AI technologies, communicate and collaborate with AI, and use AI as a tool online, at home, and in the workplace (Long & Magerko, 2020) |
| **Four-pillar model** | Ng et al.'s framework: Know & Understand AI → Use & Apply AI → Evaluate & Create AI → AI Ethics |
| **Competency family** | Long & Magerko's grouping of related AI literacy competencies (What is AI?, How does AI work?, How is AI used?, How should AI be used?, How do I use AI?) |
| **Critical thinking about AI** | The capacity to evaluate AI systems' outputs, limitations, and societal impacts — not merely to operate them |
| **Algorithmic bias** | Systematic error in AI output that arises from biased training data, flawed design choices, or non-representative evaluation |
| **Explainability** | The degree to which an AI system's decisions can be understood and communicated to affected stakeholders |
| **Human-AI collaboration** | Working patterns in which human judgment and AI capabilities are deliberately combined to produce outcomes neither could achieve alone |
| **Data literacy** | The ability to read, work with, analyze, and communicate with data — a prerequisite competency for AI literacy |

### Guiding Questions

#### Section A — Ng et al. (2021): Conceptualizing AI Literacy

1. Ng et al. identify four pillars of AI literacy organized in a progression from foundational to advanced. Why does the "Know and Understand AI" pillar logically precede the "Use and Apply AI" pillar? What happens when practitioners skip the foundational pillar and go directly to tool use?

2. The fourth pillar — AI Ethics — is positioned at the top of the hierarchy rather than the bottom. Does this sequencing imply that ethics is addressed last in professional practice? How do the authors explain the relationship between technical literacy and ethical literacy?

3. Ng et al. distinguish AI literacy from digital literacy and data literacy, arguing that AI literacy requires domain-specific competencies not captured by existing frameworks. What specific properties of AI systems necessitate a distinct literacy framework?

4. The paper identifies educational contexts ranging from K-12 to professional and workplace learning. How does the appropriate emphasis among the four pillars shift across these contexts? Which pillars are most critical for graduate-level professional learners?

5. Ng et al. note that AI literacy research is still emerging and that the field lacks consensus on assessment instruments. What are the implications of this gap for a course that attempts to assess AI literacy competencies?

#### Section B — Long & Magerko (2020): What is AI Literacy?

6. Long and Magerko identify 21 AI literacy competencies organized into five families. Which competency family most directly maps onto what this course calls "workflow thinking"? Justify your answer by citing specific competencies.

7. The paper distinguishes between competencies that involve understanding AI (conceptual) and competencies that involve using AI (operational). Why does Long and Magerko argue that both are necessary for genuine literacy, rather than operational competency alone?

8. Long and Magerko include "Recognizing AI" as a core competency — the ability to identify when and how AI is embedded in systems encountered in daily life. Why is this competency professionally significant in contexts where AI is embedded in commercial products and enterprise software?

9. The paper was presented at CHI (Computer-Human Interaction conference), which foregrounds design considerations. How does Long and Magerko's design orientation shape their definition of AI literacy differently from a purely technical or purely policy-oriented perspective?

10. Both papers were published before the widespread public availability of large language model interfaces (2022–2023). Identify two competencies from Long and Magerko's framework that have become significantly more important since then, and explain why.

### Critical Thinking Prompts

- Long and Magerko argue that AI literacy includes "the ability to communicate and collaborate effectively with AI." In what ways does this competency differ from traditional human-computer interaction skills? What new cognitive demands does it place on the professional user?

- Ng et al.'s four-pillar model implies a developmental progression. Based on the Module 1 learning objectives, where in that progression does this course primarily position students who are beginning Module 1?

## Reading Guide 4 — Chapter 2: The Automation Ecosystem — Three Paradigms, One Spectrum { #reading-guide-4 }

> **Note on sequence:** Reading Guide 4 accompanies Chapter 2 because Reading 4 (Automation Landscape Overview) is the primary source for this chapter. The AI literacy papers (Long & Magerko; Ng et al.) appear in the Chapter 2 resource list as contextual background for evaluating paradigm choices; they are covered in depth in Reading Guide 3.

**Sources covered:**

- Reading 4: Automation Landscape Overview *(internal course reading)*
- Long, D., & Magerko, B. (2020) and Ng et al. (2021) *(as contextual framework for paradigm evaluation — see Reading Guide 3 for full treatment)*

**Estimated study time:** ~30 minutes (Automation Landscape Overview) + ~10 minutes (review of AI literacy frameworks as evaluative lens)

**Chapter connection:** This reading establishes the structural vocabulary for the automation paradigm taxonomy that you will apply throughout the course — particularly in the Workflow Audit Project's paradigm selection step.

### Overview

The Automation Landscape Overview maps three paradigms — no-code, low-code, and code-first — across six comparison dimensions: technical skill requirement, system flexibility, development speed, cost at scale, data governance risk, and maintenance burden. Understanding where each paradigm sits on these dimensions, and why, is the analytical foundation for justified paradigm selection. A key course argument is that paradigm selection is a professional judgment call driven by workflow properties, not a personal preference.

The AI literacy frameworks (Long & Magerko; Ng et al.) provide the evaluative meta-lens: a professionally literate practitioner can assess the trade-offs of each paradigm relative to the workflow, the team, and the organizational context — not merely operate within one paradigm.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **No-code** | Automation platforms using visual drag-and-drop interfaces requiring minimal technical skill; high accessibility, limited flexibility (e.g., n8n visual builder, Claude Cowork) |
| **Low-code** | Frameworks blending pre-built components with custom code; require moderate technical skill; significantly more flexible for multi-agent orchestration (e.g., LangChain, CrewAI) |
| **Code-first** | Fully programmatic automation built from custom Python or other languages; maximum flexibility and data governance; highest technical skill requirement (e.g., Claude Code, custom Python agents) |
| **Data governance** | The policies, controls, and accountability structures governing how data is stored, accessed, transmitted, and used within an automation system |
| **Vendor lock-in** | Dependency on a proprietary platform's architecture, data formats, or APIs that constrains migration to alternative tools |
| **Scalability** | A system's capacity to handle increasing task volume without proportional increases in cost or engineering effort |
| **Orchestration** | Coordinating multiple agents, tools, or workflow steps to execute a complex process — the domain of low-code and code-first frameworks |
| **Self-hosted** | Deploying an automation tool on infrastructure controlled by the organization, eliminating third-party data transmission |
| **Paradigm selection criteria** | The workflow and organizational properties that justify choosing one automation paradigm over another |

### Guiding Questions

#### Section A — Automation Landscape Overview

1. The reading presents the three paradigms as positions on a single spectrum defined by two axes: required technical skill and system flexibility. Why are these two axes correlated rather than independent? Identify one scenario in which a team might need high flexibility but also has low technical skill — how should a practitioner handle this constraint?

2. Data governance is described as the most commonly underweighted factor in paradigm selection. Why does no-code automation introduce higher data governance risk than code-first automation, even when both accomplish the same workflow outcome?

3. The reading argues that no-code is not inferior to code-first — each is appropriate in different contexts. Construct one concrete example where a no-code solution is strictly preferable to a code-first solution, and justify your reasoning using at least two paradigm comparison dimensions.

4. Low-code frameworks such as LangChain and CrewAI are described as providing "better data governance by allowing organizations to self-host or integrate local models." What specific organizational conditions must be met for self-hosting to be a realistic option?

5. The reading distinguishes between the visual abstraction layer of n8n and the programmatic abstraction layer of LangChain. What does each abstraction layer make easy, and what does each abstraction layer make difficult or impossible?

6. Cost at scale is listed as a paradigm comparison dimension. Explain why task-based cloud pricing models (typical of no-code platforms) become economically unfavorable at high workflow execution volumes, and at what point low-code or code-first approaches become cost-superior.

#### Section B — AI Literacy as a Lens for Paradigm Evaluation

7. Using Long and Magerko's (2020) competency framework as a lens: which AI literacy competencies are most critical for a practitioner who must select between automation paradigms for an organizational workflow? Name at least two specific competencies and explain their relevance.

8. Ng et al.'s (2021) four-pillar model places "Evaluate and Create AI" above "Use and Apply AI." How does this hierarchy apply to paradigm selection — in what sense is selecting a paradigm an evaluative act rather than merely an operational one?

### Critical Thinking Prompts

- The no-code/low-code/code-first taxonomy implies that technical skill level is the primary differentiator. Is this the most important differentiator from a professional practice standpoint, or would a different primary axis (e.g., organizational risk tolerance, team size, workflow change frequency) produce a more useful taxonomy?

- An organization's automation tooling choices tend to persist longer than expected because of migration costs, team familiarity, and technical debt. What does this imply about the professional responsibility of the practitioner who makes the initial paradigm selection recommendation?

## Reading Guide 5 — Chapter 5: Responsible AI — From Principle to Practice, Starting Now { #reading-guide-5 }

**Sources covered:**

- National Institute of Standards and Technology. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1.
- Floridi, L., Cowls, J., Beltrametti, M., Chatila, R., et al. (2018). AI4People — An ethical framework for a good AI society: Opportunities, risks, principles, and recommendations. *Minds and Machines, 28*(4), 689–707.

**Estimated study time:** ~40 minutes (NIST AI RMF — selected sections) + ~30 minutes (Floridi et al.)

**Chapter connection:** These two sources provide the formal governance vocabulary and ethical principles that frame every subsequent design decision in the course. The NIST AI RMF is a practice-oriented risk management tool; Floridi et al. is the philosophical foundation from which those practices derive. Read the NIST document by focusing on the four core functions (Govern, Map, Measure, Manage) and the Map function in detail; read Floridi et al. in full.

### Overview

The NIST AI Risk Management Framework (AI RMF 1.0) is the current U.S. federal standard for trustworthy AI system development and deployment. It defines four core organizational functions — Govern, Map, Measure, Manage — and seven trustworthy AI characteristics. The Map function, which this module's Workflow Audit Project directly enacts, involves identifying the context, risks, and affected stakeholders of an AI system before deployment.

Floridi et al.'s AI4People framework synthesizes ethical AI principles from major international policy documents into five actionable principles: beneficence, non-maleficence, autonomy, justice, and explicability. These are not aspirational values but design constraints that translate into specific architectural and governance decisions.

### Key Terms and Concepts

| Term | Working Definition |
|---|---|
| **AI RMF** | NIST Artificial Intelligence Risk Management Framework — a voluntary framework for managing AI-related risks across the system lifecycle |
| **Govern** | The NIST AI RMF function that establishes organizational policies, accountability structures, and culture for AI risk management |
| **Map** | The NIST AI RMF function that identifies the AI system's context, risks, stakeholders, and potential impacts before deployment |
| **Measure** | The NIST AI RMF function that analyzes and assesses identified risks using quantitative and qualitative methods |
| **Manage** | The NIST AI RMF function that implements risk treatment plans, monitors outcomes, and responds to emerging risks |
| **Trustworthy AI** | NIST's seven characteristics: accountable, explainable, interpretable, privacy-enhanced, reliable, safe, and fair |
| **Beneficence** | AI should benefit people and society (Floridi et al.) |
| **Non-maleficence** | AI should not harm people — "do not harm" as a design constraint (Floridi et al.) |
| **Autonomy** | AI should preserve and enhance human agency, not diminish it (Floridi et al.) |
| **Justice** | AI's benefits and risks should be equitably distributed across populations (Floridi et al.) |
| **Explicability** | AI decisions should be intelligible to affected parties — encompasses both interpretability and accountability (Floridi et al.) |
| **Human-in-the-loop** | A design pattern in which a human reviews or approves an agent's proposed action before it is executed |
| **Accountability** | The organizational and legal responsibility for an AI system's actions and outcomes |

### Guiding Questions

#### Section A — NIST AI RMF 1.0 (2023)

1. The NIST AI RMF distinguishes between four core functions: Govern, Map, Measure, Manage. These are presented as complementary and iterative, not sequential stages. What does this non-sequential structure imply about how organizations should integrate AI risk management into existing workflows?

2. The Map function requires practitioners to identify "the context in which an AI system will operate, the risks it poses, and the stakeholders it affects." How does the Module 1 Workflow Audit Project enact the Map function? Be specific about which workflow audit fields correspond to Map activities.

3. The NIST AI RMF lists seven characteristics of trustworthy AI. Select three of these characteristics and explain how each translates into a specific design decision for an automated workflow (e.g., what would "reliable" require of a workflow that sends invoices to vendors?).

4. The framework is described as voluntary for most organizations. What are the practical incentives for organizations to adopt a voluntary standard, and what are the risks of non-adoption specifically in the context of deploying AI agents in business processes?

5. The NIST AI RMF was released in January 2023. Given the pace of AI development, what specific aspects of the framework do you anticipate will require the most significant revision in the next five years?

#### Section B — Floridi et al. (2018): AI4People

6. Floridi et al. synthesize five ethical principles for AI. Identify the specific policy documents and ethical traditions they draw on for each principle. Why is grounding the principles in existing ethical frameworks — rather than treating AI ethics as entirely novel — methodologically significant?

7. The principle of non-maleficence ("do not harm") is relatively straightforward in human ethics but is complicated in AI systems by the problem of distributed causality. Explain this complication: if an AI agent makes an error that harms a user, what is the distribution of moral responsibility among the developer, the deploying organization, and the AI system itself?

8. The principle of autonomy in AI4People refers to preserving human autonomy — not the autonomy of the AI system. How does this distinguish AI4People's use of "autonomy" from Wooldridge and Jennings' use of the same term? Why might this terminological overlap cause confusion in professional practice?

9. Floridi et al. argue that explicability — the capacity for AI decisions to be explained to affected parties — is a "meta-principle" that enables the other four principles. Why? What specifically becomes impossible if an AI system's decisions cannot be explained?

10. The paper was published in 2018. The AI4People project involved consultation across civil society, industry, and government. Evaluate the principle of justice as defined by Floridi et al. in light of AI developments since 2018 (e.g., large language models, automated hiring tools, predictive policing). Has the principle proven durable? What would need to be added?

### Critical Thinking Prompts

- The course's foundational ethical principle is: "The AI did it is never a complete ethical or legal answer." Map this principle onto Floridi et al.'s five principles. Which principle most directly grounds this claim? Which of the NIST AI RMF's four functions most directly implements it?

- In the two-dimensional automation assessment introduced in Chapter 4, Dimension 2 (consequence severity) functions as a risk management instrument. How does this dimension operationalize the principle of non-maleficence? Is it sufficient as an ethical instrument, or does it require supplementation by the other four AI4People principles?

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1.2-Addendum){target=_blank} (wiki page last changed 2026-08-05). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-1/reading-guides.md){target=_blank}.</p>
