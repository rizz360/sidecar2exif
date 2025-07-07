<p align="center">
  <strong><span style="color:red; font-size:1.2em;">🚧 DRAFT — WORK IN PROGRESS</span></strong><br>
  <em>This project is not production-ready. Use at your own risk!</em>
</p>


# sidecar2exif

💾 Inject EXIF metadata from Immich-go JSON sidecars into your photos and videos

`sidecar2exif` is a CLI tool that writes metadata like **date taken**, **location**, **description**, and **rating** into media files by reading sidecar `.JSON` files created by [`immich-go archive`](https://github.com/simulot/immich-go). This allows you to preserve and embed curated Immich metadata directly into your images or videos — making them portable and standards-compliant.

---

## ✨ Features

- ✅ Supports images and videos (`.jpg`, `.heic`, `.png`, `.mp4`, `.3gp`, etc.)
- ✅ Reads Immich-go-style sidecar files (e.g. `photo.jpg.JSON`)
- ✅ Writes metadata to EXIF/XMP/QuickTime using `exiftool`
- ✅ Warns on suspicious (e.g. future) timestamps
- ✅ Optional deletion of processed sidecar files
- ✅ Detailed CLI output and progress bar

---

## 🛠 Requirements

- **Python 3.7+**
- [`exiftool`](https://exiftool.org/) installed and in your system `PATH`

### Install ExifTool

**Ubuntu/Debian:**
```bash
sudo apt install libimage-exiftool-perl
```

**macOS (Homebrew):**

```bash
brew install exiftool
```

---

## 🚀 Usage

```bash
python3 inject_metadata.py /path/to/folder
```

To delete sidecar `.JSON` files after metadata injection:

```bash
python3 inject_metadata.py /path/to/folder --delete-sidecars
```

---

## 📁 File Structure

Each image/video should have a matching `.JSON` sidecar from `immich-go archive`:

```
photo.jpg
photo.jpg.JSON
```

---

## 💡 Why use this?

Immich doesn’t modify your original media files. While this is great for integrity, it means metadata like album name, description, or fixed capture dates aren’t embedded. `sidecar2exif` bridges that gap — it lets you export from Immich using [`immich-go archive`](https://github.com/simulot/immich-go), then **bake that data into your files** so it travels with them anywhere.

---

## ⚠️ Caveats

* Currently only `.JSON` sidecars are supported, not `.XMP`
* Always test on a backup first — even though ExifTool is safe and reliable
* This tool is unaffiliated with Immich, but complements its export format

---

## 📜 License

MIT

