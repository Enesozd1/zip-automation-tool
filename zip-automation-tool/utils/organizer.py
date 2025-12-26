import logging
from pathlib import Path
from typing import Any, Dict
from datetime import datetime       

#logic to organize a folder by extension map rules into folders, which has subfolders of date and size
EXTENSION_MAP = {
    #Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".bmp": "Images",
    ".gif": "Images",
    ".tiff": "Images",
    ".webp": "Images",
    ".svg": "Images",
    ".ico": "Images",

    #Documents
    ".pdf": "Documents",
    ".txt": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".odt": "Documents",
    ".rtf": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",

    #Code / Data
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".html": "Code",
    ".css": "Code",
    ".json": "Code",
    ".xml": "Code",
    ".yaml": "Code",
    ".yml": "Code",
    ".sql": "Code",
    ".md": "Code",

    #Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".aac": "Audio",
    ".ogg": "Audio",
    ".m4a": "Audio",

    #Video
    ".mp4": "Video",
    ".mkv": "Video",
    ".avi": "Video",
    ".mov": "Video",
    ".wmv": "Video",
    ".flv": "Video",
    ".webm": "Video",

    #Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",
    ".xz": "Archives",

    #Disk images / installers
    ".iso": "Installers",
    ".exe": "Installers",
    ".msi": "Installers",
    ".apk": "Installers",
    ".dmg": "Installers",
    ".deb": "Installers",
    ".rpm": "Installers",

    #Config / system
    ".ini": "Config",
    ".cfg": "Config",
    ".conf": "Config",
    ".env": "Config",
    ".log": "Logs",

    #Temporary / backups
    ".tmp": "Temp",
    ".bak": "Temp",
    ".old": "Temp",
}

def organizer(p: Path, conf: Dict[str, Any]) -> None:
    
    SubSet = set()
    MainSet = set()
    for item in p.iterdir():
        if not item.is_file():
            continue

        category = EXTENSION_MAP.get(item.suffix.lower())
       

        if not category:
            logging.warning(f"Unsupported extension: {item.suffix}")
            continue

        #create the destination
        dest_folder = p / category
        try:
            st = item.stat()
        except (FileNotFoundError, PermissionError, OSError) as e:
            logging.error(f"Stat failed for {item}: {e}")
            continue
        size = st.st_size
        dt = datetime.fromtimestamp(st.st_mtime)

        if size < 1_000_000:
            bucket = "Small"
        elif size < 50_000_000:
            bucket = "Medium"
        elif size < 500_000_000:
            bucket = "Large"
        else:
            bucket = "Huge"

        month_folder = f"{dt.year}-{dt.month:02d}"
       
       
        MainSet.add(category)
        SubSet.add(month_folder)
        SubSet.add(bucket)

        dest_dir = dest_folder / month_folder / bucket
        if conf["dry_run"]:
            logging.info(f"DRY RUN: would create the folder {category} / {month_folder} / {bucket} and move {item.name} inside it")
            
        else:
            try:
                #Path("a/b/c").mkdir(parents=True, exist_ok=True)
                Path(dest_dir).mkdir(parents=True, exist_ok=True)
                item.rename(dest_dir/item.name)
            except FileExistsError:
                logging.warning(f"Target exists, skipping {dest_dir/item.name}")
                continue
            except PermissionError:
                logging.error(f"No permission to move {item.name}")
                continue
            except FileNotFoundError:
                logging.warning(f"{item} has vanished")
                continue
            except OSError as e:
                logging.error(f"error for {item} : {e}")
                continue
        
    logging.info(f"Main folders: {sorted(MainSet)} | Subfolders: {sorted(SubSet)}")
    
