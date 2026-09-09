---
title: 'Module 2: Additional Suggested Resources'
description: Supplementary notes for Module 2 comparing LLM agent reasoning paradigms (Chain-of-Thought, ReAct, Tree of Thoughts, LATS), the Belief-Desire-Intention model, and how LangChain's AgentExecutor runs the ReAct loop.
type: Resource List
tags:
- module-2
- student-facing
- resources
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
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2:-Additional-Suggested--Resources
  title: 'AI Automation and Agents v2 wiki: Module-2:-Additional-Suggested--Resources'
  author: Carlos Lizárraga-Celaya
  last_modified: '2026-06-25T13:37:57-07:00'
authorship:
  created: '2026-05-09'
  updated: '2026-05-09'
  contributors:
  - C. Lizárraga
wiki_page: Module-2:-Additional-Suggested--Resources
---
# Module 2: Additional Suggested Resources

## Primary LLM Agent Reasoning Paradigms

Here is a breakdown of the primary LLM agent reasoning paradigms based on the sources:

*   **Chain-of-Thought (CoT)** 
    *   **Structure:** Uses single-path reasoning, prompting the LLM to break a problem into a sequential, step-by-step "thought process" before concluding. 
    *   **Computation:** Relatively low inference cost, as it generates a single sequence of thoughts without exploring multiple parallel paths.
    *   **Best suited for:** Mathematical, symbolic, or logical problems where the solution benefits from step-by-step deduction.

*   **ReAct (Reason + Act)**
    *   **Structure:** Interleaves internal reasoning ("Thought") with external tool use ("Action") and environmental feedback ("Observation"). The agent continuously loops through these steps until a terminal condition or goal is met.
    *   **Computation:** Moderate to high, as it requires multiple LLM calls in a loop to evaluate observations and decide the next action.
    *   **Best suited for:** Exploratory workflows, multi-hop queries, and open-ended tasks where the agent must adapt its plan dynamically based on external information.

*   **Tree of Thoughts (ToT)**
    *   **Structure:** A multi-path approach where the LLM generates multiple possible reasoning steps (branches) and self-evaluates them at each stage. It explores the problem space using search algorithms like breadth-first or depth-first search.
    *   **Computation:** Highly computationally expensive and time-consuming, often requiring dozens of LLM calls to resolve a single problem due to generating and evaluating multiple plans.
    *   **Best suited for:** Extremely complex, open-ended problem-solving where early mistakes could cascade, requiring the system to explore and weigh multiple strategies before committing.

*   **Language Agent Tree Search (LATS)**
    *   While the provided materials list LATS as a key reasoning paradigm alongside the others, they do not detail its specific structural assumptions, computational requirements, or ideal use cases. 

The ReAct (Reason + Act) pattern operates through a continuous, multi-step cycle:

*   **Thought:** The LLM analyzes the context, identifies missing information, and reasons about the best next step.
*   **Action:** Based on that reasoning, the LLM selects and invokes a specific external tool with the appropriate parameters.
*   **Observation:** The tool executes and returns a result, which is then appended back into the agent's context window.
*   **Termination:** The model evaluates whether this new observation provides enough information to satisfy the user's original query. If it does, the loop ends and the agent generates a final answer. If not, the loop repeats with a new thought.

We previously looked at a code example of how LangChain's `AgentExecutor` runs this loop. 

**Differences between ReAct and Tree of Thoughts**

The main difference between the two is how they explore solutions: ReAct follows a single, linear path of trial and error, while Tree of Thoughts (ToT) explores multiple paths simultaneously.

*   **ReAct (Reason + Act):** Operates in a single continuous loop where the agent thinks, takes an action (like using a tool), observes the result, and repeats. It is fast, practical, and highly effective for tasks that require gathering external information dynamically.
*   **Tree of Thoughts:** Generates multiple possible reasoning steps at once, branching out like a tree. The model self-evaluates each branch (often using breadth-first or depth-first search algorithms) to determine the best path forward before committing to a final answer.

**The Trade-off:** ReAct is computationally cheaper but can get stuck if it makes a wrong assumption early on. ToT is excellent for complex problem-solving where you need the agent to weigh multiple strategies, but it is extremely computationally expensive, sometimes requiring dozens of LLM calls to solve a single problem.

## Belief-Desire-Intention (BDI) architecture

The Belief-Desire-Intention (BDI) architecture is a classic model that describes an agent's decision-making process using human-like mental states. 

Here is how the three parts break down, especially in the context of modern AI:
*   **Beliefs:** What the agent "knows" about its environment, which includes its pre-trained knowledge and any real-time data it retrieves.
*   **Desires:** The end goals the agent wants to achieve, which typically map directly to the overarching objective or user prompt.
*   **Intentions:** The specific plans and action sequences (like tool calls) the agent actively commits to executing to fulfill its desires.

## ReAct loop in LangChain

In LangChain, the ReAct loop is practically managed by a runtime component called the `AgentExecutor`. 

Here is how it physically orchestrates the ReAct loop:
*   **Thought & Action:** The LLM analyzes the user's prompt and decides it needs external information. It outputs a reasoning trace (the "thought") and requests a specific tool call (the "action").
*   **Execution:** The `AgentExecutor` steps in, physically runs the requested tool (like a web search API or custom Python function), and captures the result.
*   **Observation:** The executor feeds this result (the "observation") back into the LLM's context window so the model can read it.
*   **Iteration:** The LLM evaluates the new observation and decides if the goal is met. If not, it triggers another thought and action. This loop repeats until the model determines it has enough information to formulate a final answer.

Here is a practical code example showing how to set up and run an `AgentExecutor` in LangChain. 

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# 1. Initialize the LLM and define your tools (assuming tools are already defined)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [task_status_tool, docs_search_tool]

# 2. Create the prompt template, including the required scratchpad for reasoning traces
prompt = PromptTemplate.from_template("""
You are a project assistant. Respond based on the user's input using the appropriate tools.
User's input: {input}
{agent_scratchpad}
""")

# 3. Create the agent and bind it to the AgentExecutor
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. Invoke the executor to trigger the ReAct loop
response = agent_executor.invoke({"input": "What's the status of task1?"})
print(response['output'])
```

In this setup, the `create_tool_calling_agent` function defines how the LLM interacts with the prompt and tools. The `AgentExecutor` then acts as the runtime environment that continuously cycles through selecting actions, executing the tools, and processing the outputs until the agent formulates a final conclusion. Setting `verbose=True` lets you watch the "Thought-Action-Observation" steps happen live in your console.

## Functional Components of a Tool-Calling Agent Architecture

Here is a breakdown of the functional components in a tool-calling agent:

*   **LLM Backbone:** The central reasoning engine that interprets the user's prompt, analyzes the context, and decides which actions to take.
*   **Tool Registry:** A defined collection of available functions (like APIs, web searches, or calculators) equipped with descriptions and input schemas that tell the LLM what capabilities it can use.
*   **Action Executor:** The runtime environment that physically runs the specific tool chosen by the LLM using the parameters the model generated.
*   **Memory Module:** The system that tracks past conversation history, tool outputs, and observations to maintain context across the interaction.

During a single task episode, the information flows in this sequence:
1.  The user's input is combined with past context from the **Memory Module** and sent to the **LLM Backbone**.
2.  The LLM analyzes the request alongside the available capabilities in the **Tool Registry**. It decides a tool is needed and outputs a structured tool request.
3.  The **Action Executor** intercepts this request, physically runs the specified tool, and retrieves the result.
4.  This result is appended to the **Memory Module** and fed back into the LLM's context window.
5.  The LLM evaluates this new information to determine if the task goal is met. If it is, the LLM generates the final response for the user; if not, it triggers another tool call to continue gathering information.

Here is how you combine those components into a working `AgentExecutor` in LangChain:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

# 1. Define your LLM and tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [task_status_tool, docs_search_tool]

# 2. Create the prompt (must include agent_scratchpad for reasoning memory)
prompt_template = """
You are a project assistant. Respond based on the user's input using the appropriate tools.
User's input: {input}
{agent_scratchpad}
"""
prompt = PromptTemplate.from_template(prompt_template)

# 3. Create the agent and bind it to the executor
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. Run the task episode
response = agent_executor.invoke({"input": "What's the status of task1?"})
print(response['output'])
```

The `create_tool_calling_agent` function directly combines your LLM, tool registry, and prompt. The `AgentExecutor` then steps in as the action executor, taking the user's input and continuously managing the ReAct loop until it reaches a final answer. Setting `verbose=True` allows you to watch the "Thought-Action-Observation" steps print live in your console.

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2:-Additional-Suggested--Resources){target=_blank} (wiki page last changed 2026-06-25). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-2/resources.md){target=_blank}.</p>
