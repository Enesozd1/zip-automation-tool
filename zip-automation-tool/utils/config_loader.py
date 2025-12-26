import json
from pathlib import Path
from typing import Any, Dict


class IncompleteJson(Exception):
    pass

class InvalidKey(Exception):
    pass

REQUIRED_KEYS = [
    "target_path",
    "zip_mode",
    "include_root_files",
    "dry_run",
    "log_file",
    "log_level",
    "recursive"
]


def load_config(config_path: Path) -> Dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as f:
        conf = json.load(f)

    for key in REQUIRED_KEYS:
        if key not in conf:
            raise IncompleteJson(f"Missing config key: {key}")
    conf["zip_mode"] = conf["zip_mode"].strip().lower()
    conf["include_root_files"] = conf["include_root_files"].strip().lower()
    if conf["zip_mode"] not in ("per_folder", "single_archive"):
        raise InvalidKey(f"The key: {conf['zip_mode']} is invalid")
    if conf["include_root_files"] not in ("ignore", "separate_zip"):
        raise InvalidKey(f"The key: {conf['include_root_files']} is invalid")
    
    # (Optional but helpful) normalize extensions
    # ensures [".txt"] not ["txt"]
    

    return conf
