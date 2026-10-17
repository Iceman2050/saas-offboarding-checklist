"""Runbook generation tests."""

from offboarding.runbook import build_runbook, parse_custom
from offboarding.tools import get_tool


def sample_tools():
    return [get_tool("github"), get_tool("slack")]


def test_phases_in_required_order():
    md = build_runbook("Jane Doe", "jane@example.com", sample_tools(), generated="2026-10-17")
    i_oauth = md.index("## Revoke OAuth grants & SSO sessions (do first)")
    i_keys = md.index("## Revoke API keys & tokens")
    i_shared = md.index("## Rotate shared credentials")
    i_data = md.index("## Transfer / export data")
    assert i_oauth < i_keys < i_shared < i_data, "phases out of order"


def test_checkboxes_and_vendor_links_present():
    md = build_runbook("Jane Doe", "", sample_tools(), generated="2026-10-17")
    assert "- [ ]" in md, "no checkbox steps"
    assert "Vendor how-to:" in md
    assert "https://docs.github.com/" in md
    assert "### GitHub" in md
    assert "### Slack" in md


def test_header_summary_counts():
    tools = sample_tools()
    md = build_runbook("Jane Doe", "jane@example.com", tools, generated="2026-10-17")
    total = sum(len(t["steps"]) for t in tools)
    assert md.startswith("# Offboarding runbook - Jane Doe")
    assert f"{len(tools)} tools, {total} steps" in md
    assert "Generated 2026-10-17" in md
    assert "jane@example.com" in md


def test_tools_without_steps_in_a_phase_are_skipped():
    # GitHub has no data-phase step; its section must not appear under data
    md = build_runbook("Jane Doe", "", [get_tool("github")], generated="2026-10-17")
    data_section = md.split("## Transfer / export data")[1]
    assert "### GitHub" not in data_section


def test_parse_custom_valid():
    tool = parse_custom("Acme CRM|apikeys|Revoke the user's API token in Settings")
    assert tool["name"] == "Acme CRM"
    assert tool["steps"] == [("apikeys", "Revoke the user's API token in Settings")]
    assert tool["doc_url"] == ""


def test_parse_custom_bad_phase_rejected():
    try:
        parse_custom("Acme CRM|nonsense|Do a thing")
    except ValueError:
        pass
    else:
        raise AssertionError("bad phase accepted")


def test_parse_custom_malformed_rejected():
    for bad in ("NoPipes", "Only|two", "|oauth|empty name", "Name|oauth|"):
        try:
            parse_custom(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"malformed spec accepted: {bad!r}")


def test_deterministic_output():
    a = build_runbook("Jane Doe", "", sample_tools(), generated="2026-10-17")
    b = build_runbook("Jane Doe", "", sample_tools(), generated="2026-10-17")
    assert a == b
