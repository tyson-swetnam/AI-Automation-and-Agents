---
title: "License and attribution"
description: "The course is published under Creative Commons Attribution 4.0 International, with the site code under BSD 3-Clause: who holds copyright over which part, what the license lets you do, how to attribute it, and which material is not covered."
type: Policy
tags: [course, student-facing, license, attribution, creative-commons, open-educational-resources, ai2s]
status: stable
generated:
  by: "claude/fable-5-1"
  at: "2026-09-09T00:00:00Z"
sources:
  - id: wiki-footer
    resource: "https://github.com/UA-AI2S/AI-Automation-and-Agents-v2/wiki/_Footer"
    title: "AI Automation and Agents v2 wiki: _Footer (license badge and attribution)"
    author: "Carlos Lizárraga-Celaya"
    last_modified: "2026-04-20T17:21:32-07:00"
  - id: repo-license
    resource: "https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/LICENSE"
    title: "Repository LICENSE file (CC BY 4.0)"
    author: "UA-AI2S course team; UNM CARC"
---

# License and attribution

[![Creative Commons Attribution 4.0 International](../assets/cc-by.png){ width="100" }](https://creativecommons.org/licenses/by/4.0/){target=_blank}

*AI Automation and Agents* is published under the
[Creative Commons Attribution 4.0 International license (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/){target=_blank}.
That is the most permissive of the standard Creative Commons licenses: it asks
for credit and nothing else.

## Who holds copyright over what

This site brings together two bodies of work with different owners. Both are
CC BY 4.0, so the terms below apply either way; only the credit differs.

| Part | Copyright |
| :-- | :-- |
| The course itself: the module pages, images, lab notebooks and the interactive quiz and survey | 2026 [Arizona Institute for Artificial Intelligence (AI2S)](https://responsibleai.arizona.edu/ai2s){target=_blank} and the [Office of Responsible Artificial Intelligence](https://responsibleai.arizona.edu/){target=_blank}, The University of Arizona |
| This site: the landing page, the Start here and About sections, the instructor materials page, the section indexes, the change log, the Open Knowledge Format structure and the design | 2026 The Regents of the University of New Mexico, [Center for Advanced Research Computing](https://carc.unm.edu/){target=_blank} |

The course text was written by the AI2S course team and migrated from their
wiki; every migrated page names its source page and its authors in the
`sources` and `authorship` keys of its frontmatter, so the provenance travels
with the content. UNM CARC built the site around it.

## What the license lets you do

Under CC BY 4.0 you may **share** the course material (copy and redistribute
it in any medium or format) and **adapt** it (remix, transform and build upon
it), for any purpose, including commercially. The single condition is
**attribution**: give appropriate credit, link to the license, and indicate
whether you made changes. You may not add legal or technological restrictions
that stop anyone else from doing the same.

The full legal text is at
[creativecommons.org/licenses/by/4.0/legalcode](https://creativecommons.org/licenses/by/4.0/legalcode){target=_blank}
and in the repository's `LICENSE` file.

!!! info "Why CC BY rather than a NonCommercial license"

    CC BY is one of the licenses approved for
    [Free Cultural Works](https://creativecommons.org/public-domain/freeworks/){target=_blank}
    and it meets the [Open Definition](https://opendefinition.org/){target=_blank},
    so this course qualifies as an open educational resource under the strict
    reading, not only the loose one. A NonCommercial clause would have blocked
    much of the reuse this course is designed for: a company running a module
    as internal training, a workshop that charges a registration fee, or
    another institution folding it into a paid certificate. Creative Commons
    notes that the NonCommercial test turns on the *use*, not the user, which
    makes it ambiguous for tuition-funded teaching.

Instructors at other institutions are welcome to reuse and adapt the modules,
including in paid programs, as long as they credit the original.

## How to attribute

A suggested attribution line:

> *AI Automation and Agents*, Arizona Institute for Artificial Intelligence
> (AI2S), Office of Responsible Artificial Intelligence, The University of
> Arizona, 2026. Site by the Center for Advanced Research Computing,
> University of New Mexico. Licensed under CC BY 4.0.
> https://tyson-swetnam.github.io/AI-Automation-and-Agents/

If you are reusing a course page, credit AI2S; if you are reusing the site
structure or its tooling, credit UNM CARC.

When you reuse a single page, cite that page's URL; every page on this site
has a stable address and a Markdown source you can link to (append
`index.md` to the page URL).

## Code is licensed separately

Creative Commons licenses are not designed for software, so the site's own
code carries the [BSD 3-Clause License](https://github.com/tyson-swetnam/AI-Automation-and-Agents/blob/main/LICENSE-CODE){target=_blank}
instead, copyright The Regents of the University of New Mexico. That covers
the migration and validation scripts in `scripts/`, the site configuration and
the stylesheet.

The lab notebooks and the interactive quiz and survey are course materials
written by the AI2S team, not site tooling, so they stay under CC BY 4.0 with
the rest of the content.

## Authors

The course content was written by the AI2S course team. The page footers in
the source wiki credit **Carlos Lizárraga-Celaya** and **Michelle Yung** with
creation and updates; the wiki's git history also records contributions from
**Michele Cosi**. Each page's frontmatter on this site lists the wiki page it
came from and its last wiki change under `sources`, and the `authorship` key
carries the created/updated dates and initials from the original footer.

## Material this license does not cover

The readings and reading guides summarise and quote works that keep their own
terms: the LangChain documentation, Wooldridge and Jennings' *Intelligent
Agents: Theory and Practice* (1995), vendor documentation for the frameworks
used in the labs, published standards such as the NIST AI RMF and the OWASP
Top 10 for LLM Applications, and the videos and articles linked from the
resource lists. Those remain the property of their authors and are cited
where they appear. The University of Arizona and University of New Mexico
names, logos and wordmarks are trademarks of those universities and are not
covered by the Creative Commons license.

## The site itself

The site is built with [Zensical](https://zensical.org){target=_blank} and
structured as an [Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md){target=_blank}
knowledge bundle; see [Contributing](contributing.md) for how it is
maintained and [For AI agents](ai-agents.md) for how machines should read it.
