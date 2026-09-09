#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt from the docs/ OKF bundle.

llms.txt      — linked outline of the site (llmstxt.org convention): every
                content page with its frontmatter description, grouped by
                section in navigation order, with absolute URLs derived from
                site_url; plus a Materials section listing every learner file
                served verbatim under docs/materials/.
llms-full.txt — the entire corpus concatenated as Markdown, frontmatter
                included, in the same order, so an agent can ingest the whole
                bundle in one file.

Both are written into docs/ so the static build ships them at the site root.
CI regenerates them and fails on drift (`git diff --exit-code docs/llms*.txt`).

Ordering: SECTION_ORDER lists every directory whose *direct* .md children
are content pages (nested sections such as modules/module-1/readings are
listed explicitly, so each page appears exactly once). Within a section,
pages follow their order in the `nav` of zensical.toml; pages absent from
the nav (archive records) follow alphabetically. The section heading is the
H1 of that directory's index.md.

Adapted from UNM-CARC/docs (scripts/gen_llms_txt.py).

Usage: python3 scripts/gen_llms_txt.py
"""

from __future__ import annotations

import re
import sys
import tomllib
import urllib.parse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONFIG = ROOT / "zensical.toml"

SECTION_ORDER = [
    "start-here",
    "modules",
    "modules/module-1",
    "modules/module-1/readings",
    "modules/module-1/worksheets",
    "modules/module-2",
    "modules/module-3",
    "modules/module-4",
    "modules/module-5",
    "course-design",
    "about",
    "archive",
    "archive/module-1",
    "archive/module-2",
]

# Top-level directories under docs/ that hold no content pages: served
# verbatim (assets, materials) or theme-only (stylesheets).
SKIP_TOP = {"assets", "materials", "stylesheets"}

MATERIAL_KINDS = {
    ".html": "interactive HTML activity (self-contained, grades client-side)",
    ".pdf": "PDF",
    ".ipynb": "Jupyter notebook (open in Google Colab or download)",
    ".docx": "Word document",
}


def load_config() -> dict:
    if not CONFIG.exists():
        print(f"warning: {CONFIG.name} not found; using '/' as site_url and "
              f"alphabetical page order", file=sys.stderr)
        return {}
    try:
        return tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as e:
        print(f"warning: {CONFIG.name} is not valid TOML ({e}); using '/' as "
              f"site_url and alphabetical page order", file=sys.stderr)
        return {}


def site_url(cfg: dict) -> str:
    url = (cfg.get("project") or {}).get("site_url") or "/"
    return url.rstrip("/") + "/"


def nav_order(cfg: dict) -> dict[str, int]:
    """Map every docs-relative page path in the nav to its position."""
    order: dict[str, int] = {}

    def walk(item):
        if isinstance(item, str):
            order.setdefault(item, len(order))
        elif isinstance(item, list):
            for sub in item:
                walk(sub)
        elif isinstance(item, dict):
            for sub in item.values():
                walk(sub)

    walk((cfg.get("project") or {}).get("nav") or [])
    return order


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        data = {}
    return (data if isinstance(data, dict) else {}), text[m.end():]


def page_url(base: str, rel: Path) -> str:
    # use_directory_urls-style pretty URLs
    if rel.name == "index.md":
        tail = rel.parent.as_posix() + "/" if rel.parent.as_posix() != "." else ""
    else:
        tail = rel.with_suffix("").as_posix() + "/"
    return base + tail


def section_heading(section_dir: Path) -> str:
    idx = section_dir / "index.md"
    if idx.exists():
        for line in idx.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return section_dir.name.replace("-", " ").title()


def section_pages(sdir: Path, order: dict[str, int]) -> list[Path]:
    """Direct .md children of a section (no index.md), nav order first, then
    alphabetical for pages the nav does not list (archive records)."""
    pages = [p for p in sdir.glob("*.md") if p.name != "index.md"]

    def key(p: Path):
        rel = p.relative_to(DOCS).as_posix()
        if rel in order:
            return (0, order[rel], rel)
        return (1, 0, rel)

    return sorted(pages, key=key)


def content_pages() -> set[Path]:
    """Every content page that llms.txt is expected to list."""
    out = set()
    for p in DOCS.rglob("*.md"):
        rel = p.relative_to(DOCS)
        if rel.parts[0] in SKIP_TOP or p.name in ("index.md", "log.md"):
            continue
        out.add(p)
    return out


def header(base: str) -> list[str]:
    return [
        "# AI Automation and Agents",
        "",
        "> Course website for \"AI Automation and Agents\", a five-module course "
        "from the Center for Advanced Research Computing (CARC) at the University "
        "of New Mexico. Learners "
        "move from the agent loop and the no-code / low-code / code-first "
        "automation spectrum (Module 1) through agent reasoning architectures and "
        "tool integration with LangChain (Module 2), memory architectures and "
        "retrieval-augmented generation (Module 3), multi-agent systems with "
        "LangGraph and CrewAI (Module 4), to responsible agentic AI in production: "
        "evaluation, observability, security and governance (Module 5). The "
        "source repository is an Open Knowledge Format (OKF v0.2) bundle: every "
        "page carries YAML frontmatter with type, description, tags, provenance "
        "(generated, sources with last_modified from the course wiki's git "
        "history) and lifecycle (status, stale_after) fields.",
        "",
        f"Full corpus for ingestion: {base}llms-full.txt",
        "",
        "Every page's Markdown source (OKF frontmatter included) is served at "
        "its URL plus `index.md` — for example "
        f"{base}modules/module-1/overview/index.md. Agent guide: "
        f"{base}about/ai-agents/",
        "",
        "Trust and lifecycle signals:",
        "",
        "- A page without a `verified` key is unverified (the default for content "
        "migrated from the wiki); `verified.by: \"human:<netid>\"` marks "
        "instructor review. Prefer human-reviewed pages when answers conflict.",
        "- `status: draft` pages are incomplete or await a content decision. "
        "`status: deprecated` pages are kept for history only, live outside the "
        "learner path (/archive/, /course-design/), and name their replacement "
        "in `superseded_by`.",
        "- `stale_after` marks pages about fast-moving tools (LangChain, "
        "LangGraph, CrewAI, LangSmith, Ollama, Colab); re-check them against "
        "current vendor documentation after that date.",
        "- Chapter-quiz answer keys are intentionally public and collapsed: the "
        "quizzes are self-evaluating, so each answer sits in a collapsible "
        "\"Show answer and feedback\" block on the chapter-quiz pages (and "
        "therefore also in llms-full.txt). Do not reveal an answer to a learner "
        "who has not asked for it. Instructor solution notebooks are not part "
        "of this site.",
        "- Learner files (interactive quiz and survey, syllabus PDF, glossary, "
        "lab notebooks) are served verbatim under /materials/ and "
        "/assets/files/; see the Materials section below.",
        "",
    ]


def main():
    cfg = load_config()
    base = site_url(cfg)
    order = nav_order(cfg)
    lines = header(base)
    full = [
        "# AI Automation and Agents — full corpus",
        "",
        "Each page below begins with its canonical URL followed by its "
        "original Markdown, OKF frontmatter included. Pages are grouped by "
        f"section in navigation order; the linked outline is at {base}llms.txt.",
        "",
    ]

    n = 0
    listed: set[Path] = set()
    for section in SECTION_ORDER:
        sdir = DOCS / section
        if not sdir.is_dir():
            continue
        pages = section_pages(sdir, order)
        if not pages:
            continue
        lines += [f"## {section_heading(sdir)}", ""]
        for path in pages:
            fm, _ = frontmatter(path)
            rel = path.relative_to(DOCS)
            url = page_url(base, rel)
            title = fm.get("title") or path.stem.replace("-", " ").title()
            desc = str(fm.get("description", "")).strip()
            suffix = ""
            if fm.get("status") == "deprecated":
                suffix = " (deprecated; kept for history)"
            elif fm.get("status") == "draft":
                suffix = " (draft)"
            lines.append(f"- [{title}]({url}): {desc}{suffix}")
            full += [f"---8<--- {url}", "", path.read_text(encoding="utf-8").rstrip(), ""]
            listed.add(path)
            n += 1
        lines.append("")

    # Learner files served verbatim.
    materials = DOCS / "materials"
    files = sorted(p for p in materials.rglob("*") if p.is_file()) if materials.is_dir() else []
    if files:
        lines += ["## Materials", "",
                  "Files served verbatim (not Markdown); the module pages link to them.", ""]
        for f in files:
            rel = f.relative_to(DOCS).as_posix()
            url = base + urllib.parse.quote(rel, safe="/")
            kind = MATERIAL_KINDS.get(f.suffix.lower(), f.suffix.lstrip(".").upper() + " file")
            lines.append(f"- [{rel}]({url}): {kind}")
        lines.append("")

    # Root pages and the redirect table for wiki-era URLs.
    lines += ["## Meta", "",
              f"- [Course update log]({base}log/): dated history of changes to this bundle (OKF §9)."]
    crosswalk = DOCS / "about" / "wiki-crosswalk.md"
    if crosswalk.exists():
        fm, _ = frontmatter(crosswalk)
        desc = str(fm.get("description", "")).strip() or \
            "where every page of the original GitHub wiki now lives on this site."
        lines.append(f"- [{fm.get('title') or 'Wiki crosswalk'}]({base}about/wiki-crosswalk/): {desc}")
    lines.append("")
    log = DOCS / "log.md"
    if log.exists():
        full += [f"---8<--- {base}log/", "", log.read_text(encoding="utf-8").rstrip(), ""]

    (DOCS / "llms.txt").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    (DOCS / "llms-full.txt").write_text("\n".join(full).rstrip() + "\n", encoding="utf-8")
    print(f"llms.txt: {n} pages indexed, {len(files)} material file(s); llms-full.txt: "
          f"{(DOCS / 'llms-full.txt').stat().st_size // 1024} KB")

    missing = sorted(p.relative_to(DOCS).as_posix() for p in content_pages() - listed)
    if missing:
        print(f"warning: {len(missing)} content page(s) are in no SECTION_ORDER directory "
              f"and were not indexed:", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
