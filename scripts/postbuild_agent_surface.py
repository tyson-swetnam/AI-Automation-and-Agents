#!/usr/bin/env python3
"""Post-build step: make the rendered site consumable by AI agents.

Run AFTER `zensical build`. It:

1. Mirrors every source Markdown file — OKF v0.2 frontmatter intact — into
   the built site at each page's pretty URL:
       docs/a/b.md        -> site/a/b/index.md      (page URL + "index.md")
       docs/a/index.md    -> site/a/index.md
       docs/index.md      -> site/index.md
   so any agent can turn a page URL into its canonical Markdown by appending
   `index.md`. Relative links in the mirror are rewritten to absolute URLs
   that point at the linked page's own Markdown twin (scripts/okf_links.py):
   the mirror sits one directory deeper than its source, and an agent reading
   Markdown should keep getting Markdown as it traverses. The sources under
   docs/ are never modified. docs/assets, docs/materials and docs/stylesheets
   hold no content pages and are never mirrored.
2. Injects agent-discoverable metadata into each page's <head>:
       <link rel="alternate" type="text/markdown" href="index.md">
       <meta name="okf:type" | okf:status | okf:trust-tier | okf:generated-at
             | okf:generated-by | okf:stale-after | okf:superseded-by>
   plus Open Graph and Twitter card tags (title, description, type, url,
   image, site_name, locale) and a schema.org JSON-LD record: an
   EducationalOrganization and a Course on the landing page, and a
   LearningResource tied to that Course on every typed content page. Link
   previews, search engines and site scanners read those rather than the
   OKF frontmatter.
   okf:superseded-by is emitted only for deprecated pages whose frontmatter
   names a replacement; a relative Markdown path is resolved to the
   replacement's absolute page URL.
3. Adds two *visible* pointers to every page, because text extraction and
   link-derived URL allowlists never see <head>: a "View this page as
   Markdown" button beside "View source", and a "Machine-readable" line at
   the end of the article linking the Markdown twin, the raw source on
   GitHub, llms.txt and llms-full.txt.
4. Gives 404.html a recovery body — links to the home page, llms.txt,
   llms-full.txt, sitemap.xml, the wiki crosswalk and the agent guide — and
   writes 404.md beside it, so an agent that lands on a dead URL is told
   where to look instead of reading a bare "404 - Not found".
5. Writes robots.txt advertising sitemap.xml, /llms.txt, /llms-full.txt, the
   Markdown mirror and raw-source conventions, and the agent guide at
   /about/ai-agents/.

Adapted from UNM-CARC/docs (scripts/postbuild_agent_surface.py).

Usage: python3 scripts/postbuild_agent_surface.py [site_dir]
"""

from __future__ import annotations

import html
import json
import posixpath
import re
import sys
from pathlib import Path

import yaml

from okf_links import raw_source_url, rewrite_relative_targets, site_url

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Top-level directories under docs/ that hold no content pages.
SKIP_TOP = {"assets", "materials", "stylesheets"}


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def trust_tier(fm: dict) -> str:
    """OKF §5.3: unverified | machine-confirmed | human-reviewed."""
    v = fm.get("verified")
    if not v:
        return "unverified"
    entries = v if isinstance(v, list) else [v]
    actors = [str(e.get("by", "")) for e in entries if isinstance(e, dict)]
    if any(a.startswith("human:") for a in actors):
        return "human-reviewed"
    return "machine-confirmed" if actors else "unverified"


def page_url(base: str, rel: Path) -> str:
    """Pretty (use_directory_urls) URL of a docs-relative Markdown path."""
    if rel.name == "index.md":
        tail = rel.parent.as_posix() + "/" if rel.parent.as_posix() != "." else ""
    else:
        tail = rel.with_suffix("").as_posix() + "/"
    return base + tail


def superseded_url(value, rel: Path, base: str) -> str:
    """Resolve a page's `superseded_by` to an absolute URL.

    Absolute URLs pass through. A relative Markdown path (as written in the
    frontmatter, relative to the page's own directory, e.g.
    ../../modules/module-1/activities.md) becomes the replacement's page URL.
    Anything else is emitted verbatim."""
    v = str(value).strip()
    if re.match(r"^https?://", v):
        return v
    target, _, fragment = v.partition("#")
    norm = posixpath.normpath(posixpath.join(rel.parent.as_posix(), target))
    if norm.startswith("..") or not norm.endswith(".md"):
        return v
    url = page_url(base, Path(norm))
    return url + (f"#{fragment}" if fragment else "")


LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
PROVIDER_NAME = "Center for Advanced Research Computing, University of New Mexico"
INSTRUCTOR = "Tyson Swetnam"
# Published on the syllabus page already; schema.org consumers expect a contact point.
CONTACT_EMAIL = "tswetnam@unm.edu"


def config_value(key: str, default: str = "") -> str:
    m = re.search(rf'^{key}\s*=\s*"([^"]*)"', (ROOT / "zensical.toml").read_text(encoding="utf-8"),
                  re.MULTILINE)
    return m.group(1) if m else default


def iso_duration(value: str) -> str | None:
    """"8 hours" -> PT8H, "45 minutes" -> PT45M; anything else -> None."""
    m = re.match(r"\s*(\d+(?:\.\d+)?)\s*(hours?|hrs?|minutes?|mins?)", str(value), re.I)
    if not m:
        return None
    n = float(m.group(1))
    unit = "H" if m.group(2).lower().startswith(("h", "hr")) else "M"
    return "PT" + (str(int(n)) if n.is_integer() else str(n)) + unit


def page_title(fm: dict, text: str) -> str:
    if fm.get("title"):
        return str(fm["title"])
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    return html.unescape(m.group(1)).strip() if m else config_value("site_name")


def module_titles() -> list[str]:
    out = []
    for n in range(1, 6):
        path = DOCS / f"modules/module-{n}/overview.md"
        if path.is_file():
            title = frontmatter(path).get("title")
            if title:
                out.append(str(title))
    return out


def jsonld(fm: dict, rel: Path, base: str, title: str, description: str) -> str:
    """EducationalOrganization + Course on the landing page, LearningResource elsewhere."""
    url = page_url(base, rel)
    provider = {
        "@type": "EducationalOrganization",
        "@id": base + "#provider",
        "name": PROVIDER_NAME,
        "alternateName": "UNM CARC",
        "url": "https://carc.unm.edu/",
        "sameAs": ["https://github.com/UNM-CARC"],
        "parentOrganization": {"@type": "CollegeOrUniversity",
                               "name": "University of New Mexico",
                               "url": "https://www.unm.edu/"},
        "contactPoint": {"@type": "ContactPoint", "contactType": "instructor of record",
                         "name": INSTRUCTOR, "email": CONTACT_EMAIL,
                         "url": base + "start-here/syllabus/"},
    }
    if rel.as_posix() == "index.md":
        course = {
            "@type": "Course",
            "@id": base + "#course",
            "name": config_value("site_name"),
            "url": base,
            "description": config_value("site_description"),
            "inLanguage": "en",
            "isAccessibleForFree": True,
            "license": LICENSE_URL,
            "educationalLevel": "professional development (non-credit)",
            "provider": {"@id": base + "#provider"},
            "teaches": module_titles(),
            "timeRequired": "PT40H",
            "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online",
                                  "courseWorkload": "PT40H",
                                  "instructor": {"@type": "Person", "name": INSTRUCTOR}},
        }
        graph = {"@context": "https://schema.org", "@graph": [provider, course]}
    else:
        role = "teacher" if "instructor-facing" in (fm.get("tags") or []) else "student"
        node = {
            "@context": "https://schema.org",
            "@type": "LearningResource",
            "@id": url,
            "url": url,
            "name": title,
            "description": description,
            "inLanguage": "en",
            "isAccessibleForFree": True,
            "license": LICENSE_URL,
            "isPartOf": {"@id": base + "#course"},
            "provider": {"@id": base + "#provider"},
            "encoding": {"@type": "MediaObject", "encodingFormat": "text/markdown",
                         "contentUrl": url + "index.md"},
            "audience": {"@type": "EducationalAudience", "educationalRole": role},
        }
        if fm.get("type"):
            node["learningResourceType"] = str(fm["type"])
        duration = iso_duration(fm.get("time_estimate", ""))
        if duration:
            node["timeRequired"] = duration
        gen = fm.get("generated") or {}
        if isinstance(gen, dict) and gen.get("at"):
            node["dateModified"] = str(gen["at"])
        graph = node
    return ('<script type="application/ld+json">'
            + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>")


def social_block(fm: dict, rel: Path, base: str, title: str, description: str) -> list[str]:
    url = page_url(base, rel)
    is_home = rel.as_posix() == "index.md"
    esc = lambda v: html.escape(str(v), quote=True)
    tags = [("og:title", title), ("og:description", description),
            ("og:type", "website" if is_home else "article"),
            ("og:url", url), ("og:site_name", config_value("site_name")),
            ("og:locale", "en_US"), ("og:image", base + "assets/social-card.png"),
            ("og:image:alt", config_value("site_name") + " — a University of New Mexico course")]
    lines = [f'<meta property="{k}" content="{esc(v)}">' for k, v in tags]
    lines += [f'<meta name="twitter:card" content="summary_large_image">',
              f'<meta name="twitter:title" content="{esc(title)}">',
              f'<meta name="twitter:description" content="{esc(description)}">',
              f'<meta name="twitter:image" content="{base}assets/social-card.png">']
    return lines


def head_block(fm: dict, rel: Path, base: str) -> str:
    # Sentinel first: the idempotency check looks for this, not for page content.
    lines = ['<meta name="okf:surface" content="generated">',
             '<meta name="robots" content="index, follow, max-snippet:-1, '
             'max-image-preview:large, max-video-preview:-1">',
             '<link rel="alternate" type="text/markdown" '
             'title="Markdown source (OKF v0.2 frontmatter)" href="index.md">']

    def meta(name, value):
        if value:
            lines.append(f'<meta name="{name}" content="{html.escape(str(value), quote=True)}">')

    meta("okf:type", fm.get("type"))
    meta("okf:status", fm.get("status", "stable") if fm else None)
    meta("okf:trust-tier", trust_tier(fm) if fm else None)
    gen = fm.get("generated") or {}
    if isinstance(gen, dict):
        meta("okf:generated-at", gen.get("at"))
        meta("okf:generated-by", gen.get("by"))
    meta("okf:stale-after", fm.get("stale_after"))
    if fm.get("superseded_by"):
        meta("okf:superseded-by", superseded_url(fm["superseded_by"], rel, base))
    return "\n".join(lines) + "\n"


# A document glyph for the Markdown button: two strokes of text on a dog-eared page.
MD_ICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
           'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
           'stroke-linejoin="round" aria-hidden="true">'
           '<path d="M6 2h8l4 4v16H6z"/><path d="M14 2v4h4"/><path d="M9 12h6M9 16h6"/></svg>')


def markdown_button() -> str:
    """A third content-header button, beside Edit this page and View source."""
    return ('<a href="index.md" title="View this page as Markdown (for AI agents and '
            'screen readers)" class="md-content__button md-icon" '
            'type="text/markdown">' + MD_ICON + "</a>\n")


def machine_readable_line(rel: Path, base: str) -> str:
    """Pointers in the body: <head> metadata survives no text extraction."""
    url = page_url(base, rel)
    raw = raw_source_url(rel.as_posix())
    parts = [f'<a href="{url}index.md" type="text/markdown">this page as Markdown</a>']
    if raw:
        parts.append(f'<a href="{raw}">raw source on GitHub</a>')
    parts += [f'<a href="{base}llms.txt">llms.txt</a>',
              f'<a href="{base}llms-full.txt">llms-full.txt (whole site)</a>']
    return ('<p class="course-machine-readable">Machine-readable: ' + " · ".join(parts)
            + f'. See <a href="{base}about/ai-agents/">For AI agents</a>.</p>\n')


def add_visible_pointers(text: str, rel: Path, base: str) -> str:
    marker = 'title="View source of this page" class="md-content__button md-icon">'
    if marker in text:
        end = text.index("</a>", text.index(marker)) + len("</a>")
        text = text[:end] + "\n" + markdown_button() + text[end:]
    if "</article>" in text:
        text = text.replace("</article>", machine_readable_line(rel, base) + "</article>", 1)
    return text


RECOVERY_LINKS = [
    ("", "Course home — the five modules, in order"),
    ("llms.txt", "llms.txt — a linked outline of every page, each with its Markdown twin and raw source"),
    ("llms-full.txt", "llms-full.txt — the whole corpus in one file"),
    ("sitemap.xml", "sitemap.xml — every URL on this site"),
    ("about/wiki-crosswalk/", "Wiki crosswalk — where each old course-wiki URL moved to"),
    ("about/ai-agents/", "For AI agents — the endpoints and conventions this site follows"),
]


def recovery_html(base: str) -> str:
    items = "".join(f'<li><a href="{base}{path}">{html.escape(label)}</a></li>'
                    for path, label in RECOVERY_LINKS)
    markdown = html.escape(recovery_markdown(base).strip())
    return ('<div class="course-404-recovery">'
            "<p>That page does not exist on this site. Try one of these instead:</p>"
            f"<ul>{items}</ul>"
            "<p>Any page URL plus <code>index.md</code> returns that page's Markdown with its "
            "OKF frontmatter; a Markdown copy of this page is at "
            f'<a href="{base}404.md">404.md</a>.</p>'
            "<details><summary>The same recovery points as Markdown, for agents</summary>"
            f"<pre>{markdown}</pre></details></div>\n")


def recovery_markdown(base: str) -> str:
    lines = ["# 404 — page not found", "",
             "That page does not exist on this site. Try one of these instead:", ""]
    lines += [f"- [{label}]({base}{path})" for path, label in RECOVERY_LINKS]
    lines += ["",
              "Any page URL plus `index.md` returns that page's Markdown with its OKF "
              "frontmatter. The linked outline in llms.txt is the fastest way to find the "
              "page you meant.", ""]
    return "\n".join(lines)


def dest_for(rel: Path, site: Path) -> Path:
    if rel.name == "index.md":
        return site / rel
    return site / rel.parent / rel.stem / "index.md"


def main():
    site = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "site"
    if not site.is_dir():
        print(f"error: {site} not found — run `zensical build` first", file=sys.stderr)
        sys.exit(2)
    base = site_url()

    # 0. Zensical writes an empty objects.inv (a Sphinx inventory stub). No
    # consumer reads a zero-byte inventory, so drop it from the deploy.
    inv = site / "objects.inv"
    if inv.exists() and inv.stat().st_size == 0:
        inv.unlink()

    # 1. Mirror Markdown sources at pretty URLs.
    mirrored = 0
    pages: dict[Path, tuple[Path, dict]] = {}
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS)
        if rel.parts[0] in SKIP_TOP:
            continue
        dest = dest_for(rel, site)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(rewrite_relative_targets(path.read_text(encoding="utf-8"),
                                                 rel.as_posix(), base), encoding="utf-8")
        pages[dest.parent.resolve()] = (rel, frontmatter(path))
        mirrored += 1

    # 2. Inject <head> metadata into each page whose directory has a mirror.
    injected = 0
    for htmlfile in sorted(site.rglob("index.html")):
        entry = pages.get(htmlfile.parent.resolve())
        if entry is None:
            continue
        rel, fm = entry
        text = htmlfile.read_text(encoding="utf-8")
        # A page may quote the tags this step injects — about/ai-agents.md does, in
        # inline code that no highlighter breaks up — so test for the sentinel instead.
        if 'name="okf:surface"' in text:
            continue  # already annotated
        title = page_title(fm, text)
        description = str(fm.get("description", "")).strip() or config_value("site_description")
        extra = "\n".join(social_block(fm, rel, base, title, description)
                          + [jsonld(fm, rel, base, title, description)]) + "\n"
        text = text.replace("</head>", head_block(fm, rel, base) + extra + "</head>", 1)
        text = add_visible_pointers(text, rel, base)
        htmlfile.write_text(text, encoding="utf-8")
        injected += 1

    # 3. A 404 that tells an agent where to look instead.
    notfound = site / "404.html"
    if notfound.is_file():
        html_text = notfound.read_text(encoding="utf-8")
        if "course-404-recovery" not in html_text:
            marker = "<h1>404 - Not found</h1>"
            if marker in html_text:
                html_text = html_text.replace(marker, marker + recovery_html(base), 1)
                notfound.write_text(html_text, encoding="utf-8")
    (site / "404.md").write_text(recovery_markdown(base), encoding="utf-8")

    # 4. robots.txt — explicitly welcome AI fetchers alongside the blanket allow.
    ai_agents = ["Googlebot", "Google-Extended", "GoogleOther", "Google-CloudVertexBot",
                 "GPTBot", "OAI-SearchBot", "ChatGPT-User",
                 "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot",
                 "cohere-ai", "Applebot-Extended", "CCBot", "meta-externalagent",
                 "Amazonbot", "DuckAssistBot", "MistralAI-User"]
    ai_block = "".join(f"User-agent: {a}\nAllow: /\n\n" for a in ai_agents)
    (site / "robots.txt").write_text(
        "# AI Automation and Agents — University of New Mexico (CARC) course site\n"
        f"# {base}\n"
        "# This course is published for people AND for AI agents.\n"
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        + ai_block +
        f"Sitemap: {base}sitemap.xml\n"
        "\n"
        "# AI agents and harnesses:\n"
        f"#   Machine-readable outline:  {base}llms.txt\n"
        f"#   Full corpus (one file):    {base}llms-full.txt\n"
        "#   Markdown source of any page (OKF v0.2 frontmatter: type, provenance,\n"
        "#   trust, lifecycle): append `index.md` to the page URL. Its links are\n"
        "#   absolute and point at other pages' Markdown twins.\n"
        f"#   Raw Markdown on GitHub:    {raw_source_url()}<path>.md\n"
        f"#   Agent guide:               {base}about/ai-agents/\n",
        encoding="utf-8")

    print(f"agent surface: mirrored {mirrored} markdown files (links absolutized), "
          f"annotated {injected} pages with metadata, Open Graph tags, JSON-LD, a Markdown "
          "button and a machine-readable line, wrote 404 recovery and robots.txt")


if __name__ == "__main__":
    main()
