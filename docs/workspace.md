# Repository ownership and shared development

LEM is split into three Git repositories. Work from the root of the repository being changed.
Each repository documents its own commands; no personal workspace directory is required.

| Repository | Owner and contents |
| --- | --- |
| `App/` | Qt client in `app/`, client guides, Android/desktop user manuals and a tracked `shared/` snapshot |
| `Server/` | API in `server/`, installation/operations in `deploy/`, server guides, examples and a tracked `shared/` snapshot |
| `Common/` | Canonical `shared/` resources, common `tools/` and cross-component guides |

## Working directories and outputs

Commands in the App, Server and Common guides start at their respective repository roots.
Use `.venv/` for local Python environments and ignored `build/` subdirectories for build trees,
staging folders, disposable test data and per-run reports. Keep credentials, production data and
backups private and out of Git. An ignored build directory is not a backup of unsent customer work.

Installed SDKs, compilers, Docker and Python are prerequisites, not sibling source directories.
Set their paths for the chosen machine rather than copying another developer's absolute paths.
After moving source or changing Qt/compiler/generator, configure a fresh build instead of reusing
a cache with old absolute paths. See [App builds](../../App/docs/build-and-release.md).

## Companion repositories

Cross-component tools normally expect sibling checkouts named `App`, `Server` and `Common` under
one parent. This convention is required only by the relevant cross-repository checks; the client
and server each ship a tracked shared-resource snapshot for independent builds and deployment.

App network-integration runners locate the sibling Server repository or `LEM_SERVER_REPO`.
Server's release-alignment test locates the sibling App repository or `LEM_APP_REPO`. These
variables point to repository roots, not the inner `app/` or `server/` directories. See the
[App test guide](../../App/docs/testing.md) and [Server test guide](../../Server/docs/testing.md).

## Shared resources

`Common/shared` owns the checklist, measurement/connector test cases and shared LEM logo.
`App/shared` and `Server/shared` are tracked snapshots.

From the Common repository root:

```powershell
python tools/sync_shared.py
```

The default command compares without writing. For an intentional canonical change:

1. Edit the resource under `shared/` in Common.
2. Run `python tools/sync_shared.py --write` to publish the snapshots.
3. Review App, Server and Common diffs and run the affected validation tests.
4. Stage the related changes in each repository and follow the project's commit/review process.

The synchronizer never deletes unexpected files and is not a transactional multi-repository
publish. A failed write may have updated earlier files; inspect all affected repositories.
Do not copy a component snapshot over Common without reviewing why it differs.

## Version and branding ownership

The current application/API version is `0.6.0`, Android version code is 188 and checklist version
is 7. Documentation edits do not change these application versions. Coordinate a future release's
declarations and validation across the components; see [Maintenance](maintenance.md#version-policy).
The minimum client is `0.5.5`. It receives an update notice for `0.6.0`. Earlier apps
interpret every order item as a preventive visit. The server explains the required update
on login and authenticated requests.

Brand assets must be deliberately incorporated into the responsible repository with their usage
and provenance recorded. Adding an image to a developer's local folders does not include it in
the app or reports. Preserve the masters and platform derivatives described in
[App assets](../../App/app/assets/README.md), and respect third-party artwork/trademark rights.

## Documentation ownership

App owns client build, architecture, field workflow, testing and end-user manuals. Server owns API,
deployment, administration and testing. Common owns shared contracts, maintenance and security.
`Server/deploy` retains a tool index and uninstall procedure that travel with installation payloads.

Keep executable examples relative to the owning repository root. Reference a companion repository
explicitly when a cross-component operation requires it. Local agent instructions, private audit
folders and machine-specific checkout paths are not product prerequisites.

Update existing focused guides rather than accumulating version-named notes. Git history preserves
older explanations. Detailed audits, intermediate screenshots, draft documents and test transcripts
belong in ignored `build/` directories; final user manuals belong in App's maintained documentation.
