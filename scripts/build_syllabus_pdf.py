#!/usr/bin/env python3
"""Render the course syllabus PDF from docs/start-here/syllabus.md.

The PDF is generated from the site page rather than maintained separately, so the
downloadable syllabus and the page a learner reads cannot drift apart. Everything the
PDF prints - the instructor block, the course information table, the description, the
learning outcomes, the module overview and the completion rules - is parsed out of that
page; only the cover furniture and the styling live here.

Usage:
  python scripts/build_syllabus_pdf.py            # write docs/assets/files/<OUTPUT_NAME>
  python scripts/build_syllabus_pdf.py --check    # fail if the committed PDF is stale

Requires reportlab (in requirements-dev.txt). Fonts are the built-in Helvetica family,
so the script has no font-file dependencies.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, ListFlowable,
                                ListItem, NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "start-here" / "syllabus.md"
OUTPUT = ROOT / "docs" / "assets" / "files" / "AI-Automation-and-Agents-Syllabus-UNM.pdf"

COURSE_TITLE = "AI Automation & Agents"
COURSE_TAGLINE = "Build Workflows. Deploy Agents. Work Smarter."
INSTITUTION = "Center for Advanced Research Computing, University of New Mexico"
SITE_URL = "https://tyson-swetnam.github.io/AI-Automation-and-Agents/"
# Bumped deliberately, never from the clock, so reruns are byte-stable.
REVISION = "Revised September 2026"

# UNM brand
CHERRY = colors.HexColor("#ba0c2f")
CHERRY_DARK = colors.HexColor("#6d0a1f")
TURQUOISE = colors.HexColor("#007a86")
SILVER = colors.HexColor("#a7a8aa")
INK = colors.HexColor("#1e242a")
RULE = colors.HexColor("#d8dcdf")


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------

INLINE_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)(?:\{[^}]*\})?")
INLINE_AUTOLINK = re.compile(r"<((?:https?|mailto):[^>]+|[^<>@\s]+@[^<>@\s]+)>")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
CODE = re.compile(r"`([^`]+)`")
ATTRS = re.compile(r"\{[^{}]*\}")


def inline(text: str) -> str:
    """Markdown inline markup -> the small HTML subset reportlab understands."""
    text = text.replace("&", "&amp;")
    text = INLINE_AUTOLINK.sub(lambda m: m.group(1).replace("mailto:", ""), text)
    # any angle bracket left is literal punctuation, not markup reportlab should parse
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = INLINE_LINK.sub(r"\1", text)
    text = ATTRS.sub("", text)
    text = BOLD.sub(r"<b>\1</b>", text)
    text = ITALIC.sub(r"<i>\1</i>", text)
    text = CODE.sub(r"<font face='Courier'>\1</font>", text)
    return re.sub(r"\s+", " ", text).strip()


def split_sections(body: str) -> dict[str, list[str]]:
    """Split the page body into {h2 title: [lines]} , dropping admonition blocks."""
    lines, out, current = body.split("\n"), {}, None
    skip_admonition = False
    for line in lines:
        if re.match(r"^(\?\?\?|!!!)", line):
            skip_admonition = True
            continue
        if skip_admonition:
            if line.strip() and not line.startswith("    "):
                skip_admonition = False
            else:
                continue
        m = re.match(r"^## +(.*?)\s*$", line)
        if m:
            current = m.group(1)
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return out


def parse_table(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    rows = [l.strip() for l in lines if l.strip().startswith("|")]
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [c for c in cells if not all(re.fullmatch(r":?-{2,}:?", x) for x in c)]
    return cells[0], cells[1:]


def parse_paragraphs(lines: list[str]) -> list[str]:
    """Plain prose paragraphs: skip tables, list items and their indented continuations."""
    paras, buf, in_item = [], [], False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buf:
                paras.append(" ".join(buf))
                buf = []
            in_item = False
            continue
        if stripped.startswith(("|", "-", "*", "#", "<")) or re.match(r"^\d+\.", stripped):
            in_item = True
            continue
        if in_item and line.startswith(("  ", "\t")):
            continue
        in_item = False
        buf.append(stripped)
    if buf:
        paras.append(" ".join(buf))
    return paras


def parse_list(lines: list[str], ordered: bool) -> list[str]:
    pattern = r"^\s*\d+\.\s+(.*)$" if ordered else r"^\s*[-*]\s+(.*)$"
    items, buf = [], None
    for line in lines:
        m = re.match(pattern, line)
        if m:
            if buf is not None:
                items.append(" ".join(buf))
            buf = [m.group(1).strip()]
        elif buf is not None and line.strip() and (line.startswith("  ") or line.startswith("\t")):
            buf.append(line.strip())
        elif buf is not None and not line.strip():
            items.append(" ".join(buf))
            buf = None
    if buf is not None:
        items.append(" ".join(buf))
    return items


def parse_instructor(lines: list[str]) -> list[str]:
    return [inline(l) for l in lines if l.strip() and not l.strip().startswith("#")]


# ---------------------------------------------------------------------------
# Document furniture
# ---------------------------------------------------------------------------

def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    s = {}
    s["title"] = ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold",
                                fontSize=30, leading=34, textColor=colors.white, alignment=0)
    s["tagline"] = ParagraphStyle("tagline", fontName="Helvetica", fontSize=13, leading=17,
                                  textColor=colors.white, alignment=0)
    s["covermeta"] = ParagraphStyle("covermeta", fontName="Helvetica", fontSize=10.5,
                                    leading=15, textColor=INK)
    s["h1"] = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=16, leading=20,
                             textColor=CHERRY, spaceBefore=18, spaceAfter=7)
    s["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5,
                               textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7)
    s["cell"] = ParagraphStyle("cell", fontName="Helvetica", fontSize=9, leading=12.5,
                               textColor=INK)
    s["cellb"] = ParagraphStyle("cellb", parent=s["cell"], fontName="Helvetica-Bold")
    s["cellhead"] = ParagraphStyle("cellhead", parent=s["cell"], fontName="Helvetica-Bold",
                                   textColor=colors.white)
    s["item"] = ParagraphStyle("item", parent=s["body"], alignment=0, spaceAfter=5)
    s["note"] = ParagraphStyle("note", fontName="Helvetica", fontSize=8.5, leading=12,
                               textColor=colors.HexColor("#55606a"))
    return s


def make_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(inch, 0.72 * inch, LETTER[0] - inch, 0.72 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#55606a"))
    canvas.drawString(inch, 0.55 * inch, f"{COURSE_TITLE} - {INSTITUTION}")
    canvas.drawRightString(LETTER[0] - inch, 0.55 * inch, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def make_cover_banner(canvas, doc):
    """Cherry banner with the title drawn straight onto it (white on white otherwise)."""
    h = 2.5 * inch
    top = LETTER[1]
    canvas.saveState()
    canvas.setFillColor(CHERRY_DARK)
    canvas.rect(0, top - h, LETTER[0], h, stroke=0, fill=1)
    canvas.setFillColor(CHERRY)
    canvas.rect(0, top - h, LETTER[0] * 0.66, h, stroke=0, fill=1)
    canvas.setFillColor(TURQUOISE)
    canvas.rect(0, top - h - 9, LETTER[0], 9, stroke=0, fill=1)

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 29)
    canvas.drawString(inch, top - 1.32 * inch, COURSE_TITLE)
    canvas.setFont("Helvetica", 13)
    canvas.drawString(inch, top - 1.68 * inch, COURSE_TAGLINE)
    canvas.setFont("Helvetica", 9.5)
    canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.85))
    canvas.drawString(inch, top - 2.06 * inch, INSTITUTION.upper())
    canvas.restoreState()


def table(data, col_widths, st, header=True, zebra=True):
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), CHERRY),
                  ("LINEBELOW", (0, 0), (-1, 0), 0.8, CHERRY_DARK)]
    if zebra:
        first = 1 if header else 0
        for i in range(first, len(data)):
            if (i - first) % 2 == 1:
                style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f6f7f8")))
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style))
    return t


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build(path: Path) -> None:
    raw = SOURCE.read_text(encoding="utf-8")
    body = re.sub(r"^---\n.*?\n---\n", "", raw, count=1, flags=re.S)
    lead = ""
    for line in body.split("\n"):
        if line.startswith("*AI Automation"):
            lead = line
            break
    sec = split_sections(body)
    st = styles()

    def need(name: str) -> list[str]:
        if name not in sec:
            sys.exit(f"error: '## {name}' not found in {SOURCE.relative_to(ROOT)}; "
                     "the page structure changed, update this script")
        return sec[name]

    story = []

    # --- cover -------------------------------------------------------------
    story.append(Paragraph("Course syllabus", st["h1"]))
    story.append(Paragraph(inline(lead), st["body"]))
    story.append(Spacer(1, 6))

    instructor = parse_instructor(need("Instructor of record"))
    story.append(table(
        [[Paragraph("Instructor of record", st["cellhead"])]] +
        [[Paragraph(line, st["cellb"] if i == 0 else st["cell"])] for i, line in enumerate(instructor)],
        [6.5 * inch], st))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"Course site: {SITE_URL}<br/>{REVISION}. Licensed CC BY 4.0.", st["note"]))

    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # --- course information ------------------------------------------------
    head, rows = parse_table(need("Course information"))
    story.append(Paragraph("Course information", st["h1"]))
    story.append(table(
        [[Paragraph(h, st["cellhead"]) for h in head]] +
        [[Paragraph(inline(r[0]), st["cellb"]), Paragraph(inline(r[1]), st["cell"])] for r in rows],
        [1.55 * inch, 4.95 * inch], st))

    # --- description -------------------------------------------------------
    story.append(Paragraph("Course description", st["h1"]))
    for para in parse_paragraphs(need("Course description")):
        story.append(Paragraph(inline(para), st["body"]))

    # --- outcomes ----------------------------------------------------------
    outcomes = parse_list(need("Course learning outcomes"), ordered=True)
    intro = [p for p in parse_paragraphs(need("Course learning outcomes")) if p]
    story.append(Paragraph("Course learning outcomes", st["h1"]))
    if intro:
        story.append(Paragraph(inline(intro[0]), st["body"]))
    story.append(ListFlowable(
        [ListItem(Paragraph(inline(o), st["item"]), leftIndent=18) for o in outcomes],
        bulletType="1", bulletFontName="Helvetica-Bold", bulletFontSize=10,
        leftIndent=18, bulletColor=CHERRY))

    # --- module overview ---------------------------------------------------
    head, rows = parse_table(need("Course overview"))
    story.append(PageBreak())
    story.append(Paragraph("Course overview", st["h1"]))
    story.append(table(
        [[Paragraph(h, st["cellhead"]) for h in head]] +
        [[Paragraph(inline(c), st["cellb"] if i in (0, 1) else st["cell"])
          for i, c in enumerate(r)] for r in rows],
        [0.4 * inch, 1.95 * inch, 3.55 * inch, 0.6 * inch], st))

    # --- completion --------------------------------------------------------
    completion = need("Completion and certification")
    story.append(Paragraph("Completion and certification", st["h1"]))
    for para in parse_paragraphs(completion)[:1]:
        story.append(Paragraph(inline(para), st["body"]))
    story.append(ListFlowable(
        [ListItem(Paragraph(inline(b), st["item"]), leftIndent=16)
         for b in parse_list(completion, ordered=False)],
        bulletType="bullet", bulletFontSize=8, leftIndent=16, bulletColor=TURQUOISE))
    tail = parse_paragraphs(completion)[1:]
    for para in tail:
        story.append(Paragraph(inline(para), st["body"]))

    # --- licence -----------------------------------------------------------
    licence = [Paragraph("License and attribution", st["h1"]), Paragraph(
        "Copyright 2026 The Regents of the University of New Mexico, Center for Advanced "
        "Research Computing. This syllabus and the course materials are licensed under the "
        "Creative Commons Attribution 4.0 International License (CC BY 4.0); you may share "
        "and adapt them for any purpose, including commercially, with credit. The course was "
        "developed at the Arizona Institute for Artificial Intelligence and the Office of "
        "Responsible Artificial Intelligence at the University of Arizona and released there "
        "under CC0 1.0. Third-party material quoted or linked by the course keeps its own "
        "terms.", st["body"]), Spacer(1, 4), Paragraph(
        f"Generated from docs/start-here/syllabus.md by scripts/build_syllabus_pdf.py. "
        f"The course site is the authoritative version: {SITE_URL}", st["note"])]
    story.append(KeepTogether(licence))

    frame_cover = Frame(inch, inch, LETTER[0] - 2 * inch, LETTER[1] - 2.5 * inch - 1.05 * inch,
                        id="cover", showBoundary=0)
    frame_body = Frame(inch, 0.9 * inch, LETTER[0] - 2 * inch, LETTER[1] - 1.9 * inch,
                       id="body", showBoundary=0)
    doc = BaseDocTemplate(str(path), pagesize=LETTER, title=f"{COURSE_TITLE} - Course syllabus",
                          author=INSTITUTION, subject="Course syllabus",
                          creator="scripts/build_syllabus_pdf.py")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame_cover], onPage=make_cover_banner),
        PageTemplate(id="body", frames=[frame_body], onPage=make_footer),
    ])
    doc.build(story)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="verify the committed PDF matches the page (ignores the PDF's own timestamps)")
    args = ap.parse_args()

    if args.check:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            fresh = Path(d) / OUTPUT.name
            build(fresh)
            if not OUTPUT.exists():
                print(f"ERROR {OUTPUT.relative_to(ROOT)} is missing; run this script")
                return 1
            # PDFs embed a creation timestamp and a document id, so compare page text
            a, b = pdf_text(OUTPUT), pdf_text(fresh)
            if a is None or b is None:
                print("ERROR pypdf is not installed, so the PDF cannot be compared; "
                      "pip install pypdf (see requirements-dev.txt)")
                return 1
            if a != b:
                print(f"ERROR {OUTPUT.relative_to(ROOT)} is stale; rerun scripts/build_syllabus_pdf.py")
                return 1
        print("syllabus PDF is up to date with docs/start-here/syllabus.md")
        return 0

    build(OUTPUT)
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size // 1024} KB)")
    return 0


def pdf_text(path: Path) -> str | None:
    """Extract page text for the staleness check, or None if pypdf is unavailable.

    Returning None rather than an empty string matters: two empty strings compare
    equal, so a missing pypdf would silently turn --check into a no-op that always
    passes. The caller treats None as an error instead.

    Whitespace is collapsed because reportlab decides line breaks itself, and a
    different reportlab release can wrap the same sentence differently. Comparing
    the words rather than the layout keeps the check honest about content changes
    without failing CI over a library upgrade.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    raw = " ".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
    return " ".join(raw.split())


if __name__ == "__main__":
    sys.exit(main())
