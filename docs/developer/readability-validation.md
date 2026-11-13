> Historical validation of the documented 0.1.22 edition. The subsequent 0.1.23 identifier changes are described in [rename notes](../rename-0.1.23.md); the unchanged-token claim below applies only to the earlier documentation revision.

# Documented-edition validation record

This is a documentation/formatting revision of the original **Lem 0.1.22** source
ZIP. The application/API version stays 0.1.22 and Android version code stays 122.
It introduces no runtime feature or deployment requirement.

## Scope

- Expanded C++/header, Java, Python and QML formatting with consistent indentation.
- Added English intent/ordering comments to the controller, persistence/sync flows,
  permissions, server transactions, imports, exports, Android bridge and deployment boundaries.
- Added the linked developer guide, formatter settings and an optional source-comparison tool.
- Corrected stale README statements about Android capture and conflict recovery.
- Preserved existing filenames, runtime identifiers, functions, request schemas,
  permissions, SQLAlchemy definitions, dependency requirements, UI strings, checklist,
  assets, version values and deployment commands.

No functions were renamed, moved to another class/module or reordered. Formatters
may position QML `id` declarations at the start of their original object and insert
JavaScript semicolons; this is covered separately by structure and UI checks.

## Checks actually run

| Check | Result |
| --- | --- |
| Original source comparison | All 35 existing Python/C++/Java/QML files passed AST/token/scope comparison against the unmodified release archive. |
| Server + deployment + Android OpenSSL configuration pytest suites | 50 passed; 26 optional tests skipped. |
| Optional-test reasons | 14 require an external Stations workbook; 12 require PowerShell 7, unavailable in this validation environment. |
| Native C++ offline HTTP integration | Passed: delayed local saves, lost ACK, newer typing, deferred photos, cancellation/retry, deletion, ownership/revision conflicts, independent copies and backup guards. |
| Native client persistence smoke | Passed. |
| Native storage migration | Passed. |
| Mock-backed QML interaction tests | Passed at desktop and phone sizes, without QML warnings. |
| Formatting/syntax | Black check, clang-format dry run and Bash syntax checks passed. |
| Developer guide navigation | Relative local links resolved. |

The OpenSSL tests initially could not locate CMake; rerunning after supplying
`CMAKE_COMMAND` passed all seven configuration tests. That was a test-environment
prerequisite, not a source behavior change.

The validation environment used Python 3.12, Qt/PySide6 6.10.2 for native/QML
checks, Black 26.1.0, clang-format 21.1.8 and CMake 3.31.10 for configuration tests.
The source project still requires Qt 6.12 for its final application build. This
record does not claim a full Qt 6.12 build, signed APK, Android physical-device,
iOS, Windows runtime or concurrent PostgreSQL integration validation. No live
server deployment was performed.

The checked-in synthetic demonstration PDF is retained from the original archive;
test-generated output was not included as an unrelated asset change. Generated
binaries, build directories, caches, private environment files and test databases
are excluded from the distributed source ZIP.

The comparison tool is intentionally conservative and transparent about its limits;
read [testing-and-maintenance.md](testing-and-maintenance.md) before using it as a
review aid for a future change.
