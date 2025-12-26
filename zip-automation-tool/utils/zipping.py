import logging
from pathlib import Path
from typing import Any, Dict
import zipfile

def Zip(p: Path, conf: Dict[str, Any]) -> None:
    conf["zip_mode"] = conf["zip_mode"].strip().lower()
    conf["include_root_files"] = conf["include_root_files"].strip().lower()
    folders_count = 0
    zips_created = 0
    files_zipped = 0

    try:
        root_files = [x for x in p.iterdir() if x.is_file()]
    except (PermissionError, FileNotFoundError, OSError) as e:
        logging.error(f"Failed to scan root directory {p}: {e}")
        return
    
    out_raw = conf.get("output_path")
    out_dir = Path(out_raw) if out_raw else Path(conf["target_path"])
    out_dir.mkdir(parents=True, exist_ok=True)

    if conf["zip_mode"] == "single_archive":
        logging.info("Single archive mode: Root files always included")
        zip_name = conf.get("single_archive_name",f"{p.name}_all.zip")
        zip_path = out_dir / zip_name

        if conf["dry_run"]:
            logging.info(f"Would create a single archive at {zip_path}")
            return
        
        try:
            with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
                
                for rf in root_files:
                    z.write(rf, arcname=rf.relative_to(p))
                    files_zipped += 1

                # include subfolders
                for item in p.iterdir():
                    if not item.is_dir():
                        continue

                    iterator = item.rglob("*") if conf["recursive"] else item.glob("*")
                    for f in iterator:
                        if f.is_file():
                            z.write(f, arcname=f.relative_to(p))
                            files_zipped += 1

            #zips_created += 1
            logging.info(f"Created single archive {zip_path} with {files_zipped} files")

        except (PermissionError, OSError,zipfile.BadZipFile) as e:
                   logging.error(f"single archive failed: {e}") 
        return

    for item in p.iterdir():
        
        if item.is_file():
            root_files.append(item)
            continue
        if not item.is_dir():
            continue
        
        folders_count +=1
        zip_path = out_dir / f"{item.name}.zip"
        if conf["dry_run"] == True:
            logging.info(f"DRY RUN: would create {zip_path} from {item.name}")
            continue
        try:
            with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
                iterator  = item.rglob("*") if conf["recursive"] else item.glob("*")
                for f in iterator:
                    if f.is_file():
                        z.write(f, arcname=f.relative_to(item))
                        files_zipped += 1
            zips_created += 1
            logging.info(f"Created {zip_path} from {item.name}")

        except PermissionError:
            logging.error(f"No permission to access {item.name}")
            continue
        except OSError as e:
            logging.error(f"Error when zipping: {item.name} : {e}")
            continue
        except zipfile.BadZipFile as e:
            logging.error(f"Error: {e}")
            continue
        
    if root_files:
        if conf["include_root_files"] == "ignore":
            logging.info(f"Ignored {len(root_files)} root files, (include_root_files == 'ignore')")

        elif conf["include_root_files"] == "separate_zip":
           zip_path = out_dir / "root_files.zip"
           if conf["dry_run"]:
               logging.info(f"DRY RUN: would create {zip_path} for {len(root_files)} root files")
           else:
               try:
                   with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
                    for f in root_files:
                        z.write(f,arcname=f.name)
                        files_zipped += 1
                    zips_created += 1
                    logging.info(f"Created {zip_path} for {len(root_files)} root files")    
                   
               except (PermissionError, OSError, zipfile.BadZipFile) as e:
                   logging.error(f"Failed to zip root file: {e}")

    logging.info(f"Per folder zip done. Folders seen: {folders_count}, "
                 f"Zips created: {zips_created}, Files zipped {files_zipped}")

