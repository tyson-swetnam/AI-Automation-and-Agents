# Agent guide -- AI Automation and Agents

This repository is the course site for **AI Automation and Agents**
(University of Arizona AI2S), built with [Zensical](https://zensical.org) and
deployed to <https://tyson-swetnam.github.io/AI-Automation-and-Agents/>. The
`docs/` tree is an **Open Knowledge Format (OKF) v0.2 knowledge bundle**
([spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)):
every content page carries YAML frontmatter with `type`, `description`,
`tags`, provenance (`generated`, `sources`, `authorship`), and lifecycle
(`status`, `stale_after`, `superseded_by`) fields. Section `index.md` files
are OKF §8 directory listings (no frontmatter); `docs/log.md` is the OKF §9
dated change log.

Most pages are produced by `scripts/migrate_wiki.py` from a pinned commit of
the [course wiki](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki)
while the content team keeps editing there. Interactive materials (quiz,
survey, notebooks, PDFs) live under `docs/materials/` and are served verbatim.
Instructor solution notebooks live under `instructor/`, outside the bundle.

## Reading the corpus

- `docs/llms.txt` -- linked outline of every page with its description.
- `docs/llms-full.txt` -- the entire corpus in one file, frontmatter
  included (about 1 MB).
- On the deployed site, any page URL + `index.md` is that page's Markdown
  source (e.g. `/modules/module-1/overview/index.md`); rendered pages carry
  `okf:*` meta tags and a `<link rel="alternate" type="text/markdown">`.
- **Trust**: a page without a `verified:` key is **unverified** (OKF §5.3).
  Migrated and agent-written pages are unverified by design; only an
  instructor's `verified: { by: "human:<netid>", at: ... }` promotes a page
  to human-reviewed.
- **Status**: `stable` is the default; `draft` means the content team has not
  finished the page or a content conflict is left visible (a "Draft"
  admonition sits at the top); `deprecated` means the page is history and
  points at its replacement through `superseded_by`.
- **`stale_after`**: pages tagged with a fast-moving tool (LangChain,
  LangGraph, CrewAI, LangSmith, Ollama, OpenWork, n8n, Colab, vendor pricing)
  carry an ISO 8601 horizon of last wiki change + 12 months; after it, treat
  version numbers, menus, and prices as suspect.
- **`docs/archive/`** is history: superseded drafts, the reversed lab
  checklists, old self-assessment quizzes. Those pages are built and listed
  in `archive/index.md` but never appear in the navigation; do not cite them
  as current course content.
- Chapter-quiz answer keys are public but collapsed inside `???` blocks;
  the interactive quiz carries its key in client-side JavaScript.

## Commands

```bash
uv venv --python 3.12 .venv                                        # system Python is too old
uv pip install --python .venv/bin/python -r requirements-dev.txt   # requirements.txt alone builds the site
.venv/bin/zensical serve                                           # live preview at http://localhost:8000
.venv/bin/zensical build --clean --strict                          # static site -> site/ ("No issues found")
.venv/bin/python scripts/okf_validate.py docs                      # OKF conformance (CI-enforced)
.venv/bin/python scripts/site_lint.py docs zensical.toml           # course rules on top of OKF (CI-enforced)
.venv/bin/python scripts/gen_llms_txt.py                           # regenerate llms.txt indexes (CI checks drift)
.venv/bin/python scripts/postbuild_agent_surface.py site           # after build: md mirror + okf meta + robots.txt
.venv/bin/python scripts/check_site.py site                        # post-build assertions on site/ (CI-enforced)
.venv/bin/python scripts/migrate_wiki.py                           # reproducible wiki -> docs/ pipeline
.venv/bin/python scripts/migrate_wiki.py --check                   # prove docs/ matches the pinned wiki (no writes)
.venv/bin/python scripts/migrate_wiki.py --only <wiki-page>        # convert a single page
.venv/bin/python scripts/migrate_wiki.py --notebooks               # also render the learner notebooks
.venv/bin/python scripts/render_notebooks.py                       # .ipynb -> lab pages with Colab badge
.venv/bin/python scripts/optimize_images.py [--report]             # images/ -> docs/assets/images/ (referenced only)
```

`.sources/` (gitignored) holds the clones the pipeline reads: `wiki-v2` (the
wiki, pinned to `WIKI_REF`) and `repo-v2` (images and notebooks, pinned to
`ASSETS_REF`). `WIKI_DIR` / `ASSETS_DIR` override the locations.

## Editing rules

1. **Pipeline-owned pages get fixed in the script, not in `docs/`.**
   Everything `scripts/migrate_wiki.py` writes -- the module pages
   (`overview`, `foundational-concepts`, `reading-guides`, `chapter-quizzes`,
   `activities`, `resources`, `lab-notebook`), Module 1 `readings/` and
   `worksheets/`, `course-design/{learning-design,development-plan,course-review-2026-07}.md`,
   `start-here/github-portfolio-setup.md`, everything under `archive/`, and
   `about/wiki-crosswalk.md` -- is regenerated on the next run. Put literal
   text fixes in the script's `PATCHES` dict, page metadata (title, type,
   tags, status, `stale_after`) in its `PAGES` entry, image alt text in
   `ALT_TEXT`, or set `frozen=True` and curate the file in-repo from then on.
   **Hand-written pages** are edited directly: `docs/index.md`,
   `start-here/*` (except the portfolio tutorial until it is frozen),
   `about/*` (except the crosswalk), `course-design/instructor-materials.md`,
   `modules/module-1/{concept-quiz,diagnostic-survey}.md`, and `log.md`.
   **Generated files** are never edited by hand: every section `index.md`,
   `about/wiki-crosswalk.md`, `docs/llms.txt`, `docs/llms-full.txt`.
   Run `migrate_wiki.py --check` after changing the script; it must exit 0.

2. **Every content page carries the frontmatter contract.** Start from
   `templates/page.md`:

   ```yaml
   ---
   title: "Module 1 Activities"
   description: "One sentence used by search, cards, llms.txt, and agents."
   type: Activity
   tags: [module-1, student-facing, activities, ollama]   # scope tag, audience tag, then topics
   module: 1                     # module pages only
   time_estimate: "8 hours"      # optional
   status: stable                # draft | stable | deprecated
   stale_after: "2027-07-22T00:00:00Z"   # required when a tool tag is present
   generated:
     by: "human:<netid>"         # or process:scripts/migrate_wiki.py, process:nbconvert, an agent id
     at: "2026-09-08T00:00:00Z"
   sources:
     - id: wiki-v2
       resource: "https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/Module-1:-Activities"
       title: "AI Automation and Agents v2 wiki: Module-1:-Activities"
       author: "Michelle Yung; Carlos Lizárraga-Celaya"
       last_modified: "2026-07-22T16:42:32-07:00"
   ---
   ```

   `type` comes from a closed set (the lint warns on anything else):

   | `type` | Use for |
   | --- | --- |
   | `Overview` | Module overviews (outcomes, schedule, grade weights) |
   | `Lesson` | Foundational-concepts lessons |
   | `Reading Guide` | Chapter-by-chapter guides to an assigned text |
   | `Reading` | A reading hosted on the site (summary, comparison, primer) |
   | `Activity` | Module activity sets and individual activities |
   | `Worksheet` | Fill-in worksheets (glossary, comparison diagram) |
   | `Lab` | Notebook labs and lab checklists |
   | `Assessment` | Chapter quizzes, the concept quiz, the diagnostic survey |
   | `Resource List` | Additional suggested resources |
   | `Tutorial` | Step-by-step setup guides (GitHub portfolio) |
   | `Guide` | How-to pages about the course itself (start here, contributing) |
   | `Course Design` | Learning design, development plan, reviews, instructor materials |
   | `Policy` | License and attribution |
   | `Reference` | Crosswalk, the agent guide, indexes of record |

   Root `docs/index.md` is the only `index.md` with frontmatter
   (`okf_version: "0.2"`, `title`, `description`, `hide`, `license`).
   Section indexes have none: `# Title`, a blurb, then
   `* [Title](file.md) - description` in nav order.

3. **Images go through `docs/assets/images/` only.** Put the full-resolution
   original in `images/`, reference it from the page as
   `![Alt text](../../assets/images/Name.png){ width="900" }` (byte-exact,
   case-sensitive filename; alt text required), and run
   `scripts/optimize_images.py`, which copies exactly the referenced files
   downscaled to at most 1600 px. Never link a GitHub `blob/main/images` URL
   or use `<p><img ...>`; the lint rejects both.

4. **Materials are self-contained and live under `docs/materials/`.** HTML
   activities make no `http(s)://` requests (the lint checks). Learner
   notebooks sit in `docs/materials/moduleN/` and are rendered to
   `modules/module-N/lab-notebook.md` by `render_notebooks.py`; the Colab,
   download, and GitHub buttons derive from the `REPO_SLUG` constant.
   Instructor solutions live under `instructor/` and are **never** linked,
   copied, or referenced from anything under `docs/`.

5. **Markdown that renders here, not on GitHub.** Callouts are admonitions
   (`!!! note`, `!!! tip "Hint"`, `!!! warning`); GitHub `> [!NOTE]` alert
   syntax is forbidden, as are one-column pipe tables used as callouts.
   Answer keys and feedback live only inside `??? success "Show answer and
   feedback"` collapsibles (the lint forbids a bare `Correct Answer:` or
   `**Feedback:**` line). Exactly one `# H1` per page, matching `title`.
   Code goes in fences with a language.

6. **Links.** Internal links are relative paths to the `.md` file
   (`../module-2/overview.md`, `../../assets/files/x.pdf`) and stay plain;
   external links get `{target=_blank}` (`scripts/externalize_links.py`
   sweeps them). Raw HTML `src`/`href` paths (the activity iframes) are not
   rewritten by the build, so they are written for the rendered directory URL
   (`../../../materials/module1/...`).

7. **Log every meaningful change** in `docs/log.md` under a `## YYYY-MM-DD`
   heading, newest first, bullets prefixed **Initialization / Migration /
   Creation / Update / Deprecation / Removal**.

8. **Before committing**: `okf_validate.py`, `site_lint.py`,
   `gen_llms_txt.py` (commit the regenerated `llms*.txt`), then
   `zensical build --clean --strict`. CI runs all of them and fails on any
   error or on llms drift.

9. **Never write `verified:`.** Only instructors do that, as
   `verified: { by: "human:<netid>", at: <ISO 8601> }`, and only after
   checking the page against the current syllabus and tools. Never emit a
   `generated.at` of "now": use one constant instant per change set so diffs
   stay reproducible.

10. **Deprecating a page**: set `status: deprecated`, add `superseded_by`
    (a relative path the lint resolves), move the file under `docs/archive/`
    (course-review documents may stay under `course-design/`), remove it from
    the nav, and log the change. Never delete a page that was ever deployed.
