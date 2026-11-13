# Contract deletion and recovery — 0.1.47

## Administrator workflow

In Management, select the intended contract and choose **Apagar contrato
selecionado**. The confirmation names the contract and explains that its chargers,
reports and photographs will become unavailable. The administrator must type the
exact uppercase word **APAGAR**. Both the app and API enforce this confirmation.

**Recuperar contratos** lists recoverable contracts and their deadlines in the
device's local time. **Recuperar contrato** restores the same IDs, assignments,
reports, revisions and photo bytes; it does not create duplicate reports.

## Retention and offline behavior

The server records the deletion time in UTC and an immutable deadline exactly
30 days later. Retrying deletion does not restart that period. Restoration is
rejected at or after the deadline, even before the next cleanup sweep runs.

An API lifespan worker checks expired contracts every 60 seconds, including on
startup after downtime. Physical deletion takes place on the first successful
sweep after the deadline, while the API is running. Failures are logged and
retried. No external cron job is required. Multiple PostgreSQL workers skip
contracts already locked by another worker.

The sweep deletes photo BLOBs, reports, report deletion markers and associated
ownership history, import batches, assignments, chargers, the retention entry
and contract row in one transaction per contract. General audit events remain
as UUID/action metadata. Users and company import profiles are shared resources
and are retained. Other contracts are unaffected.

Deleted contracts disappear from active contract lists. Their catalogue, report,
photo, import and assignment endpoints return HTTP 423 until final purge. This
status preserves offline work; HTTP 410 is reserved for permanently deleted
individual reports. After restoration, technicians can refresh the catalogue
and press **Sinc.** to retry any queued local work. A stale device cannot recreate
a purged contract by uploading a report against its former charger UUID.

Server deletion does not remotely wipe smartphones or edit previously exported
PDFs/ZIPs. Existing database backups also retain their original snapshots; their
retention is managed separately. Recovery through the app ends after 30 days.

## API and locking

- `POST /api/contracts/{id}/trash`, JSON `{"confirmation":"APAGAR"}`.
- `GET /api/admin/deleted-contracts`.
- `POST /api/contracts/{id}/restore`.

All three require an authenticated administrator. Normal contract access first
takes a PostgreSQL shared contract-row lock, then reads the retention marker in
a fresh statement. Trash, restore and purge take an exclusive contract lock.
Report creation now obtains this contract lock before the charger lock. This
prevents writes from being accepted behind a committed deletion, while allowing
an operation already in progress to finish before deletion.

## Deployment and validation

Deploy the server and rebuild the app. Version 0.1.47 is the current required
client release; Android version code is 158. The new `contract_trash` table is
created automatically; existing databases and reports do not need a reset.
The normal deploy scripts still back up the database before code replacement.

Server tests cover authorization, exact confirmation, all resource gates,
idempotent retries, byte-identical restoration, the exact 30-day boundary,
foreign-key-complete purge, unaffected contracts, and startup cleanup. These
tests use SQLite; PostgreSQL locking behavior is implemented through SQLAlchemy
but has not been exercised against a live PostgreSQL server here.

QML tests cover administrator visibility, confirmation reset and recovery in
desktop, narrow and landscape layouts. Native Qt tests exercise actual HTTP
requests for trash/list/restore and preservation of unsent local photographs on
HTTP 423. Physical Android/Windows builds and real deployment remain to be run.
