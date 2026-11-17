# Maintenance and common tools

Run workstation commands from the **Common repository root**. Keep generated reports and
temporary inputs in ignored `build/` subdirectories. Update the focused guides and platform
manuals rather than adding a new document for each patch.

## Common tool catalogue

| Tool | Inputs and prerequisites | Output / side effects |
| --- | --- | --- |
| [sync_shared.py](../tools/sync_shared.py) | Python standard library; sibling App/Server repositories | Default read-only byte comparison of Common/shared against both tracked snapshots; exit 1 for differences |
| `sync_shared.py --write` | Intentional canonical resource update | Copies changed/missing files into snapshots; never deletes unexpected files; not an atomic cross-repository transaction |
| [check_docs.py](../tools/check_docs.py) | Python standard library; selected repositories under the workspace | Read-only validation of local Markdown file/anchor links; prints failures and exits nonzero; no internet/link fetching |
| [check_readability.py](../tools/check_readability.py) | Python plus Pygments, original ZIP and a matching reconstructed source tree | Historical structural-comparison report for comment/format-only work; nonzero if executable structure differs |

```powershell
python tools/sync_shared.py
python tools/check_docs.py
python tools/check_docs.py --repo App --repo Common
python -m unittest discover -s tools/tests -v
```

`check_docs.py` defaults to App, Server and Common under the workspace containing its repository.
`--workspace PATH` selects another workspace. It checks relative file links and Markdown heading
anchors; it does not prove a command is safe/correct, check external URLs or validate arbitrary HTML
rendering. A missing sibling link fails even if only one repository was selected.

The legacy readability tool expects ZIP entries under one top-level package directory and source
paths with the old inner `app/`, `server/` structure. Its default `--source` is Common's root,
which is **not** a reconstructed monorepository. To use it, explicitly assemble/select a matching
tree under `build/readability-source/` and pass `--source`; do not interpret missing current-split
paths as an application defect. Functional changes should fail that comparison by design. It is not a
replacement for tests or Git review.

## Documentation and comments

Mandatory evidence always requires a photograph. Videos are optional attachments and never
satisfy a required-evidence rule. Apply this user rule to future checklists, validation and manuals.

Each guide should answer a distinct question, link to the owner of a cross-component rule, and
describe the current implementation. Keep field labels in Portuguese when quoting the UI, with
consistent English explanations. State the working directory, prerequisites, output paths and
mutations alongside a command. Mark deployment/internal helpers and destructive options explicitly
rather than hiding them among routine examples.

Source comments should explain ownership, durability boundaries, ordering constraints and
non-obvious limitations. Avoid historical changelog paragraphs inside functions or assertions that a
test run proves universal correctness. Command scripts should state their inputs, side effects and
public/internal status near the entry point.

When changing software, update affected guides and user manuals in the same work, including
maintained PDF editions when their Markdown changes. Keep source/scripts readable through clear
names, formatting and comments explaining intent and recovery, rather than restating each line.
The development workstation has WSL with Ubuntu and virtualization enabled for Linux tests and
Android emulator simulations; check installed tooling before use and distinguish emulator results
from physical-device validation.

Before staging documentation:

1. Verify the described flags/paths in source, including script defaults and outputs.
2. Run shared-snapshot and local-link checks.
3. Check Markdown headings, tables, fenced commands and UTF-8 text.
4. Review source edits for comment/format-only scope; an updated diagnostic documentation path is
   not a functional algorithm change.
5. Keep per-run artifacts under ignored `build/` directories, then inspect each repository's staged diff.
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
python -m black tools/sync_shared.py
clang-format -i ../App/app/src/Checklist.h
```

QML can be formatted with the matching Qt `qmlformat` without import sorting/attribute
normalization. Formatting tools are development dependencies, not application runtime requirements.

## Release and contract changes

Revision `0.2.5` (Android code 176) makes photographs mandatory for applicable MAN.14–18 and
observations mandatory for N/A. Minimum/latest become `0.2.5`: older offline clients can close
reports without these checks and cannot safely claim compatibility. Upgrade the app and server
together. A server-rejected local closure returns to an editable draft with its answers/evidence
preserved. Already accepted closed reports retain their historical rules. This release also allows
signing during background sync and adds clockwise photo rotation; no database schema change is needed.

App/CMake declarations, `app/src/main.cpp`, Android version name/code, Server's compatibility
policy, Compose image tag and installer/environment policy defaults must be considered together.
`test_release_alignment.py` checks the current client/server declarations when both repositories are
available. Compatibility admits versions from minimum through latest, including both bounds;
newer-than-latest clients are not assumed compatible.

### Version policy

The user's policy, recorded on 2026-11-16, applies to future app and server changes:

- Increment the last version number for an incompatible change, for example `0.2.0` to `0.2.1`.
  Raise the server's minimum client version to the first compatible app. Never ship incompatible
  software under an unchanged client version.
- Reserve the middle number for a deliberately consolidated release, for example `0.2.13` to
  `0.3.0`. Preparing that version does not authorize committing, tagging, pushing or publishing.
- A request for suggested/prepared Git commits triggers this consolidation: advance the minor
  number and reset the patch to zero, once per preparation batch. This batch moves `0.2.6` to
  `0.3.0`; revising its messages or commands does not trigger another increment.
- Always prepare cryptographically signed commit commands (`git commit -S`) for the user to
  execute. A `-s` sign-off alone is not a signature. Use a clear subject and detailed body covering
  the behavior, motivation, validation and compatibility decision; do not fall back to unsigned.
- Incompatible clients receive an explanation and cannot log in; enforce the gate on the server
  for both login and existing sessions. Preserve their local reports while they update.
- Older compatible clients may log in and receive an update notice. Advance the latest version
  without raising the minimum when compatibility is retained.
- Coordinate CMake/main/Android declarations (including a strictly increasing Android version
  code), API version, deployment defaults and release-alignment tests. Document the compatibility
  decision and test both blocked login and compatible login with an update notice.

### Form-evolution checks required before changing question meaning or structure

Treat checklist versions as data formats. Keep closed originals frozen; upgrading an administrator
correction or an editable draft must preserve content and evidence in the same transaction.
Do not reuse an item ID for another meaning without an explicit versioned mapping/archive.

- Compare native and server projections, including `_inflight_payload`, so an upgrade after a lost
  acknowledgement cannot create a false conflict. Require idempotence and unique question IDs.
- Exercise absent/null optional fields, maximum-length text, renamed/merged questions, retained
  custom/suggested notes, signatures (current and historical), photo IDs/checkpoints and unit changes.
- Test GET projection against the following PUT, photo upload before that PUT, stale revisions,
  interrupted historical closure, reopen/copy recovery, rejected writes and successful retries.
  Identical answers must not skip the PUT needed to acknowledge a changed form or upload marker.
- Expand connector questions from the complete prototype. New rules/help must not disappear
  because an expansion function copied only a fixed list of fields.
- Export the migrated result as PDF/ZIP and verify full text and original bytes. Repeat correction
  and confirm that historical evidence does not reference a removed source report.
- Retain explicit compatibility/version decisions; unknown future versions must not be silently
  projected as today's form. Follow Android graphical checks whenever the UI changes.

`Server/server/tests/test_form_evolution.py` compares the Qt adapter
`Lem-migration-projection` with Python and tests these recovery/size boundaries. Keep its cases
aligned with every new form version; see the component testing guides for invocation.

Revision `0.2.1` keeps the `0.2.0` API compatible: its minimum remains `0.2.0`, its latest is
`0.2.1`, and Android version code advances from 171 to 172. Report download isolation and durable
contract-retention suspension are client fixes; the server already rejects retention writes with
423. The new local suspension field is private metadata and is not sent in report payloads.

Revision `0.2.2` introduces atomic administrator corrections and replacement tombstones. Its
minimum/latest client versions are both `0.2.2`, with Android version code 173. Older apps interpret
every report tombstone as permission to erase the local copy; they cannot safely preserve pending
work when an administrator replaces a closed report. Update the server policy and apps together,
in place, retaining local reports. The middle version number remains unchanged; no release is
published by this change.

Revision `0.2.3` fixes presentation lookup for legacy cached reports before PDF/ZIP export.
It adds no wire-format or database incompatibility: minimum client remains `0.2.2`, latest becomes
`0.2.3`, and Android version code is 174. Clients on `0.2.2` can still log in and receive an update
notice. Deploy the updated latest-version policy before using the `0.2.3` app; an older server
whose admitted upper bound is still `0.2.2` will reject it. Preserve existing local reports.

A shared template change also needs synchronized snapshots, connector/measurement case review and a
deliberate choice about existing drafts versus closed history. Current editable-v6 corrections are
explicit functions in both components; do not assume every future template addition automatically
migrates all reports.

Revision `0.2.4` fixes the PostgreSQL first-presentation write and adds verified save feedback in
the client. The API shape and stored reports are unchanged: minimum remains `0.2.2`, latest is
`0.2.4`, Android version code 175. Updating the server repairs the rejected save for compatible
Windows/Android apps too; the new app adds persistent confirmation and error feedback. Re-save the
desired contract format after deploying because earlier failed transactions stored no choice.
No reimport, report deletion or ownership change is required.

Review the three Git diffs as a coordinated release, but keep component responsibilities separate.
The current `0.2.5` work tree adds desktop contract PDF/ZIP batching and the optional administrator
technician-password endpoint. These additions do not change existing payloads, stored reports or
login compatibility; the existing `0.2.5` minimum/latest policy is retained. The new password action
needs the updated API; an older compatible server cannot perform that action. No release/deployment
is implied by preparing these changes.

The Android photo-editor arrow is drawn geometrically instead of using a font glyph. This UI-only
fix changes no protocol, stored data or compatibility policy; the current `0.2.5` version is retained.
Every UI change now requires graphical verification of the changed APK in an actual Android
emulator, with isolated data and inspected screenshots, as recorded in the workspace AGENTS.md.

Deployment transport ZIPs are temporary payloads, not the source-of-truth workflow. No Git remote,
APK, portable EXE, production deployment or production restore follows automatically from a
documentation update.

### Checklist v7 / version 0.2.6 (2026-11-17)

App/server version and minimum/latest client are **0.2.6**, Android code **177**. Earlier apps cannot
safely interpret MAN.21/MAN.22, current units or calculated assessments. Login and authenticated
requests reject incompatible versions. Stale deployment environment values cannot lower the compiled
compatibility floor; latest is raised to that floor when necessary. This is an incompatible patch,
not a release publication. No database schema change is needed.

New reports, existing v6 drafts and administrator correction copies use v7. Closed originals remain
frozen; old offline closed v6 reports can finish staged upload without reinterpreting their answers.
See report-contract.md for unit confirmation, retired-answer/evidence preservation and the temporary
50 V criterion with the 25 V exception. Suggested observations must keep explicit provenance and
clear only untouched generated text on state change/user focus; apply this to future suggestions.

The subsequent regression fixes retain `0.2.6` / Android 177 / minimum `0.2.6`: correction lock
ordering, cloned historical-signature references and photo uploads against a projected migrated
form do not change the API contract or introduce another incompatible client. Explicit
`photo_always: false` for MAN.14–18 matches the existing default and migration output; N/A still
needs an observation and OK/NOK still need a photograph. No new UI behavior is introduced.

The `Mennekes Type 2` to `AC Type 2` terminology update also retains `0.2.6` / Android 177 /
minimum `0.2.6`. The server accepts former and current names during connector comparison;
older compatible clients are not rejected merely for their spelling. Update app and server
for consistent current wording. Counts/order and frozen answers/evidence remain unchanged.

The export/correction concurrency fix also retains `0.2.6` / Android 177 / minimum `0.2.6`.
Server PDF/ZIP preparation now releases source/contract/user locks after staging immutable
metadata and evidence, before rendering or archive assembly. This is an internal resource-lifetime
fix: no API, database schema, client behavior or compatibility floor changes. Deploying the
updated server is required to use it; rebuilding the app is not required for this fix.

The form-evolution audit fixes also retain `0.2.6` / Android 177 / minimum `0.2.6`. Existing admitted
clients remain compatible: the server accepts complete merged general notes up to 32000 characters
and an explicit current-draft PUT can reopen a rejected historical upload. Native changes repair
lost-ACK projections, historical-signature references and connector-rule inheritance without a new
payload format or database schema. Update both components to obtain all of these fixes.

### Consolidated version 0.3.0 (2026-11-17)

The user's commit-preparation request consolidates the preceding work as app/API **0.3.0**,
Android code **178**, checklist **7**. Minimum compatible client remains **0.2.6**; latest becomes
**0.3.0**. A compatible 0.2.6 app may log in and receives an update notice. Earlier incompatible
apps remain blocked. This numbering change introduces no additional protocol or schema change.
Update server deployment policy before installing the new client, preserve local reports during
upgrades, and use the prepared signed commit commands. No commit, tag or publication is automatic.
