---
title: "Instructor materials"
description: "Where the instructor solution notebooks live, the course's answer-key policy, LMS gating notes for quizzes and formative items, and how an instructor marks a page as verified."
type: Course Design
tags: [course, instructor-facing, instructor-solutions, answer-keys, lms, verification]
status: stable
generated:
  by: "claude/fable-5-1"
  at: "2026-09-09T00:00:00Z"
sources:
  - id: wiki-m1-overview
    resource: "https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1:-Overview"
    title: "AI Automation and Agents v2 wiki: Module-1:-Overview (grade weight summary)"
    author: "Carlos Lizárraga-Celaya; Michelle Yung"
    last_modified: "2026-07-22T16:32:11-07:00"
  - id: wiki-m2-overview
    resource: "https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-2:-Overview"
    title: "AI Automation and Agents v2 wiki: Module-2:-Overview (grade weight summary; the same pattern applies to Modules 3-5)"
    author: "Carlos Lizárraga-Celaya; Michelle Yung"
  - id: instructor-nb-m4
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/instructor/materials/module4/Module4_Instructor_Solution.ipynb"
    title: "Module 4 instructor solution notebook"
    author: "UA-AI2S course team"
  - id: instructor-nb-m5
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/instructor/materials/module5/Module5_Instructor_Solution.ipynb"
    title: "Module 5 instructor solution notebook"
    author: "UA-AI2S course team"
  - id: okf-spec
    resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"
    title: "Open Knowledge Format (OKF) v0.2 specification (§5.3 verification)"
    author: "team:google-cloud"
---

# Instructor materials

This page is for instructors and course maintainers. It records where the
non-student materials live, what the site deliberately makes public, how the
graded and formative items are meant to be configured in the LMS, and how you
sign off on a page you have reviewed.

!!! warning "This repository is public"

    Everything in the course repository - including the instructor solution
    notebooks under `instructor/` - is publicly readable on GitHub, and this
    site is publicly indexed. Students who look will find the solutions and
    the answer keys. Publishing the keys is deliberate: the quizzes are
    self-evaluating and the owners confirmed that policy on 2026-09-09.
    Whether the *solution notebooks* stay public is still open. Either way,
    grade what the LMS records, not what the site could reveal.

## Instructor solution notebooks

The learner notebooks for Modules 2-5 are published under `docs/materials/`
and rendered as lab pages. The two **instructor solution notebooks** are kept
in the repository *outside* `docs/`, so they are never built into the site,
never mirrored as Markdown, never listed in `llms.txt` or `llms-full.txt`, and
never linked from a student-facing page.

| Module | Instructor solution | Learner starter it solves |
| :-- | :-- | :-- |
| 4 | [`instructor/materials/module4/Module4_Instructor_Solution.ipynb`](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/instructor/materials/module4/Module4_Instructor_Solution.ipynb){target=_blank} | [Module 4 lab](../modules/module-4/lab-notebook.md) (`Module4_Learner_Starter.ipynb`) |
| 5 | [`instructor/materials/module5/Module5_Instructor_Solution.ipynb`](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/instructor/materials/module5/Module5_Instructor_Solution.ipynb){target=_blank} | [Module 5 lab](../modules/module-5/lab-notebook.md) (`Module5_Learner_Starter.ipynb`) |

Modules 2 and 3 have no separate solution notebook: their learner notebooks
are largely pre-written scaffolds with marked extension zones, and the
assessed work is the learner's extensions and written observations. The site's lint step fails any relative link from `docs/` into
`instructor/`, so the two notebooks above are linked only by their GitHub
URLs.

## Answer-key policy

Answer keys are **public but collapsed**, and the course owners have decided
to keep them that way (2026-09-09). The quizzes are written to be
self-evaluating: a learner answers, then reveals the feedback for every
option, not just the correct one. Keys are therefore visible to anyone who
opens a collapsible, and they appear in `llms-full.txt` and in each page's
Markdown mirror, so an AI assistant reading the site can see them too. Use the
LMS copy of a quiz whenever an attempt needs to be graded rather than
self-checked.

- **Chapter quizzes** (five per module, 25 questions per module, 125 in
  total). Each question's answer and feedback sits in a
  `??? success "Show answer and feedback"` collapsible on the module's
  *Chapter quizzes* page ([Module 1](../modules/module-1/chapter-quizzes.md),
  [Module 2](../modules/module-2/chapter-quizzes.md),
  [Module 3](../modules/module-3/chapter-quizzes.md),
  [Module 4](../modules/module-4/chapter-quizzes.md),
  [Module 5](../modules/module-5/chapter-quizzes.md)). Collapsed for readers,
  but present in the page's Markdown mirror (`…/index.md`) and in
  `llms-full.txt`, so search engines and AI assistants can read them.
- **Module 1 concept quiz.** The interactive HTML at
  `docs/materials/module1/module1_quiz.html` is self-contained: the key, the
  per-question feedback and the sequencing orders are constants and
  `data-answer` attributes in the page's own JavaScript and HTML, and the
  page renders an *Instructor Answer Key & Rationale* table at the bottom
  that is **visible without submitting** (it is not hidden by CSS or
  script). Grading is client-side; nothing is transmitted. The [concept quiz page](../modules/module-1/concept-quiz.md)
  tells students this. The two-attempt / best-score rule can only be enforced
  by the LMS copy.
- **Archived self-assessment quizzes** (the superseded Module 2 set under
  *Archive*) keep their answer-key tables in `??? note` collapsibles.
- **Diagnostic survey.** Ungraded, no key. The embedded copy stores answers
  only in the learner's browser; the LMS copy is the one you see before
  Module 2.

If the owners decide keys must be private, the cleanest change is to host
quizzes in the LMS and replace the collapsibles with a pointer; the
migration script's answer-key converter is the single place that would
change. Record the decision in the [update log](../log.md).

## LMS gating notes

The module overviews carry the authoritative *Grade weight summary* for each
module. Configure the LMS to match:

| Item | Module 1 | Modules 2-5 | LMS setting |
| :-- | :-- | :-- | :-- |
| Chapter quizzes (5 per module) | Self-check only | 100% of the module grade, 20% each | Graded; attempts per your cohort policy |
| Concept quiz (Module 1) | Formative | - | **Two attempts, best score retained**; no weight |
| Diagnostic survey (Module 1) | Ungraded baseline; responses visible to the instructor before Module 2 begins; learners get an anonymised cohort summary | - | Ungraded; release before the Module 1 readings |
| Guided lab submissions | Formative; required for the portfolio, not graded numerically | Notebook added to the learner's GitHub portfolio | Completion / portfolio check |
| Hands-on project | **Workflow Audit Project = the primary module grade**, scored with its rubric | Portfolio deliverable per the activities page | Module 1: rubric-graded |
| Discussion post + peer reply | Completion grade (participation, not content quality) | Required for the certificate, completion only; Module 5's is the capstone | Completion |

Formative items (labs, concept quiz, survey) are required for the portfolio
or the certificate but do not enter the numeric grade. The syllabus adds the
certificate rule: complete all five module projects and pass all five concept
quizzes at 70% or above.

## Marking a page verified

Every page on this site is generated content (converted from the wiki by
`scripts/migrate_wiki.py`, rendered from a notebook, or written by an
assistant and curated by maintainers) and is therefore **unverified** in
OKF terms until a person signs off on it. When you have read a page and
confirm it is correct for the current course, add a `verified` key to its
frontmatter:

```yaml
verified: { by: "human:<netid>", at: "2026-09-15T00:00:00Z" }
```

Rules enforced by the site's lint step:

- `by` must start with `human:` followed by your NetID. Assistants and
  scripts never write this key.
- `at` is an ISO 8601 instant and must be **later than `generated.at`**; if
  the page is regenerated afterwards, the key is removed and the page needs
  review again.
- Pages owned by the migration pipeline are regenerated from the wiki, so a
  `verified` key on one of them is lost on the next run unless the page is
  marked `frozen` in the script's page table. Ask a maintainer to freeze the
  page when you verify it, or verify only after the wiki cutover.

The rendered page then carries `<meta name="okf:trust-tier"
content="human-reviewed">`, and AI assistants are told to prefer
human-reviewed pages when answers conflict (see
[For AI agents](../about/ai-agents.md)). Add a line to the
[update log](../log.md) when you verify a batch of pages.

## Related pages

- [Formal learning design](learning-design.md) - the standard activity
  structure, Bloom's spiral, general course skills and module-specific
  skills.
- [Development plan](development-plan.md) - milestones and the development
  roadmap.
- [Course review, July 2026](course-review-2026-07.md) - a historical review
  of the course design, kept for reference.
- [Contributing](../about/contributing.md) - how to edit pages, the
  frontmatter contract and the local build.
- [License and attribution](../about/license-and-attribution.md) - CC BY 4.0
  for the content, BSD 3-Clause for the site code, and who holds copyright
  over which part.

## Open items for the course owners

1. Keep the instructor solution notebooks public in this repository, or move
   them to a private repository before the course runs. (Answer keys are
   settled: they stay public, see the policy above.)
2. Confirm the two-attempt rule for the concept quiz and the attempt policy
   for chapter quizzes in the LMS.
3. Decide who holds verification identities (`human:<netid>`) and when the
   first verification pass happens.

## Assessment revised for LangChain 1.4

The lab notebooks and code samples moved onto LangChain 1.4 in September 2026,
because LangChain 1.0 removed `AgentExecutor`, `create_react_agent`,
`RetrievalQA`, `langchain.chains`, `langchain.memory` and `langchain.prompts`
outright. The assessment content that examined those APIs has now been revised
to match, across the
[Module 2 chapter quizzes](../modules/module-2/chapter-quizzes.md) and
[reading guides](../modules/module-2/reading-guides.md), the
[Module 3 chapter quizzes](../modules/module-3/chapter-quizzes.md),
[reading guides](../modules/module-3/reading-guides.md) and
[activities](../modules/module-3/activities.md), and the
[Module 2 foundational concepts](../modules/module-2/foundational-concepts.md)
lesson the quizzes cite. This is the change the
[July 2026 course review](course-review-2026-07.md) asked for when it flagged
the `AgentExecutor` dependency.

**What was preserved.** Both quiz pages still hold 25 questions with 25 answer
keys. No correct answer moved to a different letter, no question was added or
dropped, and every item keeps its cognitive level: questions that asked a
learner to reason about a mechanism still do, rather than becoming vocabulary
recall. Distractors were rewritten to stay plausible against the current API
rather than being made obviously wrong.

**Two conventions now hold across every page.** First, one component vocabulary:
**LLM Backbone**, **Tool Registry**, **Action Executor** and **Memory Module**,
the four already used on the
[Module 2 resources](../modules/module-2/resources.md) page. The old five-item
list's fifth member, the output parser, is genuinely gone, because a
tool-calling model returns a structured call rather than text that has to be
parsed. That disappearance is taught rather than papered over. Second, one trace
format: every trace shown to a learner is what the lab's `show_trace` helper
actually prints, so `TOOL CALL:`, `ARGUMENTS:`, `OBSERVATION:` and
`[final] ANSWER:` rather than the `Thought:` / `Action:` labels a current agent
never emits.

**Where the pipeline owns the text.** All of these pages are generated by
`scripts/migrate_wiki.py`, so the revisions live in that script's `PATCHES`
table. Editing the Markdown under `docs/` directly will be reverted on the next
run. `python scripts/migrate_wiki.py --check` proves the two are in step.

!!! note "The architecture figure was redrawn"

    `AgentExecutor-Architecture.png` was a five-row LangChain 0.x design table
    using its own names: Agent (the LLM), Tool Descriptions, Tool Executor,
    Memory / State, Stopping Criteria. It is retired. In its place the Module 2
    foundational concepts page carries a Mermaid diagram of the loop
    `create_agent` actually runs and a table of the four components, so the
    figure now agrees with the vocabulary the rest of the course uses and the
    row-by-row crosswalk that made the old one readable is gone.

    Three things the crosswalk taught stand on their own and were kept as prose:
    that stopping is the loop's exit rule rather than a fifth component, that the
    0.x stopping conditions have no equivalent in the current API, and that
    older material names the same four components differently — which is still
    the place a learner meets both vocabularies at once. The diagram is Mermaid
    rather than an image so it cannot go stale as a binary; the retired PNG stays
    in `images/` as the provenance record and is no longer published.

## Content inconsistencies inherited from the source

A page-by-page review of the migration surfaced the following disagreements
*between* course materials. They exist in the wiki and the notebooks
themselves, so the migration reproduced them rather than silently deciding
which side is right. Each needs an author's call:

1. **Lab submission filenames.** The Module 2, 4 and 5 notebooks tell learners
   to rename their file using a different convention from the one required on
   the matching Activities page.
2. **Module 5 lab title.** The notebook's own heading calls it
   "LangSmith Observability & CI/CD Evaluation Pipeline", but its Lab B is the
   Comparative Observability Study; there is no CI/CD pipeline in the notebook.
   The page title follows the notebook.
3. **Learning-outcome labels.** The Module 4 lab cites "LO 4.5 and LO 4.6"
   while the Module 4 overview defines five outcomes and maps the lab to
   different numbers.
4. **Lab time budgets.** The Module 3 notebook says ~60 minutes where the
   Activities page budgets ~2 hours; Module 4 says 100-130 minutes against
   ~4 hours on its Activities page.
5. **Module 3 project instructions.** The Activities page says the hands-on
   project continues "in the same notebook" with instructions embedded there,
   and describes a four-run parameter experiment: chunk size 256, then 512,
   then MMR retrieval at `lambda_mult=0.5`, then metadata-filtered retrieval,
   closing with a plain-language reading of four RAGAS metric scores. Confirmed
   against the notebook in September 2026: none of that scaffolding exists. The
   notebook holds a single chunk-size setting, its headings run Setup,
   Configuration, Steps A1 to A4 and an optional metadata-filtering extension,
   its only mention of RAGAS is a forward reference to Module 5, and its
   submission checklist covers A1 to A4 only. The project carries no numeric
   weight in Modules 2–5, whose module grade is the chapter quizzes, but the
   syllabus requires all five module projects for completion, so a learner
   cannot currently finish the module as the page describes it. The open question is whether a second notebook was
   intended and never landed, or whether the project is meant to be authored by
   the learner in the same file; the answer decides whether the notebook gains
   cells or the page loses a promise, so it needs an author rather than a
   maintainer.
6. **Default lab provider.** The Module 5 notebook defaults to the NVIDIA API,
   while the prose in [Labs, Colab, and API keys](../start-here/labs-and-notebooks.md)
   describes Hugging Face Inference Providers as the Module 4-5 default.
7. **Module 2 chapter 5, question 1.** The wiki's answer key reads "B or C
   depending on interpretation"; the site publishes B and flags the question
   for review.
8. **Answer keys that explain three of four options.** Eight chapter-quiz
   questions name the correct answer and explain two distractors, leaving one
   with no feedback at all: Module 1 chapter 1 questions 1 (option C) and 2
   (option A), chapter 2 question 5 (option D) and chapter 5 question 1 (option
   B); Module 2 chapter 3 question 1 (option C) and chapter 5 question 1 (option
   C, the item in note 7 above); Module 4 chapter 1 question 3 (options A and C)
   and chapter 5 question 3 (option C). All eight are inherited from the wiki
   unchanged. They matter more here than they did there because these quizzes
   are self-evaluating: a learner who picked the unexplained option is told the
   right answer but never why theirs was wrong.

## What the retired posters said

Every page-top illustration was generated by NotebookLM and has been retired. Reading the 17
of them against the pages they sat on turned up 121 claims that appear in a poster and
nowhere in the page's text. Most are harmless framing. Four were teaching something the page
contradicts, and are recorded here because a learner who trusted the figure was misled:

1. **The Workflow Audit formula.** The Module 1 activities poster printed Automation
   Potential as Rule-Based Specification ÷ Consequence Severity, with no `+ 1` in the
   denominator. The page and the graded rubric both specify ÷ (Consequence Severity + 1).
2. **LangChain's paradigm.** The Module 1 resources poster classified LangChain as
   code-first. The page classifies it as low-code and reserves code-first for Claude Code
   and custom Python agents. The same poster's sample code used `LLMChain` and
   `initialize_agent`, both removed in LangChain 1.0.
3. **The desktop client's name.** The landing-page and Module 1 activities posters labelled
   it "Claude Cowork"; those pages say Claude Desktop, and Module 1's Lab B actually uses
   Openwork.
4. **The fourth memory pattern.** The Module 3 poster drew a Buffer to Summary to Vector
   Store progression. The page's fourth pattern is Hybrid; vector-store-backed
   conversational memory is not on the page at all.

Separately, several posters carried real subject matter that exists in no page text — the
Model Context Protocol and least-privilege permissions, the named EU AI Act risk tiers,
token-budget profiling, LangSmith as the observability tool, and SRE error budgets. None of
it was written into the pages, because inventing course content is an author's decision, not
a maintenance one. If any of it should be taught, it needs adding as prose first.
