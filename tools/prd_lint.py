#!/usr/bin/env python3
"""prd_lint.py: checks planning docs against the master prompt's rules.

Usage:
    python tools/prd_lint.py docs/planning
    python tools/prd_lint.py docs/planning --verify-out docs/planning/VERIFY_LIST.md

Checks (planning docs only, no application code is touched):
  R3   fenced code blocks > 15 lines in programming languages (feature code sneaking in)
  R1   headings for stories / skill cards / components / days with no 📚 or no ↩
  R2   every `🔎 verify` is collected into one list (for the Verify Pass)
  ID   duplicate story IDs (E2-US04) and skill IDs (SK-12) used as headings
  Day  DAY 1..37 present exactly once in schedule files
Exit code 1 if any ERROR is found. Warnings do not fail the run.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

CODE_LANGS = {"python", "py", "ts", "tsx", "typescript", "js", "javascript", "jsx",
              "sql", "java", "go", "cpp", "c", "rust", "yaml", "yml", "toml", "dockerfile"}
MAX_CODE_LINES = 15
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
NEEDS_LINKS = re.compile(r"\b(E\d+-US\d+|SK-\d+|C-\d+(?:\.\d+)?|DAY\s+\d+)\b", re.I)
STORY_ID = re.compile(r"\b(E\d+-US\d+)\b")
SKILL_ID = re.compile(r"\b(SK-\d+)\b")
DAY_HEAD = re.compile(r"^DAY\s+(\d+)\b", re.I)


def lint_file(path, errors, warns, verify, story_ids, skill_ids, days):
    lines = path.read_text(encoding="utf-8").splitlines()
    in_code, lang, start = False, "", 0
    headings = []  # (index, level, text)
    for i, line in enumerate(lines):
        m = re.match(r"^\s*```(\w*)", line)
        if m:
            if not in_code:
                in_code, lang, start = True, m.group(1).lower(), i
            else:
                n = i - start - 1
                if lang in CODE_LANGS and n > MAX_CODE_LINES:
                    errors.append(f"{path}:{start+1} R3: {n}-line `{lang}` block (limit {MAX_CODE_LINES}); "
                                  "specs/hints only unless I asked for it")
                in_code = False
            continue
        if in_code:
            if re.match(r"^DAY\s+\d+", line, re.I):
                d = DAY_HEAD.match(line)
                if d:
                    days[int(d.group(1))].append(f"{path}:{i+1}")
            continue
        if "🔎" in line:
            verify.append((str(path), i + 1, line.strip()))
        h = HEADING.match(line)
        if h:
            headings.append((i, len(h.group(1)), h.group(2)))
            sid = STORY_ID.search(h.group(2))
            if sid:
                story_ids[sid.group(1)].append(f"{path}:{i+1}")
            kid = SKILL_ID.search(h.group(2))
            if kid and h.group(2).lower().startswith(("sk-", "skill")):
                skill_ids[kid.group(1)].append(f"{path}:{i+1}")
            d = DAY_HEAD.match(h.group(2))
            if d:
                days[int(d.group(1))].append(f"{path}:{i+1}")
    # R1: sections that need 📚 and ↩
    for idx, (i, level, text) in enumerate(headings):
        if not NEEDS_LINKS.search(text):
            continue
        end = len(lines)
        for j, lvl, _ in headings[idx + 1:]:
            if lvl <= level:
                end = j
                break
        body = "\n".join(lines[i + 1:end])
        if "📚" not in body:
            warns.append(f"{path}:{i+1} R1: no 📚 Learn-first block under '{text[:60]}'")
        if "↩" not in body:
            warns.append(f"{path}:{i+1} R1: no ↩ Return line under '{text[:60]}'")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--verify-out")
    a = ap.parse_args()
    folder = Path(a.folder)
    files = sorted(folder.glob("part-*.md"))
    if not files:
        print(f"No part-*.md files in {folder}")
        return 1
    errors, warns, verify = [], [], []
    story_ids, skill_ids = {}, {}
    from collections import defaultdict
    story_ids, skill_ids, days = defaultdict(list), defaultdict(list), defaultdict(list)
    for f in files:
        lint_file(f, errors, warns, verify, story_ids, skill_ids, days)
    for k, v in story_ids.items():
        if len(v) > 1:
            errors.append(f"ID: story {k} defined {len(v)} times: {', '.join(v)}")
    for k, v in skill_ids.items():
        if len(v) > 1:
            warns.append(f"ID: skill {k} appears as a heading {len(v)} times: {', '.join(v)}")
    if days:
        missing = [d for d in range(1, 38) if d not in days]
        dupes = {d: v for d, v in days.items() if len(v) > 1}
        if missing and len(days) > 5:
            warns.append(f"Day: missing DAY {missing} (fine if those Parts are not written yet)")
        for d, v in dupes.items():
            errors.append(f"Day: DAY {d} appears {len(v)} times: {', '.join(v)}")
    print(f"Checked {len(files)} file(s).")
    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    print(f"{len(errors)} error(s), {len(warns)} warning(s), {len(verify)} verify item(s).")
    if a.verify_out:
        out = ["# 🔎 Verify list (generated)\n", "Run the Verify Pass prompt on this list.\n"]
        for f, n, t in verify:
            out.append(f"- `{f}:{n}` {t}")
        Path(a.verify_out).write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"Wrote {a.verify_out}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
