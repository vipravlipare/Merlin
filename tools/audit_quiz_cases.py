"""Run the actual quiz cases against isolated faulty copies of the HTML script."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def faults():
    return [
        ("script-syntax-error", "render();if(submitted)showResults(false);", "render(;if(submitted)showResults(false);"),
        ("bank-duplicate-id", '"id": 2,', '"id": 1,'),
        ("critical-question-15-ignored", "if(q.critical)", "if(q.critical&&id!==15)"),
        ("critical-question-17-ignored", "if(q.critical)", "if(q.critical&&id!==17)"),
        ("critical-question-21-ignored", "if(q.critical)", "if(q.critical&&id!==21)"),
        ("answers-always-wrong", "answers[id]===q.correct", "false"),
        ("answers-always-correct", "answers[id]===q.correct", "true"),
        ("threshold-too-strict", "correct/ids.length>=.8", "correct/ids.length>.8"),
        ("threshold-too-permissive", "correct/ids.length>=.8", "correct/ids.length>=.7"),
        ("critical-errors-ignored", "criticalMissed.length===0", "true"),
        ("invalid-answers-accepted", "!Number.isInteger(answers[id])||answers[id]<0||answers[id]>3", "false"),
        ("negative-answer-accepted", "answers[id]<0", "false"),
        ("too-large-answer-accepted", "answers[id]>3", "false"),
        ("integer-check-removed", "!Number.isInteger(answers[id])", "false"),
        ("empty-attempt-passes", "ids.length>0&&missing.length===0&&correct/ids.length>=.8&&criticalMissed.length===0", "ids.length===0||(ids.length>0&&missing.length===0&&correct/ids.length>=.8&&criticalMissed.length===0)"),
        ("unknown-question-ignored", "if(!q)throw new Error('Unknown question');", "if(!q)continue;"),
        ("full-bank-denominator", "total:ids.length", "total:QUESTIONS.length"),
        ("caller-answers-overwritten", "const ok=answers[id]===q.correct;", "answers[id]=q.correct;const ok=answers[id]===q.correct;"),
        ("topic-totals-not-counted", "topics[q.topic].total++", "topics[q.topic].total+=0"),
        ("topic-correct-not-counted", "topics[q.topic].correct+=ok?1:0", "topics[q.topic].correct+=0"),
        ("saved-states-all-rejected", "function validSaved(saved){", "function validSaved(saved){return false;"),
        ("saved-states-all-accepted", "function validSaved(saved){", "function validSaved(saved){return true;"),
        ("empty-ids-accepted", "!saved.ids.length", "false"),
        ("duplicate-ids-accepted", "new Set(saved.ids).size!==saved.ids.length", "false"),
        ("unknown-ids-accepted", "saved.ids.some(id=>!ids.has(id))", "false"),
        ("answers-not-required", "!saved.answers||typeof saved.answers!=='object'||Array.isArray(saved.answers)", "false"),
        ("answer-arrays-accepted", "Array.isArray(saved.answers)", "false"),
        ("order-not-required", "!saved.order||typeof saved.order!=='object'", "false"),
        ("permutation-length-ignored", "saved.order[id].length===4", "true"),
        ("permutation-duplicates-ignored", "new Set(saved.order[id]).size===4", "true"),
        ("permutation-bounds-ignored", "saved.order[id].every(v=>Number.isInteger(v)&&v>=0&&v<=3)", "saved.order[id].every(v=>Number.isInteger(v))"),
        ("permutation-integers-ignored", "saved.order[id].every(v=>Number.isInteger(v)&&v>=0&&v<=3)", "saved.order[id].every(v=>v>=0&&v<=3)"),
        ("saved-answer-types-ignored", "Object.values(saved.answers).every(v=>Number.isInteger(v)&&v>=0&&v<=3)", "true"),
        ("partial-submitted-cache-accepted", "if(saved.submitted===true&&saved.ids.some(id=>!Object.hasOwn(saved.answers,id)))return false;", ""),
        ("shuffle-disabled", "const j=Math.floor(random()*(i+1))", "const j=i"),
        ("shuffle-loses-choice", "return a;}", "return [0,0,2,3];}"),
        ("partial-saved-state-modified", "return saved.ids.every", "saved.answers[1]=3;return saved.ids.every"),
    ]


def execute(name, html, directory, test_source):
    folder = Path(directory) / name
    (folder / "tests").mkdir(parents=True)
    (folder / "quizzes").mkdir()
    (folder / "package.json").write_text('{"type":"module"}')
    (folder / "tests/quiz.test.js").write_text(test_source)
    (folder / "quizzes/sprint-0-quiz.html").write_text(html)
    try:
        result = subprocess.run(["node", "--test", "--test-isolation=none", "--test-reporter=tap", str(folder / "tests/quiz.test.js")],
                                capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return {"fault": name, "status": "TIMEOUT", "cases": {}}
    cases = {match[1]: "failed" if match[0].startswith("not") else "passed"
             for match in re.findall(r"^(not ok|ok) \d+ - (.+)$", result.stdout, re.M)}
    return {"fault": name, "status": "DETECTED" if result.returncode else "SURVIVED", "cases": cases,
            "output": result.stdout, "stderr": result.stderr}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    html = (ROOT / "quizzes/sprint-0-quiz.html").read_text()
    test_source = (ROOT / "tests/quiz.test.js").read_text()
    with tempfile.TemporaryDirectory(prefix="merlin-quiz-audit-") as directory:
        baseline = execute("baseline", html, directory, test_source)
        if baseline["status"] != "SURVIVED" or not baseline["cases"]:
            raise RuntimeError("Quiz baseline failed")
        rows, prepared = [], []
        for name, old, new in faults():
            if old not in html:
                rows.append({"fault": name, "status": "UNAPPLIED", "cases": {}})
            else:
                prepared.append((name, html.replace(old, new)))
        with ThreadPoolExecutor(max_workers=3) as pool:
            rows.extend(pool.map(lambda row: execute(*row, directory, test_source), prepared))
        for row in rows:
            if row["status"] in {"DETECTED", "SURVIVED"} and set(row["cases"]) != set(baseline["cases"]):
                row["status"] = "INVALID"
        matrix = [{"case": name, "baseline": outcome,
                   "detects": [row["fault"] for row in rows if row["status"] == "DETECTED" and row["cases"].get(name) == "failed"]}
                  for name, outcome in baseline["cases"].items()]
        args.out.write_text(json.dumps({"source_sha256": {file: hashlib.sha256((ROOT/file).read_bytes()).hexdigest()
                                                       for file in ["quizzes/sprint-0-quiz.html", "tests/quiz.test.js"]},
                                       "baseline": baseline, "faults": rows, "matrix": matrix}, indent=2) + "\n")
        print(json.dumps({"cases": len(matrix), "demonstrated": sum(bool(row["detects"]) for row in matrix),
                          "faults": {status: sum(row["status"] == status for row in rows)
                                     for status in ["DETECTED", "SURVIVED", "INVALID", "UNAPPLIED", "TIMEOUT"]}}))


if __name__ == "__main__":
    main()
