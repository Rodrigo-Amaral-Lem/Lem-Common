# Second bug review — 0.1.50

This pass focused on operator prompts, report immutability, metadata supplied by
the maintenance console and its interpretation by the app/Maps/PDF paths.

## Findings and corrections

1. **Report deletion after a stale confirmation.** The console displayed a draft,
   waited for APAGAR, then deleted whichever revision existed afterwards. A
   technician could finish or edit the report during that wait and lose the new
   work. The console now captures the preview revision/status before prompting,
   re-reads under the report lock and aborts if either changed. The operator must
   inspect and confirm again. Unchanged drafts and closed reports remain deletable.

2. **Metadata overriding the real charger ID.** A JSON `external_id` inside charger
   details could shadow the authoritative Charger column when the server froze a
   new report snapshot. App-created snapshots already favored the column, so the
   first sync could change the report/PDF's displayed ID. Server snapshots now
   write the authoritative column last. The console rejects reserved `external_id`
   in details and directs the operator to `--external-id`; unrelated updates also
   remove an old reserved detail key. Existing frozen reports are not relabeled.

3. **Coordinate formats accepted by the console but rejected by Maps UI.** Python
   accepts text such as `1_0` or `+1e1` as floats. The console validated them but
   retained the original strings, while QML intentionally rejects such strings.
   Validated coordinates are now stored as JSON numbers; decimal-comma input
   continues to work. Invalid/non-finite/out-of-bounds values remain rejected.

4. **Tiny numeric coordinates.** JavaScript may stringify a valid number close to
   zero as `1e-10`, which the strict imported-string parser rejected. QML now
   validates numeric values directly and retains strict validation for strings.
   Maps URLs expand small-number exponents to plain decimal without rounding.
   The coordinate/address priority, fixed HTTPS host and URL encoding are unchanged.

5. **Measurement clear usability.** With NA selected, the numeric editor contains
   no editable NA text; Backspace therefore cannot clear that stored selection.
   Measurement fields now have an explicit erase icon alongside NA, consistent
   with status-answer controls. It clears only the answer, preserving observations
   and photographs. Clearing restores the normal missing-answer review condition.
   Pressing NA again continues to select NA; it is not an implicit toggle.

## Evidence and regression checks

`server/tests/test_review_050.py` contains seven cases. Against the previous
implementation, five failed and two already-valid coordinate cases passed.
All seven pass after correction. The pre-fix Maps test also failed for numeric
`1e-10`; it now passes, including an intercepted real button launch (no external
Google Maps connection). Existing report/account deletion tests still pass.

- **266 server/deploy tests passed; 28 optional cases skipped.** Skips remain
  14 original Stations Excel cases and 14 PowerShell 7 cases, unavailable here.
- **25 UI checks passed**, covering groups, review positioning, progressive scroll,
  desktop input/bars, Android safe-area propagation, account roles/debug reveal,
  photos, exports and startup variants. Additional focused measurement, Maps,
  mobile report and review tests passed after the final clear-control adjustment.
- **21 build-configuration tests and 16 subtests passed** for Android OpenSSL
  discovery and Windows standalone configuration.
- The existing native **0.1.49 client** passed the offline integration runner
  against the disposable **0.1.50 API**: ownership conflicts, lost acknowledgements,
  deferred photos, bounded/cancel/retry downloads, local cleanup and nonblocking
  edits were exercised. No native C++ implementation changed in this release.

Tests used SQLite and Qt 6.10.2 offscreen. Live PostgreSQL contention, Docker/remote
deployment, physical Android/Windows Qt 6.12 builds and actual camera/Maps apps
were not exercised. This review does not claim that every possible bug is absent.

## Deployment

Deploy server 0.1.50 and rebuild the app to get the complete set of corrections,
including Maps and the measurement erase control. Minimum client remains 0.1.48;
0.1.48 and 0.1.49 clients remain compatible with the updated server. Android code
is 162. No database reset/migration is needed beyond the automatic initialization
already provided by 0.1.49. Existing report snapshots and recovery deadlines are
preserved.
