# Continued source review — 0.1.44

## Reproduced fixes

### Photograph mutation racing with report deletion

Both photograph upload and removal read the report during authorization, then
locked its row and called Session.refresh() on the original ORM object. If a
deletion committed in between, refresh raised InvalidRequestError rather than
returning an API-level deleted-report response.

Both handlers now select the report again under the lock with populate_existing,
check for a missing row (HTTP 410), then apply ownership/revision/state checks to
the locked current state. The missing-row path does not write a photograph or
advance a revision. Existing upload retry and photo removal idempotency remain.

`server/tests/test_review_044.py` injects a committed deletion immediately before
the locked select. Both tests failed against 0.1.43 with "Could not refresh
instance" and pass after this change. This is a deterministic interleaving in
SQLite, not a measurement of simultaneous transactions on PostgreSQL hardware.

### Obsolete HTTP response revoking a newer session

A logout request may remain in flight after local logout completes. A delayed
HTTP 426 from the previous server unconditionally cleared the current token and
installed its incompatibility policy, even after switching servers and logging
in again. The existing 401 token check also did not include server identity;
multipart responses had neither identity guard.

Ordinary and multipart requests now capture their originating server and token.
HTTP 401/426 authentication/policy side effects apply only if both still match
the active session. An old response cannot log out a new session. Matching
current-session rejections still revoke authentication normally.

The native `Lem-review-test` uses a real loopback HTTP connection: it sends an
old request, switches server/session before the rejection arrives, then checks
the new token survives. The old 426 test failed against 0.1.43. The corrected
code passes obsolete/current 401 and 426 cases. No live server is contacted.

## Validation and release

- Server/deploy suite: 149 passed, 28 skipped (original Excel workbook or PowerShell 7 required).
- Native C++ connector/PDF and recovered-photo regressions passed.
- Native HTTP regressions confirm obsolete rejections are isolated while current rejections still apply.
- Native offline client integration against a disposable HTTP API passed, including
  ownership/revision conflicts, lost acknowledgements, deferred photo batches,
  partial downloads, cancel/retry and local cleanup safeguards.
- Python source syntax and release alignment verified.

Native checks use local Qt 6.10.2. Physical Android, Windows release builds and
real concurrent PostgreSQL execution were not exercised here. QML and graphics
behaviour are unchanged from 0.1.43; no reverted Android lifecycle guard is added.

Files: app/src/Lem.cpp, app/tests/review_regressions.cpp,
server/app/main.py, server/tests/test_review_044.py, and release/deploy defaults.

Deploy the server and rebuild/install app 0.1.44 (Android code 152). Latest
supported client becomes 0.1.44; minimum stays 0.1.39. Existing data is retained.
