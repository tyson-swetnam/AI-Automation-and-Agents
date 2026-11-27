---
title: "Guest Lecture: Agentic AI for Engineering Research"
description: "A 90-minute guest lecture and hands-on for UNM's Introduction to Reliability Engineering: what AI agents are and how to build and apply them across a research project on free tools, AI watermarks and unreliable AI-text detectors, and an agent that drafts a Mars hazard assessment."
type: Lesson
tags: [course, student-facing, guest-lecture, agentic-ai, research-workflows, reliability-engineering, mars, watermarking, ai-detection, research-integrity, open-weight-models, ollama, carc]
time_estimate: "90 minutes"
status: stable
stale_after: "2027-05-30T00:00:00Z"
generated:
  by: "claude/opus-5-5"
  at: "2026-11-27T00:00:00Z"
sources:
  - id: lecture-html
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/guest-lectures/agentic-ai-for-engineering-research.html"
    title: "Agentic AI for Engineering Research: Agents, Watermarks and Research Integrity (interactive HTML slides)"
    author: "Tyson L. Swetnam"
  - id: agentic-ai-loops
    resource: "https://tyson-swetnam.github.io/AI-Automation-and-Agents/guest-lectures/agentic-ai-loops/"
    title: "Guest Lecture: Agentic AI Loops (this site)"
    author: "Tyson L. Swetnam"
  - id: say-what-you-mean
    resource: "https://tyson-swetnam.github.io/AI-Automation-and-Agents/guest-lectures/say-what-you-mean/"
    title: "Guest Lecture: Say What You Mean (this site; shares the slide viewer and branding)"
    author: "Tyson L. Swetnam"
  - id: mesa
    resource: "https://idss-mesa.github.io/"
    title: "MESA: Multidisciplinary Environment for Scientific Advancement"
    author: "team:idss-mesa"
  - id: ai-verde
    resource: "https://cyverse.org/ai-verde"
    title: "CyVerse AI VERDE"
    author: "team:cyverse"
  - id: ollama-docs
    resource: "https://docs.ollama.com/api/chat"
    title: "Ollama API documentation: chat endpoint"
    author: "team:ollama"
  - id: nasa-mars-fact-sheet
    resource: "https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html"
    title: "NASA Mars Fact Sheet (source pack values)"
    author: "NASA NSSDCA"
---

# Guest Lecture: Agentic AI for Engineering Research

*Estimated time: ~50 min talk and ~40 min hands-on as planned, ~60 min on your own with the backup slides*

**From one chat to a research workflow you can check, and how to use it
honestly.** This is the guest lecture Tyson Swetnam will give on Monday,
November 30, 2026, to UNM's *Introduction to Reliability Engineering*, taught
by Anthony and David Menicucci (Centennial Engineering 1026). It follows David
Menicucci's lecture on AI fundamentals. The students are applying Design for
Reliability (DfR) to a Martian habitat built on ACEGS, the Autonomous
Controlled-Environment Growing-Spaces framework David Menicucci developed,
which applies passive-solar theory and climate classification to
self-sustaining living and agricultural spaces. Their project starts with a
Martian environmental hazard assessment, and each team then writes a 300-word
abstract; the best goes to the Mars Society convention.

The instructors asked for two things: what agents are, how they work and how
to create and apply them across a research project; and AI watermarking and
AI-text detection, including false accusations, as they bear on research
publications and the students' abstracts. The lecture picks up David
Menicucci's thesis, that a model is limited to the information it is given,
and answers it: an agent is how you give a model context, tools, data and a
loop. It does not re-teach how language models work. The talk is 29 slides in
four parts and a close, followed by a six-slide hands-on in which teams build
a small agent workflow on a free model that drafts their hazard assessment
and checks its own sources. Four backup slides and six slides of references
(77 sources) close the deck.

[Open the lecture full screen](../materials/guest-lectures/agentic-ai-for-engineering-research.html){ .md-button .md-button--primary target=_blank }
[Download the slides (PDF)](../assets/files/Agentic-AI-for-Engineering-Research-Guest-Lecture.pdf){ .md-button target=_blank }

<iframe class="course-embed course-embed--slides" src="../materials/guest-lectures/agentic-ai-for-engineering-research.html" title="Agentic AI for Engineering Research lecture slides" loading="lazy" allow="fullscreen" allowfullscreen></iframe>

!!! tip "Driving the slides"

    Click inside the slides first, then use ++arrow-right++ and ++arrow-left++
    (or ++space++) to move, ++home++ and ++end++ to jump to either end, ++n++
    for the speaker notes and ++f++ for full screen. On a touch screen, swipe.
    The menu in the toolbar jumps to any slide, every bracketed citation is a
    link to its source, and each slide has its own address (for example
    `agentic-ai-for-engineering-research.html#steps`), so you can link to one.
    The file is self-contained: fonts and images are embedded and it makes no
    network requests, so it also works offline.

## From chat to agent

A chat is a model and your prompt. Add instructions that persist, tools it can
call (search, a code interpreter, your files, a database) and memory (documents
it can retrieve, the record of earlier steps), and Anthropic's engineering
guide calls the result an *augmented LLM*. Put that in a loop, in which the
model acts, looks at the result and decides what to do next, and you have an
agent. The loop is the old structured-programming trio of sequence, selection
and iteration, read the way the [Agentic AI Loops](agentic-ai-loops.md)
lecture reads it; what has changed is that the model, not the programmer,
decides the branches and when to stop.

| | Workflow | Agent |
| :-- | :-- | :-- |
| **Who picks the path** | You, in code or a fixed chain of prompts | The model, step by step |
| **Anthropic's definition** | "LLMs and tools are orchestrated through predefined code paths" | "LLMs dynamically direct their own processes and tool usage" |
| **Strength** | Predictable and testable | Flexible |
| **Reliability cost** | Low: you can test each step | Every decision handed to the model is a new failure mode |

The hands-on in this lecture is deliberately a workflow, with the student as
the loop.

## Anatomy of an agent

Each part is taught in depth elsewhere in this course, so the lecture links
rather than repeats.

| Part | The question it answers | Where to learn it |
| :-- | :-- | :-- |
| **Instructions** | Role, rules, output format, and what to do when it does not know | [Module 2: Foundational Concepts](../modules/module-2/foundational-concepts.md) |
| **Tools** | What it can do: search, run code, read files, query data; the Model Context Protocol connects them | [Module 2: Foundational Concepts](../modules/module-2/foundational-concepts.md) |
| **Context and memory** | What it knows: documents retrieved into the prompt, notes from earlier steps | [Module 3: Foundational Concepts](../modules/module-3/foundational-concepts.md) |
| **The loop** | Who decides what happens next: one agent, or several handing work along | [Module 4: Foundational Concepts](../modules/module-4/foundational-concepts.md) |
| **Verification** | How you know it worked: checks outside the model | [Module 5: Foundational Concepts](../modules/module-5/foundational-concepts.md) |

Start with [What Is an AI Agent?](../modules/module-1/readings/what-is-an-agent.md)
for the engineering and the theoretical definitions side by side.

Two findings shape the design advice. Retrieval-augmented models, given
documents at the time they answer, wrote more specific and more factual text
than models working from what they absorbed in training (Lewis et al., 2020),
which is David Menicucci's point turned into engineering. And a model checking
itself is not a check: self-feedback helps on some tasks (Self-Refine reports
about 20 points, absolute, on average across seven tasks), but for reasoning, models "struggle to self-correct
their responses without external feedback" (Huang et al., ICLR 2024). So the
checker needs something external: a source pack, a unit test, a hand
calculation, a person.

## Agents across the research lifecycle

| Stage | An agent can | You must check |
| :-- | :-- | :-- |
| **Literature** | Search, summarize, pull values into a table | Every citation exists and says what is claimed |
| **Data** | Find datasets, convert units, clean tables | Units, provenance, what was dropped |
| **Code** | Write and run analysis scripts and tests | Read the diff; run the tests yourself |
| **Analysis** | Build FMEA tables, fit distributions, plot | A hand calculation on one row |
| **Writing** | Outline, tighten to 300 words, fix grammar | Your claims, your voice, your disclosure |
| **Review** | Critique a draft against a rubric | It cannot verify its own facts |

What the evidence says, from three studies that are preprints or blog
reports: PaperQA2, a literature agent, answered with higher precision than
PhD-level experts on its question set (85.2% vs 73.8%) and about the same
accuracy, yet 13.5% of the cited statements in its generated articles were
unsupported by their citation. The AI Scientist reports full papers for
under $15 each; an independent evaluation found 42% of its experiments failed
on coding errors and some papers contained hallucinated numerical results.
METR's 2025 randomized trial found experienced developers took 19% longer with
early-2025 AI tools while believing they were 20% faster; METR now calls those
results out of date. The output looks equally confident either way, so you
measure.

The lecture's worked example hands a coding agent, Claude Code, the boring,
checkable part of a reliability task: turn a hazard table into an FMEA table
and write a test that fails if any row lacks a source. Claude Code comes with
Claude's paid plans, not the free plan; the hands-on ends with the same loop in
a short script against a free, local model.

### Free and open options

As each provider describes its own offering on November 27, 2026. These
change often; check the date.

| Option | What you get | Note |
| :-- | :-- | :-- |
| **Claude Free** | Web search, file creation, running code, up to five Projects | Claude Code needs a paid plan |
| **ChatGPT Free** | Search and Projects; limited uploads and data analysis | Custom GPTs are listed for paid plans |
| **Gemini Free** | Deep Research, Canvas, Gemini Notebook | With a Google account |
| **Ollama** | Open-weight models (for example `llama3.2:3b`, 2.0 GB; `gpt-oss:20b`, 14 GB) on hardware you control | On a laptop ([Module 1, Lab A](../modules/module-1/activities.md)) or in an Ollama app in the CyVerse Discovery Environment |
| **CyVerse** | The Basic tier is free: the Discovery Environment and 200 CPU core-hours a year | Register at [user.cyverse.org](https://user.cyverse.org){target=_blank} with your `.edu` address, then request VICE (interactive app) access in the User Portal; it is not granted to Gmail-type addresses |
| **AI VERDE** | Commercial and open-weight models inside university infrastructure, at [chat.cyverse.ai](https://chat.cyverse.ai){target=_blank} | Its page says it currently requires a University of Arizona NetID; students who want access can follow up with the speaker |
| **MESA** | An open-source, agentic AI platform for research data; portal at [mesa.cyverse.org](https://mesa.cyverse.org){target=_blank} | Signs in with CyVerse; docs at [idss-mesa.github.io](https://idss-mesa.github.io/){target=_blank} |

## Watermarks, detectors and research integrity

### How a text watermark works

The best-known scheme (Kirchenbauer et al., ICML 2023) splits the vocabulary,
at each step, into a "green list" and a "red list" of equal size, seeded by
the previous token, and nudges the model toward green words. A detector that
holds the key counts green tokens and runs a one-proportion z-test: human text
lands near half green by chance, and at z > 4 the false-positive probability is
3 × 10⁻⁵. Removing the watermark from a long text means rewriting roughly a
quarter of its tokens or more.

Google DeepMind's SynthID-Text (Nature, 2024) watermarks Gemini's text; in a
live test on nearly 20 million Gemini responses, user ratings did not differ.
It is open-sourced in Hugging Face Transformers, and SynthID also marks
images, audio and video. Its limits are stated by its authors: watermarks are
weakened by edits such as paraphrasing with another model, thorough rewriting
or translation greatly reduces detection, and enforcing watermarks on open-weight models is
difficult. OpenAI says it has built a text watermarking method that it
"continue[s] to consider", less robust to translation or rewording with
another model, and that it "could stigmatize use of AI" by non-native English
speakers. **A watermark can show that a text came from one vendor's model; its
absence proves nothing.**

### Why AI-text detectors misfire

Post-hoc detectors guess from style, without a key.

- Seven detectors labeled on average **61.3%** of TOEFL essays by non-native
  English writers as AI-generated, and 97.8% were flagged by at least one,
  while essays by US eighth-graders were judged accurately (Liang et al.,
  *Patterns*, 2023).
- OpenAI's own classifier caught 26% of AI-written text and flagged 9% of
  human text; OpenAI withdrew it on July 20, 2023, "due to its low rate of
  accuracy".
- A test of fourteen tools, including Turnitin, found them "neither accurate
  nor reliable" (Weber-Wulff et al., 2023), and paraphrasing defeats detectors
  and watermarks alike (Sadasivan et al., 2023).

### Who screens anyway, and false accusations

| Who | What they say they do |
| :-- | :-- |
| **Springer Nature** | Geppetto "detects AI-generated content", as a sign of paper-mill activity; a high score triggers a human check |
| **Wiley** | Piloting a paper-mill detection service, developed with Sage and IEEE, that includes "Gen-AI generated content detection" |
| **Elsevier** | Tools that "help us detect large language model usage" and hallucinated references; in-house experts review flags |
| **NIH** | Applications "substantially developed by AI" are not considered original; NIH uses AI-detection technology (NOT-OD-25-132) |
| **NeurIPS 2026** | Desk-rejected 178 position-track submissions (18.4%) on detector scores, acknowledging there would be borderline cases |

The documented false accusations are of students, not researchers. Vanderbilt
estimated that a 1% false-positive rate on its 75,000 papers a year would
mislabel about 750, and disabled Turnitin's AI detector. Australian Catholic
University registered nearly 6,000 misconduct cases in 2024, about 90% of them
AI-related (a figure ACU calls overstated); students were wrongly accused and
ACU dropped the tool. Turnitin's own guidance is that its score "should not
be used as the sole basis for adverse actions against a student", and its
blog puts its sentence-level false-positive rate at about 4%. The lecture's
research found no documented case of a researcher falsely flagged by a journal
or publisher. The base rates say it will happen, so be ready to show your
work.

### What journals ask

| Policy | AI as an author? | Disclose where | Also |
| :-- | :-- | :-- | :-- |
| **ICMJE** | No | Writing help in the acknowledgments; analysis or figures in the methods | Humans are responsible for everything submitted |
| **Springer Nature** | No | Disclose AI use | No fabricated data, citations or results |
| **Elsevier** (June 2026) | No | A declaration section, with template wording | Primary research images may not be created or altered with AI |
| **IEEE** | Not stated | Acknowledgments, naming the AI system | Disclosure recommended even for grammar editing |
| **AIAA** | No, nor cited as a source | Acknowledgments, and at submission | Failing to disclose is a violation |

**For the Mars Society abstract.** The 2026 convention's submission form
rejected abstracts over 300 words and its call asked for 150 to 300; no 2027
call has been posted, and the lecture found no AI policy on the Mars Society's
pages. When a venue is silent, follow the strictest policy you might face,
which for aerospace is AIAA's. Three habits:

1. **Disclose** in one sentence: which tool, for what, and that you checked
   the result.
2. **Keep your history.** Write in a tool with version history and keep your
   prompts and drafts; if a detector ever flags you, that is your evidence.
3. **Verify every citation.** Walters and Wilder (2023) found 55% of GPT-3.5's
   citations and 18% of GPT-4's were fabricated; in *Mata v. Avianca* (2023),
   lawyers who filed fake cases from ChatGPT were fined $5,000.

### Checklist for the DfR project and abstract

- **Before:** pick the tool and check what it does with your data; write
  instructions with a role, rules and "say when you don't know"; gather a
  source pack you have read yourself.
- **During:** ground every number in a source; check against something
  outside the model; keep prompts, drafts and version history.
- **Before you submit:** open every citation and confirm it says what you
  claim; hand-check one calculation per table; stay within 300 words, in your
  own voice.
- **Always:** disclose what AI did; no AI author and no AI-made research
  images; you are responsible for every word.

## Hands-on: a hazard-assessment agent for ACEGS

About forty minutes, in teams, on any free chat model (Claude, ChatGPT,
Gemini) or a local model in Ollama. On a free chat model **you are the loop**:
you paste each step and decide what happens next, which is sequence,
selection and iteration done by hand. The stretch goal hands the loop to a
program.

!!! note "Before class"

    Nothing needs installing. Each team needs one laptop signed in to any free
    chat model. A CyVerse account (free, registered with a UNM address) is
    needed only for the optional code version in the Discovery Environment;
    students who want it should register at user.cyverse.org with a UNM
    address and request VICE access in the User Portal before class.

??? question "Step 1: Instructions (paste first)"

    ```text
    You are a reliability engineer helping a student team apply Design for
    Reliability (DfR) to a Martian habitat built on ACEGS (Autonomous
    Controlled-Environment Growing-Spaces), a framework for self-sustaining
    living and agricultural spaces that uses passive-solar design.

    Rules:
    1. Use only facts from the SOURCE PACK I paste next. Cite its bracketed
       source after every number.
    2. If something is not in the source pack, write "not in source pack".
       Never estimate or invent a value or a reference.
    3. Use SI units. Mark derived numbers "(derived)" and show the arithmetic.
    4. Ask me before assuming anything about our habitat design.

    Reply "Ready" and wait for the source pack.
    ```

??? question "Step 2: The source pack (paste second)"

    Every value was checked on 2026-11-27 against the source it cites. Derived values are arithmetic on the sourced numbers.

    ```text
    MARS HABITAT HAZARD SOURCE PACK. Use ONLY these facts and cite the bracketed source for each number. If a value is missing, write "not in source pack"; never estimate. (derived) = calculated from sourced numbers.

    1. Pressure: 6.36 mb (636 Pa, derived), seasonal 4.0-8.7 mb (400-870 Pa, derived); CO2 95.1%, N2 2.59%, Ar 1.94% [NASA Mars Fact Sheet 2025, https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html]
    2. Temperature: average ~214 K; diurnal 184-242 K (Viking 1 site) [Fact Sheet]. Gale crater air: highs ~0 °C, lows ~-70 °C [NASA PIA16913 2013, https://science.nasa.gov/photojournal/steady-temperatures-at-mars-gale-crater]
    3. Radiation: absorbed dose rate ~0.21 mGy/day (210 µGy/day) at Gale crater; only one solar particle event was observed by RAD on the surface, and it was weak [NASA 2013, https://science.nasa.gov/resource/radiation-measurements-on-mars]. Galactic cosmic ray dose equivalent 0.67 mSv/day on the surface; 1.8 mSv/day in cruise; a 500-day surface stay ~1 Sv [SwRI 2013 press releases reporting Hassler et al. Science 2014, https://doi.org/10.1126/science.1244797, and Zeitlin et al. Science 2013, https://doi.org/10.1126/science.1235989]
    4. Dust storms: 2018 global storm, optical depth (tau) 10.8, 35 million km²; Opportunity silent from June 10 2018, mission ended Feb 2019 [JPL 2018, https://www.jpl.nasa.gov/news/opportunity-hunkers-down-during-dust-storm/; NASA 2019, https://science.nasa.gov/missions/mer/nasas-opportunity-rover-mission-on-mars-comes-to-end]
    5. Array dust: InSight fell from ~5,000 Wh/sol (18 MJ, derived) to ~500 Wh/sol (1.8 MJ, derived) by spring 2022 [NASA 2022, https://www.nasa.gov/missions/insight/nasas-insight-still-hunting-marsquakes-as-power-levels-diminish]
    6. Dust size: cross-section weighted mean radius 1.47 ± 0.21 µm and 1.52 ± 0.18 µm [Lemmon et al. Science 2004, https://doi.org/10.1126/science.1104474]
    7. Soil: 0.4-0.6% perchlorate by mass, pH 7.7 ± 0.5 [Hecht et al. Science 2009, https://doi.org/10.1126/science.1172466]; perchlorate a "critical chemical hazard to astronauts" [Davila et al. Int J Astrobiol 2013, https://doi.org/10.1017/S1473550413000189]
    8. Gravity 3.73 m/s²; day 24.6597 h, ~355 day-night cycles per Earth year (derived) [Fact Sheet]
    9. Solar irradiance: 586.2 W/m² at mean distance, top of atmosphere, not surface [Fact Sheet]
    10. Wind: 2-7 m/s summer, 5-10 m/s fall, 17-30 m/s dust storm (Viking); density 0.016 ± 0.006 kg/m³, so dynamic pressure ~0.03-7.2 Pa (derived) [Fact Sheet]
    11. Human hazards: radiation; isolation/confinement; distance; gravity (3/8 Earth); hostile/closed environments [NASA HRP, https://www.nasa.gov/hrp/hazards]
    ```

??? question "Step 3: Draft the hazard table"

    ```text
    Draft a hazard assessment for our ACEGS habitat as a Markdown table with
    columns: Hazard | Environmental value (SI) [source] | Habitat subsystem
    affected (structure, pressure shell, thermal, power, life support,
    growing space, crew) | Likely failure mode | DfR mitigation idea.
    Cover every hazard in the source pack. Then name the three hazards you
    would rank highest for reliability, and say why.
    ```

??? question "Step 4: Check and revise (open a new chat)"

    Paste the source pack, then the table, then:

    ```text
    Act as a strict reviewer. Check every number and claim in the table
    against the SOURCE PACK. For each row say SUPPORTED, MISQUOTED (give the
    correct value) or NOT IN PACK. List any reference that is not in the
    pack. End with exactly one line: VERDICT: PASS or VERDICT: REVISE.
    ```

    Take the review back to the first chat and ask it to fix every problem
    the review lists. Repeat until the verdict is PASS. Then **open two of the
    source links yourself** and confirm the values by hand: that is the check
    no model can do for you.

??? example "Stretch goal: the same loop in code"

    Forty-odd lines of standard-library Python that run draft, check and
    revise against Ollama's chat endpoint (`POST /api/chat`). Save the source
    pack as `source_pack.txt` next to the script. It runs on a laptop with
    Ollama ([Module 1, Lab A](../modules/module-1/activities.md)) or in an
    Ollama app in the CyVerse Discovery Environment. Set `MODEL` to a model
    you have pulled, for example `MODEL=llama3.2:3b python hazard_agent.py`.
    The loop logic was tested against a mock of Ollama's `/api/chat` (a
    checker that answers REVISE, then PASS, and one that echoes both
    options); it has not yet been run against a live model.

    ```python
    """A small agent loop: draft a Mars hazard table, check it against the source pack, revise.

    Sequence (draft, then check), selection (PASS or REVISE?), iteration (up to MAX_ROUNDS).
    Talks to Ollama's REST API; standard library only. Put the source pack in source_pack.txt.
    """
    import json
    import os
    import urllib.request

    URL = os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/api/chat"
    MODEL = os.environ.get("MODEL", "llama3.2:3b")
    MAX_ROUNDS = 3

    DRAFTER = """You are a reliability engineer drafting a Martian environmental hazard
    assessment for an ACEGS habitat. Use ONLY facts from the SOURCE PACK and cite the
    source after every number. Return a Markdown table with columns: Hazard |
    Environmental value (SI units) [source] | Habitat subsystem affected |
    Failure mode | Design-for-reliability mitigation. Write UNVERIFIED next to any
    claim the source pack does not support."""

    CHECKER = """You are a strict reviewer. Compare every number and claim in the DRAFT
    with the SOURCE PACK. List each claim that is missing from the pack, misquoted,
    or has the wrong units. End with exactly one line: VERDICT: PASS (nothing to fix)
    or VERDICT: REVISE."""


    def chat(system, user):
        body = json.dumps({"model": MODEL, "stream": False, "options": {"temperature": 0.2},
                           "messages": [{"role": "system", "content": system},
                                        {"role": "user", "content": user}]}).encode()
        req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=900) as r:
            return json.load(r)["message"]["content"]


    pack = open("source_pack.txt", encoding="utf-8").read()
    draft = chat(DRAFTER, f"SOURCE PACK:\n{pack}\n\nDraft the hazard table.")
    for n in range(1, MAX_ROUNDS + 1):
        report = chat(CHECKER, f"SOURCE PACK:\n{pack}\n\nDRAFT:\n{draft}")
        print(f"--- check {n} ---\n{report}\n")
        last = report.strip().splitlines()[-1] if report.strip() else ""
        if "PASS" in last and "REVISE" not in last:
            break
        draft = chat(DRAFTER, f"SOURCE PACK:\n{pack}\n\nYOUR DRAFT:\n{draft}\n\n"
                              f"REVIEW:\n{report}\n\nFix every problem the review lists.")
    else:
        print(f"Stopped after {MAX_ROUNDS} rounds without a PASS: check the last draft by hand.")
    open("hazard_table.md", "w", encoding="utf-8").write(draft)
    print(f"--- final draft (also saved to hazard_table.md) ---\n{draft}")
    ```

    The `else` branch matters most: a well-designed agent knows when to stop
    and hand the work back to a person.

??? question "Debrief (10 minutes)"

    1. **What did it invent?** Any value, unit or reference not in the source
       pack.
    2. **What did the reviewer miss**, and what did you catch when you opened
       the sources yourself?
    3. **Write the disclosure.** One sentence for your abstract: which tool,
       for what, and how you checked it. For example: *"We used a free AI
       chat model to draft an initial hazard table from a curated list of NASA
       and peer-reviewed sources; the authors checked every value against the
       original sources and take responsibility for the content."*

## Lecture outline

Each link opens the slides at that point.

| Part | Slides | What it covers |
| :-- | :-- | :-- |
| [Opening](../materials/guest-lectures/agentic-ai-for-engineering-research.html#cover) | 1-3 | The two asks and the build; the bridge from David Menicucci's lecture |
| [Part 1: From chat to agent](../materials/guest-lectures/agentic-ai-for-engineering-research.html#p1) | 4-8 | The augmented model and the loop; sequence, selection and iteration; from one paper agent to a research workflow; workflow or agent |
| [Part 2: Anatomy](../materials/guest-lectures/agentic-ai-for-engineering-research.html#p2) | 9-14 | Five parts you design; MCP; grounding; verification; the autonomy dial |
| [Part 3: Research](../materials/guest-lectures/agentic-ai-for-engineering-research.html#p3) | 15-20 | The research lifecycle; research agents measured; a coding-agent example; open-weight models; free and open options |
| [Part 4: Integrity](../materials/guest-lectures/agentic-ai-for-engineering-research.html#p4) | 21-28 | How text watermarks work; SynthID and its limits; detectors; who screens; false accusations; journal policies; the Mars Society abstract |
| [Close](../materials/guest-lectures/agentic-ai-for-engineering-research.html#checklist) | 29 | The checklist |
| [Hands-on](../materials/guest-lectures/agentic-ai-for-engineering-research.html#handson) | 30-35 | Why a source pack; four steps; the loop in code; debrief; questions |
| [Backup](../materials/guest-lectures/agentic-ai-for-engineering-research.html#appendix) | 36-39 | The source pack as a table; C2PA and the EU AI Act's marking rule; reading for reliability engineers |
| [References](../materials/guest-lectures/agentic-ai-for-engineering-research.html#refs-1) | 40-45 | 77 sources, numbered in order of first citation |

**If time runs short:** the hands-on is the part that shrinks. Steps 1 to 3
take about fifteen minutes; teams can finish step 4 and the debrief on their
own from this page.

## Reusing the lecture

The slides, this page and the PDF are licensed
[CC BY 4.0](../about/license-and-attribution.md) like the rest of the course.
The HTML file is a single self-contained document, so you can download it and
present from it without a network connection. It uses the slide viewer and
UNM branding of [Say What You Mean](say-what-you-mean.md), and reuses the
sequence, selection and iteration framing of
[Agentic AI Loops](agentic-ai-loops.md). The Mars image (PIA22330) is
NASA/JPL-Caltech/MSSS, used under NASA's media guidelines with credit. MESA is
supported by the U.S. National Science Foundation under Award 2632685.

## References

Numbered in order of first citation on the slides, in PLOS style. The last six
slides carry the same list with the slide numbers that cite each entry.

1. Schluntz E, Zhang B. Building effective agents. Anthropic Engineering. 2024 Dec 19. Available from: [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents){target=_blank}
2. Yao S, Zhao J, Yu D, Du N, Shafran I, Narasimhan K, et al. ReAct: synergizing reasoning and acting in language models. In: International Conference on Learning Representations (ICLR 2023). 2023. arXiv:2210.03629. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629){target=_blank}
3. Böhm C, Jacopini G. Flow diagrams, Turing machines and languages with only two formation rules. Commun ACM. 1966;9(5):366–371. [doi:10.1145/355592.365646](https://doi.org/10.1145/355592.365646){target=_blank}
4. Swetnam TL. Guest lecture: Agentic AI loops: sequence, selection, iteration \[slides\]. AI Automation and Agents, University of New Mexico. 2026 Sep 22. CC BY 4.0. Available from: [tyson-swetnam.github.io](https://tyson-swetnam.github.io/AI-Automation-and-Agents/guest-lectures/agentic-ai-loops/){target=_blank}
5. Model Context Protocol. What is the Model Context Protocol (MCP)? Documentation. Accessed 2026 Nov 27. Available from: [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/getting-started/intro){target=_blank}
6. Anthropic. Donating the Model Context Protocol and establishing the Agentic AI Foundation. 2025 Dec 9. Available from: [anthropic.com](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation){target=_blank}
7. MESA documentation: the MESA MCP stack (mesa-mcp, mesa-ducklake, irods-mcp-server) and the MESA Portal. idss-mesa/docs. Accessed 2026 Nov 27. Available from: [idss-mesa.github.io](https://idss-mesa.github.io/docs/){target=_blank}
8. Lewis P, Perez E, Piktus A, Petroni F, Karpukhin V, Goyal N, et al. Retrieval-augmented generation for knowledge-intensive NLP tasks. In: Advances in Neural Information Processing Systems 33 (NeurIPS 2020). 2020. arXiv:2005.11401. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401){target=_blank}
9. Madaan A, Tandon N, Gupta P, Hallinan S, Gao L, Wiegreffe S, et al. Self-Refine: iterative refinement with self-feedback. arXiv:2303.17651 \[Preprint\]. 2023. [arXiv:2303.17651](https://arxiv.org/abs/2303.17651){target=_blank}
10. Huang J, Chen X, Mishra S, Zheng HS, Yu AW, Song X, et al. Large language models cannot self-correct reasoning yet. In: International Conference on Learning Representations (ICLR 2024). 2024. arXiv:2310.01798. [arXiv:2310.01798](https://arxiv.org/abs/2310.01798){target=_blank}
11. Anthropic. Claude Code overview. Claude Code documentation. Accessed 2026 Nov 27. Available from: [code.claude.com](https://code.claude.com/docs/en/overview){target=_blank}
12. Skarlinski MD, Cox S, Laurent JM, Braza JD, Hinks M, Hammerling MJ, et al. Language agents achieve superhuman synthesis of scientific knowledge. arXiv:2409.13740 \[Preprint\]. 2024. [arXiv:2409.13740](https://arxiv.org/abs/2409.13740){target=_blank}
13. Lu C, Lu C, Lange RT, Foerster J, Clune J, Ha D. The AI Scientist: towards fully automated open-ended scientific discovery. arXiv:2408.06292 \[Preprint\]. 2024. [arXiv:2408.06292](https://arxiv.org/abs/2408.06292){target=_blank}
14. Beel J, Kan M-Y, Baumgart M. Evaluating Sakana’s AI Scientist: bold claims, mixed results, and a promising future? SIGIR Forum. 2025. arXiv:2502.14297. [arXiv:2502.14297](https://arxiv.org/abs/2502.14297){target=_blank}
15. Becker J, Rush N, Barnes B, Rein D. Measuring the impact of early-2025 AI on experienced open-source developer productivity. METR. 2025 Jul 10. Available from: [metr.org](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/){target=_blank}
16. METR. We are changing our developer productivity experiment design. 2026 Feb 24. Available from: [metr.org](https://metr.org/blog/2026-02-24-uplift-update/){target=_blank}
17. Anthropic. Plans and pricing \[Claude\]. Accessed 2026 Nov 27. Available from: [claude.com](https://claude.com/pricing){target=_blank}
18. OpenAI. Introducing gpt-oss. 2025 Aug 5. Available from: [openai.com](https://openai.com/index/introducing-gpt-oss/){target=_blank}
19. Ollama. API introduction and chat endpoint. Ollama documentation. Accessed 2026 Nov 27. Available from: [docs.ollama.com](https://docs.ollama.com/api/chat){target=_blank}
20. Ollama. Model library: llama3.2, gemma3, qwen3 and gpt-oss \[model pages with download sizes\]. Accessed 2026 Nov 27. Available from: [ollama.com](https://ollama.com/library){target=_blank}
21. OpenAI. ChatGPT pricing. Accessed 2026 Nov 27. Available from: [chatgpt.com](https://chatgpt.com/pricing){target=_blank}
22. Google. Gemini subscriptions. Accessed 2026 Nov 27. Available from: [gemini.google](https://gemini.google/subscriptions/){target=_blank}
23. CyVerse. Set up an account; subscription tiers (Basic, free). CyVerse Learning Center. Accessed 2026 Nov 27. Available from: [learning.cyverse.org](https://learning.cyverse.org/home/account/){target=_blank}
24. CyVerse. About VICE (Visual Interactive Computing Environment). CyVerse Learning Center. Accessed 2026 Nov 27. Available from: [learning.cyverse.org](https://learning.cyverse.org/de/vice/about/){target=_blank}
25. CyVerse. AI VERDE. Accessed 2026 Nov 27. Available from: [cyverse.org](https://cyverse.org/ai-verde){target=_blank}
26. Mithun P, Noriega-Atala E, Merchant N, Skidmore E. AI-VERDE: a gateway for egalitarian access to large language model-based resources for educational institutions. arXiv:2502.09651 \[Preprint\]. 2025. [arXiv:2502.09651](https://arxiv.org/abs/2502.09651){target=_blank}
27. MESA: Multidisciplinary Environment for Scientific Advancement. An open-source, agentic AI platform. University of New Mexico, University of Arizona, UNC-Chapel Hill/RENCI. Accessed 2026 Nov 27. Available from: [idss-mesa.github.io](https://idss-mesa.github.io/){target=_blank}
28. Kirchenbauer J, Geiping J, Wen Y, Katz J, Miers I, Goldstein T. A watermark for large language models. In: Proceedings of the 40th International Conference on Machine Learning (ICML). PMLR 202; 2023. p. 17061–17084. Available from: [proceedings.mlr.press](https://proceedings.mlr.press/v202/kirchenbauer23a.html){target=_blank}
29. Dathathri S, See A, Ghaisas S, Huang P-S, McAdam R, Welbl J, et al. Scalable watermarking for identifying large language model outputs. Nature. 2024;634(8035):818–823. [doi:10.1038/s41586-024-08025-4](https://doi.org/10.1038/s41586-024-08025-4){target=_blank}
30. Ghaisas S, Dathathri S, Mullins R, Gante J, Sun M, Turganbay R. Introducing SynthID Text. Hugging Face Blog. 2024 Oct 23. Available from: [huggingface.co](https://huggingface.co/blog/synthid-text){target=_blank}
31. Google DeepMind. SynthID. Accessed 2026 Nov 27. Available from: [deepmind.google](https://deepmind.google/models/synthid/){target=_blank}
32. OpenAI. Understanding the source of what we see and hear online. 2024 May 7; updated 2024 Aug 4. Available from: [openai.com](https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/){target=_blank}
33. Liang W, Yuksekgonul M, Mao Y, Wu E, Zou J. GPT detectors are biased against non-native English writers. Patterns. 2023;4(7):100779. [doi:10.1016/j.patter.2023.100779](https://doi.org/10.1016/j.patter.2023.100779){target=_blank}
34. OpenAI. New AI classifier for indicating AI-written text. 2023 Jan 31; updated 2023 Jul 20. Available from: [openai.com](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/){target=_blank}
35. Weber-Wulff D, Anohina-Naumeca A, Bjelobaba S, Foltýnek T, Guerrero-Dib J, Popoola O, et al. Testing of detection tools for AI-generated text. Int J Educ Integr. 2023;19:26. [doi:10.1007/s40979-023-00146-z](https://doi.org/10.1007/s40979-023-00146-z){target=_blank}
36. Sadasivan VS, Kumar A, Balasubramanian S, Wang W, Feizi S. Can AI-generated text be reliably detected? arXiv:2303.11156 \[Preprint\]. 2023. [arXiv:2303.11156](https://arxiv.org/abs/2303.11156){target=_blank}
37. Springer Nature. Springer Nature unveils two new AI tools to protect research integrity \[press release\]. 2024 Jun 12. Available from: [group.springernature.com](https://group.springernature.com/gp/group/media/press-releases/new-research-integrity-tools-using-ai/27200740){target=_blank}
38. Wiley. Wiley announces pilot of new AI-powered Papermill Detection service \[press release\]. 2024 Mar 13. Available from: [newsroom.wiley.com](https://newsroom.wiley.com/press-releases/press-release-details/2024/Wiley-announces-pilot-of-new-AI-powered-Papermill-Detection-service/default.aspx){target=_blank}
39. Genova Z. Enhancing research integrity through advanced technologies and expert oversight. Elsevier Connect. 2025 Mar 27. Available from: [elsevier.com](https://www.elsevier.com/connect/enhancing-research-integrity-through-advanced-technologies-and-expert-oversight){target=_blank}
40. National Institutes of Health. Supporting fairness and originality in NIH research applications. Notice NOT-OD-25-132. 2025 Jul 17. Available from: [grants.nih.gov](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-132.html){target=_blank}
41. Lu A, Lazar S, Rugamer D, Hua S, Metcalf K. AI-generated papers in the NeurIPS 2026 position paper track. NeurIPS Blog. 2026 Jun 2. Available from: [blog.neurips.cc](https://blog.neurips.cc/2026/06/02/ai-generated-papers-in-the-neurips-2026-position-paper-track/){target=_blank}
42. Vanderbilt University. Guidance on AI detection and why we’re disabling Turnitin’s AI detector. Brightspace at Vanderbilt. 2023 Aug 16. Available from: [vanderbilt.edu](https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/){target=_blank}
43. Bergin J. University wrongly accuses students of using artificial intelligence to cheat. ABC News (Australia). 2025 Oct 9. Available from: [abc.net.au](https://www.abc.net.au/news/2025-10-09/artificial-intelligence-cheating-australian-catholic-university/105863524){target=_blank}
44. Chechitelli A. Understanding the false positive rate for sentences of our AI writing detection capability. Turnitin Blog. 2023 Jun 14. Available from: [turnitin.com](https://www.turnitin.com/blog/understanding-the-false-positive-rate-for-sentences-of-our-ai-writing-detection-capability){target=_blank}
45. International Committee of Medical Journal Editors. Defining the role of authors and contributors \[Recommendations\]. Accessed 2026 Nov 27. Available from: [icmje.org](https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html){target=_blank}
46. Springer Nature. Editorial policies: artificial intelligence (AI). A risk-assessment framework for responsible AI use in research publishing. Nature Portfolio. Accessed 2026 Nov 27. Available from: [nature.com](https://www.nature.com/nature-portfolio/editorial-policies/ai){target=_blank}
47. Elsevier. Generative AI policies for journals. Updated 2026 Jun. Accessed 2026 Nov 27. Available from: [elsevier.com](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals){target=_blank}
48. IEEE. Author guidelines for artificial intelligence (AI)-generated text. IEEE Open. 2024 Apr 16. Available from: [open.ieee.org](https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/){target=_blank}
49. American Institute of Aeronautics and Astronautics. Ethical standards for publication of aeronautics and astronautics research. Accessed 2026 Nov 27. Available from: [aiaa.org](https://aiaa.org/publications/publish-with-aiaa/ethical-standards-for-publication-of-aeronautics-and-astronautics-research/){target=_blank}
50. The Mars Society. 2026 International Mars Society Convention: submit abstract. Accessed 2026 Nov 27. Available from: [convention.marssociety.org](https://convention.marssociety.org/submit-abstract){target=_blank}
51. The Mars Society. Submit an abstract: 2026 International Mars Society Convention \[call for abstracts\]. 2026. Available from: [mailchi.mp](https://mailchi.mp/marssociety/submit-an-abstract-2026-international-mars-society-convention-14565603){target=_blank}
52. Walters WH, Wilder EI. Fabrication and errors in the bibliographic citations generated by ChatGPT. Sci Rep. 2023;13:14045. [doi:10.1038/s41598-023-41032-5](https://doi.org/10.1038/s41598-023-41032-5){target=_blank}
53. Mata v. Avianca, Inc., No. 22-cv-1461 (PKC), Opinion and order on sanctions, ECF No. 54 (S.D.N.Y. 2023 Jun 22). Available from: [storage.courtlistener.com](https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.54.0_1.pdf){target=_blank}
54. NASA/JPL-Caltech/MSSS. Duluth after dust storm (PIA22330) \[image\]. 2018. Available from: [science.nasa.gov](https://science.nasa.gov/photojournal/duluth-after-dust-storm){target=_blank}
55. NASA. Guidelines for using NASA images and media. Updated 2026 Oct 27. Accessed 2026 Nov 27. Available from: [nasa.gov](https://www.nasa.gov/nasa-brand-center/images-and-media/){target=_blank}
56. NASA Jet Propulsion Laboratory. Opportunity hunkers down during dust storm. 2018 Jun (updated through Jul 26). Available from: [jpl.nasa.gov](https://www.jpl.nasa.gov/news/opportunity-hunkers-down-during-dust-storm/){target=_blank}
57. NASA. NASA’s Opportunity rover mission on Mars comes to end. 2019 Feb 13. Available from: [science.nasa.gov](https://science.nasa.gov/missions/mer/nasas-opportunity-rover-mission-on-mars-comes-to-end){target=_blank}
58. NASA. NASA’s InSight still hunting marsquakes as power levels diminish. 2022 May 17. Available from: [nasa.gov](https://www.nasa.gov/missions/insight/nasas-insight-still-hunting-marsquakes-as-power-levels-diminish){target=_blank}
59. Williams DR. Mars fact sheet. NASA Space Science Data Coordinated Archive. Updated 2025 May 19. Accessed 2026 Nov 27. Available from: [nssdc.gsfc.nasa.gov](https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html){target=_blank}
60. U.S. National Science Foundation. Award 2632685: Research Infrastructure: Category II: MESA (Multidisciplinary Environment for Scientific Advancement). 2026. Available from: [nsf.gov](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2632685){target=_blank}
61. Lemmon MT, Wolff MJ, Smith MD, Clancy RT, Banfield D, Landis GA, et al. Atmospheric imaging results from the Mars Exploration Rovers: Spirit and Opportunity. Science. 2004;306(5702):1753–1756. [doi:10.1126/science.1104474](https://doi.org/10.1126/science.1104474){target=_blank}
62. NASA/JPL-Caltech. Steady temperatures at Mars’ Gale Crater (PIA16913). 2013 Apr 8. Available from: [science.nasa.gov](https://science.nasa.gov/photojournal/steady-temperatures-at-mars-gale-crater){target=_blank}
63. Hecht MH, Kounaves SP, Quinn RC, West SJ, Young SMM, Ming DW, et al. Detection of perchlorate and the soluble chemistry of martian soil at the Phoenix lander site. Science. 2009;325(5936):64–67. [doi:10.1126/science.1172466](https://doi.org/10.1126/science.1172466){target=_blank}
64. Davila AF, Willson D, Coates JD, McKay CP. Perchlorate on Mars: a chemical hazard and a resource for humans. Int J Astrobiol. 2013;12(4):321–325. [doi:10.1017/S1473550413000189](https://doi.org/10.1017/S1473550413000189){target=_blank}
65. NASA/JPL-Caltech/SwRI. Radiation measurements on Mars. 2013 Dec 9. Available from: [science.nasa.gov](https://science.nasa.gov/resource/radiation-measurements-on-mars){target=_blank}
66. Hassler DM, Zeitlin C, Wimmer-Schweingruber RF, Ehresmann B, Rafkin S, Eigenbrode JL, et al. Mars’ surface radiation environment measured with the Mars Science Laboratory’s Curiosity rover. Science. 2014;343(6169):1244797. [doi:10.1126/science.1244797](https://doi.org/10.1126/science.1244797){target=_blank}
67. Zeitlin C, Hassler DM, Cucinotta FA, Ehresmann B, Wimmer-Schweingruber RF, Brinza DE, et al. Measurements of energetic particle radiation in transit to Mars on the Mars Science Laboratory. Science. 2013;340(6136):1080–1084. [doi:10.1126/science.1235989](https://doi.org/10.1126/science.1235989){target=_blank}
68. Southwest Research Institute. SwRI scientists publish first radiation measurements from the surface of Mars \[press release\]. 2013 Dec 9. Available from: [swri.org](https://www.swri.org/press-release/swri-scientists-publish-first-radiation-measurements-surface-mars){target=_blank}
69. NASA Human Research Program. 5 hazards of human spaceflight. Updated 2026 Jun 12. Accessed 2026 Nov 27. Available from: [nasa.gov](https://www.nasa.gov/hrp/hazards){target=_blank}
70. Coalition for Content Provenance and Authenticity. C2PA explainer, version 2.2. Accessed 2026 Nov 27. Available from: [spec.c2pa.org](https://spec.c2pa.org/specifications/specifications/2.2/explainer/Explainer.html){target=_blank}
71. European Commission. Quick facts: transparency rules for AI systems. Shaping Europe’s digital future. Updated 2026 Jul 29. Accessed 2026 Nov 27. Available from: [digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/factpages/quick-facts-transparency-rules-ai-systems){target=_blank}
72. European Parliament. AI Act: deal on simplification measures, ban on “nudifier” apps \[press release\]. 2026 May 7. Available from: [europarl.europa.eu](https://www.europarl.europa.eu/pdfs/news/expert/2026/5/press_release/20260427IPR42011/20260427IPR42011_en.pdf){target=_blank}
73. European Commission. Commission publishes Code of Practice on marking and labelling of AI-generated content. 2026 Jun 10. Available from: [digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/news/commission-publishes-code-practice-marking-and-labelling-ai-generated-content){target=_blank}
74. NASA Office of Safety and Mission Assurance. NASA reliability and maintainability (R&M) standard for spaceflight and support systems. NASA-STD-8729.1A. 2017 Jun 13. Available from: [standards.nasa.gov](https://standards.nasa.gov/sites/default/files/standards/NASA/A/0/nasa-std-87291a.pdf){target=_blank}
75. NASA. NASA reliability preferred practices for design and test. NASA-TM-4322. 1991 Sep. Available from: [ntrs.nasa.gov](https://ntrs.nasa.gov/citations/19920003068){target=_blank}
76. National Research Council. Safe on Mars: precursor measurements necessary to support human operations on the martian surface. Washington (DC): National Academies Press; 2002. [doi:10.17226/10360](https://doi.org/10.17226/10360){target=_blank}
77. Drake BG, editor. Human exploration of Mars design reference architecture 5.0. NASA/SP-2009-566. Washington (DC): NASA; 2009 Jul. Available from: [nasa.gov](https://www.nasa.gov/pdf/373665main_NASA-SP-2009-566.pdf){target=_blank}
