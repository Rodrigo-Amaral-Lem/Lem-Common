# PDF presentation - 0.1.38

Both local/offline and server PDFs now show power and power limitation with the
unit appended to the value, for example `Potência: 94 kVA` and
`Limitação de potência: 94 kVA`. There is no separate unit row. As specified for
these reports, the displayed unit is always kVA; the stored values are not
converted or rewritten. An existing trailing kVA is normalized rather than
repeated. Empty values do not produce a bare unit; a numeric zero remains visible.

The local exporter excludes the internal `import_profile` metadata and removes
its device-storage origin sentence. Server exports already selected their
metadata explicitly and do not include these implementation details.

Photograph captions retain the checkpoint designation, e.g. `Evidência PC01.01`,
and omit the original filename. The server's damaged-image warning likewise
retains its checkpoint and warning text without a filename. Photo originals and
ZIP filenames are unchanged.

Validation:

- 37 targeted server/deployment checks passed: actual extracted PDF text, numeric
  and string power, zero/absent limitation, existing units, clean photo captions,
  damaged evidence, long metadata, export permissions, ZIP and release policy.
- Native C++ PDF/auto-open regression passed. An additional real PDF fixture with
  power 94, limitation `94 kVA`, import metadata and a photograph was rendered;
  extracted text confirmed inline units and absence of the removed lines/filename.
- Native first/photo pages and server first/photo pages were rendered and visually
  reviewed. Logo, layout, page footers and checkpoint captions remain intact.
- Native validation used the available Qt 6.10.2 runtime; full platform release
  builds and on-device testing were not performed here.

Rebuild/install the app for local/offline PDFs. Deploy the server for downloaded
PDFs and the PDF inside ZIP exports. No database reset, re-import or data migration
is required. Client/server version: 0.1.38; minimum client remains 0.1.28;
Android build code: 146. Existing exported files are not changed; export again.
