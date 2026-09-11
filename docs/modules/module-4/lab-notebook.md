---
title: "Module 4 Lab: Three-Role Pipeline in LangGraph and CrewAI"
description: "Read-only rendering of the Module 4 lab notebook, Three-Role Pipeline in LangGraph and CrewAI, with links to open it in Google Colab or download the .ipynb file."
type: Lab
tags:
  - module-4
  - student-facing
  - lab
  - colab
  - langchain
  - langgraph
  - crewai
  - ollama
module: 4
time_estimate: "about 4 hours (guided lab, sections 1–2: about 2 hours; hands-on project, sections 3–4: about 2 hours)"
status: stable
stale_after: "2027-09-08T00:00:00Z"
generated:
  by: "process:nbconvert"
  at: "2026-09-08T00:00:00Z"
sources:
  - id: notebook
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module4/Module4_Learner_Starter.ipynb"
    title: "Module4_Learner_Starter.ipynb"
    author: "team:ua-ai2s"
    last_modified: "2026-09-02T10:27:43-07:00"
---

# Module 4 Lab: Three-Role Pipeline in LangGraph and CrewAI

[![Open in Colab](../../assets/colab-badge.svg)](https://colab.research.google.com/github/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module4/Module4_Learner_Starter.ipynb){ target=_blank }

[:material-download: Download the notebook (.ipynb)](../../materials/module4/Module4_Learner_Starter.ipynb){ .md-button }
[:fontawesome-brands-github: View on GitHub](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module4/Module4_Learner_Starter.ipynb){ .md-button target=_blank }

!!! warning "API keys"

    Keep API keys out of the notebook. In Colab store them as **Secrets** (the key
    icon in the left sidebar) or enter them through the `getpass` prompt the setup
    cell provides; never paste a key into a code cell, and clear outputs before you
    submit. See [Labs, Colab, and API keys](../../start-here/labs-and-notebooks.md) for the full checklist.

!!! note "Read-only rendering"

    This page is a static rendering of the notebook with all outputs cleared. To
    run the cells, open it in Google Colab with the badge above or download the
    `.ipynb` and run it in Jupyter.

**Researcher → Analyst → Critic**  
Estimated time: **about 4 hours** (guided lab, sections 1–2: about 2 hours; hands-on project, sections 3–4: about 2 hours) · Learning objectives: **2, 3 and 4** in the Module 4 overview

This one notebook holds the guided lab (sections 1–2, LangGraph) and the hands-on project (sections 3–4, CrewAI and the framework comparison). You will specify, implement, run, and compare the same three-role workflow in two frameworks. The critic may send the work back to the analyst, but the workflow permits **at most two revision cycles**.

> **Make it yours.** The included topic is only a runnable example. Replace it with a complex question from your own academic or professional domain. A personally meaningful topic will produce a much stronger debrief and framework comparison.

#### Evidence boundary

The base lab does **not** give the researcher a live web-search tool. Its output is a synthesis of model knowledge, not verified current research. Do not present generated source details as verified. For assessed factual work, give the pipeline a source packet or add an approved search/retrieval tool and verify every citation.

### How to use this notebook

1. In Google Colab, choose **Runtime → Run all** after completing each `TODO`.
2. Use the default **Hugging Face Inference Providers** route for the capable open-weight model (a Hugging Face token is required; free credits and quotas can change).
3. Alternatively choose OpenAI or Groq, or use Ollama locally without an API key.
4. Never paste a key directly into a saved code cell. The setup cell uses a masked prompt.
5. Run **both frameworks on exactly the same topic and model** for a fair comparison.
6. Before submission, keep outputs visible and rename the file to `Module4_Lab_[YourName].ipynb`.

#### Required notebook evidence

- Completed role-specification table (five fields for each role)
- LangGraph output and structured execution log
- CrewAI output and structured execution log
- Answers to the three LangGraph execution debrief questions (at least two sentences each)
- A framework comparison of at least 200 words covering all four required dimensions

```python
# Colab setup (usually 1–3 minutes). Restart the runtime only if Colab asks.
%pip install -q "langgraph>=1.0,<2" "litellm>=1.75,<2" \
    "crewai[litellm]>=1.15,<1.16"

```

```python
import json
import logging
import os
import re
from datetime import datetime, timezone
from getpass import getpass
from pathlib import Path
from typing import Literal, TypedDict

from IPython.display import Markdown, display
from langgraph.graph import END, START, StateGraph

# Keep the teaching notebook self-contained; use the JSONL logger below instead.
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")
from crewai import Agent, Crew, LLM, Process, Task
from litellm import completion

LOG_PATH = Path("module4_three_role_pipeline.log")
logger = logging.getLogger("module4_three_role_pipeline")
logger.setLevel(logging.INFO)
logger.handlers.clear()
formatter = logging.Formatter("%(message)s")
file_handler = logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

EVENTS: list[dict] = []

def log_event(framework: str, role: str, event: str, **details) -> None:
    '''Write one JSON object per line, safe for later analysis.'''
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "framework": framework,
        "role": role,
        "event": event,
        **details,
    }
    EVENTS.append(record)
    logger.info(json.dumps(record, ensure_ascii=False))
    print(f"[{framework} | {role}] {event}")

print("Imports and structured logging are ready.")

```

### Provider and model configuration

```python
# LiteLLM gives both implementations one open interface to many model providers.
# Choose: "huggingface" (default), "groq", "openai", or "ollama" (local/no key).
PROVIDER = "huggingface"

# The prefix before the first slash is the LiteLLM provider. For Hugging Face,
# "openai/" selects its OpenAI-compatible router; the remainder is the HF model ID.
MODEL_CONFIGS = {
    "huggingface": {
        "model": "openai/openai/gpt-oss-120b:cheapest",
        "display_model": "openai/gpt-oss-120b:cheapest",
        "api_base": "https://router.huggingface.co/v1",
        "key_env": "HF_TOKEN",
    },
    "groq": {
        "model": "groq/openai/gpt-oss-120b",
        "display_model": "openai/gpt-oss-120b",
        "key_env": "GROQ_API_KEY",
    },
    "openai": {
        "model": "openai/gpt-4.1-mini",
        "display_model": "gpt-4.1-mini",
        "key_env": "OPENAI_API_KEY",
    },
    "ollama": {
        "model": "ollama/qwen3:8b",
        "display_model": "qwen3:8b",
        "api_base": "http://localhost:11434",
        "key_env": None,
    },
}

if PROVIDER not in MODEL_CONFIGS:
    raise ValueError(f"Unknown provider: {PROVIDER}")
MODEL_CONFIG = MODEL_CONFIGS[PROVIDER]

def require_secret(env_name: str) -> str:
    if not os.getenv(env_name):
        os.environ[env_name] = getpass(f"Enter {env_name} (input is hidden): ")
    if not os.getenv(env_name):
        raise ValueError(f"{env_name} is required for the selected provider.")
    return os.environ[env_name]

def shared_llm_settings() -> dict:
    settings = {"model": MODEL_CONFIG["model"], "temperature": 0.2}
    if MODEL_CONFIG.get("api_base"):
        settings["api_base"] = MODEL_CONFIG["api_base"]
    if MODEL_CONFIG.get("key_env"):
        settings["api_key"] = require_secret(MODEL_CONFIG["key_env"])
    return settings

LITELLM_SETTINGS = shared_llm_settings()

def call_shared_llm(messages: list[dict]) -> str:
    '''One provider-neutral call path used by the LangGraph implementation.'''
    response = completion(messages=messages, **LITELLM_SETTINGS)
    content = response.choices[0].message.content
    return (content or "").strip()

def make_crewai_llm() -> LLM:
    # CrewAI uses `base_url`; LiteLLM's Python function uses `api_base`.
    settings = {
        "model": LITELLM_SETTINGS["model"],
        "temperature": LITELLM_SETTINGS["temperature"],
    }
    if "api_base" in LITELLM_SETTINGS:
        settings["base_url"] = LITELLM_SETTINGS["api_base"]
    if "api_key" in LITELLM_SETTINGS:
        settings["api_key"] = LITELLM_SETTINGS["api_key"]
    return LLM(**settings)

crewai_llm = make_crewai_llm()
print(f"Provider: {PROVIDER} | Model: {MODEL_CONFIG['display_model']}")
print("Shared model interface: LiteLLM")

```

### Choose one shared task

```python
# Replace this example with a complex topic from your own domain.
EXAMPLE_TOPIC = (
    "What organizational policies could reduce burnout among distributed "
    "software teams without reducing productivity? Analyze trade-offs and "
    "make three actionable recommendations for a 200-person technology company."
)

# Strongly recommended: edit this value.
TOPIC = EXAMPLE_TOPIC

assert len(TOPIC.split()) >= 12, "Use a sufficiently complex, specific topic."
print("Pipeline topic:\n", TOPIC)

```

### 1. Role specification — complete before implementation

*Guided lab: sections 1–2, about 2 hours.*

Complete **all five fields for all three roles before writing agent code**. Make each format and handoff condition directly testable.

| Field | Researcher | Analyst | Critic |
|---|---|---|---|
| **Name + one-sentence responsibility** | TODO | TODO | TODO |
| **Input format** | TODO | TODO | TODO |
| **Output format** | TODO | TODO | TODO |
| **Handoff condition** | TODO | TODO | TODO |
| **Position-specific failure + structural mitigation** | TODO | TODO | TODO |

> Your critic criteria must be measurable. Avoid phrases such as “good quality” unless you define exactly how the code or critic will evaluate them.

**Minor hints:** Give the Researcher stable evidence labels such as `[R1]`; require the
Analyst to preserve those labels; and make the Critic's first line machine-readable. A
position-specific mitigation should change state, routing, or termination—not merely add a
stronger adjective to a prompt.

```python
## Shared, deterministic quality gate
REQUIRED_HEADINGS = (
    "## Executive Summary",
    "## Evidence-Based Analysis",
    "## Recommendations",
    "## Limitations",
)
MIN_WORDS = 400
MAX_WORDS = 700
MIN_EVIDENCE_MARKERS = 3
MAX_REVISIONS = 2

def structural_checks(text: str) -> dict:
    """TODO: compute word count, distinct [R#] markers, and missing headings."""
    # Hints:
    # - re.findall(r"\b\w+[\w'-]*\b", text) finds countable word-like tokens.
    # - set(re.findall(r"\[R\d+\]", text)) removes duplicate evidence markers.
    # - a list comprehension can retain headings that are not present in text.
    # TODO: replace the placeholder return values.
    return {
        "word_count": 0,
        "word_count_ok": False,
        "evidence_markers": [],
        "evidence_count_ok": False,
        "missing_headings": list(REQUIRED_HEADINGS),
        "headings_ok": False,
    }

def structure_passes(checks: dict) -> bool:
    # TODO: return True only when word_count_ok, evidence_count_ok, and headings_ok pass.
    # Hint: all(...) is useful here.
    raise NotImplementedError

def first_line_verdict(text: str) -> Literal["APPROVED", "REVISE"]:
    # TODO: return APPROVED only when the first nonblank line is exactly APPROVED.
    # Hint: normalize with strip() and upper(); default malformed/empty output to REVISE.
    raise NotImplementedError

```

### 2. LangGraph implementation

LangGraph makes state and routing explicit. `revision_count` means **completed analyst revisions**, not critic rejections: 0 is the initial analysis, 1 and 2 are revisions. This definition makes “maximum two revision cycles” unambiguous.

```python
class PipelineState(TypedDict):
    # TODO: add every field needed by all three roles, routing, history, and final output.
    # Field checklist: each role's output, critic feedback/verdict, completed-revision count,
    # every analysis version, final output, and the termination reason.
    task: str

def call_langgraph_role(system_prompt: str, user_prompt: str) -> str:
    # TODO: call call_shared_llm with system/user message dictionaries, then return text.
    # Hint: messages use {"role": "system"|"user", "content": "..."}.
    raise NotImplementedError

```

```python
# TODO: write precise system prompts from your role specification.
# Hint: put output structure in each prompt, but enforce critical conditions in code too.
RESEARCHER_SYSTEM = """TODO"""
ANALYST_SYSTEM = """TODO"""
CRITIC_SYSTEM = """TODO"""

def researcher_node(state: PipelineState) -> dict:
    # TODO: log start/end, invoke the Researcher, and return its state update.
    # Hint: a node returns only the fields it updates, not the entire state.
    raise NotImplementedError

def analyst_node(state: PipelineState) -> dict:
    # TODO: pass research and any critic feedback; increment only completed revisions.
    # Hint: the initial draft is revision_count=0. Increment when feedback causes a rerun,
    # append the new draft to analysis_history, and consume/clear the old feedback.
    raise NotImplementedError

def critic_node(state: PipelineState) -> dict:
    # TODO: combine the deterministic gate with the model critic's first-line verdict.
    # Hint: approval requires BOTH structure_passes(checks) and an APPROVED model verdict.
    raise NotImplementedError

def critic_routing(state: PipelineState) -> Literal["analyst", "finalize"]:
    # TODO: approve, revise, or hard-stop after MAX_REVISIONS.
    # Hint: check approval first, the hard limit second, and revision otherwise.
    raise NotImplementedError

def finalize_node(state: PipelineState) -> dict:
    # TODO: retain the latest analysis and record why execution stopped.
    # Hint: distinguish "approved" from "hard stop after N revisions" in stop_reason.
    raise NotImplementedError

```

```python
builder = StateGraph(PipelineState)
# TODO: add all four nodes and all required edges.
# TODO: use add_conditional_edges for the critic's approve/revise/hard-stop decision.
# Route sketch: START → researcher → analyst → critic; critic → analyst OR finalize;
# finalize → END. Do not also add a normal edge out of critic.

langgraph_pipeline = builder.compile()
print("TODO: compile and inspect your graph.")

```

```python
# Run this cell only after completing the LangGraph TODOs.
initial_state = {
    # TODO: initialize every PipelineState field.
    # Hint: strings start empty, revision_count starts at 0, and history starts as [].
    "task": TOPIC,
}
langgraph_result = langgraph_pipeline.invoke(initial_state, {"recursion_limit": 12})
# TODO: display the final output, stop reason, and number of analysis versions.

```

#### LangGraph execution debrief — write at least two sentences per answer

1. **Which role-specification decision had the largest behavioral impact? What evidence in the log supports your answer?**  
   TODO

2. **If you added a fourth agent, what would it do, where would it go, and what new coordination failure would it introduce?**  
   TODO

3. **How does this state schema compare with a simpler one-agent schema? What does its field count reveal about agent count and state complexity?**  
   TODO

### 3. Equivalent CrewAI implementation

*Hands-on project: sections 3–4, about 2 hours.*

CrewAI's `Agent`, `Task`, and `Crew` abstractions handle each role invocation. A small bounded Python loop makes the critic-triggered revision behavior directly comparable with LangGraph. Each stage is intentionally run as a one-task sequential Crew so the exact handoff text can be logged and inspected.

```python
# TODO: instantiate three Agent objects. Give each one a role, goal, backstory,
# crewai_llm, allow_delegation=False, a bounded max_iter, and verbose=True.
# Hint: all three agents must receive the SAME `crewai_llm` object for a fair comparison.
researcher = None
analyst = None
critic = None

async def run_crewai_task(agent: Agent, description: str, expected_output: str, role: str) -> str:
    # TODO: construct one Task and sequential Crew, await kickoff_async(), log, and return text.
    # Colab already runs an event loop: do not replace kickoff_async() with kickoff().
    # Hint: result text can be normalized with str(result).strip().
    raise NotImplementedError

async def run_crewai_pipeline(topic: str, max_revisions: int = MAX_REVISIONS) -> dict:
    # TODO: await research once, then await Analyst → Critic until approval or the hard limit.
    # Keep every analysis version and return the same conceptual fields as LangGraph.
    # Pseudocode:
    # research = await Researcher
    # while True:
    #     analysis = await Analyst; append analysis to history
    #     checks = structural_checks(analysis); critique = await Critic
    #     if approved: break
    #     if revision_count >= max_revisions: hard-stop
    #     revision_count += 1; feedback = critique
    raise NotImplementedError

```

```python
# Run this cell only after completing the CrewAI TODOs.
# Top-level await is supported by Colab/Jupyter and is required by the async pipeline.
crewai_result = await run_crewai_pipeline(TOPIC)
# TODO: display the final output, stop reason, and number of analysis versions.

```

```python
# Inspect a concise, framework-by-role execution trace.
for event in EVENTS:
    print(event["timestamp_utc"], event["framework"], event["role"], event["event"],
          event.get("verdict", ""), event.get("revision_count", ""))

print(f"\nFull JSONL log saved to: {LOG_PATH.resolve()}")

```

### 4. Framework Comparison Report — minimum 200 words

Use evidence from **your own code and execution**. Count only implementation lines (exclude imports, blank lines, comments, prompts, display code, and the shared quality-gate helper) and state your counting rule.

| Dimension | LangGraph evidence | CrewAI evidence |
|---|---|---|
| Implementation verbosity | TODO: measured LOC + configuration details | TODO: measured LOC + configuration details |
| Observability | TODO: cite specific state/log records | TODO: cite specific task/crew/log records |
| Customization flexibility | TODO: name exact routing/state edits | TODO: name exact loop/task edits |
| Developer experience | TODO: identify a specific knowledge gap | TODO: identify a specific knowledge gap |

#### Structured report (≥200 words)

**Implementation verbosity.** TODO

**Observability.** TODO

**Customization flexibility.** TODO

**Developer experience.** TODO

### Offline contract checks

```python
# Add at least three offline assertions for your quality gate and routing function.
# These tests must not make LLM/API calls.
# Suggested coverage:
# 1. A structurally valid sample passes.
# 2. "APPROVED with reservations" is treated as REVISE, not APPROVED.
# 3. REVISE at revision_count == MAX_REVISIONS routes to finalize.
# TODO: build a 400–700 word sample with all headings and at least three [R#] markers.

```

### 5. Submission checklist and troubleshooting

- [ ] I replaced the example topic (or explained why it is professionally relevant to me).
- [ ] All role-specification fields are complete.
- [ ] Both frameworks used the same topic, provider, model, and quality criteria.
- [ ] Both executions and outputs are visible.
- [ ] The log shows every role invocation and any revisions.
- [ ] Each debrief response has at least two sentences.
- [ ] The comparison is at least 200 words and uses measured evidence.
- [ ] I reviewed model-generated claims and did not describe unverified notes as live research.
- [ ] I renamed and downloaded the notebook.

**Common issues**

- `401`/authentication error: rerun the provider cell and enter the correct provider token.
- Rate limit: wait for the provider window to reset or select another provider/model.
- Model not found: providers retire model IDs; choose a current model and update `MODEL_CONFIGS`.
- Hugging Face routing error: confirm the token permits Inference Providers and try another routing suffix or supported model.
- Ollama connection error: Ollama must be running and `ollama pull qwen3:8b` must complete first.
- CrewAI event-loop error: confirm your helper uses `async def`, `await crew.kickoff_async()`, and top-level `await run_crewai_pipeline(...)`.
- The critic never approves: inspect deterministic checks and the feedback; the hard limit still terminates safely.

**Current documentation used when this template was authored (August 2026):**
[LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) ·
[CrewAI LLM connections](https://docs.crewai.com/en/learn/llm-connections) ·
[Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/en/index) ·
[LiteLLM providers](https://docs.litellm.ai/)

<p class="course-provenance" markdown>Rendered by nbconvert from the notebook [Module4_Learner_Starter.ipynb](../../materials/module4/Module4_Learner_Starter.ipynb) (`docs/materials/module4/Module4_Learner_Starter.ipynb` in the [course repository](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module4/Module4_Learner_Starter.ipynb){target=_blank}); outputs cleared. Spotted a problem? Fix the notebook, not this page.</p>
