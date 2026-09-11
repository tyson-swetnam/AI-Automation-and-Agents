---
title: Module 1 Chapter Quizzes
description: Five self-evaluating five-question chapter quizzes with collapsed answer keys and per-option feedback for Module 1, From Prompts to Pipelines.
type: Assessment
tags:
- module-1
- student-facing
- quiz
- ai-agents
- agent-loop
- automation-paradigms
- workflow-audit
- self-assessment
- answer-key
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
# Module 1 Chapter Quizzes

These quizzes are self-evaluating. For each question, select your answer, then read the feedback section immediately below. Feedback is provided for every option — including why incorrect options are wrong — so you can diagnose your reasoning, not just check your answer.

Each quiz has **5 questions**. Two attempts are permitted; your best score is retained.

## Chapter 1 Quiz — Redefining Intelligence: What AI Agents Actually Are { #chapter-1-quiz }

*Based on Reading Guide 1: Wooldridge & Jennings (1995), LangChain Conceptual Guide, IBM Technology Video*

### Question 1

Wooldridge and Jennings (1995) define four properties that constitute a "weakly" intelligent agent. A traditional rule-based automation script runs at 6 a.m. every day and executes the same fixed sequence of steps whatever it finds — an empty inbox, a changed file format, a folder that no longer exists. Which property does this behavior most directly violate, and why?

A. Social ability — the script cannot interact with other agents using communication protocols.

B. Reactivity — the script does not respond to changes in its environment; it executes the same fixed sequence regardless of environmental state.

C. Pro-activeness — the script runs on a schedule, and pro-activeness is the property of acting on external triggers such as a clock.

D. Autonomy — the script requires continuous human scheduling to operate and cannot act independently.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** A rule-based script follows a predetermined sequence and does not sense or respond to changes in environmental conditions — it executes the same steps whether or not the environment has changed relevantly. Wooldridge and Jennings define reactivity as the capacity to perceive the environment and respond to changes "in a timely fashion." A script that ignores environmental state violates this property, regardless of how sophisticated its fixed logic is.

    ❌ **A is incorrect.** Social ability concerns the capacity to communicate with other agents using agent communication languages — a property relevant to multi-agent systems. A script's failure to exhibit social ability is a genuine limitation, but it is not the property most directly violated by the description "fixed sequence of steps." Many legitimate agents also lack social ability in the technical sense.

    ❌ **C is incorrect.** It gets pro-activeness backwards. Responding to external stimuli, a clock included, is the territory of reactivity; pro-activeness is goal-directed initiative that goes beyond reacting — in the lesson's words, a pro-active agent "does not merely react to stimuli." The script does lack initiative, but that is not what this option claims, and the evidence in the description — the same steps whatever the environment holds — points at reactivity.

    ❌ **D is incorrect as the best answer.** Autonomy refers to operating without continuous human direction during execution — not merely without a human scheduling trigger. Many scripts run without human intervention once initiated. The scheduling mechanism does not itself violate autonomy; the fixed, environment-ignoring execution sequence is the more salient failure point.

### Question 2

In the LangChain Conceptual Guide's four-stage agent loop, what is the primary function of the **Observe** stage?

A. To make the stop-or-continue decision — that is its only job; the tool result itself is carried into the next step by the Plan stage.

B. To update the agent's context window with the result of the previous action, enabling the agent to plan the next step with current information.

C. To log the agent's actions to an external audit trail for compliance and monitoring purposes.

D. To retrieve relevant background information from the agent's memory store before the next Plan stage.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The Observe stage feeds the result of the completed tool call or action back into the agent's context window. This updated context is what the LLM uses as input to the next Plan stage. Without Observation, the agent would plan each successive step using only its original context — it would be blind to what its prior actions actually produced, making multi-step task completion unreliable. The loop's effectiveness depends entirely on this feedback mechanism.

    ❌ **A is incorrect.** Observe does include the stop-or-continue decision — the lesson's table says it "decides whether to loop again or conclude" — but that is not its only job, and the Plan stage does not carry the result forward. Observe reads the tool output and updates the agent's state, and the decision to loop or conclude is made from that updated state. Without the update in B there would be nothing to decide from, which is why B, not A, is the Observe stage's primary function.

    ❌ **C is incorrect.** Audit logging is an infrastructure concern in production deployment, not a function of the Observe stage in the conceptual agent loop. The LangChain guide does not define Observe as a logging step. Logging may be implemented alongside Observation but is architecturally distinct.

    ❌ **D is incorrect.** Memory retrieval is architecturally associated with the Perceive stage (gathering initial context) or may occur during the Plan stage when the agent queries its memory store. The Observe stage specifically handles the return value of the action just executed — it is forward-feeding into the next cycle, not backward-looking into long-term memory.

### Question 3

A product team describes their new software as an "AI agent" because it uses a large language model to answer customer service questions in a chat window. Applying Wooldridge and Jennings' framework, which statement best characterizes this system?

A. It qualifies as a full agent because it uses an LLM, which satisfies the autonomy and reactivity properties by design.

B. It likely fails the pro-activeness property: without a mechanism to initiate actions toward goals, it functions as a reactive chatbot that responds to prompts rather than pursuing objectives.

C. It qualifies as an agent if and only if it can escalate a case to a human supervisor, because that demonstrates social ability.

D. The question cannot be answered without knowing whether the LLM was fine-tuned on domain-specific data.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** A chat interface that generates responses to user prompts satisfies reactivity (it responds to input) but does not exhibit pro-activeness — it takes no goal-directed initiative without a user prompt. It also likely lacks meaningful autonomy if it cannot take actions in the world beyond generating text. This system is accurately described as a chatbot, not an agent in the Wooldridge and Jennings sense. The commercial use of "AI agent" in product marketing is precisely the terminological overloading the authors warn against.

    ❌ **A is incorrect.** Using an LLM does not automatically satisfy any of the four agent properties. The LLM is a component; whether the system built around it satisfies autonomy, reactivity, pro-activeness, and social ability depends on the system's architecture, not the model it incorporates. Many LLM-based chatbots are not agents.

    ❌ **C is incorrect.** Social ability in the Wooldridge and Jennings framework refers to communication using defined agent communication languages in multi-agent contexts — not to the common-language notion of "social" behavior. The ability to escalate to a human might satisfy a practical requirement, but it does not constitute social ability in the technical sense, and social ability alone would not make the system a full agent.

    ❌ **D is incorrect.** Fine-tuning concerns the quality of the LLM's outputs, not the architectural properties that determine agent status. Whether the model is fine-tuned has no bearing on whether the surrounding system exhibits autonomy, reactivity, pro-activeness, or social ability.

### Question 4

The ReAct (Reasoning and Acting) pattern structures agent reasoning as alternating Thought → Action → Observation cycles. What cognitive function does the **Thought** step perform that is not performed by a conventional function call in a deterministic program?

A. It converts natural language input into structured API parameters.

B. It selects which tool to invoke and generates the rationale for that selection based on the current context, enabling flexible, context-sensitive control flow.

C. It verifies that the previous action completed without error before proceeding to the next step.

D. It retrieves relevant examples from the agent's few-shot example library to improve output quality.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** In a deterministic program, the control flow (which function to call next) is specified statically by the programmer. In ReAct, the Thought step uses the LLM to reason about the current situation — including the goal, prior observations, and available tools — and dynamically select the most appropriate next action. This is qualitatively different from a function call: the control flow is generated at runtime by the model's reasoning, not pre-specified by code. This is what enables agents to handle novel situations that the programmer did not anticipate.

    ❌ **A is incorrect.** Converting natural language to structured parameters is part of how the agent invokes a tool (a parsing or templating function), not what the Thought step does. Parameter extraction may occur as part of the Action step, but the Thought step's function is reasoning about what action to take, not formatting that action's inputs.

    ❌ **C is incorrect.** Error verification is a function of the Observation step — the agent reads the result of the action (including error signals) and incorporates that into its context. The Thought step precedes the action and cannot verify an action that has not yet occurred.

    ❌ **D is incorrect.** Few-shot example retrieval is an optional technique for improving LLM performance but is not what defines or characterizes the Thought step in the ReAct pattern. The Thought step can operate with or without retrieved examples; its defining feature is dynamic reasoning about the current context to select the next action.

### Question 5

A colleague argues: "We should use an AI agent for this workflow because agents are always more powerful than scripts." Which response best applies Wooldridge and Jennings' framework to evaluate this claim?

A. The colleague is correct: agents are definitionally more capable than scripts because they can use tools, while scripts cannot.

B. The claim is false: scripts are always preferable because they are deterministic and auditable, whereas agents introduce unpredictable behavior.

C. The claim is imprecise: "more powerful" depends on the workflow's environmental properties. For deterministic, fully rule-specifiable workflows, a script may be preferable; for dynamic, partially observable environments, an agent architecture is more appropriate.

D. The claim is correct only if the agent uses a large language model with at least 70 billion parameters, which is the threshold at which reasoning capability surpasses scripted logic.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** Wooldridge and Jennings' framework implies that agent properties — especially reactivity and pro-activeness — are most valuable in environments that are dynamic, partially observable, and non-deterministic. For workflows that are fully deterministic and can be completely specified in advance, a script is often more appropriate: it is predictable, auditable, and carries no additional overhead. This maps directly onto the Module 1 Workflow Decomposition Framework's distinction between rule-based and non-rule-based workflows. The choice between agent and script is a professional judgment, not a categorical hierarchy.

    ❌ **A is incorrect.** The ability to call tools is an architectural feature, not a guarantee of superiority. Scripts can also call APIs and external services. The relevant distinction is whether the system responds to environmental changes and takes goal-directed initiative — not merely whether it can invoke external functions.

    ❌ **B is incorrect.** This is an overcorrection. Agents are the appropriate architecture for a wide class of professionally important workflows — particularly those involving unstructured input, dynamic conditions, or multi-step reasoning that cannot be fully pre-specified. Dismissing agents in favor of scripts in all cases ignores the substantial class of problems for which scripted automation is inadequate.

    ❌ **D is incorrect.** Parameter count is a proxy for model capability, not a meaningful threshold for determining when an agent architecture supersedes scripted logic. The choice of agent vs. script is determined by workflow properties (observability, determinism, goal complexity), not by the size of the underlying model. This option conflates model capability with architectural design choice.

## Chapter 2 Quiz — The Automation Ecosystem: Three Paradigms, One Spectrum { #chapter-2-quiz }

*Based on Reading Guide 4: Automation Landscape Overview*

### Question 1

An organization needs to automate a workflow in which invoice PDFs received by email are parsed, key fields are extracted, a payment authorization status is checked against an internal database, and an approval or rejection notification is sent to the submitting vendor. Which statement best justifies selecting a **low-code** framework over a no-code platform for this workflow?

A. Low-code is always more appropriate for financial workflows because financial data is too sensitive for no-code platforms.

B. The workflow requires orchestrating multiple heterogeneous systems (email, PDF parsing, internal database, notification) and conditional routing logic that exceeds what most no-code visual builders support without custom scripting.

C. Low-code frameworks cost less per execution than no-code platforms, making them economically superior for any workflow that runs more than once per day.

D. No-code platforms cannot connect to internal databases, so any workflow requiring a database lookup requires a low-code or code-first approach.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Low-code frameworks are appropriate when a workflow requires orchestrating multiple heterogeneous systems and applying conditional logic that cannot be expressed within the constraint model of a visual no-code builder. The invoice workflow described involves: parsing unstructured PDF content (non-trivial data extraction), querying an internal database (requiring custom API integration or direct DB connection), and routing output conditionally. These requirements push beyond what most no-code tools handle reliably without workarounds. B correctly uses workflow properties — not categorical preferences — to justify the paradigm selection.

    ❌ **A is incorrect.** Financial sensitivity is a data governance concern, not a paradigm selection criterion in isolation. Data governance issues affect all three paradigms differently (no-code introduces vendor server transmission risk; self-hosted low-code eliminates it), but this concern does not categorically exclude no-code — self-hosted n8n, for example, may satisfy data governance requirements for financial workflows. The paradigm choice should be grounded in the specific data handling architecture, not a blanket rule.

    ❌ **C is incorrect.** Cost at scale is a legitimate paradigm comparison dimension, but the breakeven point depends on execution volume, platform pricing, and maintenance costs. "More than once per day" is not a meaningful threshold. Cost is one factor in a multi-criteria paradigm selection decision, not a decision rule by itself.

    ❌ **D is incorrect.** Many no-code platforms do support database integrations through native connectors (e.g., n8n has PostgreSQL, MySQL, and MongoDB nodes). The limitation is not categorical exclusion from database connectivity but rather the complexity of the conditional logic and heterogeneity of the system landscape, which is captured by option B.

### Question 2

A data science team at a mid-sized enterprise builds a no-code workflow using a third-party cloud automation platform to route weekly performance report data from their analytics tool to a shared Slack channel. The security team later raises a compliance concern. What is the most likely source of that concern?

A. No-code platforms use visual builders that are not compatible with enterprise security standards.

B. The performance report data is routed through the automation vendor's cloud servers, potentially outside the organization's data processing agreements and regulatory jurisdiction.

C. Slack is an external communication platform that violates internal data residency requirements.

D. No-code workflows cannot be audited, which violates most enterprise compliance frameworks.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The primary data governance risk of cloud-hosted no-code platforms is that organizational data — including potentially sensitive performance metrics — is transmitted to and processed on the vendor's servers. Unless a Data Processing Agreement (DPA) is in place and the vendor's server locations comply with applicable data residency regulations (e.g., GDPR, HIPAA, SOC 2), this transmission may constitute a compliance violation. This is the most commonly underweighted factor in paradigm selection, as the Automation Landscape Overview explicitly notes.

    ❌ **A is incorrect.** Visual builders are interface design choices, not a security vulnerability in themselves. Enterprise-grade no-code platforms are widely used in regulated industries and are compatible with security standards — the concern is data handling, not the interface paradigm.

    ❌ **C is incorrect** as the primary concern. While Slack data residency may itself be a concern in some regulated environments, the question specifies that the security team is raising a concern about the automation workflow, not the Slack destination. The critical compliance issue is the intermediate routing through the third-party automation vendor's servers, not the final destination.

    ❌ **D is incorrect.** No-code workflows can be audited — most enterprise no-code platforms provide execution logs. The auditability gap is a relative concern compared to code-first approaches (where every decision is in version-controlled code), but it is not a categorical audit impossibility. The more pressing compliance issue is data transmission, not auditability.

### Question 3

The Automation Landscape Overview states that "the paradigms are not hierarchically ranked." What is the most rigorous professional interpretation of this claim?

A. The three paradigms are equivalent in capability, so practitioners should choose based solely on personal preference.

B. Paradigm selection should be determined by matching the workflow's technical requirements, organizational context, and data governance constraints to the paradigm's comparison profile — not by treating code-first as the "gold standard."

C. No-code tools have become as capable as code-first approaches due to recent platform improvements, eliminating the historical capability gap.

D. Organizations should maintain proficiency in all three paradigms simultaneously to remain flexible, regardless of the specific requirements of any given workflow.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The claim that paradigms are not hierarchically ranked means that professional judgment — informed by workflow properties, team capabilities, and organizational context — determines the appropriate paradigm. A seasoned AI engineer who selects a no-code tool for a repetitive, low-complexity administrative workflow is not compromising quality; they are demonstrating appropriate tool selection. The reverse is equally true: deploying a code-first custom agent for a simple notification workflow that n8n would handle reliably is engineering overreach. The paradigm taxonomy is a decision framework, not a capability hierarchy.

    ❌ **A is incorrect.** The claim does not mean the paradigms are equivalent in capability — they clearly differ across the six comparison dimensions. "Not hierarchically ranked" refers to the absence of a universal superiority ordering, not to the absence of meaningful capability differences. Personal preference is an inappropriate primary selection criterion.

    ❌ **C is incorrect.** Recent platform improvements in no-code tools have expanded their capabilities, but the structural trade-offs described in the overview remain: no-code tools still sacrifice flexibility for accessibility, still carry higher data governance risk in cloud-hosted deployments, and still become cost-inefficient at high execution volumes relative to code-first alternatives. The capability gap has narrowed in some dimensions but has not been eliminated.

    ❌ **D is incorrect.** Organizational capability investment is a relevant workforce development consideration, but it does not follow from the "not hierarchically ranked" claim. The point of the claim is about selection criteria for specific workflows, not about team capability breadth. Additionally, maintaining proficiency in all paradigms simultaneously is a resource-intensive aspiration that most organizations calibrate based on their actual workflow portfolio.

### Question 4

An independent researcher with strong Python skills wants to build an automated literature review workflow that fetches papers from multiple academic APIs, extracts key concepts using an LLM, and writes structured summaries to a local database. Which paradigm is most appropriate, and why?

A. No-code, because the researcher does not need the full flexibility of code-first for what is essentially a data pipeline.

B. Low-code (e.g., LangChain), because it provides LLM integration abstractions while allowing custom Python for the API calls and database writes, matching the researcher's skill level and workflow complexity.

C. Code-first (custom Python agents), because data governance requires that all data remain local, which eliminates cloud-hosted no-code options, and the multi-API orchestration exceeds what low-code frameworks support.

D. No-code (n8n), because the researcher can use n8n's HTTP Request node to call any academic API without writing Python.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Low-code frameworks like LangChain are specifically designed for workflows that combine LLM reasoning with tool integration (API calls, database operations) and require moderate to complex orchestration. The researcher's Python proficiency means the low-code barrier is manageable, and the workflow — multi-API retrieval, LLM extraction, structured output — is a canonical LLM-agent orchestration task. LangChain provides purpose-built abstractions (tool decorators, chain composition, LLM bindings) that reduce engineering effort compared to building from scratch in pure Python while retaining full control over data handling.

    ❌ **A is incorrect.** A no-code platform would likely struggle with the multi-API orchestration, custom LLM prompt engineering, and structured database writes required here. Additionally, cloud-hosted no-code platforms introduce data governance risk for academic data that may be unpublished or proprietary. The researcher's Python skills make low-code or code-first viable and preferable.

    ❌ **C is incorrect as the best answer.** Data governance (local data requirement) is a valid concern, but it does not categorically require code-first — low-code frameworks like LangChain can be run entirely locally (with Ollama for the LLM, for instance). The claim that "multi-API orchestration exceeds what low-code frameworks support" is factually incorrect: multi-API orchestration is precisely what LangChain and similar frameworks are designed for. Code-first is a valid option but not required given the available low-code alternatives.

    ❌ **D is incorrect.** While n8n's HTTP Request node can call any API, building LLM-extraction logic with structured prompt management, dynamic concept extraction, and conditional output routing within n8n's visual builder would require extensive workarounds. For a researcher with strong Python skills, this approach sacrifices capability without gaining accessibility — the primary benefit of no-code.

### Question 5

According to the Automation Landscape Overview, what is the primary technical reason that code-first automation provides "absolute data governance" in a way that no-code platforms cannot guarantee?

A. Code-first automation uses encryption algorithms that no-code platforms do not support.

B. Code-first automation can be deployed on private infrastructure with local models, ensuring that data never leaves the organization's controlled environment.

C. Code-first automation is subject to stricter regulatory oversight, which forces developers to implement data governance controls.

D. Code-first automation produces human-readable code that can be independently audited, whereas no-code platform logic is proprietary and cannot be inspected.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The data governance advantage of code-first automation is architectural: the entire system — including the AI model, the orchestration logic, and the data processing — can be deployed on the organization's private infrastructure. When a local open-weight model (e.g., via Ollama) handles LLM inference and all computation runs on privately controlled servers, data never transits to third-party vendor systems. This is categorically different from a cloud-hosted no-code platform, where the vendor processes the data by design. No encryption scheme can eliminate the governance risk of third-party data processing, because the third party possesses the decrypted data during processing.

    ❌ **A is incorrect.** Encryption is a data protection technique available to all paradigms, not a code-first exclusive. Cloud-hosted no-code platforms also use TLS encryption in transit and encryption at rest. The governance issue is not about encryption but about who controls the computational environment where data is processed.

    ❌ **C is incorrect.** Code-first automation is not subject to categorically different regulatory oversight than no-code automation. Regulatory requirements apply to the data and the business process, not the tooling paradigm. If anything, the regulatory burden of demonstrating compliance may be higher for code-first because the organization owns the full system and cannot rely on vendor compliance certifications.

    ❌ **D is incorrect.** Auditable code is a real advantage of code-first automation, but it answers a different question — can you inspect what the system does? — not where the data goes. An auditable system can still send every record to a third-party API. The governance advantage the Automation Landscape Overview describes is data residency: the whole system, model included, can run on infrastructure the organization controls, so the data never leaves it.

## Chapter 3 Quiz — AI Literacy as a New Professional Imperative { #chapter-3-quiz }

*Based on Reading Guide 3: Ng et al. (2021) and Long & Magerko (2020)*

### Question 1

Ng et al.'s (2021) four-pillar AI literacy model places "Know and Understand AI" as the foundational pillar. Which statement best explains why this ordering is not merely pedagogical convenience but reflects a structural dependency?

A. Students must pass a knowledge test before being permitted access to AI tools, which requires foundational knowledge to precede applied skills.

B. Evaluating and creating AI systems presupposes the ability to use and apply them, which in turn presupposes conceptual knowledge of what AI is and how it functions — each pillar depends on the prior one being in place.

C. Foundational knowledge is quickest to teach, so it is placed first to build early learner confidence before introducing more challenging applied skills.

D. Regulatory compliance requirements mandate that practitioners demonstrate conceptual AI knowledge before deploying AI systems in organizational contexts.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Ng et al.'s sequencing reflects a genuine epistemic dependency: you cannot reliably evaluate or critique an AI system if you have no understanding of how it works; you cannot use an AI tool appropriately if you do not understand what it is capable of and where it fails. The hierarchy is not an arbitrary pedagogical sequence but a dependency structure — the higher pillars presuppose the lower ones. This is why practitioners who skip foundational understanding and go directly to tool use often exhibit characteristic failure patterns: they over-trust outputs, fail to recognize errors, and cannot adapt when tools behave unexpectedly.

    ❌ **A is incorrect.** Ng et al.'s framework is an analytical model of AI literacy competencies, not a gatekeeping policy. The paper does not recommend barring learners from tools until they pass knowledge assessments; it describes the competency dependencies that educators and practitioners should recognize in designing instruction and professional development.

    ❌ **C is incorrect.** Ease of teaching is not the organizational principle behind Ng et al.'s hierarchy. Foundational knowledge (the AI landscape, how models are trained, what ML algorithms do) is not necessarily easier to teach than applied skills — in some contexts, hands-on tool use is more accessible as a starting point. The sequencing reflects competency dependencies, not instructional difficulty.

    ❌ **D is incorrect.** Regulatory compliance requirements for AI practitioners vary widely by jurisdiction, industry, and application domain. Ng et al. do not ground their framework in regulatory mandates; they ground it in a systematic literature review of what competencies practitioners actually need to engage with AI effectively and responsibly.

### Question 2

Long and Magerko (2020) identify "Recognizing AI" as a core AI literacy competency. In a graduate professional context, what is the primary professional significance of this competency?

A. It enables practitioners to identify AI-generated content in research publications, protecting academic integrity.

B. It enables practitioners to make informed decisions about data handling, accountability, and oversight in systems where AI components may not be visible or explicitly disclosed.

C. It enables practitioners to distinguish AI systems from human workers in automated customer service contexts, satisfying disclosure requirements.

D. It enables practitioners to avoid using AI tools that have not been certified by institutional review processes.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** In professional contexts, AI is frequently embedded in enterprise software, productivity tools, and analytical platforms without explicit disclosure. A practitioner who cannot recognize when AI is making decisions — about credit risk, content moderation, scheduling, or resource allocation — cannot exercise appropriate oversight, assign accountability, or assess the reliability of system outputs. Long and Magerko's "Recognizing AI" competency is professionally significant precisely because AI is pervasive but often invisible, and the consequences of treating AI-generated outputs as if they were rule-based or human-generated outputs can be severe.

    ❌ **A is incorrect.** Identifying AI-generated content in publications is a specific application of the competency, not its primary professional significance at the graduate level. Academic integrity applications are real but narrow relative to the systemic organizational significance of recognizing AI decision-making in enterprise and professional contexts.

    ❌ **C is incorrect.** Disclosure requirements in customer service are a specific regulatory context (primarily consumer protection regulation). The competency has far broader significance across organizational decision-making contexts where no disclosure requirement exists but where AI is making consequential decisions.

    ❌ **D is incorrect.** Institutional review processes for AI tools vary widely and are not a focus of Long and Magerko's framework. The "Recognizing AI" competency is about perceptual and analytical literacy — identifying AI components in systems — not about navigating certification procedures.

### Question 3

Both Ng et al. (2021) and Long & Magerko (2020) argue that AI literacy is not reducible to technical proficiency with AI tools. Which of the following competency descriptions best illustrates the dimension of AI literacy that cannot be reduced to technical skill?

A. The ability to write a Python function that calls an LLM API and parses the JSON response.

B. The ability to fine-tune a pre-trained language model on a domain-specific dataset using transfer learning.

C. The ability to identify the populations most likely to be adversely affected by a proposed AI-based hiring screening system and articulate why those effects constitute a justice concern.

D. The ability to configure an n8n workflow to route incoming emails based on NLP-classified intent labels.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** Identifying affected populations and articulating their concerns as justice issues requires sociotechnical literacy — understanding both how the system works technically and how it interacts with social structures, power asymmetries, and historical inequities. This competency draws on Long and Magerko's ethical and societal understanding family and Ng et al.'s AI Ethics pillar. It cannot be reduced to programming skill or tool operation because it requires the practitioner to reason about social consequences, not just technical function. This is precisely the dimension of AI literacy both papers argue is distinct from and irreducible to technical competency.

    ❌ **A is incorrect.** This is a purely technical skill — API integration and data parsing — with no AI literacy dimension that goes beyond coding competency. It corresponds to the "Use and Apply" pillar, not the ethical or critical evaluation pillars.

    ❌ **B is incorrect.** Fine-tuning is a sophisticated technical skill, but it remains within the technical dimension of AI literacy. Understanding that fine-tuning can introduce or amplify biases would be a non-technical dimension, but the competency as stated ("the ability to fine-tune") is entirely technical.

    ❌ **D is incorrect.** Configuring an n8n workflow is an applied tool-use competency — important, but technical in nature. Whether the NLP classification is appropriate for the use case, whether it introduces bias in email routing, or who is affected if it fails are the non-technical literacy dimensions; the configuration itself is not.

### Question 4

Ng et al. (2021) distinguish AI literacy from digital literacy and data literacy, arguing that AI-specific competencies are not captured by existing frameworks. Which property of AI systems most directly necessitates a distinct literacy framework?

A. AI systems are more expensive to operate than traditional software, requiring practitioners to understand cost-benefit analysis in a new domain.

B. AI systems make probabilistic, context-sensitive inferences rather than executing deterministic rules, which means that understanding their behavior requires reasoning about uncertainty, training distributions, and failure modes that do not exist in traditional software.

C. AI systems are developed by specialized research teams whose internal methods are not accessible to ordinary practitioners, requiring a specific literacy for interfacing with vendor products.

D. AI systems are regulated differently than traditional software, necessitating a separate compliance literacy framework.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The fundamental property that distinguishes AI systems from traditional software — and that necessitates a distinct literacy — is their probabilistic, learned behavior. Traditional software executes deterministic rules that can be read and predicted from the code. AI systems (particularly ML-based systems) generate outputs from statistical patterns in training data; their behavior is not directly readable from their parameters, may vary with context, and can fail in ways that have no analogue in rule-based systems (e.g., distributional shift, hallucination, adversarial vulnerability). Understanding these failure modes, reasoning about uncertainty in outputs, and evaluating whether a model's training distribution matches the deployment context are competencies that digital literacy and data literacy frameworks did not anticipate.

    ❌ **A is incorrect.** Cost considerations are a practical matter for any technology adoption decision. They may require economic literacy but do not constitute a distinct literacy framework. Moreover, cost understanding is not what Ng et al. identify as the basis for AI literacy's distinctiveness.

    ❌ **C is incorrect.** Vendor opacity is a real challenge, but it characterizes many commercial software categories (enterprise ERP systems, for example) — it is not unique to AI. The distinctiveness of AI literacy derives from the nature of learned, probabilistic systems, not from the organizational opacity of AI vendors.

    ❌ **D is incorrect.** Regulatory compliance is domain- and jurisdiction-specific and does not constitute an AI-specific literacy framework. The NIST AI RMF (Chapter 5) addresses AI governance, but this is a compliance instrument, not what Ng et al. identify as the basis for AI literacy's distinctiveness from digital and data literacy.

### Question 5

Long and Magerko (2020) define AI literacy as including "the ability to communicate and collaborate effectively with AI." How does this competency differ from the ability to prompt an LLM effectively?

A. It does not differ — effective prompting is the operational definition of communicating with AI.

B. Effective prompting is one technical implementation of communication with AI; the broader competency also includes understanding the model's reasoning process, calibrating trust in outputs, recognizing when AI collaboration is inappropriate, and communicating AI-generated results accurately to non-specialist audiences.

C. Communicating with AI refers specifically to using natural language APIs, whereas prompting is a technique applied to chat interfaces — they address different technical contexts.

D. The ability to communicate with AI is a metacognitive competency about understanding one's own thought processes when using AI tools, rather than the interpersonal communication skills implied by the word "communicate."

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Long and Magerko's competency encompasses a multi-layered set of practices. Effective prompting — crafting inputs that reliably elicit the desired output — is one technical skill within this competency. But communication and collaboration with AI also requires: understanding why the model responds as it does (interpretability literacy), knowing when to trust versus verify outputs (epistemic calibration), recognizing use cases where AI collaboration introduces risk rather than value (critical evaluation), and translating AI-generated insights accurately to stakeholders who did not participate in the AI interaction (communication to non-specialists). These dimensions go well beyond prompt engineering.

    ❌ **A is incorrect.** Reducing "communicate and collaborate with AI" to prompting skill conflates a technical sub-skill with the full competency. Long and Magerko explicitly include critical evaluation, societal awareness, and communication to non-specialists as components of AI literacy — dimensions that cannot be captured by prompt engineering ability alone.

    ❌ **C is incorrect.** Long and Magerko do not draw a technical distinction between natural language APIs and chat interfaces in defining this competency. The distinction between prompting and communication is conceptual — about depth and breadth of competency — not a matter of which technical interface is used.

    ❌ **D is incorrect.** While metacognitive awareness is a valuable professional competency, Long and Magerko's "communicate and collaborate with AI" is not defined primarily as metacognitive. It includes outward-facing communication skills (explaining AI results to stakeholders) and practical collaboration patterns with AI systems — it is not primarily an introspective competency.

## Chapter 4 Quiz — Workflow Thinking as a Professional Competency { #chapter-4-quiz }

*Based on Reading Guide 2: Wing (2006) and Wooldridge & Jennings (1995)*

### Question 1

Jeannette Wing (2006) argues that abstraction is the most important cognitive skill in computational thinking. In the context of the Module 1 Workflow Decomposition Framework, which activity best demonstrates abstraction as Wing defines it?

A. Listing every click and keyboard shortcut required to complete a workflow step, so that the specification is unambiguous.

B. Identifying the logical input, transformation, and output of each workflow step while omitting implementation-specific details that would change if the tool were replaced.

C. Drawing a visual flowchart of all decision points in the workflow using standardized BPMN notation.

D. Timing each step of the workflow to establish a quantitative baseline for measuring automation ROI.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Wing defines abstraction as "suppressing irrelevant detail to expose the essential structure of a problem." In workflow decomposition, this means specifying what a step does (its logical function: what goes in, what happens, what comes out) independently of how it is currently implemented (which application, which button, which keyboard shortcut). A specification that abstracts appropriately remains valid even if the underlying tool changes, and it communicates the step's function clearly to a system — human or AI — that might implement it differently. This is what makes a workflow specification generalizable.

    ❌ **A is incorrect.** Listing every click and keyboard shortcut is the opposite of abstraction — it is maximal concreteness at the implementation level. While such specificity might be appropriate for a narrow training document, it produces a workflow specification that is brittle (any interface change breaks it) and non-transferable (it cannot guide an agent using a different tool to accomplish the same step).

    ❌ **C is incorrect.** BPMN flowcharting is a useful visualization and formalization tool, but drawing a flowchart is not itself abstraction in Wing's sense. The quality of the abstraction depends on what level of detail is included in the flowchart, not on the notation used.

    ❌ **D is incorrect.** Timing steps is a measurement activity that produces quantitative data for ROI analysis — it is relevant to the automation assessment but is not an instance of abstraction. Abstraction is a cognitive process of structural reasoning, not measurement.

### Question 2

In the Module 1 Two-Dimensional Automation Assessment Framework, a workflow step is scored **5 on Dimension 1 (Rule-Based Specification)**. What does this score mean, and what does it imply for that step's contribution to the overall automation potential?

A. The step is fully deterministic: every valid input maps to a single correct output by a rule that applies consistently without human judgment. This maximizes the step's contribution to automation potential.

B. The step is highly complex and requires five distinct sub-steps, each of which must be handled separately by the automation framework.

C. The step has been implemented successfully in five previous automation projects and is therefore low-risk to automate.

D. The step affects five or more downstream steps, making it a high-leverage point in the workflow architecture.

??? success "Show answer and feedback"

    **Correct Answer: A**

    ✅ **A is correct.** Dimension 1 scores measure how fully a step can be specified as a deterministic rule applicable consistently across all inputs. A score of 5 means the step requires zero human judgment — every valid input maps to a single, unambiguous correct output through a rule the agent can execute reliably. This is the highest possible contribution to automation potential on Dimension 1. For example, "check whether invoice number appears more than once in column A" is fully rule-based: the answer is binary (yes/no) and applies the same logic regardless of the invoice's content.

    ❌ **B is incorrect.** The Dimension 1 scale measures judgment-vs.-rule specification, not step complexity or sub-step count. A step with five sub-steps could score anywhere on the 1–5 scale, depending on how rule-specifiable those sub-steps are.

    ❌ **C is incorrect.** Dimension 1 is a structural assessment of the step's specification properties, not a historical record of past automation attempts. Prior successful implementations are useful empirical evidence but do not define the scale.

    ❌ **D is incorrect.** The number of downstream steps affected by a given step describes its blast radius — a concept related to Dimension 2 (Consequence Severity), not Dimension 1. The dimensions measure independent properties and should not be conflated.

### Question 3

A workflow has the following profile: Dimension 1 (Rule-Based) = 5, Dimension 2 (Consequence Severity) = 5. What does the Two-Dimensional Assessment Framework prescribe for this workflow?

A. Full automation is contraindicated: high consequence severity always rules out automation regardless of how rule-based the workflow is.

B. The workflow can be automated immediately because the high rule-based score eliminates the risk implied by the high consequence severity.

C. Automation is feasible but requires human-oversight checkpoints, extensive testing, and explicit approval gates before any irreversible action is taken.

D. The workflow should be redesigned to reduce consequence severity before any automation decision is made.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** The framework produces a two-dimensional profile, not a single go/no-go score. A workflow that is fully rule-based (5) and high-stakes (5) is technically automatable — the steps can be specified precisely — but the severity of errors mandates human oversight. This combination calls for approval gates before irreversible actions, extensive adversarial testing, and monitoring infrastructure. The framework does not categorically prohibit automation in high-stakes domains; it mandates that the risk profile be addressed architecturally through oversight mechanisms.

    ❌ **A is incorrect.** The framework does not contain a categorical "always" prohibition on automating high-consequence workflows. Many high-stakes workflows — medical record routing, financial transaction processing, legal document filing — are automated in practice, precisely because they are also highly rule-based. The key is appropriate risk controls.

    ❌ **B is incorrect.** A high rule-based score does not eliminate consequence severity risk. Automated systems can fail in ways that a rule-based specification does not anticipate (data corruption, edge cases, infrastructure failure). High rule-based specification reduces the probability of certain failure modes; high consequence severity means that when failures do occur, their impact is severe. Both dimensions matter independently.

    ❌ **D is incorrect.** Recommending workflow redesign to reduce consequence severity may be appropriate in some contexts, but the framework does not prescribe redesign as the default response to a high-severity score. Many workflows cannot have their consequence severity reduced — sending an email to a client is inherently a non-trivial action. The framework's response to this combination is human oversight, not redesign.

### Question 4

Wing (2006) states that computational thinking involves "thinking recursively." In the context of the Workflow Decomposition Framework, which scenario best illustrates recursive workflow structure?

A. A workflow that loops through all items in a list and applies the same processing steps to each item, where each item's output feeds back as a potential trigger for the same loop.

B. A workflow with more than five sequential steps, where later steps depend on the outputs of earlier steps.

C. A workflow that must be re-run manually if it produces an error, because automation failure returns control to the human operator.

D. A workflow in which the same tool (e.g., an LLM) is used at multiple steps for different purposes.

??? success "Show answer and feedback"

    **Correct Answer: A**

    ✅ **A is correct.** Recursive workflow structure means a workflow (or a component of it) calls itself — or an instance of the same process is applied to its own output. The scenario described — a loop that processes each item in a list, where processed outputs may feed back as inputs to the same loop — is a canonical recursive pattern. This structure poses specific challenges for the Workflow Decomposition Framework because the number of loop iterations may be indeterminate at design time, and the workflow specification must account for both the base case (list exhausted, no error) and the recursive case (item processed, next item triggered).

    ❌ **B is incorrect.** Sequential dependencies (later steps depending on earlier outputs) describe a directed acyclic workflow, not a recursive one. Sequencing is a universal property of multi-step workflows; recursion specifically involves a structure calling back to itself or applying the same process to its own output.

    ❌ **C is incorrect.** Manual re-run after failure describes a human-in-the-loop error recovery pattern, not recursion. The workflow does not call itself; a human initiates a new execution. Recursion requires the structure to self-reference within the same execution context.

    ❌ **D is incorrect.** Using the same tool at multiple steps is tool reuse, not recursive structure. The workflow steps remain sequential; there is no self-referential call pattern.

### Question 5

According to Wing (2006), computational thinking is "a fundamental skill for everyone, not just computer scientists." What is the most direct implication of this claim for a professional who does not intend to write code but will be a primary user and commissioner of automated workflows?

A. Non-technical professionals do not need computational thinking skills because they can rely on AI engineers to translate their requirements into technical specifications.

B. Non-technical professionals must learn to program in at least one language to participate meaningfully in automation design.

C. Non-technical professionals who can decompose their own workflows into precise, unambiguous specifications will produce dramatically better automation outcomes than those who delegate specification entirely to technical implementers.

D. Non-technical professionals should focus exclusively on the business outcome layer (what the workflow should achieve) and avoid engaging with the technical implementation layer.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** Wing's claim implies that the cognitive skills underlying automation — decomposition, abstraction, pattern recognition — are valuable to anyone who interacts with computational systems, including those who commission rather than build them. In practice, the quality of an automated workflow is heavily determined by the quality of the specification provided to the implementer (human or AI). A professional who can decompose their own workflows precisely produces specifications that result in automations that actually match the intended process; one who cannot produces vague requirements that lead to mismatches, rework, and trust failures. The Workflow Audit Project in Module 1 is explicitly designed to develop this capability.

    ❌ **A is incorrect.** Delegating specification entirely to technical implementers systematically produces automations that do not match real workflows, because the practitioner possesses domain knowledge that the engineer lacks and cannot reliably infer. Wing's claim directly challenges the premise that non-technical users can simply "tell the engineer what they want" without engaging in the decomposition process themselves.

    ❌ **B is incorrect.** Wing explicitly argues that computational thinking is not equivalent to computer programming. The skills she identifies — decomposition, abstraction, pattern recognition, algorithmic thinking — can be exercised and applied without writing code. Requiring programming proficiency would contradict the paper's core argument.

    ❌ **D is incorrect.** Focusing exclusively on business outcomes while ignoring implementation logic produces specifications with insufficient precision. An outcome-only specification ("automate my invoice review process") leaves critical questions unanswered: what constitutes a valid invoice, what happens when a field is missing, what counts as a duplicate. Wing's framework implies that the professional should engage with the logical structure of the process — not its implementation code, but its decomposed specification.

## Chapter 5 Quiz — Responsible AI: From Principle to Practice, Starting Now { #chapter-5-quiz }

*Based on Reading Guide 5: NIST AI RMF 1.0 (2023) and Floridi et al. (2018)*

### Question 1

The NIST AI Risk Management Framework defines four core functions: Govern, Map, Measure, Manage. Which function does the Module 1 Workflow Audit Project most directly enact, and why?

A. Govern — because producing the Workflow Audit requires students to establish their personal accountability framework for AI use.

B. Measure — because the Workflow Audit's scores measure how the automated workflows perform once they are running.

C. Map — because the Workflow Audit identifies the context, risk profiles, and stakeholder impacts of specific AI-candidate workflows before any deployment decision is made.

D. Manage — because completing the Workflow Audit is itself a management action that controls which workflows are considered for automation.

??? success "Show answer and feedback"

    **Correct Answer: C**

    ✅ **C is correct.** The NIST AI RMF defines the Map function as identifying the context in which an AI system will operate, the risks it poses, and the stakeholders it affects — prior to deployment. The Workflow Audit Project does precisely this: students identify three real workflows, characterize their properties (rule-based specification, consequence severity, affected parties), and document the potential consequences of automation errors. This is a foundational Map exercise: establishing situational awareness about the risk landscape before any tool is selected or automation is built. The Measure and Manage functions follow from Map, but they presuppose it.

    ❌ **A is incorrect.** The Govern function in the NIST AI RMF refers to organizational-level policies, accountability structures, and culture-setting activities — it is an enterprise governance function, not an individual student activity. While personal accountability is a course value, the Workflow Audit does not constitute governance in the NIST sense.

    ❌ **B is incorrect.** Its premise is wrong: the Audit scores candidate workflows before anything is automated, so there is no running system whose performance could be measured. Its two scores record properties of each workflow — how rule-based it is and how severe its errors would be — and that is identifying context and risk, which is Map. In the AI RMF, Measure "uses knowledge relevant to AI risks identified in the MAP function" to analyze, assess, benchmark and monitor those risks, including by testing AI systems before deployment and regularly while in operation.

    ❌ **D is incorrect.** The Manage function involves implementing risk treatment plans and monitoring outcomes for deployed AI systems. The Workflow Audit occurs at the pre-deployment stage — no AI system has been deployed yet at this point. Managing implies an ongoing operational relationship with a deployed system, which is not what the Workflow Audit represents.

### Question 2

Floridi et al.'s (2018) AI4People framework presents explicability as a "meta-principle" that enables the other four ethical principles. Which of the following best explains this claim?

A. Explicability is more important than the other four principles and should be prioritized when they conflict.

B. Without the ability to understand why an AI system produced a given output, it is impossible to assess whether the system is beneficial, non-harmful, autonomy-preserving, or just — making explicability a prerequisite for evaluating all other principles.

C. Explicability is a legal requirement in most jurisdictions that governs AI deployment, making it the foundational compliance concern from which other requirements follow.

D. Explicability is the principle most requested by end users of AI systems, so satisfying it first increases user acceptance of AI and thereby enables the other principles to be implemented.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** Floridi et al. argue that explicability functions as a meta-principle because it is an enabling condition for evaluating all other principles. If you cannot understand why an AI system made a decision, you cannot determine whether that decision was beneficial (beneficence), whether it caused harm (non-maleficence), whether it preserved human choice (autonomy), or whether its effects were equitably distributed (justice). Explicability is not more ethically important than the others — it is epistemically prior: you must be able to understand a system's behavior before you can evaluate it against any ethical criterion.

    ❌ **A is incorrect.** Floridi et al. do not establish a priority ranking among the five principles in general. Describing explicability as a "meta-principle" does not mean it overrides others in cases of conflict — it means it enables evaluation of the others. The paper treats the five principles as complementary, not hierarchical.

    ❌ **C is incorrect.** Floridi et al.'s argument for explicability as a meta-principle is philosophical and ethical, not legal. While the EU AI Act and GDPR include explainability requirements, the AI4People paper's argument does not rest on regulatory precedent — it rests on the epistemic claim that evaluation requires understanding.

    ❌ **D is incorrect.** User acceptance and demand are empirical facts about stakeholder preferences, not the basis for Floridi et al.'s philosophical claim. The meta-principle argument is epistemological — about what is necessary to know whether a system is ethical — not sociological — about what users want.

### Question 3

An AI agent is deployed to process loan applications and automatically rejects applications from applicants whose addresses fall in specific postal codes. The system was not deliberately designed to discriminate by geography, but the historical training data reflects discriminatory lending patterns. Which Floridi et al. principle is most directly violated, and what is the most appropriate design response?

A. Non-maleficence is violated. The appropriate response is to shut down the system immediately until the training data is replaced.

B. Justice is violated, because the benefits (access to credit) and risks (rejection) are being distributed in a way that reflects and reinforces historical inequity. The appropriate design response includes auditing training data for discriminatory patterns, implementing post-hoc fairness metrics, and establishing human review for boundary cases.

C. Autonomy is violated, because applicants cannot appeal the automated decision or choose a human reviewer.

D. Beneficence is violated, because the system is not producing net benefit to society. The appropriate response is to add a human loan officer to review all decisions.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** The scenario describes a classic algorithmic fairness violation — historically biased training data producing disparate impact by geography (which often correlates with race or ethnicity). This most directly implicates the justice principle: the system distributes a significant benefit (credit access) and risk (rejection) in a pattern that reflects historical inequity rather than creditworthiness. The appropriate response is multi-layered: retrospective data audit, fairness metrics applied at evaluation time (e.g., disparate impact testing), explainability tools to surface which features drive rejections, and human-in-the-loop review for cases near the decision boundary. This response also engages non-maleficence (reducing harm) and explicability (understanding what drives decisions), illustrating the principles' interconnection.

    ❌ **A is incorrect** as the best answer, though non-maleficence is also implicated. Non-maleficence — AI should not harm people — is violated when discriminatory rejections harm applicants. However, immediate shutdown is not the only available response, and the scenario most precisely fits the justice principle because the harm is distributional: it systematically disadvantages specific populations, not just individual applicants. The justice principle is the more precisely targeted diagnosis.

    ❌ **C is incorrect** as the primary violation, though autonomy may also be implicated. Autonomy is most relevant when AI systems constrain human choice or agency. The absence of an appeals process is an autonomy concern, but the primary harm in the scenario is distributional — systematic group-level disadvantage — which is the domain of justice.

    ❌ **D is incorrect** as the primary violation, though beneficence is relevant. Adding a human reviewer is a plausible partial mitigation, but it does not address the systemic data problem, and it may simply move the discriminatory pattern to human decision-making rather than eliminating it. The diagnosis of "beneficence violation" and the remedy of "add a human" are both underpowered for the distributional injustice the scenario describes.

### Question 4

The course establishes the following foundational principle: "The AI did it is never a complete ethical or legal answer." Which of the following scenarios most precisely illustrates the professional accountability implication of this principle?

A. An AI agent autonomously sends a legally binding contract amendment to a client without human review. When the amendment contains an error that causes financial loss, the deploying organization bears accountability for the agent's action.

B. An AI model produces an incorrect medical diagnosis that a physician relies on without verification. The AI developer is solely responsible for the medical error.

C. An AI writing tool generates a plagiarized passage that a student submits as their own work. The AI provider is responsible for the academic integrity violation.

D. An AI agent recommends a suboptimal investment strategy. Because the recommendation was clearly labeled as AI-generated, the organization bears no liability.

??? success "Show answer and feedback"

    **Correct Answer: A**

    ✅ **A is correct.** This scenario precisely illustrates the accountability principle: an agent took an autonomous action with real-world legal and financial consequences, and the deploying organization — which chose to deploy an agent with permission to send binding documents without human review — bears accountability for the result. The agent is a tool; the design decision to give it that permission scope, without a human approval gate, is a decision made by humans who are accountable for its consequences. This directly instantiates the principle: "The agent is a tool; the designer, deployer, and operator bear the accountability."

    ❌ **B is incorrect** as the best illustration. Physician reliance on an AI diagnostic tool is a shared accountability situation: the AI developer bears responsibility for the accuracy and disclosed limitations of the tool; the physician bears professional responsibility for the clinical decision, which includes verifying AI recommendations. Describing the AI developer as "solely responsible" misrepresents the distributed accountability structure the course principle addresses.

    ❌ **C is incorrect.** The student who submits plagiarized work bears primary accountability for the academic integrity violation, regardless of how the text was generated. The AI provider may bear some responsibility for generating the content without appropriate safeguards, but the course principle most precisely applies to organizations deploying agents with action authority — not to AI tool providers whose tools are misused by users.

    ❌ **D is incorrect.** Labeling a recommendation as "AI-generated" reduces — but does not eliminate — organizational liability. Disclosure is a necessary component of explainability (Floridi et al.) and transparency, but it does not transfer full responsibility to the user. Organizations that deploy AI recommendation systems in financial contexts remain subject to fiduciary and regulatory obligations regardless of disclosure labels.

### Question 5

The NIST AI RMF identifies seven characteristics of trustworthy AI. A team is deploying an automated workflow that generates and sends personalized outreach emails to prospective clients. Which combination of trustworthy AI characteristics is most critical to address in this deployment, and why?

A. Reliable and Explainable — because the emails must be sent consistently without downtime and the system must be able to explain why each email was generated.

B. Accountable, Privacy-Enhanced, and Fair — because the system makes autonomous decisions about which individuals to contact (raising fairness concerns), handles personal contact data (raising privacy concerns), and takes real-world actions on behalf of the organization (requiring clear accountability for those communications).

C. Safe and Interpretable — because automated email sending could cause system crashes and the email content must be readable by recipients.

D. Secure and Reliable — because the email delivery infrastructure must be protected from unauthorized access and must operate without failure.

??? success "Show answer and feedback"

    **Correct Answer: B**

    ✅ **B is correct.** An automated outreach system raises a specific and interrelated set of trustworthy AI concerns. Fairness: if the system selects which individuals to contact based on ML-driven scoring, the selection algorithm may reflect demographic biases that systematically exclude or over-target specific populations. Privacy: the system processes personal contact information — in many jurisdictions this triggers GDPR, CCPA, or similar data protection obligations. Accountability: every email sent by the agent is an organizational communication — if the content is misleading, incorrect, or inappropriate, the organization is accountable for it, not the AI. These three characteristics are most directly implicated by this specific deployment profile.

    ❌ **A is incorrect** as the best answer. Reliability (uptime) and explainability are both relevant in any AI deployment, but they are not the most precisely critical characteristics for this scenario. Explainability in the NIST sense goes beyond being able to generate email content — it includes accounting for why specific recipients were selected and why specific messages were composed, which connects to the fairness and accountability concerns in option B.

    ❌ **C is incorrect.** "Safe" in the NIST AI RMF refers to preventing unintended harm to people, not to system crashes — though reliability concerns overlap. "Interpretable" in NIST refers to the ability to understand how a model arrived at its outputs, not simply to whether the email text is readable. More importantly, this pair does not address the most salient concerns raised by autonomous outreach: privacy and fairness.

    ❌ **D is incorrect** as the best answer. Security (protecting the system from unauthorized access) and reliability (consistent operation) are baseline infrastructure concerns for all deployed systems, not characteristics that are specifically elevated by the autonomous outreach use case. The characteristics that are specifically heightened by this application — personal data handling, autonomous contact decisions, organizational accountability for communications — are privacy, fairness, and accountability.

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1.2-Addendum){target=_blank} (wiki page last changed 2026-08-05). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-1/chapter-quizzes.md){target=_blank}.</p>
