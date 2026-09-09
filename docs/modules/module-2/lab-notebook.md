---
title: "Module 2 Lab: Building a Multi-Tool Agent"
description: "Read-only rendering of the Module 2 lab notebook, Building a Multi-Tool Agent, with links to open it in Google Colab or download the .ipynb file."
type: Lab
tags:
  - module-2
  - student-facing
  - lab
  - colab
  - langchain
  - langgraph
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

# Module 2 Lab: Building a Multi-Tool Agent

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
**What you'll build:** A LangChain agent that can search the web and run Python code — then harden it with error handling and prompt engineering.

---

### How this notebook is structured

There are four steps. Each step has:

- **Pre-written code** — run it as-is to understand what's happening
- **Extension zones** — marked `# STUDENT EXTENSION POINT` — where you add or modify code
- **A self-check** at the end to verify your output before moving on

> **Rule:** Only modify code inside extension zones. The scaffolding is designed so each step teaches one concept in isolation — changing code outside these zones makes it harder to diagnose what went wrong.

> **Which API this lab uses:** agents are built with `create_agent` from `langchain.agents`, the current LangChain agent constructor. If you find older tutorials using `AgentExecutor` or `initialize_agent`, they target LangChain 0.x and will not import on the version pinned here. You may also find `create_react_agent` in the LangGraph documentation; that is a different, lower-level function, and this course uses `create_agent`.

---

### Agent Instruction Log

Throughout this lab you will record observations in an **Agent Instruction Log**. This is a running document (a text file, Google Doc, or a Markdown cell in this notebook) where you answer specific questions after each step. Look for 📝 **Log Entry** callouts — these tell you exactly what to record and under what heading.

The log is a portfolio artifact. It is submitted alongside your `.ipynb` file.

---
## Step 1 — Set Up Your Environment and Run a Basic Agent
**Time:** ~30 minutes

By the end of Step 1 you will have a working agent that can search the web.

#### What is ReAct?
ReAct (Yao et al., 2022) is the reasoning pattern behind most production agents. It runs a three-phase loop:

1. **Reason** — the model works out what to do next
2. **Act** — the model calls a tool with specific arguments
3. **Observe** — the tool returns a result, which feeds into the next round of reasoning

The loop repeats until the model answers instead of calling a tool.

#### How you will see that loop

Early LangChain ran this loop by asking the model to *write* the words `Thought:`, `Action:` and `Observation:` as plain text, then parsing them back out. Current models call tools natively: the model returns a structured tool call, not a sentence describing one, so there are no text labels to read.

The information is all still there, and it is now easier to inspect. `create_agent` returns a LangGraph graph, and streaming that graph reports each step as data:

| Old text label | Where the same information lives now |
|---|---|
| `Thought:` | the assistant message's `content`, when the model chooses to explain itself |
| `Action:` | `tool_call["name"]` |
| `Action Input:` | `tool_call["args"]` |
| `Observation:` | the tool message's `content` |
| `Final Answer:` | the last assistant message, the one with no tool calls |

The `show_trace` helper below prints exactly those fields, so you can still watch the loop turn by turn.

#### Platform requirements
- Google account (for Colab — free tier is sufficient)
- **OpenAI API key**, OR a locally hosted **Ollama** model (free alternative; see Section 1B below)

```python
# Install required packages. Run this cell once and wait for it to finish.
# You should see a list of installed packages with no red error text.
#
# Versions are pinned so this lab behaves the same for everyone. LangChain 1.x removed
# the older AgentExecutor API, so an unpinned install would silently change what runs.
%pip install -q "langchain==1.4.0" "langchain-openai>=1.6.2,<2" "ddgs>=9.16,<10"

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
#   2. Run `ollama pull llama3.1` in your terminal
#   3. Uncomment the lines below and run this cell
#
# Use ChatOllama, not OllamaLLM: an agent needs a model that can call tools, and only
# the chat class supports that. The model must be tool-capable too — llama3.1 is,
# plain llama3 is not, and a model that cannot call tools will simply answer from
# memory and never touch your tools.

# %pip install -q "langchain-ollama>=1.1,<2"
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="llama3.1", temperature=0)
# print("Ollama model ready:", llm.invoke("Say hello in one word.").content)

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

from langchain.agents import create_agent
from langchain_core.tools import tool
from ddgs import DDGS

# --- Tool definition ---
# The docstring IS the tool description, and the description is the only signal the
# model uses to decide when to call this tool. It must be precise: what the tool does,
# what input it expects, what it returns.
@tool
def web_search(query: str) -> str:
    """Search the web for current information, recent events, or factual data that may
    not be in the model's training data.

    Args:
        query: a plain English search query of 5-10 words.

    Returns:
        Text snippets from web search results. Do not use this tool for mathematical
        calculations.
    """
    results = DDGS().text(query, max_results=5)
    if not results:
        return "No results found."
    return "\n\n".join(
        f"{r.get('title', '')}\n{r.get('body', '')}" for r in results
    )

tools = [web_search]

# --- System prompt ---
# This controls the agent's overall behaviour. It is a plain string: there are no
# {tools}, {tool_names} or {agent_scratchpad} placeholders to fill in, because the
# agent passes the tool schemas to the model itself.
SYSTEM_PROMPT = (
    "You are a helpful research assistant. Use the available tools to answer the "
    "user's question accurately. Always search for current information before making "
    "factual claims."
)

agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)
print("Agent built with tools:", [t.name for t in tools])


# --- Trace helper ---
# create_agent returns a compiled graph rather than the old AgentExecutor, so there is
# no verbose=True text trace. Streaming the graph gives you the same loop as data.
def show_trace(agent, question, recursion_limit=12):
    """Run the agent and print each step of its reasoning loop. Returns the final answer."""
    final = ""
    step = 0
    stream = agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        {"recursion_limit": recursion_limit},
        stream_mode="updates",
    )
    for chunk in stream:
        for node, update in chunk.items():
            for msg in update.get("messages", []):
                if node == "model" and getattr(msg, "tool_calls", None):
                    if msg.content:
                        print(f"[{step + 1}] REASONING:  {msg.content}")
                    for call in msg.tool_calls:
                        step += 1
                        print(f"[{step}] TOOL CALL:  {call['name']}")
                        print(f"[{step}] ARGUMENTS:  {call['args']}")
                elif node == "model":
                    final = msg.content
                    print(f"[final] ANSWER:  {final}")
                elif node == "tools":
                    body = str(msg.content).replace("\n", " ")[:400]
                    print(f"[{step}] OBSERVATION: {body}")
    return final

```

```python
# Run the agent on the test prompt.
# show_trace prints every step of the loop, then returns the final answer.
answer = show_trace(
    agent,
    "What were the three most significant AI research papers published in the last 30 days?",
)

print("\n--- FINAL ANSWER ---")
print(answer)

```

#### ✅ Step 1 Self-Check

Scroll through the output above. You should see **all four of these lines** in the trace:

| Line | What it means |
|---|---|
| `TOOL CALL:` | Should say `web_search` |
| `ARGUMENTS:` | The search query the model chose |
| `OBSERVATION:` | The raw text returned by the search tool |
| `ANSWER:` | The model's response to the original question |

A `REASONING:` line may or may not appear. Models that call tools natively often skip
straight to the call without narrating first, and that is normal — it is not a sign the
agent is misbehaving.

**If `TOOL CALL` never appears:** the agent answered from memory instead of searching.
Common causes:

- Missing or invalid API key → re-check the key in Section 1A
- The system prompt text `'Always search for current information before making factual claims'` is missing — verify it above
- On the Ollama path, the model is not tool-capable → use `llama3.1`, not `llama3`
- DuckDuckGo returns an error → wait 30 seconds and re-run (free tier has rate limits)

---

#### 📝 Log Entry — Step 1 (record in your Agent Instruction Log)

**Heading:** `Step 1 — Single-Tool Agent`

Answer these four questions:

1. **First tool call:** Copy the exact `TOOL CALL` and `ARGUMENTS` lines from the trace
2. **Tool invoked:** Which tool was called?
3. **Observation summary:** What did the search return? (1–2 sentences)
4. **Loop count:** Did the agent answer after one tool call, or did it loop? How many `TOOL CALL` / `OBSERVATION` pairs ran?

---
## Step 2 — Multi-Tool Extension: Adding a Python Tool
**Time:** ~40 minutes

A search-only agent cannot compute. In this step you add a **Python execution tool** — a tool that lets the agent write and run Python code inside Colab and observe the result. This makes the agent capable of combining retrieval (search) with computation.

#### Why tool descriptions matter
The model has no inherent knowledge of when to use search vs. Python. It infers the right tool entirely from the **description text**, which for a `@tool` function is its docstring. A vague description leads to wrong tool selection. You will see this directly in Action 8 below.

```python
# STUDENT EXTENSION POINT — Step 2
# Task: Uncomment the run_python tool below, then add it to the tools list.
# The tool code is pre-written — you only need to (1) uncomment it and (2) update tools=[...].
#
# Note there is no try/except here. That is deliberate: Step 3 depends on this tool
# failing loudly so you can see what an unhandled tool error does to an agent.

import contextlib
import io

# --- Uncomment these lines ---
# @tool
# def run_python(code: str) -> str:
#     """Run Python code for numerical calculations, data manipulation, and general
#     computation.
#
#     Args:
#         code: valid Python source. Use print() to return a value.
#
#     Returns:
#         Whatever the code printed. Do not use this tool to look up current facts or
#         search the web.
#     """
#     buffer = io.StringIO()
#     with contextlib.redirect_stdout(buffer):
#         exec(code, {})
#     return buffer.getvalue().strip() or "(the code produced no output; use print())"

# Update the tools list to include both tools.
# Change this line:
tools = [web_search]
# To this (after uncommenting the tool above):
# tools = [web_search, run_python]

# Rebuild the agent with the updated tools list.
agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)
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
    results[label] = show_trace(agent, prompt)
    print(f"\nFINAL ANSWER ({label}):", results[label])

```

#### Action 8 — Deliberately Break Tool Selection

In the cell below, change the REPL tool description to something vague, then re-run Prompt A. Observe whether the agent's tool selection changes.

**Purpose:** This demonstrates that tool selection is controlled entirely by description text — not by task complexity or any inherent model knowledge.

```python
# STUDENT EXTENSION POINT — Step 2, Action 8
# Redefine the Python tool with a deliberately vague description.
# Then rebuild the agent and re-run Prompt A.
#
# The @tool decorator takes an explicit description that overrides the docstring, which
# is how you change the description without touching the code the tool runs.

# @tool("run_python", description="Use for advanced tasks.")  # <-- intentionally vague
# def run_python_vague(code: str) -> str:
#     buffer = io.StringIO()
#     with contextlib.redirect_stdout(buffer):
#         exec(code, {})
#     return buffer.getvalue().strip() or "(the code produced no output; use print())"

# tools_vague = [web_search, run_python_vague]
# agent_vague = create_agent(model=llm, tools=tools_vague, system_prompt=SYSTEM_PROMPT)

# answer_vague = show_trace(agent_vague, prompts["A"])
# print("\nFINAL ANSWER (vague description):", answer_vague)

```

#### ✅ Step 2 Self-Check

Before moving on, confirm:

- **Prompt A** calls `web_search` first (for population), then `run_python` (for the 3.7% calculation)
- **Prompt B** calls **only** `run_python` — no web search. If the agent searches for a compound interest formula before computing, the `run_python` description is not explicit enough that math is in scope. Add `"Use this for any mathematical computation — no web lookup is needed"` to the docstring and re-run.
- **Prompt C** calls `web_search` first (for the exchange rate), then `run_python` (for the multiplication)

---

#### 📝 Log Entry — Step 2 (record in your Agent Instruction Log)

**Heading:** `Step 2 — Multi-Tool Agent`

Create a table with the following structure (one row per prompt):

| Prompt | Tools Called (in order) | Why the agent chose those tools | Did it match your prediction? |
|---|---|---|---|
| A | ... | ... | Yes / No |
| B | ... | ... | Yes / No |
| C | ... | ... | Yes / No |

Then add one more entry:

- **Action 8 result:** Did changing the description to `'Use for advanced tasks'` change which tool was selected for Prompt A? Why or why not?

---
## Step 3 — Error Handling: Deliberate Failure and Recovery
**Time:** ~30 minutes

Production agents must fail gracefully. In this step you will:

1. Trigger a real tool failure and observe the raw (unhandled) behavior
2. Rewrite the tool so it returns a structured error message instead of raising
3. Confirm the agent now responds usefully instead of crashing

#### Why this matters
A tool that raises an exception takes the whole agent run down with it: the exception
propagates out of the graph and your program stops, so the user gets a stack trace and
no answer. A tool that catches its own errors and returns a description of what went
wrong keeps the loop alive and hands the model something it can act on — retrying with
different arguments, trying another tool, or telling the user plainly that it could not
complete the task.

This is the single most common difference between a demo agent and one that survives
contact with real users.

```python
# Action 9 — Trigger a deliberate tool failure.
# Run this cell and observe what happens. Record the agent's behavior.
# Do NOT modify this prompt.
#
# Expect this cell to raise. The traceback is the point: an unhandled tool error ends
# the run. Read the last line of the traceback before moving on.

trigger_prompt = "Run the following code: import nonexistent_module; nonexistent_module.do_something()"

try:
    answer_unhandled = show_trace(agent, trigger_prompt)
    print("\n--- AGENT RESPONSE (unhandled failure) ---")
    print(answer_unhandled)
except Exception as exc:
    print(f"\n--- RUN ENDED: {type(exc).__name__}: {exc}")
    print("The tool raised, the exception escaped the agent loop, and the user got no answer.")

```

```python
# Action 10 — Error Handling
# STUDENT EXTENSION POINT — Step 3
#
# Replace the raw Python tool with a version that catches exceptions and returns a
# structured error string instead of raising.
#
# Instructions:
#   1. Read the tool below — do not change what it does, only note the try/except.
#   2. Uncomment the safe_run_python definition.
#   3. Rebuild the agent using tools = [web_search, safe_run_python].
#      (NOT tools=[web_search, run_python] — the safe version must replace the original.)

# @tool("run_python")
# def safe_run_python(code: str) -> str:
#     """Run Python code for numerical calculations, data manipulation, and general
#     computation.
#
#     Args:
#         code: valid Python source. Use print() to return a value.
#
#     Returns:
#         Whatever the code printed, or a structured error message if the code failed.
#         Do not use this tool to look up current facts or search the web.
#     """
#     buffer = io.StringIO()
#     try:
#         with contextlib.redirect_stdout(buffer):
#             exec(code, {})
#     except Exception as exc:
#         return str({
#             "status": "error",
#             "error_type": type(exc).__name__,
#             "message": str(exc),
#             "recommendation": "Try a different approach or reformulate the request.",
#         })
#     return buffer.getvalue().strip() or "(the code produced no output; use print())"

# Rebuild with the safe version:
# tools = [web_search, safe_run_python]
# agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)
# print("Agent rebuilt with tools:", [t.name for t in tools])

```

```python
# Action 11 — Re-run the trigger prompt with the safe tool.
# The agent should now receive a structured error as its OBSERVATION and respond with
# either an alternative approach or an informative answer — and this cell should not raise.

answer_handled = show_trace(agent, trigger_prompt)
print("\n--- AGENT RESPONSE (with error handling) ---")
print(answer_handled)

```

#### ✅ Step 3 Self-Check

After adding the error handling, two things must both be true:

- The cell **runs to completion** — no traceback, no `ModuleNotFoundError` ending the run
- The `OBSERVATION` line shows your structured error dict (`'status': 'error'`), not a raw exception

If the cell still raises: the safe tool is not being used. Check that
`tools = [web_search, safe_run_python]` and that you rebuilt the agent afterwards —
`create_agent` captures the tool list at build time, so editing `tools` without
rebuilding changes nothing.

> **Common mistake:** Defining `safe_run_python` but rebuilding the agent with the
> original `run_python`. The tool list passed to `create_agent` is what counts.

---

#### 📝 Log Entry — Step 3 (record in your Agent Instruction Log)

**Heading:** `Step 3 — Error Handling`

Record the following:

- **(a) Before the error handling:** What happened when the tool failed? Quote the exception type and the last line of the traceback.
- **(b) After:** How did the agent's behavior change? What appeared in the `OBSERVATION` line?
- **(c) User utility assessment:** Was the graceful degradation response useful to a hypothetical end user? Why or why not? (2–3 sentences)

---
## Step 4 — Prompt Engineering: System Instructions and Few-Shot Demonstrations
**Time:** ~20 minutes

System instructions and few-shot examples are the primary controls for agent behavior. In this step you will:

1. Add an **output format constraint** to the system instruction and observe the change
2. Add a **few-shot demonstration** to the conversation and assess whether the agent mimics it

#### What is a few-shot demonstration?
A few-shot demonstration is a worked example of the behaviour you want, placed where the
model will read it before answering.

With native tool calling there is no text template to paste an example into. Instead you
show the model a short exchange that already happened: a user turn, the assistant's tool
call, the tool's result, and the answer that followed. Those turns go into `messages`
ahead of the real question, and the model treats them as precedent.

A demonstration that describes the behaviour in prose ("first search, then calculate")
is a much weaker signal than one that shows the turns themselves.

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
#   "Always structure your final answer with: "
#   "(1) a direct answer in the first sentence, "
#   "(2) supporting evidence cited from your search results, "
#   "(3) a confidence assessment: Low, Medium, or High."

FORMAT_CONSTRAINT = "YOUR_FORMAT_CONSTRAINT_HERE"

UPDATED_INSTRUCTION = DEFAULT_INSTRUCTION.strip() + "\n\n" + FORMAT_CONSTRAINT

# The system prompt is just a string. Rebuild the agent to apply it.
agent_formatted = create_agent(
    model=llm, tools=tools, system_prompt=UPDATED_INSTRUCTION
)

# Re-run Prompt A with the updated system instruction
answer_formatted = show_trace(agent_formatted, prompts["A"])
print("\n--- FINAL ANSWER (with format constraint) ---")
print(answer_formatted)

```

```python
# Action 15 — Add a few-shot demonstration.
# STUDENT EXTENSION POINT — Step 4
#
# Write a complete worked exchange below. Use a DIFFERENT task than Prompts A, B or C.
#
# The demonstration is a list of message turns, not a block of text. Each tool call the
# assistant makes needs a matching tool result with the same id, or the model provider
# will reject the conversation as malformed.

FEW_SHOT_MESSAGES = [
    {"role": "user", "content": "What is the GDP of France, and what is 2% of that number?"},
    {
        "role": "assistant",
        "content": "I need France's current GDP first, then I can compute 2% of it.",
        "tool_calls": [
            {
                "id": "demo_1",
                "name": "web_search",
                "args": {"query": "current GDP of France"},
                "type": "tool_call",
            }
        ],
    },
    {"role": "tool", "tool_call_id": "demo_1", "content": "France GDP is approximately $3.1 trillion USD."},
    {
        "role": "assistant",
        "content": "Now I can calculate 2% of that.",
        "tool_calls": [
            {
                "id": "demo_2",
                "name": "run_python",
                "args": {"code": "print(3.1e12 * 0.02)"},
                "type": "tool_call",
            }
        ],
    },
    {"role": "tool", "tool_call_id": "demo_2", "content": "62000000000.0"},
    {
        "role": "assistant",
        "content": (
            "France's GDP is approximately $3.1 trillion. 2% of that is $62 billion. "
            "Confidence: Medium (GDP figures vary by source and year)."
        ),
    },
]

# STUDENT EXTENSION POINT: replace FEW_SHOT_MESSAGES above with your own worked example,
# then run the agent with the demonstration in front of your real question.
your_question = "REPLACE THIS WITH YOUR OWN TWO-STEP QUESTION"

result = agent_formatted.invoke(
    {"messages": FEW_SHOT_MESSAGES + [{"role": "user", "content": your_question}]},
    {"recursion_limit": 12},
)

for message in result["messages"][len(FEW_SHOT_MESSAGES):]:
    kind = type(message).__name__
    calls = getattr(message, "tool_calls", None)
    print(f"{kind}: {str(message.content)[:300]}" + (f"  tool_calls={calls}" if calls else ""))

```

#### ✅ Step 4 Self-Check

**Format constraint:** Compare the final answer from Action 14 to the one from Step 2 (same Prompt A). Does the new answer follow the structure you specified?

**Few-shot demonstration:** Look at the messages printed by Action 15. Did the agent follow the same shape as your example — the same order of tool calls, the same style of final answer? If nothing changed, check that your demonstration is well formed: every assistant `tool_calls` entry needs a matching `{"role": "tool", "tool_call_id": ...}` turn, and the tool names must be tools the agent actually has.

---

#### 📝 Log Entry — Step 4 (record in your Agent Instruction Log)

**Heading:** `Step 4 — Prompt Engineering`

Record the following:

- **(a) Format constraint text:** Copy the exact text of your output format constraint
- **(b) Before/after comparison:** Quote the final answer from Step 2 (Prompt A, no constraint) and from Action 14 (Prompt A, with constraint). How did the structure change?
- **(c) Few-shot influence:** Did the agent follow your demonstration's shape? Cite specific evidence from the printed messages.

---
## Lab Complete — Submission Instructions

Before submitting, confirm all four checks:

- [ ] All cells have been executed (no empty output cells)
- [ ] Your Agent Instruction Log contains entries for all four steps
- [ ] Step 3's final cell runs without raising
- [ ] Step 4 shows a before/after comparison of the final answer format

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
