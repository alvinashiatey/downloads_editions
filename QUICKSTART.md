# Downloads Editions - Quick Start Guide

Get up and running with the Downloads Editions GUI in under 5 minutes!

## 🚀 Quick Start: Running the GUI

### 1. Install the Package

```bash
pip install git+https://github.com/alvinashiatey/downloads_editions
```

### 2. Launch the GUI

```bash
downloads-editions-gui
```

That's it! The GUI will open and you can start generating your booklet.

---

## 📦 Quick Start: Build Standalone App

Want to create a standalone application that doesn't require Python? Follow these steps:

### macOS / Linux

```bash
# 1. Navigate to project directory
cd downloads_editions

# 2. Run the build script
./build.sh

# 3. Find your app in the dist/ folder
open dist/DownloadsEditions.app  # macOS
# or
./dist/DownloadsEditions         # Linux
```

### Windows

```batch
:: 1. Navigate to project directory
cd downloads_editions

:: 2. Run the build script
build.bat

:: 3. Find your app in the dist\ folder
dist\DownloadsEditions.exe
```

---

## 🎯 Using the GUI

1. **Browse**: Click "Browse..." to select your folder (defaults to Downloads)
2. **Set Count**: Choose how many files to include (1-100)
3. **Generate**: Click "Generate PDF" button
4. **Done**: Your PDF opens automatically!

The PDF is saved to `/tmp/Booklet.pdf` (or `C:\Temp\Booklet.pdf` on Windows).

---

## 🛠 Manual Build (Alternative)

If the build scripts don't work, you can build manually:

```bash
# Install dependencies
pip install -e .
pip install pyinstaller

# Build
pyinstaller downloads_editions.spec

# Your app is in dist/
```

---

## 📤 Sharing Your App

### Create a ZIP for distribution:

**macOS:**
```bash
cd dist
zip -r DownloadsEditions-macOS.zip DownloadsEditions.app
```

**Windows:**
```powershell
cd dist
powershell Compress-Archive -Path DownloadsEditions.exe -DestinationPath DownloadsEditions-Windows.zip
```

**Linux:**
```bash
cd dist
tar -czf DownloadsEditions-Linux.tar.gz DownloadsEditions
```

---

## ❓ Troubleshooting

### GUI won't launch
- Make sure you installed the package: `pip install -e .`
- Try running directly: `python -m app.gui`

### Build fails
- Ensure PyInstaller is installed: `pip install pyinstaller`
- Check that all dependencies are installed: `pip install -e .`
- Try cleaning and rebuilding: `rm -rf build dist && pyinstaller downloads_editions.spec`

### App won't open on macOS
```bash
# Remove quarantine flag
xattr -cr dist/DownloadsEditions.app
```

### "Permission denied" errors
```bash
# Make the app executable
chmod +x dist/DownloadsEditions.app/Contents/MacOS/DownloadsEditions  # macOS
chmod +x dist/DownloadsEditions  # Linux
```

---

## 📚 More Information

For detailed instructions, see:
- **GUI & Build Guide**: [README_GUI_BUILD.md](README_GUI_BUILD.md)
- **Original CLI Guide**: [README.md](README.md)

---

## 💬 Need Help?

- Email: mail@alvinashiatey.com
- GitHub: https://github.com/alvinashiatey/downloads_editions

---

**Enjoy creating your digital archive booklets! 📖✨**
