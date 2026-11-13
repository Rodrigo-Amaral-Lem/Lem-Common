# Maintenance and common tools

Run workstation commands from `ongoing_work`. Keep outputs and detailed review/test evidence there.
The current documentation is one README plus four focused guides per repository; update these files
rather than adding a document for each patch.

## Common tool catalogue

| Tool | Inputs and prerequisites | Output / side effects |
| --- | --- | --- |
| [sync_shared.py](../tools/sync_shared.py) | Python standard library; sibling App/Server repositories | Default read-only byte comparison of Common/shared against both tracked snapshots; exit 1 for differences |
| `sync_shared.py --write` | Intentional canonical resource update | Copies changed/missing files into snapshots; never deletes unexpected files; not an atomic cross-repository transaction |
| [check_docs.py](../tools/check_docs.py) | Python standard library; selected repositories under the workspace | Read-only validation of local Markdown file/anchor links; prints failures and exits nonzero; no internet/link fetching |
| [check_readability.py](../tools/check_readability.py) | Python plus Pygments, original ZIP and a matching reconstructed source tree | Historical structural-comparison report for comment/format-only work; nonzero if executable structure differs |

```powershell
python ../Common/tools/sync_shared.py
python ../Common/tools/check_docs.py
python ../Common/tools/check_docs.py --repo App --repo Common
python -m unittest discover -s ../Common/tools/tests -v
```

`check_docs.py` defaults to App, Server and Common under the workspace containing its repository.
`--workspace PATH` selects another workspace. It checks relative file links and Markdown heading
anchors; it does not prove a command is safe/correct, check external URLs or validate arbitrary HTML
rendering. A missing sibling link fails even if only one repository was selected.

The legacy readability tool expects ZIP entries under one top-level package directory and source
paths with the old inner `app/`, `server/` structure. Its default `--source` is Common's root,
which is **not** a reconstructed monorepository. To use it, explicitly assemble/select a matching
tree under `ongoing_work` and pass `--source`; do not interpret missing current-split paths as an
application defect. Functional changes should fail that comparison by design. It is not a
replacement for tests or Git review.

## Documentation and comments

Each guide should answer a distinct question, link to the owner of a cross-component rule, and
describe the current implementation. Keep field labels in Portuguese when quoting the UI, with
consistent English explanations. State the working directory, prerequisites, output paths and
mutations alongside a command. Mark deployment/internal helpers and destructive options explicitly
rather than hiding them among routine examples.

Source comments should explain ownership, durability boundaries, ordering constraints and
non-obvious limitations. Avoid historical changelog paragraphs inside functions or assertions that a
test run proves universal correctness. Command scripts should state their inputs, side effects and
public/internal status near the entry point.

Before staging documentation:

1. Verify the described flags/paths in source, including script defaults and outputs.
2. Run shared-snapshot and local-link checks.
3. Check Markdown headings, tables, fenced commands and UTF-8 text.
4. Review source edits for comment/format-only scope; an updated diagnostic documentation path is
   not a functional algorithm change.
5. Keep per-run artifacts under `ongoing_work`, then inspect the staged diff in each repository.
6. Stop at staging when review was requested. Do not commit just because checks passed.

## Test coordination and formatting

Use the [App test guide](../../App/docs/testing.md) for native/QML/network runners and the
[Server test guide](../../Server/docs/testing.md) for API/deployment fixtures. A client mock test
does not establish disk/network correctness; SQLite tests do not establish PostgreSQL locking
behavior; offscreen desktop tests do not replace Android hardware validation.

The projects retain [pyproject.toml](../pyproject.toml) with Black settings, and App has
[.clang-format](../../App/.clang-format). For a formatting-only task, use the relevant tool on the
selected files and compare executable structure. Do not reformat all production source during an
unrelated documentation edit.

Examples, when those optional developer tools are installed:

```powershell
python -m black ../Common/tools/sync_shared.py
clang-format -i ../App/app/src/Checklist.h
```

QML can be formatted with the matching Qt `qmlformat` without import sorting/attribute
normalization. Formatting tools are development dependencies, not application runtime requirements.

## Release and contract changes

App/CMake declarations, `app/src/main.cpp`, Android version name/code, Server's compatibility
policy, Compose image tag and installer/environment policy defaults must be considered together.
`test_release_alignment.py` checks the current client/server declarations when both repositories are
available. Compatibility admits versions from minimum through latest, including both bounds;
newer-than-latest clients are not assumed compatible.

A shared template change also needs synchronized snapshots, connector/measurement case review and a
deliberate choice about existing drafts versus closed history. Current editable-v6 corrections are
explicit functions in both components; do not assume every future template addition automatically
migrates all reports.

Review the three Git diffs as a coordinated release, but keep component responsibilities separate.
Deployment transport ZIPs are temporary payloads, not the source-of-truth workflow. No Git remote,
APK, portable EXE, production deployment or production restore follows automatically from a
documentation update.
