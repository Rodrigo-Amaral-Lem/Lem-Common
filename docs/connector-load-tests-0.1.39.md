# Per-connector load tests - beta 0.1.39

New interventions build PC03 load tests from the charger's imported `connectors`
(Tomadas / Fichas) value. Each physical connector gets an independent status,
notes and optional photographic evidence. The generated checklist is frozen in
that intervention and used by the UI, close validation, synchronization and both
PDF exporters. Re-importing charger data later cannot silently relabel answers.

| Charger connectors | Generated load-test question |
| --- | --- |
| `CCS2, CCS2` | `PC03.01.01` - Teste de carga do conector CCS2 #1 |
| same charger | `PC03.01.02` - Teste de carga do conector CCS2 #2 |
| `Mennekes Type 2` | `PC03.01.01` - Teste de carga do conector Mennekes Type 2 |
| `Mennekes Type 2, CCS2, CHAdeMO` | Three questions in that order, without a # suffix |

Suffixes count occurrences of the same type, not the global question position.
IDs increment globally within the connector list (`PC03.01.01`, `.02`, etc.).
The remaining RFID, meter and ventilation checks retain PC03.04-PC03.06.

Comma, semicolon, slash, pipe and newline separators are accepted, as are
explicit quantities such as `2x CCS2`, `CCS2 x2` and `3×Mennekes`. Type 2/T2/Tipo 2
are displayed as Mennekes Type 2; CCS2 and CHAdeMO spelling is normalized.
Unknown names are retained. A generic AC entry is labelled `AC (tipo não indicado)`;
it is not assumed to identify a specific socket. Generic CCS is not assumed to
mean CCS2. Keep connector information precise in the imported workbook.

Missing connector information produces one explicit `tipo não indicado` load
test. It does not restore the old three fixed AC/CCS/CHAdeMO questions or silently
remove all load testing. Invalid quantities/names fail visibly. A defensive maximum
of 64 connectors prevents malformed configuration from creating unbounded forms.

The app sends its frozen connector list during synchronization. The server builds
its checklist independently from the charger's stored connector configuration.
If the configuration changed before the first upload, the server returns a
conflict explaining that a fresh intervention is required from the updated
catalogue. It does not silently assign existing answers to different connectors.

## Beta installation and data

This release uses checklist version 2, with no old-checkpoint conversion. Minimum
and latest client become **0.1.39**; the deploy scripts promote the stored policy
so an older app cannot log in after deployment. Android build code is **147**.

Deploy the server and rebuild/install the app. Clear the old beta reports on the
server and the app's local data, then create new interventions. No database schema
migration is needed. To discard the entire prototype database instead, the existing
Linux `bash deploy/deploy.sh --reset-database` or PowerShell
`deploy/deploy.ps1 -ResetDatabase` option can be used; it also removes imported
contracts/users/reports. Re-import the workbook afterwards. The live server was
not changed by this implementation.

PDF postal codes remain on their own metadata line/row. App catalogue cards retain
the postal code appended to the address.

## Validation

- 160 server/deployment checks passed, including 13 shared connector vectors,
  independent close/NOK validation, immutable checklist snapshots, PDF labels,
  invalid old checkpoint rejection, mismatch handling and minimum-version promotion.
- The native C++ implementation passed the same connector vectors and generated
  a PDF with distinct CCS2 #1/#2 answers and notes.
- A disposable real HTTP integration run imported a charger with two CCS2,
  created the draft in C++, synchronized it and closed it using the generated IDs.
  Existing offline durability, upload acknowledgement recovery, ownership, deletion,
  cache and deferred/bulk-photo checks passed in that run.
- The actual QML view passed independent dynamic answer/notes/progress tests;
  the full narrow report workflow and scroll-limit regressions passed.
- Native and server PDF pages and the narrow PC03 screen were rendered/reviewed.
  The native PDF also confirmed the postal code on its own line.
- Native/UI validation used Qt 6.10.2. Full Windows/Android Qt 6.12 release builds
  and physical-device testing remain to be performed.

Implementation: `app/src/Checklist.h`, `server/app/checklist.py`,
`shared/connector-cases.json`. The unchanged resource filename
`shared/checklist-v1.json` now declares checklist version 2.
