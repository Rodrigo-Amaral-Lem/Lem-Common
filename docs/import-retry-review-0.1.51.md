# Import and retry review — 0.1.51

This round examined repeated administrative requests and interactions between
Excel imports, console enrichment, frozen reports and globally unique identifiers.

## Confirmed findings

| Problem | Correction |
| --- | --- |
| Re-importing an existing charger replaced its entire details object. Coordinates, postal codes, connector configuration and other console-added fields disappeared when absent from the workbook mapping. | Merge imported fields over existing details. Unmapped fields survive; mapped fields still overwrite, including deliberately blank cells. New reports receive the retained connector configuration; existing snapshots/photos stay unchanged. |
| Two imports for the same contract could race after reading the existing chargers. Different contracts for one company could also race to create the shared import profile. | Committed imports take an exclusive per-contract lock directly, after workbook parsing. Shared company profiles use an atomic database upsert. Previews take no exclusive lock. |
| A contract created after another request's duplicate-name precheck could cause an internal error. | Roll back the losing transaction and return HTTP 409. |
| Uploads to different reports could claim the same globally unique photo UUID after their existence checks, causing an internal error. | Roll back the loser and return HTTP 409 without replacing the winner's photo. Existing successful lost-ack retries remain idempotent. |
| Two administrators assigning the same technician to the same contract could collide on the assignment key. PUT/retries were not fully idempotent. | Insert with ON CONFLICT DO NOTHING, preserving one assignment and returning success to repeated requests. |

The write lock is acquired **after** parsing, so workbook decoding does not hold
up ordinary contract reads. Access/retention is checked again at that point: a
contract removed while parsing cannot be modified. There is no shared-to-exclusive
lock upgrade that two imports could deadlock on. PostgreSQL and SQLite both use
their native ON CONFLICT statements for the profile and assignment operations.

## Reproductions and validation

The first four cases in `server/tests/test_review_051.py` all failed against the
uncorrected implementation. A separate reproduction of simultaneous assignment
also failed against 0.1.50. The tests use controlled SQLAlchemy interleavings to
make unique-key conflicts deterministic, rather than relying on thread timing.
The sixth case verifies that an explicitly mapped blank can still clear a value,
while an unmapped field and an existing report's snapshot/photos survive.

- Full server/deploy suite: **272 passed, 28 skipped**.
- Native 0.1.49 client against the disposable 0.1.51 API: offline synchronization,
  lost acknowledgements, ownership/revision conflicts, deferred photo batches,
  bounded/cancel/retry downloads and local recovery/cleanup passed.
- PostgreSQL upsert SQL was compiled to inspect the conflict targets and JSON
  binding. This is a syntax-generation check, not a live PostgreSQL race test.

The 28 skips remain 14 optional original Excel cases and 14 PowerShell 7 cases.
Live PostgreSQL contention, real Docker/deployment and physical Android/Windows
devices were not tested here. No UI/native C++ behavior changed in this round;
the earlier UI results are not presented as a fresh UI run.

## Deployment

Deploy server **0.1.51** for these fixes. Minimum client stays **0.1.48**; existing
0.1.48–0.1.50 apps remain compatible. Rebuilding the app is optional for this
server-only round and updates its version to 0.1.51 / Android code 163.
No reset or destructive database migration is needed. Fields lost by an earlier
re-import cannot be reconstructed automatically; re-enter them once through the
console or restore the appropriate backup. Future re-imports preserve unmapped
fields. The package contains source/build inputs, not a prebuilt Docker image.
