"""Catalog integrity tests."""

from offboarding.tools import PHASES, TOOLS, get_tool, list_slugs


def test_catalog_has_25_tools():
    assert len(TOOLS) == 25, f"expected 25 tools, got {len(TOOLS)}"


def test_slugs_unique_and_lookup_works():
    slugs = list_slugs()
    assert len(set(slugs)) == len(slugs), "duplicate slugs in catalog"
    for slug in slugs:
        tool = get_tool(slug)
        assert tool is not None
        assert tool["name"], f"{slug} has no name"


def test_unknown_slug_returns_none():
    assert get_tool("no-such-tool") is None


def test_all_doc_urls_https():
    for tool in TOOLS:
        url = tool["doc_url"]
        assert url.startswith("https://"), f"{tool['slug']}: doc URL not https: {url}"
        assert tool["doc_title"], f"{tool['slug']}: missing doc title"


def test_all_phases_valid():
    for tool in TOOLS:
        for phase, step in tool["steps"]:
            assert phase in PHASES, f"{tool['slug']}: bad phase {phase!r}"
            assert step.strip(), f"{tool['slug']}: empty step text"


def test_every_tool_has_oauth_step_first_priority():
    for tool in TOOLS:
        phases = [p for (p, _) in tool["steps"]]
        assert "oauth" in phases, f"{tool['slug']}: no OAuth/SSO revocation step"


def test_every_tool_has_at_least_three_steps():
    for tool in TOOLS:
        assert len(tool["steps"]) >= 3, f"{tool['slug']}: fewer than 3 steps"
