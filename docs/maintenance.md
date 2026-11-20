# Maintenance and common tools

Read [root AGENTS.md](../../AGENTS.md) and [Common's local instructions](../AGENTS.md).
Shared task scope, permissions, validation and staging rules live in the root instructions;
this guide documents Common's tools and detailed maintenance checks.

Run workstation commands from **ongoing_work**, using explicit paths into the repositories.
Keep generated reports, temporary inputs, caches and build output under the current
`ongoing_work/tasks/<task>/` directory. Follow the [working-area workflow](../../ongoing_work/WORKFLOW.md)
for task setup and temporary-path configuration. Repository-local output is an exception only
when a tool genuinely requires it, under the root location/ignore rules. Update the existing
focused guides and platform manuals rather than adding a document for each patch.

For parallel tasks, follow the root [parallel-work rules](../../AGENTS.md#parallel-work-and-integration-user-instruction-2026-11-18)
and [worktree/reservation workflow](../../ongoing_work/WORKFLOW.md#parallel-work).
Use the task's sibling Common/App/Server worktrees as effective repository roots,
including for `sync_shared.py`; preserve the original checkouts and existing build
paths. The user owns all branch/integration merges and later transfer to the originals.
Reserve shared resources atomically and keep task-private generated output. A worktree
copied from a dirty base contains inherited changes, not a committed checkpoint.

## Common tool catalogue

| Tool | Inputs and prerequisites | Output / side effects |
| --- | --- | --- |
| [sync_shared.py](../tools/sync_shared.py) | Python standard library; sibling App/Server repositories | Default read-only byte comparison of Common/shared against both tracked snapshots; exit 1 for differences |
| `sync_shared.py --write` | Intentional canonical resource update | Copies changed/missing files into snapshots; never deletes unexpected files; not an atomic cross-repository transaction |
| [check_docs.py](../tools/check_docs.py) | Python standard library; selected repositories under the workspace | Read-only validation of local Markdown file/anchor links; prints failures and exits nonzero; no internet/link fetching |
| [check_readability.py](../tools/check_readability.py) | Python plus Pygments, original ZIP and a matching reconstructed source tree | Historical structural-comparison report for comment/format-only work; nonzero if executable structure differs |

```powershell
# Working directory: ongoing_work. These checks are read-only.
.\.venv\Scripts\python.exe -B ..\Common\tools\sync_shared.py
.\.venv\Scripts\python.exe -B ..\Common\tools\check_docs.py
.\.venv\Scripts\python.exe -B ..\Common\tools\check_docs.py --repo App --repo Common
```

The retained interpreter path is an example; verify it before use. `-B` avoids writing
Python bytecode into product repositories. When changing the Common tools, their focused
tests can be run from ongoing_work with
`.\.venv\Scripts\python.exe -B -m unittest discover -s ..\Common\tools\tests -v`;
first point TMP/TEMP at task-local scratch as described in the workflow. Do not rerun tool
tests solely for a prose edit when the applicable documentation checks are sufficient.

`check_docs.py` defaults to App, Server and Common under the workspace containing its repository.
`--workspace PATH` selects another workspace. It checks relative file links and Markdown heading
anchors; it does not prove a command is safe/correct, check external URLs or validate arbitrary HTML
rendering. A missing sibling link fails even if only one repository was selected.

The legacy readability tool expects ZIP entries under one top-level package directory and source
paths with the old inner `app/`, `server/` structure. Its default `--source` is Common's root,
which is **not** a reconstructed monorepository. To use it, explicitly assemble/select a matching
tree under `ongoing_work/tasks/<task>/scratch/readability-source/` and pass its explicit path
with `--source`; do not interpret missing current-split paths as an application defect.
Functional changes should fail that comparison by design. It is not a
replacement for tests or Git review.

## Documentation and comments

Follow the root [maintenance and evidence rules](../../AGENTS.md#local-testing-and-readable-maintenance-user-instructions-2026-11-17),
including photographs for mandatory report/checklist evidence, Android screenshots for UI
verification, meaningful comments and regeneration/layout checks for maintained manual PDFs.

Each guide should answer a distinct question, link to the owner of a cross-component rule, and
describe the current implementation. Keep field labels in Portuguese when quoting the UI, with
consistent English explanations. State the working directory, prerequisites, output paths and
mutations alongside a command. Mark deployment/internal helpers and destructive options explicitly
rather than hiding them among routine examples.

Source comments should explain ownership, durability boundaries, ordering constraints and
non-obvious limitations. Avoid historical changelog paragraphs inside functions or assertions that a
test run proves universal correctness. Command scripts should state their inputs, side effects and
public/internal status near the entry point.

For requested documentation edits, use the checks below before staging. Review-only and
commands-only tasks preserve indexes, as required by the root
[scope](../../AGENTS.md#task-scope-and-evidence) and
[staging rules](../../AGENTS.md#staging-and-release-preparation).

1. Verify the described flags/paths in source, including script defaults and outputs.
2. Run shared-snapshot and local-link checks.
3. Check Markdown headings, tables, fenced commands and UTF-8 text.
4. If a task is comment/format-only, verify that source edits stay within that scope; changing a
   documented diagnostic path is not a functional algorithm change.
5. Keep per-run artifacts in the current ongoing_work task. Review existing edits and partial
   staging before adding only the authorized documentation changes; inspect the staged diff.
6. Implementing changes for user review permits that in-scope staging; a review-only task does
   not. Passed checks do not authorize commits, tags, pushes, production deployment or publication.

## Test coordination and formatting

Use the [App test guide](../../App/docs/testing.md) for native/QML/network runners and the
[Server test guide](../../Server/docs/testing.md) for API/deployment fixtures. A client mock test
does not establish disk/network correctness; SQLite tests do not establish PostgreSQL locking
behavior; offscreen desktop tests do not replace the required real Android emulator verification.
Label emulator and physical-device results separately; a physical device is not a substitute for
the user-required emulator check. Check available SDK/emulator tooling before use.

The projects retain [pyproject.toml](../pyproject.toml) with Black settings, and App has
[.clang-format](../../App/.clang-format). For a formatting-only task, use the relevant tool on the
selected files and compare executable structure. Do not reformat all production source during an
unrelated documentation edit.

Examples from ongoing_work, only for an authorized formatting task and when the optional tools
are installed. These commands modify the named product source files; configure any tool caches
under the current task before running them.

```powershell
.\.venv\Scripts\python.exe -B -m black --config ..\Common\pyproject.toml ..\Common\tools\sync_shared.py
clang-format -i ..\App\app\src\Checklist.h
```

QML can be formatted with the matching Qt `qmlformat` without import sorting/attribute
normalization. Formatting tools are development dependencies, not application runtime requirements.

## Release and contract changes

App/CMake declarations, `App/app/src/main.cpp`, Android version name/code, Server's compatibility
policy, Compose image tag and installer/environment policy defaults must be considered together.
[test_release_alignment.py](../../Server/server/tests/test_release_alignment.py) checks current
client/server declarations when both repositories are available. Compatibility admits versions
from minimum through latest, including both bounds;
newer-than-latest clients are not assumed compatible.

For an explicitly requested release-preparation batch, review the component diffs together while
keeping their responsibilities separate. This guide does not start a batch or authorize executing
prepared commit/deployment commands. Current declarations and batch records determine the target;
the historical version notes below are not a list of actions to perform now.

### Version policy

The user's policy, recorded on 2026-11-16, applies to future app and server changes.
Keep this maintained summary aligned with the root
[version policy](../../AGENTS.md#users-version-policy-2026-11-16) and follow its
[staging, signing and preparation boundaries](../../AGENTS.md#staging-and-release-preparation):

- Increment the last version number for an incompatible change, for example `0.2.0` to `0.2.1`.
  Raise the server's minimum client version to the first compatible app. Never ship incompatible
  software under an unchanged client version.
- Reserve the middle number for a deliberately consolidated release, for example `0.2.13` to
  `0.3.0`. Preparing that version does not authorize committing, tagging, pushing or publishing.
- A request for suggested/prepared Git commits triggers this consolidation: advance the minor
  number and reset the patch to zero, once per preparation batch (for example `0.2.6` to
  `0.3.0`). Record the actual baseline and target; revising the same batch's messages, commands
  or fixes does not repeat the minor consolidation. Genuine new incompatibilities still follow
  the patch/minimum rule. Ordinary fixes, reviews, resumption and template edits do not themselves
  request a new preparation batch.
- When commit preparation is requested, provide cryptographically signed commands (`git commit -S`)
  for the user to execute. A `-s` sign-off alone is not a signature. Use a clear subject and detailed
  body covering behavior, motivation, validation and compatibility; do not fall back to unsigned.
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

A shared template change also needs synchronized snapshots, connector/measurement case review
and a deliberate choice about existing drafts versus closed history. Editable-report migrations
use explicit functions in both components; do not assume a future template addition automatically
migrates all reports.

### Historical release notes

The following entries record past implementation and preparation decisions, including their
then-current versions and rollout advice. They do not assert today's deployed versions, grant
current staging/deployment approval or trigger another consolidation. Apply current source,
batch records and the policies above when planning new work.

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

Revision `0.2.4` fixes the PostgreSQL first-presentation write and adds verified save feedback in
the client. The API shape and stored reports are unchanged: minimum remains `0.2.2`, latest is
`0.2.4`, Android version code 175. Updating the server repairs the rejected save for compatible
Windows/Android apps too; the new app adds persistent confirmation and error feedback. Re-save the
desired contract format after deploying because earlier failed transactions stored no choice.
No reimport, report deletion or ownership change is required.

Revision `0.2.5` (Android code 176) makes photographs mandatory for applicable MAN.14–18 and
observations mandatory for N/A. Minimum/latest become `0.2.5`: older offline clients can close
reports without these checks and cannot safely claim compatibility. Upgrade the app and server
together. A server-rejected local closure returns to an editable draft with its answers/evidence
preserved. Already accepted closed reports retain their historical rules. This release also allows
signing during background sync and adds clockwise photo rotation; no database schema change is needed.

The `0.2.5` preparation work adds desktop contract PDF/ZIP batching and the optional administrator
technician-password endpoint. These additions do not change existing payloads, stored reports or
login compatibility; the existing `0.2.5` minimum/latest policy is retained. The new password action
needs the updated API; an older compatible server cannot perform that action. No release/deployment
is implied by preparing these changes.

The Android photo-editor arrow is drawn geometrically instead of using a font glyph. This UI-only
fix changes no protocol, stored data or compatibility policy; that batch retained `0.2.5`.
Current UI verification requirements are in the root maintenance/evidence rules linked above.

Deployment transport ZIPs are temporary payloads, not the source-of-truth workflow. No Git remote,
APK, portable EXE, production deployment or production restore follows automatically from a
documentation update.

### Checklist v7 / version 0.2.6 (2026-11-17)

This batch recorded app/server version and minimum/latest client as **0.2.6**, Android code **177**.
Earlier apps cannot safely interpret MAN.21/MAN.22, current units or calculated assessments. Login and authenticated
requests reject incompatible versions. Stale deployment environment values cannot lower the compiled
compatibility floor; latest is raised to that floor when necessary. This is an incompatible patch,
not a release publication. No database schema change is needed.

New reports, existing v6 drafts and administrator correction copies use v7. Closed originals remain
frozen; old offline closed v6 reports can finish staged upload without reinterpreting their answers.
See report-contract.md for unit confirmation, retired-answer/evidence preservation and the temporary
50 V criterion with the 25 V exception. Suggested observations must keep explicit provenance and
clear only untouched generated text on state change/user focus; apply this to future suggestions.
When focus clears generated text, retain the open editor and its focus, including optional OK
observations such as MAN.18. Emptying the suggestion must not remove the observation field or
require a second tap to write. The explicit observation-removal control remains available.
This shared behavior applies to every question with auto-filled notes: N/A defaults, calculated
suggestions and future form additions. Cover the full template's defaults plus calculated OK/NOK
cases in UI regressions; do not implement or test it only for MAN.18.

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

The user's commit-preparation request consolidated the preceding work as app/API **0.3.0**,
Android code **178**, checklist **7**. Minimum compatible client remained **0.2.6**; latest became
**0.3.0**. A compatible 0.2.6 app may log in and receives an update notice. Earlier incompatible
apps remain blocked. This numbering change introduces no additional protocol or schema change.
The recorded rollout order was to update server deployment policy before installing the new
client, preserving local reports during upgrades. Prepared signed commands were for user execution;
the preparation record does not establish that a commit, deployment or publication occurred.

### Prepared version 0.3.2 (2026-11-18)

The user explicitly selected **0.3.2** for this preparation batch, overriding the
usual next-minor consolidation. Android code is **179**; checklist remains **7**.
The observation editor stays open and focused when generated text is cleared.
This is compatible UI behavior: there is no API, payload, schema or persistence
change. Minimum compatible client stays **0.2.6**; latest becomes **0.3.2**.
Clients 0.2.6 through 0.3.1 remain supported and receive an update notice.
Deploy the updated server policy before distributing the new app; preserve local reports.
The batch record is `ongoing_work/tasks/2026-11-18-parallel-work/`.
Follow-up edits in this batch must not increment the version again. Preparation
does not establish a commit, merge, deployment or publication; these remain user actions.


### Prepared version 0.4.0 (2026-11-18)

The user selected a new minor consolidation after the committed 0.3.2 baseline.
This batch combines T1's safe photo-deletion acknowledgement and T2's recoverable
local checkpoints, including maintained UI failure/retry regressions. App/server
and latest client become **0.4.0**, with Android version code **180**. The minimum
compatible client remains **0.2.6**: request/cache/form formats are unchanged,
stale DELETE uses the existing 409 conflict response, and compatible older apps
continue to log in with an update notice. Local reports are preserved.

Preparation records are in `ongoing_work/tasks/2026-11-18-t1-t2-0-4-0-preparation/`.
The separate fix commits and the final version commits belong to this one batch;
do not increment again for its follow-up edits. The user commits and integrates
the fixes before applying the prepared consolidation patches. Deploy the updated
server policy before distributing the app; no deployment/publication is authorized
by preparation. This record describes a prepared candidate, not a published release.

### Prepared version 0.4.1 (2026-11-18)

The user selected **0.4.1** for the closed-report correction batch. App, API and
latest client use 0.4.1. Android version code increases to **181** and checklist stays
at **7**. Minimum client remains **0.2.6**, with update notices for compatible older
apps. Keep client storage during the app update so pending work can be retried.

The server adds a nullable opening identity baseline for closed-report corrections.
The server update goes first so the desktop app can revalidate cached model,
manufacturer and serial conflicts through the existing sync command. The source
report and its evidence stay available until the replacement transaction succeeds.

### Prepared version 0.5.0 (2026-11-19)

This release consolidates the PCVE catalogue, contract membership management, persistent
sessions and report-handling fixes after 0.4.1. App, API and latest client advance to **0.5.0**.
Android version code advances to **182**. Checklist **7** and minimum client **0.2.6** stay
current. The server accepts the earlier report format, and older compatible clients receive
an update notice. Existing sessions retain their original expiry. Deploy the server first
and update the app in place to preserve pending reports and evidence.

The release record is in `ongoing_work/tasks/2026-11-19-prepare-0-5-0/`.

### Contract membership notes in 0.5.1

The optional **Notas** column belongs to the PCVE's membership in each preventive maintenance
contract. Use the membership UUID for import, caching and editing. Keep this field out of the
shared station details, including raw spreadsheet columns. See [report contract](report-contract.md#contract-instructions-for-a-pcve).

App/API and latest client are **0.5.1**, Android code **183**. Minimum client stays **0.2.6**.
The API additions and the new membership notes table preserve earlier import and report formats.
Compatible earlier clients receive an update notice. Use the updated app to display contract notes.

### Ordens de trabalho em 0.5.2 e 0.5.3

App/API 0.5.3, Android 185, checklist 7, minimum 0.2.6. Earlier clients retain whole-contract access and receive an update notice. The new client opts into membership-scoped catalogues. Additive work-order tables keep planning, results and notifications separate from report payloads. Install the updated server before the client and preserve offline reports. Version 0.5.3 adds cancellation and draft-recovery tables. Existing clients omit cancelled orders by default. An installed 0.5.2 client can update in place.
