# Current report contract

The canonical starting template is [shared/checklist-v1.json](../shared/checklist-v1.json), version
**7**. App and Server keep tracked copies. This guide describes the present source rather than the
superseded behavior of older version notes.

## Public report identifiers and export names

Closed reports display `ChargerID_YYYY-MM-DD_HH-mm-ss_Contract`, using the frozen charger ID and
contract name plus the completion instant in `Europe/Lisbon` (including daylight saving time).
Spaces and filename-forbidden characters become hyphens; Unicode accents are preserved. Charger
and contract components are capped at 72 and 112 UTF-8 bytes so names fit common filesystems.
The PDF and ZIP filenames, and the PDF inside the ZIP, use this identifier. `report.json` retains
its technical archive name and carries the public `identifier` alongside the internal UUID `id`.

Drafts display `ChargerID_Rascunho_Contract`; legacy closed records without a valid completion
instant use `sem-data_sem-hora`. Exporting again does not change the timestamp. Internal UUIDs,
API paths, synchronization, ownership and evidence links remain stable within an intervention;
administrator correction explicitly replaces it with a new UUID as described below. App/Server share
[naming cases](../shared/report-naming-cases.json) to keep online and offline outputs consistent.

## Groups and answer shapes

| Order | Group | Current items before connector expansion |
| --- | --- | --- |
| 1 | SEG — Segurança | SEG.01–SEG.07 |
| 2 | SITE | SITE.01–SITE.06 |
| 3 | QVE | QVE.01–QVE.14 |
| 4 | EST — Estado Geral | EST.01–EST.09, EST.11–EST.18 |
| 5 | MAN | MAN.01–MAN.22 |
| 6 | CARG | One CARG.01.xx per connector, plus CARG.04–CARG.07 |
| 7 | FIN | FIN.01–FIN.03 |

Answers live in `payload.answers[checkpoint]`:

```json
{
  "value": "120 Ω",
  "assessment": "OK",
  "notes": "Terra medida no local"
}
```

`assessment` is used only where `reading_required` permits an independent OK/NOK evaluation; it is
not a replacement for `value`. `notes` is the observation. Status questions use empty/OK/NOK/NA on
draft input; a required item must have an answer before closure. Numeric not-applicable values
normalize to `Não Aplicável`. Use the item kind/flags rather than inferring behavior from an ID
number.

Text values and ordinary observations remain limited to 8000 characters. `kind: notes` observations
allow 32000 characters so merging previously valid fields does not strand an old draft/correction
(the v6 collision migration can merge three 8000-character fields). The total serialized payload
limit remains 300000. Validate after normalization, preserve complete merged text and never truncate
to make an old report pass. PDF/ZIP must retain the entire observation across page boundaries.

| Flag/kind | Current meaning |
| --- | --- |
| `kind: status` | OK/NOK/N/A controls and status-value validation |
| `kind: text` | Entered text/measurement; numeric grammar depends on the measurement key |
| `kind: notes`, `optional: true` | Optional observations/media, no status controls and no mandatory value; PDF shows `Sem observações` when empty |
| `allow_status`, `reading_required` | Separate evaluation controls alongside a required reading or N/A |
| `photo_required` | Require a real photograph when applicable |
| `photo_always` | Do not exempt the photograph for N/A |
| `na_notes_required` | N/A needs an explanation |
| `notes_disabled`, `media_disabled` | Hide observation/attachment controls; existing historical data is not silently deleted |
| `na_notes_default` | Editable suggestion when entering N/A with empty notes; unchanged suggestion is removed when leaving N/A |
| `notes_button_hidden` | Hide the observation toggle; required fields still open automatically |
| `notes_visible` | Keep the observation field visible, including FIN.02 without general media controls |
| `supports_signature` | Allow a signer name and referenced signature evidence |

## Current exceptions and optional fields

- **SEG.01:** N/A requires an observation explaining why the safety area is not applicable; N/A still exempts the photograph.
- **SEG.02–SEG.06:** NOK requires an observation, shown automatically without an observation button.
  SEG.02 and SEG.04 also require an observation for N/A. New media controls remain hidden.
- **SEG.07 — Observações gerais de segurança:** optional note and media, no status buttons.
- **SITE.06 — Observações gerais do local:** optional note, photographs and videos, no status buttons.
- **QVE.14 — QVE - Observações gerais:** optional note, photographs and videos, no status buttons.
- **MAN.22 — Observações gerais da manutenção:** optional note, photographs and videos, no status
  buttons.
- **EST.04:** accepts multiple charger/dispenser serial numbers in one text field; photograph is
  optional.
- **EST.18 — Observações gerais do equipamento:** optional note, photographs and videos, no status buttons.
- **CARG.07:** optional general observations, photographs and videos, no status buttons.
- **FIN.02:** general media controls are hidden; notes and dedicated signature controls remain available.
- **MAN.02:** OK/NOK/N/A; NOK requires an observation, N/A does not.
- **MAN.12:** requires an entered current-trip result or N/A, with a photograph when applicable. N/A requires an observation but exempts the photograph.
  OK/NOK is an independent evaluation and cannot fill the value.
- **MAN.14–MAN.17:** require a manually entered insulation result or N/A. Instrument text such as
  `>500 MΩ` or `OL` remains possible; do not impose the voltage grammar on these fields.
- **MAN.18:** numeric earth resistance in Ω or N/A, with independent OK/NOK. Changing the evaluation
  preserves the reading; valid MAN.11 triggers recalculation when either reading changes. A literal OK/NOK value
  alone cannot satisfy closure.
- **MAN.19:** status choices OK/NOK/N/A.

NOK normally requires an observation when selected as the value or separate assessment, including SEG.02–SEG.06. Selecting N/A clears an independent assessment. Returning from N/A to an
evaluation requires re-entering the reading. An empty temporary numeric edit does not silently
remove an assessment.

## Numeric formatting and limits

The shared [measurement cases](../shared/measurement-cases.json) exercise the Python, C++ and
JavaScript implementations. Current MAN keys map to legacy PC02 keys internally for compatibility;
keep those mappings stable.

| Measurements | Numeric grammar / classification |
| --- | --- |
| MAN.04–MAN.06 | Up to 3 integer digits and 2 decimals; V; 360–440 inclusive is in range |
| MAN.07–MAN.09 | Up to 3 integer digits and 2 decimals; V; 207–253 inclusive is in range |
| MAN.10 | Up to 3 integer digits and 2 decimals; V; 50 or higher is flagged out of range |
| MAN.11–MAN.12 | Up to 6 integer digits, no decimals, mA; configured MAN.11 must exceed zero at closure |
| MAN.18 | Up to 5 integer digits and 2 decimals; Ω; automatic comparison against 50 / (MAN.11 / 1000), with the temporary criterion described below |

Decimal point or comma is accepted; display normalizes to comma and unit. An out-of-range voltage
remains recordable and is marked in the interface/PDF. It is not rejected merely because it is
outside the compliance band. Partial draft typing can remain incomplete; closure validates a
finished value.

## Required photographs and connectors

The template's required-photo items are SEG.01, SITE.02–SITE.04, QVE.01/QVE.04,
EST.01/EST.05/EST.06/EST.13/EST.16, MAN.04–MAN.10/MAN.12/MAN.14–MAN.18/MAN.21, each generated CARG.01.xx, CARG.05 and
FIN.01. N/A exempts a photograph, including MAN.12.
MAN.14–18 require a photograph for either OK or NOK and an observation for N/A. Any mandatory
evidence requirement always means a photograph; videos never satisfy it. Editable v6 drafts migrate to v7 on client and server. Already closed snapshots remain intact; an administrator correction copy adopts v7 before editing.

Connector configuration expands one CARG.01.xx per physical connector, including repeated types.
The displayed Type 2 name is **AC Type 2**. Import and connector parsing continue to accept
`Mennekes Type 2`, `Mennekes`, `Type 2` and `T2` as legacy aliases. Compare canonical connector
names, order and counts during first synchronization, so the wording change alone is not a
configuration conflict. Existing frozen connector labels/metadata use the new name for display
and PDF export without changing answers, evidence IDs or the original Excel source cells.
Known aliases normalize to common names; invalid counts/types are rejected. The implementation
allows up to 64 configured connectors and retains a fallback question when type information is
unavailable. [Connector cases](../shared/connector-cases.json) are shared across implementations.

Each CARG.01.xx and CARG.05 requires an observation for N/A and a photograph for an applicable
result. A video or unrelated checkpoint's photograph does not satisfy a mandatory photograph.
Changing connector configuration later does not silently rewrite an existing closed report's frozen
questions.

## Template history and station identity

New reports use template v7. Editable v6 reports, including correction copies of closed reports,
upgrade atomically: MAN.21 general notes/evidence move to MAN.22; EST.10's full answer is archived
under `payload.retired_answers`, its notes/evidence move to EST.18. New MAN.21 needs after-maintenance
photographs (or an N/A observation). EST.01 includes before-cleaning views, EST.13 only tariff and
EST.16 only DGEG stickers. EST.15 N/A suggests `Sem POS`.

Explicit legacy A/mA values convert to integer mA only when unambiguous. Otherwise `previous_value`
retains the original while the current reading becomes empty for confirmation. Both pending and
in-flight payloads receive the same projection. Closed originals remain unchanged until a validated
correction commits; existing revisions and ownership checks still apply.

Already-closed offline v6 reports use `frozen_history: true` during staged draft/evidence/closure
upload. The server marks `template.frozen_upload` until closure; this staging record cannot be edited
or converted by another device. The immutable v6 template is retained in `shared/checklist-v6.json`.
New editable requests must use v7. This is not permission to create new v6 interventions.

Corrections of pre-v6 closed reports also adopt the current form. Since older IDs could mean
different questions, previous values and notes become separate optional `ANT` notes fields,
and evidence moves to their corresponding historical fields. This preserves full-length text
without reinterpreting a serial number as a manufacturer. The administrator must complete the
current questions and sign again; old signatures remain historical evidence. Both GET and the
transactional write use the same projection for a correction already opened by an older app.

EST.02, EST.03 and EST.04 map to station manufacturer, model and serial. When closure succeeds,
changed non-N/A values can update the physical station and the report's closing snapshot.
Conflicting concurrent corrections are rejected. A stale import must not undo verified station
fields.

## Copy provenance and evidence

QVE copying covers the entire QVE group, including QVE.14. Measurement copying covers only
MAN.04–MAN.10, not all MAN fields or MAN.21/MAN.22. Sources must be another charger in the same contract.
The source remains unchanged; new evidence IDs/files are staged and committed atomically for the
target group after successful preparation.

`payload.qve_copy` and `payload.measurement_copy` record `source_report_id`, `source_charger_id`,
`source_station_id`, `copied_by` and `copied_at`. The client prefers cached source answers,
downloading missing evidence if necessary. One other group copy can be queued in memory while the
first runs; it is not a restart-persistent job queue.

## Signatures and exports

FIN.02 supports a technician name and `payload.signatures[checkpoint]` containing `photo_id`,
`signed_by` and a timezone-aware `signed_at`. The referenced evidence must belong to that
checkpoint and be PNG. Changing the signer invalidates the old signature. A drawing or
desktop-imported JPG/PNG is normalized into the same signature flow; ordinary attachments elsewhere
cannot stand in for that reference.

A signature reference that exists must be valid at closure; the current `supports_signature` flag
itself is not a universal requirement to sign every report. Empty general observations remain
optional.

The server exports closed reports using saved snapshots/templates. ZIP contains the PDF, report JSON
and original media arranged by checkpoint; PDF and local rendering retain the reading and
independent assessment. Evidence limits and security boundaries are in [Security](security.md).

The app also exports a closed report locally when every original is available, without requiring
network access or prior synchronization. Local ZIPs use the same PDF name and media folder structure,
preserve original bytes, and include `sync_pending` in `report.json` to identify unacknowledged local
work. Public report/evidence fields are exported; private paths, upload flags and conflict/in-flight
state are excluded. Exporting does not change the report's owner, status, revision or sync state.

## N/A observations and suggestions

N/A requires an observation in SEG.01/02/04, SITE.02–04, QVE.02/04/09–12, EST.01/16/17,
MAN.12–18/20, each CARG.01 connector and CARG.05. `na_notes_default` supplies an editable
suggestion only on transition into N/A with empty notes. Existing notes are preserved; clearing
a suggestion remains possible and leaves the item pending. The server validates the submitted
observation without generating an unconfirmed explanation.

When leaving N/A (OK, NOK or clearing), the client removes notes only when they exactly match
that item's `na_notes_default`; custom notes remain. Generated CARG.01 connector items inherit
“Veículo usado não compatível”. MAN.11/12 use “intensidade”; MAN.18 displays NA in its value field
when N/A is selected, retaining the existing not-applicable storage representation.

QVE.03 has an optional N/A suggestion; it does not require an N/A observation. Legacy free text
in a status item (such as MAN.02) stays available until the technician chooses OK/NOK/N/A. Local
review, local closure and the server reject other status values rather than closing locally and
failing only on upload.

FIN.02 requires a technician signature to close current v6 reports. Unsigned drafts can be saved. The signature must match the technician name and reference a PNG attached to FIN.02; changing the name requires signing again. Existing v6 drafts receive this rule; closed history is preserved.

## Administrator correction of closed reports

Windows/Linux desktop administrators can create a private working copy of a closed report.
The server clones its answers, frozen context and original evidence under new UUIDs, remapping
signature references. The editor owns the working draft; the completed replacement retains the
original technician's ownership. Existing evidence does not need a download/upload round trip.
Start and finish accept timezone-aware instants, with finish at or after start. Every correction
has a new internal UUID. Changing only the start preserves the public filename; changing finish
updates its Lisbon date/time components.

Ordinary PUT cannot close a correction. The commit operation validates the complete copy and
compares both revisions before replacing the source in one transaction. Invalid/incomplete data,
concurrent corrections, cancelled requests and storage failure preserve recoverable work. Cancel
removes only an editing copy; a delayed cancel cannot delete an already committed replacement.
The source remains available until commit and cannot be directly deleted while a copy is editing.

Replacement tombstones include `replacement_id`; catalogue rows include `report_replacements`.
Clients remove clean old copies but retain unsent changes as protected conflicts. A lost commit
acknowledgement is recovered from the saved replacement without duplicating the report. Explicit
permanent deletion and correction replacement remain distinct operations.

Changing EST.02/03/04 in a closed-report correction updates manufacturer/model/serial for the
physical station (all contract memberships) in the same transaction as replacement, including
legacy templates. Only changed, non-empty, non-N/A values are applied. If another intervention
changed the same field to a different value since the saved snapshot, commit returns 409 and
preserves both reports and the current station. Unchanged fields never revert newer values.
Staging, cancellation and failed commit leave the station untouched; verified changes resist stale
Excel imports. Other closed reports keep their frozen snapshots. Committed corrections return
live `station_update` data on commit and GET, so clients recover lost acknowledgements without
projecting old historical answers into the catalogue. Replaying a committed request does not
apply its identity edits again. This additive behavior remains compatible with admitted clients;
it does not raise the minimum app version.

## Contract report presentation

Only administrators choose the issuer (`Lem` or `CSMTEC`) and zero, one or two
additional client logos (primary then a different secondary). The issuer appears
at the upper left; client logos appear side by side at the upper right. Lem uses
turquoise; CSMTEC uses blue/yellow. Both use the same layout, evidence rules and fonts.

Import preview/commit accept `report_issuer`, `report_logos` and `branding_revision`.
Preview writes nothing; commit saves settings atomically with the chargers. These
contract-specific keys are excluded from reusable company import profiles. Omitting
settings preserves them for old clients; new contracts default to Lem and no client logos.
The admin `PUT /api/contracts/{cid}/presentation` accepts `issuer`, `client_logos`
(catalogue IDs), and required `base_revision`. It rejects stale settings with 409.

Contract/full-report responses include `presentation` with issuer, revision and
embedded client artwork. Settings changes affect subsequent exports of existing
closed reports too. Frozen answers, identity, owner, closure and report revision do
not change. Devices receive settings on refresh/sync, including protected dirty
copies; offline exports use the latest locally received settings. Previously saved
PDFs do not change. Old offline snapshots without `presentation` fall back to Lem
and their frozen `report_logos`. Issuer logos cannot occupy client slots.

The settings writer verifies the PUT with an independent, non-cacheable
`GET /api/contracts/{cid}/presentation`. It applies the confirmed issuer, logo IDs and revision
before refreshing the catalogue; a failed catalogue refresh cannot undo that save. Lost PUT
acknowledgements and retries recover only if this read proves the requested settings. Success,
failure and in-progress feedback remain beside the controls even when the global status changes
to “Catálogo atualizado”. Selecting a different value still requires **Guardar formato dos reports**.
Individual/batch evidence downloads do not prevent this independent metadata write. Permission,
session and foreground-operation gates are enforced in C++ and exposed to the button.

Online exports also read the current presentation before local rendering, so a device need not
manually refresh first. Lower presentation revisions cannot undo a newer acknowledged choice.

Pre-branding cached reports may have neither `contract_id` nor an ID in their frozen contract
snapshot. The client resolves their charger through available catalogues; if those are absent,
an online export reads `GET /api/reports/{rid}` for the authoritative contract ID and presentation.
Only that metadata is applied, including when an administrator exports a technician's report.
Answers, evidence paths, owner, closure, report revision and dirty state are preserved. A failed or
malformed contract lookup cancels the export and preserves its destination; it must not silently
produce a LEM document. No contract is guessed from the currently selected tab or a display name.

`contract_branding` and `contract_report_styles` are additive tables and follow
contract trash/restore/purge. PostgreSQL settings writes lock the contract exclusively;
exports hold its shared lock until metadata and original bytes are staged, then release it before
PDF rendering/ZIP assembly. An already accepted export keeps that snapshot even if branding or
the source report is replaced during rendering; subsequent exports use the newer state.
Both databases use an atomic compare-and-swap on the
presentation revision, including its first insertion. Issuer and client artwork are
read in one SQL snapshot, preventing mixed settings on SQLite too.
The write verifies its claim with `RETURNING contract_id`, not the driver's INSERT `rowcount`:
psycopg can report `-1` after SQLAlchemy closes the cursor even though insertion succeeded.
Treating that value as a conflict rolled back the first presentation save on PostgreSQL.

Canonical artwork derives from the user-managed Brand_Images preferences. The issuer
assets follow Lem's `lem-logo-tight.svg` and CSMTEC's `CSMTEC.svg`. Client artwork retains
standard colour Galp, APS_noborders and the other companies' preferred files. Alsa's
SVG-named source is WebP; Siemens.svg contains PNG bytes; Barraqueiro uses unaccented
reconstruido. Original folders are unchanged. Artwork retains its trademark ownership
and is not relicensed as application code. APS retains its white background, original
colours, minimum 14 mm height and safety margin. Publish shared assets with
`tools/sync_shared.py --write` and rebuild the application.

## PDF presentation

PDF exports omit the charger `location` (Local) field while retaining the address (Morada).
Empty observation-only items display `Sem observações`; ordinary unanswered checklist items
retain `Por preencher`. Written notes and historical values remain visible.
Evidence attached to an optional observations item is independent of its text: photographs appear
in the PDF and every photo/video original belongs in the ZIP, even with an empty or null answer.
After correction migration, use the migrated checkpoint (including historical `ANT` items) when
associating evidence; never drop it because the original question code changed.

`shared/report/layout.js` is the single layout; `styles.json` contains issuer artwork
and colours; `fonts/` contains licensed DejaVu Sans regular/bold. Native C++ and the
server's isolated PySide6 worker execute the same JavaScript through Qt 6.12 QJSEngine
and draw through QPdfWriter. The bundled fonts avoid reliance on system fonts. Native
painting adapters and server worker primitives must remain equivalent.

The server starts a hidden/offscreen subprocess per admitted export, with private
temporary evidence files and a 180-second timeout. Originals remain unchanged in ZIPs.
Missing originals abort export; damaged historical images produce a visible warning
in both generators. Font ligatures are disabled; equal-length ToUnicode corrections
preserve copied spaces and canonical omega without changing PDF offsets. The shared
measurement formatter follows the app's validated rules; run measurement/PDF tests
when those rules change. Update and publish all shared files together.

## Calculated assessments and suggested observations (v7)

MAN.12 is NOK at or below 0.5 × MAN.11 or at or above 1.05 × MAN.11, including both endpoints.
MAN.18 is NOK when R > 50 / (MAN.11 / 1000); equality is accepted. Otherwise it is OK, with the
high-earth observation when R > 50 Ω. Exact integer cross-products avoid rounding at boundaries.
Both implementations share `maintenance-cases.json`; the server recomputes the assessment even if a
client sends OK. Invalid/NA/zero configured current never enters division or generates a result.

The MAN.18 criterion hint is hidden in the form, including saved templates (user request,
2026-11-17). Removing this display text does not alter the calculation or validation rules.
The 50 V criterion is temporary, per user instruction. RTIEBT 413.1.4.2 defines the TT condition
RA × Ia ≤ 50 V; RA includes electrode/protective-conductor resistance and Ia is IΔn for an RCD.
[Portaria 252/2015](https://diariodarepublica.pt/dr/detalhe/portaria/252-2015-70055493) adds section 722.
[CTE64 guide, edition 3, 5.3.2, page 28](https://www.iep.pt/wp-content/uploads/2023/10/Guia-VE-Ed.3-2023.pdf)
specifies 25 V for publicly accessible outdoor charging installations. The current calculation must
not be presented as proof that the 50 V criterion applies to every installation.

`answer.suggested_notes` stores the exact generated text; only a matching, untouched suggestion
is cleared on state change or user focus in the notes editor. Custom/modified text survives, even
if a user later types the same words as the suggestion. `auto_assessment` identifies calculated
states for invalid-reference cleanup. Client input offers suggestions; server validation does not
reinsert a dismissed suggestion. A calculated NOK still requires a nonempty observation at closure.
