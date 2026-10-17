"""CLI tests."""

import pytest

from offboarding.cli import main


def test_list_exits_zero(capsys):
    assert main(["--list"]) == 0
    out = capsys.readouterr().out
    assert "github" in out
    assert "google-workspace" in out


def test_demo_produces_runbook(capsys):
    assert main(["--demo", "--generated-date", "2026-10-17"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("# Offboarding runbook - Alex Rivera")
    assert "## Revoke OAuth grants & SSO sessions (do first)" in out
    assert "- [ ]" in out


def test_unknown_tool_errors():
    with pytest.raises(SystemExit) as exc:
        main(["--employee", "Jane", "--tools", "nope-not-real"])
    assert exc.value.code != 0


def test_missing_employee_errors():
    with pytest.raises(SystemExit):
        main(["--tools", "github"])


def test_out_writes_file(tmp_path):
    dest = tmp_path / "runbook.md"
    assert main(["--employee", "Jane Doe", "--tools", "github,slack",
                 "--out", str(dest), "--generated-date", "2026-10-17"]) == 0
    text = dest.read_text(encoding="utf-8")
    assert "# Offboarding runbook - Jane Doe" in text


def test_custom_tool_included(capsys):
    assert main(["--employee", "Jane Doe",
                 "--custom", "Acme CRM|oauth|Disable the user in Acme admin",
                 "--generated-date", "2026-10-17"]) == 0
    out = capsys.readouterr().out
    assert "### Acme CRM" in out
    assert "Disable the user in Acme admin" in out
