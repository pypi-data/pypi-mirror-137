import logging
import os
from pathlib import Path
from typing import Optional

from inspector_commons.config import Config
from inspector_commons.database import Database


class DatabaseConnector(Database):
    def __init__(
        self, path: Optional[str] = None, load_on_start: Optional[bool] = None
    ):
        super().__init__(path, load_on_start)

    def is_same_path(self, path):
        return Path(path).samefile(Path(self.path))


def get_logger(config: Config):
    logger = logging.getLogger("inspector_commons: DB")
    for handler in logger.handlers:
        logger.removeHandler(handler)

    log_level = logging.DEBUG if config.get("debug") else logging.INFO
    log_datefmt = "%Y/%m/%d %H:%M:%S"
    log_format = "%(asctime)s.%(msecs)03d › %(levelname)s › %(name)s › %(message)s"
    home = config.get("home")
    os.makedirs(home, exist_ok=True)
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=log_datefmt,
        handlers=[
            logging.FileHandler(home / "inspector_commons.log", "w"),
            logging.StreamHandler(),
        ],
    )
    return logger


def main():
    """Main for testing DatabaseConnector from commandline"""
    config = Config()
    config.set(
        "database",
        "C:\\Users\\avaissi\\Documents\\Robots\\inspector bot\\locators.json",
    )
    config.set("remote", None)
    config.set("debug", True)

    logger = get_logger(config)

    db_connect = DatabaseConnector(config.get("database"), load_on_start=True)
    locator = db_connect.get("Googlecom")
    logger.debug(f"Loaded locator: {locator}")


if __name__ == "__main__":
    main()
