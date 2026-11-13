# Measurement fields and voltage nonconformity — 0.1.46

## Fields

| Checkpoints | Input | Canonical example |
| --- | --- | --- |
| PC02.05–PC02.11 (voltage) | 1–3 integer digits, optionally 1–2 decimal places | 238,3 V |
| PC02.19 (earth resistance) | 1–5 integer digits, optionally 1–2 decimal places | 4564,4 Ω |

Comma and period are accepted as decimal separators; storage/display use comma.
Zero is valid. Negative values, exponents, thousands separators, excess digits,
third decimal places and mixed units are rejected as complete measurements.
The unit may be typed or omitted; it is appended when editing finishes or when
the report is closed. No trailing-zero padding is forced.

The alternative is `Não Aplicável`; unaccented/case-insensitive spelling and
NA/N/A are accepted and normalized to that canonical text. A dedicated button
makes this available on Android's numeric keyboard. It exempts required photos
for that measurement, matching the previous NA semantics.

Isolation tests PC02.15–PC02.18 use MΩ and are intentionally unchanged: they are
not the earth-resistance field requested here.

## Automatic voltage NOK

| Checkpoints | NOK condition |
| --- | --- |
| PC02.05–PC02.07, phase-to-phase | below 360 V or above 440 V |
| PC02.08–PC02.10, phase-to-neutral | below 207 V or above 253 V |
| PC02.11, N–T | greater than or equal to 50 V |

360/440 V and 207/253 V are accepted inclusive boundaries; N–T 50 V is NOK.
The numeric reading is never replaced with the word NOK. The UI shows a red
`NOK — fora dos limites` indication while editing and in read-only reports.
Both native offline PDF and server PDF include the reading/unit plus the red NOK
indication. Nonconformity does not prevent recording or closing a complete report;
format errors and missing required evidence still prevent closure. This change
does not impose a new earth-resistance nonconformity rule or require new notes
for a numeric nonconformity. Existing explicit NOK-status note rules remain.

## Durability and parity

Drafts retain intermediate typing such as `238,`; the client validator restricts
what can be typed, while local/native closure and server closure require complete
measurements. Draft PUT does not normalize partial values or rewrite complete
ones: preserving the exact draft payload is necessary for lost-acknowledgement
reconciliation. Closure canonicalizes the values. Existing frozen reports are not
rewritten; PDF/read-only presentation formats parsable older values for display.

Implementations: app/qml/Measurements.js, app/src/Measurements.h and
server/app/measurements.py. All consume the same 77 shared input/boundary vectors
in shared/measurement-cases.json during tests.

## Validation

- Server/deploy suite: 239 passed, 28 skipped (original Excel workbook or PowerShell required).
- 77 shared format/threshold cases passed in Python, native C++ and QML.
- API tests reject invalid closure without mutation, retain partial drafts, accept
  Not Applicable without evidence, and export canonical units/NOK in server PDFs.
- Real Qt key events confirm fourth voltage digits, sixth earth digits and a third
  decimal place cannot be entered. Field completion formats units and comma.
- Red NOK UI boundaries and NA button/photo exemption passed.
- Native closure rejects invalid numbers and preserves/formats numeric values.
- Native PDF extraction confirms value/unit/NOK; its NOK text colour was checked
  as #a12626. Server PDF content and colour style are covered separately.
- Mobile/desktop report workflow, scroll bounds, photo delegate stability and
  draft-export visibility passed. Native offline HTTP integration passed, including
  lost acknowledgements, conflicts, photo batches and local cleanup.

Local native/QML validation uses Qt/PySide 6.10.2. Physical Android/Windows/iOS
execution and a full Qt 6.12 release build were not performed here.

## Update

Update server and all app installations together. App/server/latest/minimum
client are 0.1.46; Android code 154. Older clients are blocked at login so the new
measurement validation is enforced consistently. Existing reports, photographs
and database can be kept. No schema migration or reset is required.
