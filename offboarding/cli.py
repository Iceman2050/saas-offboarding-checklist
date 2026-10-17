"""CLI for saas-offboarding-checklist."""

import argparse
import sys

from . import __version__
from .runbook import build_runbook, parse_custom
from .tools import TOOLS, get_tool, list_slugs

DEMO_EMPLOYEE = "Alex Rivera"
DEMO_EMAIL = "alex.rivera@example.com"
DEMO_TOOLS = [
    "google-workspace",
    "okta",
    "github",
    "aws",
    "slack",
    "stripe",
    "notion",
    "1password",
]


def build_parser():
    p = argparse.ArgumentParser(
        prog="offboarding",
        description="Generate an ordered SaaS access-revocation runbook for a departing employee.",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("--employee", help="Departing employee's full name")
    p.add_argument("--email", default="", help="Departing employee's work email")
    p.add_argument(
        "--tools",
        help="Comma-separated tool slugs (see --list), or 'all' for the full catalog",
    )
    p.add_argument(
        "--custom",
        action="append",
        default=[],
        metavar="'Name|phase|Step text'",
        help="Add a custom tool step; repeatable. Phase: oauth, apikeys, shared, data",
    )
    p.add_argument("--out", help="Write the runbook to a markdown file (default: stdout)")
    p.add_argument("--list", action="store_true", help="List catalog tool slugs and exit")
    p.add_argument("--demo", action="store_true", help="Run the 30-second sample demo")
    p.add_argument(
        "--generated-date",
        default=None,
        help="Override the 'Generated' date (default: today)",
    )
    return p


def resolve_tools(tool_arg, custom_specs):
    tools = []
    if tool_arg:
        if tool_arg.strip().lower() == "all":
            slugs = list_slugs()
        else:
            slugs = [s.strip().lower() for s in tool_arg.split(",") if s.strip()]
        for slug in slugs:
            tool = get_tool(slug)
            if tool is None:
                raise SystemExit(
                    f"error: unknown tool {slug!r}; run with --list to see the catalog"
                )
            tools.append(tool)
    for spec in custom_specs:
        try:
            tools.append(parse_custom(spec))
        except ValueError as e:
            raise SystemExit(f"error: {e}")
    return tools


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        for tool in TOOLS:
            print(f"{tool['slug']:20} {tool['name']}")
        return 0

    if args.demo:
        employee = DEMO_EMPLOYEE
        email = DEMO_EMAIL
        tools = [get_tool(s) for s in DEMO_TOOLS]
    else:
        if not args.employee:
            parser.error("--employee is required (or use --demo / --list)")
        if not args.tools and not args.custom:
            parser.error("give --tools and/or --custom (or use --demo)")
        employee = args.employee
        email = args.email
        tools = resolve_tools(args.tools, args.custom)

    runbook = build_runbook(employee, email, tools, generated=args.generated_date)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(runbook)
        print(f"Wrote {args.out} ({len(tools)} tools)")
    else:
        sys.stdout.write(runbook)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
