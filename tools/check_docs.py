#!/usr/bin/env python3
"""Check local Markdown links in the maintained LEM documentation.

Run from ongoing_work: python ../Common/tools/check_docs.py
Use --repo App (repeatable) to narrow the documents, or --workspace PATH to
check another sibling-repository workspace. Uses only the standard library.
It reads files without modifying them or fetching external URLs. Exit 0 means
all checked local links resolve; exit 1 means a missing file/heading was found.
"""

import argparse
from collections import Counter
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

REPOSITORIES = ("App", "Server", "Common")
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")


def prose(text):
    """Remove fenced code while keeping newlines for useful error locations."""
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            symbol = marker.group(1)[0]
            if fence is None:
                fence = symbol
            elif fence == symbol:
                fence = None
            lines.append("")
        else:
            lines.append(line if fence is None else "")
    return "\n".join(lines)


def anchors(text):
    """Return common GitHub-style ATX heading IDs, including duplicate suffixes."""
    result = set()
    counts = Counter()
    for line in prose(text).splitlines():
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        title = match.group(1).lower().replace("`", "")
        title = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
        count = counts[title]
        counts[title] += 1
        result.add(title if count == 0 else f"{title}-{count}")
    return result


def documents(root):
    """Scope the check to maintained guides, not caches or temporary test output."""
    selected = [root / "README.md", root / "AGENTS.md", root / "app/assets/README.md"]
    selected.extend((root / "docs").rglob("*.md"))
    selected.extend((root / "deploy").glob("*.md"))
    return sorted({path for path in selected if path.is_file()})


def check_document(path):
    """Yield line-numbered failures for relative file and Markdown heading links."""
    content = prose(path.read_text(encoding="utf-8-sig"))
    for match in LINK.finditer(content):
        raw = match.group(1).strip()
        # Optional Markdown link titles are intentionally outside this small checker.
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc:
            continue
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        line = content.count("\n", 0, match.start()) + 1
        if not target.exists():
            yield f"{path}:{line}: missing file: {raw}"
        elif parsed.fragment and target.suffix.lower() == ".md":
            fragment = unquote(parsed.fragment)
            if fragment not in anchors(target.read_text(encoding="utf-8-sig")):
                yield f"{path}:{line}: missing heading: {raw}"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace", type=Path, default=Path(__file__).resolve().parents[2]
    )
    parser.add_argument("--repo", action="append", choices=REPOSITORIES)
    args = parser.parse_args(argv)
    failures = []
    checked = 0
    for name in dict.fromkeys(args.repo or REPOSITORIES):
        root = args.workspace / name
        if not root.is_dir():
            failures.append(f"Missing repository directory: {root}")
            continue
        for path in documents(root):
            checked += 1
            try:
                failures.extend(check_document(path))
            except (OSError, UnicodeError, ValueError) as error:
                failures.append(f"{path}: cannot validate documentation: {error}")
    for failure in failures:
        print(failure, file=sys.stderr)
    print(f"Checked {checked} Markdown files; {len(failures)} failures.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
