# Lem source-code guide

This guide describes **0.1.32**, with a consistently named `Lem` C++ controller,
`lem` QML context and `Lem.cpp` / `LemOffline.cpp` / `Lem.h` source files.
The detailed English comments and formatting from the documented edition are retained.

## Start here

Read these in order when joining the project:

1. [Architecture and source map](architecture.md): which layer owns each responsibility.
2. [Client state and persistence](../../../App/docs/developer/client-state.md): what `Lem`, its properties and JSON fields mean.
3. [Offline synchronization](../../../App/docs/developer/offline-sync.md): ordering, acknowledgements, failure recovery and image storage.
4. [Server, database and API](../../../Server/docs/developer/server-and-api.md): authorization, transactions, endpoints and imports.
5. [QML UI](../../../App/docs/developer/qml-ui.md): controls, delegates, notifications and temporary presentation state.
6. [Platforms and deployment](platform-and-deployment.md): Android camera/TLS, storage migration and deployment scripts.
7. [Testing and maintenance](testing-and-maintenance.md): repeatable checks and change-review guidance.

For a short code tour, open [main.cpp](../../../App/app/src/main.cpp), then the public
properties/actions in [Lem.h](../../../App/app/src/Lem.h). Follow `answer()` to
`queueEdits()` to understand the responsive local path. Follow `syncNext()` and
`syncPhotos()` in [LemOffline.cpp](../../../App/app/src/LemOffline.cpp) for the
network path. On the server, follow `report_access()` and `put_report()` in
[main.py](../../../Server/server/app/main.py).

See the [validation record](readability-validation.md) for the checks run on this documented edition.

## Vocabulary

| Term | Meaning in this codebase |
| --- | --- |
| Contract | Client/year/semester/type context that scopes a charger catalogue and user assignments. |
| Charger / Station ID | A charger has an internal UUID and an imported `external_id`; the same external ID may appear in different contracts. |
| Report | One maintenance intervention on a charger, identified by its own UUID. |
| Draft | Mutable report controlled by its current owner. May exist only locally before its first successful upload. |
| Closed report | Completed locally or confirmed closed remotely; those are separate synchronization stages. |
| Checkpoint | One checklist question, e.g. `PC01.01`. `PCxx`/`PGxx` are question groups. |
| Payload | Answers, observations and report dates; separate from image bytes. |
| Snapshot | Charger/contract context frozen by the server when creating a report. |
| Dirty | Local work still needs reconciliation/acknowledgement; not necessarily an active network request. |
| Revision | Server-controlled optimistic concurrency number. Not the local edit counter. |
| Tombstone | Persistent record of a deleted report UUID, preventing stale recreation. |
| Owner | Current account allowed to edit/close a draft; can change through an explicit admin transfer. |

## Naming and compatibility

The product and C++ controller are **Lem**; QML exposes the instance as `lem`.
The deployed API/service/database identifiers retain **LEM**. The Android
application ID is `pt.lem.app` from 0.1.23, which is a new installation identity.
Synchronize pending work before switching from an older installation; private data
from a different Android package is not automatically accessible. Desktop settings
and app-data identity remain unchanged. Legacy desktop storage lookup keys remain
only for locating existing profiles.

The English comments explain intent and constraints. User-facing Portuguese
strings, JSON keys, exported filenames, table names and configuration keys retain
their original values. Existing release notes under `docs/` remain historical
records; this directory describes the current source rather than a proposed redesign.

Photo crop and video evidence: [ownership, limits, media validation, exports and tests](../evidence-media-0.1.52.md). Start with `app/qml/PhotoCropDialog.qml`, `app/src/EvidenceMedia.h` and `server/app/media.py`.
