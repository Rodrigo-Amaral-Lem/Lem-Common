# Implemented safeguards and resource limits

This guide describes what the current source enforces and its boundaries. It is not a claim of a
fresh dependency-vulnerability audit or a certification of an installed Qt/OS/container build.
Keep detailed audit outputs and dated measurements in an ignored local `build/` directory,
separate from the maintained reading path.

## Authentication and deployment boundary

The server stores salted scrypt password representations and SHA-256 session-token digests, not
recoverable plaintext passwords/raw session tokens. The API requires passwords of at least 12
characters; sessions expire after 30 days and explicit logout/password-reset paths revoke them.

The app's `PUT /api/users/{user_id}/password` action is administrator-only and accepts only current
`tech` targets (12–200 characters). The server filters the target role before obtaining a credential
write lock, rechecks against concurrent role changes, and atomically updates the salted hash,
deletes all target sessions and audits actor/target without credentials. Login/authentication share
the same User-row lock, so a racing old login cannot retain a usable session after reset. Administrator
password recovery remains a server-console operation. Reports and assignments are not modified.
Client bearer tokens are kept in memory; offline identity/cache data remain on disk.

Login uses separate pair/IP/account buckets over a 60-second window: 5 per pair, 30 per IP, 20 per
account. IPv6 addresses are grouped by /64 (IPv4-mapped addresses normalize to IPv4). Active buckets
have bounded capacity. These counters and export/media admission slots are **process-local**;
restarting clears them, and multiple workers/replicas do not share them.

The supplied container runs one API worker behind Caddy. Do not expose that worker's proxy-trusting
listener directly as if it were a public gateway. Production configuration should keep API
documentation disabled unless intentionally needed. Changing bootstrap environment variables does
not change existing account passwords or PostgreSQL volume credentials.

The client restricts redirects to the same origin and bounds response accumulation. These
application guards do not install vendor patches or prove the Qt SDK has every security fix. CMake
contains a version-based Qt Network patch advisory for versions below 6.12.1; a vendor backport can
retain its version number, so check the actual SDK's provenance independently. No new external CVE
verification was performed for this documentation-only review.

## Limits enforced in source

Binary-size limits below use MiB/KiB unless explicitly marked as the proxy's configured MB value.

| Boundary | Current behavior |
| --- | --- |
| Login request body | 4 KiB |
| Other JSON/body requests | 512 KiB |
| Multipart request body | 61 MiB; photographs remain capped at 20 MiB and videos at 60 MiB |
| Caddy request body | Configured as `65MB` |
| Photograph file | 20 MiB |
| Video file | 60 MiB |
| Server image inspection | JPEG/PNG, maximum 40 million pixels |
| Video | MP4/3GP, one supported video stream, maximum 4K-area frame; 120.5-second inspection ceiling allows timestamp rounding around 120-second capture |
| Video probe | `ffprobe`, file/pipe protocols only, 10-second subprocess timeout |
| Report evidence | Up to 200 items and 400 MiB total |
| Client evidence download reply | 60 MiB; photograph validation remains capped at 20 MiB |
| Client PDF/ZIP reply | 500 MiB |
| Other client replies | 64 MiB |
| Answer value/notes | Up to 8,000 characters each at the API boundary |
| Export admission | Default 2 slots, configured maximum 4 |
| Image/media admission | Default 1 slot, configured maximum 2 |
| Original-evidence download admission | Default 8 simultaneous responses per API worker, configured maximum 16 |

Evidence downloads release the database connection before sending and retain a separate response
slot to bound memory. Single-byte-range requests enforce the same contract/report access as full
downloads. Client evidence requests use four concurrent transfers, bounded disk staging and at most
three automatic retries. SHA-256 verification precedes publishing an original. PDF/ZIP replies also
use disk staging; local ZIP output rejects unsafe member names and checks original digests.

A video does not count as a photograph for required-photo validation. The server inspects bytes
rather than trusting an extension or claimed MIME. Failure to find `ffprobe` is an
unavailable-validator error, not acceptance of uninspected video.

Desktop signature import is a separate client path: it bounds the source file at 20 MiB/64 million
pixels and normalizes to at most 700 × 700 before calling the PNG signature saver. That path does
not raise the general server image limits.

## Excel and archive inputs

Workbook inspection limits ZIP entry count to 2,000 and expanded content to 100 MiB, rejects
DTD-based XML, and bounds total rows (100,000), columns (256) and declared/read cell workload
(2,000,000). Larger workbooks must be split or deliberately redesigned rather than disabling limits
silently.

Deployment packaging/extraction validates archive paths, release identity and checksums and refuses
unsafe symbolic-link/path cases. These are separate from Excel parsing. Use the public deployment
entry points instead of manually bypassing bootstrap checks.

## Local data, backups and removal

The client does not encrypt its offline cache or require biometrics. A person/process with access to
that OS account can access cached report/media files. Android backup exclusions protect the app's
private work from platform backup/transfer paths; they do not back up unsynchronized reports.
Synchronize before uninstalling or changing installation identity.

Keep live `.env`, private keys, production DB files and backups out of Git. Database dumps contain
reports and evidence. The uninstall tool's retained sibling backup contains
configuration/credentials and must remain private. TLS volumes are deliberately preserved by
ordinary updates and deliberately removed by a confirmed purge of the selected installation.

Permanent report deletion produces tombstones, and expired/purged contract data is not revived by an
old client cache. Backup retention, off-host copies and tested restoration are operational
responsibilities; the presence of a backup command does not prove recoverability.

If a local checkpoint or edit journal cannot be read or has an incomplete report structure, the
client suspends checkpoint/journal writes, synchronization and cleanup instead of replacing it with empty state. The
files remain recovery evidence; this safeguard is not an automatic repair or a substitute for a
backup. Automatic evidence eviction excludes conflicted/unconfirmed reports and pending deletions.

## Code to inspect when changing a safeguard

- Server: [security.py](../../Server/server/app/security.py),
  [request_limits.py](../../Server/server/app/request_limits.py),
  [images.py](../../Server/server/app/images.py), [media.py](../../Server/server/app/media.py),
  [importer.py](../../Server/server/app/importer.py).
- Client: [NetworkSecurity.h](../../App/app/src/NetworkSecurity.h),
  [SafeStorage.h](../../App/app/src/SafeStorage.h),
  [EvidenceMedia.h](../../App/app/src/EvidenceMedia.h).
- Operations: [Deployment](../../Server/docs/deployment.md),
  [Administration](../../Server/docs/administration.md) and
  [uninstall guide](../../Server/deploy/UNINSTALL.md).
