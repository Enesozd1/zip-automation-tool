# zip-automation-tool (Python)
Configurable Python tool for safe batch ZIP creation with dry-run and logging support.


Supports:
* Per-folder ZIP creation
* Single-archive ZIP creation
* Dry-run mode
* Recursive zipping
* Robust error handling & logging
* Built with Python’s standard library (pathlib, zipfile, logging).

## Features

* Batch ZIP creation
* Two zip modes:
*per_folder — one zip per subfolder
*single_archive — one zip containing everything
* Optional recursive traversal
* Dry-run mode (no filesystem changes)
* Clear logging & execution summary

## Project Structure
project/
│
├── main.py
├── config.json
├── zip.log (after compile)
├── TestZip
└── utils/
    ├── config_loader.py
    ├── logging_setup.py
    └── zip_tool.py

Configuration (config.json)
```json
{
  "target_path": "...",
  "output_path": "",
  "zip_mode": "per_folder",
  "single_archive_name": "single_archive.zip",
  "include_root_files": "ignore",
  "recursive": false,
  "dry_run": false,
  "log_file": "zip.log",
  "log_level": "INFO"
}
```

## Configuration options
* target_path - Folder to scan and zip
* output_path - Where zip files are created (empty = target_path)
* zip_mode	- "per_folder" or "single_archive"
* single_archive_name -	Name of the zip when using single_archive
* include_root_files -	"ignore" or "separate_zip" (used only in per_folder mode)
* recursive - Include subfolders recursively
* dry_run - Log actions without creating zip files
* log_file -	Log file name
* log_level - Logging level (INFO, DEBUG, etc.)

## Mode behavior
zip_mode = "single_archive"
* One ZIP file is created
* Root files are always included
* Folder structure is preserved inside the archive

zip_mode = "per_folder"
* One ZIP per subfolder
- Root files:
   - ignore → skipped
   - separate_zip → zipped into root_files.zip

## How to Run
* Edit config.json
* Run: python main.py

Check:
* ZIP output directory
* zip.log for details and summary

