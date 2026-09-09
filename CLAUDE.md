# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Start with AGENTS.md

`AGENTS.md` is the contract for this repository: what the `docs/` OKF v0.2 bundle is, which pages the migration pipeline owns versus which are hand-edited, the frontmatter contract and closed `type` set, and the rules CI enforces. Read it before touching anything under `docs/` or `scripts/`. This file adds only the command list and the conventions for the interactive HTML activities.

Ownership in short: pages written by `scripts/migrate_wiki.py` are fixed through its `PATCHES` / `PAGES` / `ALT_TEXT` tables (or frozen), not edited in place; `docs/index.md`, `start-here/*`, `about/*`, `course-design/instructor-materials.md`, `modules/module-1/{concept-quiz,diagnostic-survey}.md`, and `docs/log.md` are hand-written; section `index.md` files, `about/wiki-crosswalk.md`, and `docs/llms*.txt` are generated. Never write a `verified:` key. Never link anything under `instructor/` from `docs/`.

## Commands

```bash
uv venv --python 3.12 .venv                                        # system Python is too old
uv pip install --python .venv/bin/python -r requirements-dev.txt   # requirements.txt alone builds the site
.venv/bin/zensical serve                                           # live preview at http://localhost:8000
.venv/bin/zensical build --clean --strict                          # static site -> site/
.venv/bin/python scripts/okf_validate.py docs                      # OKF conformance (CI)
.venv/bin/python scripts/site_lint.py docs zensical.toml           # course lint (CI)
.venv/bin/python scripts/gen_llms_txt.py                           # regenerate llms.txt indexes (CI checks drift)
.venv/bin/python scripts/postbuild_agent_surface.py site           # after build: md mirror + okf meta + robots.txt
.venv/bin/python scripts/check_site.py site                        # post-build assertions (CI)
.venv/bin/python scripts/migrate_wiki.py [--check|--only <page>|--notebooks]
.venv/bin/python scripts/render_notebooks.py
.venv/bin/python scripts/optimize_images.py [--report]
```

Before committing content: `okf_validate.py`, `site_lint.py`, `gen_llms_txt.py`, a strict build, and a dated entry in `docs/log.md`.

## Interactive HTML activities

`docs/materials/module1/module1_quiz.html` (Module 1 concept quiz) and `docs/materials/module1/diagnostic_survey.html` (ungraded diagnostic survey) are single-file, zero-dependency pages: inline CSS with a `:root` variable palette, inline vanilla JS, no external scripts, stylesheets, fonts, or requests (`site_lint.py` rejects any `http(s)://` asset reference). Preserve that so instructors can distribute a single file. Each ships with a PDF twin (`Module_1_Quiz.pdf`, `Diagnostic_Knowledge_Survey.pdf`); keep the pair in sync when editing one.

The site embeds them: `docs/modules/module-1/concept-quiz.md` and `diagnostic-survey.md` iframe the HTML with `src` written for the rendered directory URL (`../../../materials/module1/...`) and offer full-screen and PDF links. The Markdown pages carry the OKF frontmatter; the HTML files carry none. Grading and validation happen client-side; nothing is sent anywhere.

Conventions in the current files:

- **Quiz** (`module1_quiz.html`): 15 questions in three types, tagged to learning outcomes with `<span class="lo">LO 1.1</span>`. The answer key and feedback are JS constants at the top of the `<script>`: `MC` (multiple-choice and scenario-classification answers, `q1..q11`), `FB` (per-option feedback), `SEQ` (drag-and-drop sequencing, `12..15`), `SEQ_FB`. Cards are `id="card-N"` with feedback in `id="fb-N"`; sequencing lists are `id="seq-N"` with `.seq-item` children whose `data-text` must match the strings in `SEQ[N]` **exactly**, in order. The count 15 is a literal repeated in the header `.chip` badges ("15 Questions", "6 MC Definitions", "5 Scenario Classification", "4 Sequencing"), the progress label `#plbl` ("0 of 15 answered"), the `#pbar` width, and the scoring (`total/15`); update them all together with the constants when adding or removing a question.
- **Survey** (`diagnostic_survey.html`): `const TOTAL = 12` questions; cards are `id="card-qN"` with inputs `name="qN"`; progress is `#pbar` / `#plabel`; 1-5 scale buttons write to hidden inputs (`#q8-val`, `#q11-val`); submit validates required fields, shows a summary rather than a score, and saves the submitted responses to `localStorage` (`ai_agents_baseline_survey`). Update `TOTAL` and the header counts together when adding a question.

Learning-outcome codes (LO N.N) come from the syllabus (`docs/assets/files/AI_Automation_Agents_Syllabus_v2.pdf`); reuse existing codes rather than inventing new ones.
