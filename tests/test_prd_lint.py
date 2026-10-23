"""Planning checks must find moved Parts and reject genuinely broken links."""

import subprocess
import sys
from pathlib import Path

import pytest

from tools.prd_lint import local_link_errors


LINTER = Path(__file__).resolve().parents[1] / "tools" / "prd_lint.py"


def test_docs_subfolder_is_not_mistaken_for_legacy_planning_root(tmp_path):
    folder = tmp_path / "docs" / "architecture"
    folder.mkdir(parents=True)
    (folder / "part-01-design.md").write_text("# Design\n")
    (folder.parent / "part-02-other.md").write_text("[Broken](missing.md)\n")
    result = run_linter(folder)
    assert result.returncode == 0 and "Checked 1 file(s)." in result.stdout


@pytest.mark.parametrize("target", ["README.md", "AGENTS.md"])
def test_document_root_audits_external_entrypoints(tmp_path, target):
    docs=tmp_path / "docs"
    docs.mkdir()
    (docs / "part-01-design.md").write_text("# Design\n")
    entry=tmp_path / target
    entry.parent.mkdir(exist_ok=True)
    entry.write_text("[Broken](missing.md)\n")
    result=run_linter(docs)
    assert result.returncode == 1 and str(entry) in result.stdout


@pytest.mark.parametrize("text,warning", [
    ("# SK-01\n📚 Learn first\n↩ Return\n",False),
    ("# SK-01\n📚 Learn first\n↩ Return\n# SK-01\n📚 Learn first\n↩ Return\n",True),
    ("# Skills overview\n",False),
])
def test_skill_heading_warnings_are_precise(tmp_path,text,warning):
    (tmp_path / "part-01-design.md").write_text(text)
    result=run_linter(tmp_path)
    assert result.returncode == 0
    assert ("skill SK-01 appears" in result.stdout) is warning


@pytest.mark.parametrize("days,warning", [(1,False),(6,True),(37,False)])
def test_missing_schedule_warning_requires_a_substantial_incomplete_schedule(tmp_path,days,warning):
    (tmp_path / "part-18-sprint1.md").write_text("\n".join(f"## DAY {day} — Scheduled\n📚 Learn first\n↩ Return" for day in range(1,days+1)))
    result=run_linter(tmp_path)
    assert result.returncode == 0
    assert ("missing DAY" in result.stdout) is warning


def test_fenced_day_examples_in_other_parts_do_not_become_schedule_entries(tmp_path):
    (tmp_path / "part-01-design.md").write_text("```text\nDAY 1 — Example\nDAY 1 — Example again\n```\n")
    result=run_linter(tmp_path)
    assert result.returncode == 0 and "DAY 1 appears" not in result.stdout


def test_peer_section_links_cannot_satisfy_a_missing_learn_return_block(tmp_path):
    (tmp_path / "part-01-design.md").write_text("# C-01\nMissing links\n# C-02\n📚 Learn first\n↩ Return\n")
    result=run_linter(tmp_path)
    assert result.returncode == 0
    assert "no 📚 Learn-first block under 'C-01'" in result.stdout
    assert "no ↩ Return line under 'C-01'" in result.stdout
    assert "under 'C-02'" not in result.stdout


@pytest.mark.parametrize("fence", ["```", "~~~", "~~~~"])
def test_links_after_a_closed_fence_are_audited(tmp_path,fence):
    path=tmp_path / "guide.md"
    path.write_text(fence+"text\n[Example](not-real.md)\n"+fence+"\n[Broken](missing.md)\n")
    errors=local_link_errors(path)
    assert len(errors)==1 and ":4 LINK: missing local target missing.md" in errors[0]


@pytest.mark.parametrize("false_closer", ["~~~", "``", "```text"])
def test_incorrect_fence_closers_leave_examples_as_examples(tmp_path,false_closer):
    path=tmp_path / "guide.md"
    path.write_text("```text\n"+false_closer+"\n[Example](missing.md)\n```\n")
    assert local_link_errors(path)==[]
    (tmp_path / "part-01-design.md").write_text("```python\n"+false_closer+"\n"+"pass\n"*15+"```\n")
    result=run_linter(tmp_path)
    assert result.returncode==1 and "R3: 16-line" in result.stdout


def run_linter(folder):
    return subprocess.run([sys.executable, str(LINTER), str(folder)],
                          capture_output=True, text=True, timeout=10)


def test_legacy_folder_finds_topic_parts(tmp_path):
    docs = tmp_path / "docs"
    (docs / "planning").mkdir(parents=True)
    (docs / "architecture").mkdir()
    (docs / "architecture" / "part-01-design.md").write_text("# Design\n")
    result = run_linter(docs / "planning")
    assert result.returncode == 0, result.stdout
    assert "Checked 1 file(s)." in result.stdout


def test_empty_tree_is_not_a_successful_lint(tmp_path):
    result = run_linter(tmp_path)
    assert result.returncode == 1
    assert "No part-*.md files" in result.stdout


@pytest.mark.parametrize("reference", [
    "[Guide](missing.md)", "[guide]: missing.md", '<a href="missing.md">Guide</a>',
])
def test_missing_targets_report_file_and_line(tmp_path, reference):
    path = tmp_path / "guide.md"
    path.write_text(reference + "\n")
    errors = local_link_errors(path)
    assert len(errors) == 1
    assert f"{path}:1 LINK: missing local target missing.md" == errors[0]


def test_valid_relative_encoded_external_and_anchor_links(tmp_path):
    (tmp_path / "target file.md").write_text("# Target\n")
    path = tmp_path / "guide.md"
    path.write_text('[Target](target%20file.md#target)\n[Local](#heading)\n'
                    '[Docs](https://docs.python.org/3/)\n')
    assert local_link_errors(path) == []




def test_broken_guide_link_fails_whole_lint(tmp_path):
    (tmp_path / "part-01-design.md").write_text("# Design\n")
    (tmp_path / "guide.md").write_text("[Missing](missing.md)\n")
    result = run_linter(tmp_path)
    assert result.returncode == 1
    assert "LINK: missing local target missing.md" in result.stdout


def test_long_code_block_still_fails(tmp_path):
    (tmp_path / "part-01-design.md").write_text("```python\n" + "pass\n" * 16 + "```\n")
    result = run_linter(tmp_path)
    assert result.returncode == 1
    assert "R3: 16-line" in result.stdout


def test_duplicate_story_definitions_still_fail(tmp_path):
    for name in ["part-01-design.md", "part-02-design.md"]:
        (tmp_path / name).write_text("# E2-US04\n📚 Learn first\n↩ Return\n")
    result = run_linter(tmp_path)
    assert result.returncode == 1
    assert "story E2-US04 defined 2 times" in result.stdout


def test_day_references_and_checklists_are_not_duplicate_schedule_entries(tmp_path):
    (tmp_path / "part-18-sprint1.md").write_text(
        "## Day 6 — Tuesday — Foundation\n📚 Learn first\n↩ Return\n"
        "### Day 6 checklist — steps\n📚 Learn first\n↩ Return\n")
    (tmp_path / "part-11-schema.md").write_text("## Day 6 — Candidate\n📚 Learn first\n↩ Return\n")
    result = run_linter(tmp_path)
    assert result.returncode == 0, result.stdout
    assert "appears" not in result.stdout


def test_duplicate_primary_schedule_days_still_fail(tmp_path):
    (tmp_path / "part-18-sprint1.md").write_text(
        "## Day 6 — Tuesday — Foundation\n📚 Learn first\n↩ Return\n"
        "## Day 6 — Wednesday — Duplicate\n📚 Learn first\n↩ Return\n")
    result = run_linter(tmp_path)
    assert result.returncode == 1
    assert "DAY 6 appears 2 times" in result.stdout


# Common Markdown forms must not create false broken-link reports.
@pytest.mark.parametrize("reference", [
    "[Target](target.md 'A title')", "[target]: <target file.md>",
])
def test_common_markdown_link_forms_are_valid(tmp_path, reference):
    (tmp_path / "target.md").write_text("# Target\n")
    (tmp_path / "target file.md").write_text("# Target\n")
    path = tmp_path / "guide.md"
    path.write_text(reference + "\n")
    assert local_link_errors(path) == []




@pytest.mark.parametrize("fence", ["```", "~~~", "````"])
def test_all_supported_markdown_fences_enforce_the_code_limit(tmp_path, fence):
    (tmp_path / "part-01-design.md").write_text(fence + "sql\n" + "SELECT 1;\n" * 16 + fence + "\n")
    result = run_linter(tmp_path)
    assert result.returncode == 1
    assert "R3: 16-line" in result.stdout


def test_exactly_fifteen_code_lines_are_allowed(tmp_path):
    (tmp_path / "part-01-design.md").write_text("```python\n" + "pass\n" * 15 + "```\n")
    result = run_linter(tmp_path)
    assert result.returncode == 0, result.stdout


def test_inline_code_example_is_ignored_but_real_link_still_checked(tmp_path):
    path = tmp_path / "guide.md"
    path.write_text('`[Example](ignored.md)` and [Missing](real-missing.md)\n')
    assert local_link_errors(path) == [f"{path}:1 LINK: missing local target real-missing.md"]
