---
title: "Labs, Colab, and API keys"
description: "How the four guided lab notebooks run in Google Colab, which model providers each one supports, how to keep API keys out of your notebooks with Colab Secrets or getpass, what the labs cost, and how to save your work to your portfolio."
type: Guide
tags: [course, student-facing, labs, colab, langchain, langgraph, crewai, langsmith, ollama, api-keys, portfolio]
time_estimate: "15 minutes"
status: stable
stale_after: "2027-09-01T00:00:00Z"
generated:
  by: "claude/fable-5-1"
  at: "2026-09-09T00:00:00Z"
sources:
  - id: nb-module2
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module2/Module-2-Guided-Lab-Notebook.ipynb"
    title: "Module 2 Guided Lab: Building a Multi-Tool ReAct Agent (notebook)"
    author: "UA-AI2S course team"
  - id: nb-module3
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module3/Module-3-Lab.ipynb"
    title: "Module 3 Lab — Building a RAG Pipeline with LangChain + Chroma (notebook)"
    author: "UA-AI2S course team"
  - id: nb-module4
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module4/Module4_Learner_Starter.ipynb"
    title: "Module 4 Lab (Learner Starter) — Three-Role Pipeline in LangGraph and CrewAI (notebook)"
    author: "UA-AI2S course team"
  - id: nb-module5
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/module5/Module5_Learner_Starter.ipynb"
    title: "Module 5 Lab (Learner Starter) — LangSmith Tracing and a Comparative Observability Study (notebook)"
    author: "UA-AI2S course team"
  - id: wiki-m2-activities
    resource: "https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2:-Activities"
    title: "AI Automation and Agents v2 wiki: Module-2:-Activities (platform setup and submission rules; the same boxes appear on the Module 3-5 activities pages)"
    author: "Carlos Lizárraga-Celaya; Michelle Yung"
---

# Labs, Colab, and API keys

Modules 2 to 5 each have one guided lab that you complete in a Jupyter
notebook on **Google Colab**. The free Colab tier is enough; you do not need a
paid subscription. What you *do* need is a Google account, and for most labs
an API key for a language-model provider (or a local Ollama model as the free
alternative). This page covers the practical side: how to open and run a
notebook, how to handle keys safely, what to expect in cost, and how to turn a
finished notebook into a portfolio submission.

Module 1's two labs are different: they install
[Ollama](https://ollama.com/){target=_blank} and
[Openwork](https://openworklabs.com/){target=_blank} on your own computer and
need no notebook. They are described on the
[Module 1 activities page](../modules/module-1/activities.md).

## The four lab notebooks

Each lab has a page on this site with the notebook rendered as text, an *Open
in Colab* button and a download link. Read the module's activities page
first; it holds the *Platform setup* and *What to submit* boxes.

| Module | Lab page and notebook | What you build | Frameworks | Time |
| :-- | :-- | :-- | :-- | :-- |
| 2 | [Module 2 lab](../modules/module-2/lab-notebook.md) - [`Module-2-Guided-Lab-Notebook.ipynb`](../materials/module2/Module-2-Guided-Lab-Notebook.ipynb) | A LangChain agent that searches the web (DuckDuckGo) and runs Python, then hardened with error handling and prompt engineering; you keep an *Agent Instruction Log* alongside it | LangChain 1.4.0 (`create_agent`) | Lab ~2 hours, project ~2 hours |
| 3 | [Module 3 lab](../modules/module-3/lab-notebook.md) - [`Module-3-Lab.ipynb`](../materials/module3/Module-3-Lab.ipynb) | A retrieval-augmented generation pipeline: load a PDF corpus, chunk, embed and persist to Chroma, run a retrieval QA chain, add a second corpus and compare; then a four-run retrieval experiment and a RAGAS interpretation | LangChain 1.4.0 (pinned), Chroma, pypdf | Lab ~2 hours, project ~2 hours |
| 4 | [Module 4 lab](../modules/module-4/lab-notebook.md) - [`Module4_Learner_Starter.ipynb`](../materials/module4/Module4_Learner_Starter.ipynb) | The same Researcher -> Analyst -> Critic pipeline implemented twice, in LangGraph and in CrewAI, with structured logs and a framework comparison | LangGraph, CrewAI, LiteLLM | Lab ~2 hours, project ~2 hours |
| 5 | [Module 5 lab](../modules/module-5/lab-notebook.md) - [`Module5_Learner_Starter.ipynb`](../materials/module5/Module5_Learner_Starter.ipynb) | Lab A instruments a two-tool ReAct agent with LangSmith tracing and analyzes ten runs; Lab B runs the same agent under two or three configurations and recommends one from the trace data | LangChain 1.4.0, LangGraph 1.2.11, LangSmith 0.12.4, LiteLLM | Lab ~1 hour, project ~2 hours |

### Model providers each notebook supports

Every lab has at least one free path. The notebook's configuration cell is
where you choose.

| Module | Paid or hosted options | Free options |
| :-- | :-- | :-- |
| 2 | OpenAI (`gpt-4o-mini`), key `OPENAI_API_KEY` | Ollama running locally (`llama3.1`, which supports tool calling) via `langchain-ollama` |
| 3 | OpenAI embeddings (`text-embedding-3-small`) and chat (`gpt-4o-mini`) | Local `sentence-transformers/all-MiniLM-L6-v2` embeddings (first run downloads about 90 MB) with a small local generator (`Qwen/Qwen2.5-0.5B-Instruct`) or Ollama (`llama3.1`); a `"none"` setting runs retrieval only |
| 4 | Hugging Face Inference Providers (default; token `HF_TOKEN`), Groq (`GROQ_API_KEY`), OpenAI (`gpt-4.1-mini`, `OPENAI_API_KEY`) | Ollama locally (`qwen3:8b`), no key; Hugging Face's free credits and quotas can change |
| 5 | NVIDIA API (default; `NVIDIA_API_KEY`), Hugging Face (`HF_TOKEN`), Groq, OpenAI - plus a **LangSmith API key** (free account at [smith.langchain.com](https://smith.langchain.com){target=_blank}) for tracing | Ollama locally (`qwen3:8b`) for the model; LangSmith itself has a free tier |

!!! note "Module 3 needs two PDF corpora"

    The Module 3 notebook works from two NIST publications, AI 100-1 and AI
    600-1 (`CORPUS_1` and `CORPUS_2` in the configuration cell). Its
    configuration step downloads them, from this site first and from NIST if
    that fails, and checks each against the lab's reference copy. If Colab
    cannot reach either source, download the two PDFs yourself and upload them
    to Colab's `/content/` folder with the file browser in the left sidebar.

## How to run a lab

1. **Open the notebook in Colab** with the *Open in Colab* button on the lab
   page. Colab loads the notebook straight from this course's GitHub
   repository.
2. **Save your own copy first**: *File -> Save a copy in Drive*. Until you do
   this your edits live only in the browser tab.
3. **Read the top cells.** Each notebook explains its structure, its
   deliverables and the cells you are expected to edit (`# STUDENT EXTENSION
   POINT` or `TODO` markers). Do not change the scaffolding outside those
   zones; it is designed so that each step teaches one thing.
4. **Run the install cell and wait.** Installs take one to four minutes on
   Colab. If Colab asks you to restart the runtime (*Runtime -> Restart
   session*), do so and run again from the top.
5. **Work top to bottom.** Later cells depend on variables defined earlier.
   Once your `TODO` cells are complete, *Runtime -> Run all* re-executes the
   whole notebook cleanly - which is how it must look when you submit it.
6. **Keep outputs visible.** Submissions with empty output cells are not
   accepted; the graded part of several labs is your reading of the printed
   output, not the code.

## API keys: Colab Secrets and `getpass`

!!! warning "Never paste a key into a notebook cell"

    A key typed into a code cell is saved with the notebook, and your notebook
    ends up in a **public** portfolio repository. Anyone who finds it can
    spend your money or your quota. Use one of the two methods below, and if
    a key ever does leak, revoke it in the provider's dashboard and create a
    new one.

**Colab Secrets** (recommended). Click the key icon in Colab's left sidebar,
add a secret named for the environment variable the notebook expects (for
example `OPENAI_API_KEY`, `HF_TOKEN`, `GROQ_API_KEY`, `NVIDIA_API_KEY` or
`LANGSMITH_API_KEY`), and enable *Notebook access*. Then read it in a cell:

```python
import os
from google.colab import userdata   # available only inside Colab

os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
```

**A hidden prompt with `getpass`.** The Module 4 and 5 notebooks already do
this: their `require_secret()` helper asks for any missing key with a masked
prompt, so nothing is written into the file.

```python
import os
from getpass import getpass

if not os.getenv("HF_TOKEN"):
    os.environ["HF_TOKEN"] = getpass("Enter HF_TOKEN (input is hidden): ")
```

The Module 2 notebook contains a placeholder cell of the form
`os.environ["OPENAI_API_KEY"] = "sk-YOUR-KEY-HERE"`. Replace that line with
the Colab Secrets snippet above rather than typing your key into it; the
notebook's own security note recommends the same.

## What the labs cost

- **Colab**: the free tier is sufficient for all four labs. Free runtimes are
  reclaimed after a period of inactivity, so finish a lab in a sitting or
  re-run from the top.
- **OpenAI, Groq, NVIDIA**: usage is billed or metered to your own account.
  The labs use small models and short runs, but check the provider's current
  pricing and free-tier terms before you start; this site does not quote
  prices because they change.
- **Hugging Face Inference Providers**: the default in Module 4 and an option
  in Module 5, whose default is the NVIDIA API. A free token comes with
  credits and quotas that can change; the notebooks say so.
- **Ollama**: free, but it runs on your own machine. Models are 2-5 GB
  downloads and need a reasonably recent computer; small models are slower
  and less capable than hosted ones, which is fine for the labs.
- **LangSmith**: a free account is enough for the Module 5 traces.

If cost is a concern, the syllabus's free-tier path (Ollama plus Colab) is
supported end to end and earns the same certificate.

## Saving a finished lab to your portfolio

1. In Colab, confirm every cell has run and its output is visible
   (*Runtime -> Run all*).
2. Rename the notebook as the module's *What to submit* box asks:
   `Module2_Lab_[YourName].ipynb`, `Module3_Lab_[YourName].ipynb`,
   `Module4_Lab_[YourName].ipynb` or `Module5_Lab_[YourName].ipynb`, the
   names the notebooks' own submission checklists use.
3. *File -> Download -> Download .ipynb*.
4. Commit the file into the matching module folder of your
   `ai-automation-agents-portfolio` repository, together with any companion
   document the lab asks for (the Module 2 *Agent Instruction Log*, the
   Module 5 *Observability Report*). Update that module's `README.md` and your
   learning log. [GitHub portfolio setup](github-portfolio-setup.md) walks
   through the repository structure and the commit workflow.
5. Check the diff before you push: no API keys, no personal data in outputs.

Instructor solution notebooks exist for Modules 4 and 5 but are not published
on this site; if you are stuck, ask in the discussion forum or bring it to a
cohort session.
