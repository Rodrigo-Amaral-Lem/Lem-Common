# Cross-feature review — 0.1.49

This review traces the 0.1.46–0.1.48 changes together: measurement validation,
review navigation, progressive menus, grouped management, account administration,
retention/purge, ownership, offline sync and exports. No live service was accessed.

## Reproduced problems and fixes

| Area | Failure | Resolution |
| --- | --- | --- |
| Account deletion | Confirming an account identified by email could delete a different account if the email was reassigned while the confirmation prompt was open. | Bind confirmation to the original UUID; reload that exact active account after the prompt. |
| Forced contract purge | The CLI committed an expired deadline, released its contract lock, then purged in a second transaction. A restore could win in between; the CLI still reported success. | CLI and background sweeper share a purge helper. Forced deletion keeps its exclusive contract lock and commits all dependent deletion in one transaction. |
| Session revocation | A request could read a valid token, have it revoked during its user lookup, and still authorize the operation. | Acquire a shared User lock and recheck the token in a fresh query afterwards. Login also holds the User lock until token creation commits. |
| Password reset | A password prompt could wait while another operator deleted the account; resetting then modified the inactive account and reported success. | Release the preview transaction before prompting, then lock/reload the original active UUID before writing. |
| Charger metadata | Numeric serial/postal fields supplied through console JSON remained JSON numbers. Native QString readers could show them as empty. Invalid/non-finite coordinates could also reach storage/Maps. | Normalize textual metadata to strings, reject compound values in scalar fields, reject non-finite JSON numbers, and validate coordinate bounds/types. |
| Concurrent account creation | Two requests passing the email precheck could collide on the unique constraint and raise an internal server error. | Roll back the losing transaction and return HTTP 409 without database/password details. |

The first nine cases in `server/tests/test_cross_feature_review.py` were run
against the original 0.1.48 implementation: **all nine failed**. They all pass
after correction. They cover the first five rows, including four invalid-coordinate
variants. Two additional checks cover racing account creation and an existing
database upgrade that retains contracts, reports and original photograph bytes.

## Locking and integration hardening

A new singleton `account_admin_lock` table serializes console credential/role
mutations and the last-active-administrator check. It is created and initialized
automatically; no data reset is required. This replaces taking exclusive locks
on every administrator row, which could conflict with cross-account operations.

Console credential writes lock the target User with PostgreSQL NO KEY UPDATE,
before changing sessions/reports. This blocks concurrent API shared User locks
while permitting the FK KEY SHARE checks used by audit/ownership history during
cleanup. Ownership/assignment operations lock the active destination User before
contract/charger/report locks. Account changes do not hold write locks while
waiting for password input or APAGAR confirmation.

These ordering changes were reviewed in source and exercised through SQLite
interleaving regressions. **Actual PostgreSQL lock contention/deadlock testing was
not available here**; it remains a deployment-level validation item. Read-only
console charger listing now uses a shared contract lock rather than unnecessarily
excluding ordinary contract reads.

Token revocation adds one constant-size authentication query. The catalogue
regression still verifies a bounded number of bulk metadata queries, without
reading report payloads or photo BLOBs per charger. Purge uses bulk deletion
without loading photo data or materializing ORM identity lists.

## Verification performed

| Check | Outcome |
| --- | --- |
| Unmodified 0.1.48 baseline | 248 server/deploy tests passed, 28 skipped. |
| Full corrected server/deploy run | 257 passed, 28 skipped. |
| Final cross-feature regression run | 11 passed; includes two additional cases added after the full run, for 259 distinct backend/deploy cases verified overall. |
| Qt UI scripts | 25 checks passed, including desktop/mobile report flows, progressive gestures, review alignment, safe areas, desktop scrolling, account roles/debug toggle, exports, startup variants and photo delegate stability. |
| Build configuration | 21 tests and 16 subtests passed for Windows standalone configuration and Android OpenSSL discovery. |
| Native Qt C++ tests | Connector generation/PDF, stale auth replies, target-report photo validation, contract trash/restore, preservation of local work, report/photo projections, measurement formatting/NOK and offline PDF passed. |
| Real native client against disposable HTTP API | Offline ownership changes, revision conflicts, lost upload/delete acknowledgements, deferred photos, cancellation/retry, bounded downloads, local cleanup, nonblocking save operations and stale-copy deletion passed. |
| Native compatibility handshake | Latest/outdated-compatible/blocked/missing/malformed/wrong-echo/version-change-during-login policies passed. |

The 28 backend/deploy skips are 14 optional original Stations Excel cases and 14
PowerShell 7 cases. Original client Excel and PowerShell 7 were unavailable. Docker,
PostgreSQL, physical Android/Windows Qt 6.12 release builds, camera intents and the
remote deployment were not exercised. Native/QML tests use local Qt 6.10.2.

Three pre-existing UI test fixtures assumed Management was a single long form.
After the 0.1.48 split, the default Contracts area fits on screen and correctly
has no scrollbar/hide-on-scroll. The fixtures now select the longer Accounts area
when testing scrolling. Their original failures were stale test assumptions,
not changes made to the product to force scrolling onto a short page.

## Release/deployment

Deploy the 0.1.49 server package to obtain the corrections and the automatic
account-lock-table upgrade. Existing data and contract recovery deadlines are
preserved. Version 0.1.48 clients remain compatible (minimum 0.1.48, latest 0.1.49).
Rebuilding the app updates its version to 0.1.49 / Android code 161; no UI behavior
or offline file format changed in this review. The server source ZIP is build
input, not a prebuilt Docker image. Backups/offline copies keep their existing
retention policy.
