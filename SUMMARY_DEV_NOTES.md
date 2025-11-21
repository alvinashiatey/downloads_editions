# Downloads Editions — Developer Digest

## Architecture at a Glance
```
app/
├─ config.py        # defaults & global settings
├─ file_utils.py    # folder scanning, sampling, metadata
├─ image_utils.py   # Pillow-based pixelation helpers
├─ pdf_utils.py     # ReportLab booklet assembly
├─ main.py          # CLI entry point (argparse)
└─ gui.py           # Tkinter GUI (new)

Build Surface
├─ downloads_editions.spec  # PyInstaller recipe (onefile, GUI-focused)
├─ build.sh / build.bat     # platform-aware automation
├─ requirements-build.txt   # pin PyInstaller + optional tooling
└─ dist/ + build/           # generated artifacts (gitignored)
```
- `setup.py` exposes both CLI (`downloads-editions`) and GUI (`downloads-editions-gui`) console scripts.
- GUI spawns a worker thread for PDF generation; uses `root.after()` callbacks to keep UI responsive and log-safe.
- Standalone binaries rely on PyInstaller hidden imports for ReportLab/Pillow to avoid runtime errors.

## Operational Summary
| Area | Details |
| --- | --- |
| Entry Points | CLI, GUI, PyInstaller-built executables (all cross-platform). |
| Output | Booklet PDF saved to `/tmp/Booklet.pdf` (Unix) or `C:\\Temp\\Booklet.pdf` (Windows) and opened automatically via default viewer. |
| Distribution | Zip/Tar bundles plus optional DMG/installer (instructions in README_GUI_BUILD.md & WALKTHROUGH.md). |
| Documentation Layers | README (overview), QUICKSTART (5-min guide), README_GUI_BUILD (deep dive), PROJECT_STRUCTURE (architecture), COMMANDS (cheat sheet), WALKTHROUGH (step-by-step), FOR_END_USERS (ship-with-app), CONVERSION/CHANGES summaries. |

## Build & Test Checklist
1. `pip install -e . && pip install -r requirements-build.txt` to prime deps.
2. Run `downloads-editions` and `downloads-editions-gui` locally to confirm CLI + GUI parity.
3. Execute platform script (`./build.sh` or `build.bat`); inspect `dist/` output and logs in `build/`.
4. Launch the generated binary/app and verify folder selection, file sampling, PDF creation, auto-open, and logging.
5. Spot-check `/tmp/Booklet.pdf` metadata/layout and confirm booklet page ordering.
6. Clean artifacts via `rm -rf build dist` (or Windows equivalents) before re-running PyInstaller.

## High-Level Change Log
- Introduced Tkinter GUI (`app/gui.py`) with polished layout, progress bar, threaded generation, and robust dialog feedback.
- Added build infrastructure (`downloads_editions.spec`, shell/batch scripts, requirements-build.txt) enabling one-file executables on all major OSes.
- Expanded documentation suite to cover onboarding (QUICKSTART), deep-dive (README_GUI_BUILD), architecture (PROJECT_STRUCTURE), operational cheats (COMMANDS), walkthroughs, and end-user packaging instructions.
- Updated README + setup entry points while keeping CLI code paths untouched for backwards compatibility.

## Frequently Used Commands
```bash
# Installation
pip install git+https://github.com/alvinashiatey/downloads_editions
pip install -e .  # dev mode

# Execution
downloads-editions                      # CLI defaults
downloads-editions --folder ~/Docs --files 48
downloads-editions-gui                  # GUI launcher
python -m app.gui                       # debug-friendly run

# Builds & Distribution
./build.sh   # macOS/Linux
build.bat    # Windows
cd dist && zip -r DownloadsEditions-macOS.zip DownloadsEditions.app
cd dist && powershell Compress-Archive -Path DownloadsEditions.exe -DestinationPath DownloadsEditions-Windows.zip
cd dist && tar -czf DownloadsEditions-Linux.tar.gz DownloadsEditions

# Cleanup & Diagnostics
rm -rf build dist && pyinstaller downloads_editions.spec
xattr -cr dist/DownloadsEditions.app   # macOS Gatekeeper fix
chmod +x dist/DownloadsEditions        # Linux permissions
cat build/DownloadsEditions/warn-DownloadsEditions.txt
```

## Future Enhancement Ideas
- GUI niceties: drag-and-drop folders, recent-folder history, advanced settings dialog, multiple layout templates, inline file previews.
- Distribution upgrades: CI-powered multi-platform builds, code signing, auto-updaters, installers (DMG/MSI/PKG) baked into release workflows.
- Analytics & customization: stats dashboards, configurable output paths, alternate booklet formats (A5, zine), optional cloud storage sources.

## Support Channels
- Issues/PRs: `https://github.com/alvinashiatey/downloads_editions`
- Contact: `mail@alvinashiatey.com`
- Maintainer: Alvin Ashiatey (January 2025 conversion of CLI → GUI + standalone release).
