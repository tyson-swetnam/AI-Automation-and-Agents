## Summary

<!-- One or two sentences: what changed and why. Link the wiki page, issue or discussion if there is one. -->

## Checklist

- [ ] **Frontmatter**: every new or edited content page has OKF frontmatter with a `type` from the closed set (`title`, `description`, tags with a scope tag and an audience tag; `stale_after` if a tool tag is present; `superseded_by` if `status: deprecated`). No `verified` key was added or changed by me. Section `index.md` files carry no frontmatter.
- [ ] **One H1**: each page has exactly one `# ` heading and it matches the frontmatter `title`.
- [ ] **Links**: internal links and images are relative (`../section/page.md`, `../assets/images/...`); external links carry `{target=_blank}`; nothing links into `instructor/` or to a GitHub `blob`/wiki URL; raw HTML `src`/`href` paths were computed from the rendered directory URL.
- [ ] **Validators**: `python scripts/okf_validate.py docs` and `python scripts/site_lint.py docs zensical.toml` pass locally with 0 errors (pipeline-owned pages were fixed in the wiki or in `scripts/migrate_wiki.py` `PATCHES`, not by hand).
- [ ] **llms indexes**: ran `python scripts/gen_llms_txt.py` and committed `docs/llms.txt` and `docs/llms-full.txt` (CI fails on drift).
- [ ] **Log**: added a `## YYYY-MM-DD` entry (newest first) to `docs/log.md`, prefixed **Initialization / Migration / Creation / Update / Deprecation / Removal**.

## Notes for reviewers

<!-- Anything a reviewer should look at closely: content conflicts left visible, pages marked draft, answer-key handling, materials added under docs/materials/. -->
