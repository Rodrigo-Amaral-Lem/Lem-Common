# Testing and maintenance

Run commands from the extracted project root (`Lem/`). Tests use fictitious data
and disposable databases; do not point test runners at a production database.

## Server and deployment helpers

Use a development Python environment with `server/requirements.txt`, pytest, pypdf (PDF text assertions) and
httpx installed. Then run:

```bash
PYTHONPATH=server python -m pytest server/tests deploy/tests -q -rs
python -m pytest app/tests/test_android_openssl.py -q
```

The first command checks imports, report/photo permissions, revisions, deletion,
ownership history/upgrades and deployment packaging/configuration. Some tests
require optional external inputs/tools: Stations fixture workbooks and PowerShell 7.
Read each skip reason instead of treating a skipped test as a pass. Set `PWSH` to a
PowerShell executable when needed. The OpenSSL configuration tests require CMake
on PATH, or `CMAKE_COMMAND=/absolute/path/to/cmake`; they do not require an Android SDK.

`server/tests/test_workflow.py` writes a fictitious demonstration PDF under
`examples/`. Restore the previously shipped sample when preparing an unrelated
source-only change so a renderer timestamp does not create an accidental asset diff.

## C++ build and persistence tests

With a Qt 6.12 desktop kit available:

```bash
cmake -S app -B build -DCMAKE_PREFIX_PATH="/path/to/Qt/6.12.0/gcc_64" -DLEM_BUILD_TESTS=ON
cmake --build build --parallel
QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure
```

The `LEM_BUILD_TESTS` option is an existing compatibility name. Targets include:

| Target / test | Checks |
| --- | --- |
| `Lem --smoke-test` / qml-startup | QML startup, model shape and warnings using temporary demo storage. |
| `Lem-client-smoke` / client-persistence | Basic report editing, persistence and local guards. |
| `Lem-storage-test` / storage-migration | Legacy copy/URL/settings migration, including interruption/retry behavior. |
| `Lem-offline-test` / offline-persistence | Journals, restart recovery, delayed disk writes, independent copies and cache safeguards. |

For the network integration scenario:

```bash
QT_QPA_PLATFORM=offscreen python app/tests/test_offline_sync.py build/Lem-offline-test
```

The runner starts a disposable local API on port 18765, imports synthetic chargers,
adds controlled latency and a lost acknowledgement, then launches the C++ executable
with network-test arguments. It tests newer edits during an upload, deferred photo
batches, cancellation/resume, deletion, owner transfer with offline work, revision
conflict, complete copies and backup guards. It also checks bounded photo download
concurrency and absence of unnecessary catalogue refreshes after upload batches.

`LEM_TESTING` enables the disk-delay hook. `LEM_TEST_WRITE_DELAY_MS` is a test-only
environment input used to confirm that a 500 ms file write does not freeze answer
handling. Do not add that artificial delay to production behavior.

## QML interaction checks

With PySide6 available for the mock-backed UI test:

```bash
python app/tests/test_report_tabs.py report mobile
python app/tests/test_report_tabs.py report
python app/tests/test_scroll_chrome.py
python app/tests/test_contract_year.py
python app/tests/test_photo_delegate_stability.py
python app/tests/test_measurement_inputs.py
python app/tests/test_startup_variants.py
```

The tests select offscreen/software rendering themselves and uses demo data. It checks
one-tap answers, group navigation/retained state, camera routing, optional/NOK notes,
evidence/review, read-only/confirmation guards, visible progress and conflict/transfer
actions. Passing the mock test does not validate actual network or disk behavior.

Desktop offscreen tests do not replace Android device testing. Validate camera
handoff, gallery content URIs, Activity recreation, platform TLS and signed release
installation in the intended Android Qt kit/device.

## Formatting

The root `.clang-format` specifies four spaces, 100 columns, unchanged include order
and unchanged string literal boundaries. It applies to C++/headers and the Java bridge.
`pyproject.toml` contains only Black settings, not a new application dependency or
packaging system. QML is formatted with Qt's qmlformat without import sorting or
attribute normalization.

Typical maintenance commands (using developer-installed tools) are:

```bash
clang-format -i app/src/*.cpp app/src/*.h app/tests/*.cpp app/android/src/pt/lem/app/*.java
python -m black server/app server/tests app/tests deploy tools
qmlformat -i -w 4 -W 100 app/qml/Main.qml
```

Use the formatter matching the intended Qt kit for future changes. Avoid
`qmlformat --sort-imports`: shadowed names can change meaning when imports move.
Avoid large formatting-only diffs mixed into a functional bug fix.

## Readability-only comparison

[tools/check_readability.py](../../tools/check_readability.py) compares the current
source against a baseline ZIP from before a readability-only edit. The 0.1.23
controller/package rename intentionally changes identifiers, so comparison with the
original 0.1.22 ZIP is no longer expected to pass:

```bash
python -m pip install Pygments
python tools/check_readability.py /path/to/original/Lem_Qt_0.1.22.zip
```

It checks Python ASTs with location attributes omitted, C++/Java lexical tokens
without comments/whitespace, and QML tokens/scopes with formatter semicolons and
same-object `id` movement permitted. New documentation/formatting tools are outside
the original-file comparison. The script is a review aid, not a compiler or formal
proof of behavior: QML automatic semicolon insertion, preprocessing, build settings
and native-platform behavior still require the appropriate tests/review.

The documented 0.1.22 edition passed comparison for all 35 original code files;
its historical validation record is retained. Version 0.1.23 deliberately renames
controller identifiers, source files and the Android application ID, and updates
version values and import-validation wording. Database schemas, credentials,
shared checklist and storage/synchronization algorithms are unchanged.

## Reviewing a future functional change

- Trace each local mutation through memory, journal, full checkpoint and eventual ACK.
- Keep server revision and local edit sequence separate. Ask what happens if the response is lost or the technician edits again during the request.
- Capture IDs before async work and reconcile into the right report after navigation.
- Check owner/contract/revision on the server; a client-side guard is not sufficient.
- Preserve the ordering between photo uploads and final closure.
- Distinguish ordinary cache eviction, manual local cleanup and permanent remote deletion.
- Check legacy storage/package/configuration compatibility before renaming identifiers.
- Document the tests actually run, optional skips and platform gaps.

## Local PDF and field navigation (0.1.27)

Build with `LEM_BUILD_TESTS=ON` and run `ctest -R local-pdf --output-on-failure`.
`Lem-pdf-test /absolute/path/report.pdf` keeps its synthetic output for Poppler inspection.
The fixture has no authenticated session and deliberately spans several pages.
Run `python app/tests/test_field_navigation.py` for the touch/group/anchor regression.
`server/tests/test_voltage_labels.py` verifies current labels and an older frozen
report export, including that rendering leaves its template unchanged. PDF text
assertions require Poppler; no additional Python PDF dependency is necessary.

## Client release policy and naming (0.1.28)

`server/tests/test_compatibility.py` covers numeric ordering, absent/malformed/old/future
versions, compatible update reminders, token issuance and existing-session rejection.
Build `Lem-compatibility-test` with `LEM_BUILD_TESTS=ON`, then run
`python app/tests/test_client_compatibility.py /absolute/path/Lem-compatibility-test`.
This starts disposable local APIs and verifies real native requests, including zero
credential POSTs for blocked/unverifiable policy, and a policy change between GET/POST.
`test_version_notice.py` exercises QML notices independently of transient status.
`test_scroll_chrome.py` now also checks a full-height track, minimum thumb size and
clamping at both elastic overshoot extremes. Deployment tests include scoped prototype
cleanup, simulated Docker failures and preservation of unrelated resources.

## Desktop parity and feedback (0.1.29)

Run `test_report_tabs.py report` as well as `test_report_tabs.py report mobile`.
Both execute the shared answer/photo/review/permission/navigation suite.
`test_feedback_layout.py` checks toast/footer separation and dismiss interaction across
narrow and wide windows and intermediate footer positions. Build/run
`Lem-server-settings-test` for the pure cross-platform preference policy. The desktop
controller is the same native controller used by offline/PDF/compatibility HTTP tests;
only Android camera integration and mobile gestures/chrome have platform guards.
`deploy/tests/test_client_policy_config.py` verifies a pinned latest version advances
with the published client while preserving minimum version, secrets and newer policy.

## Scroll end limits (0.1.31)

`test_scroll_limits.py` presses/drags at the settled document end, including variable
catalogue delegate heights, visible/hidden footer, short groups, empty/single-item
catalogues and desktop. It checks physical final-item/footer geometry as well as
contentY during the gesture. `test_scroll_chrome.py` still checks stable geometry on
every animation frame. The regression fails against 0.1.30 (duplicated final inset),
and the revised pages prohibit elastic movement beyond the end.

## Swipe-to-end with hidden controls (0.1.32)

`test_scroll_end_transition.py` starts at the top and drives real touch swipes until
controls hide and the actual final card is reached. It checks per-frame rendered
bounds and stable footer size, repeats/reverses gestures, changes answers/groups and
resizes the viewport. `test_desktop_page_input.py` checks wheel and keyboard paging
for the explicit page Flickables. The previous end-limit suite remains useful but
its programmatic end positioning alone did not reproduce the Android issue.
