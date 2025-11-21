# Downloads Editions — User-Facing Summary

## Project Snapshot
- Turns the clutter of any folder (defaults to `~/Downloads`) into a printable booklet PDF that captures filenames, metadata, and pixelated previews.
- Offers three ways to run: CLI (`downloads-editions`), GUI (`downloads-editions-gui`), or standalone executables produced via PyInstaller builds for macOS, Windows, and Linux.
- Outputs `Booklet.pdf` to `/tmp` on macOS/Linux or `C:\\Temp` on Windows and opens it automatically.

## Quick Start
| Task | Command / Action |
| --- | --- |
| Install directly from GitHub | `pip install git+https://github.com/alvinashiatey/downloads_editions` |
| Launch GUI (recommended) | `downloads-editions-gui` |
| Run CLI with defaults | `downloads-editions` |
| Run CLI with custom folder/files | `downloads-editions --folder ~/Pictures --files 30` |
| Build standalone app (macOS/Linux) | `./build.sh` |
| Build standalone app (Windows) | `build.bat` |

### GUI Flow
1. Launch the GUI (Python installed or by double-clicking the packaged app).
2. Click **Browse…** to choose a folder (defaults to Downloads).
3. Use the spinner to select 1–100 files (24 gives a balanced booklet).
4. Press **Generate PDF** and monitor the progress/log area.
5. The PDF opens automatically; move it from `/tmp`/`C:\\Temp` if you want to keep it.

### Standalone Distribution
- Build artifacts land in `dist/` ( `.app`, `.exe`, or binary ).
- Repackage with ZIP/DMG/TAR.GZ plus `FOR_END_USERS.md` or your preferred README for recipients.
- macOS: remove Gatekeeper flags via `xattr -cr dist/DownloadsEditions.app` if needed.
- Linux: `chmod +x dist/DownloadsEditions` before shipping.

## Key Features
- GUI built with Tkinter: folder picker, file-count spinbox, progress bar, timestamped log, and modal dialogs for success/errors.
- CLI remains untouched for automation; accepts `--folder` and `--files` flags.
- PDFs are booklet-ready (Letter, landscape, 2-up layout) and pixelate imagery for privacy.
- Standalone binaries embed Python/Pillow/ReportLab and run without dependencies.

## Printing & Sharing Tips
- Print duplex on short-edge binding, fold in half, and staple the spine for a zine-like result.
- Run multiple times with different folders (Documents, Pictures, seasonal snapshots) for themed editions.
- Email finished booklets to `mail@alvinashiatey.com` to contribute to the communal archive.

## Troubleshooting Cheats
| Issue | Remedy |
| --- | --- |
| GUI fails to start | Run `python -m app.gui` for verbose errors; ensure Tkinter is available. |
| Build errors | `pip install -e . && pip install -U pyinstaller`, then `rm -rf build dist` and rebuild. |
| macOS warns "app is damaged" | `xattr -cr dist/DownloadsEditions.app` then relaunch. |
| Permission denied (Linux) | `chmod +x DownloadsEditions` before running/extracting. |
| PDF missing | Check `/tmp/Booklet.pdf` or `C:\\Temp\\Booklet.pdf` directly. |

## Support & Links
- GitHub repo/issues: `https://github.com/alvinashiatey/downloads_editions`
- Email: `mail@alvinashiatey.com`
- Author: Alvin Ashiatey — project explores digital archives, privacy, and design through automated booklets.
