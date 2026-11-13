# SPDX-License-Identifier: GPL-3.0-only
# Part of LEM. See the accompanying LICENSE for license terms and warranty disclaimer.

# Workspace tool: default read-only comparison; --write publishes canonical Common/shared snapshots.
# Requires sibling App and Server roots. Never deletes unexpected files; nonzero means review is needed.
# Writes are not transactional across repositories: inspect all diffs after an interrupted/failed --write.
# See docs/workspace.md for the coordinated review workflow.

from pathlib import Path
import argparse, hashlib, shutil, sys

common = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(
    description="Check or publish Common/shared snapshots to App and Server."
)
parser.add_argument(
    "--write",
    action="store_true",
    help="Explicitly update tracked shared snapshots; default is read-only verification.",
)
args = parser.parse_args()
changes = []
for repo in ("App", "Server"):
    target = common.parent / repo / "shared"
    if not target.parent.is_dir():
        raise SystemExit(f"Missing sibling repository: {target.parent}")
    source = common / "shared"
    for p in sorted(source.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(source)
        dst = target / rel
        if not dst.exists() or p.read_bytes() != dst.read_bytes():
            changes.append(f"{repo}/shared/{rel.as_posix()}")
            if args.write:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(p, dst)
    for p in sorted(target.rglob("*")):
        if p.is_file() and not (source / p.relative_to(target)).exists():
            raise SystemExit(
                f"Extra shared file requires manual review (never deleted automatically): {p}"
            )
print(("Updated" if args.write else "Differences") + f": {len(changes)}")
for change in changes:
    print(change)
if changes and not args.write:
    sys.exit(1)
