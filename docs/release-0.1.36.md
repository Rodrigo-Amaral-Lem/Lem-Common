# Reviewed integration — Lem 0.1.36

Date: 2026-11-11. Integrates the supplied proposal against 0.1.35 R2, with the
additional corrections identified in review. No live server was contacted or
updated during implementation; tests use disposable local storage/API instances.

## Included client improvements

- QML bindings reuse the active report projection. Catalogue input snapshots avoid
  rebuilding QVariant rows for unrelated notifications, and the encoded catalogue
  comparison is cached. Search matches data values rather than JSON keys/UUIDs and
  waits 180 ms after typing. Contract cards, colors and scroll fixes remain.
- Reads of potentially absent reports use value() and group-boundary release
  ignores an absent report. Empty legacy cache placeholders are removed on load;
  non-empty damaged records are retained for recovery rather than discarded.
- PDF/ZIP requests allow 180 seconds without response data while rendering.
- Permanent 4xx rejection of one report does not block the following reports.
  Local data stays intact. Ownership/revision conflicts retain their stronger
  protection; network/5xx/408/429 failures retain retry/backoff behavior.
- Lost photograph-DELETE acknowledgements recover only with a matching deletion
  intent saved before sending, matching server revision/payload and absent photo.
  Successful acknowledgement clears the saved intent. This supplements, rather
  than removes, optimistic revision and ownership checks.
- Discarded camera results for deleted reports no longer block future captures.
  Deletion uses canonical-path containment in the private camera directory.
- Stored server preferences follow the existing HTTPS rule (HTTP loopback remains
  available for development).

## Included server improvements

- Long text-answer rows can span PDF pages. Excel previews without declared sheet
  dimensions read the bounded preview window instead of one cell.
- Uploads verify and decode JPEG/PNG before storage. Damaged JPEG/PNG produces 422;
  resource failures are not misreported as invalid user input. JPEG decoding uses
  DCT scaling and image handles are closed promptly.
- PDF renditions use DCT scaling. Previously stored undecodable images have a
  visible warning in the PDF; their available original bytes remain in ZIP exports.
- Original BLOBs are loaded individually rather than all at once. ZIP generation
  uses a temporary spool (16 MiB memory threshold) and stores already compressed
  originals without another compression pass. PDF renditions still require memory;
  this is not a claim of constant total rendering memory.
- IPv6 addresses share /64 login buckets; IPv4-mapped addresses share IPv4 keys.
- Interactive API docs/schema are off by default. Enabling them makes them public;
  it is a development option, not an authentication control.

## Corrections made to the proposal

1. Missing originals abort PDF/ZIP with HTTP 409 instead of silently omitting
   evidence. DB-read exceptions propagate separately from image decode errors.
2. Exports acquire a PostgreSQL shared report lock while generating documents,
   preventing administrative deletion midway through a closed-report export.
   SQLite cannot provide this row lock, so missing-evidence checks remain necessary.
3. Export/image admission fails fast with 503 and Retry-After before authentication
   retains a DB connection. There is no 20-second wait while holding a connection.
4. ZIP streaming releases the DB connection/report lock before sending file data.
   Its spool is closed even if the client disconnects before the first chunk.
5. Full upload decoding has its own admission limit. Limits apply per API process;
   the supplied deployment remains one worker. They bound concurrency, not a fixed
   RSS ceiling. Do not add workers without reviewing this and the login limiter.
6. New configuration flags are wired through Docker Compose, not only read in Python.

## Configuration

Optional values in deploy/.env, applied on API recreation/deploy:

```dotenv
LEM_EXPORT_CONCURRENCY=2
LEM_IMAGE_CONCURRENCY=1
LEM_API_DOCS=0
```

Export concurrency is clamped to 1–4 and image admission to 1–2; invalid numbers
fall back to defaults. Export slots remain reserved until the response finishes,
including ZIP streaming, but no DB connection is held during that streaming.
Busy clients receive 503 and should retry later. Keep the defaults unless server
memory and workloads have been measured. Existing file/pixel/report quotas remain.

## Validation

- **142 backend/deploy tests passed**, none skipped, including the original XLSM
  integration and PowerShell simulations. Seven new resource/completeness tests
  cover missing evidence, DB/MemoryError classification, concurrent export/image
  admission, connection release during streaming and spool closure on disconnect.
- Native controller rebuilt with Qt 6.10.2/Linux. Full C++/temporary API integration
  passed, including a deliberately lost DELETE acknowledgement and a 413-rejected
  report followed by a successfully synchronized report. Existing offline
  durability, ownership/conflicts, copying, deletion, batch photos and cleanup pass.
- Native local-PDF and catalogue-notification checks passed. QML checks passed for
  navigation, retained positions, scroll bounds, export visibility, version notices
  and Android Back behavior, without warnings.
- PostgreSQL row-lock semantics were reviewed in code, but no live PostgreSQL load
  test was performed. Windows/Android/iOS binaries were not generated or tested on
  physical devices. The Android-only camera branch was reviewed, not device-tested.
- Python formatting was checked with Black and modules compile successfully.

## Deploy

Update the server with the normal deploy script and rebuild/install app 0.1.36
(Android version code 140). **No database reset or schema change is required.**
Minimum compatible version stays 0.1.28; deploy promotes latest to 0.1.36 without
reducing a higher configured value. Earlier clients continue to work within the
configured compatibility policy. The supplied source does not update the local
Qt SDK or Android OpenSSL binaries; previous SDK security guidance still applies.
