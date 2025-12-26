from pathlib import Path
import logging

from utils.config_loader import load_config, IncompleteJson
from utils.logging_setup import setup_logging
from utils.zipping import Zip



def main() -> None:
    config_path = Path(__file__).parent / "config.json"

    try:
        conf = load_config(config_path)
    except IncompleteJson as e:
        # logging isn't configured yet
        print(f"Config error: {e}")
        return

    setup_logging(conf)

    BASE_DIR = Path(__file__).parent
    target_raw = conf["target_path"]
    target_path = Path(target_raw)

    # If user gave a relative path, resolve it relative to the repo folder
    if not target_path.is_absolute():
        target_path = BASE_DIR / target_path
        
    logging.info("Starting run...")
    Zip(target_path, conf)
    logging.info("Finished run.")


if __name__ == "__main__":
    main()
