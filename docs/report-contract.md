# Current report contract

The canonical starting template is [shared/checklist-v1.json](../shared/checklist-v1.json), version
**6**. App and Server keep tracked copies. This guide describes the present source rather than the
superseded behavior of older version notes.

## Groups and answer shapes

| Order | Group | Current items before connector expansion |
| --- | --- | --- |
| 1 | SEG — Segurança | SEG.01–SEG.07 |
| 2 | SITE | SITE.01–SITE.06 |
| 3 | QVE | QVE.01–QVE.14 |
| 4 | EST — Estado Geral | EST.01–EST.18 |
| 5 | MAN | MAN.01–MAN.21 |
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

| Flag/kind | Current meaning |
| --- | --- |
| `kind: status` | OK/NOK/N/A controls and status-value validation |
| `kind: text` | Entered text/measurement; numeric grammar depends on the measurement key |
| `kind: notes`, `optional: true` | Optional observations/media, no status controls and no mandatory value |
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
- **MAN.21 — Observações gerais da manutenção:** optional note, photographs and videos, no status
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
  preserves the reading, and editing the reading preserves the evaluation. A literal OK/NOK value
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
| MAN.18 | Up to 5 integer digits and 2 decimals; Ω; no automatic earth-resistance threshold is defined here |

Decimal point or comma is accepted; display normalizes to comma and unit. An out-of-range voltage
remains recordable and is marked in the interface/PDF. It is not rejected merely because it is
outside the compliance band. Partial draft typing can remain incomplete; closure validates a
finished value.

## Required photographs and connectors

The template's required-photo items are SEG.01, SITE.02–SITE.04, QVE.01/QVE.04,
EST.01/EST.05/EST.06/EST.13/EST.16, MAN.04–MAN.10/MAN.12, each generated CARG.01.xx, CARG.05 and
FIN.01. N/A exempts a photograph, including MAN.12.

Connector configuration expands one CARG.01.xx per physical connector, including repeated types.
Known aliases normalize to common names; invalid counts/types are rejected. The implementation
allows up to 64 configured connectors and retains a fallback question when type information is
unavailable. [Connector cases](../shared/connector-cases.json) are shared across implementations.

Each CARG.01.xx and CARG.05 requires an observation for N/A and a photograph for an applicable
result. A video or unrelated checkpoint's photograph does not satisfy a mandatory photograph.
Changing connector configuration later does not silently rewrite an existing closed report's frozen
questions.

## Template history and station identity

New reports use today's template/connector expansion. Existing reports must send their saved
`checklist_version`. Current editable v6 reports receive targeted corrections: group order, safety
controls, manual fields and missing optional general-note items. **Closed reports retain the saved
template.** Older checklist versions are not automatically reinterpreted as v6.

EST.02, EST.03 and EST.04 map to station manufacturer, model and serial. When closure succeeds,
changed non-N/A values can update the physical station and the report's closing snapshot.
Conflicting concurrent corrections are rejected. A stale import must not undo verified station
fields.

## Copy provenance and evidence

QVE copying covers the entire QVE group, including QVE.14. Measurement copying covers only
MAN.04–MAN.10, not all MAN fields or MAN.21. Sources must be another charger in the same contract.
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

## N/A observations and suggestions

N/A requires an observation in SEG.01/02/04, SITE.02–04, QVE.02/04/09–12, EST.01/16/17,
MAN.12/13/18/20, each CARG.01 connector and CARG.05. `na_notes_default` supplies an editable
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
