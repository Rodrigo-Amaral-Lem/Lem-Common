> Integrated and revised in 0.1.36 after additional review. See [release validation](release-0.1.36.md) for the final behavior and tests; the notes below describe the original proposal.

# Review fixes after 0.1.35 R2 (2026-11-10)

Version identifiers, the client policy and the database schema are unchanged. Update the
server and rebuild the app; no database reset.

## Server (covered by `server/tests/test_bug_regressions.py`)

- **Long text answers no longer break PDF/ZIP export.** Checklist rows may split across
  pages (`pdf_report.py`). A 3000-character answer previously raised `LayoutError`.
- **Uploads are fully decoded before being stored** (`app/images.py`, used by
  `PUT /api/reports/{id}/photos/{pid}`). A truncated JPEG was accepted by `Image.verify()`
  and later made the closed report unexportable; a damaged PNG raised `SyntaxError`
  (HTTP 500, retried forever by the app). Both are now HTTP 422.
- **Already stored damaged photographs** are listed in the PDF as unreadable instead of
  failing the export. Originals remain in the database and ZIP.
- **JPEG renditions use DCT scaling** (`draft`), roughly halving decode time per photograph.
- **Import preview** shows the normal 12 x 60 window for workbooks without `<dimension>`
  (previously a single cell).

## App (not compiled in the review environment: build and run `Lem-offline-test`)

- **Lost acknowledgement of a photograph deletion** is recognised (server revision is
  exactly one ahead, same answers, photograph already absent) instead of becoming a
  durable conflict (`LemOffline.cpp`, `syncNext`).
- **A report the server keeps rejecting (400/404/413…) no longer blocks the reports queued
  after it.** It is set aside as "needs attention" like 422; only 403/409 mark a durable
  conflict. Network errors, 5xx, 408 and 429 still retry with backoff.
- **No placeholder entries in the report cache.** Reads of reports that may be missing use
  `value()`; existing null/ID-less entries are dropped when the cache is loaded.
- **Catalogue search matches values only** (ID, details and imported columns), not JSON
  field names or UUIDs (`Main.qml`, `chargerMatches`).

## Second pass: performance and hardening

### Server

- **Exports use bounded memory.** PDF/ZIP load one photograph at a time instead of every
  BLOB of the report; the ZIP is written to a spooled temporary file and streamed
  (`app/exports.py`). Photographs are stored uncompressed inside the ZIP (already JPEG/PNG).
- **At most `LEM_EXPORT_CONCURRENCY` exports run at once** (default 2). A request that waits
  more than 20 s receives HTTP 503 with `Retry-After`.
- **`/docs`, `/redoc` and `/openapi.json` are disabled** unless `LEM_API_DOCS=1`.
- **Login rate limits group IPv6 clients by /64**; IPv4-mapped addresses count as IPv4.
- A photograph upload retry compares identity columns without loading the stored image.
- The checklist is read explicitly as UTF-8.

### App (not compiled in the review environment)

- **Catalogue rows are rebuilt only when chargers or report summaries change**, not on every
  `changed()` (which fires for each typed character).
- **QML bindings read `win.reportData`** (one conversion of the active report per
  notification) instead of `lem.current` (one full conversion per binding). Handlers that
  run right after a `lem` action still read `lem.current`.
- **Catalogue search waits 180 ms after typing** and no longer re-serializes the displayed
  catalogue on each refresh.
- PDF/ZIP downloads allow 180 s without data while the server renders.
- A camera result for a report deleted meanwhile is discarded instead of blocking the camera.
- A stored server preference that is not HTTPS (or HTTP on localhost) falls back to the default.

### Deliberately not changed

- Full cache checkpoint (`persist()`) after each synchronization acknowledgement: replacing
  it touches the journal/`_edit_seq` recovery rules and needs the offline test suite.
- Photograph delegates are still recreated when the report projection changes.
- Password hashing parameters, account lockout policy, access revocation endpoints and
  container memory limits: these are product/operations decisions.
