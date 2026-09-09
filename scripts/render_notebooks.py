#!/usr/bin/env python3
"""Render the learner notebooks under docs/materials/ into static lab pages.

Each learner notebook is converted with `jupyter nbconvert --to markdown`
(outputs cleared) and wrapped as an OKF v0.2 page at
docs/modules/module-N/lab-notebook.md with:

  * a single H1 "Module N Lab: <notebook title>" (every heading from the
    notebook is demoted one level; the notebook's own H1 becomes the title);
  * an Open-in-Colab badge plus Download / View-on-GitHub buttons, all built
    from the REPO_SLUG and BRANCH constants so a fork change is one edit;
  * an "API keys" warning and a "Read-only rendering" note;
  * frontmatter (type Lab, module tags, framework tags detected from the
    notebook text, time estimate, stale_after = GENERATED_AT + STALE_MONTHS,
    provenance pointing at the .ipynb blob in the repository).

Output is deterministic: no timestamps other than the constants below and the
notebook's last git commit date, so reruns produce byte-identical pages.
Instructor-solution notebooks live under instructor/ and are never rendered.

Usage:
  python scripts/render_notebooks.py            # write the lab pages
  python scripts/render_notebooks.py --check    # exit 1 if any page would change
  python scripts/render_notebooks.py --only 3   # one module

The migration script imports `lab_pages()` / `lab_page_for()` from here.
Requires nbconvert (see requirements-dev.txt).
"""

from __future__ import annotations

import argparse
import calendar
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
# Clone of the v2 course repo (UA-AI2S/AI-Automation-and-Agents-v2) used only
# for each notebook's last commit date. Override with $COURSE_ASSETS_REPO or
# --assets-repo; when absent, `last_modified` is simply omitted.
ASSETS_REPO = Path(os.environ.get("COURSE_ASSETS_REPO", ROOT / ".cache" / "repo-v2"))

REPO_SLUG = "tyson-swetnam/AI-Automation-and-Agents"
BRANCH = "main"
GENERATED_AT = "2026-09-08T00:00:00Z"
GENERATED_BY = "process:nbconvert"
STALE_MONTHS = 12
SOURCE_AUTHOR = "team:ua-ai2s"

# Tool tags that trigger `stale_after` (see the frontmatter contract), in the
# order they are emitted when detected in the notebook text.
FRAMEWORKS = ("langchain", "langgraph", "crewai", "langsmith", "ollama", "chroma")

# docs-relative notebook path -> (docs-relative page path, module number)
NOTEBOOKS: dict[str, tuple[str, int]] = {
    "docs/materials/module2/Module-2-Guided-Lab-Notebook.ipynb": ("modules/module-2/lab-notebook.md", 2),
    "docs/materials/module3/Module-3-Lab.ipynb": ("modules/module-3/lab-notebook.md", 3),
    "docs/materials/module4/Module4_Learner_Starter.ipynb": ("modules/module-4/lab-notebook.md", 4),
    "docs/materials/module5/Module5_Learner_Starter.ipynb": ("modules/module-5/lab-notebook.md", 5),
}


# --------------------------------------------------------------------------- #
# shared helpers (imported by scripts/migrate_wiki.py)
# --------------------------------------------------------------------------- #

def lab_pages() -> list[str]:
    """Docs-relative paths of the rendered lab pages, in module order."""
    return [page for page, _ in sorted(NOTEBOOKS.values(), key=lambda t: t[1])]


def lab_page_for(module: int) -> str | None:
    """Docs-relative lab page for a module (None when the module has no notebook)."""
    for page, n in NOTEBOOKS.values():
        if n == module:
            return page
    return None


def notebook_for_page(page: str) -> str | None:
    """Repo-relative .ipynb path that produces a given docs-relative lab page."""
    for nb, (p, _) in NOTEBOOKS.items():
        if p == page:
            return nb
    return None


# --------------------------------------------------------------------------- #
# small utilities
# --------------------------------------------------------------------------- #

def yq(s: str) -> str:
    """YAML-safe double-quoted scalar."""
    return json.dumps(s, ensure_ascii=False)


def add_months(iso_utc: str, months: int) -> str:
    """'2026-09-08T00:00:00Z' + 12 months -> '2027-09-08T00:00:00Z' (day clamped)."""
    dt = datetime.strptime(iso_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    total = dt.year * 12 + (dt.month - 1) + months
    year, month = divmod(total, 12)
    month += 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day).strftime("%Y-%m-%dT%H:%M:%SZ")


def sh(cmd: list[str], cwd: Path | None = None) -> str:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return r.stdout.strip() if r.returncode == 0 else ""


def last_modified(nb_rel: str) -> str | None:
    """Author date of the notebook's last commit in the v2 course repo, if cloned."""
    if not (ASSETS_REPO / ".git").exists():
        return None
    upstream_rel = nb_rel.split("/", 1)[1] if nb_rel.startswith("docs/") else nb_rel
    return sh(["git", "log", "-1", "--format=%aI", "--", upstream_rel], cwd=ASSETS_REPO) or None


def rel_href(from_page: str, to_docs_path: str) -> str:
    """Relative link from a docs page to another docs path (POSIX separators)."""
    return Path(os.path.relpath(to_docs_path, start=Path(from_page).parent)).as_posix()


# --------------------------------------------------------------------------- #
# nbconvert + Markdown massaging
# --------------------------------------------------------------------------- #

FENCE_RE = re.compile(r"^ {0,3}(?P<ticks>`{3,})(?P<info>.*)$")


def nbconvert_markdown(src: Path) -> str:
    """Run nbconvert (outputs cleared) and return the Markdown text."""
    with tempfile.TemporaryDirectory(prefix="nbmd-") as tmp:
        cmd = [sys.executable, "-m", "nbconvert", "--to", "markdown",
               "--ClearOutputPreprocessor.enabled=True", "--log-level=ERROR",
               f"--output-dir={tmp}", "--output=notebook", str(src)]
        subprocess.run(cmd, check=True)
        md = (Path(tmp) / "notebook.md").read_text(encoding="utf-8")
        extracted = Path(tmp) / "notebook_files"
        if extracted.exists() and any(extracted.iterdir()):
            raise RuntimeError(f"{src.name}: nbconvert extracted output files although "
                               "outputs were cleared; refusing to render")
    return md


def walk_lines(md: str):
    """Yield (line, in_fence, is_opening_fence) with a CommonMark-ish fence tracker."""
    open_ticks = 0
    for line in md.splitlines():
        m = FENCE_RE.match(line)
        if open_ticks:
            if m and len(m.group("ticks")) >= open_ticks and not m.group("info").strip():
                open_ticks = 0
                yield line, True, False
            else:
                yield line, True, False
        elif m:
            open_ticks = len(m.group("ticks"))
            yield line, False, True
        else:
            yield line, False, False


def first_h1(md: str) -> str | None:
    for line, in_fence, _ in walk_lines(md):
        if not in_fence and line.startswith("# "):
            return line[2:].strip()
    return None


def transform_body(md: str) -> str:
    """Drop the notebook's first H1, demote remaining headings one level, force
    bare code fences to ```python, and collapse blank-line runs outside fences."""
    out: list[str] = []
    dropped_title = False
    blank_run = 0
    for line, in_fence, is_open in walk_lines(md):
        if is_open:
            m = FENCE_RE.match(line)
            if not m.group("info").strip():
                line = line.rstrip() + "python"
            blank_run = 0
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if not line.strip():
            blank_run += 1
            if blank_run > 1:
                continue
            out.append("")
            continue
        blank_run = 0
        if line.startswith("# ") and not dropped_title:
            dropped_title = True
            continue
        m = re.match(r"^(#{1,6})(?=\s)", line)
        if m:
            level = min(len(m.group(1)) + 1, 6)
            line = "#" * level + line[len(m.group(1)):]
        out.append(line)
    return "\n".join(out).strip("\n") + "\n"


def page_title(module: int, heading: str) -> str:
    """'Module 4 Lab (Learner Starter) — Three-Role Pipeline …' -> 'Module 4 Lab: Three-Role Pipeline …'."""
    t = re.sub(r"\(\s*Learner\s+Starter\s*\)", "", heading, flags=re.I)
    t = re.sub(rf"^\s*Module\s+{module}\s+(?:Guided\s+)?Lab\b", "", t, flags=re.I)
    t = re.sub(r"\s{2,}", " ", t).strip(" \t:\u2014\u2013-")
    return f"Module {module} Lab: {t}" if t else f"Module {module} Lab"


def time_estimate(md: str) -> str | None:
    """First 'Estimated time:'/'Time:' value, e.g. '~2 hours', '100–130 minutes'."""
    for line, in_fence, _ in walk_lines(md):
        if in_fence:
            continue
        plain = re.sub(r"[*_`]+", "", line).strip()
        m = re.match(r"^(?:Estimated\s+time|Time)\s*:\s*(.+)$", plain, flags=re.I)
        if m:
            value = re.split(r"\s+[|\u00b7\u2014]\s+|\s{2,}", m.group(1), maxsplit=1)[0]
            value = value.strip(" .;,")
            if value:
                return value
    return None


def detect_frameworks(nb: dict) -> list[str]:
    text = "\n".join("".join(c.get("source", [])) for c in nb.get("cells", [])).lower()
    return [f for f in FRAMEWORKS if f in text]


# --------------------------------------------------------------------------- #
# page assembly
# --------------------------------------------------------------------------- #

def frontmatter(title: str, description: str, module: int, tags: list[str],
                estimate: str | None, nb_rel: str, blob_url: str) -> str:
    lines = ["---",
             f"title: {yq(title)}",
             f"description: {yq(description)}",
             "type: Lab",
             "tags:"]
    lines += [f"  - {t}" for t in tags]
    lines.append(f"module: {module}")
    if estimate:
        lines.append(f"time_estimate: {yq(estimate)}")
    lines += ["status: stable",
              f"stale_after: {yq(add_months(GENERATED_AT, STALE_MONTHS))}",
              "generated:",
              f"  by: {yq(GENERATED_BY)}",
              f"  at: {yq(GENERATED_AT)}",
              "sources:",
              "  - id: notebook",
              f"    resource: {yq(blob_url)}",
              f"    title: {yq(Path(nb_rel).name)}",
              f"    author: {yq(SOURCE_AUTHOR)}"]
    lm = last_modified(nb_rel)
    if lm:
        lines.append(f"    last_modified: {yq(lm)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def render(nb_rel: str, page_rel: str, module: int) -> str:
    src = ROOT / nb_rel
    if not src.is_file():
        raise FileNotFoundError(f"notebook not found: {src}")
    nb = json.loads(src.read_text(encoding="utf-8"))
    md = nbconvert_markdown(src)

    heading = first_h1(md)
    if not heading:
        raise ValueError(f"{nb_rel}: no '# ' heading found to use as the notebook title")
    title = page_title(module, heading)
    subtitle = title.split(": ", 1)[1] if ": " in title else heading
    description = (f"Read-only rendering of the Module {module} lab notebook, {subtitle}, "
                   "with links to open it in Google Colab or download the .ipynb file.")

    frameworks = detect_frameworks(nb)
    tags = [f"module-{module}", "student-facing", "lab", "colab", *frameworks]
    estimate = time_estimate(md)

    nb_name = Path(nb_rel).name
    docs_path_of_nb = nb_rel  # e.g. docs/materials/module2/X.ipynb
    blob_url = f"https://github.com/{REPO_SLUG}/blob/{BRANCH}/{docs_path_of_nb}"
    colab_url = f"https://colab.research.google.com/github/{REPO_SLUG}/blob/{BRANCH}/{docs_path_of_nb}"
    nb_docs_rel = nb_rel.split("/", 1)[1]                 # materials/module2/X.ipynb
    nb_href = rel_href(page_rel, nb_docs_rel)             # ../../materials/module2/X.ipynb
    badge_href = rel_href(page_rel, "assets/colab-badge.svg")
    keys_href = rel_href(page_rel, "start-here/labs-and-notebooks.md")

    body = transform_body(md)

    parts = [
        frontmatter(title, description, module, tags, estimate, nb_rel, blob_url),
        f"# {title}\n",
        f"[![Open in Colab]({badge_href})]({colab_url}){{ target=_blank }}\n",
        f"[:material-download: Download the notebook (.ipynb)]({nb_href}){{ .md-button }}\n"
        f"[:fontawesome-brands-github: View on GitHub]({blob_url}){{ .md-button target=_blank }}\n",
        '!!! warning "API keys"\n'
        "\n"
        "    Keep API keys out of the notebook. In Colab store them as **Secrets** (the key\n"
        "    icon in the left sidebar) or enter them through the `getpass` prompt the setup\n"
        "    cell provides; never paste a key into a code cell, and clear outputs before you\n"
        f"    submit. See [Labs, Colab, and API keys]({keys_href}) for the full checklist.\n",
        '!!! note "Read-only rendering"\n'
        "\n"
        "    This page is a static rendering of the notebook with all outputs cleared. To\n"
        "    run the cells, open it in Google Colab with the badge above or download the\n"
        "    `.ipynb` and run it in Jupyter.\n",
        body,
        f'<p class="course-provenance" markdown>Rendered by nbconvert from the notebook '
        f"[{nb_name}]({nb_href}) (`{docs_path_of_nb}` in the "
        f"[course repository]({blob_url}){{target=_blank}}); outputs cleared. "
        f"Spotted a problem? Fix the notebook, not this page.</p>\n",
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main() -> int:
    global ASSETS_REPO
    ap = argparse.ArgumentParser(description="Render learner notebooks into lab pages.")
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit 1 if any page differs from what would be rendered")
    ap.add_argument("--only", type=int, metavar="N", help="render only module N")
    ap.add_argument("--assets-repo", type=Path, metavar="DIR",
                    help="clone of the v2 course repo for notebook commit dates "
                         f"(default: $COURSE_ASSETS_REPO or {ASSETS_REPO})")
    args = ap.parse_args()
    if args.assets_repo is not None:
        ASSETS_REPO = args.assets_repo.resolve()
    if not (ASSETS_REPO / ".git").exists():
        print(f"note: {ASSETS_REPO} is not a git clone; sources[].last_modified will be omitted",
              file=sys.stderr)

    drift = 0
    written = 0
    for nb_rel, (page_rel, module) in sorted(NOTEBOOKS.items(), key=lambda kv: kv[1][1]):
        if args.only is not None and module != args.only:
            continue
        content = render(nb_rel, page_rel, module)
        dest = DOCS / page_rel
        current = dest.read_text(encoding="utf-8") if dest.is_file() else None
        if current == content:
            print(f"  unchanged {page_rel}")
            continue
        if args.check:
            print(f"  DRIFT     {page_rel}" + ("" if current is not None else " (missing)"))
            drift += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        written += 1
        print(f"  wrote     {page_rel}")

    if args.check:
        print(f"render_notebooks: {drift} page(s) out of date")
        return 1 if drift else 0
    print(f"render_notebooks: {written} page(s) written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
