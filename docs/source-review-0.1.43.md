# Source review — 0.1.43

Reviewed the Qt controller/persistence/sync and QML presentation, Android capture
bridge and packaging, server models/auth/permissions/import/checklist/PDF/ZIP,
and deployment/version policy/build helpers. This report records concrete fixes
and the validation performed, rather than claiming that all defects are excluded.

## Fixes

| Issue | Before | After | Main code |
| --- | --- | --- | --- |
| Calendar-year grouping | SpinBox used regional number grouping, e.g. 2,026 | Calendar years always display plain digits; initial value is the current year | app/qml/Main.qml |
| Missing connectors in mixed lists | N/A in a mixed/slash-separated list became fictional N and A connectors; counted NA could also generate tests | Missing-value markers remain one token and are omitted before generating physical connector tests | app/src/Checklist.h, server/app/checklist.py |
| Recovered camera result | Attachment checkpoint was checked against the currently open report template | Validate against the target report's own frozen template; unrelated current report remains untouched | app/src/Lem.cpp |
| Whitespace-only contracts | Length checks accepted company/kind consisting of spaces before storage stripped them | Trim before server constraints and disable the create button for blank trimmed inputs | server/app/main.py, app/qml/Main.qml |
| App/server release drift regression | A newer app could ship while deployment still advertised an older maximum version | New alignment test checks app, Android version name, server policy, Compose and installer defaults together | server/tests/test_release_alignment.py |

The stored year was always an integer; the comma was a display issue. No database
repair or migration is needed. Connector changes affect newly generated report
checklists; existing frozen checklists and answers are preserved. No Android
lifecycle guard from the reverted 0.1.42 branch is included.

## Validation

- Server/deploy suite: 146 passed, 28 skipped; release alignment additionally passed.
- The 28 skips require the original Stations Excel workbook (14) or PowerShell 7 (14).
- Build/security configuration tests: 21 passed, with 16 additional subtests.
- Native C++ shared connector vectors (17 cases), generated question IDs/labels and PDF generation passed.
- Native C++ recovered-photo regression passed: A has two connectors, B has three;
  while B is open, A accepts its second connector and rejects B's third connector.
- Native client against a disposable HTTP API passed the offline integration:
  local journals, 500 ms disk-delay responsiveness, background synchronization,
  latest edits surviving acknowledgements, lost PUT/DELETE acknowledgements,
  transfer/conflict recovery, independent copies, draft/closed deletion,
  photo batching/concurrency, partial retry, cancellation, offline pinning and cache cleanup.
- QML year display passed for en_US, pt_PT, de_DE and fr_FR, at 2020/2026/2100.
- QML mobile and desktop report workflows, scroll bounds, desktop scrollbar dragging,
  draft export visibility and startup choices/timing passed.

Backend checks use disposable SQLite and synthetic import fixtures. Native/UI
validation used local Qt/PySide 6.10.2. Full target builds require Qt 6.12; the
physical Android/iOS runtime, Windows release executable and simultaneous
PostgreSQL transactions were not exercised here. PowerShell-specific scenarios
remain skipped in this environment.

## Applying the release

Deploy the server using the existing Linux or PowerShell deploy script, then
rebuild/install app 0.1.43. Latest supported client is 0.1.43; minimum remains
0.1.39. Deployment promotes an older pinned latest version in .env. No reset of
reports, photographs or the database is required.
