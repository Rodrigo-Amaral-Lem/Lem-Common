# Workspace and repository ownership

The workspace is deliberately split into three local Git repositories. Open the repository relevant
to the change, and keep command working directories and generated output under `ongoing_work`.

| Directory | Owner and contents |
| --- | --- |
| `App/` | Qt client in `app/`, client guides and a tracked `shared/` snapshot |
| `Server/` | API in `server/`, installation/operations in `deploy/`, server guides, examples and a tracked `shared/` snapshot |
| `Common/` | Canonical `shared/` resources, common `tools/` and cross-component guides |
| `ongoing_work/` | Build trees, environments, test databases, logs, audits and temporary scripts; not a product repository |
| `Brand_Images/` | User-managed customer-brand input resources; not an implicit runtime dependency |

Existing source ZIPs at the workspace root are archive artifacts. Do not produce more unless
requested. Do not create a fourth Git repository around the workspace or version generated
dependencies/builds. The root remains for organized repositories, resources and final artifacts.

## Current baseline and source paths

The migration imported the approved `Lem_Qt_0.1.57_GeneralNotesAndSignaturePhoto.zip`. Initial
commits are App `dba527e`, Server `e642242` and Common `1555e41`. The repository layout retains
`app/`, `server/`, `deploy/` and `shared/` internally because build/deployment code uses those
paths.

Application/API version declarations remain `0.1.57`; Android version code is 170 and checklist
version is 6. These identifiers do not automatically change because documentation or repository
organization changes. A future release must update and verify the relevant declarations together.

The repositories are on branch `main`. Local Git identity is
`Rodrigo Amaral <rodrigo.amaral@lem.com.pt>`. No remote was created/published, and identity
settings were not changed globally. Do not commit or publish while the user has asked for staged
review only.

## Shared resources

`Common/shared` owns the checklist, measurement/connector test cases and existing shared LEM logo.
`App/shared` and `Server/shared` are tracked snapshots, so each component can build/deploy without a
sibling checkout at runtime.

1. Edit the canonical file in Common.
2. Run `python ../Common/tools/sync_shared.py` from `ongoing_work` to inspect differences.
3. Run `python ../Common/tools/sync_shared.py --write` only for the intended update.
4. Review App, Server and Common diffs; run the affected validation tests.
5. Stage the related snapshots together. Make commits only after the applicable review/approval.

The synchronizer does not delete unexpected files and is not a transactional multi-repository
publish. A failed `--write` can have updated earlier files before encountering another problem;
inspect every repository after a failure. Do not fix a schema mismatch by copying a component
snapshot back over the canonical file without reviewing why it differs.

## Branding inputs and product assets

`Brand_Images` belongs to the user. Adding a customer image there does not automatically include it
in builds or reports. Incorporate a chosen resource deliberately into the responsible repository
when implementing a requested feature, and record its provenance/usage. Preserve the existing app
masters and platform derivatives described in [App assets](../../App/app/assets/README.md).

## Working directories and cross-repository tests

Keep CMake builds and environments outside Git trees. After moving source or changing
Qt/compiler/generator, configure a new build under `ongoing_work` instead of reusing an old cache
with absolute paths. Open `App/app/CMakeLists.txt` in Qt Creator.

Most component tests work independently. App network-integration runners locate the sibling Server
repository or `LEM_SERVER_REPO`; Server's release-alignment test locates the sibling App repository
or `LEM_APP_REPO`. These environment variables point to repository roots, not their inner `app/` or
`server/` directories.

## Documentation ownership

Each repository has one README and four focused guides. App owns build/client
internals/workflows/tests; Server owns API/deployment/administration/tests; Common owns
workspace/contract/maintenance/security. `Server/deploy` retains a tool index and uninstall
procedure useful with the installation payload, and App assets have a short provenance guide beside
the files.

Update existing guides when current behavior changes. Detailed audits, screenshots, intermediate
drafts and per-run test records belong in `ongoing_work/documentation-review` or another clearly
named working directory, not a new version-named document in a product repository. Git history
preserves old explanations; current guides must not rely on a reader reconciling conflicting old
release notes.
