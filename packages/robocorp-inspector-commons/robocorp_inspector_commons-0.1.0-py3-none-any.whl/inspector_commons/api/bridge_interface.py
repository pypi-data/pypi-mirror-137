import logging
import os

from inspector_commons.bridge.browser_bridge import BrowserBridge
from inspector_commons.config import Config
from inspector_commons.context import Context


class BridgeConnector(BrowserBridge):
    def __init__(self, context: Context, *args, **kwargs):
        super().__init__(context, *args, **kwargs)


def get_logger(config: Config):
    logger = logging.getLogger("inspector_commons: Browser")
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
    """Main for testing BridgeInterface from commandline"""
    config = Config()
    config.set(
        "database",
        "C:\\Users\\avaissi\\Documents\\Robots\\inspector bot\\locators.json",
    )
    config.set("remote", None)
    config.set("debug", True)

    logger = get_logger(config)

    context = Context(logger, config)

    bridge = BridgeConnector(context)
    bridge.start()
    locator = bridge.pick()
    logger.debug(f"Picked locator: {locator}")


if __name__ == "__main__":
    main()
