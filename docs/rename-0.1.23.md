# Unified Lem naming — 0.1.23

The controller, source filenames, QML context, tests and developer references now
use the Lem name consistently:

| Area | Current name |
| --- | --- |
| C++ controller | `Lem` |
| Controller declaration | `app/src/Lem.h` |
| Controller implementation | `app/src/Lem.cpp` and `app/src/LemOffline.cpp` |
| QML context property / Python mock instance | `lem` |
| Android application ID and Java namespace | `pt.lem.app` |
| Executable / QML module / displayed app title | `Lem` |
| Application / API version | `0.1.23` |
| Android version code | `123` |

CMake targets, includes, meta-object generation and documentation links refer to
the renamed files. Generic Portuguese form terminology uses “atributo” or “caixa”.
The demonstration PDF has been regenerated with a consistently named evidence file.
The English source comments and detailed developer guide remain included.

## Fresh installation

This delivery supports a fresh installation without retaining previous application
or server test data. Android treats `pt.lem.app` as a separate application with its
own private storage. Use a fresh build directory in Qt Creator, or reconfigure CMake
so cached generated files from an earlier build cannot refer to obsolete headers.
A release APK still needs signing before installation.

To recreate server test data through the existing deployment script, run from the
project root:

```bash
bash deploy/deploy.sh --reset-database
```

This existing reset option deletes server users, contracts, chargers, reports and
photographs while retaining the deployment environment and certificate volumes.
Normal deploy remains available without the flag. The server's service/database
identifiers remain LEM; no schema or synchronization algorithm change is required
by the controller rename.

## Validation scope

The source/package inventory and extracted PDF text are checked for obsolete naming.
Desktop and phone-size QML interactions, native C++ synchronization, server,
deployment helpers and Android OpenSSL configuration are tested locally. Optional
PowerShell/workbook tests require their external tools/fixtures. A physical Android
install and full Qt 6.12 APK build are still separate device/kit validation steps.
No live server reset or deployment is performed by preparing this source package.
