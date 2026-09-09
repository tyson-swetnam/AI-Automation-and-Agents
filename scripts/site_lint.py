#!/usr/bin/env python3
"""Course-specific lint for the AI Automation and Agents docs/ bundle.

`scripts/okf_validate.py` checks Open Knowledge Format v0.2 conformance. This
script layers the course's own conventions (AGENTS.md, templates/page.md) on
top of it. "Content pages" are every `.md` under docs/ except `index.md` and
`log.md`; body and link rules apply to every `.md`. Fenced code is ignored.

Rules (E = error, fails the run; W = warning):

  Frontmatter (content pages)
    E  title and description present and non-empty
    W  description longer than 300 characters
    W  type outside TYPES
    W  tags not a non-empty list of lowercase kebab-case strings, not exactly
       one scope tag (course, module-1..module-5), or no audience tag
    E  status not in draft|stable|deprecated; module not in 1..5
    W  module key disagrees with the module-N scope tag or a modules/module-N/ path
    E  verified.by must start with "human:" and verified.at >= generated.at
  Body (all .md)
    E  not exactly one H1 (`# ` at column 0);  W  H1 text differs from title
    W  empty heading (nothing before the next heading of the same or higher level)
    E  GitHub alert syntax `> [!NOTE]` (use admonitions)
    E  `<p><img` heroes (use a Markdown image with `{ width="900" }`)
    E  one-column pipe table used as a callout (use an admonition)
    E  UA-AI2S wiki or blob/main/images URL; exempt: lines carrying
       class="course-provenance" and the pages in WIKI_URL_ALLOWED
    E  answer-key line (`> **Correct Answer`, `**Feedback:**`, `Answer: **X`)
       not indented 4+ spaces inside a `???` collapsible
  Links (Markdown links/images, reference definitions, raw HTML src=/href=)
    E  relative target does not resolve under docs/ (Markdown targets resolve
       against the source file; Zensical rewrites raw HTML the same way)
    E  #fragment matches neither a heading slug (Python-Markdown toc slugify,
       `_1` suffixes for duplicates) nor a pinned `{ #id }` on the target
    E  target under instructor/ or otherwise outside docs/
    E  raw HTML href/src pointing at a .md file (the build does not rewrite raw HTML)
    W  absolute (/-rooted) target
  Lifecycle
    W  tool tag (TOOL_TAGS) without stale_after
    E  status: deprecated without a resolvable superseded_by, outside archive/
       or course-design/, or an archive/ page listed in the zensical.toml nav
    E  nav path in zensical.toml does not exist
    W  content page not linked from its directory's index.md
  Materials and assets
    W  file under materials/, assets/images/, assets/files/ referenced from no .md
    E  HTML under materials/ with http(s):// in src=, href=, or CSS url()
  Consistency (W)
    site_url, repo_url, repo_name, edit_uri in zensical.toml and REPO_SLUG in
    scripts/render_notebooks.py describe the same repository and docs dir

Usage: python scripts/site_lint.py docs zensical.toml
Output: `ERROR <rel>: msg` / `WARN <rel>: msg`; under GITHUB_ACTIONS the same
findings are also emitted as ::error/::warning file annotations.
Exit code 1 on any error, 2 on usage problems. Requires Python 3.11+ and PyYAML.
"""

from __future__ import annotations

import datetime as dt
import html
import os
import re
import sys
import tomllib
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

import yaml

# --- Vocabulary ---------------------------------------------------------------

TYPES = {
    "Overview", "Lesson", "Reading Guide", "Reading", "Activity", "Worksheet",
    "Lab", "Assessment", "Resource List", "Tutorial", "Guide", "Course Design",
    "Policy", "Reference",
}
STATUSES = {"draft", "stable", "deprecated"}
SCOPE_TAGS = {"course", "module-1", "module-2", "module-3", "module-4", "module-5"}
AUDIENCE_TAGS = {"student-facing", "instructor-facing"}
TOOL_TAGS = {
    "langchain", "langgraph", "crewai", "langsmith", "langfuse", "ollama",
    "openwork", "claude-desktop", "n8n", "autogen", "colab", "chroma",
}
RESERVED = {"index.md", "log.md"}
DEPRECATED_DIRS = {"archive", "course-design"}
# Pages that legitimately list wiki URLs (the redirect table and the change log).
WIKI_URL_ALLOWED = {"about/wiki-crosswalk.md", "log.md"}
# Directories whose files must be referenced from at least one page.
REFERENCED_ROOTS = ("materials", "assets/images", "assets/files")
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript", "ftp", "ftps", "sftp"}
MAX_DESCRIPTION = 300
PROVENANCE_MARK = 'class="course-provenance"'

# --- Regexes ------------------------------------------------------------------

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^( *)(#{1,6})(?:\s+(.*?))?\s*$")
H1_RE = re.compile(r"^# ")
CLOSING_HASHES_RE = re.compile(r"(?:^|\s+)#+\s*$")
ATTR_BLOCK_RE = re.compile(r"\s*\{:?\s*([^{}]*)\}\s*$")
ATTR_ID_RE = re.compile(r"(?:^|\s)#([^\s}]+)")
HTML_ID_RE = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""")
ALERT_RE = re.compile(r"^\s*>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]")
P_IMG_RE = re.compile(r"<p>\s*<img", re.IGNORECASE)
WIKI_URL_RE = re.compile(r"github\.com/UA-AI2S/[^/\s)]+/(wiki|blob/main/images)")
ANSWER_KEY_RES = (
    re.compile(r"^\s*>\s*\*\*Correct Answer"),
    re.compile(r"^\s*\*\*Feedback:\*\*"),
    re.compile(r"^\s*Answer:\s*\*\*[A-D]"),
)
COLLAPSIBLE_RE = re.compile(r"^\s*\?\?\?\+?(?:\s|$)")
TABLE_DELIM_RE = re.compile(r"^:?-+:?$")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
MD_LINK_RE = re.compile(
    r"(!?)\[((?:[^\[\]]|\[[^\[\]]*\])*)\]"           # [text], one level of nesting
    r"\(\s*(<[^>]*>|(?:[^()\s]|\([^()\s]*\))*)"      # (target, balanced parens
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)"           # optional "title")
)
REF_DEF_RE = re.compile(
    r"""^ {0,3}\[(?!\^)[^\]]+\]:\s*(<[^>]*>|\S+)(?:\s+(?:"[^"]*"|'[^']*'|\([^)]*\)))?\s*$"""
)
HTML_ATTR_RE = re.compile(r"""\b(?:src|href)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
EXTERNAL_RESOURCE_RE = re.compile(
    r"""(?:\b(?:src|href)\s*=\s*["']?|url\(\s*["']?)\s*(https?://[^"'\s)>]+)""", re.IGNORECASE
)
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REPO_SLUG_RE = re.compile(r'REPO_SLUG\s*=\s*"([^"]+)"')
GITHUB_REPO_RE = re.compile(r"^https?://github\.com/([^/\s]+)/([^/\s]+?)(?:\.git)?/?$")
SCHEME_RE = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.-]*):")
IDCOUNT_RE = re.compile(r"^(.*)_([0-9]+)$")
MODULE_PATH_RE = re.compile(r"^modules/module-([1-5])/")


# --- Reporting ----------------------------------------------------------------

class Report:
    """Collects findings; prints them grouped at the end (and as GitHub annotations live)."""

    def __init__(self, docs: Path) -> None:
        self.docs = docs
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.annotate = bool(os.environ.get("GITHUB_ACTIONS"))

    def error(self, rel: str, msg: str, *, line: int | None = None, file: Path | None = None) -> None:
        self._add("error", rel, msg, line, file)

    def warn(self, rel: str, msg: str, *, line: int | None = None, file: Path | None = None) -> None:
        self._add("warning", rel, msg, line, file)

    def _add(self, level: str, rel: str, msg: str, line: int | None, file: Path | None) -> None:
        text = f"{rel}: {msg}" + (f" (line {line})" if line else "")
        (self.errors if level == "error" else self.warnings).append(text)
        if self.annotate:
            path = file if file is not None else self.docs / rel
            try:
                shown = os.path.relpath(path)
            except ValueError:
                shown = str(path)
            loc = f"file={shown}" + (f",line={line}" if line else "")
            escaped = msg.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print(f"::{level} {loc}::{rel}: {escaped}")

    def finish(self, n_pages: int) -> int:
        for w in self.warnings:
            print(f"WARN {w}")
        for e in self.errors:
            print(f"ERROR {e}")
        print(f"\nChecked {n_pages} markdown files: {len(self.errors)} error(s), "
              f"{len(self.warnings)} warning(s).")
        return 1 if self.errors else 0


# --- Markdown helpers ---------------------------------------------------------

@dataclass
class Heading:
    indent: int
    level: int
    text: str
    pinned: str | None


@dataclass
class Page:
    path: Path                      # absolute
    rel: str                        # posix path relative to docs/
    fm: dict | None                 # None when the file has no frontmatter block
    body: list[str]
    offset: int                     # file lines preceding the body
    heading_ids: set[str] = field(default_factory=set)
    link_targets: set[Path] = field(default_factory=set)

    @property
    def is_index(self) -> bool:
        return self.path.name == "index.md"

    @property
    def is_reserved(self) -> bool:
        return self.path.name in RESERVED


def split_frontmatter(text: str) -> tuple[dict | None, str, int]:
    """Return (frontmatter, body, lines_consumed). Raises ValueError on bad YAML."""
    if not text.startswith("---"):
        return None, text, 0
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return None, text, 0
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        raise ValueError(f"unparseable YAML frontmatter: {e}") from e
    return (data if isinstance(data, dict) else {}), text[m.end():], text[:m.end()].count("\n")


def iter_fenced_aware_lines(lines: list[str], offset: int = 0):
    """Yield (lineno, line, in_code) for every line; in_code covers fence
    delimiters and their contents. lineno is 1-based within the file."""
    fence_char: str | None = None
    fence_len = 0
    for i, line in enumerate(lines, start=offset + 1):
        m = FENCE_RE.match(line)
        if fence_char is None:
            if m:
                fence_char, fence_len = m.group(1)[0], len(m.group(1))
                yield i, line, True
            else:
                yield i, line, False
        else:
            stripped = line.strip()
            if stripped and set(stripped) == {fence_char} and len(stripped) >= fence_len:
                fence_char = None
            yield i, line, True


def heading_parts(line: str) -> Heading | None:
    m = HEADING_RE.match(line)
    if not m:
        return None
    indent, hashes, rest = len(m.group(1)), m.group(2), m.group(3) or ""
    text = CLOSING_HASHES_RE.sub("", rest)
    pinned = None
    am = ATTR_BLOCK_RE.search(text)
    if am:
        im = ATTR_ID_RE.search(am.group(1))
        pinned = im.group(1) if im else None
        text = text[:am.start()]
    return Heading(indent, len(hashes), text.strip(), pinned)


def strip_inline_markup(text: str) -> str:
    """Approximate the text content of a rendered heading (what toc slugifies)."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)            # images have no text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)          # inline links
    text = re.sub(r"\[([^\]]*)\]\[[^\]]*\]", r"\1", text)         # reference links
    text = re.sub(r"<[^>]+>", "", text)                            # raw HTML tags
    text = re.sub(r":[a-z0-9_+-]+:", "", text)                     # emoji/icon shortcodes render as SVG
    text = INLINE_CODE_RE.sub(r"\2", text)                         # code spans keep their text
    text = re.sub(r"(?<!\w)(\*{1,3}|_{1,3})(?=\S)(.+?)(?<=\S)\1(?!\w)", r"\2", text)
    return html.unescape(text).strip()


def slugify(value: str, separator: str = "-") -> str:
    """Python-Markdown's default toc slugify (what Zensical uses for heading ids)."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(rf"[{separator}\s]+", separator, value)


def unique(slug: str, used: set[str]) -> str:
    """Python-Markdown's toc.unique: append _1, _2, ... until unused."""
    while slug in used or not slug:
        m = IDCOUNT_RE.match(slug)
        slug = f"{m.group(1)}_{int(m.group(2)) + 1}" if m else f"{slug}_1"
    used.add(slug)
    return slug


def collect_heading_ids(body: list[str]) -> set[str]:
    """Ids the rendered page will carry: raw-HTML ids and pinned { #id } first
    (toc reserves them before assigning slugs), then slugified headings."""
    used: set[str] = set()
    headings: list[Heading] = []
    for _, line, in_code in iter_fenced_aware_lines(body):
        if in_code:
            continue
        used.update(HTML_ID_RE.findall(line))
        hp = heading_parts(line.expandtabs(4))
        if hp is None:
            continue
        headings.append(hp)
        if hp.pinned:
            used.add(hp.pinned)
    ids = set(used)
    for hp in headings:
        if not hp.pinned:
            ids.add(unique(slugify(strip_inline_markup(hp.text)), used))
    return ids


def pipe_cells(stripped: str) -> list[str] | None:
    """Cells of a pipe-table row, or None if the line is not a row."""
    if "|" not in stripped or not (stripped.startswith("|") or stripped.endswith("|")):
        return None
    s = stripped[1:] if stripped.startswith("|") else stripped
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def iter_markdown_targets(text: str):
    """Targets of inline links and images, including ones nested in link text."""
    for m in MD_LINK_RE.finditer(text):
        yield m.group(3)
        if "](" in m.group(2):
            yield from iter_markdown_targets(m.group(2))


def parse_datetime(value) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        parsed = value
    elif isinstance(value, dt.date):
        parsed = dt.datetime(value.year, value.month, value.day)
    elif isinstance(value, str):
        try:
            parsed = dt.datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def normalize_ws(text: str) -> str:
    return " ".join(text.split())


# --- Configuration ------------------------------------------------------------

def load_nav_paths(nav) -> list[str]:
    """Flatten a zensical.toml nav (strings, lists, and {label = ...} tables) in order."""
    paths: list[str] = []

    def walk(node) -> None:
        if isinstance(node, str):
            paths.append(node)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)

    walk(nav)
    return paths


def load_config(toml_path: Path, report: Report) -> tuple[dict, list[str]]:
    if not toml_path.is_file():
        report.error(toml_path.name, "not found; nav and consistency checks skipped", file=toml_path)
        return {}, []
    try:
        with toml_path.open("rb") as fh:
            data = tomllib.load(fh)
    except tomllib.TOMLDecodeError as e:
        report.error(toml_path.name, f"unparseable TOML: {e}", file=toml_path)
        return {}, []
    project = data.get("project", {})
    if not isinstance(project, dict):
        report.error(toml_path.name, "[project] table missing", file=toml_path)
        return {}, []
    return project, load_nav_paths(project.get("nav", []))


# --- Loading ------------------------------------------------------------------

def load_pages(docs: Path, report: Report) -> dict[Path, Page]:
    pages: dict[Path, Page] = {}
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(docs).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            report.error(rel, f"not valid UTF-8: {e}")
            continue
        if text.startswith("\ufeff"):
            report.warn(rel, "file starts with a UTF-8 byte-order mark")
            text = text[1:]
        try:
            fm, body, offset = split_frontmatter(text)
        except ValueError as e:
            report.error(rel, str(e))
            continue
        page = Page(path, rel, fm, body.splitlines(), offset)
        page.heading_ids = collect_heading_ids(page.body)
        pages[path] = page
    return pages


# --- Checks: frontmatter ------------------------------------------------------

def check_frontmatter(page: Page, nav_set: set[str], docs: Path, report: Report) -> None:
    fm = page.fm
    if fm is None:
        report.error(page.rel, "missing YAML frontmatter (title, description, type, tags, ...)")
        return

    title = fm.get("title")
    if not isinstance(title, str) or not title.strip():
        report.error(page.rel, "frontmatter needs a non-empty string `title`")

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        report.error(page.rel, "frontmatter needs a non-empty string `description`")
    elif len(desc) > MAX_DESCRIPTION:
        report.warn(page.rel, f"description is {len(desc)} characters (keep it to one sentence, "
                              f"<= {MAX_DESCRIPTION})")

    page_type = fm.get("type")
    if page_type not in TYPES:
        report.warn(page.rel, f"type {page_type!r} is not in the closed set {sorted(TYPES)}")

    tags = fm.get("tags")
    scope_tags: list[str] = []
    if not isinstance(tags, list) or not tags:
        report.warn(page.rel, "tags must be a non-empty list [scope, audience, topics...]")
    else:
        bad = [t for t in tags if not isinstance(t, str) or not KEBAB_RE.match(t)]
        if bad:
            report.warn(page.rel, f"tags must be lowercase kebab-case strings: {bad}")
        scope_tags = [t for t in tags if t in SCOPE_TAGS]
        if len(scope_tags) != 1:
            report.warn(page.rel, f"tags need exactly one scope tag from {sorted(SCOPE_TAGS)} "
                                  f"(found {scope_tags or 'none'})")
        if not any(t in AUDIENCE_TAGS for t in tags):
            report.warn(page.rel, f"tags need an audience tag from {sorted(AUDIENCE_TAGS)}")

    status = fm.get("status")
    if status is not None and status not in STATUSES:
        report.error(page.rel, f"status {status!r} not in {sorted(STATUSES)}")

    module = fm.get("module")
    module_n: int | None = None
    if module is not None:
        if isinstance(module, bool) or not str(module).strip().isdigit() or not 1 <= int(module) <= 5:
            report.error(page.rel, f"module {module!r} must be an integer 1..5")
        else:
            module_n = int(module)
    if scope_tags and scope_tags[0].startswith("module-"):
        tag_n = int(scope_tags[0].split("-")[1])
        if module_n != tag_n:
            report.warn(page.rel, f"module key {module!r} disagrees with scope tag {scope_tags[0]!r}")
    pm = MODULE_PATH_RE.match(page.rel)
    if pm and module_n != int(pm.group(1)):
        report.warn(page.rel, f"module key {module!r} disagrees with the modules/module-{pm.group(1)}/ path")

    generated = fm.get("generated")
    generated_at = None
    if isinstance(generated, dict) and generated.get("at") is not None:
        generated_at = parse_datetime(generated.get("at"))
        if generated_at is None:
            report.error(page.rel, f"generated.at {generated.get('at')!r} is not an ISO 8601 datetime")

    verified = fm.get("verified")
    if verified is not None:
        if not isinstance(verified, dict):
            report.error(page.rel, "verified must be a mapping { by: \"human:<netid>\", at: <ISO 8601> }")
        else:
            by = str(verified.get("by", ""))
            if not by.startswith("human:"):
                report.error(page.rel, f"verified.by {by!r} must start with \"human:\"")
            verified_at = parse_datetime(verified.get("at"))
            if verified_at is None:
                report.error(page.rel, f"verified.at {verified.get('at')!r} is not an ISO 8601 datetime")
            elif generated_at is not None and verified_at < generated_at:
                report.error(page.rel, f"verified.at {verified.get('at')} is earlier than generated.at "
                                       f"{generated.get('at')}; re-verify after regeneration")

    if isinstance(tags, list):
        tools = sorted(t for t in tags if isinstance(t, str) and t in TOOL_TAGS)
        if tools and not fm.get("stale_after"):
            report.warn(page.rel, f"tool tags {tools} require stale_after (last_modified + 12 months)")

    if status == "deprecated":
        superseded = fm.get("superseded_by")
        if not isinstance(superseded, str) or not superseded.strip():
            report.error(page.rel, "status: deprecated requires superseded_by (relative path to the replacement)")
        else:
            target = Path(os.path.normpath(page.path.parent / unquote(superseded.split("#", 1)[0])))
            if not target.is_file() or not target.is_relative_to(docs):
                report.error(page.rel, f"superseded_by {superseded!r} does not resolve under docs/")
        if page.rel.split("/", 1)[0] not in DEPRECATED_DIRS:
            report.error(page.rel, f"deprecated pages must live under {sorted(DEPRECATED_DIRS)}/")
        # archived pages stay out of the nav; deprecated course-design documents (historical
        # reviews) may be listed because they carry a "Historical document" admonition
        if page.rel in nav_set and page.rel.split("/", 1)[0] == "archive":
            report.error(page.rel, "deprecated archive page is listed in the zensical.toml nav")


# --- Checks: body -------------------------------------------------------------

def check_body(page: Page, report: Report) -> None:
    visible = list(iter_fenced_aware_lines(page.body, page.offset))
    h1s: list[tuple[int, str]] = []
    headings: list[tuple[int, int, Heading]] = []       # (index in visible, lineno, heading)
    collapsible_indent: int | None = None
    wiki_urls_allowed = page.rel in WIKI_URL_ALLOWED

    for i, (lineno, raw, in_code) in enumerate(visible):
        if in_code:
            continue
        line = raw.expandtabs(4)
        stripped = line.strip()
        prose = INLINE_CODE_RE.sub(" ", line)      # code spans may quote forbidden syntax

        hp = heading_parts(line)
        if hp is not None and hp.indent <= 3:
            headings.append((i, lineno, hp))
            if H1_RE.match(line):
                h1s.append((lineno, hp.text))

        if ALERT_RE.match(line):
            report.error(page.rel, "GitHub alert syntax `> [!NOTE]`; use an admonition (`!!! note`)", line=lineno)
        if P_IMG_RE.search(prose):
            report.error(page.rel, "`<p><img` hero; use a Markdown image with `{ width=\"900\" }`", line=lineno)
        if WIKI_URL_RE.search(prose) and PROVENANCE_MARK not in line and not wiki_urls_allowed:
            report.error(page.rel, "unconverted UA-AI2S wiki / blob-image URL; link the site page or "
                                   "the assets/images copy", line=lineno)

        cells = pipe_cells(stripped)
        if cells is not None and len(cells) == 1 and cells[0] and i + 1 < len(visible):
            nxt_line, nxt_in_code = visible[i + 1][1], visible[i + 1][2]
            nxt_cells = None if nxt_in_code else pipe_cells(nxt_line.strip())
            if nxt_cells is not None and len(nxt_cells) == 1 and TABLE_DELIM_RE.match(nxt_cells[0].replace(" ", "")):
                report.error(page.rel, f"one-column pipe table {stripped!r} used as a callout; "
                                       "convert it to an admonition", line=lineno)

        if stripped:
            indent = len(line) - len(line.lstrip(" "))
            if COLLAPSIBLE_RE.match(line):
                collapsible_indent = indent
            elif collapsible_indent is not None and indent <= collapsible_indent:
                collapsible_indent = None
            if any(r.match(line) for r in ANSWER_KEY_RES):
                inside = collapsible_indent is not None and indent >= collapsible_indent + 4
                if not inside:
                    report.error(page.rel, "answer key exposed outside a `???` collapsible: "
                                           f"{stripped[:60]!r}", line=lineno)

    if len(h1s) != 1:
        where = ", ".join(str(n) for n, _ in h1s) or "none"
        report.error(page.rel, f"expected exactly one H1 (`# `), found {len(h1s)} (lines: {where})")
    elif page.fm and isinstance(page.fm.get("title"), str):
        if normalize_ws(h1s[0][1]) != normalize_ws(page.fm["title"]):
            report.warn(page.rel, f"H1 {h1s[0][1]!r} differs from title {page.fm['title']!r}", line=h1s[0][0])

    for i, lineno, hp in headings:
        following = next(((ln, cd) for _, ln, cd in visible[i + 1:] if cd or ln.strip()), None)
        if following is None:
            report.warn(page.rel, f"empty heading {hp.text!r} (nothing follows it)", line=lineno)
            continue
        nxt_line, nxt_in_code = following
        nxt = None if nxt_in_code else heading_parts(nxt_line.expandtabs(4))
        if nxt is not None and nxt.indent <= 3 and nxt.level <= hp.level:
            report.warn(page.rel, f"empty heading {hp.text!r} (next heading follows with no content)", line=lineno)


# --- Checks: links ------------------------------------------------------------

def check_links(page: Page, pages: dict[Path, Page], docs: Path, report: Report) -> None:
    source_dir = page.path.parent
    # Zensical rewrites raw-HTML src=/href= paths the same way it rewrites Markdown links:
    # they are authored relative to the SOURCE file and re-emitted relative to the rendered
    # directory URL (verified: src="../../materials/x" in docs/modules/module-1/concept-quiz.md
    # ships as src="../../../materials/x" at /modules/module-1/concept-quiz/). A path that does
    # not resolve under docs/ is passed through untouched and will almost certainly 404.
    rendered_dir = source_dir
    for lineno, raw, in_code in iter_fenced_aware_lines(page.body, page.offset):
        if in_code:
            continue
        line = INLINE_CODE_RE.sub(" ", raw)
        for target in iter_markdown_targets(line):
            check_target(page, target, source_dir, "markdown", lineno, pages, docs, report)
        for m in HTML_ATTR_RE.finditer(line):
            check_target(page, m.group(1) or m.group(2) or "", rendered_dir, "html", lineno, pages, docs, report)
        m = REF_DEF_RE.match(line)
        if m:
            check_target(page, m.group(1), source_dir, "markdown", lineno, pages, docs, report)


def check_target(page: Page, raw: str, base_dir: Path, kind: str, lineno: int,
                 pages: dict[Path, Page], docs: Path, report: Report) -> None:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if not target or target.startswith("//"):
        return
    m = SCHEME_RE.match(target)
    if m and m.group(1).lower() in EXTERNAL_SCHEMES:
        return

    path_part, _, fragment = target.partition("#")
    path_part = unquote(path_part.split("?", 1)[0])
    if not path_part:
        if fragment and fragment not in page.heading_ids:
            report.error(page.rel, f"anchor #{fragment} matches no heading on this page", line=lineno)
        return

    if path_part.startswith("/"):
        report.warn(page.rel, f"absolute link {target!r}; use a path relative to this page", line=lineno)
        candidate = docs / path_part.lstrip("/")
    else:
        candidate = base_dir / path_part
    resolved = Path(os.path.normpath(candidate))

    if not resolved.is_relative_to(docs):
        if "instructor" in resolved.parts:
            report.error(page.rel, f"link {target!r} points into instructor/ (instructor materials are never "
                                   "learner-facing)", line=lineno)
        else:
            report.error(page.rel, f"link {target!r} escapes {docs.name}/", line=lineno)
        return
    rel_target = resolved.relative_to(docs).as_posix()
    if resolved.is_dir():
        report.error(page.rel, f"link {target!r} targets a directory; link to {rel_target}/index.md", line=lineno)
        return
    if not resolved.is_file():
        report.error(page.rel, f"link target {target!r} not found ({rel_target})", line=lineno)
        return

    page.link_targets.add(resolved)
    if kind == "html" and resolved.suffix == ".md":
        report.error(page.rel, f"raw HTML attribute targets {rel_target}; use a Markdown link so the "
                               "build rewrites it", line=lineno)
        return
    if fragment and resolved.suffix == ".md":
        target_page = pages.get(resolved)
        if target_page is not None and fragment not in target_page.heading_ids:
            report.error(page.rel, f"anchor #{fragment} not found in {rel_target} (pin it with "
                                   "`{ #id }` on the heading or fix the slug)", line=lineno)


# --- Checks: site-wide --------------------------------------------------------

def check_indexes(pages: dict[Path, Page], report: Report) -> None:
    for page in pages.values():
        if page.is_reserved:
            continue
        index = pages.get(page.path.parent / "index.md")
        if index is not None and page.path not in index.link_targets:
            report.warn(page.rel, f"not linked from its section index {index.rel}")


def check_nav(nav_paths: list[str], docs: Path, toml_path: Path, report: Report) -> None:
    for nav_path in nav_paths:
        if SCHEME_RE.match(nav_path):
            continue
        if not (docs / nav_path).is_file():
            report.error(toml_path.name, f"nav entry {nav_path!r} does not exist under {docs.name}/", file=toml_path)


def check_unreferenced(pages: dict[Path, Page], docs: Path, report: Report) -> None:
    referenced: set[Path] = set()
    for page in pages.values():
        referenced |= page.link_targets
    for root in REFERENCED_ROOTS:
        base = docs / root
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and not path.name.startswith(".") and path.suffix != ".md" \
                    and path not in referenced:
                report.warn(path.relative_to(docs).as_posix(), "not referenced from any .md page")


def check_materials_html(docs: Path, report: Report) -> None:
    base = docs / "materials"
    if not base.is_dir():
        return
    for path in sorted(base.rglob("*.html")):
        rel = path.relative_to(docs).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = [(text.count("\n", 0, m.start()) + 1, m.group(1)) for m in EXTERNAL_RESOURCE_RE.finditer(text)]
        for line, url in hits[:10]:
            report.error(rel, f"external resource {url} (materials HTML must be self-contained)", line=line)
        if len(hits) > 10:
            report.error(rel, f"{len(hits) - 10} more external resource(s) not listed")


def check_consistency(project: dict, docs: Path, toml_path: Path, report: Report) -> None:
    name = toml_path.name
    repo_url = str(project.get("repo_url", "") or "")
    m = GITHUB_REPO_RE.match(repo_url)
    slug = f"{m.group(1)}/{m.group(2)}" if m else None
    if not slug:
        report.warn(name, f"repo_url {repo_url!r} is not a https://github.com/<owner>/<repo> URL", file=toml_path)

    repo_name = project.get("repo_name")
    if repo_name and slug and repo_name != slug:
        report.warn(name, f"repo_name {repo_name!r} disagrees with repo_url slug {slug!r}", file=toml_path)

    site_url = str(project.get("site_url", "") or "")
    if not site_url:
        report.warn(name, "site_url is not set", file=toml_path)
    else:
        if not site_url.endswith("/"):
            report.warn(name, f"site_url {site_url!r} should end with a slash", file=toml_path)
        sm = re.match(r"^https?://([^./]+)\.github\.io/([^/?#]*)/?", site_url)
        if sm and slug:
            owner, repo = slug.split("/")
            if sm.group(1).lower() != owner.lower() or sm.group(2) != repo:
                report.warn(name, f"site_url {site_url!r} does not match repo slug {slug!r} "
                                  "(expected https://<owner>.github.io/<repo>/)", file=toml_path)

    edit_uri = str(project.get("edit_uri", "") or "")
    if edit_uri and not re.fullmatch(rf"(edit|blob)/[^/]+/{re.escape(docs.name)}/", edit_uri):
        report.warn(name, f"edit_uri {edit_uri!r} should look like edit/<branch>/{docs.name}/", file=toml_path)

    render = Path(__file__).resolve().parent / "render_notebooks.py"
    if render.is_file():
        rm = REPO_SLUG_RE.search(render.read_text(encoding="utf-8", errors="replace"))
        if not rm:
            report.warn(render.name, 'no REPO_SLUG = "<owner>/<repo>" constant found', file=render)
        elif slug and rm.group(1) != slug:
            report.warn(render.name, f"REPO_SLUG {rm.group(1)!r} disagrees with repo_url slug {slug!r}", file=render)


# --- Entry point --------------------------------------------------------------

def main(argv: list[str]) -> int:
    args = argv[1:]
    if not 1 <= len(args) <= 2:
        print("usage: site_lint.py <docs_dir> [zensical.toml]", file=sys.stderr)
        return 2
    docs = Path(args[0]).resolve()
    toml_path = Path(args[1]) if len(args) == 2 else Path("zensical.toml")
    if not docs.is_dir():
        print(f"error: {args[0]} is not a directory", file=sys.stderr)
        return 2

    report = Report(docs)
    pages = load_pages(docs, report)
    project, nav_paths = load_config(toml_path, report)
    nav_set = set(nav_paths)

    for page in pages.values():
        if not page.is_reserved:
            check_frontmatter(page, nav_set, docs, report)
        check_body(page, report)
        check_links(page, pages, docs, report)

    check_indexes(pages, report)
    check_nav(nav_paths, docs, toml_path, report)
    check_unreferenced(pages, docs, report)
    check_materials_html(docs, report)
    if project:
        check_consistency(project, docs, toml_path, report)
    return report.finish(len(pages))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
