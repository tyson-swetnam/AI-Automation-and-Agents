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
    2: "Supplementary notes for Module 2 comparing LLM agent reasoning paradigms (Chain-of-Thought, ReAct, Tree of Thoughts, LATS), the Belief-Desire-Intention model, and how LangChain's AgentExecutor runs the ReAct loop.",
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
         lead="The course team tracks development milestones in a shared spreadsheet (a University of Arizona login may be required)."),
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
PATCHES: dict[str, list[tuple[str, str]]] = {
    "modules/module-1/foundational-concepts.md": [
        ("* Merrill, M. D. (2002). [First principles of instruction](https://link.springer.com/content/pdf/10.1007/bf02505024.pdf). Educational technology research and development, 50(3), 43-59 (**👁️‍🗨️ 👁️‍🗨️ 👁️‍🗨️ Remove this source - not related to course**)\n", ""),
        ("* Wiggins, G. P., & McTighe, J. (2005). [Understanding by design](https://pdfs.semanticscholar.org/03e8/20730a873e7f44dbb1f64e4f047b9b321460.pdf). Ascd (**👁️‍🗨️ 👁️‍🗨️ 👁️‍🗨️ Remove this source - not related to course**)\n", ""),
        ("### Three Automation Paradigms:", "**Three automation paradigms**\n"),
    ],
    "modules/module-1/activities.md": [
        ("### a. Self-Check Prompts", "## a. Self-Check Prompts"),
    ],
    "modules/module-2/activities.md": [
        ("👁️‍🗨️ (Write language about providing thoughtful feedback to two peers on their proposals)",
         "!!! warning \"Under construction\"\n\n    Guidance on giving thoughtful feedback to two peers on their proposals is still being written."),
    ],
    "modules/module-2/chapter-quizzes.md": [
        ("> **Correct Answer: B or C depending on interpretation; B is the strongest answer.**",
         "> **Correct Answer: B** (an instructor review is pending: C is defensible under another interpretation)"),
    ],
    "modules/module-3/activities.md": [
        ("### Notebook Flow Summary", "### Guided lab notebook flow"),
        ("### Notebook Flow Summary", "### Project notebook flow"),
    ],
    "modules/module-4/activities.md": [
        ("### Notebook Flow Summary", "### Guided lab notebook flow"),
        ("### Notebook Flow Summary", "### Project notebook flow"),
    ],
    "modules/module-5/activities.md": [
        ("### Notebook Flow Summary", "### Guided lab notebook flow"),
        ("### Notebook Flow Summary", "### Project notebook flow"),
    ],
    "modules/module-3/chapter-quizzes.md": [
        ("# Module 3 — Chapter 3 Quiz\n## Conversational Memory Management", "## Chapter 3 Quiz — Conversational Memory Management"),
    ],
    "modules/module-1/readings/what-is-an-agent.md": [
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
        ("### Academic References", "## Academic References"),
    ],
    "course-design/course-review-2026-07.md": [
        ("## Module-by-Module Analysis\n", ""),
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
    "2D-Automation-AssessmentMatrix.png": "Two-dimensional automation assessment matrix",
    "Agent-Prompt-Architecture.png": "Agent prompt architecture",
    "AgentExecutor-Architecture.png": "LangChain AgentExecutor architecture",
    "AI_Agent_Memory_Integration.png": "AI agent memory integration",
    "AI_Automation_Agents.png": "AI Automation and Agents course banner",
    "AI_Automation_Ecosystem.png": "The AI automation ecosystem",
    "AI_Professional_Portfolio_Guide.png": "AI professional portfolio guide",
    "Architects-Guide-to-Agents.png": "An architect's guide to agents",
    "Automation_Tools.png": "Automation tools landscape",
    "Automation-Designers-LP.png": "Thinking like an automation designer",
    "Blooms_Spiral_Progression.png": "Bloom's spiral progression across the course",
    "BuildingAIAutomationPipelines.png": "Building AI automation pipelines",
    "Chain-of-Thought.png": "Chain-of-thought prompting",
    "Chunking-Strategy-Selection.png": "Chunking strategy selection",
    "Critical_Distinctions.png": "Critical distinctions between agents and other systems",
    "Decoding_AI_Agents.png": "Decoding AI agents",
    "Four_PIllars_AI_Literacy.png": "The four pillars of AI literacy",
    "Four_Stage_Agent_Loop.png": "The four-stage agent loop",
    "Four-Paradigm-Comparative-Framework.png": "Four-paradigm comparative framework",
    "Four-RAGAS-Metrics.png": "The four RAGAS metrics",
    "From-Prototype-to-Production.png": "From prototype to production",
    "Journey-to-AI-Agency.png": "Journey to AI agency",
    "Mastering-Responsible-AgenticAI.png": "Mastering responsible agentic AI",
    "Modern_AI_Stack.png": "The modern AI stack",
    "Module1_ActivitySkillMatrix.png": "Module 1 activity-skill alignment matrix",
    "Module1_Units_Plan.png": "Module 1 units plan",
    "ModuleLearningActivitiesDescription1.png": "Module learning activities (part 1)",
    "ModuleLearningActivitiesDescription2.png": "Module learning activities (part 2)",
    "Multi-Agent-Orchestration-Map.png": "Multi-agent orchestration map",
    "Path-to-AI-Memory.png": "The path to AI memory",
    "ReAct-Phase.png": "Phases of the ReAct loop",
    "Reasoning-Trace-Failures.png": "Reasoning trace failure modes",
    "ResponsibleAgenticAIControl.png": "Responsible agentic AI control",
    "Six-Dimensions-Trade-Off_Assessment.png": "Six-dimension trade-off assessment",
    "SIx-Functional-Stages-RAG.png": "The six functional stages of RAG",
    "StandardActivityStructurePerModule.png": "Standard activity structure per module",
    "The_New_Frontier.png": "The new frontier of AI agents",
    "Three-Orchestration-Frameworks.png": "Three orchestration frameworks: LangGraph, AutoGen, CrewAI",
    "Three-RAG-Failure-Modes.png": "Three RAG failure modes",
    "Three-RAG-Paradigms2.png": "Three RAG paradigms",
    "Visual_vs_Programmatic.png": "Visual versus programmatic automation",
    "Workflow_Automation_Components.png": "Workflow automation components",
    "WorkflowAuditProject-Rubric.png": "Workflow Audit project rubric",
    "WorkflowMapping-Template.png": "Workflow mapping template",
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
    3: [("materials/module3/Module-3-Lab.ipynb", "Module 3 RAG lab notebook")],
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
                # skip blank lines and the hero image between the title and its subtitle
                while k < len(lines) and k < idx + 8 and (not lines[k].strip() or lines[k].startswith("![")):
                    k += 1
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
