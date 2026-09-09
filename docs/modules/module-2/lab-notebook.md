---
title: "Module 2 Lab: Building a Multi-Tool ReAct Agent"
description: "Read-only rendering of the Module 2 lab notebook, Building a Multi-Tool ReAct Agent, with links to open it in Google Colab or download the .ipynb file."
type: Lab
tags:
  - module-2
  - student-facing
  - lab
  - colab
  - langchain
  - ollama
module: 2
time_estimate: "~2 hours"
status: stable
stale_after: "2027-09-08T00:00:00Z"
generated:
  by: "process:nbconvert"
  at: "2026-09-08T00:00:00Z"
sources:
  - id: notebook
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module2/Module-2-Guided-Lab-Notebook.ipynb"
    title: "Module-2-Guided-Lab-Notebook.ipynb"
    author: "team:ua-ai2s"
    last_modified: "2026-09-02T10:27:43-07:00"
---

# Module 2 Lab: Building a Multi-Tool ReAct Agent

[![Open in Colab](../../assets/colab-badge.svg)](https://colab.research.google.com/github/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module2/Module-2-Guided-Lab-Notebook.ipynb){ target=_blank }

[:material-download: Download the notebook (.ipynb)](../../materials/module2/Module-2-Guided-Lab-Notebook.ipynb){ .md-button }
[:fontawesome-brands-github: View on GitHub](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module2/Module-2-Guided-Lab-Notebook.ipynb){ .md-button target=_blank }

!!! warning "API keys"

    Keep API keys out of the notebook. In Colab store them as **Secrets** (the key
    icon in the left sidebar) or enter them through the `getpass` prompt the setup
    cell provides; never paste a key into a code cell, and clear outputs before you
    submit. See [Labs, Colab, and API keys](../../start-here/labs-and-notebooks.md) for the full checklist.

!!! note "Read-only rendering"

    This page is a static rendering of the notebook with all outputs cleared. To
    run the cells, open it in Google Colab with the badge above or download the
    `.ipynb` and run it in Jupyter.

**Estimated time:** ~2 hours  
**What you'll build:** A LangChain ReAct agent that can search the web and run Python code — then harden it with error handling and prompt engineering.

---

### How this notebook is structured

There are four steps. Each step has:
- **Pre-written code** — run it as-is to understand what's happening
- **Extension zones** — marked `# STUDENT EXTENSION POINT` — where you add or modify code
- **A self-check** at the end to verify your output before moving on

> **Rule:** Only modify code inside extension zones. The scaffolding is designed so each step teaches one concept in isolation — changing code outside these zones makes it harder to diagnose what went wrong.

---

### Agent Instruction Log

Throughout this lab you will record observations in an **Agent Instruction Log**. This is a running document (a text file, Google Doc, or a Markdown cell in this notebook) where you answer specific questions after each step. Look for 📝 **Log Entry** callouts — these tell you exactly what to record and under what heading.

The log is a portfolio artifact. It is submitted alongside your `.ipynb` file.

---
## Step 1 — Set Up Your Environment and Run a Basic Agent
**Time:** ~30 minutes

By the end of Step 1 you will have a working ReAct agent that can search the web.

#### What is ReAct?
ReAct (Yao et al., 2022) is the default reasoning architecture for production agents. It runs a three-phase loop:

1. **Thought** — the model reasons about what to do next
2. **Action** — the model calls a tool with specific input
3. **Observation** — the tool returns a result, which feeds into the next Thought

This loop repeats until the model produces a **Final Answer**. You will see these exact labels in the output when you run the agent below.

#### Platform requirements
- Google account (for Colab — free tier is sufficient)
- **OpenAI API key**, OR a locally hosted **Ollama** model (free alternative; see Section 1B below)

```python
# Install required packages. Run this cell once and wait for it to finish.
# You should see a list of installed packages with no red error text.
!pip install -q langchain langchain-openai langchain-community duckduckgo-search
```

#### Section 1A — OpenAI API Key Setup

Paste your OpenAI API key in the cell below. The key starts with `sk-`.

> **Security note:** Never share a notebook with your key visible. In Colab, use the Secrets panel (🔑 icon in the left sidebar) and reference it as `userdata.get('OPENAI_API_KEY')` for a safer alternative.

#### Section 1B — Ollama Alternative (free, no API key needed)

If you do not have an OpenAI key, skip to the **Ollama Setup** cell below and follow those instructions instead. Skip the OpenAI cell.

```python
import os

# STUDENT EXTENSION POINT — Step 1: Add your API key here
os.environ["OPENAI_API_KEY"] = "sk-YOUR-KEY-HERE"

# Verify the key is set (prints True if it starts with 'sk-')
print("API key set:", os.environ.get("OPENAI_API_KEY", "").startswith("sk-"))
```

```python
# SECTION 1B — Ollama Alternative
# Only run this cell if you are NOT using OpenAI.
# Skip entirely if you completed Section 1A.
#
# Steps:
#   1. Install Ollama from https://ollama.com
#   2. Run `ollama pull llama3` in your terminal
#   3. Uncomment the lines below and run this cell

# !pip install -q langchain-ollama
# from langchain_ollama import OllamaLLM
# llm = OllamaLLM(model="llama3")
# print("Ollama LLM ready:", llm.invoke("Say hello in one word."))
```

```python
# Initialize the LLM (OpenAI path).
# If using Ollama, comment out these two lines — the llm variable was set above.
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Quick connectivity test — should print a short reply
print(llm.invoke("Reply with exactly three words: model is ready.").content)
```

```python
# Build a single-tool web-search agent.
# Pre-written — read every comment before running.

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate

# --- Tool definition ---
# The description is the only signal the LLM uses to decide when to call this tool.
# It must be precise: what the tool does, what input it expects, what it returns.
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="duckduckgo_search",
    func=search.run,
    description=(
        "Use this tool to search the web for current information, recent events, "
        "or factual data that may not be in the model's training data. "
        "Input: a plain English search query of 5–10 words. "
        "Output: a text snippet from web search results. "
        "Do not use this tool for mathematical calculations."
    )
)
tools = [search_tool]

# --- System prompt ---
# This controls the agent's overall behavior.
# The {tools}, {tool_names}, {input}, and {agent_scratchpad} placeholders are
# required by LangChain's ReAct template — do not remove them.
SYSTEM_PROMPT = PromptTemplate.from_template("""
You are a helpful research assistant. Use the available tools to answer the user's
question accurately. Always search for current information before making factual claims.

You have access to the following tools:
{tools}

Use this format:
Thought: what you need to do and why
Action: the tool name (must be one of [{tool_names}])
Action Input: the exact input to pass to the tool
Observation: the result returned by the tool
... (repeat Thought/Action/Observation as needed)
Thought: I now have enough information to answer
Final Answer: your complete answer to the user's question

Begin!
Question: {input}
{agent_scratchpad}
""")

# --- Agent assembly ---
agent = create_react_agent(llm=llm, tools=tools, prompt=SYSTEM_PROMPT)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,       # prints the full Thought/Action/Observation trace
    max_iterations=5,   # safety limit: stops after 5 reasoning steps
    handle_parsing_errors=True
)

print("Agent ready.")
```

```python
# Run the agent on the test prompt.
# With verbose=True you will see the full ReAct trace in the output.
result = agent_executor.invoke({
    "input": "What were the three most significant AI research papers published in the last 30 days?"
})

print("\n--- FINAL ANSWER ---")
print(result["output"])
```

#### ✅ Step 1 Self-Check

Scroll through the output above. You should see **all five of these labels** in the trace:

| Label | What it means |
|---|---|
| `Thought:` | The model's reasoning about what to do |
| `Action:` | Should say `duckduckgo_search` |
| `Action Input:` | The search query the model chose |
| `Observation:` | The raw text returned by the search tool |
| `Final Answer:` | The model's response to the original question |

**If any label is missing:** The agent is not running the ReAct pattern correctly. Common causes:
- Missing or invalid API key → re-check the key in Section 1A
- `Final Answer` appears immediately without searching → the system prompt text `'Always search for current information before making factual claims'` must be present — verify it above
- DuckDuckGo returns an error → wait 30 seconds and re-run (free tier has rate limits)

---

#### 📝 Log Entry — Step 1 (record in your Agent Instruction Log)

**Heading:** `Step 1 — Single-Tool Agent`

Answer these four questions:
1. **Thought (first step):** Copy the exact text of the first `Thought:` in the trace
2. **Tool invoked:** Which tool was called?
3. **Observation summary:** What did the search return? (1–2 sentences)
4. **Loop count:** Did the agent reach `Final Answer` in one iteration, or did it loop? How many `Thought/Action/Observation` cycles ran?

---
## Step 2 — Multi-Tool Extension: Adding a Python REPL
**Time:** ~40 minutes

A search-only agent cannot compute. In this step you add a **Python REPL tool** — a tool that lets the agent write and execute Python code inside Colab and observe the result. This makes the agent capable of combining retrieval (search) with computation (REPL).

#### Why tool descriptions matter
The LLM has no inherent knowledge of when to use search vs. REPL. It infers the right tool entirely from the **description text**. A vague description leads to wrong tool selection. You will see this directly in Action 8 below.

```python
# STUDENT EXTENSION POINT — Step 2
# Task: Uncomment the REPL tool definition below, then add `repl_tool` to the tools list.
# The tool code is pre-written — you only need to (1) uncomment it and (2) update tools=[...].

from langchain_experimental.tools.python.tool import PythonREPLTool

# --- Uncomment these lines ---
# repl = PythonREPLTool()
# repl_tool = Tool(
#     name="python_repl",
#     func=repl.run,
#     description=(
#         "Use this tool for numerical calculations, data manipulation, and Python code execution. "
#         "Input: valid Python code as a string. "
#         "Output: the printed output or result of the code. "
#         "Do not use this tool to look up current facts or search the web."
#     )
# )

# Update the tools list to include both tools.
# Change this line:
tools = [search_tool]
# To this (after uncommenting the REPL tool above):
# tools = [search_tool, repl_tool]

# Rebuild the agent with the updated tools list.
agent = create_react_agent(llm=llm, tools=tools, prompt=SYSTEM_PROMPT)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, max_iterations=6, handle_parsing_errors=True
)
print("Agent rebuilt with tools:", [t.name for t in tools])
```

```python
# Run all three test prompts in sequence.
# Do not modify the prompts — they are designed to test specific tool selection behaviors.

prompts = {
    "A": "What is the current population of Tokyo, and what is 3.7% of that number?",
    "B": "Calculate the compound interest on a $10,000 principal at 5.25% annual rate over 8 years.",
    "C": "Find today's exchange rate between USD and EUR, then calculate how much EUR you would receive for $2,500."
}

results = {}
for label, prompt in prompts.items():
    print(f"\n{'='*60}")
    print(f"PROMPT {label}: {prompt}")
    print('='*60)
    results[label] = agent_executor.invoke({"input": prompt})
    print(f"\nFINAL ANSWER ({label}):", results[label]["output"])
```

#### Action 8 — Deliberately Break Tool Selection

In the cell below, change the REPL tool description to something vague, then re-run Prompt A. Observe whether the agent's tool selection changes.

**Purpose:** This demonstrates that tool selection is controlled entirely by description text — not by task complexity or any inherent model knowledge.

```python
# STUDENT EXTENSION POINT — Step 2, Action 8
# Redefine repl_tool with a deliberately vague description.
# Then rebuild the agent and re-run Prompt A.

# repl_tool_vague = Tool(
#     name="python_repl",
#     func=repl.run,
#     description="Use for advanced tasks."  # <-- intentionally vague
# )
# tools_vague = [search_tool, repl_tool_vague]
# agent_vague = create_react_agent(llm=llm, tools=tools_vague, prompt=SYSTEM_PROMPT)
# executor_vague = AgentExecutor(agent=agent_vague, tools=tools_vague, verbose=True, max_iterations=6, handle_parsing_errors=True)

# result_vague = executor_vague.invoke({"input": prompts["A"]})
# print("\nFINAL ANSWER (vague description):", result_vague["output"])
```

#### ✅ Step 2 Self-Check

Before moving on, confirm:

- **Prompt A** invokes `duckduckgo_search` first (for population), then `python_repl` (for the 3.7% calculation)
- **Prompt B** invokes **only** `python_repl` — no web search. If the agent searches for a compound interest formula before computing, the REPL description is not explicit enough that math is in scope. Add `"Use this for any mathematical computation — no web lookup is needed"` to the description and re-run.
- **Prompt C** invokes search first (for the exchange rate), then REPL (for the multiplication)

---

#### 📝 Log Entry — Step 2 (record in your Agent Instruction Log)

**Heading:** `Step 2 — Multi-Tool Agent`

Create a table with the following structure (one row per prompt):

| Prompt | Tools Invoked (in order) | Why the agent chose those tools | Did it match your prediction? |
|---|---|---|---|
| A | ... | ... | Yes / No |
| B | ... | ... | Yes / No |
| C | ... | ... | Yes / No |

Then add one more entry:
- **Action 8 result:** Did changing the REPL description to `'Use for advanced tasks'` change which tool was selected for Prompt A? Why or why not?

---
## Step 3 — Error Handling: Deliberate Failure and Recovery
**Time:** ~30 minutes

Production agents must fail gracefully. In this step you will:
1. Trigger a real tool failure and observe the raw (unhandled) behavior
2. Implement an error handling wrapper that returns a structured error message instead of a Python traceback
3. Confirm the agent now responds usefully instead of crashing or hallucinating

#### Why this matters
An unhandled exception in a tool produces a raw Python traceback in the agent's `Observation`. Most LLMs will either loop indefinitely trying to fix the code, or produce a hallucinated Final Answer that ignores the failure. A structured error message gives the model actionable information to recover from.

```python
# Action 9 — Trigger a deliberate tool failure.
# Run this cell and observe what happens. Record the agent's behavior.
# Do NOT modify this prompt.

trigger_prompt = "Run the following code: import nonexistent_module; nonexistent_module.do_something()"

result_unhandled = agent_executor.invoke({"input": trigger_prompt})
print("\n--- AGENT RESPONSE (unhandled failure) ---")
print(result_unhandled["output"])
```

```python
# Action 10 — Error Handling Wrapper
# STUDENT EXTENSION POINT — Step 3
#
# Replace the raw REPL tool with a wrapped version that catches exceptions
# and returns a structured error dict instead of a raw traceback.
#
# Instructions:
#   1. Read the wrapper function below — do not modify it.
#   2. Uncomment the wrapped_repl_tool definition.
#   3. Rebuild the agent using tools = [search_tool, wrapped_repl_tool].
#      (NOT tools=[search_tool, repl_tool] — the wrapped version must replace the original.)

import traceback

def safe_repl_run(code: str) -> str:
    """Wraps the REPL tool to return structured errors instead of raw tracebacks."""
    try:
        return repl.run(code)
    except Exception as e:
        return str({
            "status": "error",
            "message": str(e),
            "recommendation": "Try a different approach or reformulate the query."
        })

# Uncomment these lines:
# wrapped_repl_tool = Tool(
#     name="python_repl",
#     func=safe_repl_run,
#     description=(
#         "Use this tool for numerical calculations, data manipulation, and Python code execution. "
#         "Input: valid Python code as a string. "
#         "Output: the printed output, or a structured error message if the code fails. "
#         "Do not use this tool to look up current facts or search the web."
#     )
# )

# Rebuild with the wrapped version:
# tools = [search_tool, wrapped_repl_tool]
# agent = create_react_agent(llm=llm, tools=tools, prompt=SYSTEM_PROMPT)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=6, handle_parsing_errors=True)
# print("Agent rebuilt with wrapped REPL:", [t.name for t in tools])
```

```python
# Action 11 — Re-run the trigger prompt with the wrapped tool.
# The agent should now receive a structured error in its Observation
# and respond with either an alternative approach or an informative Final Answer.

result_handled = agent_executor.invoke({"input": trigger_prompt})
print("\n--- AGENT RESPONSE (with error wrapper) ---")
print(result_handled["output"])
```

#### ✅ Step 3 Self-Check

After implementing the wrapper, the agent's Final Answer **must not** contain a raw Python traceback (lines starting with `Traceback (most recent call last):`). 

If a traceback still appears: the wrapper is not being applied. Check that `tools = [search_tool, wrapped_repl_tool]` uses the wrapped version, not the original `repl_tool`.

> **Common mistake:** Defining `safe_repl_run` but then passing `repl_tool` (the original) to the `tools` list. The function must be used in `wrapped_repl_tool`, which must be in `tools`.

---

#### 📝 Log Entry — Step 3 (record in your Agent Instruction Log)

**Heading:** `Step 3 — Error Handling`

Record the following:
- **(a) Before the wrapper:** What did the agent do when the tool failed? (Looped? Hallucinated? Produced a traceback in Final Answer?)
- **(b) After the wrapper:** How did the agent's behavior change? What appeared in the `Observation`?
- **(c) User utility assessment:** Was the graceful degradation response useful to a hypothetical end user? Why or why not? (2–3 sentences)

---
## Step 4 — Prompt Engineering: System Instructions and Few-Shot Demonstrations
**Time:** ~20 minutes

System instructions and few-shot examples are the primary controls for agent behavior. In this step you will:
1. Add an **output format constraint** to the system instruction and observe the change
2. Add a **few-shot demonstration** to the prompt and assess whether the agent mimics it

#### What is a few-shot demonstration?
A few-shot demonstration is a complete example of the reasoning trace you want the agent to follow, placed inside the prompt. It must be a full `Thought → Action → Action Input → Observation → Thought → Final Answer` sequence — not a plain text description. LangChain requires it to be formatted as a Human/AI turn pair (see the template below). A syntactically malformed demonstration is silently ignored.

```python
# Action 13 — Read the default system instruction.
# The default instruction is pre-written below.
# Do not modify it yet — read it carefully before Action 14.

DEFAULT_INSTRUCTION = """
You are a helpful research assistant. Use the available tools to answer the user's
question accurately. Always search for current information before making factual claims.
"""

print(DEFAULT_INSTRUCTION)
```

```python
# Action 14 — Add an output format constraint.
# STUDENT EXTENSION POINT — Step 4
#
# Replace YOUR_FORMAT_CONSTRAINT_HERE with a specific output structure requirement.
# Example (copy this or write your own):
#   "Always structure your Final Answer with: "
#   "(1) a direct answer in the first sentence, "
#   "(2) supporting evidence cited from your search results, "
#   "(3) a confidence assessment: Low, Medium, or High."

FORMAT_CONSTRAINT = "YOUR_FORMAT_CONSTRAINT_HERE"

UPDATED_INSTRUCTION = DEFAULT_INSTRUCTION.strip() + "\n\n" + FORMAT_CONSTRAINT

UPDATED_PROMPT = PromptTemplate.from_template(
    UPDATED_INSTRUCTION + """

You have access to the following tools:
{tools}

Use this format:
Thought: what you need to do and why
Action: the tool name (must be one of [{tool_names}])
Action Input: the exact input to pass to the tool
Observation: the result returned by the tool
... (repeat as needed)
Thought: I now have enough information to answer
Final Answer: your complete answer

Begin!
Question: {input}
{agent_scratchpad}
"""
)

agent = create_react_agent(llm=llm, tools=tools, prompt=UPDATED_PROMPT)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=6, handle_parsing_errors=True)

# Re-run Prompt A with the updated system instruction
result_formatted = agent_executor.invoke({"input": prompts["A"]})
print("\n--- FINAL ANSWER (with format constraint) ---")
print(result_formatted["output"])
```

```python
# Action 15 — Add a few-shot demonstration.
# STUDENT EXTENSION POINT — Step 4
#
# Write a complete Thought → Action → Action Input → Observation → Thought → Final Answer
# sequence below. Use a DIFFERENT task than Prompts A, B, or C.
#
# The example MUST be formatted as a Human/AI turn pair (shown below).
# A plain-text example placed in the system prompt will be ignored.

from langchain.prompts import FewShotPromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# Section 4B — Few-Shot Template
# Fill in YOUR_FEW_SHOT_EXAMPLE with your own complete trace.
# The example below is a placeholder — replace it with a task from your domain.
FEW_SHOT_EXAMPLE = """Human: What is the GDP of France, and what is 2% of that number?
AI:
Thought: I need the current GDP of France, then I can compute 2% of it.
Action: duckduckgo_search
Action Input: current GDP of France 2024
Observation: France GDP 2024 is approximately $3.1 trillion USD.
Thought: I have the GDP. Now I can calculate 2% using the REPL.
Action: python_repl
Action Input: print(3.1e12 * 0.02)
Observation: 62000000000.0
Thought: I have both pieces of information.
Final Answer: France's GDP is approximately $3.1 trillion. 2% of that is $62 billion. Confidence: Medium (GDP figures vary by source and year)."""

# Append the few-shot example to the prompt
FEW_SHOT_PROMPT = PromptTemplate.from_template(
    UPDATED_INSTRUCTION + "\n\nHere is an example of the reasoning format:\n\n" + FEW_SHOT_EXAMPLE + """

You have access to the following tools:
{tools}

Use this format:
Thought: what you need to do and why
Action: the tool name (must be one of [{tool_names}])
Action Input: the exact input to pass to the tool
Observation: the result returned by the tool
... (repeat as needed)
Thought: I now have enough information to answer
Final Answer: your complete answer

Begin!
Question: {input}
{agent_scratchpad}
"""
)

agent = create_react_agent(llm=llm, tools=tools, prompt=FEW_SHOT_PROMPT)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=6, handle_parsing_errors=True)

# Run Prompt C with the few-shot prompt
result_fewshot = agent_executor.invoke({"input": prompts["C"]})
print("\n--- FINAL ANSWER (with few-shot) ---")
print(result_fewshot["output"])
```

#### ✅ Step 4 Self-Check

**Format constraint:** Compare the Final Answer from Action 14 to the one from Step 2 (same Prompt A). Does the new answer follow the structure you specified?

**Few-shot demonstration:** Look at the reasoning trace from Action 15. Does the agent's `Thought →...→ Final Answer` structure resemble your example? If not, check that your few-shot example is syntactically complete (all six labels present) and that it is formatted as a `Human:`/`AI:` turn pair.

---

#### 📝 Log Entry — Step 4 (record in your Agent Instruction Log)

**Heading:** `Step 4 — Prompt Engineering`

Record the following:
- **(a) Format constraint text:** Copy the exact text of your output format constraint
- **(b) Before/after comparison:** Quote the Final Answer from Step 2 (Prompt A, no constraint) and the Final Answer from Action 14 (Prompt A, with constraint). How did the structure change?
- **(c) Few-shot influence:** Did the agent's reasoning trace in Action 15 mimic your demonstration's format? Cite specific evidence from the trace.

---
## Lab Complete — Submission Instructions

Before submitting, confirm all four checks:

- [ ] All cells have been executed (no empty output cells)
- [ ] Your Agent Instruction Log contains entries for all four steps
- [ ] Step 3's Final Answer contains no raw Python tracebacks
- [ ] Step 4 shows a before/after comparison of Final Answer format

**Submit to GitHub:**
- File: `Module2_Unit3_Lab_[YourName].ipynb`
- All cells must be executed with visible output

---

### What's next?

Unit 4 builds directly on this lab. In Task 1 you will design your own complete prompt engineering suite — system instruction, tool descriptions, and few-shot demonstrations — for a domain of your choice. The agent architecture insights from Steps 2–4 are the inputs to that design task.

```python
# Optional: Use this cell as your Agent Instruction Log if you prefer to keep it in the notebook.
# Add your entries below — one section per step.

AGENT_INSTRUCTION_LOG = """
=== AGENT INSTRUCTION LOG ===

--- Step 1 — Single-Tool Agent ---
1. First Thought:
2. Tool invoked:
3. Observation summary:
4. Loop count:

--- Step 2 — Multi-Tool Agent ---
| Prompt | Tools Invoked | Why | Matched prediction? |
| A      |               |     |                     |
| B      |               |     |                     |
| C      |               |     |                     |

Action 8 result:

--- Step 3 — Error Handling ---
(a) Before wrapper:
(b) After wrapper:
(c) User utility assessment:

--- Step 4 — Prompt Engineering ---
(a) Format constraint text:
(b) Before/after Final Answer comparison:
(c) Few-shot influence:
"""

print(AGENT_INSTRUCTION_LOG)
```

<p class="course-provenance" markdown>Rendered by nbconvert from the notebook [Module-2-Guided-Lab-Notebook.ipynb](../../materials/module2/Module-2-Guided-Lab-Notebook.ipynb) (`docs/materials/module2/Module-2-Guided-Lab-Notebook.ipynb` in the [course repository](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module2/Module-2-Guided-Lab-Notebook.ipynb){target=_blank}); outputs cleared. Spotted a problem? Fix the notebook, not this page.</p>
