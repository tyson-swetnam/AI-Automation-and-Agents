---
title: 'Intelligent Agents: Theory and Practice (Reading Summary)'
description: 'Student-oriented summary of Wooldridge and Jennings (1995): the weak and strong notions of agency, the four pillars of agent behavior, intentional systems, and how agents differ from objects and processes.'
type: Reading
tags:
- module-1
- student-facing
- reading
- ai-agents
- agent-loop
- automation-paradigms
- workflow-audit
- wooldridge-jennings
- bdi
module: 1
status: stable
generated:
  by: process:scripts/migrate_wiki.py
  at: '2026-09-08T00:00:00Z'
sources:
- id: wiki-v2
  resource: https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1:-Intelligent-Agents-(book-summary)
  title: 'AI Automation and Agents v2 wiki: Module-1:-Intelligent-Agents-(book-summary)'
  author: Carlos Lizárraga-Celaya
  last_modified: '2026-04-30T06:38:54-07:00'
- id: wooldridge-jennings-1995
  resource: https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/ker95.pdf
  title: 'Intelligent Agents: Theory and Practice (1995)'
  author: Michael Wooldridge; Nicholas R. Jennings
wiki_page: Module-1:-Intelligent-Agents-(book-summary)
---
# Intelligent Agents: Theory and Practice (Reading Summary)

**Book summary:** Wooldridge & Jennings (1995), [Intelligent Agents: Theory and Practice](https://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/ker95.pdf){target=_blank}

## 1. Introduction: The Dawn of the Intelligent Assistant

Welcome to the forefront of modern computing. As you progress in your study of Artificial Intelligence, you will find that we are moving away from a paradigm where humans "use" tools toward one where we "collaborate" with entities. In the field of Distributed Artificial Intelligence (DAI) and concurrent systems research, we describe these entities as agents. To understand the "magic" of agency, we must look at how these systems navigate complexity that would paralyze traditional software.

**The Power of Agency in Action**

Imagine a future where the key air-traffic control systems in the country of Ruritania suddenly fail due to freak weather conditions. Rather than a total system collapse, computerized air-traffic control systems in neighboring countries negotiate among themselves to track and reroute all affected flights, averting disaster. Back on the ground, you log into your computer and find your Personal Digital Assistant (PDA) has already sorted your email by importance. It draws your attention to a specific news article describing work close to your own and—having already communicated with other PDAs—it has retrieved a relevant technical report for you from a remote FTP site. Finally, upon detecting an acceptance email for a conference, your PDA predicts your need for travel and, without prompting, consults various databases to present you with a summary of the most convenient travel options.

The "so what?" of this technology is profound: agents are not just programs you run; they are hardware or software-based systems that act on your behalf. To design such systems, we must first master the fundamental definition of what constitutes "agency."

## 2. Defining the Agent: The "Weak" Notion of Agency

In mainstream computer science, the most common and uncontentious usage of the term is referred to as the **weak notion of agency**. This definition serves as our baseline, establishing the minimum criteria for a system to be considered an agent rather than a standard piece of software or a simple subroutine.

A hardware or (more usually) software-based computer system that enjoys the following properties:

- **Autonomy:** Operating without the direct intervention of humans or others, possessing control over its actions and internal state.
- **Social Ability:** Interacting with other agents (and possibly humans) via an agent-communication language.
- **Reactivity:** Perceiving the environment and responding in a timely fashion to changes.
- **Pro-activeness:** Taking the initiative to exhibit goal-directed behavior.

While "weak" may sound dismissive, this framework provides the four essential pillars that separate intelligent agents from the static code of the past.

## 3. The Four Pillars of Intelligent Behavior

To move beyond traditional software, a system must integrate four core properties. Each provides a distinct "Agent Advantage" that allows a system designer to handle unpredictability in ways traditional code cannot.

| Property | Core Definition | The "Agent Advantage" |
| :-- | :-- | :-- |
| Autonomy | The ability to operate without human intervention and maintain control over internal state. | Independent Operation: Designers can delegate tasks to the system, knowing it will manage its own execution path without constant polling. |
| Social Ability | Interaction via an expressive agent-communication language (e.g., KQML or KIF) to perform negotiation. | Sophisticated Coordination: Unlike simple message passing, agents can negotiate, cooperate, and solve conflicts through high-level communication. |
| Reactivity | The capacity to perceive environmental changes (via sensors or interfaces) and respond in real-time. | Timely Awareness: The system remains robust and relevant by adapting to "freak" events or changing user contexts as they occur. |
| Pro-activeness | The ability to take the initiative rather than simply responding to stimulus. | Goal-Directed Initiative: The agent doesn't just wait for a command; it actively seeks to fulfill its programmed objectives (e.g., booking travel). |

While these four pillars define most contemporary agents, some researchers argue that "true" agency requires a deeper, more human-like abstraction.

## 4. The "Strong" Notion: Agents with Intentionality

In the more theoretical circles of Artificial Intelligence, we often employ a **strong notion of agency**. This approach characterizes agents using **mentalistic notions**—concepts usually reserved for humans. This is known as the **intentional stance**, a term coined by Daniel Dennett and championed by John McCarthy.

McCarthy argues that attributing "beliefs" or "desires" to a machine is not just anthropomorphism; it is a "legitimate" and "useful" abstraction tool, especially when the internal structure of a complex system is **incompletely known**. For example, it is more efficient to say a computer "knows" the printer is busy than to describe the millions of logical gate transitions occurring in the hardware.

We categorize these mental states into two distinct groups:

- **Information Attitudes**
    - **Belief:** The information an agent holds about its world. Unlike *Knowledge*, which implies the information is true, a *Belief* might be false.
    - **Knowledge:** Information that is both believed and factually true.
- **Pro-attitudes** (The states that guide and motivate action)
    - **Desire:** What the agent wants to see happen in the world.
    - **Intention:** A persistent goal to which the agent is committed.
    - **Obligation:** Actions the agent is required to perform based on its role.
    - **Commitment:** The internal pledge to pursue a specific goal.
    - **Choice:** The selection of a specific course of action from available alternatives.

Note that these intentional notions are **referentially opaque**. In standard logic, you can swap equal terms without changing truth, but in agent logic, "believing x" is not the same as "believing y" even if x=y, because the agent may not *know* they are the same.

## 5. Synthesis: Agents vs. Traditional Software Processes

Students often ask: "Is an object in Java an agent? Is a UNIX process an agent?" The answer lies in the level of control and persistence. While agents can be as simple as subroutines, they are typically larger entities with **persistent control**.

Consider the distinction between an Object and an Agent: Objects encapsulate state and provide methods, but they do not have control over whether they execute those methods when called. As the literature famously notes: **"Objects do it for free; agents do it because they want to."** An agent has autonomous control over its state and may refuse a request.

A concrete example is Etzioni’s **"softbot"** (software robot). A softbot interacts with a software environment by issuing shell commands (like `ls` or `ftp`) and interpreting the feedback as sensory data. It is a persistent entity that lives in the environment, rather than a script that runs once and terminates.

### ✅ Checklist for Agency

To determine if your software qualifies as an agent, ask:

1. **Does it exhibit initiative?** Does the system take action to achieve a goal without a direct user command?
2. **Is its control persistent?** Does it monitor its environment over time rather than executing a linear script and exiting?
3. **Does it have autonomous control over its state?** Can it choose how to respond to external requests based on its own goals?
4. **Is it socially capable?** Does it use a high-level communication language to negotiate with other entities?

## 6. Summary and Key Takeaways

The transition to agent-based computing is one of the most significant shifts in modern software development. As you begin designing these systems, keep these three lessons in mind:

1. **Agency is a Spectrum:** We distinguish between the **Weak Notion** (autonomy, social ability, reactivity, pro-activeness) and the **Strong Notion** (attributing mentalistic abstractions like belief and intention).
2. **The Four Pillars are Interconnected:** An intelligent agent must balance **reactivity** (responding to the world) with **pro-activeness** (taking initiative). A system that is only reactive is merely a slave to its environment; a system that is only pro-active is a blind "robot" that cannot adapt.
3. **Agents are Intentional Systems:** Attributing mental states to software is a vital engineering tool for managing complexity. It allows us to predict and explain the behavior of sophisticated, concurrent systems where a purely mechanical description is no longer practicable.

The future of technology belongs to those who can build systems that don't just compute, but *act*. Welcome to the age of the intelligent agent.

<p class="course-provenance" markdown>Migrated from the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1:-Intelligent-Agents-(book-summary)){target=_blank} (wiki page last changed 2026-04-30). Spotted a problem? [Edit this page](https://github.com/tyson-swetnam/AI-Automation-and-Agents/edit/main/docs/modules/module-1/readings/intelligent-agents-wooldridge-jennings.md){target=_blank}.</p>
