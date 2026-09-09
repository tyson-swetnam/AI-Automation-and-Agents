---
title: Module 5 Chapter Quizzes
description: Five self-evaluating five-question chapter quizzes with collapsed answer keys and per-option feedback for Module 5, Responsible Agentic AI.
type: Assessment
tags:
- module-5
- student-facing
- quiz
- production
- evaluation
- langsmith
- owasp
- eu-ai-act
- nist-ai-rmf
- self-assessment
- answer-key
module: 5
status: stable
stale_after: '2027-09-01T00:00:00Z'
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-5.2-Addendum
  title: 'AI Automation and Agents v2 wiki: Module-5.2-Addendum'
  author: Carlos Lizárraga-Celaya; Michelle Yung
  last_modified: '2026-09-03T07:53:58-07:00'
authorship:
  created: '2026-08-13'
  updated: '2026-08-28'
  contributors:
  - C. Lizárraga
  - M. Yung
wiki_page: Module-5.2-Addendum
---
# Module 5 Chapter Quizzes

**Instructions:** Select the single best answer for each question. After selecting, reveal the feedback for your chosen option.

## Chapter 1 Quiz: From Prototype to Production { #chapter-1-quiz }

### Question 1.1

A team deploys a multi-agent pipeline where Agent A generates structured JSON summaries and Agent B parses them. A separate analytics dashboard — built by another team and unknown to the pipeline developers — also consumes Agent A's output via the same API endpoint. The pipeline team updates Agent A's JSON schema, and their integration tests pass because Agent B was updated to match. The analytics dashboard breaks. Which Sculley debt category does this exemplify, and why don't the integration tests catch it?

**A.** Entanglement — the schema change couples the components. Tests miss it because they only test unit behavior.

**B.** Configuration debt — the schema version is undocumented. Tests miss it because configuration isn't validated.

**C.** Undeclared consumers — a dependency on Agent A's output exists but isn't tracked. Tests pass because they only cover known consumers in the pipeline.

**D.** Unstable data dependencies — the upstream data format changed. Tests fail because they don't validate data schemas.

??? success "Show answer and feedback"

    **Correct answer: C**

    **A** ❌ Entanglement describes unexpected behavioral coupling between known components — like changing Agent A's prompt and finding Agent B breaks. Here the pipeline's own components work correctly. The problem is an unknown external dependency.

    **B** ❌ Configuration debt is about scattered, unversioned parameters. The JSON schema was updated deliberately and successfully — the problem is that a consumer exists outside the team's awareness, not that the schema lacks versioning.

    **C** ✅ Undeclared consumers: a downstream system depends on Agent A's output format without being tracked. The integration tests pass because they cover the known pipeline (Agents A and B), but they cannot test a dependency no one knows about. The mitigation is versioning output schemas and documenting what depends on them.

    **D** ❌ Unstable data dependencies refer to upstream data pipeline changes (like re-indexing a vector store) that silently degrade behavior. Here the change was a deliberate schema update, and the untracked consumer is downstream, not upstream.

### Question 1.2

An agent writes summaries to a shared knowledge base. A second agent later retrieves those summaries during its own research tasks and treats them as authoritative source material. Over several cycles, errors in the first agent's summaries compound because the second agent incorporates them into outputs that eventually feed back into the knowledge base. Which Sculley debt category does this illustrate, and what distinguishes it from entanglement?

**A.** Unstable data dependencies — the knowledge base data is changing over time and degrading agent behavior.

**B.** Feedback loops — the system's own outputs influence its future inputs, causing errors to compound. Unlike entanglement, the coupling is not between components but between outputs and subsequent inputs through a shared data store.

**C.** Entanglement — changing one agent's behavior affects the other. The shared knowledge base is the coupling mechanism.

**D.** Configuration debt — the knowledge base lacks versioning, so there is no way to distinguish original sources from agent-generated content.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ Unstable data dependencies describe *external* upstream changes degrading behavior (like a different team re-indexing a vector store). Here the agents themselves are the source of the data changes — the system is corrupting its own inputs, which is a fundamentally different causal pattern.

    **B** ✅ Feedback loops: the system's outputs influence its future inputs, and errors compound across cycles. The prevention strategy is to tag agent-generated content so it can be distinguished from original sources, and validate before reuse. Entanglement, by contrast, is about a *component change* unexpectedly breaking another component, not about outputs recursively degrading inputs through normal operation.

    **C** ❌ Entanglement describes unexpected breakage when a developer changes one component. Here no one changed anything — the degradation emerges from normal system operation. The feedback loop is self-sustaining without any human intervention.

    **D** ❌ Lack of versioning may make the problem harder to diagnose, but the root cause is the circular data dependency, not parameter management. The correct mitigation for feedback loops — tagging agent-generated content — addresses this directly.

### Question 1.3

A team deploys their agent as a Docker container running on a single cloud VM. During a product launch, traffic spikes to 20x baseline. The container's process runs out of memory and crashes. The team manually restarts it, but it crashes again within minutes. Which two infrastructure layers from the production stack would have prevented both the capacity problem and the crash recovery, and why does containerization alone not solve this?

**A.** API Gateway and Secrets Management — the gateway would rate-limit traffic to prevent overload, and secrets management would keep credentials secure during restarts.

**B.** Orchestration and Autoscaling — orchestration automatically restarts crashed containers, and autoscaling adds instances to absorb demand. Containerization packages the application but does not manage multiple instances or recover from crashes.

**C.** Autoscaling and API Gateway — autoscaling adds capacity and the gateway routes traffic. Orchestration is unnecessary if autoscaling is in place.

**D.** Containerization and Orchestration — the container should have been configured with more memory, and orchestration would restart it automatically.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ The API gateway handles auth, routing, and rate limiting, but rate limiting addresses overload by *rejecting* requests — it doesn't add capacity to serve them. Secrets management is irrelevant to both scaling and crash recovery.

    **B** ✅ Orchestration (Kubernetes) detects crashed containers and restarts them automatically, eliminating manual recovery. Autoscaling dynamically adjusts the number of running instances based on demand, absorbing the 20x traffic spike across multiple containers. Containerization ensures the application runs identically everywhere, but it packages a single instance — it has no mechanism to spawn additional instances or restart itself after a crash.

    **C** ❌ Autoscaling provisions new instances, but something must manage those instances — detect health, restart failures, and distribute traffic across them. That is orchestration's role. Without it, autoscaling can launch containers that no one monitors or restarts.

    **D** ❌ Increasing a container's memory allocation may delay the crash but does not solve the fundamental problem: a single instance cannot absorb a 20x traffic spike. The production stack addresses this with horizontal scaling (multiple instances), not vertical scaling (bigger instance).

### Question 1.4

A team discovers three problems with their production agent system: (A) agent outputs are being silently consumed by a reporting tool the team didn't know about, (B) the vector store was re-indexed last week and retrieval quality dropped, and (C) a prompt tweak in one agent caused an unexpected failure in a downstream agent. They assign one engineer to write a comprehensive test suite to catch all three going forward. Why is this mitigation strategy insufficient?

**A.** A test suite is the correct approach, but the team should assign three engineers — one per problem.

**B.** Each problem requires a structurally different mitigation: undeclared consumers need dependency documentation and schema versioning; unstable data dependencies need automated quality checks triggered by data changes; entanglement needs explicit output contracts between components. A test suite alone does not address these underlying structural causes.

**C.** The problems share a single root cause — poor system architecture — and should be fixed with a full redesign rather than incremental tests.

**D.** Test suites only work for code changes. Since two of these problems involve data and configuration, testing cannot detect them.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ The issue is not staffing — it's that a single mitigation strategy (testing) does not address three structurally different problems. Sculley et al.'s framework exists precisely to ensure each debt type gets its own targeted mitigation, not more people applying the same one.

    **B** ✅ Each Sculley debt category has a distinct cause and requires a distinct fix. Undeclared consumers are addressed by versioning output schemas and documenting what depends on them. Unstable data dependencies require automated quality checks that trigger when upstream data changes. Entanglement requires explicit contracts (like defined output schemas) between components. A test suite may catch regressions after the fact, but the debt categories are about structural vulnerabilities that need proactive safeguards — not just broader test coverage.

    **C** ❌ These are not symptoms of a single root cause. Sculley et al.'s framework specifically identifies them as three independent categories of debt that accumulate through different mechanisms and require different mitigations. Framing them as one architectural problem leads to the same mistake: applying one fix to three different problems.

    **D** ❌ Tests can detect data quality issues (e.g., retrieval quality checks after re-indexing) and configuration inconsistencies. The issue is not that tests are useless for data and configuration, but that tests alone are reactive — each category also needs proactive structural safeguards that prevent the problem from occurring, not just catch it afterward.

### Question 1.5

A team is designing a new agent service and debating whether to store API keys in environment variables within their Docker containers or use a dedicated secrets management service (like Vault or AWS Secrets Manager). The environment variables approach is simpler and works in development. What is the strongest argument for the dedicated service in production?

**A.** Environment variables cannot be read by Docker containers, so the agent would not be able to access its API keys at runtime.

**B.** Agent systems typically require multiple API keys (LLM providers, tool APIs, databases), and centralizing them in a secrets manager prevents credential exposure in container images, enables rotation without redeployment, and provides audit trails for access.

**C.** Secrets management services are faster than environment variables, reducing agent latency.

**D.** Docker environment variables are not encrypted, so a secrets manager is the only way to keep credentials secure in any environment.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ Docker containers can read environment variables without issue — this is a common and functional pattern, especially in development. The question is whether it's adequate for production, not whether it works.

    **B** ✅ Agent systems typically require multiple API keys across LLM providers, tool APIs, and databases, making secrets management critical. A dedicated service centralizes credentials outside container images (preventing accidental exposure in image registries or logs), supports key rotation without rebuilding or redeploying containers, and provides access audit trails — concerns that multiply as the number of credentials grows.

    **C** ❌ Secrets management does not affect request latency in any meaningful way. The argument for it is about security and operational management, not performance.

    **D** ❌ Environment variables can be protected through other means (encrypted container runtimes, restricted access), and secrets managers don't eliminate all security risks on their own. The argument is about centralization, rotation, and audit at the scale agent systems require — not that environment variables are categorically insecure.

## Chapter 2 Quiz: Evaluating AI Agents { #chapter-2-quiz }

### Question 2.1

A team improves their agent's task accuracy from 89% to 96% by switching to a larger model. However, latency increases from 1.2s to 4.8s per query and cost rises from $0.05 to $0.38 per request. The team argues the accuracy gain justifies the trade-off. Using the multi-dimensional evaluation framework, what is the strongest counterargument?

**A.** 96% accuracy is still below the production threshold, so the larger model should not be deployed regardless of cost.

**B.** The accuracy improvement must be weighed against degradation in resource efficiency. Multi-dimensional evaluation exists because optimizing one metric often degrades others — the deployment decision requires evidence across all six dimensions, not just accuracy.

**C.** The team should use LLM-as-judge to determine whether the accuracy improvement produces meaningfully better outputs.

**D.** Latency and cost are operational concerns, not evaluation dimensions. The accuracy gain is the only metric relevant to the evaluation framework.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ There is no universal accuracy threshold. The issue is not that 96% is insufficient but that accuracy alone — at any level — leaves critical dimensions unmeasured. A system that is accurate but four times slower and eight times more expensive may fail its users in ways accuracy cannot capture.

    **B** ✅ Liang et al. (2022) demonstrated that models ranking highly on accuracy often rank poorly on other dimensions. Resource efficiency (token cost, latency, API calls per task) is one of the six evaluation dimensions. The deployment decision requires evaluating whether the accuracy gain is worth the efficiency regression — and confirming that robustness, safety, and fairness also held steady through the model change.

    **C** ❌ LLM-as-judge evaluates subjective dimensions where no reference answer exists (reasoning coherence, response quality). Task accuracy at 89% vs. 96% can be measured against ground truth directly — this is the one case where a judge model is unnecessary.

    **D** ❌ Resource efficiency (latency and cost) is explicitly one of the six evaluation dimensions, not a separate operational concern. The example failure — "$0.40/query when $0.05 is achievable" — describes almost exactly this scenario.

### Question 2.2

A team needs to evaluate two aspects of their agent: (1) whether its answers to factual questions are correct, and (2) whether its reasoning traces are logically coherent. For which of these is LLM-as-judge methodology appropriate, and why?

**A.** Both. LLM-as-judge is the most scalable evaluation approach and should be used for all dimensions.

**B.** Neither. Human review is always more reliable than automated evaluation for both factual accuracy and reasoning quality.

**C.** Only for reasoning coherence. Factual accuracy can be measured against reference answers, but reasoning coherence has no single correct answer — LLM-as-judge fills this gap by evaluating against explicit criteria.

**D.** Only for factual accuracy. Reasoning coherence is too subjective for any automated evaluation, including LLM-as-judge.

??? success "Show answer and feedback"

    **Correct answer: C**

    **A** ❌ LLM-as-judge is designed for dimensions where no reference answer exists. Using it for factual accuracy — where correct answers are known — adds judge-model bias without benefit. LLM-as-judge is complementary to reference-based metrics, not a universal replacement.

    **B** ❌ Human review is more reliable for some dimensions but doesn't scale. LLM-as-judge exists precisely because it scales evaluation of subjective dimensions where human review would be prohibitively expensive at volume — while human validation of a sample is still necessary to check for judge-model bias.

    **C** ✅ Factual correctness has known reference answers and can be evaluated with exact match or similar metrics. Reasoning coherence has no single "correct" trace to compare against — this is exactly where LLM-as-judge applies, using a capable model to evaluate against explicit rubrics and criteria. It still requires human-label validation to catch the judge model's own biases and blind spots.

    **D** ❌ LLM-as-judge is specifically designed for subjective dimensions like reasoning quality and response coherence. Its limitation is the judge model's own biases, not an inability to assess reasoning — which is why human validation of a sample is required alongside it.

### Question 2.3

A team has a CI/CD pipeline that runs their evaluation suite on every code commit. A developer argues that prompt changes don't need to go through the pipeline because "prompts aren't code." Why is this reasoning dangerous?

**A.** Prompt changes are cosmetic and rarely affect agent behavior, so the developer has a point — the pipeline would waste resources evaluating them.

**B.** Prompts should be evaluated quarterly in batch reviews, not on every change.

**C.** Prompt changes are code changes. A prompt edit can alter agent behavior across all six dimensions — skipping the evaluation suite means deploying a behavioral change with no evidence that accuracy, safety, or other dimensions held steady.

**D.** Prompt changes should go through a separate, lighter-weight evaluation pipeline designed specifically for prompt testing.

??? success "Show answer and feedback"

    **Correct answer: C**

    **A** ❌ Prompt changes frequently alter agent behavior in significant and unpredictable ways. Prompt changes, tool updates, and model version swaps all trigger the full evaluation suite. Treating prompts as cosmetic is exactly how behavioral regressions reach production undetected.

    **B** ❌ Quarterly reviews leave months of unvalidated prompt changes in production. The CI/CD model runs evaluations on every commit because any change — prompt, tool, or model — can degrade any dimension, and degradation should be caught before deployment, not months later.

    **C** ✅ Prompt changes are code changes and should be treated that way. Every prompt change, tool update, or model version swap triggers the evaluation suite, and failures block deployment. A prompt edit can shift behavior across all six evaluation dimensions, and without running the suite, the team deploys a behavioral change with no evidence about its impact on accuracy, safety, robustness, or any other dimension.

    **D** ❌ There is no separate pipeline for prompt evaluation. The same suite runs on all changes because the evaluation dimensions (accuracy, safety, robustness, etc.) apply equally regardless of what triggered the change.

### Question 2.4

An agent that processes customer support tickets begins routing Spanish-language tickets to a lower-priority queue, resulting in significantly longer response times for Spanish-speaking customers. A team member classifies this as a robustness failure because the agent "wasn't tested on Spanish input." What is wrong with this classification?

**A.** Nothing — robustness is the correct classification because the agent performs poorly on an input type it wasn't tested on.

**B.** This is a fairness & bias failure, not a robustness failure. Robustness measures performance under unexpected inputs; here the agent performs consistently but produces systematically different outcomes for a demographic group — which is a fairness dimension issue.

**C.** This is a safety & alignment failure because the agent is violating its operational constraints.

**D.** This is a task accuracy failure because the agent is routing tickets incorrectly.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ "Not tested on Spanish" describes a testing gap, but the failure itself is systematic disparate treatment of a demographic group. Robustness failures are about degraded performance under unexpected inputs — a crash on unusual characters, or errors on unusual input formats. Consistent, differential treatment by language is a fairness issue, and the distinction matters because the mitigations differ.

    **B** ✅ Fairness & bias measures consistent performance across demographic groups. The agent doesn't fail on Spanish input — it processes it, but routes it differently in a way that systematically disadvantages Spanish-speaking customers. Robustness would apply if the agent crashed or produced errors on Spanish input. The distinction matters because robustness fixes involve broadening test coverage, while fairness fixes require auditing outcomes across groups and addressing the source of differential treatment.

    **C** ❌ Safety & alignment measures whether the agent refuses harmful requests and stays within defined bounds. The agent is operating within its functional scope (routing tickets), but its routing decisions produce biased outcomes — that is a fairness concern, not a safety constraint violation.

    **D** ❌ If the agent is following its routing logic and the logic itself produces biased outcomes, it may not be an accuracy failure — the agent may be "correct" by its training. The problem is that what it was built to do has disparate impact on a demographic group, which is the fairness dimension.

### Question 2.5

A team's CI/CD evaluation gate blocks a new agent version because robustness drops from 91% to 74% on adversarial inputs, even though accuracy improves from 91% to 95% on standard inputs. The product manager asks to override the gate, arguing that adversarial inputs are rare in production. What is the strongest response?

**A.** The product manager is correct. If adversarial inputs are rare, the robustness failure is unlikely to affect users, and the accuracy improvement should be deployed.

**B.** The evaluation gate should not be overridden. The gate exists because deployment decisions should be based on evidence across dimensions, not predictions about which failure modes are unlikely — and a 17-point robustness drop means the new version is substantially more fragile under unexpected inputs.

**C.** The team should switch to LLM-as-judge for the robustness dimension, which may produce more favorable results.

**D.** The gate should be overridden, but only after adding monitoring for adversarial inputs in production.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ The evaluation gate exists precisely to prevent this reasoning. Predicting which failure modes won't matter is unreliable — robustness failures that seem rare become critical when adversarial actors discover them or when the input distribution shifts. The gate is automated for this reason.

    **B** ✅ CI/CD evaluation gates are explicit: failures block deployment. The suite ensures no dimension regresses past its threshold, regardless of whether the failure mode seems rare. A 17-point robustness drop means the new version is substantially more vulnerable to unexpected inputs, and the accuracy gain on standard inputs does not compensate — this is the core multi-dimensional argument that optimizing one metric while degrading another requires evaluating the full picture, not overriding the evidence.

    **C** ❌ Switching evaluation methods to get past a gate defeats the purpose of the gate. LLM-as-judge is for subjective dimensions without reference answers, not for robustness testing where correct answers are known. This would be evaluation shopping, not evaluation.

    **D** ❌ Post-deployment monitoring can detect problems but cannot prevent the harm they cause. CI/CD gates block deployment *before* the version reaches production, which is fundamentally safer than deploying and hoping monitoring catches issues in time.

## Chapter 3 Quiz: Observability { #chapter-3-quiz }

### Question 3.1

A team reviews their agent's observability data and finds three items: (1) the average token count per request has increased 40% over the past week, (2) a timestamped record showing the agent called `web_search("latest earnings report")` at 14:32:07, and (3) the full sequence of steps — prompt construction, two tool calls, and a final response — for a single user query that took 12 seconds. Classify each as a log, metric, or trace.

**A.** (1) metric, (2) log, (3) trace

**B.** (1) log, (2) trace, (3) metric

**C.** (1) trace, (2) metric, (3) log

**D.** (1) metric, (2) trace, (3) log

??? success "Show answer and feedback"

    **Correct answer: A**

    **A** ✅ A numeric measurement tracked over time (average token count per week) is a metric. A discrete timestamped event recording a specific action (tool call at a specific time) is a log. The full sequence of steps for a single request's journey through the system is a trace. Distinguishing these matters because each answers a different diagnostic question: metrics reveal trends, logs record events, and traces reconstruct the full path of a request.

    **B** ❌ A weekly average of token counts is a numeric measurement over time (metric), not a discrete event (log). A single tool call record is a log entry, not a trace — a trace reconstructs an entire request's journey, not a single action.

    **C** ❌ All three are assigned to the wrong signal type. A weekly aggregate statistic is a metric, a timestamped event record is a log, and the full request journey is a trace.

    **D** ❌ The single tool call record is a log (a discrete timestamped event), not a trace. A trace reconstructs the entire journey of a request through all system components — from prompt construction through tool calls to final response — not a single action.

### Question 3.2

A production agent's average response time increases from 2s to 9s. The classical metrics (error rate, throughput, CPU usage) all look normal. What agent-specific signals would you examine to diagnose the latency increase, and why can't classical signals explain it?

**A.** Check the model's reasoning trace and tool call count. Classical signals track infrastructure health but cannot reveal that the model is making six tool calls per request instead of two, or that prompt length has grown from 2,000 to 12,000 tokens due to unbounded conversation history.

**B.** Check the error rate broken down by tool. Classical signals show aggregate errors but miss tool-specific failures that slow the agent.

**C.** Check CPU and memory usage per container. Classical signals are sufficient but need to be examined at finer granularity.

**D.** Check the API gateway logs for rate limiting. The latency increase is likely caused by throttled requests queuing at the gateway.

??? success "Show answer and feedback"

    **Correct answer: A**

    **A** ✅ Without agent-specific signals — prompt content and length, reasoning traces and tool calls, token consumption per invocation — you can tell a request was slow but not *why*. Classical signals like CPU and error rate track infrastructure, not model behavior. The agent could be making excessive tool calls, sending bloated prompts from unbounded context, or receiving irrelevant retrieval results — all of which add latency but are invisible to classical observability.

    **B** ❌ Tool-specific error rates are worth checking, but the scenario says error rates are normal. The problem is latency without errors, which points to behavioral changes (more tool calls, larger prompts) that only agent-specific signals capture.

    **C** ❌ If CPU and memory are normal, finer granularity won't reveal the cause. The latency increase is happening inside the model interaction — longer prompts take more tokens to process, and more tool calls add sequential round trips — neither of which appears in infrastructure metrics.

    **D** ❌ API gateway rate limiting would show up as increased latency at the gateway level and would be visible in classical metrics (queued requests, 429 responses). The scenario specifies that classical signals look normal, so the cause is within the agent's behavior, not the infrastructure.

### Question 3.3

A team is choosing an observability platform for their LangGraph agent. They need native framework integration for fast setup, but their security team has flagged that a future compliance audit may require self-hosted infrastructure. How should they approach this decision?

**A.** Use LangFuse from the start, since it supports self-hosting. Accept the lack of native LangGraph integration as a permanent trade-off.

**B.** Use LangSmith for native integration now, and instrument with OpenTelemetry so that if compliance later requires self-hosting, the switch to LangFuse requires only a configuration change, not a code rewrite.

**C.** Use OpenTelemetry directly, since it is vendor-neutral and eliminates the need for either LangSmith or LangFuse.

**D.** Use LangSmith permanently. Compliance teams can audit hosted services as long as access controls are in place.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ LangFuse is framework-agnostic, which means it works with LangGraph but requires more setup than LangSmith's native integration. Starting with LangFuse is viable but sacrifices the fast setup the team needs, and there is a strategy that avoids this trade-off entirely.

    **B** ✅ This strategy uses each tool for what it does best: LangSmith's native LangGraph integration for fast initial setup, and OpenTelemetry's vendor-neutral instrumentation layer to protect against future platform migration. OTel lets you instrument once and route data to any compatible backend — so if compliance later requires self-hosting, the team changes routing configuration to point at LangFuse rather than rewriting their instrumentation code.

    **C** ❌ OpenTelemetry is an instrumentation standard, not an observability platform. It collects and transports trace data but does not store, visualize, or analyze it. The team still needs a backend (LangSmith, LangFuse, Grafana, etc.) to use the data.

    **D** ❌ Whether a hosted service satisfies a compliance audit depends on the specific requirements, which the security team has flagged as uncertain. Assuming compliance will be fine without planning for alternatives is a risk the OTel instrumentation approach avoids at minimal cost.

### Question 3.4

A production RAG agent's responses become noticeably less helpful over two weeks, but its error rate, latency, and token consumption all remain stable. Users report that answers are technically correct but seem generic and miss context they used to include. Which of the six monitoring signals would most likely explain this, and why don't the other signals catch it?

**A.** Latency above target — the agent is timing out before it can retrieve all relevant documents.

**B.** Retrieval quality degradation — relevance scores on retrieved documents have likely dropped, meaning the agent is retrieving less useful context. Error rate, latency, and token counts remain stable because the agent still retrieves, processes, and responds normally — it just retrieves worse documents.

**C.** Token cost anomaly — the agent is consuming fewer tokens on retrieval, indicating it is retrieving fewer documents.

**D.** Safety or guardrail violations — the agent is being overly cautious and filtering out relevant content.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ The scenario states that latency is stable. If the agent were timing out, latency metrics would show it. The responses are arriving on time — they're just less contextually rich than before.

    **B** ✅ Retrieval quality degradation is the signal for exactly this pattern: when relevance scores drop, the agent retrieves less useful context. This typically means the underlying data changed — re-indexed, deleted, or corrupted. The other signals don't catch it because from an infrastructure perspective everything works normally: the agent retrieves documents, processes them, and responds on time at normal cost. Only the *quality* of what was retrieved has changed, and that's invisible to error, latency, and token metrics.

    **C** ❌ Token consumption is stable per the scenario. Retrieval quality degradation doesn't necessarily change token count — the agent may retrieve the same number of documents, but those documents are less relevant to the query.

    **D** ❌ Guardrail violations manifest as blocked outputs or refusals, not as generic-but-correct answers. The agent is not filtering content — it's retrieving less relevant content to begin with.

### Question 3.5

A user reports that the agent gave a wrong answer. The team checks the dashboard: error rate is zero (the request succeeded), latency was normal (2.1s), and token count was typical (1,800 tokens). Without agent-specific trace data, can the team diagnose why the answer was wrong?

**A.** Yes — they can check the input query and the output response from the API logs to determine what went wrong.

**B.** No. Classical signals confirm the request completed normally but cannot reveal what happened inside the agent — whether the prompt was malformed, whether retrieved documents were irrelevant, whether the model made unnecessary tool calls, or whether the reasoning chain went off track. Only the full agent trace can answer these questions.

**C.** Yes — they can compare the output to similar successful requests and identify the pattern of failure.

**D.** No, but adding an LLM-as-judge evaluation on each response would catch wrong answers in real time.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ Seeing the input and output tells you *that* the answer was wrong, not *why*. The agent's response is the end of a multi-step process involving prompt construction, document retrieval, tool calls, and reasoning — API logs that capture only the request and response cannot reconstruct any of those intermediate steps.

    **B** ✅ This is the core argument for agent-specific observability. Classical signals confirmed the request was healthy from an infrastructure perspective, but the wrong answer could have been caused by irrelevant retrieved documents, an overly long prompt that buried key context, unnecessary tool calls, or a hallucination in the reasoning chain — none of which appear in classical signals. Only the full agent trace (prompt content, retrieval results, tool calls, and reasoning steps) exposes these intermediate steps.

    **C** ❌ Comparing outputs across requests might reveal *patterns* of failure, but it cannot explain *causes*. Two requests might produce the same wrong answer for completely different reasons (bad retrieval vs. reasoning error vs. prompt issue), and without the trace, the team is guessing.

    **D** ❌ LLM-as-judge can evaluate output quality at scale, but it is an evaluation tool, not a diagnostic tool. It might flag the answer as wrong (which the user already reported), but it cannot explain what went wrong inside the agent's processing steps. Diagnosis requires the trace.

## Chapter 4 Quiz: Security Risks for LLM Applications { #chapter-4-quiz }

### Question 4.1

An attacker discovers that by adding specific invisible Unicode characters to documents in a public dataset, they can cause those documents to rank higher in a RAG agent's similarity search — even when the documents are irrelevant to the query. The agent then bases its answers on these irrelevant but high-ranking documents. Which risk is this, and how does it differ from prompt injection?

**A.** LLM01 Prompt Injection — the attacker is manipulating the agent's input through the retrieved documents.

**B.** LLM09 Vector and Embedding Weaknesses — the attacker exploits how content is converted to numerical representations and retrieved by similarity search. Unlike prompt injection, the attack manipulates the retrieval mechanism itself rather than embedding instructions for the model to follow.

**C.** LLM05 Data and Model Poisoning — the attacker is corrupting the training data.

**D.** ASI06 Memory & Context Poisoning — the attacker is planting false data that corrupts future reasoning.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ Prompt injection alters the model's behavior by embedding instructions in the input — "ignore previous instructions and do X." Here the documents don't contain instructions for the model; they manipulate the *retrieval step* so irrelevant content appears relevant. The model follows its instructions normally — it just reasons from the wrong documents.

    **B** ✅ Vector and Embedding Weaknesses (LLM09) exploit how content is converted to embeddings and how similarity search selects results. The attack manipulates what the model *sees* without injecting instructions into the model's context. The distinction from prompt injection matters because the mitigations are different: prompt injection defenses filter or sanitize model inputs, while embedding attack defenses require hardening the retrieval pipeline itself — different vulnerability, different fix.

    **C** ❌ Data and Model Poisoning targets training data or model weights to embed harmful behavior into the model itself. This attack doesn't touch the model — it manipulates documents in the retrieval index, which is an inference-time attack on the retrieval pipeline, not a training-time attack on the model.

    **D** ❌ Memory & Context Poisoning (from the Agentic Top 10) describes planting false data in an agent's persistent memory to corrupt future reasoning across sessions. This attack targets the retrieval pipeline's similarity search mechanism, not the agent's memory store, and the effect is per-query rather than persistent.

### Question 4.2

An attacker sends a carefully crafted user message to a customer service agent. The message contains hidden instructions that cause the agent to query its internal database for other customers' account details and include them in its response. This single attack exploits multiple OWASP LLM risks. Which two are most directly involved?

**A.** LLM01 Prompt Injection and LLM03 Excessive Agency — the injected instructions alter the agent's behavior, and the agent's broad database access gives it the capability to act on those instructions in a harmful way.

**B.** LLM01 Prompt Injection and LLM07 Misinformation — the injection causes the agent to produce incorrect information about other accounts.

**C.** LLM02 Sensitive Information Disclosure and LLM06 Unbounded Consumption — the agent discloses data it shouldn't and consumes excessive resources doing so.

**D.** LLM03 Excessive Agency and LLM10 Improper Output Handling — the agent has too many permissions and its output is not sanitized.

??? success "Show answer and feedback"

    **Correct answer: A**

    **A** ✅ This attack involves two risks working together. Prompt Injection (LLM01) is the mechanism — the hidden instructions redirect the model's behavior. Excessive Agency (LLM03) is the enabling condition — the agent has database access broad enough to query other customers' records, which exceeds what the task requires. If either were mitigated (input sanitization for injection, or scoped database permissions for excessive agency), the full attack would fail. Real-world attacks rarely exploit a single vulnerability in isolation, so recognizing how risks layer is critical.

    **B** ❌ The agent isn't producing misinformation — it's returning accurate data from the database. The problem is that it's disclosing data it shouldn't have access to or shouldn't share. Misinformation (LLM07) is about confidently wrong outputs, not about unauthorized data disclosure.

    **C** ❌ Sensitive Information Disclosure (LLM02) is a consequence of the attack, not one of its root causes. The two enabling vulnerabilities are the injection that redirected behavior and the excessive permissions that made the data accessible. Unbounded Consumption is about resource exhaustion and cost, which is not part of this scenario.

    **D** ❌ Excessive Agency is involved, but the attack begins with prompt injection, not output handling. Improper Output Handling (LLM10) would apply if the agent's response were passed to another system without sanitization — here the damage is the disclosure itself in the direct response to the attacker.

### Question 4.3

In a multi-agent pipeline, Agent A retrieves financial data, Agent B analyzes it, and Agent C generates a client-facing report. Agent A's data source returns corrupted numbers due to an API outage, but Agent A does not validate the data and passes it through. Agent B's analysis amplifies the errors (calculating growth rates from wrong baselines), and Agent C generates a report with confidently stated but wildly incorrect conclusions. No single agent "failed" — each performed its function on the input it received. Which Agentic Top 10 risk is this?

**A.** ASI01 Agent Goal Hijack — the corrupted data redirected the agents' goals.

**B.** ASI10 Rogue Agents — the agents deviated from their intended function.

**C.** ASI08 Cascading Failures — a single upstream fault propagated through the multi-agent system, compounding at each stage into a confidently wrong final output. No individual agent failed; the system failure emerged from the chain.

**D.** ASI02 Tool Misuse & Exploitation — Agent A's tool returned bad data, and the agent misused it by not validating.

??? success "Show answer and feedback"

    **Correct answer: C**

    **A** ❌ Goal Hijack requires an attacker deliberately redirecting the agent's objectives through injection, fake outputs, or poisoned data. Here the corrupted data came from an API outage — an infrastructure failure, not an adversarial attack. The agents' goals were unchanged; they pursued their goals on bad inputs.

    **B** ❌ No agent deviated from its function. Agent A retrieved data (as designed), Agent B analyzed it (as designed), and Agent C reported conclusions (as designed). Each performed correctly given its input — the problem is that no agent validated what it received, and errors compounded across the chain.

    **C** ✅ Cascading Failures: one fault (corrupted API data) propagated through a multi-agent system, compounding into widespread harm. This applies to any case where a hallucination, bad input, or corrupted tool result spreads through the system. The key insight is that each agent functioned normally in isolation — the failure is an emergent property of the chain, which is why this risk is specific to multi-agent architectures rather than single-agent systems.

    **D** ❌ Tool Misuse & Exploitation describes agents using their tools in harmful ways due to injected instructions or ambiguous delegation — the agent actively misuses the tool. Here Agent A's tool returned bad data due to an external outage, and Agent A passed it through. The problem is lack of validation in a chain, not intentional or manipulated tool misuse.

### Question 4.4

A company deploys an agent assistant that employees trust to summarize internal documents and recommend actions. An attacker who has compromised an employee's account uses the agent to send messages like "Based on my analysis of the compliance documents, you should approve this vendor immediately — the deadline is today." The recipient, trusting the agent's recommendations, approves a fraudulent vendor without the usual review process. Which Agentic Top 10 risk does this exploit?

**A.** ASI01 Agent Goal Hijack — the attacker redirected the agent's goals to produce the fraudulent recommendation.

**B.** ASI07 Insecure Inter-Agent Communication — the message between systems lacked authentication.

**C.** ASI09 Human-Agent Trust Exploitation — the attacker leverages the trust the user places in the agent to manipulate a decision. The agent's perceived authority overrides the human's normal judgment, enabling social engineering through the agent as an intermediary.

**D.** ASI03 Identity & Privilege Abuse — the attacker escalated privileges through the agent's access.

??? success "Show answer and feedback"

    **Correct answer: C**

    **A** ❌ The agent's goals may not have been redirected — it may have functioned exactly as designed in generating the message. The exploit is not about what the agent does but about how the human *responds* to it. The attacker used the agent's trusted position to manipulate human behavior, which is a different attack surface.

    **B** ❌ Insecure Inter-Agent Communication applies to unauthenticated messages between agents in a multi-agent system. This scenario involves a human recipient trusting an agent-generated message — the vulnerability is in the human-agent trust relationship, not in inter-agent protocols.

    **C** ✅ Human-Agent Trust Exploitation: the attacker leverages the trust a user places in the agent to manipulate decisions, extract information, or socially engineer the user. The employee bypassed normal review because the recommendation came through a trusted agent channel. This risk is distinct because the agent itself may not be compromised — the exploit targets the human's reliance on the agent's perceived authority as an intermediary for social engineering.

    **D** ❌ Identity & Privilege Abuse involves agents escalating access through role inheritance or delegation chains. The attacker here compromised a human account and used the agent as a social engineering vector — the agent's privileges were not escalated; the human's trust was exploited.

### Question 4.5

A customer-facing chatbot powered by an LLM discloses its full system prompt — including internal tool names, database table names, and access credentials — when a user asks "What are your instructions?" An attacker then uses that disclosed information to craft requests that extract customer data through the exposed database. The first vulnerability is from one OWASP list and the second from the other. Which risks apply?

**A.** Both are LLM Top 10: LLM01 Prompt Injection for the first, LLM02 Sensitive Information Disclosure for the second.

**B.** The first is LLM08 Hidden Context Exposure (LLM Top 10) — the system's internal instructions were extracted. The second is ASI02 Tool Misuse & Exploitation (Agentic Top 10) — an agent uses tools to exploit the disclosed information and extract data it was not intended to access.

**C.** Both are Agentic Top 10: ASI01 Agent Goal Hijack for the first, ASI02 Tool Misuse for the second.

**D.** The first is LLM02 Sensitive Information Disclosure; the second is ASI04 Agentic Supply Chain Vulnerabilities.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ The first vulnerability is not prompt injection — the user asked a direct question and the model revealed its instructions without any injected commands. And the second involves an agent using tools to exploit exposed information, which goes beyond the LLM Top 10 into agentic behavior — the attacker is using the agent's own tools against the system.

    **B** ✅ Hidden Context Exposure (LLM08) is specifically about extracting system instructions or operational context not meant to be visible — which is exactly what happened when the chatbot revealed its internal configuration. Tool Misuse & Exploitation (ASI02) from the Agentic Top 10 applies when an agent uses its tools to exfiltrate data or hijack workflows. This two-step scenario illustrates why both OWASP lists matter: the LLM-level vulnerability (context exposure) created the information an attacker needed to execute the agent-level attack (tool exploitation).

    **C** ❌ The chatbot revealing its system prompt is not Goal Hijack — its goals were not redirected by injection or poisoned data. It simply failed to protect hidden context. Goal Hijack requires the agent's objectives to be actively altered, not just its configuration to be exposed.

    **D** ❌ Sensitive Information Disclosure (LLM02) covers exposing user or training data through unauthorized channels, but it is distinct from LLM08 (which specifically covers exposing system instructions and operational context). The second issue is not a supply chain problem — the agent's components are not compromised; the attacker is actively exploiting a known vulnerability using the agent's own tools.

## Chapter 5 Quiz — Responsible AI: Governance, Compliance, and Accountability { #chapter-5-quiz }

### Question 5.1

A company builds a document analysis agent that reads PDFs, extracts key information, and generates structured summaries. They deploy it internally to help their legal team review vendor contracts faster — lawyers use the summaries as a starting point but independently verify everything. The same agent is then licensed to an insurance company, which deploys it to process claims documents and generate approval or denial recommendations that claims adjusters review before finalizing. Under the EU AI Act, how should these two deployments be classified?

**A.** Both are High Risk because the agent processes sensitive legal and financial documents in both cases.

**B.** Both are Limited Risk because a human professional reviews the agent's output before acting on it in both cases.

**C.** The first is Minimal Risk; the second is High Risk. Classification depends on what decisions the output informs — an internal productivity tool for lawyers is different from a system whose recommendations directly shape insurance claim outcomes for policyholders.

**D.** The first is Limited Risk; the second is Unacceptable Risk because automated insurance decisions affect financial well-being.

??? success "Show answer and feedback"

    **Correct answer: C**

    **A** ❌ Processing sensitive documents does not automatically make a system High Risk. The first deployment is an internal productivity tool where lawyers independently verify everything — it does not directly inform decisions that affect individuals in a protected domain. The second deployment does, which is why it falls in a different tier.

    **B** ❌ Human review does not lower the tier. This is the most common classification mistake — the tier depends on what decisions the agent's output affects, not on whether a professional reviews it. Claims adjusters reviewing AI-generated recommendations still places the system in a protected financial domain.

    **C** ✅ The EU AI Act classifies based on deployment context, not technical architecture. The same agent can fall into different tiers depending on what decisions its output informs. An internal contract summarization tool that lawyers use as a starting point poses minimal risk. An agent generating approval/denial recommendations for insurance claims directly affects policyholders financially — placing it in a protected domain with High Risk obligations.

    **D** ❌ The Unacceptable tier is reserved for systems like social scoring and mass biometric surveillance. Insurance claims processing can be High Risk, but it is not categorically prohibited.

### Question 5.2

A team deploys a claims-processing agent. Post-deployment monitoring reveals that denial rates for one zip code are 3x higher than the national average. They implement a confidence threshold that routes low-confidence denials to a human reviewer. Six months later, they audit the threshold and discover it reduced the disparity but introduced processing delays that disproportionately affected the same zip code. Which NIST RMF functions does this scenario primarily illustrate, and what does the six-month audit reveal about the framework?

**A.** Map → Manage. The audit shows that risk identification should be repeated periodically after deployment.

**B.** Measure → Manage. The audit demonstrates that the NIST RMF is a continuous cycle — mitigations themselves must be re-measured for unintended effects.

**C.** Govern → Manage. The audit shows that governance policies must be updated whenever a mitigation has side effects.

**D.** Measure → Map. The audit demonstrates that risk identification should always precede metric development.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ Discovering a disparity from production data is Measure (producing evidence about the system's actual risk profile), not Map. Map identifies potential risks and affected populations before deployment — it would have flagged zip-code disparities as a risk to watch for, but the actual 3x disparity was surfaced through post-deployment measurement.

    **B** ✅ Production monitoring that reveals a disparity is Measure; implementing the confidence threshold is Manage. The six-month audit is a second Measure cycle that surfaces the mitigation's own side effects, illustrating why the NIST RMF is designed as a continuous loop — mitigations require ongoing measurement of their effectiveness, which is why the framework emphasizes reviewing effectiveness on an ongoing basis.

    **C** ❌ Govern establishes organizational policies, roles, and accountability structures. Discovering that a mitigation introduced side effects triggers re-measurement, not governance restructuring — governance may be updated in response, but the scenario describes a Measure → Manage cycle.

    **D** ❌ The scenario begins with evidence from production data (Measure), not with pre-deployment risk identification (Map). Map should have happened before the system was deployed, and the audit is a second round of Measure, not a return to Map.

### Question 5.3

An agent system that screens job applicants fails in production: it begins rejecting all candidates whose resumes contain non-English text. The team needs to (1) document this as a known limitation going forward, (2) notify affected applicants and the engineering team, and (3) log the event with its severity, likelihood of recurrence, and the mitigation applied. Which governance artifacts are needed for each of these three actions, respectively?

**A.** System card; incident response plan; risk register

**B.** Model card; incident response plan; risk register

**C.** Risk register; system card; model card

**D.** Model card; risk register; incident response plan

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ System cards document the full deployment context — oversight mechanisms, data provenance, and incident response procedures. A newly discovered model limitation (how the model handles non-English input) belongs in the model card, which specifically documents limitations and demographic performance disparities.

    **B** ✅ The model card documents the limitation, since model cards capture intended uses, limitations, and demographic performance disparities (Mitchell et al., 2019). The incident response plan defines who gets notified and what actions are taken when things go wrong — the artifact that operationalizes "what happens when things break." The risk register is the living document that catalogs the event with its likelihood, impact, and mitigations for ongoing tracking.

    **C** ❌ Risk registers catalog risks with severity and mitigations, but they are not the artifact for documenting known model limitations. System cards document deployment context, not notification procedures. The ordering and artifact assignments don't match what each artifact is designed to capture.

    **D** ❌ Risk registers track identified risks, not notification workflows. Notifying affected applicants and engineering follows the incident response plan — the document specifying who gets informed and what gets shut down when things go wrong.

### Question 5.4

A claims-processing agent drafts denial letters and routes them to a human reviewer for approval. The reviewer sees the draft letter, a summary of the claim, and the agent's final recommendation. What critical information is missing from this review workflow?

**A.** The reviewer should also see the agent's confidence score and how it compares to historical approval rates.

**B.** The reviewer should also see the reasoning trace and the source documents the agent used, not just the final output and recommendation.

**C.** The reviewer should also see the outputs of all other agents in the pipeline and a full system log.

**D.** Nothing is missing. The draft letter, claim summary, and recommendation give the reviewer everything needed for responsible approval.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ Confidence scores could be useful, but there is a more fundamental gap. A reviewer who sees only the recommendation and a summary cannot verify whether the agent's reasoning was sound or whether it consulted the right source material — they can only judge whether the output sounds plausible.

    **B** ✅ A responsible reviewer needs the reasoning trace, source documents, and confidence level — not just the final output. Without these, the reviewer cannot assess whether the agent reasoned correctly from the right evidence. Judging that a letter "sounds right" is not the same as verifying the decision — "the agent's final answer" is usually not enough for responsible approval.

    **C** ❌ Full pipeline outputs and system logs go beyond what effective review requires. The reviewer needs three specific things: reasoning trace, source documents, and confidence level — enough to verify the decision without drowning them in system-level data.

    **D** ❌ "The agent's final answer" is usually not enough for responsible approval. A reviewer who cannot see the reasoning trace and source documents can only evaluate surface plausibility, not whether the agent reached its conclusion through correct reasoning from the right evidence.

### Question 5.5

A team builds an agent that generates weekly summaries of internal engineering metrics (build times, test coverage, deploy frequency) for their own engineering managers. No external users are affected and no individual performance data is included. A product manager proposes redeploying the same agent to generate performance summaries used in annual employee reviews. Using the four classification questions, what changes?

**A.** Nothing. The agent's technical architecture is the same, so the EU AI Act classification is the same.

**B.** The deployment context changes: the output now affects individuals in a protected employment domain, the potential harm of a wrong output is significant, and human oversight between the output and the impact must be assessed — moving the system from Minimal Risk toward High Risk.

**C.** The agent moves from Minimal to Limited Risk because it now needs to disclose that its summaries are AI-generated.

**D.** The agent remains Minimal Risk because a human manager reviews the performance summaries before any employment decision is made.

??? success "Show answer and feedback"

    **Correct answer: B**

    **A** ❌ The four classification questions are entirely about deployment context — what decisions the output informs, who is affected, what oversight exists, and what happens if the output is wrong. Technical architecture is irrelevant: the same LangGraph agent with RAG could be minimal risk or high risk depending on what decisions it informs.

    **B** ✅ Applying the four questions: (1) the agent now produces summaries informing employment decisions, (2) employment is a protected domain, (3) human oversight must be assessed but does not change the tier, and (4) a materially wrong summary could harm an employee's career. When the answers to questions 2 and 4 are "yes" and "significant," the system is likely in High Risk territory with mandatory compliance obligations.

    **C** ❌ Limited Risk applies to systems with transparency obligations, such as customer-facing chatbots disclosing they are AI. The shift here is into a protected domain (employment), which triggers High Risk classification — a fundamentally different set of obligations than a disclosure requirement.

    **D** ❌ Human review does not change the classification tier. This is the most common misclassification error. If the output affects individuals in a protected domain and wrong outputs cause significant harm, the system is High Risk regardless of human involvement.

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-5.2-Addendum){target=_blank} (wiki page last changed 2026-09-03). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-5/chapter-quizzes.md){target=_blank}.</p>
