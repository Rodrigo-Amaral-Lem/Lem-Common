# Photo cropping and video evidence — 0.1.52

## Using the app

In an editable draft, use the crop icon below a photograph. Drag a corner of the
selection to resize it, or drag the centre to reposition it. **Repor** selects the
whole image; **Cancelar** keeps the current photograph. **Recortar** saves the
selection at original resolution, respecting camera orientation. Cropping is
available for existing local draft photographs on Android, Windows and Linux.
The original in the gallery is never modified. Closed reports remain immutable.

Use the video camera icon on Android to choose **Gravar vídeo** or **Escolher
vídeo**. Recording delegates to the installed camera app and requests a short,
low-quality clip to control storage and mobile transfers. On desktop, the icon
opens a video file picker. Tap a downloaded video to open the system video player.
There is no new Qt Multimedia/static Windows dependency.

- Formats: MP4 or 3GP, up to **60 seconds and 20 MB each**. Capture duration/size
  hints depend on the camera app; Lem also validates the returned file.
- Server accepts one video stream up to 4K (8,294,400 pixels), H.264, HEVC,
  MPEG-4 or H.263. A player supporting the recorded codec must be installed.
- The combined report limit stays **200 attachments / 250 MB**.
- Videos supplement photographs. They do **not** satisfy a mandatory photograph.
- Attachments stay local while working and use the existing deferred upload at
  group changes/report exit or manual synchronization. Cropping does not upload
  immediately. Downloads, removal, cache cleanup and conflict copies include videos.
- PDF exports label video evidence rather than embedding playable video. ZIP
  exports include the original clips under `videos/<checkpoint>/` and original
  photographs under `fotografias/<checkpoint>/`. ZIP still needs a synchronized
  closed report/server connection; the existing local PDF export remains available.
- A closed report with all its evidence cached can export its PDF while logged
  off/offline. Neither PDF nor ZIP is enabled for drafts.

## Deployment

Deploy this server **before** distributing rebuilt 0.1.52 clients. The default
minimum/latest client policy is now 0.1.52, preventing older clients from treating
video attachments as photographs. Standard deployment promotes existing `.env`
policy bounds and preserves data; no schema migration or database reset is needed.
Android version code: **164**.

The Dockerfile now installs FFmpeg, supplying **ffprobe**. Deploy rebuilds the API
image. For a server run outside Docker, install `ffmpeg` with the system package
manager. Videos fail with an explicit validation error if ffprobe is unavailable;
photographs continue working. No new port is needed.

## Implementation and invariants

The existing `Photo` table and `/photos/` route remain the internal attachment
transport; MIME identifies images versus videos. This preserves owner/revision
checks, upload retry digests, quota accounting and deletion tombstones. File paths
come from `SafeStorage::photoPath`, which admits only safe IDs and known extensions.
The private cache keeps all attachments under `photos/` for shared cleanup rules.

`EvidenceMedia.h` checks bounded ISO BMFF box lengths and movie duration offline.
The server independently inspects streams/container/duration with ffprobe, a
10-second subprocess timeout and network protocols disabled, under the existing
media admission semaphore. This is container/stream validation, not full-frame
video decoding or a guarantee that every third-party player supports a clip.

`PhotoCropDialog.qml` works in normalized oriented-image coordinates, excluding
letterboxing. The preview is capped at 1600 pixels; native cropping/encoding runs
on the edit worker pool against the full image. A crop receives a fresh ID and a
deletion tombstone for the previous attachment (including lost-upload-ACK cases).
The replacement journal must commit before the old private copy is removed.
Failures retain the previous attachment. Backend draft ownership and busy guards
remain authoritative even if a dialog was opened earlier.

## Verification and limits

Regression coverage includes real MP4 acceptance/retry/download/removal, video
versus required-photo validation, byte-identical ZIP video export, server/native
PDF generation, crop coordinate validation, private-file removal, original gallery
preservation, crop replacement journaling, immutable report guards, and actual
pointer-driven crop geometry on 320/360-pixel and desktop layouts. The broader server,
deployment, native and QML suites are run alongside these new regressions.

No physical Android camera/device, Windows toolchain, Docker daemon or live
PostgreSQL/server is available in this environment. Camera intents and system
video playback still need a device smoke test. The ZIPs contain source/build and
deployment inputs, not prebuilt APK/EXE/Docker images.

Checks completed: 289 server/deployment tests passed across the main suite and 14 checks with
the supplied original XLSM (14 PowerShell checks skipped: PowerShell unavailable); 26 QML script checks passed; 21 Android OpenSSL /
Windows standalone configuration tests passed, including 16 subtests. Native
connector, session/revision, projection, measurement and crop/video regressions
passed with the available Qt 6.10.2 test runtime. Production kits remain Qt 6.12.

The native offline HTTP integration also passed against a disposable local API, including deferred uploads, lost acknowledgements, conflict handling, cache cleanup and download cancel/resume.

Original workbook checks use `STATIONS_TEST_WORKBOOK` pointing to the supplied XLSM; the workbook is read-only and excluded from both distribution archives.
