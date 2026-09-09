---
title: 'Module 1: Foundational Concepts'
description: 'Five-chapter conceptual lesson for Module 1: what AI agents are, the no-code/low-code/code-first automation spectrum, AI literacy frameworks, workflow decomposition and two-dimensional automation assessment, and responsible AI governance.'
type: Lesson
tags:
- module-1
- student-facing
- lesson
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
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1:-Foundational-Concepts
  title: 'AI Automation and Agents v2 wiki: Module-1:-Foundational-Concepts'
  author: Michelle Yung; Carlos Lizárraga-Celaya
  last_modified: '2026-07-23T08:01:20-07:00'
authorship:
  created: '2026-04-20'
  updated: '2026-07-21'
  contributors:
  - C. Lizárraga
  - M. Yung
wiki_page: Module-1:-Foundational-Concepts
---
# Module 1: Foundational Concepts

![The new frontier of AI agents](../../assets/images/The_New_Frontier.png){ width="900" }

## Foundational Concepts for Module

*Estimated time: ~7 min*

Module 1 of AI Automation and Agents establishes the conceptual and practical foundation
for everything that follows in the course. Its title — From Prompts to Pipelines: Thinking Like
an Automation Designer — signals the module’s central cognitive shift: moving from viewing
AI as a conversational tool you prompt to viewing it as an autonomous agent you design
workflows for.

**Three critical takeaways define the module’s contribution to your professional
development:**

- AI agents are not chatbots. They perceive their environment, plan actions, use tools,
and observe outcomes across a structured loop — delegating nothing to chance and
nothing to the user once set in motion. Understanding this distinction is a non-
negotiable prerequisite for all subsequent course modules.

- The automation landscape is a spectrum, not a binary choice. Three paradigms —
no-code, low-code, and code-first — address different user profiles, risk tolerances,
and organizational requirements. Exercising professional judgment about which
paradigm to select for a given workflow is a high-value skill.

- Your own professional practice is the course’s primary raw material. The Workflow
Audit Project you produce in this module is not a homework exercise — it is the
foundational portfolio artifact that every subsequent module will build upon. The
quality and specificity of your workflow documentation here determines the quality of
your subsequent applied work.

By the end of this module, you will have completed your first hands-on AI agent interactions,
mapped three real workflows from your professional practice, assessed their automation
potential using a structured framework, and produced your first reflective self-assessment —
a metacognitive baseline you will revisit in Module 5 to observe your growth.

The sources assigned in Module 1 establish five interconnected conceptual
frameworks that serve as the analytical vocabulary for the entire course. Each framework
addresses a distinct dimension of the AI automation landscape: what agents are, how the tool
ecosystem is structured, what AI literacy requires of professionals, how to think computationally
about workflows, and what responsible deployment requires from the first day of practice.

### Chapter 1: Redefining Intelligence — What AI Agents Actually Are

#### Chapter 1 Lesson

*Estimated time: ~14 min*

Public discourse around AI often confuses four structurally distinct entities: chatbots,
search engines, rule-based automation scripts, and AI agents. This is not a minor
terminological imprecision — it leads to fundamental errors in system design, risk assessment,
and organizational decision-making. Module 1 begins by resolving this confusion with analytical
precision.

**THE FOUR-STAGE AGENT LOOP**

Wooldridge and Jennings (1995) — the foundational theoretical paper on intelligent agents —
define an agent as a computer system capable of autonomous action in an environment in
order to meet its design objectives. The critical word is 'autonomous': an agent acts without
continuous human direction. The LangChain Conceptual Guide operationalizes this definition in
contemporary practice through a four-stage agent loop:

![The four-stage agent loop](../../assets/images/Four_Stage_Agent_Loop.png){ width="800" }

**FOUR PROPERTIES THAT DEFINE A TRUE AGENT (Wooldridge & Jennings, 1995)**

* **Autonomy:** The agent operates without continuous human direction. It makes decisions based
on its own internal state and goals, not external prompts at each step.

* **Reactivity:** The agent perceives its environment and responds to changes in that environment
in a timely fashion — it is not executing a fixed script.

* **Pro-activeness:** The agent does not merely react to stimuli; it exhibits goal-directed behavior,
taking initiative to achieve design objectives.

* **Social ability:** The agent can interact with other agents (and humans) using defined
communication protocols — essential for multi-agent systems introduced in Module 4.

![Critical distinctions between agents and other systems](../../assets/images/Critical_Distinctions.png){ width="800" }

!!! note "WHY THIS MATTERS"

    Every design decision in the course — from tool selection to memory architecture to
    responsible deployment — depends on whether you are working with a true agent or one of
    its lookalikes. Misclassifying a system as an 'agent' when it is a script leads to unrealistic
    expectations, inappropriate risk assessments, and flawed evaluation frameworks. Precision
    here is not pedantry; it is professional practice.

#### Learning Resources

* [LangChain - What are Agents?](https://docs.langchain.com/oss/python/langchain/agents){target=_blank}
* Wooldridge, M., & Jennings, N. R. (1995). [Intelligent agents: Theory and practice](readings/intelligent-agents-wooldridge-jennings.md). The knowledge engineering review, 10(2), 115-152.
* [Video 1: "What are Agents?"](https://www.youtube.com/watch?v=F8NKVhkZZWI){target=_blank} - IBM Technology

[**Reading Guide Chapter 1 - Redefining Intelligence, what AI agents actually are**](reading-guides.md#reading-guide-1)

#### Chapter 1 Quiz

[Take the Chapter 1 Quiz](chapter-quizzes.md#chapter-1-quiz){ .md-button }

### Chapter 2: The Automation Ecosystem — Three Paradigms, One Spectrum

#### Chapter 2 Lesson

*Estimated time: ~10 min*

Automation tools exist on a spectrum defined by two axes: required user technical skill and system
flexibility. Understanding where each tool class sits on this spectrum — and why — is a core
professional competency. Choosing the wrong paradigm for an organizational workflow wastes
engineering resources, introduces data governance risks, or creates a system the team that built it
cannot maintain.

**Three automation paradigms**

- No-code
- Low-code
- Code-first

![Automation tools landscape](../../assets/images/Automation_Tools.png){ width="800" }

**Two Critical Observations Emerge From The Comparison.** 

First, the paradigms are not hierarchically
ranked — no-code is not inferior to code-first; each is appropriate in different contexts. A seasoned
AI engineer who builds a no-code workflow for a repetitive administrative process is exercising
professional judgment, not laziness. 

Second, data governance is the most commonly
underweighted factor in paradigm selection. Organizations that move sensitive data
through no-code vendor servers without explicit data processing agreements may be in regulatory
violation, regardless of how elegant the workflow is.

#### Learning Resources

* Long, D., & Magerko, B. (2020, April). [What is AI literacy? Competencies and design considerations](https://dl.acm.org/doi/pdf/10.1145/3313831.3376727){target=_blank}. In Proceedings of the 2020 CHI conference on human factors in computing systems (pp. 1-16).
* Ng, D. T. K., Leung, J. K. L., Chu, S. K. W., & Qiao, M. S. (2021). [Conceptualizing AI literacy: An exploratory review](https://www.sciencedirect.com/science/article/pii/S2666920X21000357){target=_blank}. Computers and Education: Artificial Intelligence, 2, 100041.

[**Reading Guide Chapter 2 - Automation Landscape Overview**](reading-guides.md#reading-guide-4)

#### Chapter 2 Quiz

[Take the Chapter 2 Quiz](chapter-quizzes.md#chapter-2-quiz){ .md-button }

### Chapter 3: AI Literacy as a New Professional Imperative

#### Chapter 3 Lesson

Ng, Leung, Chu, and Qiao (2021) conducted an exploratory review of the AI literacy literature and
synthesized a four-pillar competency model that directly informs the design of this course.
Long and Magerko (2020) complement this with twenty-one specific AI literacy competencies,
organized into five families. Together, these frameworks articulate what it means to be literate in AI —
not merely to use AI tools, but to understand, evaluate, and create with them.

![The four pillars of AI literacy](../../assets/images/Four_PIllars_AI_Literacy.png){ width="800" }

Long and Magerko (2020) add an important nuance: AI literacy is not merely technical proficiency with AI tools. It includes the capacity to recognize AI in deployed systems, understand the ethical and social implications of AI decisions, and communicate AI concepts accurately to non-specialist audiences. This breadth is why the course’s five general skills include both technical implementation and communication and evidence-based reasoning — professional AI literacy is a multi-domain competency, not a single technical credential.

#### Learning Resources

* Long, D., & Magerko, B. (2020, April). [What is AI literacy? Competencies and design considerations](https://dl.acm.org/doi/pdf/10.1145/3313831.3376727){target=_blank}. In Proceedings of the 2020 CHI conference on human factors in computing systems (pp. 1-16).
* Ng, D. T. K., Leung, J. K. L., Chu, S. K. W., & Qiao, M. S. (2021). [Conceptualizing AI literacy: An exploratory review](https://www.sciencedirect.com/science/article/pii/S2666920X21000357){target=_blank}. Computers and Education: Artificial Intelligence, 2, 100041.

[**Reading Guide Chapter 3 - AI Literacy**](reading-guides.md#reading-guide-3) - Ng et al. (2021): AI Literacy Framework

#### Chapter 3 Quiz

[Take the Chapter 3 Quiz](chapter-quizzes.md#chapter-3-quiz){ .md-button }

### Chapter 4: Workflow Thinking as a Professional Competency

#### Chapter 4 Lesson

Jeannette Wing's (2006) foundational essay on computational thinking argues that the ability to decompose problems, recognize patterns, and abstract processes into clear specifications is a fundamental intellectual skill, analogous to reading and arithmetic, rather than one specific to computer scientists. The following **Workflow Decomposition Framework** and **Two-Dimensional Automation Assessment** explains how one can systematically break down any multi-step professional process into its atomic components and assess it's potential for automation.

**The Workflow Decomposition Framework**

Every workflow capable of automation can be completely specified by six components: Trigger, Sequential Steps, Tools and Resources, Conditional Branches, Error Handling, and Output.

![Workflow automation components](../../assets/images/Workflow_Automation_Components.png){ width="800" }

**The Two-Dimensional Automation Assessment Framework**

The following automation assessment framework evaluates any workflow across two independent dimensions to produce a justified automation-potential score.

**Dimension 1 — Rule-Based Specification (1–5 scale)**

How fully can this workflow be specified as a set of rules that apply consistently, without human judgment, across all expected inputs?

- A score of 5 means every step has a deterministic rule.
- A score of 1 means every step requires human judgment that cannot be codified.
- Higher scores indicate higher automation potential.

**Dimension 2 — Consequence Severity of Errors (1–5 scale, inverse)**

If an automated step produces an incorrect output, how severe are the consequences?

- A score of 1 means errors are immediately visible, easily corrected, and costless (low severity = high automation potential).
- A score of 5 means errors are irreversible, legally significant, or harmful to people (high severity = lower automation potential regardless of rule-based specification).

**INTERPRETING THE OUTPUT**

The framework produces a two-dimensional profile, not a single score. A workflow can be highly rule-based and highly high-stakes. This combination does not rule out automation, but it mandates human-oversight checkpoints, extensive testing, and explicit approval gates before the agent takes any irreversible action.

**Shared vocabulary**

The vocabulary of this assessment — rule-based, high-stakes, reversibility, blast radius — will be used throughout the course.

#### Learning Resources

* Wing, J. M. (2006). [Computational thinking](https://dl.acm.org/doi/pdf/10.1145/1118178.1118215){target=_blank}. Communications of the ACM, 49(3), 33-35

[**Reading Guide Chapter 4 - Workflow thinking**](reading-guides.md#reading-guide-2) - Wooldridge & Jennings (1995): Intelligent Agents

#### Chapter 4 Quiz

[Take the Chapter 4 Quiz](chapter-quizzes.md#chapter-4-quiz){ .md-button }

### Chapter 5: Responsible AI — From Principle to Practice, Starting Now

#### Chapter 5 Lesson

Module 1 introduces responsible deployment not as a separate ethics unit, but as an integral part of the automation assessment framework. The high-stakes dimension of the two-dimensional assessment is itself a risk management instrument. The NIST AI Risk Management Framework (2023) and the AI4People ethical principles (Floridi et al., 2018) provide the formal governance vocabulary the course will use throughout.

**NIST AI RISK MANAGEMENT FRAMEWORK (2023)**

The NIST AI RMF 1.0 identifies four core functions — Govern, Map, Measure, Manage — that organizations should enact across the AI system lifecycle. Module 1 introduces the Map function: identifying the context in which an AI system will operate, the risks it poses, and the stakeholders it affects. The Workflow Audit Project you complete in Module 1 is a foundational Map exercise: you identify three workflows, characterize their risk profiles, and document the consequences of automation errors.

!!! note "Note"

    FOUNDATIONAL PRINCIPLE
    'The AI did it' is never a complete ethical or legal answer. When an AI agent takes an action
    — sends an email, modifies a file, charges a payment, contacts a person — a human being
    or organization is accountable for that action. The agent is a tool; the designer, deployer, and
    operator of that tool bear the accountability. This principle will be reinforced in every module
    and constitutes the foundational ethical commitment of the course.

Floridi et al.'s (2018) AI4People framework articulates five ethical principles for AI systems that
professional practitioners should be able to identify and apply: 

* beneficence (AI should benefit people), 
* non-maleficence (AI should not harm people), 
* autonomy (AI should preserve human agency), 
* justice (AI's benefits and risks should be equitably distributed), and 
* explicability (AI decisions should be intelligible to affected parties). 

These principles are not abstract values —
they translate directly into design decisions about oversight mechanisms, error handling,
permission scoping, and audit logging for production AI systems.

#### Learning Resources

* AI, N. (2023). [Artificial intelligence risk management framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf?isid=enterprisehub_us&ikw=enterprisehub_us_lead%2Fhow-to-responsibly-use-ai-powered-hr-tools_textlink_https%3A%2F%2Fnvlpubs.nist.gov%2Fnistpubs%2Fai%2FNIST.AI.100-1.pdf){target=_blank}. URL: https://nvlpubs. nist. gov/nistpubs/ai/nist. ai, 100-1.
* Floridi, L., Cowls, J., Beltrametti, M., Chatila, R., Chazerand, P., Dignum, V., ... & Vayena, E. (2018). [AI4People—An ethical framework for a good AI society: Opportunities, risks, principles, and recommendations](https://link.springer.com/content/pdf/10.1007/s11023-018-9482-5.pdf){target=_blank}. Minds and machines, 28(4), 689-707.

[**Reading Guide Chapter 5 - Responsible AI**](reading-guides.md#reading-guide-5)

#### Chapter 5 Quiz

[Take the Chapter 5 Quiz](chapter-quizzes.md#chapter-5-quiz){ .md-button }

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1:-Foundational-Concepts){target=_blank} (wiki page last changed 2026-07-23). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-1/foundational-concepts.md){target=_blank}.</p>
