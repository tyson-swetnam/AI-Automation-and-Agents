---
title: 'Module 4 Overview: Multi-Agent Systems'
description: 'Overview of Module 4 (8 hours): designing, implementing, and evaluating multi-agent systems with LangGraph and CrewAI, with learning objectives, checklist, and grade weights.'
type: Overview
tags:
- module-4
- student-facing
- overview
- multi-agent-systems
- langgraph
- crewai
- orchestration
module: 4
time_estimate: 8 hours
status: stable
stale_after: '2027-09-01T00:00:00Z'
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-4:-Overview
  title: 'AI Automation and Agents v2 wiki: Module-4:-Overview'
  author: Carlos Lizárraga-Celaya; Michelle Yung
  last_modified: '2026-08-12T15:32:40-07:00'
authorship:
  created: '2026-05-09'
  updated: '2026-05-09'
  contributors:
  - C. Lizárraga
wiki_page: Module-4:-Overview
---
# Module 4 Overview: Multi-Agent Systems

**Time:** 8 hours

## Introduction

This module focuses on the design, implementation, and evaluation of multi-agent systems (MAS) — architectures where
specialized AI agents collaborate on tasks similarly to how humans work in teams. You will implement multi-agent
systems using LangGraph and CrewAI through guided Jupyter Notebook on Google Colab.

While multi-agent systems offer several advantages over single-agent designs (including parallelization, specialization, and built-in checks and balances), they come with trade-offs. Coordination overhead adds latency, increases token costs, and raises engineering complexity. A well-designed single agent will often outperform a poorly designed multi-agent system.

## Topics Covered

* Multi-agent coordination architectures
* LangGraph implementation of multi-agent systems
* Design of a three-role agent pipeline
* Framework implementation and comparison: CrewAI vs. LangGraph
* Diagnosing failures in multi-agent systems

## Learning Objectives

* **Classify** the four coordination architectures and their failure modes
* **Implement** a LangGraph hierarchical agent system with routing and logging
* **Build** a three-role pipeline with defined input-output interfaces
* **Compare** LangGraph against CrewAI on implementation and observability
* **Diagnose** coordination failures and prescribe structural interventions

## Module 4 Checklist

| Chapter | Type | Primary LOs | Deliverable |
| :--: | :-- | :-- | :-- |
| **1** | Why Multi-Agent Systems Exist | LO 1 | Chapter 1 Quiz |
| **2** | The Four Coordination Architecture Patterns | LO 1 | Chapter 2 Quiz |
| **3** | Orchestration Frameworks: LangGraph, AutoGen, and CrewAI | LO 2, 4 | Chapter 3 Quiz |
| **4** | Coordination Failure Taxonomy | LO 5 | Chapter 4 Quiz |
| **5** | Evidence-Based Benchmarking | LO 4, 5 | Chapter 5 Quiz |
| **Lab** | Guided Lab Exercise | LO 2, 3 | Colab Notebook: Build 3-agent system with LangGraph |
| **Project** | Hands-On Project | LO 3, 4 | CrewAI vs. LangGraph for 3-agent system |
| **Discussion** | Multi-agent system outline for your domain | LO 5 | Discussion Post + Peer Reply |

## Grade Weight Summary

!!! info "Grade weight summary"

    Chapter Quizzes (Units 1–5): 100% of module grade — 20% each

    Discussion Post + Peer Reply: required for certificate — completion only, but please give meaningful responses to your fellow learners

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-4:-Overview){target=_blank} (wiki page last changed 2026-08-12). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-4/overview.md){target=_blank}.</p>
