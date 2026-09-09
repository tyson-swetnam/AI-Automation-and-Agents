---
title: "Instructor materials"
description: "Where the instructor solution notebooks live, the course's answer-key policy, LMS gating notes for quizzes and formative items, and how an instructor marks a page as verified."
type: Course Design
tags: [course, instructor-facing, instructor-solutions, answer-keys, lms, verification]
status: stable
generated:
  by: "claude/fable-5-1"
  at: "2026-09-08T00:00:00Z"
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
   project continues "in the same notebook" with instructions embedded there;
   the notebook does not contain them.
6. **Default lab provider.** The Module 5 notebook defaults to the NVIDIA API,
   while the prose in [Labs, Colab, and API keys](../start-here/labs-and-notebooks.md)
   describes Hugging Face Inference Providers as the Module 4-5 default.
7. **Module 2 chapter 5, question 1.** The wiki's answer key reads "B or C
   depending on interpretation"; the site publishes B and flags the question
   for review.
