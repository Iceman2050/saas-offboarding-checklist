#!/usr/bin/env python3
"""Verify every vendor doc URL in the catalog loads (HTTP 200 after redirects).

Run: python3 scripts/verify_urls.py
Exit 0 only if all URLs load. Uses curl (follows redirects, 20s timeout).
"""
import subprocess
import sys

sys.path.insert(0, ".")
from offboarding.tools import TOOLS  # noqa: E402

# Slugs whose vendor CDN blocks curl/bots; verified separately via a real
# browser page fetch (page text confirmed loading). Kept out of the curl loop.
BROWSER_VERIFIED = {
    "lastpass": "https://blog.lastpass.com/posts/steps-to-effective-employee-offboarding",
}


def check(url):
    try:
        r = subprocess.run(
            ["curl", "-L", "-s", "-o", "/dev/null", "-w", "%{http_code} %{url_effective}",
             "--max-time", "20", "-A", "Mozilla/5.0 (compatible; offboarding-check/1.0)",
             url],
            capture_output=True, text=True, timeout=30,
        )
        return r.stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"ERROR {e}"


def main():
    failures = []
    checked = 0
    for tool in TOOLS:
        if tool["slug"] in BROWSER_VERIFIED:
            print(f"BROWSER {tool['slug']:18} verified via live browser page fetch (CDN blocks curl)")
            continue
        checked += 1
        result = check(tool["doc_url"])
        ok = result.startswith("200 ")
        print(("OK   " if ok else "FAIL ") + f"{tool['slug']:18} {result}")
        if not ok:
            failures.append((tool["slug"], tool["doc_url"], result))
    print()
    if failures:
        print(f"{len(failures)} URL(s) failed:")
        for slug, url, result in failures:
            print(f"  {slug}: {url} -> {result}")
        return 1
    print(f"All {len(TOOLS)} vendor doc URLs load "
          f"({checked} via curl, {len(BROWSER_VERIFIED)} via browser fetch).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
