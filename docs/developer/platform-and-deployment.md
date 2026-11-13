# Platforms, compatibility and deployment source

## Startup and storage migration

`main.cpp` establishes the OpenSSL suffix on Android before using Qt Network,
selects Fusion controls, sets Lem application identity/theme/icon, resolves storage,
constructs `Lem` and exposes it to the QML engine. Smoke/screenshot paths are
explicit test features; smoke uses a temporary root and fictitious demo data.

`AppStorage::prepare()` handles older storage identities. `resolve()` discovers
existing data, writes a retry marker, **copies** the tree and rewrites local file URLs
in full cache files and per-report edit journals. Source files remain available if
copy/relocation fails. Settings lookup also recovers an unambiguous old server URL.
Do not remove the old `LEM` lookup strings because the visible product is now Lem.

The Android package is `pt.lem.app` from 0.1.23, matching the Java namespace and
manifest/JNI references. Changing this ID creates a separate Android application
and private data directory. The previous app remains installed until the user
removes it; do not assume its local-only drafts/photos migrate. Synchronize pending
work before switching and verify the new app can log in and retrieve server data.
Desktop organization/application settings remain Lem, so desktop data paths do not
change from this internal controller rename.

## Android camera bridge

| Stage | Implementation |
| --- | --- |
| User taps camera | QML calls `Lem::takePhoto(checkpoint)`. |
| Capture identity | C++ passes report/checkpoint IDs into `CaptureActivity.launch()`. |
| Launch camera | Activity creates a cache JPEG, obtains a FileProvider content URI and starts `ACTION_IMAGE_CAPTURE` with temporary URI grants. |
| Activity recreation | Saved photo path/URI/waiting state prevents a second launch after rotation/recreation. |
| Return | Activity writes `camera-result.tmp`, syncs it, renames it to `camera-result.json`, revokes grants and finishes. |
| Consume | Qt polls while active and invokes `attachToReport()` using the captured IDs. |
| Cleanup | Successful source capture remains until Qt successfully copies it into private report storage; cancelled captures are removed. |

This delegates to an installed camera app; it is not a Qt viewfinder or an Activity
subclass replacing Qt's main Activity. `CameraFileProvider` has a separate identity
from Qt's document-sharing provider. The provider path configuration and manifest
must agree with Java's URI authority.

## Android TLS/build configuration

`AndroidOpenSSL.cmake` accepts `LEM_ANDROID_OPENSSL_ROOT` or searches the configured
SDK locations. It selects `ssl_3/<ABI>/libcrypto_3.so` and `libssl_3.so` for each
selected ABI, preferring the complete `no-asm` pair for Debug when present. It checks
ELF class/machine and rejects missing/wrong-ABI/conflicting host libraries before
packaging via `QT_ANDROID_EXTRA_LIBS`.

`ANDROID_OPENSSL_SUFFIX=_3` in startup matches those packaged names. Android system
`/system/lib/libcrypto.so` is not an application dependency substitute. The early
TLS log helps distinguish packaged/backend/runtime problems. The configuration
tests use synthetic ELF headers; they do not prove actual TLS works on a phone.

The project requires Qt 6.12 and C++17. The `Lem` executable is separate from the
`build/qml/Lem` module output, avoiding the Linux executable/directory collision.
Release Android packages still require signing with the intended application key;
readability edits do not change the signing configuration or version code.

## Deployment file responsibilities

| File | Runs where / purpose |
| --- | --- |
| [deploy.sh](../../../Server/deploy/deploy.sh) | Personal Linux laptop: validate options, build payload, SSH/SCP transfer and bootstrap. `--package-only` avoids a server connection. |
| [deploy.ps1](../../../Server/deploy/deploy.ps1) | Windows PowerShell entry point for the equivalent deployment workflow. |
| [deploy-package.py](../../../Server/deploy/deploy-package.py) | Package only server/shared/deploy plus `.dockerignore`, excluding private/config/cache/build material. |
| [deploy-bootstrap.py](../../../Server/deploy/deploy-bootstrap.py) | Remote Python bootstrap: validate checksum, archive paths/size/types, extract safely, resolve target and execute shared remote script. |
| [find-installation.py](../../../Server/deploy/find-installation.py) | Discover an existing installation by its files and optional domain; reject ambiguous targets. |
| [prepare-config.py](../../../Server/deploy/prepare-config.py) | Preserve private environment values and exact HTTPS volumes while preparing selected deployment identifiers. |
| [remote-deploy.sh](../../../Server/deploy/remote-deploy.sh) | Shared remote transaction-like sequence: lock, inspect, build, backup/reset, replace and HTTPS health check. |
| [compose.yml](../../../Server/deploy/compose.yml), [Dockerfile](../../../Server/deploy/Dockerfile), [Caddyfile](../../../Server/deploy/Caddyfile) | PostgreSQL/API/proxy topology, API image and HTTPS routing. |
| [backup.sh](../../../Server/deploy/backup.sh) | PostgreSQL backup helper. |

The remote script takes an installation lock, checks the existing environment and
volume identity, prepares configuration, and builds the new image **before** stopping
the existing API. Normal deployment saves a PostgreSQL dump and previous source/
configuration. Certificate volumes are preserved. A failed HTTPS health check reports
the retained previous source/configuration; it does not promise an automatic rollback.

`--reset-database`/`-ResetDatabase` is an explicit destructive test-data path, not a
routine source/documentation upgrade. No deployment is required merely to read this
documented edition, and this documentation task did not contact the live server.

The source ZIP includes the client and developer docs. The deployment payload
intentionally includes only server/shared/deploy; developer docs are not runtime
inputs and the local formatter settings do not change container dependencies.

## Clean prototype setup (0.1.28)

Current defaults are project/database/container user `lem`, folder `Lem`, domain
`lem.rodrod.pt`, environment prefix `LEM_` and initial administrator `admin@lem.pt`.
Existing user-supplied host/account/domain settings are not silently rewritten.
Normal deployment preserves its selected target and TLS volumes. To remove earlier
installation identifiers, use `deploy/remove-prototype.py` from the new package and
then install into `~/apps/Lem`; see [clean setup](../compatibility-0.1.28.md).
The cleanup script resolves exact resource names from the selected Compose configuration;
it never guesses another project's names. Its default prints a plan, while `--delete`
removes the explicitly selected prototype, database, HTTPS volumes and local images.
It stops on any failed Docker removal and leaves the directory available for recovery.
