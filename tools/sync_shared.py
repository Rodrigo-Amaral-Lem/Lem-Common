# SPDX-License-Identifier: GPL-3.0-only
# Part of LEM. See the accompanying LICENSE for license terms and warranty disclaimer.

# Compare each sibling snapshot with Common/shared. With --write, files are
# copied as differences are found. An interruption can leave earlier copies in
# place. See docs/workspace.md for the review procedure.

import argparse
from pathlib import Path
import shutil
import sys

common_root = Path(__file__).resolve().parents[1]
source_root = common_root / "shared"
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

for repo_name in ("App", "Server"):
    snapshot_root = common_root.parent / repo_name / "shared"
    if not snapshot_root.parent.is_dir():
        raise SystemExit(f"Missing sibling repository: {snapshot_root.parent}")

    for source_file in sorted(source_root.rglob("*")):
        if not source_file.is_file():
            continue
        relative_path = source_file.relative_to(source_root)
        snapshot_file = snapshot_root / relative_path
        if snapshot_file.exists() and source_file.read_bytes() == snapshot_file.read_bytes():
            continue
        changes.append(f"{repo_name}/shared/{relative_path.as_posix()}")
        if args.write:
            snapshot_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_file, snapshot_file)

    for snapshot_file in sorted(snapshot_root.rglob("*")):
        if not snapshot_file.is_file():
            continue
        relative_path = snapshot_file.relative_to(snapshot_root)
        if not (source_root / relative_path).exists():
            raise SystemExit(
                f"Extra shared file requires manual review (never deleted automatically): {snapshot_file}"
            )

print(("Updated" if args.write else "Differences") + f": {len(changes)}")
for change in changes:
    print(change)
if changes and not args.write:
    sys.exit(1)
