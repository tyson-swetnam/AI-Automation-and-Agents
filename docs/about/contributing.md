---
title: "Contributing to the course site"
description: "How to fix a page, the OKF frontmatter contract every content page follows, how to read a failing CI check, how to build the site locally, what the pipeline scripts own, and the house style."
type: Reference
tags: [course, instructor-facing, contributing, okf, frontmatter, ci, style-guide]
status: stable
generated:
  by: "claude/fable-5-1"
  at: "2026-09-08T00:00:00Z"
sources:
  - id: carc-contributing
    resource: "https://github.com/UNM-CARC/docs/blob/main/docs/about/contributing.md"
    title: "CARC Documentation: Contributing to these docs (adapted)"
    author: "team:unm-carc"
  - id: okf-spec
    resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"
    title: "Open Knowledge Format (OKF) v0.2 specification"
    author: "team:google-cloud"
---

# Contributing to the course site

This site is a git repository of Markdown files under `docs/`, built with
[Zensical](https://zensical.org){target=_blank} and structured as an
[Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md){target=_blank}
knowledge bundle: every page is readable by people *and* consumable by AI
agents, with provenance and lifecycle signals in its frontmatter. The content
was converted from the course wiki
([UA-AI2S/AI-Automation-and-Agents-v2](https://github.com/UA-AI2S/AI-Automation-and-Agents-v2){target=_blank})
by a reproducible script, and while the content team still edits the wiki the
script can be re-run to pick up their changes. This page tells you how to
change things without fighting that pipeline.

## Small fixes

Every page has an **edit button** (:material-pencil:) at the top right that
opens the source file on GitHub. Fix the text, propose the change as a pull
request, and CI validates it; once merged it is deployed automatically.

Before you do, check the page's frontmatter:

- `generated.by: "process:scripts/migrate_wiki.py"` means the page is
  **owned by the pipeline** and will be regenerated from the wiki. Either
  make the fix in the wiki (it arrives at the next migration run) or add an
  exact-literal entry to the script's `PATCHES` table. A hand edit to the
  file itself is overwritten.
- `generated.by: "process:nbconvert"` means a lab page rendered from a
  notebook; edit the `.ipynb` under `docs/materials/` and re-run the render.
- `generated.by: "claude/fable-5-1"` or `"human:<netid>"` means a
  hand-written, **frozen** page (the landing page, everything under
  *Start here* and *About*, the instructor materials page, the two
  interactive Module 1 pages, and the update log). Edit it directly.

## The frontmatter contract

Every content page starts with YAML frontmatter. OKF requires `type`; the
rest make the page trustworthy and discoverable. A copy-paste template lives
in `templates/page.md` in the repository.

```yaml
---
title: "Module 1 Activities"
description: "One sentence used by search, cards, llms.txt, and agents."
type: Activity                 # closed set, lint-warned: Overview | Lesson | Reading Guide | Reading | Activity |
                               # Worksheet | Lab | Assessment | Resource List | Tutorial | Guide | Course Design | Policy | Reference
tags: [module-1, student-facing, activities, ollama, openwork, workflow-audit]   # scope tag + audience tag + topics
module: 1                      # custom keys are tolerated by OKF consumers
time_estimate: "8 hours"
status: stable                 # draft | stable | deprecated (default stable)
stale_after: "2027-07-22T00:00:00Z"   # required when a tool tag (langchain, langgraph, crewai, langsmith, ollama, openwork, n8n, colab…) is present: last_modified + 12 months
generated:
  by: "process:scripts/migrate_wiki.py"     # hand-written pages: "claude/fable-5-1" or "human:<netid>"; notebook pages: "process:nbconvert"
  at: "2026-09-08T00:00:00Z"                # constant per migration run, never now() (reproducible diffs)
sources:
  - id: wiki-v2
    resource: "<URL of the wiki page, e.g. .../AI-Automation-and-Agents-v2/wiki/Module-1:-Activities>"
    title: "AI Automation and Agents v2 wiki: Module-1:-Activities"
    author: "Michelle Yung; Carlos Lizárraga-Celaya"   # real names from git log --follow
    last_modified: "2026-07-22T16:42:32-07:00"        # git log -1 --format=%aI
authorship: { created: "2026-04-22", updated: "2026-07-21", contributors: ["C. Lizárraga", "M. Yung"] }  # from the wiki footer
wiki_page: "Module-1:-Activities"                       # exact wiki stem; drives the crosswalk
superseded_by: "../../modules/module-1/activities.md"   # deprecated pages only; lint verifies it resolves
---
```

Key by key:

- **`type`** is the closed set above. It says what kind of page this is
  (*Lesson* teaches, *Reading Guide* structures a reading, *Assessment*
  tests, *Course Design* documents the design, *Policy* states a rule). The
  linter warns on anything else.
- **`tags`** always start with a *scope* tag (`course` or `module-N`) and an
  *audience* tag (`student-facing` or `instructor-facing`), then topics.
  Tool names are tags too - and they trigger the next rule.
- **`stale_after`** is required on any page tagged with a tool or framework,
  set to twelve months after the source's last change. A monthly CI run
  surfaces pages past that date so someone re-checks versions, pricing and
  screenshots. Update the date when you re-check; do not just delete it.
- **`status`** is `stable` by default. `draft` marks a page with a known
  content problem (it gets a *Draft* banner); `deprecated` marks history.
- **`superseded_by`** is required on every `deprecated` page and must be a
  relative path that resolves. Deprecated pages live under `archive/` (or
  `course-design/` for historical design documents), carry a *Superseded*
  banner, and are never in the navigation.
- **`generated`** and **`sources`** are provenance: who or what produced the
  current text and where it came from, with the upstream `last_modified`
  taken from git.
- **Never write `verified`.** Only an instructor adds
  `verified: { by: "human:<netid>", at: … }` after reviewing a page; the
  linter rejects anything else. How and when is described in
  [Instructor materials](../course-design/instructor-materials.md).

Section `index.md` files are OKF directory listings and carry **no
frontmatter**; the pipeline generates them, so do not hand-edit them. The
root `docs/index.md` is the only index with frontmatter. `docs/log.md` is the
dated change log: add a `## YYYY-MM-DD` entry (newest first) with a bullet
prefixed **Initialization**, **Migration**, **Creation**, **Update**,
**Deprecation** or **Removal** whenever you make a meaningful change.

## How to read a red X

CI runs three checks on every pull request. Open the *Files changed* tab; the
failures are annotated on the exact line.

| Check | What it enforces | Typical message and fix |
| :-- | :-- | :-- |
| `scripts/okf_validate.py docs` | OKF conformance: parseable frontmatter, a non-empty `type`, `status` in the allowed set, ISO 8601 `stale_after`, no frontmatter on section indexes, ISO date headings in `log.md` | `ERROR modules/module-2/x.md: frontmatter missing non-empty type` - add the key. `unparseable YAML frontmatter` - usually an unquoted colon in a title or description; quote the string. |
| `scripts/site_lint.py docs zensical.toml` | Course rules: one H1, `title` and `description` present, every relative link and image resolves, external links carry `{target=_blank}`, no wiki-era constructs (`[!NOTE]` alerts, `<p><img`, one-column callout tables, wiki or `blob/main/images` URLs), answer keys only inside `???` collapsibles, `stale_after` on tool-tagged pages, deprecated pages have a resolving `superseded_by`, every nav path exists, every page is listed in its section index, `verified.by` starts with `human:` | Printed as `::error file=docs/…,line=N::message`, which GitHub shows inline. Fix the line it names; if it flags a generated page, fix the source (wiki or `PATCHES`) instead. |
| `scripts/gen_llms_txt.py` + `git diff --exit-code docs/llms*.txt` | The machine-readable indexes must match the pages | "llms.txt drift": you changed a title, description or page set without regenerating. Run `python scripts/gen_llms_txt.py` and commit `docs/llms.txt` and `docs/llms-full.txt`. |

The *build* job then runs `zensical build --clean --strict`; a broken
Markdown link or a missing nav file fails it with the file name in the log.

## Building locally

The site needs Python 3.12 (the system Python on macOS is too old). The
repository uses [uv](https://docs.astral.sh/uv/){target=_blank} to create the
environment; a `uv`-created venv has no `pip`, so install with `uv pip`.

```bash
git clone https://github.com/tyson-swetnam/AI-Automation-and-Agents.git
cd AI-Automation-and-Agents
uv venv --python 3.12 .venv
uv pip install -r requirements-dev.txt     # zensical, pyyaml + nbconvert, markdownify, bs4, pillow
source .venv/bin/activate

zensical serve                             # live preview at http://localhost:8000
python scripts/okf_validate.py docs        # OKF conformance
python scripts/site_lint.py docs zensical.toml
python scripts/gen_llms_txt.py             # regenerate docs/llms.txt and docs/llms-full.txt
zensical build --clean --strict            # what CI runs; output in site/
python scripts/postbuild_agent_surface.py site && python scripts/check_site.py site
```

If you prefer plain `pip`, create the venv with `uv venv --seed` (or
`python3.12 -m venv .venv`) and run `.venv/bin/pip install -r
requirements-dev.txt`. `requirements.txt` alone is enough to build; the
`-dev` file adds what the migration scripts need.

## The pipeline scripts

- **`scripts/migrate_wiki.py`** - the reproducible wiki-to-`docs/` pipeline.
  It reads a clone of the course wiki at a **pinned commit** (`WIKI_REF`) and
  the course repository's images and notebooks (`ASSETS_REF`), and owns the
  page mapping (`PAGES`), exact-literal fixes (`PATCHES`, an unmatched patch
  is an error), image alt text (`ALT_TEXT`), the callout-table and anchor
  maps, and the list of **frozen** pages it must never overwrite. It also
  generates every section `index.md`, the wiki crosswalk and (with
  `--notebooks`) the lab pages. Run it with `--check` to diff against `docs/`
  without writing, `--only <page>` for one page. If the wiki gains a page,
  the script fails until you add it to `PAGES` or `DROPPED`. To adopt new
  wiki edits, move `WIKI_REF` forward, run the script, review the diff.
- **`scripts/render_notebooks.py`** - converts each learner `.ipynb` under
  `docs/materials/` to a lab page with the *Open in Colab* / download / view
  buttons and the API-key warning. Instructor solutions are never rendered.
- **`scripts/optimize_images.py`** - copies exactly the referenced images
  from `images/` (full-resolution originals) into `docs/assets/images/`,
  downscaled to at most 1600 px wide, keeping byte-exact file names.
  `--report` lists unreferenced originals.
- **`scripts/okf_validate.py`**, **`scripts/site_lint.py`** - the two
  validators described above.
- **`scripts/gen_llms_txt.py`** - builds `docs/llms.txt` (a linked outline per
  [llmstxt.org](https://llmstxt.org){target=_blank}) and `docs/llms-full.txt`
  (the whole corpus with frontmatter).
- **`scripts/postbuild_agent_surface.py`** and **`scripts/check_site.py`** -
  run after `zensical build`: add the Markdown mirror, `okf:*` meta tags and
  `robots.txt` to `site/`, then assert the build is complete.
- **`scripts/okf_links.py`** - the one rule for publishing Markdown to
  agents: a relative link becomes an absolute URL pointing at the linked
  page's Markdown twin (page URL + `index.md`). Used by
  `postbuild_agent_surface.py` when it mirrors a page and by
  `gen_llms_txt.py` when it builds `llms-full.txt`; the sources under `docs/`
  keep their relative links.
- **`scripts/check_consistency.py`** - checks that the lab notebooks, the
  activities pages, the module overviews and *Labs, Colab, and API keys*
  agree on submission filenames, time budgets, learning-objective labels,
  provider defaults and what each lab contains, and that every quiz
  question has feedback for every option. Run it after changing any of
  those; it is not part of CI.

## Style notes

- **One `# ` H1 per page**, matching the frontmatter `title`. Headings carry
  no letter or roman-numeral prefixes and no time estimates; put an italic
  *Estimated time: ~N min* line under the heading instead.
- **Admonitions, not one-column tables.** The wiki's `| HINT |` and
  `| WHAT TO SUBMIT |` boxes become `!!! tip "Hint"` and
  `!!! info "What to submit"`; use `!!! note`, `!!! warning`, `!!! example`
  and `??? question` the same way.
- **Answer keys go in `??? success "Show answer and feedback"`** collapsibles
  (or `??? note` for key tables), never in plain text. The linter fails a
  key line outside a `???` block.
- **Diagrams** are written as Mermaid inside a `mermaid` fence, not committed as
  pictures. The source stays readable in the diff, the figure cannot quietly go
  stale the way a binary can, and anyone can edit it without image tooling.
- **Tables** are written as Markdown tables. A table shipped as a screenshot is
  invisible to search, to screen readers and to `llms.txt`, and it cannot reflow
  on a phone.
- **Images** are for photographs and screenshots of real interfaces. They live in
  `docs/assets/images/` and are referenced relatively with alt text and an
  `attr_list` width — `![alt text](<relative path>){ width="900" }`. Add the
  original to `images/` and let `optimize_images.py` produce the served copy;
  never link to a GitHub `blob` URL.
- **Downloadable materials** (notebooks, PDFs, HTML activities, the glossary
  `.docx`) live in `docs/materials/moduleN/` and are linked relatively.
  Anything only instructors should have goes in `instructor/`, outside
  `docs/`. It is never rendered on the site, and only the instructor
  materials page links to it, by its GitHub URL.
- **Links**: internal links are relative (`../modules/module-2/overview.md`)
  and plain; external links get `{target=_blank}`. Raw HTML `src`/`href`
  attributes are not rewritten by the build, so compute them from the
  rendered directory URL (`../../../materials/…` from a page two levels
  deep).
- **Code** goes in fenced blocks with a language (`python`, `bash`, `text`).
- Keep the wiki's voice: short paragraphs, direct instructions, real
  examples.

## Pull requests

The pull request template lists the six things reviewers check: frontmatter
with a `type`, one H1, relative internal links and `{target=_blank}` external
ones, both validators run, `gen_llms_txt.py` run, and a `docs/log.md` entry.
Keep pull requests to one topic so the log entry can describe them in a line.
