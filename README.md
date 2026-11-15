# LEM Common

The shared contract, resources, maintenance tools and cross-component documentation for the LEM
client and server. The current source is labelled **0.2.0**, with checklist **6** and the
subsequently approved fixes included.

| Guide | Use it for |
| --- | --- |
| [Workspace](docs/workspace.md) | Repository ownership, Git review, shared snapshots, branding and generated files |
| [Report contract](docs/report-contract.md) | Current groups, required/optional fields, measurements, evidence, copies and signatures |
| [Maintenance](docs/maintenance.md) | Common tools, documentation checks, test coordination and release changes |
| [Security and limits](docs/security.md) | Implemented safeguards, configured resource limits and known boundaries |

`shared/` is canonical. `App/shared/` and `Server/shared/` are tracked copies for independent
builds/deployments. Run tools from the **Common repository root**:

```powershell
python tools/sync_shared.py
python tools/check_docs.py
```

The first command checks byte equality without writing. To publish an intentional shared-resource
change, use `sync_shared.py --write`, inspect all affected Git diffs and stage/commit according to
the current review instruction. No remote repositories are configured by this documentation.

Component-specific guides are in [App](../App/README.md) and [Server](../Server/README.md).
Historical release-note files are no longer part of the current reading path; Git history retains
the previous documentation.

## License

First-party LEM source code, tests, build/deployment tools, configuration, schemas and accompanying
project documentation are licensed under the **GNU General Public License, version 3 only**
(`GPL-3.0-only`). See [LICENSE](LICENSE) for the complete terms and warranty disclaimer.

Source files carry SPDX notices. JSON data keeps its original strict format and has adjacent
`.json.license` notices. Existing third-party license notices remain applicable; this declaration
does not relicense Qt, Python dependencies, bundled fonts or third-party customer artwork/trademarks.
Generated reports and customer data are not relicensed by this source-code notice.
