---
title: "Guest Lecture: Say What You Mean"
description: "A 30-minute guest lecture on AI ethics and the resources CARC is building, for UNM's CS 491/591 Introduction to HCI: a primer on metadata, knowledge graphs, ML, RL and agents, vibe coding and voice prompts, and documentation written for AI agents."
type: Lesson
tags: [course, student-facing, guest-lecture, hci, ai-ethics, agentic-ai, vibe-coding, voice-dictation, llms-txt, okf, knowledge-graphs, carc]
time_estimate: "30 minutes"
status: stable
stale_after: "2027-11-13T00:00:00Z"
generated:
  by: "claude/opus-5-5"
  at: "2026-11-13T00:00:00Z"
sources:
  - id: lecture-html
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/docs/materials/guest-lectures/say-what-you-mean.html"
    title: "Say What You Mean: Vibe Coding, Voice Prompts and a Lakehouse Agents Can Read (interactive HTML slides)"
    author: "Tyson L. Swetnam"
  - id: cs-colloquium
    resource: "https://tyson-swetnam.github.io/2026-11-04-cs-colloquium-/"
    title: "How I Learned to Stop Worrying and Love the AI (UNM Computer Science Colloquium, Nov. 4, 2026; slides and per-slide evidence)"
    author: "Tyson L. Swetnam"
  - id: mesa-docs-llms
    resource: "https://idss-mesa.github.io/docs/llms.txt"
    title: "MESA documentation llms.txt and the For AI agents guide"
    author: "team:idss-mesa"
  - id: agentic-ai-loops
    resource: "https://tyson-swetnam.github.io/AI-Automation-and-Agents/guest-lectures/agentic-ai-loops/"
    title: "Guest Lecture: Agentic AI Loops (this site)"
    author: "Tyson L. Swetnam"
  - id: gpt101-ethics
    resource: "https://tyson-swetnam.github.io/intro-gpt/ethics/"
    title: "GPT 101: Ethics of Artificial Intelligence"
    author: "team:unm-carc"
  - id: carc-docs-llms
    resource: "https://carc.unm.edu/docs/llms.txt"
    title: "CARC documentation llms.txt and the For AI agents guide"
    author: "team:unm-carc"
  - id: hci-course
    resource: "https://handandmachine.org/classes/hci/schedule.html"
    title: "CS 491/591 Introduction to HCI, Fall 2026: schedule (Week 13, Ubiquitous Computing and Tangible Computing)"
    author: "Leah Buechley"
  - id: okf-spec
    resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"
    title: "Open Knowledge Format (OKF) v0.2 specification"
    author: "team:google-cloud"
---

# Guest Lecture: Say What You Mean

*Estimated time: ~30 min as delivered, ~50 min on your own with the backup slides*

**AI ethics, agentic AI, and what CARC is building, as the way we ask
questions of data changes.** This is the guest lecture Tyson Swetnam gave on
Friday, November 13, 2026, to Professor Leah Buechley's
[CS 491/591 Introduction to HCI](https://handandmachine.org/classes/hci/schedule.html){target=_blank}
at the University of New Mexico, in the course's week on ubiquitous and
tangible computing. Professor Buechley asked for two things: AI ethics, and
the resources the speaker is bringing to UNM's Center for Advanced Research
Computing (CARC). The lecture opens from the week's founding texts, Weiser's
"the most profound technologies are those that disappear" (1991) and Ishii and
Ullmer's *Tangible Bits* (1997), and follows one thread: how people ask
questions of data is changing, from writing queries to delegating to AI
agents, and the answers now rest on metadata, knowledge graphs and models
trained by machine learning and reinforcement learning, steered by how we
speak or type our prompts.

It reuses slides from the speaker's
[UNM Computer Science Colloquium](https://tyson-swetnam.github.io/2026-11-04-cs-colloquium-/){target=_blank}
of November 4, 2026, whose repository keeps evidence for every claim on every
slide, from his [GPT 101](https://tyson-swetnam.github.io/intro-gpt/ethics/){target=_blank}
ethics material, and from this site's [Agentic AI Loops](agentic-ai-loops.md)
lecture (*who decides what happens next*, *coding harnesses* and *AI
sandboxes*, in the backup section), whose slide viewer it also shares. Numbers
from the colloquium appear only where that evidence marks them supported, in
its corrected wording. The talk is 30 slides in four parts. Twenty-one backup
slides follow, including two short class activities, and 98 numbered
references close the deck.

[Open the lecture full screen](../materials/guest-lectures/say-what-you-mean.html){ .md-button .md-button--primary target=_blank }
[Download the slides (PDF)](../assets/files/Say-What-You-Mean-Guest-Lecture.pdf){ .md-button target=_blank }

<iframe class="course-embed course-embed--slides" src="../materials/guest-lectures/say-what-you-mean.html" title="Say What You Mean lecture slides" loading="lazy" allow="fullscreen" allowfullscreen></iframe>

!!! tip "Driving the slides"

    Click inside the slides first, then use ++arrow-right++ and ++arrow-left++
    (or ++space++) to move, ++home++ and ++end++ to jump to either end, ++n++
    for the speaker notes and ++f++ for full screen. On a touch screen, swipe.
    The menu in the toolbar jumps to any slide, every bracketed citation is a
    link to its source, and each slide has its own address (for example
    `say-what-you-mean.html#concerns`), so you can link to one. The file is
    self-contained: fonts and images are embedded and it makes no network
    requests, so it also works offline. The two demo slides link to their
    recordings in the colloquium deck, which needs a connection.

## The thread: how we ask questions of data is changing

| Step | What you do | What the answer rests on |
| :-- | :-- | :-- |
| **Query** | Write SQL or click filters | Knowing where the data is and what it is called |
| **Search** | Type keywords, read the ranked results | Your own reading and analysis |
| **Ask** | Type or say a question | What a language model read in training |
| **Delegate** | State a goal; an agent finds the data, runs models, checks, reports | Metadata, knowledge graphs, trained models, and how well you said what you meant |

Norman's vocabulary explains what changed: language models took the syntax out
of the *gulf of execution* (telling the computer what you want), though you
still have to articulate it, and they widened the *gulf of evaluation*
(checking that you got it). Subramonyam and colleagues (CHI 2024) add a *gulf
of envisioning* before either.

## Primer: six words

| Word | In one line |
| :-- | :-- |
| **Metadata** | Data about data: what, who, when, where, in what units. The FAIR principles ask that it be usable by machines, not only people. |
| **Ontology** | A formal, machine-readable statement of what terms mean: Carabidae, the ground beetles, is a family within Coleoptera, the beetles. |
| **Knowledge graph** | Things as nodes and relations as edges (specimen, *collected at*, site). GraphRAG lets a language model answer questions across one. |
| **Machine learning** | A system learns if its performance at a task improves with experience; supervised models learn from labeled examples to classify, detect or segment. |
| **Reinforcement learning** | Learning what to do by trial and error to maximize a reward. It tunes chatbots to follow instructions (RLHF) and trains reasoning and coding agents. |
| **Agentic AI and the harness** | A language model using tools in a loop, choosing its next step from what comes back. The harness is the app you talk to: Claude Code, Codex, Antigravity. |

The lecture stacks these on one real question from the speaker's NEON
ground-beetle project: the prompt, an agent trained with reinforcement
learning, columns tagged with ontology terms, measurements made by
conventional models (Grounding DINO, SAM 2.1 and a Mask2Former model), and a
DuckLake lakehouse. That is ontology-linked metadata, the building block of a
knowledge graph; MESA does not yet ship a knowledge-graph product.

### Every device is becoming a way to prompt

| Device | It used to | Now (vendors' own descriptions, Nov. 2026) |
| :-- | :-- | :-- |
| **Keyboard** | Type commands, code and text | Prompts and approvals in a harness: Claude Code in a terminal, IDE, desktop app or the web; Antigravity |
| **Mouse and display** | Point, click, read the screen | An agent clicks and types for you while you review: computer use in Claude Desktop and ChatGPT; Claude in Chrome, Gemini in Chrome, Perplexity's Comet |
| **Microphone** | Calls, occasional dictation | Dictation into Claude Code; spoken conversations in Claude's voice mode and ChatGPT Voice |
| **Camera** | Take pictures | Point the phone at something and talk about it with Gemini Live |
| **Phone and tablet** | Run apps you operate | A remote for agents that keep working: Claude Code Remote Control, Codex on iOS; always-on agents such as Claude Duet (research preview, Oct. 2026) and OpenAI's dots |

## Vibe and voice

Andrej Karpathy named vibe coding on February 2, 2025, in a post that
described a voice interface: "I just talk to Composer with SuperWhisper so I
barely even touch the keyboard." METR's July 2025 randomized trial found 16
experienced open-source developers took 19% longer with early-2025 AI tools
while believing they were 20% faster; in February 2026 METR called its
follow-up an unreliable signal, because more developers declined to work
without AI. The speaker's three dictation tools differ most in where the audio
goes: Claude Code's `/voice` and Wispr Flow transcribe in the cloud, while
superwhisper and MacWhisper can run local models such as Whisper. The habits:
say the context, pin down the identifiers, and read the transcript before
pressing Enter.

## AI ethics

Many AI principles are interface requirements. Floridi and Cowls (2019) give
five principles for AI in society: beneficence, non-maleficence, autonomy,
justice and explicability. The non-binding White House Blueprint for an AI Bill
of Rights (2022) adds *notice and explanation* and *human alternatives,
consideration, and fallback*: tell people an automated system is in use, and
let them reach a person.

| Concern | One example from the lecture |
| :-- | :-- |
| **Power and water** | The IEA projects data-centre electricity will more than double by 2030 to about 945 TWh, about what Japan uses today; cheaper AI may mean more AI, as Jevons saw with coal. |
| **Consent and credit** | Courts have held training on books to be fair use, but pirated copies went to trial; *Bartz v. Anthropic* settled for $1.5 billion, about $3,000 per work. |
| **Bias** | A widely used US care algorithm steered less care to Black patients because it used past health spending as a proxy for need (Obermeyer et al., 2019). |
| **Accountability** | In the July 2026 OpenAI and Hugging Face incident, roughly 7% of agent transcripts carried spoofed tool calls; an independent investigation established what happened. |

Three essays from 2026 frame the debate: Rutger Bregman ("abandoning the field
is not the same as stopping the technology"), Bill Gates ("we are not
preparing for it") and Dario Amodei ("we must slow the pace at which we
improve the capabilities of AI models"). All three reject "shut it down" and
ask for capacity to be built before the disruption arrives. The section closes
with Pope Leo XIV ("its future depends on the choices we make") and Alondra
Nelson ("Red states and blue states are writing AI Bills of Rights"), and the
speaker's own view that sitting it out is also a choice. GPT 101's
[ethics module](https://tyson-swetnam.github.io/intro-gpt/ethics/){target=_blank}
covers each topic in depth.

## CARC: documentation for agents, and resources you can use

CARC's documentation is published for people and for AI agents, an example of
what the lecture calls agentic, interactive documentation:

1. **[`llms.txt`](https://carc.unm.edu/docs/llms.txt){target=_blank}** lists
   about 80 pages, each with a one-line description and three addresses (the
   page, a Markdown twin and the raw source on GitHub), and `llms-full.txt`
   holds the whole corpus, about 178,000 tokens by CARC's own estimate. MESA,
   this course site, DUST 2026 and GPT 101 publish the same way.
2. **Frontmatter in the Open Knowledge Format** answers four questions any
   careful reader asks:

    | The reader asks | The page answers with |
    | :-- | :-- |
    | What is this? | `type`, `title`, `description` |
    | Where did it come from? | `generated`, `sources` |
    | How much should I trust it? | `verified`, from which OKF derives unverified, machine-confirmed or human-reviewed |
    | Is it still true? | `status`, `stale_after` |

    CARC's agent guide says plainly that an AI drafted it and that no person
    has verified it yet. The lecture treats that disclosure as an ethics
    feature.

3. **A human fallback.** "When the corpus does not answer a question, direct
   users to the humans … do not guess cluster-specific facts." That is the
   Blueprint's human-alternatives principle, written for an agent.

What CARC offers students and faculty, from its documentation as of November
13, 2026: the Easley cluster (8 NVIDIA H100 and 36 L40S GPUs) and Hopper (26
A100 and 2 V100), with the H100 and L40S partitions open through an allocation
the PI requests; free access for UNM researchers through an account and a PI's
project in ColdFront; help by ticket, email, office hours and consultation;
workshops, guest lectures, and open AI-ethics lessons in DUST 2026 and GPT 101.
CARC "does not currently provide hosted AI, large language model (LLM), or
agent services as a production service" and points researchers to the NAIRR
Pilot, ACCESS and CyVerse AI-VERDE. The lecture also shows the help desk's
self-hosted AI ticket summaries, as reported by CARC.

## Lecture outline

Each link opens the slides at that point.

| Part | Slides | What it covers |
| :-- | :-- | :-- |
| [Opening](../materials/guest-lectures/say-what-you-mean.html#cover) | 1-4 | The two asks; Weiser and Ishii and Ullmer on computing that disappears; the thread: how we ask questions of data is changing |
| [Part 1: Primer](../materials/guest-lectures/say-what-you-mean.html#p1) | 5-9 | Norman's gulfs; metadata, ontologies, knowledge graphs, machine learning, reinforcement learning, agents and harnesses; one question through every layer; how devices are becoming ways to prompt |
| [Part 2: Vibe and voice](../materials/guest-lectures/say-what-you-mean.html#p2) | 10-14 | Where vibe coding came from, the productivity and security evidence, three dictation tools and where your voice goes, a spoken brief |
| [Part 3: Ethics](../materials/guest-lectures/say-what-you-mean.html#p3) | 15-20 | Principles as interface requirements, four concerns, three 2026 essays, hallucination made checkable, who writes the rules |
| [Part 4: CARC](../materials/guest-lectures/say-what-you-mean.html#p4) | 21-28 | llms.txt and frontmatter for agents, a human fallback, the MESA pattern and lakehouse, what CARC offers, self-hosted AI on the help desk |
| [Close](../materials/guest-lectures/say-what-you-mean.html#lessons) | 29-30 | Four take-aways and questions |
| [Backup](../materials/guest-lectures/say-what-you-mean.html#appendix) | 31-49 | Nielsen's paradigms, Shneiderman's 1997 bet, the dial from vibe coding to agentic engineering, an agent contract, who makes what, the recorded beetle demo, HCI principles for agents, three slides from [Agentic AI Loops](agentic-ai-loops.md), MESA in depth |
| [Activities](../materials/guest-lectures/say-what-you-mean.html#activity-voice) | 50-51 | Two short class activities, below |
| [References](../materials/guest-lectures/say-what-you-mean.html#refs-1) | 52-58 | 98 sources, numbered in order of first citation |

## Activities

The two activities sit in the backup slides for an instructor who wants to
use part of the class period. They need nothing beyond the dictation built
into a phone or laptop, so no student data goes to a third-party service.

??? question "Activity 1: Dictate a brief (10 minutes, pairs)"

    1. Pick a small change to something you built this term.
    2. Type the prompt you would normally give a coding agent. Count the
       words.
    3. Dictate the same request for one minute. Count again.
    4. Compare: what did speech add (the goal, context, constraints, how to
       check the result)? What did transcription get wrong?

    *For facilitators:* ask pairs to swap prompts and predict what an agent
    would do with each version, then ask which gulf each version helped with,
    execution or evaluation.

??? question "Activity 2: Design for the second reader (15 minutes, groups)"

    1. Choose a site you use every week: a department page, a course site, a
       library guide.
    2. Write its `llms.txt`: one summary paragraph, then five links with
       one-line descriptions. What would an agent need first?
    3. Add trust signals to each link: what type of page it is, who wrote it,
       when it goes stale, and who checked it.

    *For facilitators:* point students at [llmstxt.org](https://llmstxt.org/){target=_blank}
    and at a real example such as MESA's
    [llms.txt](https://idss-mesa.github.io/docs/llms.txt){target=_blank}.
    The richest discussion is usually the trust question: who on staff would
    be allowed to mark a page verified, and what does a human reader gain or
    lose from the same signals?

## Reusing the lecture

The slides, this page and the PDF are licensed
[CC BY 4.0](../about/license-and-attribution.md) like the rest of the course.
The HTML file is a single self-contained document, so you can download it and
present from it without a network connection. The branding follows the UNM
Computer Science Colloquium deck of November 4, 2026, from which the
lakehouse, hallucination, ethics, CARC documentation, help-desk, demo and MESA
slides are reused; that repository keeps the evidence behind each of them. Three backup slides are
reused from [Agentic AI Loops](agentic-ai-loops.md), restyled. MESA is supported by the
U.S. National Science Foundation under Award OAC-2632685.

## References

Numbered in order of first citation on the slides, in PLOS style. The last
seven slides carry the same list with the slide numbers that cite each entry.

1. Weiser M. The computer for the 21st century. Sci Am. 1991;265(3):94–104. [doi:10.1038/scientificamerican0991-94](https://doi.org/10.1038/scientificamerican0991-94){target=_blank}
2. Ishii H, Ullmer B. Tangible bits: towards seamless interfaces between people, bits and atoms. In: Proceedings of the ACM SIGCHI Conference on Human Factors in Computing Systems (CHI ’97). New York: ACM; 1997. p. 234–241. [doi:10.1145/258549.258715](https://doi.org/10.1145/258549.258715){target=_blank}
3. Subramonyam H, Pea R, Pondoc C, Agrawala M, Seifert C. Bridging the gulf of envisioning: cognitive challenges in prompt based interactions with LLMs. In: Proceedings of the CHI Conference on Human Factors in Computing Systems (CHI ’24). New York: ACM; 2024. p. 1–19. [doi:10.1145/3613904.3642754](https://doi.org/10.1145/3613904.3642754){target=_blank}
4. Hutchins EL, Hollan JD, Norman DA. Direct manipulation interfaces. Hum Comput Interact. 1985;1(4):311–338. [doi:10.1207/s15327051hci0104_2](https://doi.org/10.1207/s15327051hci0104_2){target=_blank}
5. Riley J. Understanding metadata: what is metadata, and what is it for? A primer publication of the National Information Standards Organization. Baltimore: NISO; 2017. Available from: [groups.niso.org](http://groups.niso.org/higherlogic/ws/public/download/17446/Understanding%20Metadata.pdf){target=_blank}
6. Wilkinson MD, Dumontier M, Aalbersberg IJ, Appleton G, Axton M, Baak A, et al. The FAIR guiding principles for scientific data management and stewardship. Sci Data. 2016;3:160018. [doi:10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18){target=_blank}
7. Hogan A, Blomqvist E, Cochez M, d’Amato C, de Melo G, Gutierrez C, et al. Knowledge graphs. ACM Comput Surv. 2021;54(4):71:1–71:37. [doi:10.1145/3447772](https://doi.org/10.1145/3447772){target=_blank}
8. EMBL-EBI. Ontology Lookup Service (OLS4): NCBITaxon_41073 (Carabidae), hierarchical ancestors. Accessed 2026 Nov 13. Available from: [ebi.ac.uk](https://www.ebi.ac.uk/ols4/ontologies/ncbitaxon/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FNCBITaxon_41073){target=_blank}
9. Edge D, Trinh H, Cheng N, Bradley J, Chao A, Mody A, et al. From local to global: a graph RAG approach to query-focused summarization. arXiv:2404.16130 \[Preprint\]. 2024. [arXiv:2404.16130](https://arxiv.org/abs/2404.16130){target=_blank}
10. Mitchell TM. The discipline of machine learning. Pittsburgh: Carnegie Mellon University; 2006. Report No.: CMU-ML-06-108. Available from: [cs.cmu.edu](https://www.cs.cmu.edu/~tom/pubs/MachineLearning.pdf){target=_blank}
11. Sutton RS, Barto AG. Reinforcement learning: an introduction. 2nd ed. Cambridge (MA): MIT Press; 2018. Available from: [incompleteideas.net](http://incompleteideas.net/book/RLbook2020.pdf){target=_blank}
12. Ouyang L, Wu J, Jiang X, Almeida D, Wainwright CL, Mishkin P, et al. Training language models to follow instructions with human feedback. arXiv:2203.02155 \[Preprint\]. 2022. [arXiv:2203.02155](https://arxiv.org/abs/2203.02155){target=_blank}
13. OpenAI. OpenAI o1 system card. 2024 Dec 5. Available from: [cdn.openai.com](https://cdn.openai.com/o1-system-card-20241205.pdf){target=_blank}
14. OpenAI. Addendum to o3 and o4-mini system card: Codex. 2025 May 16. Available from: [cdn.openai.com](https://cdn.openai.com/pdf/8df7697b-c1b2-4222-be00-1fd3298f351d/codex_system_card.pdf){target=_blank}
15. Schluntz E, Zhang B. Building effective agents. Anthropic Engineering. 2024 Dec 19. Available from: [anthropic.com](https://www.anthropic.com/engineering/building-effective-agents){target=_blank}
16. Swetnam TL. neon-beetle-seg: models and data dictionary (docs/models.md, docs/schema.md), v0.2.0. GitHub. 2026 Oct. Available from: [github.com](https://github.com/tyson-swetnam/neon-beetle-seg/blob/main/docs/models.md){target=_blank}
17. Anthropic. Claude Code overview. Claude Code documentation. Accessed 2026 Nov 13. Available from: [code.claude.com](https://code.claude.com/docs/en/overview){target=_blank}
18. Google. Building the agentic future: developer highlights from I/O 2026. The Keyword. 2026 May 19. Available from: [blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/){target=_blank}
19. Anthropic. Let Claude use your computer in Cowork. Claude Help Center. Accessed 2026 Nov 13. Available from: [support.claude.com](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork){target=_blank}
20. OpenAI. Computer use. ChatGPT and Codex documentation. Accessed 2026 Nov 13. Available from: [learn.chatgpt.com](https://learn.chatgpt.com/docs/computer-use){target=_blank}
21. Anthropic. Claude in Chrome \[product page\]. Accessed 2026 Nov 13. Available from: [claude.com](https://claude.com/chrome){target=_blank}
22. Google. The new era of browsing: putting Gemini to work in Chrome. The Keyword. 2026 Jan 28. Available from: [blog.google](https://blog.google/products-and-platforms/products/chrome/gemini-3-auto-browse/){target=_blank}
23. Perplexity. Comet \[product page\]. Accessed 2026 Nov 13. Available from: [perplexity.ai](https://www.perplexity.ai/comet){target=_blank}
24. Anthropic. Use voice mode. Claude Help Center. Accessed 2026 Nov 13. Available from: [support.claude.com](https://support.claude.com/en/articles/11101966-use-voice-mode){target=_blank}
25. OpenAI. Voice. ChatGPT and Codex documentation. Accessed 2026 Nov 13. Available from: [learn.chatgpt.com](https://learn.chatgpt.com/docs/features/voice){target=_blank}
26. Google. Gemini gets more personal, proactive and powerful. The Keyword. 2025 May 20. Available from: [blog.google](https://blog.google/products-and-platforms/products/gemini/gemini-app-updates-io-2025/){target=_blank}
27. Anthropic. Continue local sessions from any device with Remote Control. Claude Code documentation. Accessed 2026 Nov 13. Available from: [code.claude.com](https://code.claude.com/docs/en/remote-control){target=_blank}
28. OpenAI. Codex mobile. ChatGPT and Codex documentation. Accessed 2026 Nov 13. Available from: [learn.chatgpt.com](https://learn.chatgpt.com/docs/mobile){target=_blank}
29. Anthropic. Introducing Claude Duet. Claude blog. 2026 Oct 21. Available from: [claude.com](https://claude.com/blog/claude-duet){target=_blank}
30. OpenAI. dots: overview. ChatGPT and Codex documentation. Accessed 2026 Nov 13. Available from: [learn.chatgpt.com](https://learn.chatgpt.com/docs/dots?nav=overview){target=_blank}
31. Karpathy A. “There’s a new kind of coding I call ‘vibe coding’…” \[post on X\]. 2025 Feb 2. Available from: [x.com](https://x.com/karpathy/status/1886192184808149383){target=_blank}
32. Collins Dictionary. Collins’ Word of the Year 2025: AI meets authenticity as society shifts. Collins Language Lovers blog. 2025 Nov 6. Available from: [blog.collinsdictionary.com](https://blog.collinsdictionary.com/language-lovers/collins-word-of-the-year-2025-ai-meets-authenticity-as-society-shifts){target=_blank}
33. METR. Measuring the impact of early-2025 AI on experienced open-source developer productivity. 2025 Jul 10. Available from: [metr.org](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/){target=_blank}
34. METR. We are changing our developer productivity experiment design. 2026 Feb 24. Available from: [metr.org](https://metr.org/blog/2026-02-24-uplift-update/){target=_blank}
35. Spracklen J, Wijewickrama R, Sakib AHMN, Maiti A, Viswanath B, Jadliwala M. We have a package for you! A comprehensive analysis of package hallucinations by code generating LLMs. In: 34th USENIX Security Symposium (USENIX Security ’25). 2025. arXiv:2406.10279. [arXiv:2406.10279](https://arxiv.org/abs/2406.10279){target=_blank}
36. Veracode. AI-generated code poses major security risks in nearly half of all development tasks, Veracode research reveals \[press release on the 2025 GenAI Code Security Report\]. 2025 Jul 30. Available from: [veracode.com](https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/){target=_blank}
37. Radford A, Kim JW, Xu T, Brockman G, McLeavey C, Sutskever I. Robust speech recognition via large-scale weak supervision. In: Proceedings of the 40th International Conference on Machine Learning (ICML). PMLR 202; 2023. p. 28492–28518. [arXiv:2212.04356](https://arxiv.org/abs/2212.04356){target=_blank}
38. Anthropic. Voice dictation. Claude Code documentation. Accessed 2026 Nov 13. Available from: [code.claude.com](https://code.claude.com/docs/en/voice-dictation){target=_blank}
39. Wispr. Wispr Flow features \[vendor documentation\]. Accessed 2026 Nov 13. Available from: [wisprflow.ai](https://wisprflow.ai/features){target=_blank}
40. Wispr. Wispr Flow privacy \[vendor documentation\]. Accessed 2026 Nov 13. Available from: [wisprflow.ai](https://wisprflow.ai/privacy){target=_blank}
41. superwhisper. Documentation: overview and coding agents \[vendor documentation\]. Accessed 2026 Nov 13. Available from: [superwhisper.com](https://superwhisper.com/docs){target=_blank}
42. Good Snooze (Bruin J). MacWhisper \[vendor website\]. Accessed 2026 Nov 13. Available from: [macwhisper.com](https://macwhisper.com/){target=_blank}
43. Floridi L, Cowls J. A unified framework of five principles for AI in society. Harv Data Sci Rev. 2019;1(1). [doi:10.1162/99608f92.8cd550d1](https://doi.org/10.1162/99608f92.8cd550d1){target=_blank}
44. White House Office of Science and Technology Policy. Blueprint for an AI Bill of Rights: making automated systems work for the American people. 2022 Oct. Available from: [bidenwhitehouse.archives.gov](https://bidenwhitehouse.archives.gov/ostp/ai-bill-of-rights/){target=_blank}
45. International Energy Agency. AI is set to drive surging electricity demand from data centres while offering the potential to transform how the energy sector works \[press release\]. 2025 Apr 10. Available from: [iea.org](https://www.iea.org/news/ai-is-set-to-drive-surging-electricity-demand-from-data-centres-while-offering-the-potential-to-transform-how-the-energy-sector-works){target=_blank}
46. Jevons WS. The coal question. London: Macmillan; 1865. Chapter VII. Available from: [econlib.org](https://www.econlib.org/library/YPDBooks/Jevons/jvnCQ.html?chapter_num=9){target=_blank}
47. Bartz v. Anthropic PBC, No. 3:24-cv-05417 (N.D. Cal.). Order granting final approval of class action settlement. 2026 Jul 20. Available from: [publishers.org](https://publishers.org/wp-content/uploads/2026/07/Order-Granting-Final-Approval-of-Settlement171.pdf){target=_blank}
48. Obermeyer Z, Powers B, Vogeli C, Mullainathan S. Dissecting racial bias in an algorithm used to manage the health of populations. Science. 2019;366(6464):447–453. [doi:10.1126/science.aax2342](https://doi.org/10.1126/science.aax2342){target=_blank}
49. METR, Redwood Research. Brief independent investigation of agents’ behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident. 2026 Aug 26. Available from: [metr.org](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/){target=_blank}
50. UNM Center for Advanced Research Computing. GPT 101: Ethics of artificial intelligence. 2026. CC BY 4.0. Available from: [tyson-swetnam.github.io](https://tyson-swetnam.github.io/intro-gpt/ethics/){target=_blank}
51. Bregman R. An inconvenient truth about AI. Substack. 2026 Jun 7. Available from: [rutgerbregman.substack.com](https://rutgerbregman.substack.com/p/an-inconvenient-truth-about-ai){target=_blank}
52. Gates B. The turbulent AI era is here. The choices we make now are critical. Gates Notes. 2026 Aug 26. Available from: [gatesnotes.com](https://www.gatesnotes.com/a-turbulent-ai-era-and-critical-choices-to-make){target=_blank}
53. Amodei D. We must pace the frontier. 2026 Sep. Available from: [darioamodei.com](https://darioamodei.com/post/we-must-pace-the-frontier){target=_blank}
54. Swetnam TL. How I learned to stop worrying and love the AI \[UNM Computer Science Colloquium; slides and per-slide evidence\]. 2026 Nov 4. Available from: [tyson-swetnam.github.io](https://tyson-swetnam.github.io/2026-11-04-cs-colloquium-/){target=_blank}
55. Pope Leo XIV (@Pontifex). “The future of #ArtificialIntelligence is not pre-determined…” \[post on X\]. 2026 Oct 30. Available from: [x.com](https://x.com/Pontifex/status/2116146977230459383){target=_blank}
56. Nelson A. “Red states and blue states are writing AI Bills of Rights” \[post on Bluesky\]. 2026 May 14. Available from: [bsky.app](https://bsky.app/profile/alondra.bsky.social/post/3mltg2efhms2a){target=_blank}
57. Howard J. /llms.txt: a proposal to provide information to help LLMs use websites. Answer.AI. 2024 Sep 3. Available from: [answer.ai](https://www.answer.ai/posts/2024-09-03-llmstxt.html){target=_blank}
58. Howard J. The /llms.txt file \[proposal, version 2\]. llmstxt.org. 2024 Sep 3; modified 2026 Aug 10. Available from: [llmstxt.org](https://llmstxt.org/){target=_blank}
59. UNM Center for Advanced Research Computing. CARC documentation llms.txt. Accessed 2026 Nov 13. Available from: [carc.unm.edu](https://carc.unm.edu/docs/llms.txt){target=_blank}
60. MESA documentation. llms.txt \[outline of the MESA MCP stack documentation\]. idss-mesa/docs. Accessed 2026 Nov 13. Available from: [idss-mesa.github.io](https://idss-mesa.github.io/docs/llms.txt){target=_blank}
61. UNM Center for Advanced Research Computing. DUST 2026: lessons on open science, research data management and AI ethics. llms.txt. Accessed 2026 Nov 13. Available from: [unm-carc.github.io](https://unm-carc.github.io/dust-2026/llms.txt){target=_blank}
62. Google Cloud. Open Knowledge Format (OKF), version 0.2 \[specification\]. GoogleCloudPlatform/knowledge-catalog. Available from: [github.com](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md){target=_blank}
63. UNM Center for Advanced Research Computing. CARC documentation: For AI agents. 2026 Sep 12 \[accessed 2026 Nov 13\]. Available from: [carc.unm.edu](https://carc.unm.edu/docs/about/ai-agents/){target=_blank}
64. MESA documentation. For AI agents. idss-mesa/docs. 2026 Oct 8 \[accessed 2026 Nov 13\]. Available from: [idss-mesa.github.io](https://idss-mesa.github.io/docs/about/ai-agents/){target=_blank}
65. Armbrust M, Ghodsi A, Xin R, Zaharia M. Lakehouse: a new generation of open platforms that unify data warehousing and advanced analytics. In: 11th Conference on Innovative Data Systems Research (CIDR ’21). 2021. Available from: [cidrdb.org](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf){target=_blank}
66. Raasveldt M, Mühleisen H. DuckLake: SQL as a lakehouse format. DuckDB blog. 2025 May 27. Available from: [duckdb.org](https://duckdb.org/2025/05/27/ducklake.html){target=_blank}
67. The DuckDB team. DuckLake 1.0: the lakehouse format built on SQL reaches production-readiness. 2026 Apr 13. Available from: [ducklake.select](https://ducklake.select/2026/04/13/ducklake-10/){target=_blank}
68. MESA documentation. mesa-ducklake: the AVU metadata-history library that backs mesa-mcp. idss-mesa/docs. Available from: [idss-mesa.github.io](https://idss-mesa.github.io/docs/servers/mesa-ducklake/){target=_blank}
69. iRODS Consortium. iRODS 5.0.2 documentation: metadata (imeta). Available from: [docs.irods.org](https://docs.irods.org/5.0.2/icommands/metadata/){target=_blank}
70. U.S. National Science Foundation. Award 2632685: Research Infrastructure: Category II: MESA (Multidisciplinary Environment for Scientific Advancement). 2026. Available from: [nsf.gov](https://www.nsf.gov/awardsearch/show-award/?AWD_ID=2632685){target=_blank}
71. UNM Center for Advanced Research Computing. CARC documentation: Systems overview. Accessed 2026 Nov 13. Available from: [carc.unm.edu](https://carc.unm.edu/docs/systems/overview/){target=_blank}
72. UNM Center for Advanced Research Computing. CARC documentation: General FAQ. Accessed 2026 Nov 13. Available from: [carc.unm.edu](https://carc.unm.edu/docs/faq/general/){target=_blank}
73. UNM Center for Advanced Research Computing. CARC documentation: Getting started at CARC. Accessed 2026 Nov 13. Available from: [carc.unm.edu](https://carc.unm.edu/docs/getting-started/overview/){target=_blank}
74. UNM Center for Advanced Research Computing. CARC documentation: Getting help. Accessed 2026 Nov 13. Available from: [carc.unm.edu](https://carc.unm.edu/docs/support/help/){target=_blank}
75. UNM Center for Advanced Research Computing. CARC documentation: Workshops and slides. Accessed 2026 Nov 13. Available from: [carc.unm.edu](https://carc.unm.edu/docs/training/workshops/){target=_blank}
76. UNM Center for Advanced Research Computing. GPT 101: a workshop on generative AI and prompt engineering. 2026. CC BY 4.0. Available from: [tyson-swetnam.github.io](https://tyson-swetnam.github.io/intro-gpt/){target=_blank}
77. UNM Center for Advanced Research Computing. AI research resources. Accessed 2026 Nov 13. Available from: [carc.unm.edu](https://carc.unm.edu/ai-research-resources/){target=_blank}
78. NVIDIA. DGX Spark hardware overview. NVIDIA documentation. Accessed 2026 Nov 13. Available from: [docs.nvidia.com](https://docs.nvidia.com/dgx/dgx-spark/hardware.html){target=_blank}
79. Shneiderman B. Direct manipulation: a step beyond programming languages. Computer. 1983;16(8):57–69. [doi:10.1109/MC.1983.1654471](https://doi.org/10.1109/MC.1983.1654471){target=_blank}
80. Nielsen J. AI: first new UI paradigm in 60 years. Nielsen Norman Group. 2023 Jun 18. Available from: [nngroup.com](https://www.nngroup.com/articles/ai-paradigm/){target=_blank}
81. Shneiderman B. Direct manipulation for comprehensible, predictable and controllable user interfaces. 1997. Adapted from: Designing the user interface. 3rd ed. Reading (MA): Addison Wesley; 1997. Available from: [cs.umd.edu](https://www.cs.umd.edu/users/ben/papers/Shneiderman1997Direct2.pdf){target=_blank}
82. Anthropic. Introducing the Model Context Protocol. 2024 Nov 25. Available from: [anthropic.com](https://www.anthropic.com/news/model-context-protocol){target=_blank}
83. Model Context Protocol. What is the Model Context Protocol (MCP)? Documentation. Available from: [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/getting-started/intro){target=_blank}
84. Willison S. Not all AI-assisted programming is vibe coding (but vibe coding rocks). simonwillison.net. 2025 Mar 19. Available from: [simonwillison.net](https://simonwillison.net/2025/Mar/19/vibe-coding/){target=_blank}
85. Karpathy A. \[Post on X proposing “agentic engineering”\]. 2026 Feb 4. Available from: [x.com](https://x.com/karpathy/status/2019137879310836075){target=_blank}
86. Sarkar A, Drosos I. Vibe coding: programming through conversation with artificial intelligence. In: Proceedings of the 36th Annual Conference of the Psychology of Programming Interest Group (PPIG 2025). 2025. arXiv:2506.23253. [arXiv:2506.23253](https://arxiv.org/abs/2506.23253){target=_blank}
87. Center for Advanced Research Computing, University of New Mexico. AI Automation and Agents \[online course\]: AGENTS.md, the contract for agents editing the course site. 2026. CC BY 4.0. Available from: [github.com](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/AGENTS.md){target=_blank}
88. Ruan S, Wobbrock JO, Liou K, Ng A, Landay JA. Comparing speech and keyboard text entry for short messages in two languages on touchscreen phones. Proc ACM Interact Mob Wearable Ubiquitous Technol. 2017;1(4):159. [doi:10.1145/3161187](https://doi.org/10.1145/3161187){target=_blank}
89. Nielsen J. The articulation barrier: prompt-driven AI UX hurts usability. Jakob Nielsen on UX. 2023 Jun 26. Available from: [jakobnielsenphd.substack.com](https://jakobnielsenphd.substack.com/p/prompt-driven-ai-ux-hurts-usability){target=_blank}
90. Nielsen J. Prompt augmentation: UX design patterns for better AI prompting. Jakob Nielsen on UX. 2025 Mar 27. Available from: [jakobnielsenphd.substack.com](https://jakobnielsenphd.substack.com/p/prompt-augmentation){target=_blank}
91. Nowrin S, Ordóñez P, Vertanen K. Exploring motor-impaired programmers’ use of speech recognition. In: Proceedings of the 24th International ACM SIGACCESS Conference on Computers and Accessibility (ASSETS ’22). New York: ACM; 2022. [doi:10.1145/3517428.3550392](https://doi.org/10.1145/3517428.3550392){target=_blank}
92. Swetnam TL. neon-beetle-seg: segmenting and measuring NEON ground beetles \[software and DuckLake lakehouse\]. GitHub. Available from: [github.com](https://github.com/tyson-swetnam/neon-beetle-seg){target=_blank}
93. Amershi S, Weld D, Vorvoreanu M, Fourney A, Nushi B, Collisson P, et al. Guidelines for human-AI interaction. In: Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems (CHI ’19). New York: ACM; 2019. p. 1–13. [doi:10.1145/3290605.3300233](https://doi.org/10.1145/3290605.3300233){target=_blank}
94. Horvitz E. Principles of mixed-initiative user interfaces. In: Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI ’99). New York: ACM; 1999. p. 159–166. [doi:10.1145/302979.303030](https://doi.org/10.1145/302979.303030){target=_blank}
95. Barke S, James MB, Polikarpova N. Grounded Copilot: how programmers interact with code-generating models. Proc ACM Program Lang. 2023;7(OOPSLA1):85–111. [doi:10.1145/3586030](https://doi.org/10.1145/3586030){target=_blank}
96. Swetnam TL. Guest lecture: Agentic AI loops: sequence, selection, iteration \[slides\]. AI Automation and Agents, University of New Mexico. 2026 Sep 22. CC BY 4.0. Available from: [tyson-swetnam.github.io](https://tyson-swetnam.github.io/AI-Automation-and-Agents/guest-lectures/agentic-ai-loops/){target=_blank}
97. Anthropic. Beyond permission prompts: making Claude Code more secure and autonomous. 2025 Oct 20. Available from: [anthropic.com](https://www.anthropic.com/engineering/claude-code-sandboxing){target=_blank}
98. MESA: Multidisciplinary Environment for Scientific Advancement. NSF Award OAC-2632685. University of New Mexico. Available from: [idss-mesa.github.io](https://idss-mesa.github.io/){target=_blank}
