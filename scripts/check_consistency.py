#!/usr/bin/env python3
"""Cross-document consistency check for the labs and the pages that describe them.

The validators (okf_validate, site_lint, check_site) check structure; none of
them notices when two documents disagree. This script checks that they agree:

  1. Submission filenames: each lab notebook (learner and instructor copies),
     its activities page and the labs page all name ModuleN_Lab_[YourName].ipynb.
  2. Time budgets: the labs-page table and each notebook header match the
     activities page's guided-lab and project estimates.
  3. Learning-objective labels: the Module 4 and 5 notebooks cite the
     objectives their overview's checklist maps to the lab and project.
  4. Provider defaults: each notebook's PROVIDER line, its prose and the labs
     page agree.
  5. Lab contents: the pages describe the tools, sections and title the
     notebooks actually have.
  6. Module 1 no longer says learners operate Claude Desktop, and the Module 2
     lesson and reading guide list the same six trade-off dimensions.
  7. Answer keys: 25 collapsibles per quiz page, and feedback for every option
     of all 125 questions.

Several expectations encode decisions recorded on
docs/course-design/instructor-materials.md (2026-09-11). When an author changes
one on purpose, update the check in the same commit. Not run in CI.

Usage: python3 scripts/check_consistency.py
Exit code 1 if any check fails.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "docs"
fails = 0


def check(label, ok, detail=""):
    global fails
    fails += not ok
    print(("PASS " if ok else "FAIL ") + label + (f"  [{detail}]" if detail and not ok else ""))


def md(nbpath):
    nb = json.loads((ROOT / nbpath).read_text())
    return "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown")


def code(nbpath):
    nb = json.loads((ROOT / nbpath).read_text())
    return "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")


NB = {2: "docs/materials/module2/Module-2-Guided-Lab-Notebook.ipynb", 3: "docs/materials/module3/Module-3-Lab.ipynb",
      4: "docs/materials/module4/Module4_Learner_Starter.ipynb", 5: "docs/materials/module5/Module5_Learner_Starter.ipynb"}
INB = {4: "instructor/materials/module4/Module4_Instructor_Solution.ipynb",
       5: "instructor/materials/module5/Module5_Instructor_Solution.ipynb"}
labs = (D / "start-here/labs-and-notebooks.md").read_text()
FN = re.compile(r"Module\d_[A-Za-z0-9_]*\[YourName\]\.ipynb")

print("== submission filenames")
for m, nb in NB.items():
    want = {f"Module{m}_Lab_[YourName].ipynb"}
    act = (D / f"modules/module-{m}/activities.md").read_text()
    check(f"M{m} notebook", set(FN.findall(md(nb))) == want, set(FN.findall(md(nb))))
    check(f"M{m} activities page", set(FN.findall(act)) == want, set(FN.findall(act)))
    check(f"M{m} labs-page list", f"`Module{m}_Lab_[YourName].ipynb`" in labs)
    if m in INB:
        check(f"M{m} instructor notebook", set(FN.findall(md(INB[m]))) == want, set(FN.findall(md(INB[m]))))

print("== time budgets (activities page is the reference)")
H = re.compile(r"~\s*(\d+)\s*(hrs?|hours?|minutes|min)\b")


def hours(s):
    n, u = H.search(s).groups()
    return int(n) / 60 if u.startswith("min") else int(n)


for m, nb in NB.items():
    act = (D / f"modules/module-{m}/activities.md").read_text()
    lab = re.search(r"^## (?:Guided )?Lab.*?\n\n\*Estimated time: ([^*]+)\*", act, re.M | re.S | re.I)
    proj = re.search(r"^## Hands-[Oo]n Project.*?\n\n\*Estimated time: ([^*]+)\*", act, re.M | re.S)
    lh, ph = hours(lab.group(1)), hours(proj.group(1))
    unit = lambda h: f"~{h:g} hour" + ("s" if h != 1 else "")
    row = next(l for l in labs.split("\n") if l.startswith(f"| {m} | [Module {m} lab]"))
    check(f"M{m} labs table = lab {lh:g}h + project {ph:g}h", f"Lab {unit(lh)}, project {unit(ph)}" in row, row[-60:])
    head = "".join(json.loads((ROOT / nb).read_text())["cells"][0]["source"])
    tline = next(l for l in head.split("\n") if re.search(r"time", l, re.I))
    nums = [int(x) for x in re.findall(r"(\d+) hours?", tline)]
    if m == 2:
        ok = nums == [int(lh), int(ph)]
    elif m == 3:
        ok = nums == [2, 2]
    else:
        ok = nums == [int(lh + ph), int(lh), int(ph)] or (m == 5 and "about 1 hour" in tline and nums == [3, 2])
    check(f"M{m} notebook header time", ok, tline)

print("== learning-objective labels vs overview checklist")
for m, want in ((4, "**2, 3 and 4** in the Module 4 overview"), (5, "**2 and 3** in the Module 5 overview")):
    ov = (D / f"modules/module-{m}/overview.md").read_text()
    los = set()
    for kind in ("Lab", "Project"):
        r = re.search(rf"^\| \*\*{kind}\*\* \|[^|]*\| LO ([\d, ]+) \|", ov, re.M).group(1)
        los |= {int(x) for x in r.replace(" ", "").split(",")}
    check(f"M{m} overview maps lab+project to {sorted(los)}", want.startswith("**" + " and ".join(
        [", ".join(map(str, sorted(los)[:-1])), str(sorted(los)[-1])]) + "**"), sorted(los))
    for p in [NB[m], INB[m]]:
        check(f"M{m} {Path(p).name} cites them", want in md(p) and not re.search(r"LO \d\.\d", md(p)))

print("== provider defaults")
for m, prov, phrase in ((4, "huggingface", "Hugging Face Inference Providers (default"), (5, "nvidia", "NVIDIA API (default")):
    c = code(NB[m])
    check(f"M{m} code default is {prov}", f'PROVIDER = "{prov}"' in c)
    row = next(l for l in labs.split("\n") if l.startswith(f"| {m} | Hugging") or l.startswith(f"| {m} | NVIDIA"))
    check(f"M{m} labs provider row", phrase in row, row[:60])
check("M5 notebook prose names NVIDIA as default", "The default is the NVIDIA API" in md(NB[5])
      and "The default is Hugging Face" not in md(NB[5]))
check("labs cost section: HF default only in Module 4", "the default in Module 4 and an option\n  in Module 5" in labs
      and "the default in Modules 4 and 5" not in labs)

print("== notebook content vs activities description")
act5 = (D / "modules/module-5/activities.md").read_text()
check("M5 activities: no webpage-reading tool", "webpage reading" not in act5 and "calculator" in act5)
check("M5 notebook tools are search + calculator", "tools = [search, calculator]" in code(NB[5]))
check("M5 notebook: no CI/CD or regression-suite Lab B",
      not re.search(r"CI/CD|regression|Evaluation Pipeline|Pipeline Report", md(NB[5])), "")
nb4 = md(NB[4])
nb2 = json.loads((ROOT / NB[2]).read_text())
check("M2 notebook has a scaffolded project section before submission",
      [c.get("id") for c in nb2["cells"]].index("project-tool") < [c.get("id") for c in nb2["cells"]].index("submission")
      and "# Hands-On Project — Add Your Own Tool" in md(NB[2]))
check("M4 notebook sections 1-4 exist", all(f"## {i}. " in nb4 for i in range(1, 5)))
check("M4 notebook: no stale Lab A/Lab B labels", not re.search(r"\bLab [AB]\b", nb4),
      re.findall(r".{30}\bLab [AB]\b.{20}", nb4))
stale = [p for p in D.rglob("*.md") if "CI/CD Evaluation Pipeline" in p.read_text()
         and p.name not in ("log.md", "instructor-materials.md")]
check("no page still carries the old Module 5 title", not stale, stale)
check("labs page M3 note describes the download", "downloads them" in labs and "upload cell the notebook" not in labs)

print("== Module 1 and Claude Desktop")
hits = [str(p.relative_to(D)) for p in D.rglob("*.md") if not str(p).startswith(str(D / "archive"))
        and p.name not in ("log.md", "instructor-materials.md", "course-review-2026-07.md")
        and re.search(r"Operate Claude Desktop|operating Claude Desktop|introducing \[?Claude Desktop|"
                      r"Guided Labs: Claude Desktop|interaction with Claude Desktop|no-code automation pipeline using",
                      p.read_text())]
check("no page says learners operate Claude Desktop in the labs", not hits, hits)

print("== Module 2 six dimensions")
fc = (D / "modules/module-2/foundational-concepts.md").read_text()
rg = (D / "modules/module-2/reading-guides.md").read_text()
table = re.findall(r"^\| \*\*([^*]+)\*\* \|", fc.split("The Six-Dimension Trade-off Assessment Framework")[1].split("\n\n", 2)[1], re.M)
guide = re.findall(r"^\s+\d\. \*([^*]+)\*", rg.split("Six assessment dimensions")[1].split("- **Multi-objective")[0], re.M)
check("lesson table dimensions == reading guide dimensions", [t.lower() for t in table] == [g.lower() for g in guide],
      (table, guide))

print("== quiz keys")
total = 0
for m in range(1, 6):
    t = (D / f"modules/module-{m}/chapter-quizzes.md").read_text()
    n = t.count('??? success "Show answer and feedback"')
    check(f"M{m} has 25 answer collapsibles", n == 25, n)
    for ch in re.split(r"(?m)^## .*\{ #chapter-\d+-quiz \}", t)[1:]:
        for q in re.split(r"(?m)^### Question [\d.]+.*$", ch)[1:]:
            stem, _, key = q.partition("??? success")
            opts = set(re.findall(r"(?m)^\s*(?:[-*]\s*)?\**([A-D])[.)]\**\s", stem))
            fb = set(re.findall(r"\*\*([A-D])\b", key))
            total += 1
            if not opts or opts - fb:
                check(f"M{m} question with options {sorted(opts)} has feedback for each", False, sorted(fb))
check(f"all {total} questions have feedback for every option", total == 125, total)
partly = [f"M{m}: {l.strip()[:60]}" for m in range(1, 6)
          for l in (D / f"modules/module-{m}/chapter-quizzes.md").read_text().split("\n")
          if l.strip().startswith("❌") and re.match(r"❌ \*\*[A-D] is partially", l.strip())]
check("no option is marked wrong while its feedback calls it partially right", not partly, partly)
q2 = (D / "modules/module-2/chapter-quizzes.md").read_text()
q1 = re.split(r"(?m)^### Question", q2.split("{ #chapter-5-quiz }")[1])[1]
check("M2 ch5 Q1 keyed B without a pending note",
      "**Correct Answer: B**\n" in q1 and "pending" not in q1 and "B or C" not in q1)

print(f"\n{'ALL CONSISTENT' if not fails else f'{fails} FAILURE(S)'}")
raise SystemExit(1 if fails else 0)
