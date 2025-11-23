# Downloads Editions

This project experiments with scripting the creation of a book—each edition generated directly from the contents of a download folder, a crossroads where the web meets local files that might otherwise be forgotten. Each edition reflects on the digital clutter accumulating over time, revealing the hidden stories within our downloads.

To contribute to future editions, simply download the provided script and run it on your computer. The script automates the generation of a book from your download folder. Once completed, you can submit your book for inclusion in the collective archive of editions, adding your own chapter to this ongoing exploration of digital archives.

## 🎨 New: GUI Application

Downloads Editions now includes a user-friendly graphical interface! No need to use the command line—just click buttons to generate your booklet.

**Quick Start with GUI:**

```bash
# Run instantly without installing anything permanently
curl -sL https://raw.githubusercontent.com/alvinashiatey/downloads_editions/main/quickstart.sh | bash
```

Or install permanently:

```bash
pip install git+https://github.com/alvinashiatey/downloads_editions
downloads-editions-gui
```

For detailed GUI instructions and building standalone applications, see:

- **[Quick Start Guide](QUICKSTART.md)** - Get started in under 5 minutes
- **[GUI & Build Guide](README_GUI_BUILD.md)** - Comprehensive guide with standalone app building instructions

## Installation

You can easily install this tool directly from GitHub using Python’s package installer, pip. Just follow these steps:

1. Open your Terminal.
2. Run the following command to install the package:

```bash
pip install git+https://github.com/alvinashiatey/downloads_editions
```

## Usage

### GUI Application (Recommended for most users)

Launch the graphical interface:

```bash
downloads-editions-gui
```

Then simply:

1. Browse to select your folder
2. Choose how many files to include
3. Click "Generate PDF"

### Command Line Interface

For advanced users or scripting:

```bash
downloads-editions
```

With custom options:

```bash
downloads-editions --folder ~/Documents --files 30
```

## Building Standalone Applications

Want to share the app without requiring Python installation? You can build standalone executables:

```bash
# macOS/Linux
./build.sh

# Windows
build.bat
```

The standalone app will be created in the `dist/` folder. See [README_GUI_BUILD.md](README_GUI_BUILD.md) for complete instructions.

## Uninstallation

If you ever need to remove the package from your system, it's just as easy to uninstall:

1. Open your Terminal.
2. Run the following command:

```bash
pip uninstall downloads-editions
```

## Submitting Your Edition

After your booklet PDF is generated, we’d love to include your work in our collective archive. Simply email your generated Booklet.pdf to:

[mail@alvinashiatey.com](mailto:mail@alvinashiatey.com)

Your submission will help contribute to the ongoing exploration of digital archives, where every edition adds a unique perspective.

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide for GUI and building
- **[README_GUI_BUILD.md](README_GUI_BUILD.md)** - Comprehensive GUI and standalone build guide
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project architecture and component overview

## Features

- ✅ Command-line interface for automation
- ✅ Graphical user interface for ease of use
- ✅ Build as standalone application (no Python required)
- ✅ Cross-platform support (macOS, Windows, Linux)
- ✅ Privacy-focused (pixelated images)
- ✅ Booklet-style PDF layout for printing

## License

MIT License - See LICENSE file for details

## Author

**Alvin Ashiatey**

- Email: mail@alvinashiatey.com
- GitHub: https://github.com/alvinashiatey/downloads_editions
