---
title: 'Lab Checklist: Local LLM with Ollama (Superseded)'
description: Early checklist lab for installing Ollama, pulling llama3.2, and probing it with factual, reasoning, and uncertainty prompts; superseded by Lab A in the Module 1 activities.
type: Lab
tags:
- module-1
- student-facing
- lab
- ai-agents
- agent-loop
- automation-paradigms
- workflow-audit
- ollama
- superseded
module: 1
status: deprecated
stale_after: '2027-09-01T00:00:00Z'
superseded_by: ../../modules/module-1/activities.md
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1-Unit-3-Lab-B
  title: 'AI Automation and Agents v2 wiki: Module-1-Unit-3-Lab-B'
  author: Michele Cosi
  last_modified: '2026-05-18T16:42:07-07:00'
wiki_page: Module-1-Unit-3-Lab-B
---
# Lab Checklist: Local LLM with Ollama (Superseded)

!!! warning "Superseded"

    This page is kept for history. The current version is [Module 1 Activities](../../modules/module-1/activities.md).

The goal of this Lab is to help and guide the user to understand the process of installing and accessing a local AI model, building baseline intuition for LLM capabilities required for agent frameworks in later Modules (Modules 3 and 4).

This exercise will require the use of the Command Line Interface of the learner's computer.

Report exercise outcomes in a Lab Log document to be submitted.

## Setup
- [ ] Download and install [Ollama](https://ollama.com/){target=_blank}
- [ ] Start the Ollama service, pulling the llama3.2 model
    - Learners can rely on the official [Quickstart documentation](https://docs.ollama.com/quickstart){target=_blank} and the [llama3 instructions](https://ollama.com/library/llama3){target=_blank}

## Exercise
- For each of the following, complete a Model Behavior Observation form for each: **what was submitted**, **what was returned**, **whether the response was accurate**, and **what an agent with tool access would do differently**. 

- Ask Ollama 
    - [ ] a direct factual question
    - [ ] a multi-step reasoning question
    - [ ] a question where the model should acknowledge uncertainty

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1-Unit-3-Lab-B){target=_blank} (wiki page last changed 2026-05-18). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/archive/module-1/lab-checklist-ollama.md){target=_blank}.</p>
