#!/usr/bin/env python3
"""Migrate the UA-AI2S AI-Automation-and-Agents-v2 GitHub wiki into the OKF/Zensical bundle under docs/.

Reproducible pipeline (modeled on UNM-CARC/docs scripts/migrate_quickbytes.py):

  1. Reads every wiki page from WIKI_DIR (a clone of
     https://github.com/UA-AI2S/AI-Automation-and-Agents-v2.wiki.git, pinned at WIKI_REF).
  2. For every entry in PAGES: extracts the Created/Updated footer, splits the two-document
     "Addendum" pages, converts GitHub-only constructs (raw <img> heroes, [!NOTE] alerts,
     one-column callout tables, exposed answer keys, letter/roman heading prefixes, wiki URLs)
     into Zensical Markdown (admonitions, collapsibles, relative links, attr_list images),
     applies exact-literal PATCHES, and prepends OKF v0.2 frontmatter with provenance taken
     from the wiki git history.
  3. Writes section index.md directory listings (no frontmatter, OKF section 8) and the
     wiki-to-site crosswalk page.
  4. Self-checks the output (no blob URLs, no GitHub alerts, no exposed keys, one H1 per page).

Usage:
  python scripts/migrate_wiki.py                 # regenerate docs/ pages owned by the pipeline
  python scripts/migrate_wiki.py --check         # write to a temp dir and diff against docs/
  python scripts/migrate_wiki.py --only Home.md  # process a single wiki page
  python scripts/migrate_wiki.py --notebooks     # also render the lab notebooks (render_notebooks.py)

Environment: WIKI_DIR (default .sources/wiki-v2), ASSETS_DIR (default .sources/repo-v2),
SKIP_REF_CHECK=1 to bypass the pinned-commit assertion.
Hand-curated pages are marked frozen=True and are never overwritten once they exist.
"""

from __future__ import annotations

import argparse
import datetime as dt
import filecmp
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unicodedata
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
WIKI_DIR = Path(os.environ.get("WIKI_DIR", ROOT / ".sources" / "wiki-v2"))
ASSETS_DIR = Path(os.environ.get("ASSETS_DIR", ROOT / ".sources" / "repo-v2"))

WIKI_REF = "fcc9835d10d30ab10d4502cc531cc6bd0ff5c47a"
ASSETS_REF = "cb749d1fd31c2cf1fa74000c8b5a1cd6af7b80e4"
GENERATED_AT = "2026-09-08T00:00:00Z"
GENERATED_BY = "process:scripts/migrate_wiki.py"
STALE_TOOLS = "2027-09-01T00:00:00Z"      # framework/tool-version-sensitive pages
STALE_PRICING = "2027-04-30T00:00:00Z"    # vendor pricing claims

WIKI_BASE = "https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/"
REPO_SLUG = "tyson-swetnam/AI-Automation-and-Agents"
REPO_URL = f"https://github.com/{REPO_SLUG}"
EDIT_BASE = f"{REPO_URL}/edit/main/docs/"

HYPHEN_U2010 = "\u2010"
EYE = "\U0001F441\uFE0F\u200D\U0001F5E8\uFE0F"

# Tags that mark a page as tool-version-sensitive (site_lint requires stale_after when present).
TOOL_TAGS = {"langchain", "langgraph", "crewai", "langsmith", "langfuse", "ollama", "openwork",
             "claude-desktop", "n8n", "autogen", "colab", "chroma", "zapier", "make"}

CREDIT_NAMES = {
    "Carlos Lizarraga-Celaya": "Carlos Lizárraga-Celaya",
    "cosimichele": "Michele Cosi",
    "C. Lizarraga": "C. Lizárraga",
}

# ---------------------------------------------------------------------------
# Page mapping
# ---------------------------------------------------------------------------


@dataclass
class Page:
    src: str                      # exact wiki filename (may contain U+2010, ':', '?', parentheses)
    dest: str                     # path relative to docs/
    title: str
    description: str
    type: str
    tags: list[str]
    module: int | None = None
    status: str = ""              # "", draft, deprecated
    stale_after: str = ""
    time_estimate: str = ""
    superseded_by: str = ""       # docs-relative path of the live page (deprecated pages only)
    part: str = ""                # "" whole file, "A" reading guides, "B" chapter quizzes
    drop_title: int = 0           # number of leading title/subtitle heading lines to drop
    html_body: bool = False       # page is a full <html> document
    pandoc: bool = False          # pandoc leftovers (Act-3)
    gdocs: bool = False           # Google-Docs backslash escapes (portfolio tutorial)
    lead: str = ""                # italic lead line under the H1
    note: str = ""                # extra admonition body after the H1 (historical documents)
    audience: str = "student-facing"
    extra_sources: list[dict] = field(default_factory=list)
    frozen: bool = False

    @property
    def wiki_name(self) -> str:
        return self.src[:-3] if self.src.endswith(".md") else self.src


MODULE_TITLES = {
    1: "From Prompts to Pipelines",
    2: "Agent Reasoning Architectures and Tool Integration",
    3: "Memory Architectures and Retrieval-Augmented Generation",
    4: "Multi-Agent Systems",
    5: "Responsible Agentic AI",
}

OVERVIEW_DESC = {
    1: "Introduction to Module 1 (8 hours): what an AI agent is, the perceive-plan-act-observe loop, the no-code/low-code/code-first automation landscape, learning objectives, unit checklist, grade weights, and the diagnostic self-survey.",
    2: "Overview of Module 2 (8 hours): agent reasoning paradigms (Chain-of-Thought, ReAct, Tree of Thoughts, LATS), LangChain tool integration, prompt design, reasoning-trace evaluation, chapter checklist, and grade weights.",
    3: "Overview of Module 3 (8 hours) on agent memory and Retrieval-Augmented Generation: introduction, topics, learning objectives, chapter and deliverable checklist, and grade weights.",
    4: "Overview of Module 4 (8 hours): designing, implementing, and evaluating multi-agent systems with LangGraph and CrewAI, with learning objectives, checklist, and grade weights.",
    5: "Overview of Module 5 (8 hours) on taking agents from prototype to production: evaluation, LangSmith observability, OWASP Top 10 for LLM applications, and EU AI Act / NIST AI RMF governance.",
}
FC_DESC = {
    1: "Five-chapter conceptual lesson for Module 1: what AI agents are, the no-code/low-code/code-first automation spectrum, AI literacy frameworks, workflow decomposition and two-dimensional automation assessment, and responsible AI governance.",
    2: "Five-chapter lesson on how LLM-based agents reason and act: the CoT/ReAct/Tree-of-Thoughts/LATS paradigms, LangChain tool integration, reasoning-trace failure analysis, prompt engineering for behavioral control, and architectural trade-offs.",
    3: "Five-chapter lesson on agent memory and RAG: parametric vs. non-parametric memory, the six-stage RAG pipeline, four conversational memory patterns in LangChain, retrieval and context-window optimization, and RAGAS evaluation.",
    4: "Five-chapter lesson on multi-agent systems: when MAS is justified, four coordination patterns, the LangGraph/AutoGen/CrewAI orchestration frameworks, the coordination-failure taxonomy, and evidence-based single-vs-multi-agent benchmarks.",
    5: "Five-chapter lesson on taking AI agents from prototype to production: hidden technical debt and the production stack, multi-dimensional evaluation and CI/CD, observability, the OWASP Top 10 for LLM applications, and responsible AI governance.",
}
RG_DESC = {
    1: "Reading guides (sources, key terms, guiding questions, critical-thinking prompts) for the five chapters of Module 1, From Prompts to Pipelines.",
    2: "Read-extract-synthesize reading guides for the five Module 2 chapters: CoT, ReAct, Tree of Thoughts, LATS, tool integration, reasoning-trace critique, agent prompt engineering, and architectural trade-offs.",
    3: "Reading guides with guiding questions for the five chapters of Module 3 on memory architectures and retrieval-augmented generation.",
    4: "Five reading guides (sources, key terms, guiding questions, critical-thinking prompts) for Module 4, Multi-Agent Systems: design, coordination, and evidence-based evaluation.",
    5: "Chapter-by-chapter reading guides (focus points and active reading tasks) for the Module 5 chapters on production deployment, evaluation, observability, LLM security, and responsible AI.",
}
QUIZ_DESC = {
    n: f"Five self-evaluating five-question chapter quizzes with collapsed answer keys and per-option feedback for Module {n}, {MODULE_TITLES[n]}."
    for n in range(1, 6)
}
ACT_DESC = {
    1: "Activity guide for Module 1: ungraded self-check prompts, two hands-on labs (running Llama 3.2 locally with Ollama and delegating file tasks to an agent via Openwork), the Workflow Audit project with mapping template and assessment matrix, and the peer discussion.",
    2: "Module 2 activity guide: self-check prompts on reasoning paradigms, a guided Colab lab building a multi-tool LangChain ReAct agent, a hands-on project adding a custom tool, and a project-proposal discussion with peer review.",
    3: "Step-by-step activity guide for Module 3: self-check prompts, the guided LangChain RAG lab in Colab, a chunking and retrieval optimization project, and a domain-focused peer discussion.",
    4: "Self-check prompts, the LangGraph Researcher-Analyst-Critic lab, a CrewAI framework-comparison project, and the peer-discussion assignment for Module 4 on multi-agent systems.",
    5: "Self-check prompts, the LangSmith observability guided lab and comparative observability project, and the capstone Responsible Deployment Plan peer discussion for Module 5.",
}
RES_DESC = {
    1: "Curated supplementary notes for Module 1 covering generative AI foundations, agent types, development tooling, what distinguishes an agent from chatbots, APIs and scripts, the ReAct loop, and automation paradigms with low-code examples.",
    2: "Supplementary notes for Module 2 comparing LLM agent reasoning paradigms (Chain-of-Thought, ReAct, Tree of Thoughts, LATS), the Belief-Desire-Intention model, and how LangChain's create_agent runtime runs the ReAct loop.",
    3: "Supplementary notes for Module 3 explaining parametric vs. non-parametric agent memory, the six-stage RAG pipeline with its design decisions and consequences, the RAGAS faithfulness metric, and text-splitting strategies.",
}
TOPIC_TAGS = {
    1: ["ai-agents", "agent-loop", "automation-paradigms", "workflow-audit"],
    2: ["reasoning-paradigms", "react", "langchain", "tool-use", "prompt-engineering"],
    3: ["memory", "rag", "langchain", "chroma", "ragas"],
    4: ["multi-agent-systems", "langgraph", "crewai", "orchestration"],
    5: ["production", "evaluation", "langsmith", "owasp", "eu-ai-act", "nist-ai-rmf"],
}


def _tags(module: int | None, role: str, *extra: str, audience: str = "student-facing") -> list[str]:
    scope = f"module-{module}" if module else "course"
    seen: list[str] = []
    for t in [scope, audience, role, *(TOPIC_TAGS.get(module, []) if module else []), *extra]:
        if t and t not in seen:
            seen.append(t)
    return seen


PAGES: list[Page] = []

for n in range(1, 6):
    overview_title = {
        1: "Module 1 Overview: From Prompts to Pipelines",
        2: "Module 2 Overview: Agent Reasoning Architectures and Tool Integration",
        3: "Module 3 Overview: Memory Architectures and RAG",
        4: "Module 4 Overview: Multi-Agent Systems",
        5: "Module 5 Overview: Responsible Agentic AI",
    }[n]
    PAGES.append(Page(f"Module-{n}:-Overview.md", f"modules/module-{n}/overview.md", overview_title, OVERVIEW_DESC[n],
                      "Overview", _tags(n, "overview"), module=n, drop_title=1,
                      stale_after=STALE_TOOLS if n == 3 else ""))
    PAGES.append(Page(f"Module-{n}:-Foundational-Concepts.md", f"modules/module-{n}/foundational-concepts.md",
                      f"Module {n}: Foundational Concepts", FC_DESC[n], "Lesson", _tags(n, "lesson"), module=n,
                      drop_title=1 if n in (1, 2) else 0, stale_after="" if n == 1 else STALE_TOOLS))
    addendum = "Module-1.2-Addendum.md" if n == 1 else f"Module-{n}.2-Addendum.md"
    PAGES.append(Page(addendum, f"modules/module-{n}/reading-guides.md", f"Module {n} Reading Guides", RG_DESC[n],
                      "Reading Guide", _tags(n, "reading-guide"), module=n, part="A", drop_title=2,
                      stale_after="" if n == 1 else STALE_TOOLS))
    PAGES.append(Page(addendum, f"modules/module-{n}/chapter-quizzes.md", f"Module {n} Chapter Quizzes", QUIZ_DESC[n],
                      "Assessment", _tags(n, "quiz", "self-assessment", "answer-key"), module=n, part="B",
                      drop_title=1 if n == 5 else 2, stale_after="" if n == 1 else STALE_TOOLS))
    PAGES.append(Page(f"Module-{n}:-Activities.md", f"modules/module-{n}/activities.md", f"Module {n} Activities",
                      ACT_DESC[n], "Activity", _tags(n, "activities", *(["ollama", "openwork"] if n == 1 else ["colab"])),
                      module=n, drop_title=1 if n in (3, 5) else 0, status="draft" if n == 2 else "",
                      stale_after=STALE_TOOLS))
    if n <= 3:
        src = "Module-2:-Additional-Suggested--Resources.md" if n == 2 else f"Module-{n}:-Additional-Suggested-Resources.md"
        # every resources page quotes framework APIs, so all three carry tool tags + stale_after
        extra_res = ["langchain", "crewai"] if n == 1 else []
        PAGES.append(Page(src, f"modules/module-{n}/resources.md", f"Module {n}: Additional Suggested Resources",
                          RES_DESC[n], "Resource List", _tags(n, "resources", *extra_res), module=n,
                          stale_after=STALE_TOOLS))

PAGES += [
    Page("Module-1-Act-3:-What-is-an-agent?.md", "modules/module-1/readings/what-is-an-agent.md",
         "What Is an AI Agent?",
         "Module 1 reading package contrasting LangChain's engineering definition of an agent with Wooldridge and Jennings' (1995) theoretical definition, ending with a 12-term glossary pre-fill worksheet and synthesis questions.",
         "Reading", _tags(1, "reading", "langchain", "bdi", "wooldridge-jennings"), module=1, drop_title=1, pandoc=True,
         extra_sources=[
             {"id": "langchain-agents", "resource": "https://python.langchain.com/docs/concepts/agents/", "title": "LangChain Conceptual Guide: Agents", "author": "team:langchain"},
             {"id": "wooldridge-jennings-1995", "resource": "https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/ker95.pdf", "title": "Intelligent Agents: Theory and Practice (1995)", "author": "Michael Wooldridge; Nicholas R. Jennings"},
         ]),
    Page("Module-1-Act-5:-AI-Automation-and-Multi\u2010Agent-Frameworks.md",
         "modules/module-1/readings/automation-and-multi-agent-frameworks.md",
         "AI Automation and Multi-Agent Frameworks: A Strategic Comparison",
         "Reading that compares the no-code and low-code automation platforms Zapier, Make and n8n with the developer-centric multi-agent frameworks CrewAI and LangChain/LangGraph, and maps them onto an AI maturity roadmap.",
         "Reading", _tags(1, "reading", "n8n", "zapier", "make", "crewai", "langchain"), module=1, drop_title=1,
         html_body=True, stale_after=STALE_PRICING),
    Page("Module-1:-Intelligent-Agents-(book-summary).md",
         "modules/module-1/readings/intelligent-agents-wooldridge-jennings.md",
         "Intelligent Agents: Theory and Practice (Reading Summary)",
         "Student-oriented summary of Wooldridge and Jennings (1995): the weak and strong notions of agency, the four pillars of agent behavior, intentional systems, and how agents differ from objects and processes.",
         "Reading", _tags(1, "reading", "wooldridge-jennings", "bdi"), module=1, drop_title=1, html_body=True,
         extra_sources=[{"id": "wooldridge-jennings-1995", "resource": "https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/ker95.pdf", "title": "Intelligent Agents: Theory and Practice (1995)", "author": "Michael Wooldridge; Nicholas R. Jennings"}]),
    Page("Module-1-Act-6:-AI-Agents-Glossary.md", "modules/module-1/worksheets/ai-agents-glossary.md",
         "Worksheet: AI Agents Glossary",
         "Fill-in glossary worksheet of AI-agent concepts and tools (agent, context window, embedding, RAG, MCP, prompt injection, n8n, LangGraph, Claude Code, Ollama, and more) with columns for definition, own words, and one example.",
         "Worksheet", _tags(1, "worksheet", "glossary"), module=1, status="draft",
         lead="Fill in each row: the formal definition from the readings, the definition in your own words, and one concrete example. A [Word version of this worksheet](../../../materials/module1/Illustrated_AI_Glossary.docx) is available to download."),
    Page("Module-1-Act-7:-Automation-Paradigms-Comparison-Diagram.md",
         "modules/module-1/worksheets/automation-paradigms-comparison.md",
         "Worksheet: Automation Paradigms Comparison",
         "Blank comparison worksheet for contrasting the no-code, low-code, and code-first automation paradigms across tools, technical skill, setup effort, learning curve, flexibility, cost, data governance, and best-for use cases.",
         "Worksheet", _tags(1, "worksheet", "automation-paradigms"), module=1, status="draft",
         lead="Compare the three automation paradigms across each feature row, using Chapter 2 of the [foundational concepts](../foundational-concepts.md) and your own research."),
    Page("Module-1-Act-8:-Module-1-Concept-Quiz.md", "archive/module-1/concept-quiz-spec-draft.md",
         "Module 1 Concept Quiz (Specification Draft)",
         "Superseded specification and partial draft of the 15-question Module 1 concept quiz; the live quiz is the interactive page.",
         "Assessment", _tags(1, "quiz", "answer-key", "superseded"), module=1, status="deprecated",
         superseded_by="modules/module-1/concept-quiz.md"),
    Page("Module-1-Act-11:-Guided-Workflow-Mapping-Exercise.md", "archive/module-1/guided-workflow-mapping-stub.md",
         "Guided Workflow Mapping Exercise (Stub)",
         "Unfinished synopsis of a scaffolded invoice-review mapping rehearsal; the Workflow Audit project in the Module 1 activities absorbs this exercise.",
         "Activity", _tags(1, "activities", "workflow-mapping", "superseded"), module=1, status="deprecated",
         superseded_by="modules/module-1/activities.md"),
    Page("Module-1-Unit-3-Lab-A.md", "archive/module-1/lab-checklist-claude-desktop.md",
         "Lab Checklist: Claude Desktop Orientation (Superseded)",
         "Early checklist lab for installing Claude Desktop and delegating a test task through Chat and Cowork; superseded by Lab B in the Module 1 activities.",
         "Lab", _tags(1, "lab", "claude-desktop", "superseded"), module=1, status="deprecated",
         superseded_by="modules/module-1/activities.md"),
    Page("Module-1-Unit-3-Lab-B.md", "archive/module-1/lab-checklist-ollama.md",
         "Lab Checklist: Local LLM with Ollama (Superseded)",
         "Early checklist lab for installing Ollama, pulling llama3.2, and probing it with factual, reasoning, and uncertainty prompts; superseded by Lab A in the Module 1 activities.",
         "Lab", _tags(1, "lab", "ollama", "superseded"), module=1, status="deprecated",
         superseded_by="modules/module-1/activities.md"),
    Page("Module-1:-Overview2.md", "archive/module-1/overview-draft-2026-06.md",
         "Module 1 Overview (June 2026 Draft)",
         "Superseded June 2026 draft of the Module 1 overview containing the detailed tiered learning objectives table (LO 1.1-1.8), the Workflow Audit hands-on project brief, and a curated resource list.",
         "Overview", _tags(1, "overview", "superseded"), module=1, status="deprecated", drop_title=1,
         superseded_by="modules/module-1/overview.md"),
    Page("Module-2.2-Addendum-\u2010-OLD.md", "archive/module-2/self-assessment-quizzes.md",
         "Module 2 Self-Assessment Quizzes (Retired)",
         "Five ungraded five-question self-assessment quizzes with answer keys for the Module 2 chapters; retired in favor of the chapter quizzes.",
         "Assessment", _tags(2, "quiz", "answer-key", "superseded"), module=2, status="deprecated", drop_title=1,
         superseded_by="modules/module-2/chapter-quizzes.md"),
    Page("Github-Portfolio-Tutorial.md", "start-here/github-portfolio-setup.md", "GitHub Portfolio Setup Guide",
         "Step-by-step guide for students to open a GitHub account, create the course portfolio repository, structure it by module, write README and learning-log templates, and maintain it with regular commits.",
         "Tutorial", _tags(None, "tutorial", "github", "portfolio"), drop_title=2, gdocs=True),
    Page("Formal-Learning-Design-Information.md", "course-design/learning-design.md", "Formal Learning Design",
         "Course-level instructional design document mapping the standard per-module activity structure to Bloom's Taxonomy and defining the general course competencies and the module-specific skills for Modules 1-5.",
         "Course Design", _tags(None, "course-design", "blooms-taxonomy", "learning-outcomes", audience="instructor-facing"),
         audience="instructor-facing"),
    Page("Development-Plan.md", "course-design/development-plan.md", "Course Development Plan",
         "Pointer to the Google Sheets milestone tracker used to plan and track development of the course.",
         "Course Design", _tags(None, "course-design", "milestones", audience="instructor-facing"), status="draft",
         audience="instructor-facing",
         lead="The course team tracks development milestones in a shared spreadsheet (an institutional login may be required)."),
    Page("Course-Review-Analysis-v1.md", "course-design/course-review-2026-07.md", "Course Review Analysis (July 2026)",
         "Internal pedagogical review of the five-module course written from a graduate student's perspective, flagging overview/content mismatches, prerequisite escalation, and writing-load imbalance as of July 2026.",
         "Course Design", _tags(None, "course-design", "review", audience="instructor-facing"), status="deprecated",
         drop_title=1, audience="instructor-facing", superseded_by="course-design/development-plan.md",
         note="This review reflects the course as of 2026-07-31. Several findings (overview rewrites, Module 2 alternative frameworks) have since been addressed; see the development plan for current status."),
]

# Wiki files that do not become pages, with the site path they resolve to.
DROPPED: dict[str, str] = {
    "Home": "index.md",
    "_Sidebar": "",
    "_Footer": "about/license-and-attribution.md",
    "Module-2.2-\u2010-Addendum": "modules/module-2/reading-guides.md",
}

# Exact-literal patches keyed by dest; each (old, new) must match at least once in the source text.
# Module 2's resources page shipped two LangChain 0.x samples. Kept as named
# constants because they are long enough to drown the PATCHES table inline.
M2_RESOURCES_CODE_1_OLD = '```python\nfrom langchain_openai import ChatOpenAI\nfrom langchain.agents import create_tool_calling_agent, AgentExecutor\nfrom langchain_core.prompts import PromptTemplate\n\n# 1. Initialize the LLM and define your tools (assuming tools are already defined)\nllm = ChatOpenAI(model="gpt-4o-mini", temperature=0)\ntools = [task_status_tool, docs_search_tool]\n\n# 2. Create the prompt template, including the required scratchpad for reasoning traces\nprompt = PromptTemplate.from_template("""\nYou are a project assistant. Respond based on the user\'s input using the appropriate tools.\nUser\'s input: {input}\n{agent_scratchpad}\n""")\n\n# 3. Create the agent and bind it to the AgentExecutor\nagent = create_tool_calling_agent(llm, tools, prompt)\nagent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)\n\n# 4. Invoke the executor to trigger the ReAct loop\nresponse = agent_executor.invoke({"input": "What\'s the status of task1?"})\nprint(response[\'output\'])\n```'

M2_RESOURCES_CODE_1_NEW = '```python\nfrom langchain.agents import create_agent\nfrom langchain_openai import ChatOpenAI\n\n# 1. Initialize the LLM and define your tools (assuming tools are already defined)\nllm = ChatOpenAI(model="gpt-4o-mini", temperature=0)\ntools = [task_status_tool, docs_search_tool]\n\n# 2. The system prompt is a plain string. There is no {agent_scratchpad} placeholder:\n#    the agent keeps the reasoning history in its own message state.\nSYSTEM_PROMPT = "You are a project assistant. Answer the user using the appropriate tools."\n\n# 3. Build the agent\nagent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)\n\n# 4. Invoke it to trigger the reasoning loop\nresponse = agent.invoke(\n    {"messages": [{"role": "user", "content": "What\'s the status of task1?"}]}\n)\nprint(response["messages"][-1].content)\n```'

M2_RESOURCES_CODE_2_OLD = '```python\nfrom langchain_openai import ChatOpenAI\nfrom langchain.prompts import PromptTemplate\nfrom langchain.agents import create_tool_calling_agent, AgentExecutor\n\n# 1. Define your LLM and tools\nllm = ChatOpenAI(model="gpt-4o-mini", temperature=0)\ntools = [task_status_tool, docs_search_tool]\n\n# 2. Create the prompt (must include agent_scratchpad for reasoning memory)\nprompt_template = """\nYou are a project assistant. Respond based on the user\'s input using the appropriate tools.\nUser\'s input: {input}\n{agent_scratchpad}\n"""\nprompt = PromptTemplate.from_template(prompt_template)\n\n# 3. Create the agent and bind it to the executor\nagent = create_tool_calling_agent(llm, tools, prompt)\nagent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)\n\n# 4. Run the task episode\nresponse = agent_executor.invoke({"input": "What\'s the status of task1?"})\nprint(response[\'output\'])\n```'

M2_RESOURCES_CODE_2_NEW = '```python\nfrom langchain.agents import create_agent\nfrom langchain_openai import ChatOpenAI\n\n# 1. Define your LLM and tools\nllm = ChatOpenAI(model="gpt-4o-mini", temperature=0)\ntools = [task_status_tool, docs_search_tool]\n\n# 2. Give the agent its instructions. The tool registry is passed separately, so the\n#    prompt does not need to list the tools or reserve a slot for reasoning memory.\nSYSTEM_PROMPT = "You are a project assistant. Answer the user using the appropriate tools."\n\n# 3. Build the agent\nagent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)\n\n# 4. Run the task episode\nresponse = agent.invoke(\n    {"messages": [{"role": "user", "content": "What\'s the status of task1?"}]}\n)\nprint(response["messages"][-1].content)\n```'

# The Module 2 lesson's architecture figure, redrawn. The wiki shipped a LangChain 0.x
# AgentExecutor design table; it is retired rather than recaptioned, so the crosswalk that
# made it readable is gone and what it taught independently is now prose. Kept as a constant
# because a fenced diagram and a table do not read well inline in the PATCHES table.
M2_AGENT_RUNTIME = '**The agent runtime.** Four structural components, and the loop that connects them:\n\n```mermaid\nflowchart TD\n    IN["User message"] --> STATE["Memory Module"]\n    STATE --> LLM["LLM Backbone"]\n    LLM --> Q{"Requests a tool?"}\n    Q -- no --> OUT["Final answer"]\n    Q -- yes --> EXEC["Action Executor"]\n    EXEC --> OBS["Observation"]\n    OBS --> STATE\n    REG["Tool Registry"] -- descriptions --> LLM\n    REG -- callables --> EXEC\n```\n\n| Component | Role and design considerations |\n| --- | --- |\n| **LLM Backbone** | The reasoning core. Reads the system prompt, the message state and the tool descriptions, then produces either a tool call or a final answer. It never runs a tool itself: it names one and supplies the arguments. |\n| **Tool Registry** | The registered tools, each with a description and an input schema. The model reads the descriptions to choose; for a `@tool` function the description is its docstring unless an explicit `description=` overrides it. Description quality is the single largest determinant of reliable tool use — ambiguous or incomplete descriptions produce wrong choices and invented arguments. |\n| **Action Executor** | Runs the tool the model named, with the arguments it supplied, and appends the result to the state as an observation. A tool that raises propagates out and ends the run, so a production tool catches its own errors and returns them as text the model can reason about. |\n| **Memory Module** | The running message state: the conversation, every tool call and every observation. Each pass of the loop sees what the previous passes produced. Pass a `checkpointer` to `create_agent` to persist it across invocations. |\n\n**Stopping is a rule, not a component.** The loop ends when the model returns a message that requests no tools, and that message carries the final answer; the step cap is the `recursion_limit` config key. The LangChain 0.x design listed three stopping conditions instead — a "Final Answer" token, a maximum-iteration argument and a parsing-error threshold — and the current API has none of them. The first two are replaced by the rule and the config key above. The third has nothing left to act on: a tool-calling model emits the structured call directly, so no component parses text into an action.\n\n**Older tutorials use different names.** Material written against the `AgentExecutor` that LangChain 1.0 removed calls these four *Agent (the LLM)*, *Tool Descriptions*, *Tool Executor* and *Memory / State*. Those component lists often run to five, and the extra entry is one of two things: an output parser, which a tool-calling model makes unnecessary, or stopping criteria, which is the loop rule above rather than a part of the runtime.'

# Tables that the wiki shipped as PNG screenshots, transcribed back into Markdown so the
# content is searchable, reflows on a phone, and reaches screen readers and llms.txt. Each
# was read from the full-resolution original in images/ and checked against it a second time.
IMAGE_TABLES: dict[str, str] = {
    '2D-Automation-AssessmentMatrix': '| Dimension | Score 5 (High) | Score 1 (Low) |\n| --- | --- | --- |\n| **Rule-Based Specification Score (1–5)** | Every step can be specified in advance as a complete rule — no human judgment is required at any decision point. The conditional branches are fully enumerable. | At least one step requires genuine human expertise, ethical judgment, or contextual knowledge that cannot be pre-specified as a rule. |\n| **Consequence Severity Score (1–5)** | An automation error would have irreversible, significant financial, legal, or reputational consequences. Error blast radius is wide and recovery is costly. | An automation error is easily detected, immediately reversible, and has no external impact. Error blast radius is narrow and recovery is trivial. |\n| **Automation Potential Score** | Calculated: Rule-Based Score ÷ (Consequence Severity + 1). This formula penalizes high-consequence workflows even when they are technically rule-based. | Lower scores indicate poorer automation candidates, either because the workflow requires judgment or because errors are high-stakes. |',
    'Agent-Prompt-Architecture': "**The Four-Dimension Agent Prompt Architecture**\n\n**Dimension 1: System Instructions**\n\nThe system prompt defines the agent's identity, role, operational domain, and constraints. Effective system instructions specify: what the agent is for (domain scope), what it is not for (negative scope — prevents the agent from attempting tasks outside its competency), what it must always do (standing behavioral requirements), and what it must never do (hard behavioral limits). Vague system instructions produce agents with unpredictable behavioral boundaries.\n\n**Dimension 2: Tool Descriptions**\n\nAs detailed in Theme 2, tool descriptions function as the agent's mental model of its available capabilities. In the prompt architecture, tool descriptions are presented to the agent as a structured list immediately after the system instructions, before any conversation context. The order in which tools are listed can affect which tool the agent selects when multiple tools are plausible candidates for a given subtask — an empirical effect documented in LangChain's design guidance.\n\n**Dimension 3: Few-Shot CoT Scaffolds**\n\nFew-shot examples demonstrate correct reasoning patterns for the agent's task domain. Brown et al. (2020) established that in-context few-shot examples can elicit capabilities in LLMs that zero-shot prompting cannot. For agents, few-shot examples in the system prompt demonstrate: what a correct Thought step looks like for this problem type, how to select the right tool given a specific context, how to interpret the tool's output, and when to conclude versus continue the loop.\n\n**Dimension 4: Output Format Constraints**\n\nAgents must produce outputs in formats that the AgentExecutor can parse. Output format constraints in the system prompt specify: the exact JSON structure for tool call specifications, the token or string that signals task completion (Final Answer), the format of intermediate Thought steps, and any constraints on output length or content. Poorly specified output format constraints produce parsing errors that terminate the agent prematurely or cause the executor to misinterpret a reasoning step as a tool call.",
    'Automation_Tools': '| Dimension | No-Code | Low-Code | Code-First | Key Criterion |\n| --- | --- | --- | --- | --- |\n| **Representative tools** | Claude Cowork, n8n, Zapier, Make | LangChain, CrewAI, LangGraph | Claude Code, custom Python agents, AutoGen | What does your team know? |\n| **Primary user** | Knowledge workers, operations professionals, non-developers | Data scientists, AI practitioners, technical analysts | Software engineers, ML researchers | Who will build and maintain this? |\n| **Setup effort** | Minutes to hours; visual interface | Hours to days; configuration + scripting | Days to weeks; full development cycle | What is the time budget? |\n| **Flexibility** | Limited to platform capabilities | High within framework constraints | Unlimited — any architecture possible | How custom is the workflow? |\n| **Cost model** | Subscription; per-workflow or per-seat | API costs + developer time | Full developer cost + infrastructure | What is the total cost of ownership? |\n| **Data governance** | Data processed on vendor servers | API data transit; partial control | Full data sovereignty possible | What are the compliance requirements? |\n| **Best suited for** | Standard repetitive processes with low customization needs | Complex workflows requiring LLM reasoning and tool integration | Novel architectures, proprietary data, maximum control | What does the workflow require? |',
    'Blooms_Spiral_Progression': "**Bloom's Spiral Progression Across the Course**\n\n**Modules 1–2:** Weighted toward L1–L2 (Remember, Understand) — building vocabulary and mental models for automation design.\n\n**Modules 3–4:** Weighted toward L2–L3 (Understand, Apply) — integrating tools and building functional agent systems.\n\n**Module 5:** Weighted toward L3–L4 (Apply, Analyze) — auditing, policy-writing, and analytical evaluation of complete systems.",
    'Chain-of-Thought': "| Dimension | Chain-of-Thought Characteristics |\n| --- | --- |\n| **Core mechanism** | Decompose the problem into a linear sequence of intermediate reasoning steps before producing the final answer. |\n| **Prompting approach** | Few-shot examples where each example includes the reasoning chain (thought steps) followed by the answer, OR zero-shot 'Let's think step by step.' |\n| **Key strength** | Dramatically improves multi-step arithmetic, commonsense reasoning, and symbolic tasks. Low computational overhead — produces one reasoning chain per query. |\n| **Key limitation** | Linear: once a reasoning step is committed to, the model cannot backtrack. If an early step contains an error, subsequent reasoning inherits and compounds it. No mechanism for exploration of alternatives. |\n| **When to use** | Problems with a natural linear decomposition, where intermediate steps are checkable or low-stakes, and where computational cost is a primary constraint. |",
    'Chunking-Strategy-Selection': "| Strategy | Mechanism | When to Use | Failure Mode |\n| --- | --- | --- | --- |\n| **Fixed-Size Chunking** | Split text at a fixed token or character count, with a specified overlap between adjacent chunks | Uniform text (narrative prose, documentation) with no structural hierarchy; simplest to implement | Splits semantic units mid-sentence; chunk boundaries are arbitrary relative to content structure |\n| **Recursive Character Text Splitting** | Attempt to split at natural boundaries in order: paragraph breaks → sentence breaks → word breaks → characters; falls back to finer granularity only when a chunk exceeds the size limit | Mixed-format documents with variable paragraph lengths; LangChain's default and most broadly applicable strategy | May still split mid-concept when natural boundaries are unevenly distributed |\n| **Semantic Chunking** | Embed each sentence individually; cluster sentences by embedding similarity; split at embedding-similarity discontinuities that signal topic transitions | Documents with clear topic shifts (research papers, multi-topic reports); produces thematically coherent chunks | Computationally expensive — embeds every sentence before splitting; may over-split on very dense or technical documents |\n| **Sentence-Window Chunking** | Embed individual sentences for retrieval but expand each retrieved sentence to include surrounding context sentences before injecting into the generation prompt | When the retrieval unit (sentence) needs to be finer than the generation unit (context window); produces highly targeted retrieval with rich generation context | Requires more complex retrieval pipeline; the expansion logic must be correctly configured to avoid context overflow |",
    'Critical_Distinctions': '**The Critical Distinctions — What Is Not an AI Agent**\n\n| System Type | Why It Is Not an AI Agent |\n| --- | --- |\n| **Chatbot** | Responds to a single prompt; has no persistent state across the conversation turn; cannot take actions in external systems; does not loop. |\n| **Rule-based script** | Executes a fixed sequence of steps; has no capacity to reason, adapt, or select actions based on context; has no LLM component. |\n| **API call** | A single request-response transaction with no reasoning, planning, or state — a tool that an agent might use, not an agent itself. |\n| **Search engine** | Retrieves information based on a query; does not plan, act, or use tools autonomously; has no goal-directed behavior. |',
    'Four-Paradigm-Comparative-Framework': '| Dimension | CoT | ReAct | ToT | LATS |\n| --- | --- | --- | --- | --- |\n| **Reasoning structure** | Linear chain — one path, committed at each step | Interleaved Thought-Act-Observe cycles | Branching tree — multiple paths explored and pruned | Tree search with real-world tool use at each node |\n| **Tool use** | None — operates on internal knowledge only | Yes — tool calls interleaved with reasoning | Not inherent — can be added but not the core architecture | Yes — tool use IS the tree expansion mechanism |\n| **Backtracking** | No — errors propagate forward | No — linear like CoT, just grounded | Yes — key feature: prune and backtrack | Yes — core capability |\n| **Computational cost** | Low — one reasoning pass per query | Medium — proportional to number of tool calls | High — proportional to tree breadth × depth | Very high — tree breadth × depth × tool calls |\n| **Best problem type** | Structured, decomposable, linear | Grounded fact-finding, QA with external sources, multi-step task execution | Open-ended planning, constraint satisfaction, proof construction | Complex planning requiring external information at each decision point |\n| **Hallucination risk** | High — no grounding in external facts | Low — observations ground each reasoning step | Medium — internal evaluation may be unreliable | Low — external observations ground evaluations |\n| **Interpretability** | High — trace is a natural language argument | High — trace shows exact tool calls and outcomes | Moderate — tree structure adds complexity | Low — tree plus tool use plus self-reflection is complex |',
    'Four-RAGAS-Metrics': "**The Four RAGAS Metrics — Definitions, Computation, and Diagnostic Use**\n\n| Metric | Definition | What a Low Score Means | Which Pipeline Component is Implicated |\n| --- | --- | --- | --- |\n| **Faithfulness** | The proportion of claims in the generated answer that are directly supported by the retrieved context. Computed by decomposing the answer into atomic claims and verifying each against the context. | The generator is hallucinating — producing claims not supported by the retrieved context. The answer cannot be trusted even if retrieval was successful. | Generator (Stage 6) — revise the generation prompt to strengthen the 'use only the provided context' instruction; or the retrieved context is too sparse to support the answer. |\n| **Answer Relevance** | The degree to which the generated answer addresses the user's question, independent of whether the answer is factually correct. Computed by generating questions from the answer and measuring their similarity to the original question. | The generator is producing on-topic but non-responsive output — answering a related but different question or providing a broader or narrower response than requested. | Generator (Stage 6) — revise the generation prompt to clarify the required response scope; or the query was ambiguous and should be pre-processed. |\n| **Context Precision** | The proportion of retrieved context chunks that are relevant to answering the question. Measures retrieval precision — how much of what was retrieved was needed. | The retriever is returning too many irrelevant chunks. Relevant information is buried in noise, increasing context window consumption and degrading generation quality. | Retriever (Stage 5) — reduce k, switch to MMR, add metadata filtering, or improve the embedding model's domain sensitivity. |\n| **Context Recall** | The proportion of the ground-truth answer that is supported by the retrieved context. Measures retrieval completeness — how much of what was needed was retrieved. | The retriever is missing relevant documents. The generator cannot answer correctly because the relevant information was not retrieved. | Retriever (Stage 5) and/or text splitter (Stage 2) — increase k, adjust chunking to prevent relevant content from being fragmented across chunk boundaries, or review corpus coverage. |",
    'Four_PIllars_AI_Literacy': '**The Four-Pillar AI Literacy Model (Ng et al., 2021)**\n\n**Pillar: KNOW AI**\n\nUnderstand the fundamental concepts, capabilities, and limitations of AI systems. In Module 1, this means understanding the agent loop, the properties of autonomous agents, and the boundaries of what current LLMs can and cannot do without tool access.\n\n*Module 1 focus — Units 1 and 2 (Reading, Video, Concept Quiz)*\n\n**Pillar: USE AI**\n\nOperate AI tools productively in authentic contexts. In Module 1, this means running a local model with Ollama and delegating a structured task to an agent through Openwork — not just reading about it.\n\n*Module 1 focus — Unit 3 (Guided Labs: Ollama, Openwork)*\n\n**Pillar: EVALUATE AI**\n\nCritically assess AI outputs, assess automation potential, compare frameworks, and identify failure modes. In Module 1, this means applying the two-dimensional assessment matrix to your own workflows with written justifications.\n\n*Module 1 focus — Units 4 and 5 (Workflow Audit, Paradigm Comparison)*\n\n**Pillar: CREATE WITH AI**\n\nDesign original AI-enabled solutions for real-world problems. Module 1 plants the seed: the Workflow Audit produces the specification that Modules 2–5 will attempt to automate. Create competency is the terminal goal of the entire course.\n\n*Introduced Module 1, fully developed Modules 3–5*',
    'Four_Stage_Agent_Loop': '| Stage | What the Agent Does | Technical Mechanism | Professional Analogy |\n| --- | --- | --- | --- |\n| **PERCEIVE** | Reads the current environment state | Processes context window: instructions, tool outputs, history | A consultant reads the brief, prior meeting notes, and available data before responding |\n| **PLAN** | Decides what action to take next | LLM reasoning step: selects the next tool or determines task completion | The consultant drafts a response strategy, selecting which of their available resources to deploy |\n| **ACT** | Executes the chosen action via a tool call | Issues a structured tool call (web search, code execution, file write, API request) | The consultant executes: sends an email, retrieves a document, runs a calculation |\n| **OBSERVE** | Reads the tool output and updates state | Parses tool response; decides whether to loop again or conclude | The consultant reads the result, determines whether the task is complete, and acts accordingly |',
    'Module1_Units_Plan': '| Unit | Activity Type | Est. Time | Learning Objectives | Graded |\n| --- | --- | --- | --- | --- |\n| 1 | Reading + Video Content | 1.5 hours | LO 1, LO 2 | No |\n| 2 | Concept Quiz / Retrieval Check | 0.5 hours | LO 1, LO 2 | No |\n| 3 | Guided Lab Exercise | 2.0 hours | LO 3, LO 4 | No* |\n| 4 | Hands-On Project — Workflow Audit | 2.5 hours | LO 5, LO 6 | **YES** |\n| 5 | Case Study / Comparative Analysis | 1.0 hour | LO 7 | No* |\n| 6 | Peer Discussion + Reflection | 0.5 hours | LO 8 | Completion |\n| — | TOTAL | 8.0 hours | LO 1–8 | |',
    'ModuleLearningActivitiesDescription1': "| ID | Activity Name | Bloom's | Strategy |\n| --- | --- | --- | --- |\n| **A0** | Guided Pre-Reading with Structured Annotation | L1 | Annotation template (5–8 key terms, one-sentence summaries, clarifying questions) made explicit in Unit 1 guidance rather than assumed as student initiative. |\n| **A1** | Prior Knowledge Activation Recall | L1 | Explanatory feedback on every incorrect response replicates the correction function. Advisory note targets the three most consequential misconceptions for the module's content domain proactively. |\n| **A2** | Concept Mapping from Memory | L1 | Reference concept map provided in Unit 2 quiz feedback serves the same correction function as the instructor's displayed map. Partial credit: described in advisory, not graded. |\n| **A3** | Instructor-Led Conceptual Walkthrough with Live Narration | L2 | Video narration is the closest equivalent to live instructor voice. Annotated notebook preserves decision rationale in text form. Prediction prompts must be explicitly embedded — they do not arise naturally in self-paced reading. |\n| **A4** | Comparative Analysis Matrix | L2 | Model matrix comparison replicates the correction function of the class debrief. Students instructed to compare entries before proceeding to Unit 3 lab. |\n| **A5** | Think-Pair-Share Conceptual Discussion | L2 | Forum prompt design is critical: must require evidence-based explanation ('explain why X rather than Y, citing a specific assigned reading'), not reflection ('what did you find interesting?'). Partially compensated — social presence is delayed, not immediate. |\n| **A6** | Peer Teaching — Concept Explanation | L2 | Peer review rubric must require substantive design justification questions, not generic feedback. The 'explain to your partner' mechanism is partially reproduced through the reviewer's required justification questions. |\n| **A7** | Worked Example Code Walkthrough | L3 | Decision narration in comments must match the granularity of live narration. A reference implementation that shows what without explaining why a solution template is, not a worked example — it trains copying rather than schema formation. |\n| **A8** | Guided Implementation Lab (Scaffolded) | L3 | Troubleshooting guide replaces instructor just-in-time support. Must be proactively designed from documented common errors. Verification checkpoint specificity (exact expected output) is the most important design element. |\n| **A9** | Independent / Pair Implementation Lab | L3 | 3-sentence design rationale is a mandatory submission element, not optional — under time pressure students omit optional elements, defeating the purpose of articulating tacit design decisions. |\n| **A10** | Parameter Variation and Controlled Experiment | L3 | Parameter specification in submission checklist prevents under-compliance. Students instructed to form a conclusion before consulting benchmark reference values — conclusion first, then comparison. |",
    'ModuleLearningActivitiesDescription2': "| ID | Activity Name | Bloom's | Strategy |\n| --- | --- | --- | --- |\n| **A11** | Structured Peer Demonstration and Critique | L3 | Specificity requirement ('reference the specific design decision in Section X') prevents generic feedback. Asynchronous peer review produces equivalent analytical depth but lacks the real-time dialogue that live demo enables. |\n| **A12** | Diagnostic Analysis Using a Structured Rubric | L4 | Model diagnosis for one deficiency provided in Unit 5 feedback after submission — replicates the instructor-led debriefs misconception-correction function with a time delay. Students must not access this before submitting their own analysis. |\n| **A13** | Comparative Evaluation and Evidence Synthesis | L4 | Benchmark comparison is a partial substitute for peer data pooling — it provides comparison values without collaborative synthesis. Forum data-sharing approximates A13's small-group function over a longer time window. This is the most significant functional loss in the self-paced adaptation. |\n| **A14** | Failure Mode Diagnosis and Remediation Design | L4 | Word count per diagnostic step prevents superficial responses. The prediction requirement ('expected behavior after the fix') is the most important element — it forces forward-chaining reasoning rather than retrospective labeling. |\n| **A15** | Session Debrief and Misconception Correction | L1–L4 Cross-cutting | Advisory misconceptions must be anticipatory, not responsive — drawn from documented common errors in the content domain, not from observing the current cohort. This is a real limitation: live instructors detect misconceptions from student behavior that no asynchronous artifact reveals until after submission. |\n| **A16** | Synthesis Reflection and Self-Assessment | L1–L4 Cross-cutting | Making A16 a graded required section (not optional) is the critical design decision. Research on self-regulated learning predicts that time-pressured students will omit non-graded reflection tasks precisely when they are most needed — at the end of the most demanding unit. |",
    'ReAct-Phase': '| ReAct Phase | What Happens in This Phase |\n| --- | --- |\n| **THOUGHT** | The agent produces an internal reasoning step: what does it know, what does it need, what is its next action plan? This step is natural language — no tool is called. |\n| **ACT** | The agent issues a tool call — a web search, a calculator invocation, a database query, a file read. The action is specified using a structured format that the tool interface can parse. |\n| **OBSERVE** | The agent receives the tool output and incorporates it into its context. The observation becomes the input for the next Thought step, creating a closed reasoning-acting loop. |',
    'Reasoning-Trace-Failures': "| Failure Class | Diagnostic Signature | Structural Fix |\n| --- | --- | --- |\n| **Hallucinated Tool Call** | The agent calls a tool that does not exist or calls a real tool with an argument that is not valid per the tool description. The executor returns an error or unexpected output. | Revise the tool description to make the tool's name, purpose, and argument schema unambiguous. Add negative examples if the agent confuses this tool with another. |\n| **Premature Termination** | The agent produces a Final Answer token before completing the task — typically after a successful first tool call, incorrectly treating partial information as a complete answer. | Revise the system prompt to specify the termination condition explicitly. Add a rubric for what 'task complete' means in terms of observable outputs. |\n| **Observation Misinterpretation** | The agent receives a valid tool output but misreads it — extracts the wrong field from a JSON response, misinterprets a numeric value, or confuses an error string with a data string. | Revise the tool description to specify the output format precisely. Add parsing instructions to the system prompt if the output format is complex. |\n| **Infinite Loop** | The agent repeats the same tool call with the same or similar arguments across multiple iterations, never converging to a Final Answer. The observation does not resolve the agent's reasoning state. | Add a loop-detection stopping criterion. Revise the system prompt to specify what to do when a tool call does not resolve the current uncertainty. |\n| **Logical Gap in Reasoning Chain** | The agent's Thought step contains a reasoning error — an incorrect inference, a false premise, or a misattributed observation — that propagates into subsequent tool selection or argument construction. | Add few-shot examples that demonstrate correct reasoning for this problem type. Consider switching to a more powerful base model or a more deliberate architecture (ToT or LATS) for complex reasoning problems. |",
    'SIx-Functional-Stages-RAG': "**The Six Functional Stages of Every RAG Pipeline**\n\n| # | Stage | What Happens | Critical Design Decision and Downstream Consequence |\n| --- | --- | --- | --- |\n| 1 | **Document Ingestion** | Raw source documents (PDFs, web pages, databases, code files) are loaded into the pipeline using document loaders. Each loader parses the source format and extracts text content. | Document scope and quality directly determine what the system can know. Documents with poor formatting, ambiguous structure, or low information density degrade all subsequent stages. Garbage in, garbage out — at pipeline scale. |\n| 2 | **Text Splitting** | The extracted text is divided into smaller chunks using a text splitter. The chunk size and overlap parameters are configured at this stage. | Chunk size determines information granularity. Chunks too large: retrieval returns chunks with mostly irrelevant content alongside the target information (context noise). Chunks too small: a single complete idea is fragmented across multiple chunks, none of which is individually informative enough for generation. Overlap prevents sentence-boundary information loss. |\n| 3 | **Embedding Generation** | Each text chunk is converted into a dense vector representation — an embedding — by a pre-trained embedding model. Semantically similar chunks have embeddings that are geometrically close in the vector space. | The embedding model determines the semantic space in which retrieval operates. Models trained on general corpora (OpenAI Ada-002) may underperform in highly specialized domains (medical, legal, scientific) where domain-specific terminology carries high semantic load. Embedding dimensionality affects storage cost and retrieval speed. |\n| 4 | **Vector Store Indexing** | The embeddings are stored in a vector database (FAISS, Chroma, Pinecone) along with the original chunk text and metadata. The vector store builds an index that enables efficient approximate nearest-neighbor search. | The vector store choice involves trade-offs among query latency, scalability, cost, and persistence. FAISS is fast and local but not persistent across sessions. Chroma provides persistence with modest infrastructure. Pinecone provides managed cloud-scale retrieval. Metadata storage enables filtering (retrieve only documents from a specific date range, author, or category). |\n| 5 | **Similarity Retrieval** | At query time, the user's query is embedded using the same embedding model, and the vector store is searched for the k chunks with highest semantic similarity to the query embedding. MMR retrieval balances similarity with diversity to reduce redundancy. | The retrieval method (similarity vs. MMR) and the value of k determine context quality. Too few retrieved chunks: the answer may be incomplete. Too many: context window overflow and generation degradation. MMR is preferred when the corpus contains many near-duplicate or paraphrase chunks, as pure similarity retrieval would return a set of nearly identical chunks. |\n| 6 | **Augmented Generation** | The retrieved chunks are injected into the LLM's prompt as context, alongside the user's query. The LLM generates an answer grounded in the retrieved context. | The prompt template for context injection is a design artifact with significant impact on generation quality. The template must instruct the LLM to use only the provided context, to cite its source, and to acknowledge when the context does not contain sufficient information to answer the query — the 'I don't know' instruction that prevents hallucination when retrieval fails. |",
    'Six-Dimensions-Trade-Off_Assessment': "**The Six-Dimension Trade-off Assessment Framework**\n\n| Dimension | Assessment Questions | Architecture Implications |\n| --- | --- | --- |\n| **Task complexity** | How many sub-tasks are there, and how do they depend on each other? Does the task need backtracking — exploring alternatives and abandoning the ones that fail? | For structured, well-defined tasks, linear reasoning (CoT or ReAct) is typically sufficient. Open-ended or highly constrained tasks, where linear reasoning produces frequent errors, are where ToT and LATS earn their cost by branching and backtracking. |\n| **Inference cost** | What is the total token budget per query at the expected volume? Are per-query cost constraints strict? | CoT has the lowest cost. ReAct cost scales with the number of tool calls. ToT and LATS costs scale super-linearly with tree depth and branching factor. |\n| **Latency requirements** | What is the acceptable response time? Is the agent operating in a real-time, near-real-time, or batch context? | CoT and ReAct have lower latency than ToT and LATS. Branching search is inappropriate for real-time, user-facing applications. |\n| **External information needs** | Does the task need information that is not in the prompt — retrieval, lookups, live data — while it reasons? | If it does, CoT is ruled out: CoT reasons only over what is already in its context, and ReAct adds the ability to act and observe the result. If everything the task needs is in the prompt, tool calls add cost and failure points without adding information. |\n| **Interpretability requirements** | Must operators, auditors, or regulators be able to follow the reasoning? Does the EU AI Act's Article 13 apply? | CoT and ReAct traces are linear and comparatively easy to audit. ToT and LATS traces branch, so auditing them means logging the whole search tree, not only the path that was selected. |\n| **Deployment risk profile** | Is the domain high-risk — healthcare, legal, financial, employment — so that regulation such as EU AI Act Article 13 applies? Who is harmed if the agent is wrong? | A high-risk domain raises the bar for interpretability and review, but it does not by itself dictate a paradigm: a wrong answer from an easy-to-audit system is not safer than a correct answer from a harder-to-audit one. |\n\nTwo further considerations sit alongside the six. **Scalability:** stateless paradigms (CoT, ReAct) scale horizontally more easily than stateful ones (ToT, LATS), which need more sophisticated state-management infrastructure. **Organizational integration:** tool choices must fit the organization's data-governance policies, and ToT and LATS carry a heavier maintenance burden than CoT and ReAct.",
    'StandardActivityStructurePerModule': "| Self-Paced Structure | Bloom's Level | Primary Activities Translated |\n| --- | --- | --- |\n| Unit 1: Reading and Video 1.5 hours | L1 — Remember | A0 → structured reading with annotation protocol; instructor video introduction |\n| Unit 2: Concept Quiz 0.5 hours | L1–L2 | A1, A2 → formative quiz with explanatory feedback; concept map self-check |\n| Unit 3: Guided Labs 2.0 hours | L2–L3 | A3 → annotated reference notebook/video; A7 → scaffolded reference implementation; A8 → lab with verification checkpoints |\n| Unit 4: Hands-On Project 2.5 hours | L3–L4 | A9, A10 → open-specification project with experiment log; A12 → self-rubric analysis |\n| Unit 5: Case Study 1.0 hour | L4 — Analyze | A12, A14 → ill-structured diagnostic case with failure mode taxonomy |\n| Unit 6: Peer Discussion + Capstone 0.5h + Capstone | L4–L6 | A11, A13 → structured peer review rubric; A16 → required synthesis reflection in capstone |",
    'Three-Orchestration-Frameworks': '| Framework | Core Design Philosophy | Strengths | Limitations |\n| --- | --- | --- | --- |\n| **LangGraph** | Graph-based state machine: agents are nodes; state transitions are edges; shared state schema is typed and explicit. The supervisor-worker pattern is the primary multi-agent implementation. | Explicit state visibility; fine-grained control over coordination logic; full LangChain ecosystem integration; strong observability through LangSmith. | Higher implementation complexity; requires explicit state schema design; steeper learning curve than higher-level frameworks. |\n| **AutoGen (Wu et al., 2023)** | Conversation-based: agents interact through structured natural language conversations; an orchestrator agent manages the conversation flow. Peer collaboration is the primary pattern. | Flexible conversational coordination; easy to prototype with; supports human-in-the-loop participation through the human proxy agent pattern. | Less explicit state management than LangGraph; conversation history can grow large; harder to reason about system behavior from conversation logs. |\n| **CrewAI** | Role-and-process abstraction: agents are defined by role, goal, and backstory; tasks are assigned to specific agents; crews execute tasks in sequential or hierarchical processes. | High-level abstraction reduces implementation boilerplate; rapid prototyping of role-based pipelines; intuitive role specification for non-expert developers. | Lower-level control is limited; customization beyond built-in process types requires framework extensions; less suitable for complex conditional routing. |',
    'Three-RAG-Failure-Modes': "| Failure Mode | RAGAS Signature | Remediation Strategy |\n| --- | --- | --- |\n| **Hallucination** | Low Faithfulness; Answer Relevance may be moderate to high (the hallucinated answer addresses the question — it is just not supported by context) | Strengthen the 'grounded generation' instruction in the prompt template. Add explicit 'If the context does not contain sufficient information, state that you cannot answer.' Increase context coverage (higher k or improved retrieval precision). |\n| **Retrieval Failure** | Low Context Recall; Faithfulness may be high for what was retrieved but the answer is incomplete or incorrect because key information was not retrieved | Increase k. Review and revise chunking strategy to ensure relevant content is not fragmented. Check corpus coverage — the relevant documents may simply not be in the knowledge base. Consider query rewriting or decomposition to better match the query embedding to the relevant chunks. |\n| **Context Irrelevance / Overflow** | Low Context Precision; Faithfulness may be low or variable (the generator is working with noisy context); latency may be high due to large context payloads | Reduce k. Apply metadata filtering to restrict the retrieval search space. Switch from similarity search to MMR. Apply context compression (LLMLingua) to distill retrieved chunks before injection. |",
    'Three-RAG-Paradigms2': '**The Three RAG Paradigms (Gao et al., 2023)**\n\n**Naive RAG**\n\nThe straightforward implementation of the six-stage pipeline with fixed chunking, single-stage retrieval, and direct context injection. Naive RAG is appropriate for small, well-structured corpora where retrieval precision is naturally high, and context windows are not a bottleneck. Its primary failure modes are low retrieval precision (irrelevant chunks retrieved) and hallucination when retrieved context is insufficient.\n\n**Advanced RAG**\n\nIntroduces pre-retrieval optimizations (query rewriting, query decomposition, HyDE — Hypothetical Document Embedding) and post-retrieval optimizations (re-ranking, context compression, contextual compression using LLMLingua). Advanced RAG is appropriate when naive retrieval quality is insufficient — typically when the corpus is large, heterogeneous, or the user query is ambiguous or multi-part. It adds engineering complexity in exchange for higher retrieval precision.\n\n**Modular RAG**\n\nTreats each RAG stage as an independently configurable, swappable module. This architecture enables specialized retrievers (sparse BM25, dense vector, hybrid), routing between multiple knowledge sources, and integration of additional components such as re-rankers and knowledge graph augmentation. Modular RAG is the state of the art for production systems that must handle diverse query types and knowledge domains. Its engineering overhead is substantial.',
    'WorkflowAuditProject-Rubric': "| Criterion | Weight | 4 — Distinguished | 3 — Proficient | 2 — Developing |\n| --- | --- | --- | --- | --- |\n| Completeness (all required fields present for all 3 workflows) | 25% | All 15 fields complete with required specificity; all conditional branches identified | All 15 fields present; 1–2 missing conditional branches or incomplete time estimates | 1–2 fields missing or unacceptably vague ('uses email') across all workflows |\n| Accuracy and Specificity of Workflow Mapping | 25% | Each step specifies tool/system, input format, output format, and judgment indicator; workflows are from genuine practice and non-hypothetical | Steps specify tools but omit input/output format for 2–3 steps; one workflow may be partially generic | Steps name categories rather than specific tools; workflows appear hypothetical or generic |\n| Assessment Matrix Reasoning (Task 2) | 30% | Scores justified with ≥100 words each using ≥4 course terms; scoring formula applied correctly; lowest-ranked candidate identification persuasive | Justifications present but ≤80 words or missing ≥2 course terms; formula correct | Justifications vague or circular; formula misapplied; no lowest-candidate identification |\n| Paradigm Selection Reflection (Task 3) | 20% | 200-word reflection cites ≥2 diagram criteria by name; paradigm selection follows from workflow properties; one specific tool named with justification | Reflection present; ≥150 words; 1 criterion cited; tool named without justification | Reflection &lt;100 words; no diagram criteria cited; paradigm selection unsupported |",
    'WorkflowMapping-Template': "| Field | Specification Requirement |\n| --- | --- |\n| **Trigger** | What event initiates the workflow? Must be specific and external: an email arriving with a particular subject line or sender, a calendar event at a specific recurrence, a file appearing in a designated folder, or a recurring time. 'Someone sends me a request' is not a trigger. |\n| **Sequential Steps** | Minimum four steps. Each step must specify: (a) the specific tool or system touched (email client, CRM, spreadsheet software, file system — not 'the computer'); (b) the input format and output format at that step; and (c) whether any judgment is exercised at that step or whether it is fully mechanical. |\n| **Conditional Branches** | At least one 'if X, then Y; else Z' decision point in at least two of your three workflows. The condition must be statable as a rule: 'if the invoice amount exceeds $5,000, route to VP approval; else forward to accounts payable directly.' |\n| **Output** | The final deliverable or state change that signals the workflow is complete. Must be specific: 'a PDF report emailed to three recipients' not 'a report.' |\n| **Time Estimate** | How many minutes or hours this workflow currently takes per week, and how you derived that estimate (measurement, best estimate, or calculation). This becomes the ROI baseline for the automation assessment. |",
    'Workflow_Automation_Components': "| Component | Definition | Why It Matters for Automation |\n| --- | --- | --- |\n| **TRIGGER** | The specific event that initiates the workflow — a received email, a scheduled time, a form submission, a file upload | Agents must know exactly what starts them. Vague triggers produce agents that activate at the wrong time or not at all. |\n| **SEQUENTIAL STEPS** | The ordered set of actions the workflow executes — minimum four steps; each step must be atomic and non-ambiguous | Agents cannot execute ambiguous instructions. Each step must be specifiable precisely enough to be delegated. |\n| **TOOLS AND RESOURCES** | The systems, files, APIs, and data sources touched at each step — named specifically (e.g., 'Google Sheets API', not 'spreadsheet') | Tool identification directly maps to agent tool provisioning. Vague resource naming is a design error. |\n| **CONDITIONAL BRANCHES** | Decision points where the workflow splits based on evaluated conditions — the if/then logic that real processes always contain | Agents implement conditionals via routing logic. Undocumented branches produce agents that fail silently on edge cases. |\n| **ERROR HANDLING** | What happens when a step fails, returns unexpected output, or times out — the fallback logic | Production agents must handle failures gracefully. Workflows without error handling are prototype-grade, not production-grade. |\n| **OUTPUT** | The final deliverable of the workflow — specified precisely (file format, destination, recipient, content type) | Agents need a concrete termination condition. Undefined outputs produce agents that run indefinitely or terminate prematurely. |",
}

# The wiki opened most pages with an illustrated poster generated by NotebookLM. Where a
# page has a structure worth showing, the poster is replaced by one of these schematics,
# written from that page's own text; where it does not, the poster simply goes. Node labels
# stay short on purpose: long labels make the boxes overlap, and the explanation belongs in
# the sentence above the figure.
PAGE_DIAGRAMS: dict[str, str] = {
    'AI_Automation_Ecosystem|modules/module-1/readings/automation-and-multi-agent-frameworks.md': 'The page\'s roadmap runs Zapier to Make to n8n or CrewAI — Zapier\'s costs are the stated reason to leave it, and Stage 5+ is where data control and deep customization are mandatory.\n\n```mermaid\nflowchart LR\n  A["Stage 3 Zapier"] -- costs prohibitive --> B["Stage 4 Make"]\n  B -- need data control --> C["Stage 5+ Advanced"]\n  C --> D["n8n self-hosted"]\n  C --> E["CrewAI crews and flows"]\n```',
    'AI_Professional_Portfolio_Guide|start-here/github-portfolio-setup.md': 'Everything from the account through the module directories is the one-time Day 1 setup checklist; once the repository URL goes to the instructor, the loop at the bottom is the ongoing routine — at least one learning-log entry and at least two commits a week.\n\n```mermaid\nflowchart TD\n  A["GitHub account"] -- enable 2FA --> B["Public course repo"]\n  B --> C["Root README.md"]\n  C --> D["LEARNING_LOG.md"]\n  D --> E["Module directories"]\n  E -- share URL with instructor --> F["Add deliverables"]\n  F -- update module README --> G["Weekly log entry"]\n  G --> H["Commit changes"]\n  H -- at least twice weekly --> F\n```',
    'Architects-Guide-to-Agents|modules/module-2/foundational-concepts.md': 'Each paradigm answers a limitation of the one before it, gaining capability and cost together; ReAct remains the production default and LATS the high-cost frontier.\n\n```mermaid\nflowchart LR\n    COT["CoT"] -- no external information --> REACT["ReAct"]\n    REACT -- no backtracking --> TOT["Tree of Thoughts"]\n    TOT -- internal evaluation only --> LATS["LATS"]\n```',
    'Automation-Designers-LP|modules/module-1/activities.md': 'The Workflow Audit project runs as a pipeline: each mapped workflow is scored on two dimensions, and its automation potential is the rule-based score divided by (consequence severity + 1).\n\n```mermaid\nflowchart LR\n    W["Candidate workflows"] --> M["Workflow map"]\n    M --> R["Rule-based score"]\n    M --> C["Consequence severity"]\n    R --> P["Automation potential"]\n    C --> P\n    P -- highest score --> T["Top-ranked workflow"]\n    T --> D["Paradigm choice"]\n    T --> N["Module 2 build"]\n```',
    'Decoding_AI_Agents|modules/module-1/readings/what-is-an-agent.md': 'Section 1.3\'s ReAct loop runs Thought, Action and Observation until the model judges the observation sufficient to answer; the page maps those three phases onto deliberation, pro-activeness and perceiving the environment in classical agent theory.\n\n```mermaid\nflowchart TD\n    A["User query"] --> B["Thought"]\n    B -- selects a tool --> C["Action"]\n    C -- tool executes --> D["Observation"]\n    D -- model evaluates --> E{"Observation sufficient?"}\n    E -- no, new thought --> B\n    E -- yes --> F["Final answer"]\n```',
    'Mastering-Responsible-AgenticAI|modules/module-5/activities.md': 'The Module 5 activities in order, and the two channels their work is submitted through — note that the guided lab and the comparative study share one notebook, submitted to GitHub under the same filename.\n\n```mermaid\nflowchart TD\n    A["Self-check prompts"] -- ungraded --> B["Guided lab"]\n    B -- same notebook --> C["Comparative study"]\n    B --> G["One .ipynb to GitHub"]\n    C --> G\n    C --> D["Capstone post"]\n    D --> E["Peer reply"]\n    D --> L["LMS discussion thread"]\n    E --> L\n```',
    'Multi-Agent-Orchestration-Map|modules/module-4/activities.md': 'The guided lab builds this three-role pipeline in LangGraph; the hands-on project then rebuilds the same Researcher → Analyst → Critic roles in CrewAI, with the same topic, model, and quality criteria.\n\n```mermaid\nflowchart TD\n    TOPIC["Complex topic"] --> R["Researcher"]\n    R --> A["Analyst"]\n    A --> C["Critic"]\n    C --> GATE{"Quality gate"}\n    GATE -- pass --> OUT["Final output"]\n    GATE -- reject --> LIM{"Revision limit"}\n    LIM -- under cap --> A\n    LIM -- cap reached --> OUT\n```',
    'Path-to-AI-Memory|modules/module-3/activities.md': 'The four activities run in sequence — self-check prompts (~30 min), the guided RAG lab (~2 hrs), the four-run chunking experiment (~2 hrs), and the peer discussion (~60 min) — with the lab and experiment sharing one notebook and the experiment\'s results feeding the discussion post.\n\n```mermaid\nflowchart TD\n  A["Self-check prompts"] --> B["Guided RAG lab"]\n  B -- same notebook --> C["Four-run chunking experiment"]\n  C -- cite a run result --> D["Discussion post"]\n  D --> E["Peer reply"]\n  C -- completed notebook --> F["Submit to GitHub"]\n  D --> G["Submit to LMS"]\n  E --> G\n```',
    'Path-to-AI-Memory|modules/module-3/foundational-concepts.md': 'The six-stage RAG pipeline of Chapter 2, with three of Chapter 5\'s RAGAS metrics pointing back at the pipeline components each low score implicates.\n\n```mermaid\nflowchart TD\n    ING["Document ingestion"] --> SPL["Text splitting"]\n    SPL --> EMB["Embedding generation"]\n    EMB --> IDX["Vector store indexing"]\n    IDX --> RET["Similarity retrieval"]\n    QRY["User query"] --> RET\n    RET --> GEN["Augmented generation"]\n    GEN --> EVAL["RAGAS evaluation"]\n    EVAL -- low faithfulness --> GEN\n    EVAL -- low context precision --> RET\n    EVAL -- low context recall --> RET\n    EVAL -- low context recall --> SPL\n```',
    'ResponsibleAgenticAIControl|modules/module-5/overview.md': 'Module 5 adds four areas to the notebook agents built earlier in the course, and the capstone folds all four into a single deployment plan.\n\n```mermaid\nflowchart TD\n  P["Notebook prototype"] --> E["Evaluation"]\n  P --> O["Observability"]\n  P --> S["Security"]\n  P --> G["Governance"]\n  E --> C["Responsible deployment plan"]\n  O --> C\n  S --> C\n  G --> C\n```',
    'The_New_Frontier|modules/module-1/foundational-concepts.md': 'The four-stage agent loop that Chapter 1 defines, and the point at which the agent exits it.\n\n```mermaid\nflowchart TD\n    A["Perceive"] -- environment state --> B["Plan"]\n    B -- chosen action --> C["Act"]\n    C -- tool output --> D["Observe"]\n    D -- updated state --> E{"Task complete?"}\n    E -- no --> A\n    E -- yes --> F["Conclude"]\n```',
    'Visual_vs_Programmatic|modules/module-1/resources.md': 'n8n and LangChain sit one step apart on the same spectrum, which runs from visual builders to fully programmable environments and trades accessibility away for flexibility, cost efficiency at scale, and data governance as you move right.\n\n```mermaid\nflowchart LR\n    NC["No-code: n8n"] -- more flexibility and lower cost --> LC["Low-code: LangChain, CrewAI"]\n    LC -- full control and data governance --> CF["Code-first: Claude Code"]\n```',
}

PATCHES: dict[str, list[tuple[str, str]]] = {
    "modules/module-3/foundational-concepts.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Path-to-AI-Memory.png" width=900>',
         PAGE_DIAGRAMS['Path-to-AI-Memory|modules/module-3/foundational-concepts.md']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Chunking-Strategy-Selection.png" width=800>',
         IMAGE_TABLES['Chunking-Strategy-Selection']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Four-RAGAS-Metrics.png" width=800>',
         IMAGE_TABLES['Four-RAGAS-Metrics']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/SIx-Functional-Stages-RAG.png" width=800>',
         IMAGE_TABLES['SIx-Functional-Stages-RAG']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Three-RAG-Failure-Modes.png" width=800>',
         IMAGE_TABLES['Three-RAG-Failure-Modes']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Three-RAG-Paradigms2.png" width=800>',
         IMAGE_TABLES['Three-RAG-Paradigms2']),
        # Last live student-facing reference to RetrievalQA as current LangChain documentation.
        # The URL already points at the retrievers integrations page, so only the label was wrong.
        ("[RetrievalQA](https://docs.langchain.com/oss/python/integrations/retrievers)",
         "[Retrievers](https://docs.langchain.com/oss/python/integrations/retrievers)"),
    ],
    "modules/module-1/foundational-concepts.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/The_New_Frontier.png" width=900>',
         PAGE_DIAGRAMS['The_New_Frontier|modules/module-1/foundational-concepts.md']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Automation_Tools.png" width=800>',
         IMAGE_TABLES['Automation_Tools']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Critical_Distinctions.png" width=800>',
         IMAGE_TABLES['Critical_Distinctions']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Four_Stage_Agent_Loop.png" width=800>',
         IMAGE_TABLES['Four_Stage_Agent_Loop']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Workflow_Automation_Components.png" width=800>',
         IMAGE_TABLES['Workflow_Automation_Components']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Four_PIllars_AI_Literacy.png" width=800>',
         IMAGE_TABLES['Four_PIllars_AI_Literacy']),
        ("* Merrill, M. D. (2002). [First principles of instruction](https://link.springer.com/content/pdf/10.1007/bf02505024.pdf). Educational technology research and development, 50(3), 43-59 (**👁️‍🗨️ 👁️‍🗨️ 👁️‍🗨️ Remove this source - not related to course**)\n", ""),
        ("* Wiggins, G. P., & McTighe, J. (2005). [Understanding by design](https://pdfs.semanticscholar.org/03e8/20730a873e7f44dbb1f64e4f047b9b321460.pdf). Ascd (**👁️‍🗨️ 👁️‍🗨️ 👁️‍🗨️ Remove this source - not related to course**)\n", ""),
        ("### Three Automation Paradigms:", "**Three automation paradigms**\n"),
    ],
    "modules/module-1/activities.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Automation-Designers-LP.png" width=900>',
         PAGE_DIAGRAMS['Automation-Designers-LP|modules/module-1/activities.md']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/2D-Automation-AssessmentMatrix.png" width=700>',
         IMAGE_TABLES['2D-Automation-AssessmentMatrix']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/WorkflowAuditProject-Rubric.png" width=700>',
         IMAGE_TABLES['WorkflowAuditProject-Rubric']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/WorkflowMapping-Template.png" width=700>',
         IMAGE_TABLES['WorkflowMapping-Template']),
        ("### a. Self-Check Prompts", "## a. Self-Check Prompts"),
        # Module 2 builds a LangChain agent, not a no-code Openwork or n8n pipeline.
        ('Module 2 begins with your top-ranked workflow from the Workflow Audit. You will build your first no-code automation pipeline using Openwork or n8n applied to that workflow. Ensure your Workflow Audit document is complete before starting — it is the anchor for all subsequent module projects.',
         'Module 2 moves from mapping workflows to building agents: you will build a tool-using agent in LangChain, and its hands-on project asks you to add a tool that could support a workflow from your own work. Your top-ranked workflow from the Workflow Audit is the natural candidate, so make sure the audit is complete before you start — it is the anchor for all subsequent module projects.'),
    ],
    "modules/module-2/activities.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Journey-to-AI-Agency.png" width=900>',
         ''),
        ("👁️‍🗨️ (Write language about providing thoughtful feedback to two peers on their proposals)",
         "!!! warning \"Under construction\"\n\n    Guidance on giving thoughtful feedback to two peers on their proposals is still being written."),
        # A 2026-08-03 wiki edit turned Module2_Project_[YourName] into Module2__[YourName] and left the lab box's
        # "all four steps" text in place. As in Modules 4 and 5, the project continues in the lab notebook.
        ('Submit the `.ipynb` file with your completed extension code (all four steps). All cells must be executed with output visible — do not submit a notebook with empty output cells. Filename: `Module2__[YourName].ipynb`.',
         'Submit the lab notebook with your new tool added: its definition and description, the three test prompts run with output visible, and your before-and-after comparison. The project has its own section at the end of the lab notebook, so the filename is the same: `Module2_Lab_[YourName].ipynb`.'),
    ],
    "modules/module-2/chapter-quizzes.md": [
        ("C. The student is partially correct — in LangChain's AgentExecutor implementation, the LLM generates both the Action and the Observation, while the tool executor only validates that the Action is syntactically correct.",
         "C. The student is partially correct — in LangChain's `create_agent` runtime, the model generates both the Action and the Observation, and the runtime only checks that the tool name the model asked for exists in the tool registry."),
        ("> ❌ **C is incorrect.** In LangChain's AgentExecutor, the LLM generates the `Action:` and `Action Input:` (the tool name and arguments), and the tool executor invokes the actual tool and returns its output as the `Observation:`. The LLM does not generate the Observation content. The output parser converts the LLM's text to a structured tool call — it does not validate the Action alone and leave Observation generation to the LLM.",
         '> ❌ **C is incorrect.** In an agent built with `create_agent`, the model\'s message carries the Action as a structured tool call — `tool_call["name"]` is the tool and `tool_call["args"]` are its arguments — and the agent\'s action executor then invokes that tool and returns its output as a `ToolMessage`. The content of that `ToolMessage` is the Observation, and the model does not generate it. The runtime also does more than check the name: it executes the call and feeds the result back into the loop as the model\'s next input.'),
        ("> ❌ **D is incorrect.** When the tool is a Python REPL, the LLM generates the *code to execute* (the `Action Input:`) — not the Observation. The Observation is the output produced by the Python interpreter when it runs the LLM-generated code. The tool (the REPL) generates the Observation; the LLM generates the code that produces it. This distinction is not tool-type-specific — across all tool types, the Observation is the tool's output, not the LLM's.",
         "> ❌ **D is incorrect.** When the tool is a Python REPL, the LLM generates the *code to execute* (the `args` of its tool call) — not the Observation. The Observation is the output produced by the Python interpreter when it runs the LLM-generated code, handed back to the model as a `ToolMessage`. The tool (the REPL) generates the Observation; the LLM generates the code that produces it. This distinction is not tool-type-specific — across all tool types, the Observation is the tool's output, not the LLM's."),
        ('> ❌ **B is incorrect.** ReAct is fully capable of production API integration — the AgentExecutor architecture with a tool registry is exactly the mechanism designed for this. LATS\'s action-observation-at-node structure adds deliberate search capability that this task does not require. The claim that "ReAct is insufficient for production API integration" is factually incorrect; ReAct is the standard production architecture for tool-calling agents and is used at scale in exactly this type of deployment.',
         '> ❌ **B is incorrect.** ReAct is fully capable of production API integration — an agent runtime such as the one `create_agent` builds, backed by a tool registry, is exactly the mechanism designed for this. LATS\'s action-observation-at-node structure adds deliberate search capability that this task does not require. The claim that "ReAct is insufficient for production API integration" is factually incorrect; ReAct is the standard production architecture for tool-calling agents and is used at scale in exactly this type of deployment.'),
        ('*Based on Reading Guide 2: LangChain AgentExecutor Documentation, Tool Creation Reference, Chapter 2 Lesson*',
         "*Based on Reading Guide 2: LangChain Agents Documentation (`create_agent`) and Tools reference, the agent trace printed by the lab's `show_trace` helper, Chapter 2 Lesson*"),
        ('**Question 1.** The AgentExecutor architecture has five structural components. During a single reasoning loop, an agent generates the Action: `web_search` with Action Input: `"current Bitcoin price"`. The tool registry is queried and the tool is invoked. Which component is responsible for converting the LLM\'s raw text output (which reads: `"Action: web_search\\nAction Input: current Bitcoin price"`) into the structured Python object that can actually call the web search function?\n\nA. The memory module — it stores the previous Thought step and converts subsequent Action text into executable format by referencing the prior conversation turn.\n\nB. The output parser — it parses the LLM\'s raw text Action specification into a structured object (tool name as a string matching a registry entry + arguments in the expected format) that the action executor can then invoke against the tool registry.\n\nC. The tool registry — it receives the raw LLM text, looks up "web_search" in its directory, and automatically extracts the action input by pattern matching against the tool\'s argument schema.\n\nD. The LLM backbone — it generates both the raw Action text and its structured equivalent simultaneously; the AgentExecutor uses the structured version and discards the text representation.',
         "**Question 1.** An agent built with `create_agent` has four structural components. Asked for the current Bitcoin price, the agent is run with the lab's `show_trace` helper, which prints:\n\n```\n[1] TOOL CALL:  web_search\n[1] ARGUMENTS:  {'query': 'current Bitcoin price'}\n[1] OBSERVATION: BTC/USD 64,812.40 as of 14:02 UTC\n[final] ANSWER:  Bitcoin is trading at $64,812.40 as of 14:02 UTC.\n```\n\nThe `TOOL CALL:` and `ARGUMENTS:` lines are the model's *request*; the `OBSERVATION:` line shows that the registered `web_search` function actually ran. Which of the four components turns that request into that execution?\n\nA. The memory module — it holds the earlier steps of the run and converts the pending tool request into an executable call by referencing the prior conversation turn.\n\nB. The action executor — it reads the tool call's `name`, resolves it against the tool registry the agent was built with, invokes the underlying Python function with the `args` the model supplied, and returns what comes back as the tool result shown on the `OBSERVATION:` line.\n\nC. The tool registry — it receives the model's message directly, matches `web_search` against its entries, and runs the matching function as part of the lookup.\n\nD. The LLM backbone — a tool-calling model's message carries both the call and the tool's result, so no separate runtime step has to run anything; the `OBSERVATION:` line is the trace re-printing output the model already supplied."),
        ('> ✅ **B is correct.** The output parser is the structural component whose specific function is converting the LLM\'s natural language text output into a typed, executable format. The LLM generates the Action as natural language text — a string that looks like a tool call but is not yet a function call. The output parser performs this text-to-structure conversion: it extracts the tool name (matching it against the registry\'s known names), extracts the action input arguments, and produces a structured object that the action executor can pass to the actual tool function. Without the output parser, the gap between "the LLM\'s text response" and "an executable function call" cannot be bridged. The Reading Guide identifies this as one of the five named structural components with this specific function.\n>\n> ❌ **A is incorrect.** The memory module stores prior Thought/Action/Observation turns to provide context for subsequent reasoning steps — it does not perform text-to-structure conversion of Action specifications. The memory module\'s function is context management across turns, not parsing of individual action outputs.\n>\n> ❌ **C is incorrect.** The tool registry is a directory that maps tool names to tool objects (descriptions + callable functions) — it does not receive raw LLM text or perform pattern matching against it. The registry is passive: it is queried by the action executor after the output parser has already produced a structured tool call specifying which tool to invoke. The registry does not parse; it stores and retrieves.\n>\n> ❌ **D is incorrect.** The LLM backbone generates natural language text — it produces one representation (the text), not two simultaneous representations. LLMs do not natively output typed Python objects; the conversion from text to structured format is performed by a separate component (the output parser) external to the LLM itself. This separation is architecturally significant: it means the output parser can be swapped or upgraded independently of the LLM.',
         '> ✅ **B is correct.** The action executor is the component that turns a request into an execution. The LLM backbone\'s work ends when it emits a message carrying a tool call: a `name` and an `args` dictionary. That is a request — nothing has run yet. The action executor takes `tool_call["name"]`, resolves it against the tool registry the agent was built with, invokes the underlying Python function with `tool_call["args"]`, and hands the result back into the loop, where it prints as the `OBSERVATION:` line and becomes the model\'s input for its next step. The other three components do adjacent jobs and not this one: the backbone decides, the registry supplies the callable and the description the model reads when choosing, and the memory module carries the accumulated history forward. Note what is no longer in this division of labour: the component an older text-based agent needed between the model and the executor — an output parser that turned the model\'s `Action:` text into a call — has no work left to do, because a tool-calling model emits the structured `name`/`args` pair directly.\n>\n> ❌ **A is incorrect.** The memory module carries the conversation history, tool calls and tool results forward so that each model step sees what came before — it is context, not execution. It never converts a pending tool request into a function call, and an agent that persists no history at all still executes tools normally. Assigning this work to the memory module confuses what the loop remembers with what the loop does.\n>\n> ❌ **C is incorrect.** The tool registry is the set of tools the agent was built with: it maps a tool name to a callable and to the description the model reads when choosing. It is passive — it does not receive the model\'s message and it does not run anything. It is consulted *by* the action executor, which performs the lookup and then the invocation. The registry stores and resolves; it does not execute.\n>\n> ❌ **D is incorrect.** A tool-calling model emits one thing, the request: its message carries `tool_calls` entries and no tool output. The result arrives afterwards, from a different component, which is why the `OBSERVATION:` line is a separate step in the trace rather than part of the model\'s message. The model has no access to the process that runs the tool. This separation is architecturally significant: tool execution can be logged, sandboxed, rate-limited or refused independently of the model that asked for it.'),
        ('> ❌ **D is incorrect.** In the AgentExecutor architecture, tool descriptions are provided to the LLM during tool selection — the LLM reads the descriptions from the tool registry to determine which tool is appropriate. A meta-description in the system instruction is a complementary practice (listing available tools at a high level) but it does not replace individual tool descriptions; both are used. The claim that "individual tool descriptions alone are not read by the LLM during tool selection" is factually incorrect.',
         '> ❌ **D is incorrect.** Tool descriptions are sent to the model with every request — each `@tool` function\'s docstring (or the explicit `description=` it was given) becomes the text the model reads when deciding which tool is appropriate. A meta-description in the system instruction is a complementary practice (listing available tools at a high level) but it does not replace individual tool descriptions; both are used. The claim that "individual tool descriptions alone are not read by the LLM during tool selection" is factually incorrect.'),
        ('**Question 5.** The chapter lesson states that "undocumented errors produce agents that silently misinterpret failure states as data." A web search tool returns the error message `{"error": "RATE_LIMIT_EXCEEDED", "retry_after": 30}` — a rate limiting error the tool description does not mention. The ReAct agent reads this as an Observation and generates the Thought: "The search results show that RATE_LIMIT_EXCEEDED is the current status of the query. The retry delay of 30 seconds suggests the topic has limited available sources." The agent then generates a Final Answer based on this misinterpretation. Which failure mechanism does this scenario most precisely instantiate?',
         '**Question 5.** The chapter lesson states that "undocumented errors produce agents that silently misinterpret failure states as data." A web search tool returns the error message `{"error": "RATE_LIMIT_EXCEEDED", "retry_after": 30}` — a rate limiting error the tool description does not mention. The agent receives this string as the content of the `ToolMessage`, and its next message carries no tool call, so it ends the run: it reasons "The search results show that RATE_LIMIT_EXCEEDED is the current status of the query. The retry delay of 30 seconds suggests the topic has limited available sources," and on that basis gives its final answer. Which failure mechanism does this scenario most precisely instantiate?'),
        ('B. Observation misinterpretation caused by undocumented error state — the agent received a structured error response (not data), but without documentation specifying that `RATE_LIMIT_EXCEEDED` is an error state requiring a wait-and-retry action (not information to reason about), the agent treated the error JSON as semantic content and generated a factually incorrect Final Answer.',
         'B. Observation misinterpretation caused by undocumented error state — the agent received a structured error response (not data), but without documentation specifying that `RATE_LIMIT_EXCEEDED` is an error state requiring a wait-and-retry action (not information to reason about), the agent treated the error JSON as semantic content and produced a factually incorrect final answer.'),
        ('C. Hallucination in Thought — the agent invented the interpretation "limited available sources" from parametric memory rather than from the Observation, demonstrating that the model inserted training knowledge to fill an information gap.',
         'C. Hallucination in Thought — the agent invented the interpretation "limited available sources" from parametric memory rather than from the tool result, demonstrating that the model inserted training knowledge to fill an information gap.'),
        ('D. Premature termination — the agent generated a Final Answer after a single tool call that returned incomplete information, rather than retrying the search after the rate limit expired.',
         'D. Premature termination — the agent returned a final answer after a single tool call that came back with incomplete information, rather than retrying the search after the rate limit expired.'),
        ('> ❌ **C is incorrect.** The agent\'s interpretation ("limited available sources") is derived from the Observation content — it reads the field values from the JSON error and constructs a semantically plausible (but wrong) interpretation of them. This is not parametric memory insertion in the hallucination sense; the agent is actively reasoning about what it received. The failure is that what it received was an error, not data — a distinction it cannot make without error state documentation.',
         '> ❌ **C is incorrect.** The agent\'s interpretation ("limited available sources") is derived from the tool result\'s content — it reads the field values from the JSON error and constructs a semantically plausible (but wrong) interpretation of them. This is not parametric memory insertion in the hallucination sense; the agent is actively reasoning about what it received. The failure is that what it received was an error, not data — a distinction it cannot make without error state documentation.'),
        ('> ❌ **D is incorrect.** Premature termination is a distinct failure class where the agent generates a Final Answer before sufficient information has been gathered. In this scenario, the agent does generate a Final Answer — but the reason is not that it stopped too early; it is that it misinterpreted the error response as data and believed it had sufficient information. The agent completed its reasoning loop with a malformed input; premature termination implies the loop ended correctly but with an insufficient number of iterations.',
         '> ❌ **D is incorrect.** Premature termination is a distinct failure class where the agent returns a final answer before sufficient information has been gathered. In this scenario, the agent does return a final answer — but the reason is not that it stopped too early; it is that it misinterpreted the error response as data and believed it had sufficient information. The run ending here is not the tell for this class: a run that finishes normally always ends with a model message carrying no tool call, because a message with no tool calls is what terminates the loop. Premature termination means stopping before enough had been gathered; here the agent did gather a tool result and misread it. The fixes differ accordingly: premature termination is answered by demonstrating multi-step loops, this failure by documenting the error state in the tool description.'),
        ('> ✅ **B is correct.** This scenario precisely instantiates the "undocumented error produces silent misinterpretation" failure described in the chapter lesson and Reading Guide 2. The error state `RATE_LIMIT_EXCEEDED` is a control signal — it tells the system to wait and retry, not to reason about the content. But because the tool description does not document this error state (what it means, and what the agent should do when it receives it), the agent has no basis for distinguishing it from a valid data Observation. The agent treats the JSON error response as semantic content and extracts meaning from its fields (`RATE_LIMIT_EXCEEDED` → "limited available sources"; `retry_after: 30` → "30 seconds suggests limited sources"). The final answer is factually wrong, but the trace appears complete — no parsing errors, no missing Observations, all labels present. This is the silent misinterpretation failure: the trace looks correct, but the agent built its answer on an error message. The fix is to document the error state in the tool description and specify the required agent response (wait retry_after seconds, then re-invoke the tool).',
         '> ✅ **B is correct.** This scenario precisely instantiates the "undocumented error produces silent misinterpretation" failure described in the chapter lesson and Reading Guide 2. The error state `RATE_LIMIT_EXCEEDED` is a control signal — it tells the system to wait and retry, not to reason about the content. But because the tool description does not document this error state (what it means, and what the agent should do when it receives it), the agent has no basis for distinguishing it from a valid data result: both arrive as the content of a `ToolMessage`, and both are just text to the model. The agent treats the JSON error response as semantic content and extracts meaning from its fields (`RATE_LIMIT_EXCEEDED` → "limited available sources"; `retry_after: 30` → "30 seconds suggests limited sources"). The final answer is factually wrong, but the run itself looks healthy — no exception was raised, no step is missing, the tool was called and answered. This is the silent misinterpretation failure: the trace looks correct, but the agent built its answer on an error message. The fix is to document the error state in the tool description and specify the required agent response (wait retry_after seconds, then re-invoke the tool).'),
        ('*Based on Reading Guide 3: Yao et al. (2022) ReAct, AgentExecutor verbose output, Chapter 3 lesson (Five Failure Classes)*',
         "*Based on Reading Guide 3: Yao et al. (2022) ReAct, the agent trace printed by the lab's `show_trace` helper, Chapter 3 lesson (Five Failure Classes)*"),
        ("**Question 1.** A verbose AgentExecutor log contains the following sequence:\n\n```\nThought: I need to find the population of Tokyo.\nAction: calculator\nAction Input: Tokyo population\nObservation: Error: invalid expression — 'Tokyo population' is not a mathematical expression.\nThought: The calculator returned an error. The population of Tokyo is approximately 13.96 million based on my knowledge.\nFinal Answer: Tokyo's population is approximately 13.96 million.\n```",
         "**Question 1.** An agent is run with the lab's `show_trace` helper, which prints each step of the loop as it happens. The trace reads:\n\n```\n[1] REASONING:  I need to find the population of Tokyo.\n[1] TOOL CALL:  calculator\n[1] ARGUMENTS:  {'expression': 'Tokyo population'}\n[1] OBSERVATION: Error: invalid expression — 'Tokyo population' is not a mathematical expression.\n[final] ANSWER:  The calculator could not evaluate that. Tokyo's population is approximately 13.96 million based on my knowledge.\n```"),
        ('C. Hallucination in Thought — after the calculator error, the agent inserted a population figure from parametric memory (not from any Observation) as if it were retrieved information; the combined failure involves both incorrect tool selection (root cause) and hallucination in Thought (secondary consequence).',
         'C. Hallucination in Thought — after the calculator error, the agent inserted a population figure from parametric memory (not from any tool result) as if it were retrieved information; the fix is a system-prompt rule that forbids stating any figure no tool returned.'),
        ('> ✅ **B is correct** as the primary failure class (with C describing the secondary consequence). The root failure is incorrect tool selection: the agent invoked the calculator tool for a factual population lookup — a task for which web search is the appropriate tool. The calculator\'s scope boundary ("Use for mathematical calculations") is apparently either missing or insufficiently explicit, because the agent attempted to use it as a general-purpose information retrieval tool. The structural fix is to add an explicit "Do not use for..." clause to the calculator tool description: "Do not use this tool for factual lookups, demographic data, geographic information, or any query that is not a mathematical expression." This prevents the initial incorrect selection. The hallucination in the second Thought is a secondary consequence — once the agent\'s only invoked tool failed, it fell back on parametric memory. Fixing the tool selection failure (by providing a web search tool with a clear scope) removes the scenario that led to the hallucination.',
         '> ✅ **B is correct** as the primary failure class (with C describing the secondary consequence). The root failure is incorrect tool selection: the agent invoked the calculator tool for a factual population lookup — a task for which web search is the appropriate tool. The calculator\'s scope boundary ("Use for mathematical calculations") is apparently either missing or insufficiently explicit, because the agent attempted to use it as a general-purpose information retrieval tool. The structural fix is to add an explicit "Do not use for..." clause to the calculator tool description: "Do not use this tool for factual lookups, demographic data, geographic information, or any query that is not a mathematical expression." This prevents the initial incorrect selection. The hallucinated figure in the final message is a secondary consequence — once the agent\'s only invoked tool failed, it fell back on parametric memory. Fixing the tool selection failure (by providing a web search tool with a clear scope) removes the scenario that led to the hallucination.'),
        ('> ❌ **A is incorrect.** The agent does correctly read the error message — it acknowledges "the calculator returned an error." The failure is not in misinterpreting the error; it is in: (1) selecting the wrong tool initially, and (2) falling back on parametric memory rather than retrying with a correct tool. Observation misinterpretation applies when a valid tool output is misread, not when an error is correctly acknowledged.',
         '> ❌ **A is incorrect.** The agent does correctly read the error message — its final message opens by acknowledging that "the calculator could not evaluate that." The failure is not in misinterpreting the error; it is in: (1) selecting the wrong tool initially, and (2) falling back on parametric memory rather than retrying with a correct tool. Observation misinterpretation applies when a valid tool result is misread, not when an error is correctly acknowledged.'),
        ('> ❌ **C is partially correct** but incomplete as a primary classification. The hallucination in Thought is real — the agent inserts a specific figure (13.96 million) not grounded in any Observation. However, Reading Guide 3 structures the five failure classes by root cause, and the root cause here is incorrect tool selection, not hallucination. Identifying the root cause is what enables the structural fix — and fixing tool selection (providing a web search option with clear scope) resolves both failures simultaneously.',
         '> ❌ **C is incorrect.** It names the symptom, not the root cause. The hallucination is real — the agent asserts a specific figure (13.96 million) that no tool result contained. However, Reading Guide 3 structures the five failure classes by root cause, and the root cause here is incorrect tool selection. A prompt rule against unsupported figures treats only the symptom: the agent would still send a population lookup to the calculator, and would now reply that it could not find the figure. Fixing tool selection — a web search tool with a clear scope, and a calculator description that says what it is not for — resolves both failures at once.'),
        ('> ❌ **D is incorrect.** Premature termination applies when the agent generates a Final Answer without having gathered sufficient information — but in this trace, the agent believes it has sufficient information (from its parametric memory) and generates a semantically complete Final Answer. The failure is not that the loop ended too soon; it is that the agent substituted hallucinated content for retrieved content after the tool failure. These are distinct failure mechanisms with different fixes.',
         '> ❌ **D is incorrect.** Premature termination means the loop stopped while the task still needed another tool call, and the test for it is whether letting the loop run longer would fix the answer. Here it would not: raising the `recursion_limit`, or adding demonstrations of multi-step reasoning, gives the agent more steps, not a better tool choice — and the calculator would still reject `Tokyo population`. The stopping condition is not where this failure lives — the tool choice upstream of it is. Nor is the shape of the ending a tell: a run that finishes normally always ends with a model message that carries no tool call, so answering after a single tool call is not by itself premature termination. The agent here believes it has sufficient information (from its parametric memory) and returns a semantically complete answer; what it actually did was substitute hallucinated content for retrieved content after the tool failed. These are distinct failure mechanisms with different fixes.'),
        ('**Question 2.** Reading Guide 3\'s synthesis task presents an abbreviated trace in which the agent reports Brazil\'s 2023 inflation rate (4.6%) in the Final Answer, despite that figure never appearing in any Observation. A student\'s analysis states: "This is a hallucination in Thought. The agent inserted a numerical value from parametric memory and attributed it to the search results without verifying it." Which assessment of this analysis is most precise?',
         '**Question 2.** Reading Guide 3\'s synthesis task presents an abbreviated trace in which the agent reports Brazil\'s 2023 inflation rate (4.6%) in its final answer, despite that figure never appearing in any tool result. A student\'s analysis states: "This is a hallucination in Thought. The agent inserted a numerical value from parametric memory and stated it in the same answer as the retrieved GDP figure, though no tool returned it." Which assessment of this analysis is most precise?'),
        ('A. The analysis is incorrect — because the web search Observation is present in the trace, any additional factual claim the agent makes in its Thought must be derived from that Observation; the agent cannot insert parametric knowledge when an Observation is already present.',
         'A. The analysis is incorrect — because the web search result is present in the trace, any additional factual claim the agent makes must be derived from it; the agent cannot insert parametric knowledge once a tool has returned something.'),
        ('B. The analysis is correct and complete: it correctly identifies the failure class (hallucination in Thought), the mechanism (parametric memory insertion into a Thought step as if it were retrieved), and the evidence (the inflation rate appears in the Final Answer but not in any Observation). The prescribed fix — a system instruction requiring all numerical claims to be grounded in a tool Observation — directly addresses the root cause.',
         'B. The analysis is correct and complete: it correctly identifies the failure class (hallucination in Thought), the mechanism (parametric memory presented alongside retrieved data in the same answer, without a tool having supplied it), and the evidence (the inflation rate appears in the final answer but in no tool result). The prescribed fix — a system instruction requiring all numerical claims to be grounded in a tool result — directly addresses the root cause.'),
        ('C. The analysis correctly identifies the failure class but prescribes the wrong fix: the correct fix is to add an Observation that explicitly states "No inflation rate data was found" so the agent cannot claim retrieval of the figure.',
         'C. The analysis correctly identifies the failure class but prescribes the wrong fix: the correct fix is to have the search tool return "No inflation rate data was found" so the agent cannot claim retrieval of the figure.'),
        ('D. The analysis is partially correct: the failure is hallucination in Thought, but the cause is premature termination — the agent terminated before retrieving the inflation rate, forcing it to hallucinate. The fix is to increase max_iterations so the agent makes a second search call.',
         "D. The analysis is partially correct: the failure is hallucination in Thought, but the cause is premature termination — the agent terminated before retrieving the inflation rate, forcing it to hallucinate. The fix is to raise the run's `recursion_limit` so the agent makes a second search call."),
        ("> ✅ **B is correct.** The Reading Guide provides this trace as the synthesis task's target analysis, including the answer key: the failure is hallucination in Thought (the inflation rate 4.6% was never returned by any Observation, but the agent states it in a Thought step as established context), and the fix is a system instruction requiring numerical claims to be grounded in an Observation. The student's analysis correctly identifies all three elements: the failure class, the mechanism, and the evidence. The fix is also correct: requiring explicit Observation grounding prevents the agent from asserting parametric facts as if they were retrieved — it must cite an Observation or invoke a tool to retrieve the missing data.",
         '> ✅ **B is correct.** The Reading Guide provides this trace as the synthesis task\'s target analysis, including the answer key: the failure is hallucination in Thought (the inflation rate 4.6% was never returned by any tool, but the agent states it in the same answer as the retrieved GDP figure), and the fix is a system instruction requiring numerical claims to be grounded in a tool result. The student\'s analysis correctly identifies all three elements: the failure class, the mechanism, and the evidence. The agent\'s own hedge — "From what I know" — does not rescue the answer: the figure is still asserted next to retrieved data with no tool result behind it, and a reader who is not holding the trace cannot tell the two apart. The fix is also correct: requiring explicit grounding stops the agent from mixing parametric facts into an answer built from tool results — it must point to a tool result or invoke a tool to retrieve the missing data.'),
        ('> ❌ **A is incorrect.** The presence of an Observation in the trace does not prevent the agent from inserting additional claims from parametric memory. LLMs do not automatically switch off their parametric knowledge when an Observation is present — they combine retrieved information and stored knowledge in their generation, sometimes without distinguishing between sources. This is precisely why the hallucination in Thought failure class exists: the trace contains a valid Observation, but the agent goes beyond it to assert additional facts not grounded in any retrieval.',
         '> ❌ **A is incorrect.** The presence of a tool result in the trace does not prevent the agent from inserting additional claims from parametric memory. LLMs do not automatically switch off their parametric knowledge when a `ToolMessage` is in the context — they combine retrieved information and stored knowledge in their generation, sometimes without distinguishing between sources. This is precisely why the hallucination in Thought failure class exists: the trace contains a valid tool result, but the agent goes beyond it to assert additional facts grounded in nothing.'),
        ('> ❌ **C is incorrect.** Adding an Observation that says "No inflation rate data was found" would require the agent to have made a tool call specifically for inflation rate data — which the trace shows it did not do. The fix prescribed in the Reading Guide (a system instruction) prevents the agent from asserting unretrieved facts in the first place; it does not depend on modifying the tool\'s output. The suggested fix in C is also circular: it requires the agent to know it should search for inflation rate data, which is the behavior the system instruction would produce.',
         '> ❌ **C is incorrect.** Having the tool return "No inflation rate data was found" would require the agent to have called it for inflation rate data — which the trace shows it did not do. The fix prescribed in the Reading Guide (a system instruction) prevents the agent from asserting unretrieved facts in the first place; it does not depend on modifying the tool\'s output. The suggested fix in C is also circular: it requires the agent to know it should search for inflation rate data, which is the behavior the system instruction would produce.'),
        ('> ❌ **D is incorrect.** The agent did not terminate prematurely — it generated a Final Answer after completing its reasoning loop with the information it had. Premature termination implies stopping before sufficient information is gathered; this trace shows the agent generating a complete-appearing Final Answer by supplementing retrieved data with hallucinated data. Increasing max_iterations would only cause the agent to make additional searches; it would not prevent the agent from hallucinating in the Thoughts that already occurred.',
         '> ❌ **D is incorrect.** The agent did not terminate prematurely — it returned a final answer after completing its reasoning loop with the information it had. Premature termination implies stopping before sufficient information is gathered; this trace shows the agent producing a complete-appearing answer by supplementing retrieved data with hallucinated data. Raising the `recursion_limit` would only allow the agent to make additional searches; it would not prevent the agent from hallucinating in the reasoning that already occurred.'),
        ('**Question 3.** The Chapter 3 lesson states: "The ability to read a reasoning trace analytically — identifying where reasoning deviated, why a tool call was incorrect, and what change to the agent design would fix the failure — is a high-value professional competency." A practitioner is investigating a production failure where the agent\'s final answer contains incorrect pricing data. The practitioner has access to the verbose trace. What is the minimum diagnostic information a complete trace analysis must provide, according to the Reading Guide?',
         '**Question 3.** The Chapter 3 lesson states: "The ability to read a reasoning trace analytically — identifying where reasoning deviated, why a tool call was incorrect, and what change to the agent design would fix the failure — is a high-value professional competency." A practitioner is investigating a production failure where the agent\'s final answer contains incorrect pricing data. The practitioner has the streamed trace of the run. What is the minimum diagnostic information a complete trace analysis must provide, according to the Reading Guide?'),
        ('B. Three elements: (1) the specific trace location where the failure manifested (which Thought, Action, or Observation step), (2) the root cause class from the five-failure taxonomy (which structural failure produced the error), and (3) the corrective structural intervention (which agent design element — tool description, system instruction, few-shot example, or output format — must be changed, and how).',
         'B. Three elements: (1) the specific trace location where the failure manifested (which model message, which tool call, or which tool result), (2) the root cause class from the five-failure taxonomy (which structural failure produced the error), and (3) the corrective structural intervention (which agent design element — tool description, system instruction, few-shot example, or output format — must be changed, and how).'),
        ("> ✅ **B is correct.** Reading Guide 3's diagnostic protocol maps directly to the three-element structure in B. The guide's synthesis task and the Chapter 3 lesson both specify that a complete trace analysis identifies: (1) where in the trace the failure manifested — which specific step (which Thought's inference, which Action's tool selection, which Observation's misinterpretation); (2) what failure class from the five-category taxonomy applies — this determines the structural category of the root cause; and (3) what structural fix addresses the root cause — not what behavioral change to hope for, but what specific design element to modify. This three-element structure ensures that the analysis is both diagnostic (locates the failure) and prescriptive (produces an actionable fix) — the two outputs that make trace analysis professionally valuable.",
         "> ✅ **B is correct.** Reading Guide 3's diagnostic protocol maps directly to the three-element structure in B. The guide's synthesis task and the Chapter 3 lesson both specify that a complete trace analysis identifies: (1) where in the trace the failure manifested — which specific step (which model message's inference, which tool call's tool selection, which tool result's misinterpretation); (2) what failure class from the five-category taxonomy applies — this determines the structural category of the root cause; and (3) what structural fix addresses the root cause — not what behavioral change to hope for, but what specific design element to modify. This three-element structure ensures that the analysis is both diagnostic (locates the failure) and prescriptive (produces an actionable fix) — the two outputs that make trace analysis professionally valuable."),
        ('**Question 4.** A practitioner observes the following abbreviated trace:\n\n```\nThought: The user wants a compound interest calculation for $10,000 at 5% for 3 years.\nAction: web_search\nAction Input: "compound interest $10000 5% 3 years"\nObservation: [Search returned several articles about compound interest formulas]\nThought: Based on the search results, I\'ll calculate this now.\nFinal Answer: $10,000 compounded at 5% for 3 years is approximately $11,576.25.\n```',
         "**Question 4.** A practitioner runs an agent with the lab's `show_trace` helper and observes the following abbreviated trace:\n\n```\n[1] REASONING:  The user wants a compound interest calculation for $10,000 at 5% for 3 years.\n[1] TOOL CALL:  web_search\n[1] ARGUMENTS:  {'query': 'compound interest $10000 5% 3 years'}\n[1] OBSERVATION: [Search returned several articles about compound interest formulas]\n[final] ANSWER:  Based on the search results, I'll calculate this now. $10,000 compounded at 5% for 3 years is approximately $11,576.25.\n```"),
        ('A. Observation misinterpretation — the agent misread the search results articles and produced an incorrect calculation; the Final Answer value is wrong because the agent misinterpreted the retrieved formula.',
         'A. Observation misinterpretation — the agent misread the search results articles and produced an incorrect calculation; the final answer is wrong because the agent misinterpreted the retrieved formula.'),
        ('B. Incorrect tool selection — the trace shows `Action: web_search` for a mathematical calculation task for which the Python REPL is explicitly the correct tool per its description. The evidence is the Action line: the agent searched the web for compound interest articles rather than executing `A = 10000 * (1 + 0.05)**3` in the REPL. The fix is to add a scope boundary to the web search tool: "Do not use for mathematical calculations — use the Python REPL instead."',
         'B. Incorrect tool selection — the trace shows the model requesting `web_search` for a mathematical calculation task for which the Python REPL is explicitly the correct tool per its description. The evidence is the `TOOL CALL:` line: the agent searched the web for compound interest articles rather than executing `A = 10000 * (1 + 0.05)**3` in the REPL. The fix is to add a scope boundary to the web search tool: "Do not use for mathematical calculations — use the Python REPL instead."'),
        ('C. Hallucination in Thought — the second Thought says "Based on the search results, I\'ll calculate this now," but the Final Answer is actually computed from parametric memory (the formula), not from code execution. This is hallucination because the agent claims to use search results but does not.',
         'C. Hallucination in Thought — the final message says "Based on the search results, I\'ll calculate this now," but the number is actually produced from parametric memory (the formula), not from code execution. This is hallucination because the agent claims to use search results but does not.'),
        ('> ✅ **B is correct.** The trace\'s `Action: web_search` line provides the direct evidence: the agent selected the web search tool for a task — compound interest calculation — that the Python REPL tool\'s description explicitly covers ("Use for mathematical calculations"). This is an incorrect tool selection failure: the right tool was available, its description specified the correct use case, but the web search tool was selected instead. The most likely cause is that the web search tool\'s description does not include a scope boundary prohibiting mathematical calculations, creating ambiguity about which tool to use for math-related queries. The structural fix is to add to the web search tool\'s description: "Do not use for mathematical calculations or data processing tasks — use the Python REPL for these." Reading Guide 3 identifies the `Action:` line as the trace location where incorrect tool selection failures manifest.',
         '> ✅ **B is correct.** The `TOOL CALL:  web_search` line provides the direct evidence: the agent selected the web search tool for a task — compound interest calculation — that the Python REPL tool\'s description explicitly covers ("Use for mathematical calculations"). This is an incorrect tool selection failure: the right tool was available, its description specified the correct use case, but the web search tool was selected instead. The most likely cause is that the web search tool\'s description does not include a scope boundary prohibiting mathematical calculations, creating ambiguity about which tool to use for math-related queries. The structural fix is to add to the web search tool\'s description: "Do not use for mathematical calculations or data processing tasks — use the Python REPL for these." The name the model puts in its tool call — the `TOOL CALL:` line of the trace — is the location where incorrect tool selection failures manifest.'),
        ('> ❌ **A is incorrect.** The Final Answer value ($11,576.25) is arithmetically correct — $10,000 × (1.05)³ = $11,576.25. The agent did not misread a formula; it computed or recalled the correct value. The failure is in which tool was used to arrive at the answer (web search instead of REPL), not in the accuracy of the final computation. Observation misinterpretation produces a wrong answer from a correctly executed tool call; this trace produces a correct answer from an incorrectly selected tool.',
         '> ❌ **A is incorrect.** The final value ($11,576.25) is arithmetically correct — $10,000 × (1.05)³ = $11,576.25. The agent did not misread a formula; it computed or recalled the correct value. The failure is in which tool was used to arrive at the answer (web search instead of REPL), not in the accuracy of the final computation. Observation misinterpretation produces a wrong answer from a correctly executed tool call; this trace produces a correct answer from an incorrectly selected tool.'),
        ('> ❌ **C is incorrect.** The agent\'s Thought "Based on the search results, I\'ll calculate this now" is a loose description of its reasoning process — it acknowledges the search results and then produces a calculation. Whether the actual arithmetic was performed parametrically or from a formula in the search results is not determinable from the trace alone, and the Final Answer is correct either way. The failure is not hallucination in Thought (asserting a false fact as retrieved); it is using the wrong tool for the task from the start.',
         '> ❌ **C is incorrect.** The agent\'s narration — "Based on the search results, I\'ll calculate this now" — is a loose description of its own reasoning: it acknowledges the search results and then produces a calculation. Whether the arithmetic was performed parametrically or read out of a formula in the search results is not determinable from the trace alone, and the answer is correct either way. The failure is not hallucination in Thought (asserting a false fact as retrieved); it is using the wrong tool for the task from the start.'),
        ('*Based on Reading Guide 4: Liu et al. (2023) ACM Computing Surveys, Brown et al. (2020), Wei et al. (2022), LangChain AgentExecutor*',
         '*Based on Reading Guide 4: Liu et al. (2023) ACM Computing Surveys, Brown et al. (2020), Wei et al. (2022), LangChain agent prompt design (`create_agent`)*'),
        ('**Question 5.** The Chapter 3 lesson states that reasoning trace analysis is the "primary diagnostic skill of Module 2." A student argues: "If I just look at whether the Final Answer is correct, I don\'t need to read the trace — a correct Final Answer means the agent succeeded, and an incorrect one means it failed. Trace reading is extra work." What is the most precise refutation of this argument, based on Reading Guide 3?',
         '**Question 5.** The Chapter 3 lesson states that reasoning trace analysis is the "primary diagnostic skill of Module 2." A student argues: "If I just look at whether the final answer is correct, I don\'t need to read the trace — a correct final answer means the agent succeeded, and an incorrect one means it failed. Trace reading is extra work." What is the most precise refutation of this argument, based on Reading Guide 3?'),
        ('A. The student is correct in practice — trace reading is necessary only when the Final Answer is incorrect. For correct Final Answers, confirming the result is sufficient; reading the trace provides no additional diagnostic value.',
         'A. The student is correct in practice — trace reading is necessary only when the final answer is incorrect. For correct final answers, confirming the result is sufficient; reading the trace provides no additional diagnostic value.'),
        ('B. The student is incorrect on both counts: a correct Final Answer can coexist with a trace-visible failure (e.g., the agent hallucinated a correct fact from parametric memory rather than retrieving it — the answer is right but the architecture is unreliable for novel queries), and reading the trace after an incorrect answer tells the practitioner which failure class applies, which determines what structural fix is required. Without trace reading, incorrect and correct failures cannot be distinguished by type.',
         'B. The student is incorrect on both counts: a correct final answer can coexist with a trace-visible failure (e.g., the agent hallucinated a correct fact from parametric memory rather than retrieving it — the answer is right but the architecture is unreliable for novel queries), and reading the trace after an incorrect answer tells the practitioner which failure class applies, which determines what structural fix is required. Without trace reading, incorrect and correct failures cannot be distinguished by type.'),
        ('D. The student is partially correct — trace reading is unnecessary for simple single-tool tasks with deterministic outputs, but is required for complex multi-tool tasks with probabilistic outputs where the Final Answer alone does not indicate which tool produced each component.',
         'D. The student is partially correct — trace reading is unnecessary for simple single-tool tasks with deterministic outputs, but is required for complex multi-tool tasks with probabilistic outputs where the final answer alone does not indicate which tool produced each component.'),
        ("> ✅ **B is correct.** Reading Guide 3 establishes two distinct reasons why Final Answer inspection is insufficient. First, a correct Final Answer can mask a trace failure: the hallucination in Thought failure class specifically produces a trace where the Final Answer may be factually correct (the agent happened to recall the right fact parametrically), but the reasoning was unreliable — on a novel query where the agent's parametric memory contains the wrong answer, the same flawed architecture would produce an incorrect result. A practitioner who only inspects Final Answers would not detect this latent reliability problem. Second, when the Final Answer is incorrect, reading the trace identifies which failure class applies — incorrect tool selection, malformed tool call, observation misinterpretation, premature termination, or hallucination in Thought — each requiring a different structural fix. Without trace reading, the practitioner cannot determine the correct fix and may apply the wrong intervention.",
         "> ✅ **B is correct.** Reading Guide 3 establishes two distinct reasons why inspecting the final answer alone is insufficient. First, a correct final answer — the text the lab's trace prints on its `[final] ANSWER:` line — can mask a trace failure: the hallucination in Thought failure class specifically produces a trace where the final answer may be factually correct (the agent happened to recall the right fact parametrically), but the reasoning was unreliable — on a novel query where the agent's parametric memory contains the wrong answer, the same flawed architecture would produce an incorrect result. A practitioner who only inspects final answers would not detect this latent reliability problem. Second, when the final answer is incorrect, reading the trace identifies which failure class applies — incorrect tool selection, malformed tool call, observation misinterpretation, premature termination, or hallucination in Thought — each requiring a different structural fix. Without trace reading, the practitioner cannot determine the correct fix and may apply the wrong intervention."),
        ('> ❌ **A is incorrect.** Reading Guide 3 explicitly addresses this argument: a correct Final Answer does not guarantee a reliable reasoning architecture. The hallucination in Thought failure class demonstrates that a trace can produce a correct answer by accident (parametric memory happens to contain the right value) while the underlying architecture is unreliable. Skipping trace reading for correct answers misses this reliability signal.',
         '> ❌ **A is incorrect.** Reading Guide 3 explicitly addresses this argument: a correct final answer does not guarantee a reliable reasoning architecture. The hallucination in Thought failure class demonstrates that a trace can produce a correct answer by accident (parametric memory happens to contain the right value) while the underlying architecture is unreliable. Skipping trace reading for correct answers misses this reliability signal.'),
        ('> ❌ **D is incorrect.** Reading Guide 3 does not establish a task-complexity threshold for trace reading. The hallucination in Thought failure class can occur in single-tool tasks with simple outputs — the trace in the synthesis task involves only one tool (web search) and one Observation. Complexity and tool count do not determine whether trace reading is diagnostically necessary; the potential for silent trace failures does.',
         '> ❌ **D is incorrect.** Reading Guide 3 does not establish a task-complexity threshold for trace reading. The hallucination in Thought failure class can occur in single-tool tasks with simple outputs — the trace in the synthesis task involves only one tool (web search) and one tool result. Complexity and tool count do not determine whether trace reading is diagnostically necessary; the potential for silent trace failures does.'),
        ('**Question 1.** Liu et al. (2023) describe a four-component prompt taxonomy: instruction, context, input indicator, and output indicator. A practitioner designing a legal document review agent writes the following prompt component: "Final Answer format: (1) Executive Summary — ≤50 words; (2) Key Clauses Identified — bulleted list with clause name and page number; (3) Risk Assessment — High/Medium/Low with one-sentence justification; (4) Recommended Actions — numbered list." Which Liu et al. component does this text instantiate, and what function does it serve in the agent\'s generation process?',
         '**Question 1.** Liu et al. (2023) describe a four-component prompt taxonomy: instruction, context, input indicator, and output indicator. A practitioner designing a legal document review agent writes the following prompt component: "Final answer format: (1) Executive Summary — ≤50 words; (2) Key Clauses Identified — bulleted list with clause name and page number; (3) Risk Assessment — High/Medium/Low with one-sentence justification; (4) Recommended Actions — numbered list." Which Liu et al. component does this text instantiate, and what function does it serve in the agent\'s generation process?'),
        ("C. Output indicator — it specifies the required structure and format of the agent's Final Answer, shaping the model's generation to conform to a defined output schema rather than producing free-form text.",
         "C. Output indicator — it specifies the required structure and format of the agent's final answer, shaping the model's generation to conform to a defined output schema rather than producing free-form text."),
        ("> ✅ **C is correct.** Liu et al.'s output indicator is the prompt component that specifies the desired output format, structure, or type. The text in the question does not specify what to do (instruction), does not provide background knowledge (context), and does not mark the input location (input indicator) — it specifies exactly how the Final Answer must be structured: four numbered sections with specific format requirements for each. This is the output indicator component. In the agent context, the output indicator corresponds to the output format constraints dimension of agent prompt engineering (Reading Guide 4's cross-mapping table). The output indicator functions to constrain the model's generation space: instead of producing free-form text, the model conditions its generation on the defined schema, producing consistently structured outputs that downstream systems or human reviewers can process reliably.",
         "> ✅ **C is correct.** Liu et al.'s output indicator is the prompt component that specifies the desired output format, structure, or type. The text in the question does not specify what to do (instruction), does not provide background knowledge (context), and does not mark the input location (input indicator) — it specifies exactly how the final answer must be structured: four numbered sections with specific format requirements for each. This is the output indicator component. In the agent context, the output indicator corresponds to the output format constraints dimension of agent prompt engineering (Reading Guide 4's cross-mapping table). The output indicator functions to constrain the model's generation space: instead of producing free-form text, the model conditions its generation on the defined schema, producing consistently structured outputs that downstream systems or human reviewers can process reliably."),
        ('> ❌ **D is incorrect.** The input indicator marks the boundary between the prompt\'s framing components (instructions, context) and the specific input instance to be processed in this call (e.g., "CONTRACT TEXT: [document content]"). A formatting specification for the Final Answer does not mark the input location; it appears at the end of the prompt to shape the output, not at the input boundary.',
         '> ❌ **D is incorrect.** The input indicator marks the boundary between the prompt\'s framing components (instructions, context) and the specific input instance to be processed in this call (e.g., "CONTRACT TEXT: [document content]"). A formatting specification for the final answer does not mark the input location; it appears at the end of the prompt to shape the output, not at the input boundary.'),
        ("> ❌ **D is incorrect.** The output indicator specifies the required format of the model's output — section headers, citation format, confidence levels. Tool descriptions specify input argument schemas (what the tool requires), not the format of the model's Final Answer output. The output format constraints dimension (corresponding to output indicator) governs how the agent structures its Final Answer, not how it calls tools.",
         "> ❌ **D is incorrect.** The output indicator specifies the required format of the model's output — section headers, citation format, confidence levels. Tool descriptions specify input argument schemas (what the tool requires), not the format of the model's final answer. The output format constraints dimension (corresponding to output indicator) governs how the agent structures its final answer, not how it calls tools."),
        ("> **Correct Answer: B or C depending on interpretation; B is the strongest answer.**",
         "> **Correct Answer: B**"),
        # Chapter 5 Q1 was keyed "B or C depending on interpretation" because the stem never said where the
        # sales data lived: if the agent had to query it, ReAct (C) is right. The stem now puts the figures in the
        # prompt, C argues for ReAct from "multi-step" alone, and the key stays B.
        ('**Question 1.** The six-dimension trade-off assessment framework requires evaluating architectural choices across: task complexity, inference cost, latency requirements, external information needs, interpretability requirements, and deployment risk profile. A practitioner evaluating an agent for "weekly automated analysis of internal sales data to generate a board-level performance report" assesses the task as follows: complex multi-step analysis with no backtracking; moderate cost acceptable; latency of hours acceptable; no external real-time data needed; no regulatory interpretability requirement; internal low-risk deployment. Which paradigm does the framework most directly support, and which dimension most decisively rules out LATS?',
         "**Question 1.** The six-dimension trade-off assessment framework requires evaluating architectural choices across: task complexity, inference cost, latency requirements, external information needs, interpretability requirements, and deployment risk profile. A practitioner is choosing a reasoning paradigm for a weekly agent that turns internal sales figures into a board-level performance report. Each week's figures are exported as a table and placed directly in the prompt, so the agent needs no retrieval or tool calls while it reasons. The analysis is complex and multi-step, but it follows the same known structure every week, with no backtracking. Moderate cost and a latency of hours are acceptable, there is no regulatory interpretability requirement, and the deployment is internal and low-risk. Which paradigm does the framework most directly support?"),
        ("B. CoT — because the task requires no external data access (ruling out ReAct, ToT, and LATS as unnecessarily complex), and CoT's linear reasoning is sufficient for a structured sales data analysis task where the data is provided in the prompt.",
         "B. CoT — every figure the analysis needs is already in the prompt, so ReAct's tool loop would have nothing to fetch, and a known structure with no backtracking leaves ToT and LATS no alternatives worth searching; linear reasoning over the provided data is sufficient, at the lowest cost."),
        ('C. ReAct — because while complex analysis is required, the task does not require backtracking (ruling out ToT/LATS as unjustified), does not require real-time external data (the sales data is internal and can be loaded directly), and the latency/cost constraints are moderate but not absent. The most decisive dimension ruling out LATS is task complexity: the task does not require deliberate search over a large state space because the analysis structure is known and backtracking is not necessary.',
         'C. ReAct — the analysis takes many steps, and interleaving reasoning with tool calls is the safer default for any multi-step task; the relaxed cost and latency budgets make the tool-calling overhead affordable.'),
        ("> ✅ **B is correct.** Applying the six-dimension framework systematically: (1) Task complexity — structured sales analysis is a known analytical procedure, not an open-ended search problem; no backtracking is needed. (2) Inference cost — moderate; weekly cadence means cost is not a per-query constraint. (3) Latency — hours; not a differentiating constraint. (4) External information needs — none: internal data loaded directly, not requiring real-time retrieval. (5) Interpretability — low; no regulatory requirement. (6) Risk — low; internal deployment. The external information needs dimension rules out the necessity of tool-calling architecture: if all required data is available in the context window, CoT's direct reasoning over provided data is architecturally sufficient. ReAct adds tool-calling overhead that is not needed when no external retrieval is required. The most decisive dimension ruling out ReAct, ToT, and LATS is external information needs — the task can be fully specified within the prompt context without requiring any tool invocation.",
         "> ✅ **B is correct.** Walk the six dimensions. External information needs: none — the figures are in the prompt, and what ReAct adds over CoT is the ability to act and observe the result, which this task never needs. Task complexity: many steps, but a known structure with no backtracking, so ToT and LATS have no alternatives worth searching. Inference cost: CoT is the cheapest paradigm, ReAct's cost grows with every tool call, and branching search grows super-linearly. Latency, interpretability and deployment risk are all relaxed here, so none of them pulls toward a heavier paradigm; a relaxed budget makes a heavier paradigm affordable, not necessary. CoT is the lightest paradigm that satisfies every dimension."),
        ('> ❌ **C is plausible but less optimal than B.** ReAct is a reasonable choice if the sales data requires tool access (e.g., querying a database API) rather than being provided directly in context. However, the question specifies "internal sales data" with no external real-time data need, suggesting the data can be incorporated in the prompt. For a task where all data is in-context, CoT is more precisely correct — adding a tool-calling layer (ReAct) for data that is already in context adds architectural complexity without benefit.',
         '> ❌ **C is incorrect.** Multi-step is not the same as needing to act. CoT handles multi-step reasoning over data it has been given; ReAct earns its place when the agent must fetch information it does not have, such as by querying a database, searching, or calling an API. Here every figure is already in the prompt, so each tool call would add cost and a new place to fail without adding information. Had the figures lived in a database the agent had to query, ReAct would be the right answer; the stem rules that out.'),
    ],
    "modules/module-2/resources.md": [
        # The guide and the quizzes ask for "structural components"; make the heading a learner
        # searching that phrase can actually find.
        ("## Functional Components of a Tool-Calling Agent Architecture",
         "## Structural Components of a Tool-Calling Agent Architecture"),
        # The page was written against LangChain 0.x. AgentExecutor, create_tool_calling_agent
        # and langchain.prompts were all removed in LangChain 1.x, so both code samples raised
        # ImportError for anyone who copied them. The conceptual model on this page (LLM
        # backbone, tool registry, action executor, memory) is framework-agnostic and correct,
        # so only the API names and the two samples are rewritten onto create_agent.
        ("We previously looked at a code example of how LangChain's `AgentExecutor` runs this loop. ",
         "We previously looked at a code example of how LangChain's agent runtime runs this loop. "),
        ("In LangChain, the ReAct loop is practically managed by a runtime component called the `AgentExecutor`. ",
         "In LangChain, the ReAct loop is managed for you by the agent that `create_agent` builds. "
         "Older tutorials call this runtime the `AgentExecutor`; that class was removed in LangChain 1.0 "
         "and `create_agent` replaced it. "),
        ("*   **Execution:** The `AgentExecutor` steps in, physically runs the requested tool",
         "*   **Execution:** The agent runtime steps in, physically runs the requested tool"),
        ("Here is a practical code example showing how to set up and run an `AgentExecutor` in LangChain. ",
         "Here is a practical code example showing how to set up and run an agent in LangChain. "),
        (M2_RESOURCES_CODE_1_OLD, M2_RESOURCES_CODE_1_NEW),
        ("In this setup, the `create_tool_calling_agent` function defines how the LLM interacts with the prompt and tools. The `AgentExecutor` then acts as the runtime environment that continuously cycles through selecting actions, executing the tools, and processing the outputs until the agent formulates a final conclusion. Setting `verbose=True` lets you watch the \"Thought-Action-Observation\" steps happen live in your console.",
         "In this setup, `create_agent` builds a runnable agent from three arguments — the model, its tools "
         "and its instructions. The agent cycles through selecting actions, executing tools and processing the outputs "
         "until it formulates a final conclusion. To watch those steps as they happen, stream the agent "
         "instead of invoking it: `agent.stream(..., stream_mode=\"updates\")` reports each tool call and "
         "each tool result as structured data, which is what replaced the old `verbose=True` text trace."),
        ("Here is how you combine those components into a working `AgentExecutor` in LangChain:",
         "Here is how you combine those components into a working agent in LangChain:"),
        (M2_RESOURCES_CODE_2_OLD, M2_RESOURCES_CODE_2_NEW),
        ("The `create_tool_calling_agent` function directly combines your LLM, tool registry, and prompt. The `AgentExecutor` then steps in as the action executor, taking the user's input and continuously managing the ReAct loop until it reaches a final answer. Setting `verbose=True` allows you to watch the \"Thought-Action-Observation\" steps print live in your console.",
         "The `create_agent` function takes your model, your tools and your instructions and returns a runnable "
         "agent whose action executor takes the user's input and manages the reasoning "
         "loop until it reaches a final answer. Stream the agent with "
         "`stream_mode=\"updates\"` to watch each tool call and tool result as it happens."),
    ],
    "modules/module-3/activities.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Path-to-AI-Memory.png" width=900>',
         PAGE_DIAGRAMS['Path-to-AI-Memory|modules/module-3/activities.md']),
        ('3. RetrievalQA chain configuration with k=4 retrieval and testing across five evaluation queries.',
         '3. Retrieval and generation composed with LangChain Expression Language — a `k=4` retriever whose chunks are formatted into a prompt for a chat model, returning the answer and its source chunks together — then tested across five evaluation queries.'),
        ("### Notebook Flow Summary", "### Guided lab notebook flow"),
        ("### Notebook Flow Summary", "### Project notebook flow"),
        ('**Open the lab notebook:** [Module-3-Lab.ipynb](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/materials/module3/Module-3-Lab.ipynb)',
         "**Open the lab notebook:** [Module-3-Lab.ipynb](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/materials/module3/Module-3-Lab.ipynb)\n\nThe corpus is NIST's AI Risk Management Framework ([NIST AI 100-1](../../materials/module3/NIST.AI.100-1.pdf)) and its Generative AI Profile ([NIST AI 600-1](../../materials/module3/NIST.AI.600-1.pdf)), both public-domain US government publications. The notebook downloads them for you."),
        ('score answer quality using a provided rubric, and write a mechanistic analysis of your results.',
         'score answer quality on a 1–4 rubric against ten evaluation questions with reference answers, and write a mechanistic analysis of your results.'),
        ('The notebook walks you through a controlled 4-run parameter variation experiment:\n\n1. Run 1 — Small fixed-size chunking baseline (chunk_size=256, similarity search, k=4).',
         'Part B of the notebook walks you through a controlled 4-run parameter variation experiment on ten evaluation questions about the AI RMF, each with a reference answer and the page it comes from:\n\n1. Run 1 — Small fixed-size chunking baseline (chunk_size=256, chunk_overlap=25, similarity search, k=4).'),
        ('2. Run 2 — Larger fixed-size chunking (chunk_size=512) to observe',
         '2. Run 2 — Larger fixed-size chunking (chunk_size=512, chunk_overlap=50) to observe'),
        ('4. Run 4 (optional) — Metadata-filtered retrieval to evaluate precision gains from source-level filtering.\n5. RAGAS metric interpretation — plain-language interpretation of four RAGAS metric scores for a non-technical stakeholder.\n\nDetailed instructions are embedded directly in the notebook.',
         "4. Run 4 (optional) — Metadata-filtered retrieval on the two-document store from Step A4, to evaluate precision gains from source-level filtering.\n5. Experiment log — the mean score for each run and a two-paragraph mechanistic conclusion, written before you check it against the notebook's retrieval evidence.\n6. RAGAS metric interpretation — plain-language interpretation of four provided RAGAS metric scores for a non-technical stakeholder.\n\nThe rubric, the evaluation questions and the instructions for every step are in the notebook."),
    ],
    "modules/module-4/activities.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Multi-Agent-Orchestration-Map.png" width=900>',
         PAGE_DIAGRAMS['Multi-Agent-Orchestration-Map|modules/module-4/activities.md']),
        ("### Notebook Flow Summary", "### Guided lab notebook flow"),
        ("### Notebook Flow Summary", "### Project notebook flow"),
    ],
    "modules/module-5/activities.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Mastering-Responsible-AgenticAI.png" width=900>',
         PAGE_DIAGRAMS['Mastering-Responsible-AgenticAI|modules/module-5/activities.md']),
        ("### Notebook Flow Summary", "### Guided lab notebook flow"),
        ("### Notebook Flow Summary", "### Project notebook flow"),
        # The notebook's agent has a simulated search tool and a calculator (live DuckDuckGo is optional) and runs
        # 10 prompts in five categories; the page described live web search and webpage reading.
        ('In this lab, you will instrument a research agent with LangSmith tracing, execute it on 10 complex research prompts using real web search tools (DuckDuckGo + webpage reading), and explore what the resulting traces reveal about how your agent actually behaves.',
         "In this lab, you will instrument a two-tool agent with LangSmith tracing, run it on 10 test prompts spanning five categories (factual, calculation, multi-step, format and safety), and explore what the resulting traces reveal about how your agent actually behaves. The agent's search tool returns simulated results so that every run is reproducible; the notebook shows how to switch to a live DuckDuckGo search if you want one."),
        ('1. Build a research agent with two real tools (web search and webpage reading) using LangGraph.',
         "1. Build a ReAct agent with two tools, search and a calculator, using LangChain's `create_agent`, which runs on LangGraph."),
        ('3. Execute the agent on 10 diverse research prompts with structured metadata tags for filtering.',
         '3. Execute the agent on the 10 test prompts with structured metadata tags for filtering.'),
        ('comparing 2–3 agent configurations on the same research tasks',
         'comparing 2–3 agent configurations on the same prompts'),
        ('2. Run each configuration on the same 10 research prompts, collecting traces and metrics for each condition.',
         '2. Run each configuration on the same 10 test prompts from the guided lab, collecting traces and metrics for each condition.'),
        ('3. Compute comparative metrics (average latency, p90 latency, output quality, success rate) across conditions.',
         '3. Compute comparative metrics (average latency, p90 latency, average output length, success rate) across conditions.'),
    ],
    "modules/module-3/chapter-quizzes.md": [
        ('**Question 4.** A LangChain RAG chain is configured with `RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)`. A practitioner runs a test query and observes that the generated answer contains a specific factual claim that does not appear in any of the returned `source_documents`. What failure mode does this observation most precisely identify?',
         '**Question 4.** A LangChain RAG chain composes the retriever and the generator with LCEL, so that a single invocation returns both the generated `result` and the `source_documents` the retriever supplied for that query. A practitioner runs a test query and observes that the generated answer contains a specific factual claim that does not appear in any of the returned `source_documents`. What failure mode does this observation most precisely identify?'),
        ('> ✅ **B is correct.** The `return_source_documents=True` parameter enables direct inspection of the retrieval stage output. When the practitioner confirms that the factual claim in the generated answer is absent from all returned source documents, they have identified a faithfulness violation: the LLM generated a claim that is not supported by the retrieved context. This is precisely what the RAGAS faithfulness metric measures. The LLM "filled the gap" using parametric memory — a dangerous behavior in any application where answers must be attributable to verified sources. The diagnostic value of `return_source_documents=True` is exactly this: it makes faithfulness violations visible without requiring RAGAS instrumentation.',
         '> ✅ **B is correct.** Because the chain carries `source_documents` alongside `result`, the output of the retrieval stage can be inspected for the very query that produced the answer. When the practitioner confirms that the factual claim in the generated answer is absent from all returned source documents, they have identified a faithfulness violation: the LLM generated a claim that is not supported by the retrieved context. This is precisely what the RAGAS faithfulness metric measures. The LLM "filled the gap" using parametric memory — a dangerous behavior in any application where answers must be attributable to verified sources. The diagnostic value of keeping the retrieved chunks in the chain\'s own output is exactly this: it makes faithfulness violations visible without requiring RAGAS instrumentation.'),
        ("# Module 3 — Chapter 3 Quiz\n## Conversational Memory Management", "## Chapter 3 Quiz — Conversational Memory Management"),
        ('**Question 5.** A practitioner implementing the Unit 4 Token Budget Analysis identifies that the retrieved context block (k=4 chunks × chunk_size=512 tokens) accounts for 68% of total input tokens per turn. They propose reducing k from 4 to 2 as a token reduction strategy. What specific quantitative check must the Quality Impact Assessment include before adopting this strategy?',
         '**Question 5.** A practitioner profiling a RAG system finds that the retrieved context block (k=4 chunks at chunk_size=512) accounts for 68% of total input tokens per turn. They propose reducing k from 4 to 2 to cut token cost. What quantitative check must they run before adopting this change?'),
        ('B. A comparison of the mean evaluation score at k=4 vs. k=2 on the same evaluation query set, to determine whether the approximately 50% reduction in retrieved context tokens produces a mean score degradation greater than 0.5 points on the 1–4 scale — the threshold at which the quality cost must be explicitly justified or an alternative strategy proposed.',
         'B. A comparison of the mean evaluation score at k=4 vs. k=2 on the same evaluation query set and rubric, to measure how much answer quality the roughly 50% cut in retrieved context tokens costs before deciding whether the saving is worth it.'),
        ('> ✅ **B is correct.** The module explicitly specifies this check:',
         '> ✅ **B is correct.** This is the check that matters:'),
        ('The Quality Impact Assessment must run the same evaluation query set used in Task 1 on the reduced-k configuration and compare mean scores. The module establishes a specific threshold: if the token reduction degrades mean score by more than 0.5 points (on a 1–4 scale), the report must either justify why the token saving is worth the quality cost or propose an alternative strategy. This is not an arbitrary threshold — a 0.5-point degradation from a baseline of 3.0 (75%) to 2.5 (62.5%) represents a meaningful user-experience decline in answer completeness.',
         "The only way to know whether that risk materializes is a controlled comparison — the same design as the module's retrieval experiment: hold everything else fixed, run the same evaluation queries under k=4 and k=2, score both on the same rubric, and compare the means. If quality drops by more than the token saving can justify, a different strategy is needed, such as trimming the system prompt or compressing the retrieved context."),
        ('the primary motivation specified in the task is token cost reduction',
         'the motivation here is token cost reduction'),
        ('does not address the quality risk that the module requires the assessment to evaluate. The quality impact check (B) is explicitly required; latency profiling is not.',
         'does not address the quality risk the change introduces. The quality check in B has to come first; latency profiling is optional.'),
    ],
    "modules/module-1/readings/what-is-an-agent.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Decoding_AI_Agents.png" width=900>',
         PAGE_DIAGRAMS['Decoding_AI_Agents|modules/module-1/readings/what-is-an-agent.md']),
        ("### AI Automation and Agents", "### Contents of this package"),
    ],
    "modules/module-1/worksheets/ai-agents-glossary.md": [
        ("## Building a common glossary or terms", "## Building a common glossary of terms"),
    ],
    "archive/module-1/concept-quiz-spec-draft.md": [
        ("Activity 8 — Module 1 Concept Quiz\n", ""),
    ],
    "archive/module-1/guided-workflow-mapping-stub.md": [
        ("Activity 11 — Guided Workflow Mapping Exercise\n", ""),
    ],
    "course-design/learning-design.md": [
        ('<img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/ModuleLearningActivitiesDescription1.png" width=800>',
         IMAGE_TABLES['ModuleLearningActivitiesDescription1']),
        ('<img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/ModuleLearningActivitiesDescription2.png" width=800>',
         IMAGE_TABLES['ModuleLearningActivitiesDescription2']),
        ('<img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/StandardActivityStructurePerModule.png" width=600>',
         IMAGE_TABLES['StandardActivityStructurePerModule']),
        ('<img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Blooms_Spiral_Progression.png" width=800>',
         IMAGE_TABLES['Blooms_Spiral_Progression']),
        ("### Academic References", "## Academic References"),
    ],
    "course-design/course-review-2026-07.md": [
        ("## Module-by-Module Analysis\n", ""),
    ],
    "modules/module-2/reading-guides.md": [
        ('- Reading 5: LangChain Documentation — *AgentExecutor Conceptual Guide and Tool Creation Reference.* Read the complete AgentExecutor Conceptual Guide. Focus: tool registry role, tool description use for tool selection, output parser conversion of LLM text to structured tool calls.',
         '- Reading 5: LangChain Documentation — *[Agents](https://docs.langchain.com/oss/python/langchain/agents) and [Tools](https://docs.langchain.com/oss/python/langchain/tools).* Read the complete Agents guide; use the Tools reference for Part B. Focus: tool registry role, tool description use for tool selection, and how a tool-calling model returns a structured call — a `name` and an `args` dictionary — instead of text that an output parser has to convert.'),
        ('- Video 2: Sam Witteveen — *"Understanding ReACT with LangChain"* (~22 min). Watch focus: conceptual distinction between CoT and ReAct; the observation integration step.',
         '- Video 2: Sam Witteveen — *"Understanding ReACT with LangChain"* (~22 min). Watch focus: conceptual distinction between CoT and ReAct; the observation integration step. The video was recorded against LangChain 0.x, whose `AgentExecutor` class was removed in LangChain 1.0 — take the reasoning-loop explanation from the video and the API from Reading 5.'),
        ('### Part A: The AgentExecutor Architecture',
         '### Part A: The Agent Runtime Architecture'),
        ('**Scope:** AgentExecutor Conceptual Guide — complete.',
         '**Scope:** LangChain Agents guide — complete.'),
        ('1. The AgentExecutor has five structural components. Name all five and describe the specific function of each in one sentence. Pay particular attention to the **tool registry**: what does it store, and how does the agent access it during a reasoning loop?',
         "1. The agent runtime has four structural components. Name all four and describe the specific function of each in one sentence. Pay particular attention to the **tool registry**: what does it store, where does each tool's description come from, and how does the model use it during a reasoning loop?"),
        ("2. The documentation describes how the **output parser** converts the LLM's raw text output into a structured tool call. What would happen if the output parser received a malformed LLM response — for example, a response that names a tool that does not exist in the registry?",
         "2. Older agent runtimes asked the model to *write* its action as text and then ran an **output parser** over that text; a tool-calling model instead returns the call as structured data (a `name` and an `args` dictionary) that the runtime executes directly. Which class of failure does that design remove? Then work through a failure it does not remove: the correct tool is called but raises an exception while it runs. What happens to the rest of the run, and what must the tool's author do instead?"),
        ('3. The chapter lesson emphasizes that tool use is "what separates an AI agent from an LLM." Using the AgentExecutor architecture as a reference, explain exactly what structural capability the executor adds that a standalone LLM call does not have.',
         '3. The chapter lesson emphasizes that tool use is "what separates an AI agent from an LLM." Using the agent runtime as a reference, explain exactly what structural capability the agent adds that a standalone LLM call does not have.'),
        ("- **Five AgentExecutor structural components:**\n  1. *LLM backbone* — generates Thought and Action steps; the core reasoning engine.\n  2. *Tool registry* — a dictionary of registered tools with names, descriptions, and callable functions; the agent accesses it to know what actions are available.\n  3. *Output parser* — converts the LLM's raw text Action into a structured object (tool name + arguments) that can be executed.\n  4. *Action executor* — invokes the selected tool with the parsed arguments and returns the result.\n  5. *Memory module* — stores prior Thought/Action/Observation turns to provide the agent with conversational context across reasoning steps.",
         "- **Four structural components of the agent runtime:**\n  1. *LLM backbone* — the central reasoning engine; it reads the conversation so far and decides which action to take next, or that the question can now be answered.\n  2. *Tool registry* — the registered tools with their descriptions and input schemas; it is the whole set of actions the model may choose from, and the agent reads it to know what capabilities are available.\n  3. *Action executor* — the runtime that actually runs the chosen tool with the arguments the model supplied, and returns the result as the observation.\n  4. *Memory module* — carries conversation history, tool outputs and observations forward, so each turn of the loop sees what the previous turns produced.\n- **The fifth component that no longer exists:** older LangChain listed a fifth, an *output parser*, whose job was to convert the model's raw text Action into a structured tool call. A tool-calling model emits that structure directly — each entry in the message's `tool_calls` carries a `name` and an `args` dictionary — so there is no text left to parse and the component has no work to do. Four is the current count; if an older component list hands you five, the extra one is the parser. A figure that shows stopping criteria as a fifth row is counting something else again \u2014 the rule that ends the loop, not a part of the runtime."),
        ('- **Tool registry function:** Maps tool names (as strings) to tool objects (description + callable); the LLM reads tool descriptions from the registry to select the appropriate tool.',
         '- **Tool registry function:** Maps tool names (as strings) to tool objects (description + callable); the model reads those descriptions — for a `@tool` function the description is its docstring, unless an explicit `description=` overrides it — and selects a tool by naming it in a tool call.'),
        ('- **Malformed output handling:** If the output parser receives an unrecognized tool name, the executor raises a parsing error or invokes an error-handling fallback — the tool call does not execute silently.',
         '- **Tool failure handling:** Structured tool calls remove the text-parsing failure mode, but not tool failure. A tool that raises lets the exception propagate out of the agent and end the run, so the user gets a traceback and no answer. A production tool catches its own errors and returns a description of the failure, which reaches the model as an ordinary observation it can reason about — retrying with different arguments, switching tools, or reporting the limitation.'),
        ('- **Loop termination:** The loop terminates when the LLM generates a `Final Answer:` token (agent-side), or when a maximum step count is reached (framework-side hard stop).',
         "- **Loop termination:** The loop terminates when the LLM produces an answer instead of another action (agent-side), or when a step limit is reached (framework-side hard stop). In the paper's prompt format the agent signals completion with a finish action written as text; a modern tool-calling model signals it structurally, by returning a message that requests no tools, and the step limit is set by the `recursion_limit` config key rather than a `max_iterations` argument."),
        ('- LangChain AgentExecutor verbose output (from Lab Exercise Step 1).',
         '- The streamed agent trace printed by the `show_trace` helper in Lab Exercise Step 1 (`REASONING`, `TOOL CALL`, `ARGUMENTS`, `OBSERVATION`, `ANSWER` lines).'),
        ('In a verbose AgentExecutor output, which specific labeled elements constitute the reasoning trace? List them in order.',
         "In the streamed trace the lab's `show_trace` helper prints, which specific labeled lines constitute the reasoning trace? List them in order, and say which one may legitimately be missing from a correct run that did call a tool."),
        ('How does the trace structure map to this cycle — that is, where in a real verbose AgentExecutor output would you locate each of the three phases?',
         'How does the trace structure map to this cycle — that is, where in a real streamed trace would you locate each of the three phases, given that a model calling tools natively never writes the words "Thought:", "Action:" or "Observation:"?'),
        ('- **Reasoning trace elements (in order):** `Thought:` → `Action:` → `Action Input:` → `Observation:` (repeated per loop iteration) → `Final Answer:`.',
         "- **Reasoning trace elements (in order):** `REASONING:` (the model's own text, printed only when it chooses to narrate — frequently absent, and its absence is not a fault) → `TOOL CALL:` (the tool name) → `ARGUMENTS:` (the argument dictionary) → `OBSERVATION:` (the content the tool returned), repeated per loop iteration → `ANSWER:` (the last model message, the one that requests no tools)."),
        ('- **Production diagnostic requirement:** Verbose mode or structured logging must be enabled in deployment; a production agent without trace logging cannot be diagnosed post-failure.',
         '- **Production diagnostic requirement:** There is no `verbose=True` switch to turn on any more. The agent must be streamed (`agent.stream(..., stream_mode="updates")`) or otherwise instrumented so that every tool call, its arguments and the content the tool returned are recorded; a deployment that logs only the final answer cannot be diagnosed post-failure.'),
        ('- **Trace-to-cycle mapping:** `Thought:` = Thought phase; `Action:` + `Action Input:` = Action phase (tool name + arguments); `Observation:` = Observation phase (tool output).',
         '- **Trace-to-cycle mapping:** Thought phase = the model message\'s own `content` (the `REASONING:` line), which the model may omit entirely; Action phase = `tool_call["name"]` plus `tool_call["args"]` (the `TOOL CALL:` and `ARGUMENTS:` lines); Observation phase = the tool message\'s `content` (the `OBSERVATION:` line).'),
        ('  1. *Incorrect tool selection* — Trace shows Action naming the wrong tool for the sub-task. Root cause: tool description ambiguity or missing scope boundary. Fix: revise tool description.',
         '  1. *Incorrect tool selection* — The `TOOL CALL` line names the wrong tool for the sub-task. Root cause: tool description ambiguity or missing scope boundary. Fix: revise tool description.'),
        ('  2. *Malformed tool call* — Action phase names the correct tool but provides incorrect or malformed arguments. Root cause: ambiguous argument specification. Fix: clarify argument format and constraints in tool description.',
         '  2. *Malformed tool call* — `TOOL CALL` names the correct tool but `ARGUMENTS` carries incorrect or malformed values. Root cause: ambiguous argument specification. Fix: clarify argument format and constraints in tool description.'),
        ('  3. *Observation misinterpretation* — Correct tool is called with correct arguments; Observation is returned correctly; but the subsequent Thought misreads the Observation and draws an incorrect inference.',
         "  3. *Observation misinterpretation* — Correct tool is called with correct arguments and the `OBSERVATION` line shows a correct result, but the model's next message misreads it and draws an incorrect inference."),
        ('  4. *Premature termination* — Agent generates `Final Answer:` before the reasoning task is complete (e.g., after first tool call, regardless of whether sufficient information has been retrieved). Root cause: stopping condition is triggered too early; few-shot examples do not demonstrate multi-step loops. Fix: add few-shot demonstrations of multi-loop reasoning; adjust max_iterations.',
         '  4. *Premature termination* — Agent returns an answer message with no tool calls before the reasoning task is complete (e.g., after the first tool call, regardless of whether sufficient information has been retrieved). Root cause: stopping condition is triggered too early; the demonstrations do not show multi-step loops. Fix: add demonstrations of multi-loop reasoning. Separately, check whether the run was cut short by the `recursion_limit` config key, which replaced the old `max_iterations` argument.'),
        ('  5. *Hallucination in Thought* — Agent generates a Thought that asserts a false fact as if it were retrieved from a tool Observation, when no such Observation occurred.',
         '  5. *Hallucination in Thought* — The agent asserts a false fact in its own text — the `REASONING:` line, or the answer itself — as though a tool had returned it, when no `OBSERVATION` line contains it.'),
        ('- **Distinguishing incorrect tool selection vs. malformed tool call:** Incorrect tool selection is visible in the `Action:` line (wrong tool name); malformed tool call shows the correct tool name in `Action:` but incorrect content in `Action Input:`.',
         '- **Distinguishing incorrect tool selection vs. malformed tool call:** Incorrect tool selection is visible on the `TOOL CALL` line (wrong tool name); a malformed tool call shows the correct name on `TOOL CALL` but wrong content on `ARGUMENTS`.'),
        ('- **Trace-complete failure class:** Hallucination in Thought — the trace shows all phases correctly, but the Thought contains an asserted fact that was never returned by any tool Observation.',
         "- **Trace-complete failure class:** Hallucination in Thought — every step of the trace is well formed and no error is logged, but the model's text contains an asserted fact that no `OBSERVATION` line ever returned."),
        ('```\nThought: I need to find the current GDP of Brazil.\nAction: web_search\nAction Input: "Brazil GDP"\nObservation: [Search returned: "Brazil GDP 2023: $2.08 trillion (World Bank)"]\nThought: The search confirmed Brazil\'s GDP is $2.08 trillion. \n         I also know from context that Brazil\'s inflation rate in 2023 was 4.6%.\nFinal Answer: Brazil\'s GDP is $2.08 trillion and its inflation rate is 4.6%.\n```',
         "```\n[1] REASONING:  I need to find the current GDP of Brazil.\n[1] TOOL CALL:  web_search\n[1] ARGUMENTS:  {'query': 'Brazil GDP'}\n[1] OBSERVATION: Brazil GDP 2023: $2.08 trillion (World Bank)\n[final] ANSWER:  Brazil's GDP is $2.08 trillion. From what I know, its inflation rate in 2023 was 4.6%.\n```"),
        ('*(Answer: Hallucination in Thought — the inflation rate 4.6% was never returned by any Observation; it was inserted from parametric memory. Fix: add a system instruction requiring that all numerical claims be grounded in a tool Observation.)*',
         '*(Answer: Hallucination in Thought — the only `OBSERVATION` in the trace returned a GDP figure and nothing else, so the 4.6% inflation rate came from the model\'s parametric memory, which the answer all but admits with "From what I know". It is not premature termination: the agent did not stop short, it answered in full and sourced part of that answer from memory instead of a tool — premature termination means stopping before enough was gathered, hallucination means asserting what was never gathered. The trace is otherwise well formed: one tool call, one observation, one answer, no error. Fix: add a system instruction requiring that every numerical claim be grounded in a tool result, and read traces by checking each figure in the answer against the observations above it.)*'),
        ('Focus: four-component prompt architecture and cross-mapping to AgentExecutor components.',
         'Focus: four-component prompt architecture and cross-mapping to the four agent prompt engineering dimensions of Part B (system instructions, tool descriptions, few-shot CoT scaffolds, output format constraints).'),
        ('*(Reference readings: Brown et al. 2020, Wei et al. 2022 — revisit as needed for few-shot context; LangChain AgentExecutor system prompt design.)*',
         '*(Reference readings: Brown et al. 2020, Wei et al. 2022 — revisit as needed for few-shot context; the LangChain [Agents guide](https://docs.langchain.com/oss/python/langchain/agents) on the `system_prompt` argument to `create_agent`.)*'),
        ("  3. *Few-shot CoT scaffolds:* Demonstration examples showing the desired Thought-Action-Observation-Final Answer pattern — the agent's reasoning template.",
         "  3. *Few-shot CoT scaffolds:* Worked exchanges placed in the message list ahead of the real question — a user turn, the assistant's tool call, the tool's result, and the answer that followed — which the model reads as precedent for its own loop."),
        ('| Context | Tool descriptions + few-shot scaffolds | Web search tool description + Thought→Action→Obs demonstration |',
         '| Context | Tool descriptions + few-shot scaffolds | Web search tool docstring + a worked tool call → tool result → answer exchange |'),
        ("- *Output indicator → Output format constraints:* The required structure of the agent's Final Answer (section headers, citation format, word count, confidence levels).",
         "- *Output indicator → Output format constraints:* The required structure of the agent's final answer message (section headers, citation format, word count, confidence levels)."),
        ('  4. *Output format constraints:* Required structure, length, citation format, or confidence framing for the Final Answer.',
         '  4. *Output format constraints:* Required structure, length, citation format, or confidence framing for the final answer.'),
        ('| Output indicator | Output format constraints | "Final Answer must contain: Summary (≤100 words), Risk Level (High/Med/Low), Citations." |',
         '| Output indicator | Output format constraints | "Your final answer must contain: Summary (≤100 words), Risk Level (High/Med/Low), Citations." |'),
        # The lesson's dimension table is now text, not an image, and lists the same six as this guide.
        ('(from lesson image and text)',
         "(from the lesson's table and text)"),
    ],
    "modules/module-3/reading-guides.md": [
        ('- LangChain Documentation: Document Loaders, Text Splitters, Vector Stores, RetrievalQA',
         '- LangChain Documentation: Document Loaders, Text Splitters, Vector Stores, and the LangChain Expression Language (LCEL) runnables that compose them'),
        ("8. LangChain's RetrievalQA chain is the primary interface for Stage 6 in the lab. What does the `return_source_documents=True` parameter expose, and why is this output critical for diagnosing faithfulness failures (i.e., identifying when the LLM generates an answer that contradicts or goes beyond the retrieved context)?",
         "8. The lab composes Stage 6 explicitly rather than calling a prebuilt question-answering chain: `RunnableParallel(question=RunnablePassthrough(), source_documents=retriever)` fans the query out to the retriever, and a second step adds the generated `result`. What does the chain's `source_documents` key give you that the answer string alone does not, and why is this output critical for diagnosing faithfulness failures (i.e., identifying when the LLM generates an answer that contradicts or goes beyond the retrieved context)?"),
        ("What does this composition pattern enable that the older sequential chain API (RetrievalQA) does not? What specific optimization does LCEL's composability simplify?",
         "What does this composition pattern enable that the older prebuilt chain classes — `RetrievalQA` and its siblings, which packaged retrieve-then-generate into a single preconfigured call and were removed from `langchain` in 1.0 — did not? What specific optimization does LCEL's composability simplify?"),
    ],
    "modules/module-2/foundational-concepts.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Architects-Guide-to-Agents.png" width=900>',
         PAGE_DIAGRAMS['Architects-Guide-to-Agents|modules/module-2/foundational-concepts.md']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Chain-of-Thought.png" width=800>',
         IMAGE_TABLES['Chain-of-Thought']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Four-Paradigm-Comparative-Framework.png" width=800>',
         IMAGE_TABLES['Four-Paradigm-Comparative-Framework']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/ReAct-Phase.png" width=800>',
         IMAGE_TABLES['ReAct-Phase']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Reasoning-Trace-Failures.png" width=800>',
         IMAGE_TABLES['Reasoning-Trace-Failures']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Six-Dimensions-Trade-Off_Assessment.png" width=800>',
         IMAGE_TABLES['Six-Dimensions-Trade-Off_Assessment']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Agent-Prompt-Architecture.png" width=800>',
         IMAGE_TABLES['Agent-Prompt-Architecture']),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/AgentExecutor-Architecture.png" width=800>',
         M2_AGENT_RUNTIME),
        ("When set, the agent's output parser enforces this format rather than returning raw text.",
         "When set, that schema is imposed on the model's own output rather than recovered afterwards from text by an output parser. That is the general pattern in a tool-calling agent: an action comes back as a structured call — each entry in the message's `tool_calls` carries a `name` and an `args` dictionary — so there is nothing left for a parsing component to convert."),
        ('The agent returned by `create_agent` runs a LangGraph-backed ReAct loop internally: on each invocation, it iterates through Thought → tool call → Observation cycles until a terminal condition is reached, then produces a Final Answer in the specified response format. Unlike `AgentExecutor`, state management, loop control, and tool dispatch are handled by the underlying LangGraph execution graph — making the agent inherently compatible with checkpointing, streaming, and multi-agent orchestration.',
         'The agent returned by `create_agent` is a compiled graph that runs the ReAct loop internally: invoke it with `{"messages": [...]}` and it repeats a reasoning → tool call → observation cycle until the model returns a message that requests no tools. That message ends the run and carries the final answer, which you read from `result["messages"][-1].content`; the step cap is the `recursion_limit` config key. Unlike `AgentExecutor`, state management, loop control, and tool dispatch are handled by the underlying LangGraph execution graph — making the agent inherently compatible with checkpointing, streaming, and multi-agent orchestration. *Thought*, *Action* and *Observation* are the ReAct paper\'s names for the phases of that cycle, not labels the agent emits — the model\'s message carries structured `tool_calls`, and it is the Module 2 lab\'s `show_trace` helper that gives the steps printable names (`REASONING:` — only when the model narrates before calling — then `TOOL CALL:`, `ARGUMENTS:`, `OBSERVATION:` and `[final] ANSWER:`).'),
        ('* LangChain [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) verbose trace output.',
         '* LangChain [`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) — the streamed step trace from `agent.stream(..., stream_mode="updates")`, which the Module 2 lab wraps in its `show_trace` helper. There is no `verbose=True` switch to turn on.'),
        ('The ability to read and diagnose a ReAct trace - identifying which Thought step was faulty, which Act was incorrectly specified, or which Observe was\nmisinterpreted - is the core diagnostic skill of Module 2.',
         "The ability to read and diagnose a ReAct trace - identifying which piece of reasoning was faulty, which tool call was incorrectly specified, or which observation was misinterpreted - is the core diagnostic skill of Module 2. Thought, Act and Observe are the paper's names for the three phases, not labels a current agent prints: the Module 2 lab prints the same three steps as `REASONING:`, `TOOL CALL:` / `ARGUMENTS:` and `OBSERVATION:` lines."),
        ('`create_agent` accepts five primary parameters and returns a compiled, runnable agent:',
         "`create_agent` accepts five primary parameters — constructor arguments, not the agent's structural components — and returns a compiled, runnable agent:"),
    ],
    "modules/module-1/overview.md": [
        ('<img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Modern_AI_Stack.png" width=900>',
         ''),
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Module1_Units_Plan.png" width=700>',
         IMAGE_TABLES['Module1_Units_Plan']),
        # The labs moved from Claude Desktop to Ollama + Openwork on 2026-07-21; this objective predates that.
        ('3. Operate Claude Desktop on a basic agentic task.',
         "3. Operate a local agent interface (Openwork, or Claude Desktop's Cowork tab) on a basic agentic task."),
    ],
    "modules/module-4/foundational-concepts.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Three-Orchestration-Frameworks.png" width=700>',
         IMAGE_TABLES['Three-Orchestration-Frameworks']),
    ],
    "modules/module-1/readings/automation-and-multi-agent-frameworks.md": [
        ('<img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/AI_Automation_Ecosystem.png" width=900>',
         PAGE_DIAGRAMS['AI_Automation_Ecosystem|modules/module-1/readings/automation-and-multi-agent-frameworks.md']),
    ],
    "modules/module-1/resources.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Visual_vs_Programmatic.png" width=800>',
         PAGE_DIAGRAMS['Visual_vs_Programmatic|modules/module-1/resources.md']),
    ],
    "modules/module-2/overview.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/BuildingAIAutomationPipelines.png" width=900>',
         ''),
    ],
    "modules/module-3/overview.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/AI_Agent_Memory_Integration.png" width=900>',
         ''),
        ('| **Project** | Hands-On Project | Optimization Experiment Log + Token Budget Report + Brief Outline |',
         '| **Project** | Hands-On Project | Optimization Experiment Log + RAGAS interpretation, in the lab notebook |'),
    ],
    "modules/module-5/foundational-concepts.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/From-Prototype-to-Production.png" width=900>',
         ''),
    ],
    "modules/module-5/overview.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/ResponsibleAgenticAIControl.png" width=900>',
         PAGE_DIAGRAMS['ResponsibleAgenticAIControl|modules/module-5/overview.md']),
    ],
    "start-here/github-portfolio-setup.md": [
        ('<p><img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/AI_Professional_Portfolio_Guide.png" width=1000>',
         PAGE_DIAGRAMS['AI_Professional_Portfolio_Guide|start-here/github-portfolio-setup.md']),
    ],
    "archive/module-1/overview-draft-2026-06.md": [
        ('<img src="https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/blob/main/images/Modern_AI_Stack.png" width=900>',
         ''),
    ],
    "modules/module-1/chapter-quizzes.md": [
        # Four distractors were marked wrong while their feedback called them partially correct. Each option now
        # makes a claim that is wrong on its own terms, and its feedback says why. Keys are unchanged.
        # Chapter 1 Q1: a scheduled script also lacks pro-activeness, so the stem now shows the reactivity evidence
        # and C misdefines pro-activeness.
        ('**Question 1.** Wooldridge and Jennings (1995) define four properties that constitute a "weakly" intelligent agent. Which property is violated by a traditional rule-based automation script that executes a fixed sequence of steps in response to a scheduled trigger?',
         '**Question 1.** Wooldridge and Jennings (1995) define four properties that constitute a "weakly" intelligent agent. A traditional rule-based automation script runs at 6 a.m. every day and executes the same fixed sequence of steps whatever it finds — an empty inbox, a changed file format, a folder that no longer exists. Which property does this behavior most directly violate, and why?'),
        ('C. Pro-activeness — the script is triggered externally and therefore cannot take initiative toward its own design objectives.',
         'C. Pro-activeness — the script runs on a schedule, and pro-activeness is the property of acting on external triggers such as a clock.'),
        ('> ❌ **C is partially correct but imprecise.** Pro-activeness involves goal-directed initiative, and a script does not exhibit it in the full sense. However, the more precise violation in the description is reactivity: the script does not respond to environmental changes, period. A script could theoretically be triggered by an environmental event (making it superficially reactive) while still following a fixed sequence once triggered. The question specifies a "fixed sequence regardless of state," which targets reactivity directly.',
         '> ❌ **C is incorrect.** It misdefines pro-activeness. Pro-activeness is initiative that no trigger prompts — in the lesson\'s words, a pro-active agent "does not merely react to stimuli" — so acting when a clock fires is not what the property means. Firing on a timer does not make the script reactive either: reactivity is perceiving changes in the environment and responding to them, and the description shows the script ignoring every change it meets. That evidence is why the answer is reactivity, not the property this option misdefines.'),
        # Chapter 1 Q2: the lesson's table does put the loop-or-conclude decision in Observe, so A is now wrong
        # about Observe having no other job rather than about the decision.
        ("A. To evaluate whether the agent's overall goal has been achieved and terminate the loop if so.",
         'A. To make the stop-or-continue decision — that is its only job; the tool result itself is carried into the next step by the Plan stage.'),
        ('> ❌ **A is partially true but incomplete as the primary function.** Termination evaluation does occur during or after Observation — the agent determines whether the goal is met. But the primary mechanical function of the Observe stage is the context update (B), from which goal-completion evaluation derives. Describing Observation as primarily a termination check misses the broader role it plays in every iteration, not just the final one.',
         '> ❌ **A is incorrect.** Observe does include the stop-or-continue decision — the lesson\'s table says it "decides whether to loop again or conclude" — but that is not its only job, and the Plan stage does not carry the result forward. Observe reads the tool output and updates the agent\'s state, and the decision to loop or conclude is made from that updated state. Without the update in B there would be nothing to decide from, which is why B, not A, is the Observe stage\'s primary function.'),
        # Chapter 2 Q5: D's claim is true but answers a different question; only its feedback changes.
        ('> ❌ **D is partially true but not the primary reason for "absolute data governance."** Auditability through human-readable code is a genuine advantage of code-first automation for compliance purposes, but it addresses transparency, not data residency. An auditable system can still transmit data to third-party servers. The governance advantage identified in the Automation Landscape Overview is specifically about data residency and computational control, not code readability.',
         '> ❌ **D is incorrect.** Auditable code is a real advantage of code-first automation, but it answers a different question — can you inspect what the system does? — not where the data goes. An auditable system can still send every record to a third-party API. The governance advantage the Automation Landscape Overview describes is data residency: the whole system, model included, can run on infrastructure the organization controls, so the data never leaves it.'),
        # Chapter 5 Q1: the Audit does score workflows, so B now rests on a false premise (a running system).
        ('B. Measure — because the two-dimensional automation assessment produces quantitative scores that characterize workflow risk.',
         "B. Measure — because the Workflow Audit's scores measure how the automated workflows perform once they are running."),
        ("> ❌ **B is partially correct but is the weaker answer.** The two-dimensional automation assessment does produce scores that characterize risk properties, which is a Measure-like activity. However, Measure in the NIST framework specifically refers to analyzing and assessing identified risks using defined metrics — it presupposes that the Map function has already identified what to measure. The Workflow Audit's primary function is identification and contextualization (Map), not quantitative risk assessment (Measure), even though scoring is part of it.",
         '> ❌ **B is incorrect.** Its premise is wrong: the Audit scores candidate workflows before anything is automated, so there is no running system whose performance could be measured. Its two scores record properties of each workflow — how rule-based it is and how severe its errors would be — and that is identifying context and risk, which is Map. In the AI RMF, Measure "uses knowledge relevant to AI risks identified in the MAP function" to analyze, assess, benchmark and monitor those risks, including by testing AI systems before deployment and regularly while in operation.'),
    ],
    "modules/module-4/chapter-quizzes.md": [
        # Three distractors were marked wrong while their feedback called them partially applicable or valid. Each
        # now rests on a false premise or proposes a fix that would not fix the problem. Keys are unchanged.
        ('A. Task specialization — because reading papers and synthesizing across papers require different cognitive skills, justifying separate specialist agents for each sub-task.',
         'A. Task specialization — because no single model can both summarize individual papers and synthesize across them, so each sub-task needs its own specialist agent.'),
        ('> ❌ **A is partially applicable but is not the most precise justification.** Task specialization is relevant if reading and synthesis genuinely require different prompting strategies or tool access. However, a capable LLM can handle both reading and synthesis within a single agent. Task specialization is a weaker justification here than context window limitation, which is a hard constraint rather than a quality optimization.',
         "> ❌ **A is incorrect.** Its premise is false: one capable model can summarize a paper and also synthesize across papers; the two sub-tasks call for different prompts, not different models. Task specialization can improve quality, but it does not make a multi-agent design necessary here. What does is the hard limit in B: 500 full papers cannot fit into any single agent's context window."),
        ('C. Cross-agent quality control — because a separate critic agent should verify each paper summary before it is used in the final synthesis.',
         'C. Cross-agent quality control — because the task specification requires a separate critic agent to verify each paper summary before synthesis.'),
        ('> ❌ **C is partially applicable but is not the primary justification.** Cross-agent quality control adds value if summary verification is a bottleneck or if the generator agent cannot reliably critique its own summaries. While a critic agent may improve quality, this condition does not explain why MAS is structurally necessary — it explains why it might be qualitatively superior. Context window limitation makes MAS necessary; cross-agent quality control makes it better.',
         '> ❌ **C is incorrect.** The task as described asks for no verification step, so a critic cannot be what justifies the architecture. A critic agent might well improve the summaries, but that would make a multi-agent design better, not necessary. The constraint the task does impose — all 500 papers read and summarized before synthesis — is one no single context window can hold.'),
        ('C. It fails to calculate the coordination overhead ratio, which is required before making any recommendation.',
         'C. The only thing missing is the coordination overhead ratio; adding that number would turn the paragraph into a formal recommendation.'),
        ('> ❌ **C is partially valid** but not the main issue. Calculating the ratio is required, but the primary failure is the absence of a committed position.',
         '> ❌ **C is incorrect.** The coordination overhead ratio is useful evidence — the lesson uses it to judge whether a system spends more effort coordinating than producing — but adding it would not fix this paragraph. It would still describe trade-offs without choosing between them. What makes a recommendation formal is a committed position with stated conditions, and no additional metric supplies that.'),
    ],
}

# Regex clean-ups applied after PATCHES (pattern, replacement) keyed by dest.
REGEX_PATCHES: dict[str, list[tuple[str, str]]] = {
    # The wiki's "Connecting CrewAi and LangChain" section is a verbatim copy of the LangChain
    # example above it (same intro, same code, same closing paragraph): drop the duplicate.
    "modules/module-1/resources.md": [
        (r"\*\*Connecting CrewAi and LangChain\*\*\n\nHere is a quick code example[\s\S]*?\n```\n\nIn this setup, the `@tool` decorator[^\n]*\n", ""),
    ],
    # the quiz specification draft has 14 empty "Question N" headings after the single authored question
    "archive/module-1/concept-quiz-spec-draft.md": [
        # the four options are <br>-separated lines; make them a real list
        (r"^([A-D])\.\s+(.+?)\s*<br>\s*$", r"- **\1.** \2"),
        (r"(?:^#{3,4} Question (?:[2-9]|1[0-5])\s*\n+)+\Z",
         "*Questions 2-15 were never authored in this wiki draft; the complete quiz is the live [Module 1 Concept Quiz](../../modules/module-1/concept-quiz.md).*\n"),
    ],
}

# Alt text for referenced images (fallback: humanized filename).
ALT_TEXT = {
    "Module1_ActivitySkillMatrix.png": "Module 1 activity-skill alignment matrix",

}

# One-column callout table header -> (admonition kind, title)
CALLOUT_MAP = [
    (r"^hint$", "tip", "Hint"),
    (r"^note$", "note", "Note"),
    (r"^example$", "example", "Example"),
    (r"^common mistake", "warning", "Common mistake — read before submitting"),
    (r"^question$", "question", "Question"),
    (r"^what to submit$", "info", "What to submit"),
    (r"^platform setup", "warning", "Platform setup — read before starting"),
    (r"^summative submission$", "example", "Summative submission"),
    (r"^grade weight summary$", "info", "Grade weight summary"),
    (r"^instructor note$", "info", "Instructor note"),
    (r"^competency description$", "abstract", "General course competencies"),
    (r"^your workflow audit$", "example", "Your Workflow Audit"),
    (r"^tier ", "info", None),   # Overview2 tiered learning-objective tables keep their own header as title
]

SECTION_META: dict[str, tuple[str, str]] = {
    "start-here": ("Start here", "How the course works, the syllabus, your GitHub portfolio, and how to run the labs."),
    "modules": ("Modules", "The five course modules, each budgeted at eight hours: overview, foundational concepts, reading guides, activities, labs, chapter quizzes, and resources."),
    "modules/module-1": ("Module 1: From Prompts to Pipelines", "Thinking like an automation designer: what agents are, the automation spectrum, hands-on agent labs, and your Workflow Audit."),
    "modules/module-1/readings": ("Module 1 Readings", "Course reading packages for Module 1."),
    "modules/module-1/worksheets": ("Module 1 Worksheets", "Fill-in worksheets used in the Module 1 activities (drafts under construction)."),
    "modules/module-2": ("Module 2: Agent Reasoning Architectures and Tool Integration", "How agents reason and act: Chain-of-Thought, ReAct, Tree of Thoughts, LATS, tool integration with LangChain, prompt design, and trace evaluation."),
    "modules/module-3": ("Module 3: Memory Architectures and RAG", "Parametric and non-parametric memory, the six-stage RAG pipeline, conversational memory patterns, retrieval optimization, and RAGAS evaluation."),
    "modules/module-4": ("Module 4: Multi-Agent Systems", "Coordination architectures, LangGraph and CrewAI implementation, the three-role pipeline, and coordination-failure diagnosis."),
    "modules/module-5": ("Module 5: Responsible Agentic AI", "Production deployment, multi-dimensional evaluation, observability with LangSmith, OWASP Top 10 for LLM applications, and EU AI Act / NIST AI RMF governance."),
    "course-design": ("Course design", "Instructor-facing design documents: the formal learning design, development plan, instructor materials, and the July 2026 course review."),
    "about": ("About", "License and attribution, how to contribute, how AI agents should consume this site, and the wiki-to-site crosswalk."),
    "archive": ("Archive", "Superseded wiki pages kept for history. Each page names the live page that replaced it."),
}

MODULE_MATERIALS = {
    1: [("materials/module1/module1_quiz.html", "Module 1 concept quiz (interactive HTML)"),
        ("materials/module1/Module_1_Quiz.pdf", "Module 1 concept quiz (printable PDF)"),
        ("materials/module1/diagnostic_survey.html", "Diagnostic knowledge survey (interactive HTML)"),
        ("materials/module1/Diagnostic_Knowledge_Survey.pdf", "Diagnostic knowledge survey (printable PDF)"),
        ("materials/module1/Illustrated_AI_Glossary.docx", "Illustrated AI glossary worksheet (Word)")],
    2: [("materials/module2/Module-2-Guided-Lab-Notebook.ipynb", "Module 2 guided lab notebook")],
    3: [("materials/module3/Module-3-Lab.ipynb", "Module 3 RAG lab notebook"),
        ("materials/module3/NIST.AI.100-1.pdf", "Lab corpus 1: NIST AI 100-1, AI Risk Management Framework (PDF)"),
        ("materials/module3/NIST.AI.600-1.pdf", "Lab corpus 2: NIST AI 600-1, Generative AI Profile (PDF)")],
    4: [("materials/module4/Module4_Learner_Starter.ipynb", "Module 4 learner starter notebook")],
    5: [("materials/module5/Module5_Learner_Starter.ipynb", "Module 5 learner starter notebook")],
}

WARNINGS: list[str] = []
ERRORS: list[str] = []


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"WARN  {msg}")


def err(msg: str) -> None:
    ERRORS.append(msg)
    print(f"ERROR {msg}")


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------

_GIT_CACHE: dict[str, tuple[list[str], str]] = {}


def git_provenance(src: str) -> tuple[list[str], str]:
    """Return (authors oldest-first unique, last_modified ISO) for a wiki file."""
    if src in _GIT_CACHE:
        return _GIT_CACHE[src]
    try:
        out = subprocess.run(["git", "-C", str(WIKI_DIR), "log", "--follow", "--format=%an|%aI", "--", src],
                             check=True, capture_output=True, text=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        out = ""
    authors: list[str] = []
    last = ""
    for i, line in enumerate(l for l in out.splitlines() if "|" in l):
        name, date = line.split("|", 1)
        name = CREDIT_NAMES.get(name.strip(), name.strip())
        if i == 0:
            last = date.strip()
        if name not in authors:
            authors.append(name)
    authors.reverse()
    _GIT_CACHE[src] = (authors, last)
    return authors, last


FOOTER_RE = re.compile(
    r"^\s*\**\s*(?P<key>Created|Craeted|Updated?|Update)\s*:\**\s*(?P<m>\d{2})/(?P<d>\d{2})/(?P<y>\d{4})\.?\s*\(\s*(?P<who>[^)]*?)\s*\)\.?\**\s*(?:<br\s*/?>)?\s*$",
    re.M | re.I)


def extract_footer(text: str) -> tuple[dict, str]:
    """Pull the wiki's Created/Updated lines into an authorship dict and remove them (and a preceding rule)."""
    meta: dict = {}
    contributors: list[str] = []
    positions: list[tuple[int, int]] = []
    for m in FOOTER_RE.finditer(text):
        key = m.group("key").lower()
        iso = f"{m.group('y')}-{m.group('m')}-{m.group('d')}"
        meta["created" if key.startswith("c") else "updated"] = iso
        for who in re.split(r"[;,]\s*|\s+and\s+", m.group("who")):
            who = CREDIT_NAMES.get(who.strip(), who.strip())
            if who and who not in contributors:
                contributors.append(who)
        positions.append(m.span())
    for start, end in reversed(positions):
        text = text[:start] + text[end:]
    if contributors:
        meta["contributors"] = contributors
    # drop a trailing rule / stray asterisks left above the footer
    text = re.sub(r"(?:\n\s*(?:\*{3,}|-{3,}|_{3,})\s*)+\s*\Z", "\n", text)
    return meta, text.rstrip() + "\n"


# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------

FENCE_OPEN_RE = re.compile(r"^\s{0,3}(```|~~~)(.*)$")


def mask_fences(text: str) -> tuple[str, list[str]]:
    out: list[str] = []
    blocks: list[str] = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = FENCE_OPEN_RE.match(lines[i])
        if m:
            marker = m.group(1)
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith(marker):
                j += 1
            block = "\n".join(lines[i:j + 1])
            blocks.append(block)
            out.append(f"\x00FENCE{len(blocks) - 1}\x00")
            i = j + 1
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out), blocks


def unmask_fences(text: str, blocks: list[str], default_lang: str = "text") -> str:
    def repl(m: re.Match) -> str:
        block = blocks[int(m.group(1))]
        first, _, rest = block.partition("\n")
        if re.fullmatch(r"\s*(```|~~~)\s*", first):
            first = first.rstrip() + default_lang
        return first + "\n" + rest if rest or "\n" in block else first
    return re.sub(r"\x00FENCE(\d+)\x00", repl, text)


def is_heading(line: str) -> bool:
    return bool(re.match(r"^#{1,6}\s", line))


def heading_level(line: str) -> int:
    return len(re.match(r"^(#+)", line).group(1))


LIST_ITEM_RE = re.compile(r"^(?P<indent>[ \t]*)(?:[-*+]|\d+[.)])\s+\S")


def ensure_blank_before_lists(text: str) -> str:
    """Insert a blank line between a paragraph line and a list that follows it.

    GitHub's Markdown starts a list right after a paragraph line; Python-Markdown (what
    Zensical renders with) does not, and swallows the items into the paragraph with their
    literal "- "/"1. " markers visible. The wiki relies on the GitHub behaviour in dozens
    of places, so normalize it here. Fenced code is already masked when this runs.
    """
    lines = text.split("\n")
    out: list[str] = []
    for line in lines:
        m = LIST_ITEM_RE.match(line)
        if m and out:
            prev = out[-1]
            indent = m.group("indent")
            same_block = prev.strip() and prev[:len(indent)] == indent and not prev[len(indent):len(indent) + 1].isspace()
            prev_is_list = bool(LIST_ITEM_RE.match(prev))
            prev_is_boundary = (
                not prev.strip()
                or prev.lstrip().startswith(("#", "|", "!!!", "???", ">", "\x00FENCE"))
                or prev.rstrip().endswith(("  ", "<br>", "<br/>"))
            )
            if same_block and not prev_is_list and not prev_is_boundary:
                out.append("")
        out.append(line)
    return "\n".join(out)


def relpath(target: str, dest: str) -> str:
    """Relative link from page `dest` (docs-relative) to docs-relative `target`."""
    return posixpath.relpath(target, posixpath.dirname(dest) or ".")


def humanize(name: str) -> str:
    stem = posixpath.splitext(name)[0]
    return re.sub(r"[-_]+", " ", stem).strip()


# ---------------------------------------------------------------------------
# Transformations
# ---------------------------------------------------------------------------

def split_addendum(text: str, part: str) -> str:
    """Split a two-document Addendum at the second H1."""
    lines = text.split("\n")
    h1s = [i for i, l in enumerate(lines) if re.match(r"^# ", l)]
    if len(h1s) < 2:
        err(f"cannot split addendum: fewer than two H1 headings")
        return text
    cut = h1s[1]
    if part == "A":
        head = lines[:cut]
        while head and re.fullmatch(r"\s*(?:\*{3,}|-{3,}|_{3,})?\s*", head[-1]):
            head.pop()
        return "\n".join(head) + "\n"
    return "\n".join(lines[cut:]) + "\n"


def html_to_markdown(text: str) -> str:
    """Convert the two full-HTML wiki pages to Markdown (markdownify), protecting GFM tables."""
    from bs4 import BeautifulSoup
    from markdownify import markdownify

    text = re.sub(r"(?is)\A\s*<html>\s*<head>\s*</head>\s*<body>\s*", "", text)
    text = re.sub(r"(?is)\s*</body>\s*</html>\s*\Z", "\n", text)
    # protect pipe tables (they are plain text inside the HTML)
    tables: list[str] = []

    def keep_table(m: re.Match) -> str:
        tables.append(m.group(0).strip("\n"))
        return f"\n\n<p>TABLEPLACEHOLDER{len(tables) - 1}</p>\n\n"

    text = re.sub(r"(?:^[ \t]*\|.*\|?[ \t]*\n?){2,}", keep_table, text, flags=re.M)
    text = re.sub(r"<p>\s*(<hr\s*/?>)\s*</p>", r"\1", text, flags=re.I)
    text = re.sub(r"</p>\s*(?=<(?:p|h[1-6]|ul|ol|hr|table)\b)", "</p>\n\n", text, flags=re.I)
    text = re.sub(r"(</h[1-6]>)\s*(?=<)", r"\1\n\n", text, flags=re.I)
    soup = BeautifulSoup(text, "html.parser")
    md = markdownify(str(soup), heading_style="ATX", bullets="-", strong_em_symbol="*",
                     escape_underscores=False, escape_asterisks=False, escape_misc=False)
    md = re.sub(r"^\s*\* \* \*\s*$", "---", md, flags=re.M)
    md = re.sub(r"<hr\s*/?>", "---", md)

    def restore(m: re.Match) -> str:
        return "\n\n" + tables[int(m.group(1))] + "\n\n"

    md = re.sub(r"TABLEPLACEHOLDER(\d+)", restore, md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip("\n") + "\n"


def strip_comments_and_banners(text: str) -> tuple[str, bool]:
    text = re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)
    under_construction = False
    if re.search(r"^\s*\U0001F6A7", text, flags=re.M):
        under_construction = True
        text = re.sub(r"^\s*\U0001F6A7.*$\n?", "", text, flags=re.M)
    # reviewer parentheticals like (** 👁️‍🗨️ ... **) and the eye emoji itself
    text = re.sub(r"\s*\(\*\*\s*(?:" + re.escape(EYE) + r"\s*)+[^*]*?\*\*\)", "", text)
    # strip the emoji and any spaces that followed it (spaces only, never a newline), so a
    # leading "**👁️‍🗨️  Reading Guide" does not leave "** Reading Guide" with unclosable bold
    text = re.sub(re.escape(EYE) + r" *", "", text)
    text = text.replace(":open_file_folder:", "")
    return text, under_construction


IMG_HTML_RE = re.compile(
    r"(?:<p>\s*)?<img\s+src=\"https://github\.com/UA-AI2S/[^/\"]+/blob/main/images/(?P<name>[^\"?]+)\"(?:\s+width=\"?(?P<w>\d+)\"?)?\s*/?>(?:\s*</p>)?",
    re.I)
IMG_MD_RE = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\(https://github\.com/UA-AI2S/[^/)]+/blob/main/images/(?P<name>[^)?\s]+)(?:\?[^)]*)?\)")
USED_IMAGES: set[str] = set()


def convert_images(text: str, page: Page) -> str:
    rel_dir = relpath("assets/images", page.dest)

    def build(name: str, width: str | None, alt: str | None = None) -> str:
        name = urllib.parse.unquote(name)
        if not (ASSETS_DIR / "images" / name).exists() and not (ROOT / "images" / name).exists():
            err(f"{page.dest}: referenced image not found in sources: {name}")
        USED_IMAGES.add(name)
        alt_text = ALT_TEXT.get(name) or alt or humanize(name)
        attr = f'{{ width="{width}" }}' if width else ""
        return f"\n\n![{alt_text}]({rel_dir}/{name}){attr}\n\n"

    text = IMG_HTML_RE.sub(lambda m: build(m.group("name"), m.group("w")), text)
    text = IMG_MD_RE.sub(lambda m: build(m.group("name"), None, m.group("alt")), text)
    return text


ALERT_RE = re.compile(r"^\s{0,3}>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$")
ALERT_KIND = {"NOTE": "note", "TIP": "tip", "IMPORTANT": "info", "WARNING": "warning", "CAUTION": "danger"}


CALLOUT_QUOTE_RE = re.compile(r"^\s{0,3}>\s*\*\*[⚠✦]?\s*(?P<k>Note|Tip):\*\*\s*(?P<rest>.*)$")


def convert_alerts(text: str) -> str:
    """GitHub alerts (> [!NOTE]) and '> **⚠ Note:**' style blockquotes -> admonitions."""
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        m = ALERT_RE.match(lines[i])
        q = CALLOUT_QUOTE_RE.match(lines[i]) if not m else None
        if not m and not q:
            out.append(lines[i])
            i += 1
            continue
        if m:
            kind = ALERT_KIND[m.group(1)]
            first_body: list[str] = []
        else:
            kind = q.group("k").lower()
            first_body = [q.group("rest").strip()] if q.group("rest").strip() else []
        body: list[str] = list(first_body)
        j = i + 1
        while j < len(lines) and re.match(r"^\s{0,3}>", lines[j]):
            body.append(re.sub(r"^\s{0,3}>\s?", "", lines[j]).rstrip())
            j += 1
        body = [re.sub(r"\s*<br\s*/?>\s*$", "", b) for b in body]
        while body and not body[0].strip():
            body.pop(0)
        title = kind.capitalize() if kind != "info" else "Important"
        if body and m:
            tm = re.match(r"^\s*(?:\U0001F4CC\s*)?\*\*(?P<t>[^*]+?)\s*:?\*\*\s*:?\s*(?P<rest>.*)$", body[0])
            if tm:
                # keep the 📌 pin: the source page tells readers annotations carry that icon
                title = tm.group("t").strip().rstrip(":").strip()
                rest = tm.group("rest").strip()
                body[0] = rest
                if not rest:
                    body.pop(0)
                while body and not body[0].strip():
                    body.pop(0)
        out.append(f'!!! {kind} "{title}"')
        out.append("")
        for b in body:
            out.append(("    " + b) if b.strip() else "")
        out.append("")
        i = j
    return "\n".join(out)


TABLE_HEADER_RE = re.compile(r"^\|\s*(?P<h>[^|]+?)\s*\|\s*$")
TABLE_DELIM_RE = re.compile(r"^\|?\s*:?-{2,}:?\s*\|?\s*$")


def callout_for(header: str) -> tuple[str, str]:
    link = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", header.strip())
    if link:
        return "info", f"Next: {link.group(1)}"
    plain = re.sub(r"[*_`]", "", header).strip()
    key = re.sub(r"[^a-z0-9 ]+", " ", plain.lower()).strip()
    key = re.sub(r"\s+", " ", key)
    for pattern, kind, title in CALLOUT_MAP:
        if re.search(pattern, key):
            return kind, (title or plain)
    warn(f"one-column table header not in CALLOUT_MAP, using note: {plain!r}")
    return "note", plain


def convert_callout_tables(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        m = TABLE_HEADER_RE.match(lines[i])
        if m and i + 1 < len(lines) and TABLE_DELIM_RE.match(lines[i + 1]) and lines[i + 1].count("|") <= 2:
            header = m.group("h")
            rows: list[str] = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                cell = lines[j].strip()
                cell = cell[1:] if cell.startswith("|") else cell
                cell = cell[:-1] if cell.endswith("|") else cell
                rows.append(cell.strip())
                j += 1
            kind, title = callout_for(header)
            out.append(f'!!! {kind} "{title}"')
            out.append("")
            if kind == "info" and title.startswith("Next:"):
                out.append("    " + header.strip())
                out.append("")
            for row in rows:
                parts = [p.strip() for p in re.split(r"<br\s*/?>", row) if p.strip()]
                for p in parts:
                    out.append("    " + p)
                out.append("")
            i = j
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def convert_answer_keys(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # (a) blockquote "> **Correct Answer: X**"
        if re.match(r"^\s*>\s*\*\*Correct Answer", line):
            body: list[str] = []
            j = i
            while j < n and re.match(r"^\s*>", lines[j]):
                body.append(re.sub(r"^\s*>\s?", "", lines[j]).rstrip())
                j += 1
            out.append('??? success "Show answer and feedback"')
            out.append("")
            for b in body:
                out.append(("    " + b) if b.strip() else "")
            out.append("")
            i = j
            continue
        # (b) "**Feedback:**" paragraphs (Module 5, Module 3 chapter 3)
        if re.match(r"^\*\*Feedback:\*\*\s*$", line):
            body = []
            j = i + 1
            while j < n and not re.match(r"^(#{1,6}\s|---\s*$|\*\*Question\b)", lines[j]):
                body.append(lines[j].rstrip())
                j += 1
            while body and not body[-1].strip():
                body.pop()
            correct = ""
            for b in body:
                cm = re.match(r"^\*\*([A-D])\.?\*\*\s*\u2705", b)
                if cm:
                    correct = cm.group(1)
                    break
            out.append('??? success "Show answer and feedback"')
            out.append("")
            if correct:
                out.append(f"    **Correct answer: {correct}**")
                out.append("")
            for b in body:
                out.append(("    " + b) if b.strip() else "")
            out.append("")
            i = j
            continue
        # (c) inline "*(Answer: ...)*"
        m = re.match(r"^\*\(Answer:\s*(.*)\)\*\s*$", line)
        if m:
            out += ['??? success "Answer"', "", "    " + m.group(1).strip(), ""]
            i += 1
            continue
        # (d) archived self-assessment "### Answer Key — Quiz N" + table
        m = re.match(r"^###\s+Answer Key\s*[—–-]\s*Quiz\s*(\d+)\s*$", line)
        if m:
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            table: list[str] = []
            while j < n and lines[j].strip().startswith("|"):
                table.append(lines[j].rstrip())
                j += 1
            out.append(f'??? note "Answer key — Quiz {m.group(1)}"')
            out.append("")
            for t in table:
                out.append("    " + t)
            out.append("")
            i = j
            continue
        # (e) Act-8 "Answer: **B**" + rationale bullets
        m = re.match(r"^Answer:\s*\*\*([A-D])\*\*\s*$", line)
        if m:
            body = []
            j = i + 1
            while j < n and (not lines[j].strip() or lines[j].lstrip().startswith(("-", "*"))):
                if lines[j].strip():
                    body.append(lines[j].rstrip())
                j += 1
                if j < n and lines[j].strip().startswith("---"):
                    break
            out.append('??? success "Answer and rationale"')
            out.append("")
            out.append(f"    **Answer: {m.group(1)}**")
            out.append("")
            for b in body:
                out.append("    " + b)
            out.append("")
            i = j
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


PREFIX_RE = re.compile(r"^(#{1,6})\s+(?:[a-f]\.?|i{1,3}\.?|iv\.?|v\.?)\s+(?=\S)")
TIME_RE = re.compile(r"\s*[\[(]\s*~\s*(?P<t>[^\])]*?)\s*[\])]\s*$")
TIME_LINE_RE = re.compile(r"^\*\*Time\*?\*?\s*:?\*?\*?\s*:?\s*(?P<t>.+?)\s*$", re.M)


def fix_headings(text: str, page: Page) -> str:
    lines = text.split("\n")

    # 1. drop the wiki's title / subtitle heading lines
    dropped = 0
    if page.drop_title:
        idx = next((k for k, l in enumerate(lines[:20]) if is_heading(l)), None)
        if idx is not None:
            del lines[idx]
            dropped = 1
            if page.drop_title >= 2:
                k = idx
                # Skip the hero figure sitting between the title and its subtitle. It is either
                # the wiki's image, or the sentence and ```mermaid block that replaced it, so
                # allow blank lines freely but at most one prose line and one fenced block --
                # enough for the figure, too little to swallow a real heading further down.
                prose = fences = 0
                while k < len(lines):
                    stripped = lines[k].strip()
                    if not stripped or lines[k].startswith("!["):
                        k += 1
                    elif re.fullmatch(r"\x00FENCE\d+\x00", stripped) and not fences:
                        # Fenced code is masked to a placeholder before the line rules run,
                        # so the hero's ```mermaid block reaches here as a single token.
                        fences += 1
                        k += 1
                    elif not is_heading(lines[k]) and not prose:
                        prose += 1
                        k += 1
                    else:
                        break
                if k < len(lines) and is_heading(lines[k]) and heading_level(lines[k]) == 2:
                    del lines[k]
                    dropped = 2
        if dropped < page.drop_title:
            warn(f"{page.dest}: expected to drop {page.drop_title} title heading(s), dropped {dropped}")

    # 2. per-line heading fixes
    fixed: list[str] = []
    for line in lines:
        if not is_heading(line):
            fixed.append(line)
            continue
        line = PREFIX_RE.sub(r"\1 ", line).rstrip()
        line = re.sub(r"^(#+)\s{2,}", r"\1 ", line)
        time_note = ""
        tm = TIME_RE.search(line)
        if tm and "~" in tm.group(0):
            line = line[:tm.start()].rstrip()
            time_note = f"*Estimated time: ~{tm.group('t').strip()}*"
        line = re.sub(r"^(#+\s+.*?)\s*[:.]\s*$", r"\1", line)
        # link-only heading -> heading + button
        lm = re.match(r"^(#+)\s+\[([^\]]+)\]\(([^)]+)\)\s*$", line)
        if lm:
            fixed.append(f"{lm.group(1)} {lm.group(2).strip()}")
            fixed.append("")
            fixed.append(f"[Take the {lm.group(2).strip()}]({lm.group(3)}){{ .md-button }}")
        else:
            fixed.append(line)
        if time_note:
            fixed.append("")
            fixed.append(time_note)
            fixed.append("")   # the estimate is its own paragraph; a list may follow it
    lines = fixed

    # 3. Module 5 addendum: merge "## Chapter N Reading Guide/Quiz" + "### Subtitle"
    merged: list[str] = []
    k = 0
    while k < len(lines):
        m = re.match(r"^## (Chapter \d+ (?:Reading Guide|Quiz))\s*$", lines[k])
        if m:
            j = k + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and re.match(r"^### \S", lines[j]):
                subtitle = lines[j][4:].strip()
                sep = " — " if ":" in subtitle else ": "   # avoid "Quiz: Responsible AI: Governance"
                merged.append(f"## {m.group(1)}{sep}{subtitle}")
                k = j + 1
                continue
        merged.append(lines[k])
        k += 1
    lines = merged
    lines = [re.sub(r"^#### (What to Focus On|Active Reading Tasks)\s*$", r"### \1", l) for l in lines]

    # 4. pseudo-headings
    lines = [re.sub(r"^\*\*Question (\d+(?:\.\d+)?)\.?\*\*\s*(.*)$", lambda m: f"### Question {m.group(1)}" + (f"\n\n{m.group(2).strip()}" if m.group(2).strip() else ""), l) for l in lines]
    lines = "\n".join(lines).split("\n")
    lines = [re.sub(r"^\*\*(Section [A-D]\s*[—–-]\s*.+?)\*\*\s*$", r"#### \1", l) for l in lines]
    lines = [re.sub(r"^\*\*(Prompt \d+\s*[—–-]\s*.+?)\*\*\s*$", r"#### \1", l) for l in lines]

    # 5. pinned ids on reading-guide and quiz section headings
    def pin(l: str) -> str:
        m = re.match(r"^## (Reading Guide (\d+)\b.*)$", l)
        if m and "{ #" not in l:
            return f"## {m.group(1)} {{ #reading-guide-{m.group(2)} }}"
        m = re.match(r"^## (Chapter (\d+) Reading Guide\b.*)$", l)
        if m and "{ #" not in l:
            return f"## {m.group(1)} {{ #reading-guide-{m.group(2)} }}"
        m = re.match(r"^## (Chapter (\d+) Quiz\b.*)$", l)
        if m and "{ #" not in l:
            return f"## {m.group(1)} {{ #chapter-{m.group(2)}-quiz }}"
        return l
    lines = [pin(l) for l in lines]

    # 6. empty "Chapter N Quiz" headings in the lesson pages -> button to the quiz page
    if page.type == "Lesson":
        result: list[str] = []
        for idx, l in enumerate(lines):
            result.append(l)
            m = re.match(r"^#{2,6}\s+Chapter (\d+) Quiz\s*$", l)
            if m:
                nxt = next((x for x in lines[idx + 1:] if x.strip()), "")
                if not nxt or is_heading(nxt) or re.fullmatch(r"\s*(\*{3,}|-{3,})\s*", nxt):
                    result.append("")
                    result.append(f"[Take the Chapter {m.group(1)} quiz](chapter-quizzes.md#chapter-{m.group(1)}-quiz){{ .md-button }}")
        lines = result

    # 7. single H1: demote stray H1s, insert ours, then normalize the minimum level to 2
    lines = [("#" + l if re.match(r"^# ", l) else l) for l in lines]
    levels = [heading_level(l) for l in lines if is_heading(l)]
    if levels and min(levels) > 2:
        shift = min(levels) - 2
        lines = [l[shift:] if is_heading(l) else l for l in lines]
    return "\n".join(lines)


WIKI_LINK_RE = re.compile(
    r"\]\((?:https?://github\.com/UA-AI2S/AI-Automation-and-Agents(?:-v2)?/wiki/?)"
    r"(?P<page>[^()\s#]*(?:\([^()\s]*\)[^()\s#]*)*)(?P<frag>#[^)\s]*)?\)")
BLOB_LINK_RE = re.compile(
    r"\]\(https?://github\.com/UA-AI2S/AI-Automation-and-Agents(?:-v2)?/blob/main/(?P<path>[^)\s]+?)\)")
SURVEY_URL_RE = re.compile(r"\]\(https?://ua-ai2s\.github\.io/website-home/aiautomation/html/(?P<file>[^)\s]+)\)")
EXTERNAL_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\((https?://[^)\s]+)\)(?!\{)")

LINK_MAP: dict[str, str] = {}
QUIZ_DEST: dict[str, str] = {}   # reading-guide dest -> quiz dest


def build_link_map() -> None:
    for p in PAGES:
        if not p.src:
            continue
        if p.part == "B":
            continue
        LINK_MAP[p.wiki_name] = p.dest
    for p in PAGES:
        if p.part == "B":
            a = next(q for q in PAGES if q.src == p.src and q.part == "A")
            QUIZ_DEST[a.dest] = p.dest
    for name, dest in DROPPED.items():
        LINK_MAP[name] = dest
    LINK_MAP["Module-1"] = "modules/module-1/overview.md"
    LINK_MAP[""] = "index.md"
    # ASCII-hyphen variants for the U+2010 names
    for name in list(LINK_MAP):
        if HYPHEN_U2010 in name:
            LINK_MAP[name.replace(HYPHEN_U2010, "-")] = LINK_MAP[name]


def resolve_wiki_link(page_name: str, frag: str, page: Page) -> str | None:
    name = unicodedata.normalize("NFC", urllib.parse.unquote(page_name)).rstrip("/")
    dest = LINK_MAP.get(name) or LINK_MAP.get(name.replace(HYPHEN_U2010, "-"))
    if dest is None:
        return None
    if dest == "":
        return None
    new_frag = ""
    if frag:
        f = frag[1:]
        m = re.match(r"chapter-(\d+)-quiz", f)
        if m and dest in QUIZ_DEST:
            dest = QUIZ_DEST[dest]
            new_frag = f"#chapter-{m.group(1)}-quiz"
        else:
            m = re.match(r"reading-guide-(\d+)", f)
            if m:
                new_frag = f"#reading-guide-{m.group(1)}"
            else:
                warn(f"{page.dest}: dropping unmapped fragment {frag} on link to {name}")
    return relpath(dest, page.dest) + new_frag


def convert_links(text: str, page: Page) -> str:
    def wiki(m: re.Match) -> str:
        target = resolve_wiki_link(m.group("page"), m.group("frag") or "", page)
        if target is None:
            err(f"{page.dest}: unresolved wiki link to {m.group('page')!r}")
            return m.group(0)
        return f"]({target})"

    text = WIKI_LINK_RE.sub(wiki, text)

    def blob(m: re.Match) -> str:
        path = urllib.parse.unquote(m.group("path"))
        nb = re.match(r"materials/module(\d)/[^/]+\.ipynb$", path)
        if nb:
            return f"]({relpath(f'modules/module-{nb.group(1)}/lab-notebook.md', page.dest)})"
        if path.startswith("docs/AI_Automation_Agents_Syllabus_v2.pdf"):
            return f"]({relpath('assets/files/AI_Automation_Agents_Syllabus_v2.pdf', page.dest)})"
        if path.startswith("materials/"):
            return f"]({relpath(path, page.dest)})"
        if path.startswith("images/"):
            return f"]({relpath('assets/' + path, page.dest)})"
        warn(f"{page.dest}: unhandled blob link {path}")
        return m.group(0)

    text = BLOB_LINK_RE.sub(blob, text)

    def survey(m: re.Match) -> str:
        f = m.group("file")
        target = "modules/module-1/diagnostic-survey.md" if "survey" in f else "modules/module-1/concept-quiz.md"
        return f"]({relpath(target, page.dest)})"

    text = SURVEY_URL_RE.sub(survey, text)
    text = re.sub(r"^\*(https?://\S+?)\*\s*$", r"<\1>", text, flags=re.M)
    text = EXTERNAL_LINK_RE.sub(r"[\1](\2){target=_blank}", text)
    return text


def fix_misc(text: str, page: Page) -> str:
    lines = text.split("\n")
    out: list[str] = []
    last_top_level_list_item = False
    for l in lines:
        s = l
        if page.pandoc and re.match(r"^\s+-{6,}(\s+-+)*\s*$", s):
            continue
        if re.fullmatch(r"\s*(\*{3,}|_{3,}|-{3,}|\u2014{3,})\s*", s):
            out.append("---")
            continue
        if not s.strip():
            out.append("")
            continue
        in_table = s.lstrip().startswith("|")
        if not in_table:
            s = re.sub(r"(?:\s*<br\s*/?>)+\s*$", "", s)
            s = re.sub(r"^\s*<p>\s*", "", s)
            s = s.replace("</p>", "")
        else:
            # keep a 4-space indent (a table nested in an admonition or ??? collapsible
            # body); drop a stray 1-3 space indent, and never let the whitespace collapse
            # below eat the indent itself
            raw_indent = len(s) - len(s.lstrip())
            indent = "    " if raw_indent >= 4 else ""
            s = s.strip()
            s = s.replace("&emsp;", "")
            s = indent + re.sub(r"[ \t]{2,}", " ", s)
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            if page.pandoc and cells and all(not c for c in cells):
                s = "| Term | Details |"   # Act-3 glossary table has an empty header row
            elif "&nbsp;" in s and all(re.fullmatch(r"(&nbsp;|\s)*", c) for c in cells):
                continue   # worksheet filler rows
        s = s.replace("&rarr;", "→")
        s = re.sub(r"<(?=\d)", "&lt;", s)
        s = re.sub(r"^(\s*)\+\s+", r"\1- ", s)
        # the wiki nests sub-bullets with 2-3 spaces, which GitHub accepts but
        # Python-Markdown flattens; promote them to a real 4-space nest, but only
        # when the enclosing list item starts at column 0
        m_list = re.match(r"^(?P<indent> {1,3})(?:[-*+]|\d+[.)])\s+\S", s)
        if m_list and last_top_level_list_item:
            s = "    " + s.lstrip()
        elif re.match(r"^(?:[-*+]|\d+[.)])\s+\S", s):
            last_top_level_list_item = True
        elif not s.strip():
            pass
        elif not s.startswith(" "):
            last_top_level_list_item = False
        out.append(s)
    text = "\n".join(out)
    if page.pandoc:
        text = re.sub(r"(?<=\S) --- (?=\S)", " — ", text)
        text = re.sub(r"(?<=\w)---(?=\w)", "—", text)
        text = re.sub(r"(?<=\w)--(?=\w)", "–", text)
    # the wiki numbers the ReAct stages "**1. Perceive:**" then "&rarr; **2. Plan...**";
    # make the arrow optional so all four become one ordered list numbered 1-4
    text = re.sub(r"^(?:→\s*)?\*\*(\d+)\.\s*", r"\1. **", text, flags=re.M)
    text = ensure_blank_before_lists(text)
    # rules: drop those adjacent to headings/admonitions, consecutive ones, and at the ends
    lines = text.split("\n")
    cleaned: list[str] = []
    for idx, l in enumerate(lines):
        if l == "---":
            prev = next((x for x in reversed(cleaned) if x.strip()), "")
            nxt = next((x for x in lines[idx + 1:] if x.strip()), "")
            if not prev or not nxt or is_heading(prev) or is_heading(nxt) or prev == "---" \
                    or nxt.startswith(("???", "!!!")) or prev.startswith("    ") or re.match(r"^\*Estimated time", prev):
                continue
        cleaned.append(l)
    text = ensure_blank_before_lists("\n".join(cleaned))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip("\n") + "\n"


# Google-Docs-exported templates in the portfolio tutorial: (start regex, end regex, language,
# regex that must have been seen inside the region before the end regex counts).
GDOCS_FENCES = [
    (r"^\\# AI Automation and Agents — Digital Portfolio", r"^your@email", "markdown", None),
    (r"^\\# Module 01", r"^\\- What evaluation metrics", "markdown", None),
    (r"^\\# Learning Log", r"^\\---\s*$", "markdown", r"^\\#\\#\\#\\# Next steps"),
    (r"^\\# Good — specific", r"^changes\s*$", "text", None),
    (r"^\\# Clone your repository", r"^git push origin main", "bash", None),
    (r"^\\# Repository name", r"non-descriptive\s*$", "text", None),
]
UNESCAPE_RE = re.compile(r"\\([#*_\[\]()+.`>|\-])")


def fix_gdocs(text: str) -> str:
    """Portfolio tutorial: fence the escaped Google-Docs templates, then unescape prose."""
    lines = text.split("\n")
    fenced: list[str] = []
    active: tuple[str, re.Pattern, re.Pattern | None] | None = None
    gate_seen = False
    for l in lines:
        if active is None:
            hit = next(((s, e, lang, g) for s, e, lang, g in GDOCS_FENCES if re.match(s, l)), None)
            if hit:
                _, end, lang, gate = hit
                active = (lang, re.compile(end), re.compile(gate) if gate else None)
                gate_seen = gate is None
                fenced.append("")
                fenced.append(f"```{lang}")
                fenced.append(UNESCAPE_RE.sub(r"\1", l))
                continue
            fenced.append(l)
            continue
        lang, end_re, gate_re = active
        if l.strip() == "```":
            continue  # inner fences around tables become part of the template
        if gate_re and gate_re.search(l):
            gate_seen = True
        unescaped = UNESCAPE_RE.sub(r"\1", l)
        # search, not match: several end markers sit at the end of a line
        # ("Untitled.ipynb   \# non-descriptive"), and an unmatched end swallows the page tail
        if gate_seen and end_re.search(l):
            if not re.match(r"^\\---", l):
                fenced.append(unescaped)
            while fenced and not fenced[-1].strip():
                fenced.pop()
            fenced.append("```")
            fenced.append("")
            active = None
            continue
        # Google Docs doubles blank lines inside templates; keep single blanks
        if not unescaped.strip() and fenced and not fenced[-1].strip():
            continue
        fenced.append(unescaped)
    if active is not None:
        fenced.append("```")
    text = "\n".join(fenced)
    text = UNESCAPE_RE.sub(r"\1", text)
    # manual contents block -> removed (the theme renders a table of contents)
    text = re.sub(r"^## Contents\s*\n(?:\d+\.\s+\[[^\]]+\]\(#[^)]*\)\s*\n?)+", "", text, flags=re.M)
    # stray <br> inside legitimate code fences (the directory tree)
    out: list[str] = []
    in_fence = False
    for l in text.split("\n"):
        if l.strip().startswith("```"):
            in_fence = not in_fence
        elif in_fence:
            l = re.sub(r"\s*<br\s*/?>", "", l)
        out.append(l)
    return "\n".join(out)


def apply_patches(text: str, page: Page) -> str:
    for old, new in PATCHES.get(page.dest, []):
        if old not in text:
            err(f"{page.dest}: patch text not found: {old[:70]!r}")
            continue
        text = text.replace(old, new, 1)
    for pattern, new in REGEX_PATCHES.get(page.dest, []):
        text, n = re.subn(pattern, new, text, flags=re.M)
        if n == 0:
            err(f"{page.dest}: regex patch matched nothing: {pattern[:70]!r}")
    return text


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def frontmatter(page: Page, meta: dict, authors: list[str], last_modified: str) -> str:
    fm: dict = {"title": page.title, "description": page.description, "type": page.type, "tags": page.tags}
    if page.module:
        fm["module"] = page.module
    if page.time_estimate:
        fm["time_estimate"] = page.time_estimate
    fm["status"] = page.status or "stable"
    stale = page.stale_after or (STALE_TOOLS if any(t in TOOL_TAGS for t in page.tags) else "")
    if stale:
        fm["stale_after"] = stale
    if page.superseded_by:
        fm["superseded_by"] = relpath(page.superseded_by, page.dest)
    fm["generated"] = {"by": GENERATED_BY, "at": GENERATED_AT}
    src = {
        "id": "wiki-v2",
        "resource": WIKI_BASE + urllib.parse.quote(page.wiki_name, safe=":()-._~"),
        "title": f"AI Automation and Agents v2 wiki: {page.wiki_name}",
        "author": "; ".join(authors) if authors else "team:ua-ai2s",
    }
    if last_modified:
        src["last_modified"] = last_modified
    fm["sources"] = [src, *page.extra_sources]
    if meta:
        fm["authorship"] = meta
    fm["wiki_page"] = page.wiki_name
    dumped = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=10000, default_flow_style=False)
    return f"---\n{dumped}---\n"


def lifecycle_admonition(page: Page) -> str:
    if page.status == "deprecated":
        live = next((p.title for p in PAGES if p.dest == page.superseded_by), None) or HAND_TITLES.get(page.superseded_by, "the current page")
        body = page.note or f"This page is kept for history. The current version is [{live}]({relpath(page.superseded_by, page.dest)})."
        title = "Historical document" if page.note else "Superseded"
        return f'!!! warning "{title}"\n\n    {body}\n\n'
    if page.status == "draft":
        return '!!! note "Draft"\n\n    This page is still being written; content may change.\n\n'
    return ""


HAND_TITLES = {
    "modules/module-1/concept-quiz.md": "Module 1 Concept Quiz",
    "modules/module-1/diagnostic-survey.md": "Diagnostic Knowledge Survey",
    "index.md": "AI Automation and Agents",
}


def provenance_line(page: Page, last_modified: str) -> str:
    wiki_url = WIKI_BASE + urllib.parse.quote(page.wiki_name, safe=":()-._~")
    changed = f" (wiki page last changed {last_modified[:10]})" if last_modified else ""
    return (f'<p class="course-provenance" markdown>Migrated from the [course wiki]({wiki_url}){{target=_blank}}{changed}. '
            f'Spotted a problem? [Edit this page]({EDIT_BASE}{page.dest}){{target=_blank}}.</p>\n')


def convert_page(page: Page, raw_full: str) -> str:
    meta, text = extract_footer(raw_full)
    if page.part:
        text = split_addendum(text, page.part)
    text = apply_patches(text, page)
    if page.html_body:
        text = convert_images(text, page)   # keep the width attribute before markdownify sees the <img>
        text = html_to_markdown(text)
    text, under_construction = strip_comments_and_banners(text)
    if under_construction and not page.status:
        page.status = "draft"
    tm = TIME_LINE_RE.search(text)
    if tm and page.type == "Overview":
        page.time_estimate = tm.group("t").strip()
        text = TIME_LINE_RE.sub("", text, count=1)
    if page.gdocs:
        text = fix_gdocs(text)
    text, fences = mask_fences(text)
    text = convert_images(text, page)
    text = convert_alerts(text)
    text = convert_callout_tables(text)
    text = convert_answer_keys(text)
    text = fix_headings(text, page)
    text = convert_links(text, page)
    text = fix_misc(text, page)
    text = unmask_fences(text, fences, default_lang="text")
    authors, last_modified = git_provenance(page.src)
    parts = [frontmatter(page, meta, authors, last_modified), f"# {page.title}\n\n"]
    if page.lead:
        parts.append(f"*{page.lead}*\n\n")
    if page.time_estimate:
        parts.append(f"**Time:** {page.time_estimate}\n\n")
    parts.append(lifecycle_admonition(page))
    parts.append(text.strip("\n") + "\n\n")
    parts.append(provenance_line(page, last_modified))
    return "".join(parts)


# ---------------------------------------------------------------------------
# Indexes and crosswalk
# ---------------------------------------------------------------------------

def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def nav_order(root: Path) -> list[str]:
    cfg = root / "zensical.toml"
    if not cfg.exists():
        return []
    try:
        data = tomllib.loads(cfg.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return []
    order: list[str] = []

    def walk(items) -> None:
        if isinstance(items, str):
            order.append(items)
        elif isinstance(items, list):
            for it in items:
                walk(it)
        elif isinstance(items, dict):
            for v in items.values():
                walk(v)

    walk(data.get("project", {}).get("nav", []))
    return order


def write_indexes(out_root: Path) -> list[str]:
    written: list[str] = []
    order = nav_order(ROOT)
    rank = {p: i for i, p in enumerate(order)}

    def entries(section: str) -> list[tuple[str, dict]]:
        d = out_root / section
        items: list[tuple[str, dict]] = []
        for f in sorted(d.glob("*.md")) if d.exists() else []:
            if f.name == "index.md":
                continue
            fm = read_frontmatter(f)
            if not fm.get("title"):
                continue
            items.append((f.name, fm))
        items.sort(key=lambda t: (rank.get(f"{section}/{t[0]}", 10_000), t[0]))
        return items

    def bullet(link: str, fm: dict) -> str:
        suffix = ""
        if fm.get("status") == "deprecated":
            suffix = " *(archived)*"
        elif fm.get("status") == "draft":
            suffix = " *(draft)*"
        return f"* [{fm['title']}]({link}) - {fm.get('description', '').strip()}{suffix}"

    for section, (title, blurb) in SECTION_META.items():
        d = out_root / section
        if not d.exists():
            continue
        lines = [f"# {title}", "", blurb, ""]
        if section == "modules":
            for n in range(1, 6):
                mt, mb = SECTION_META[f"modules/module-{n}"]
                lines.append(f"* [{mt}](module-{n}/index.md) - {mb}")
        elif section == "archive":
            for sub in ("module-1", "module-2"):
                for name, fm in entries(f"archive/{sub}"):
                    lines.append(bullet(f"{sub}/{name}", fm))
        else:
            for name, fm in entries(section):
                lines.append(bullet(name, fm))
            for sub in ("readings", "worksheets"):
                if (d / sub / "index.md").exists() or (d / sub).is_dir():
                    st, sb = SECTION_META.get(f"{section}/{sub}", (sub.title(), ""))
                    lines.append(f"* [{st}]({sub}/index.md) - {sb}")
        m = re.fullmatch(r"modules/module-(\d)", section)
        if m:
            n = int(m.group(1))
            lines += ["", "## Materials", ""]
            for path, label in MODULE_MATERIALS[n]:
                lines.append(f"* [{label}]({relpath(path, section + '/index.md')})")
        content = "\n".join(lines).rstrip() + "\n"
        target = d / "index.md"
        write_if_changed(target, content)
        written.append(str(target.relative_to(out_root)))
    return written


def write_crosswalk(out_root: Path) -> str:
    rows: list[str] = []
    all_names = sorted(p.stem for p in WIKI_DIR.glob("*.md"))
    for name in all_names:
        url = WIKI_BASE + urllib.parse.quote(name, safe=":()-._~")
        pages = [p for p in PAGES if p.wiki_name == name]
        if pages:
            targets = ", ".join(f"[{p.title}]({relpath(p.dest, 'about/wiki-crosswalk.md')})" for p in pages)
            disp = "split into two pages" if len(pages) > 1 else ("archived (deprecated)" if pages[0].status == "deprecated" else "migrated")
        elif name in DROPPED:
            dest = DROPPED[name]
            if name == "_Sidebar":
                targets, disp = "site navigation", "not a page: became the nav in zensical.toml"
            elif name == "Home":
                targets, disp = f"[Home]({relpath('index.md', 'about/wiki-crosswalk.md')})", "hand-written landing page"
            elif name == "_Footer":
                targets, disp = f"[License and attribution]({relpath(dest, 'about/wiki-crosswalk.md')})", "footer text moved to the site footer and this page"
            else:
                targets, disp = f"[Module 2 Reading Guides]({relpath(dest, 'about/wiki-crosswalk.md')})", "dropped: near-duplicate of Module-2.2-Addendum"
        else:
            targets, disp = "", "UNMAPPED"
            err(f"crosswalk: wiki page {name!r} has no mapping")
        rows.append(f"| [{name}]({url}){{target=_blank}} | {targets} | {disp} |")
    body = (
        "---\n"
        'title: "Wiki-to-site crosswalk"\n'
        'description: "Where every page of the original GitHub wiki lives on this site: migrated, split, archived, or dropped."\n'
        "type: Reference\n"
        "tags: [course, instructor-facing, crosswalk, wiki]\n"
        "status: stable\n"
        "generated:\n"
        f'  by: "{GENERATED_BY}"\n'
        f'  at: "{GENERATED_AT}"\n'
        "sources:\n"
        "  - id: wiki-v2\n"
        f'    resource: "{WIKI_BASE}"\n'
        '    title: "AI Automation and Agents v2 wiki"\n'
        '    author: "team:ua-ai2s"\n'
        "---\n\n"
        "# Wiki-to-site crosswalk\n\n"
        f"The course content was migrated from the [GitHub wiki]({WIKI_BASE}){{target=_blank}} (commit `{WIKI_REF[:12]}`) "
        "by `scripts/migrate_wiki.py`. This table maps every wiki page to its destination on this site.\n\n"
        "| Wiki page | Site page(s) | Disposition |\n| --- | --- | --- |\n"
        + "\n".join(rows) + "\n"
    )
    target = out_root / "about" / "wiki-crosswalk.md"
    write_if_changed(target, body)
    return "about/wiki-crosswalk.md"


def write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Self checks
# ---------------------------------------------------------------------------

BANNED = [
    (re.compile(r"github\.com/UA-AI2S/[^/\s)]+/blob/main/images"), "blob image URL"),
    (re.compile(r"^\s*>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", re.M), "GitHub alert"),
    (re.compile(r"<p><img"), "raw <p><img"),
    (re.compile(r"^>\s*\*\*Correct Answer", re.M), "exposed answer key"),
    (re.compile(r"^\*\*Feedback:\*\*", re.M), "exposed feedback block"),
    (re.compile(EYE), "reviewer eye emoji"),
    (re.compile("\U0001F6A7"), "construction banner"),
]


def self_check(out_root: Path, dests: list[str]) -> None:
    for dest in dests:
        path = out_root / dest
        if not path.exists():
            err(f"{dest}: not written")
            continue
        text = path.read_text(encoding="utf-8")
        body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
        body_no_prov = "\n".join(l for l in body.split("\n") if "course-provenance" not in l)
        masked, _ = mask_fences(body_no_prov)
        h1 = len(re.findall(r"^# ", masked, flags=re.M))
        if h1 != 1:
            err(f"{dest}: expected exactly one H1, found {h1}")
        for rx, label in BANNED:
            if rx.search(masked):
                err(f"{dest}: {label} still present")
        if re.search(r"github\.com/UA-AI2S/AI-Automation-and-Agents(?:-v2)?/wiki/", masked):
            err(f"{dest}: wiki URL still present in body")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def check_refs() -> None:
    if os.environ.get("SKIP_REF_CHECK"):
        return
    for label, d, ref in (("WIKI_DIR", WIKI_DIR, WIKI_REF), ("ASSETS_DIR", ASSETS_DIR, ASSETS_REF)):
        try:
            head = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            sys.exit(f"error: {label} {d} is not a git checkout; clone the source repo there or set SKIP_REF_CHECK=1")
        if head != ref:
            sys.exit(f"error: {label} is at {head[:12]} but the pipeline is pinned to {ref[:12]} "
                     f"(git -C {d} checkout {ref}, or bump the constant deliberately)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="write to a temp dir and diff against docs/")
    ap.add_argument("--only", help="process a single wiki page (filename)")
    ap.add_argument("--notebooks", action="store_true", help="also run scripts/render_notebooks.py")
    args = ap.parse_args()

    if not WIKI_DIR.is_dir():
        sys.exit(f"error: WIKI_DIR {WIKI_DIR} not found")
    check_refs()
    build_link_map()

    wiki_files = {p.name for p in WIKI_DIR.glob("*.md")}
    mapped = {p.src for p in PAGES} | {f"{n}.md" for n in DROPPED}
    missing = wiki_files - mapped
    extra = mapped - wiki_files
    if missing:
        err(f"wiki pages without a PAGES/DROPPED entry: {sorted(missing)}")
    if extra:
        err(f"PAGES entries whose wiki file does not exist: {sorted(extra)}")

    out_root = Path(tempfile.mkdtemp(prefix="migrate-check-")) if args.check else DOCS
    if args.check:
        # seed the temp tree with frozen/hand pages so indexes can read their frontmatter
        for f in DOCS.rglob("*.md"):
            rel = f.relative_to(DOCS)
            (out_root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, out_root / rel)

    dests: list[str] = []
    changed = 0
    frozen_kept = 0
    for page in PAGES:
        if args.only and page.src != args.only:
            continue
        raw = (WIKI_DIR / page.src).read_text(encoding="utf-8").replace("\r\n", "\n")
        raw = unicodedata.normalize("NFC", raw)
        target = out_root / page.dest
        if page.frozen and target.exists():
            frozen_kept += 1
            dests.append(page.dest)
            continue
        content = convert_page(page, raw)
        if write_if_changed(target, content):
            changed += 1
        dests.append(page.dest)

    if not args.only:
        write_indexes(out_root)
        write_crosswalk(out_root)
        (ROOT / ".sources").mkdir(exist_ok=True)
        (ROOT / ".sources" / "used_images.json").write_text(json.dumps(sorted(USED_IMAGES), indent=2) + "\n")
    self_check(out_root, dests)

    if args.notebooks:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "render_notebooks.py")], check=False)

    if args.check:
        drift = []
        for f in out_root.rglob("*.md"):
            rel = f.relative_to(out_root)
            if not (DOCS / rel).exists() or not filecmp.cmp(f, DOCS / rel, shallow=False):
                drift.append(str(rel))
        shutil.rmtree(out_root)
        if drift:
            err(f"--check: {len(drift)} file(s) differ from docs/: {drift[:15]}")
        else:
            print("--check: docs/ is up to date with the pinned wiki")

    print(f"\n{len(dests)} pages processed, {changed} written, {frozen_kept} frozen kept, "
          f"{len(USED_IMAGES)} images referenced; {len(ERRORS)} error(s), {len(WARNINGS)} warning(s).")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
