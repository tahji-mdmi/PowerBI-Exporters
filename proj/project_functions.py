# -*- coding: utf-8 -*-
import os
import argparse
import logging
from datetime import datetime, timezone, tzinfo
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import GRANTA_MIScriptingToolkit as gdl
from Configify.config import Config, import_config
from GRANTA_MIScriptingToolkit import granta

current_directory: Path = Path(__file__).parent
parent_directory: Path = current_directory.parent
config_file_path: Path = parent_directory / "config.json"

__version__: str = "0.0.0"
__name__ = "RecentlyModifiedRecordsReport"
logger: logging.Logger
args: argparse.Namespace
config: Config
session: granta.mi.Session  # Streamlined
gdl_session: gdl.GRANTA_MISession  # Foundation


UTC: timezone = timezone.utc
MI_DATE_FORMAT = "%Y-%m-%d"
MI_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def start():
    os.chdir(current_directory)

    get_arguments()
    get_config_contents()

    log_folder_path = parent_directory / "logs"
    start_logging(
        folder_path=log_folder_path, name=__name__, level=config.get("LOG LEVEL")
    )

    logger.info("Version: " + __version__)
    logger.info(config)
    logger.info(args)

    try:
        make_MI_session(config["MI"])
    except Exception as ex:
        logger.exception(ex)
        logger.critical("Could not make MI Session, this script must exit.")
        raise ex
    return


def get_arguments():
    global args
    parser = argparse.ArgumentParser(prog=__name__)
    parser.add_argument("-db-key", "--db-key", help="The database key to use.")
    parser.add_argument("-table-name", "--table-name", help="The table name to use.")
    parser.add_argument(
        "-search-after-datetime",
        "--search-after-datetime",
        type=convert_datetime,
        help="The UTC datetime after which to search."
        + " In format 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS'.",
    )
    args = parser.parse_args()
    return args


def get_config_contents() -> Config:
    global config
    if "config" not in globals():
        config = import_config(config_file_path)
    return config


def parse_datetime_string(
    datetime_string: str, _timezone: tzinfo | None = UTC, ignore_errors=False
) -> datetime | None:
    result = None

    if not isinstance(datetime_string, str):
        if ignore_errors:
            return result

        raise TypeError(
            "Input datetime_string is of type "
            + f"'{type(datetime_string)}'. Expected 'str'"
        )

    _formats = {MI_DATETIME_FORMAT, "%Y-%m-%dT%H%M%S", MI_DATE_FORMAT}

    def _parse(_string, _format):
        try:
            return datetime.strptime(_string, _format)
        except ValueError:
            return None

    for _format in _formats:
        result = _parse(datetime_string, _format)
        if result:
            return result if not _timezone else result.replace(tzinfo=_timezone)

    if ignore_errors:
        return result

    # Raise error
    raise ValueError(
        f"Time data {datetime_string} does not match any of "
        + f'formats {", ".join(_formats)}'
    )


def convert_datetime(datetime: str) -> datetime:
    """This is a wrapper for `parse_datetime_string` for use
    in the argparse `type` parameter. This method should not be
    used outside of argparse!
    """
    # Call parse_datetime_string
    try:
        return parse_datetime_string(datetime)

    # Raise argparse error instead
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Time data {datetime} does must match one of "
            + "formats: 'YYYY-MM-DD', 'YYYY-MM-DDTHH:MM:SS',"
            + " 'YYYY-MM-DDTHH:MM:SS.ffffff'"
        )


def make_MI_session(MI_config: dict) -> granta.Session:
    """Creates an MI Session object with information from the config."""
    global session
    global gdl_session
    service_layer_URL = MI_config["SERVICE LAYER URL"]
    timeout = MI_config.get("TIMEOUT") or 300000

    if MI_config.get("AUTOLOGON"):
        session = granta.connect(service_layer_URL, timeout=timeout, autologon=True)
    else:
        username = MI_config.get("USERNAME", "")
        password = MI_config.get("PASSWORD", "")
        domain = MI_config.get("DOMAIN", "")
        session = granta.connect(
            service_layer_URL, username, password, domain, timeout=timeout
        )
    gdl_session = session.spawn_session()
    return session


def start_logging(
    folder_path: Path = Path("logs"), name: str | None = None, level: str | None = None
) -> logging.Logger:
    global logger
    name = name or str(Path(__file__).parent.parent / ".log")
    name = name + ".log" if not name.lower().endswith(".log") else name
    level = level or "INFO"
    logging.basicConfig(level=logging.getLevelName(level.upper()))
    logger = logging.getLogger(name)
    folder_path.mkdir(exist_ok=True)
    file_path = folder_path / name
    handler = TimedRotatingFileHandler(
        filename=file_path, when="midnight", interval=1, encoding="utf-8"
    )
    handler.suffix = "%Y-%m-%d"
    formatter = logging.Formatter(
        "%(asctime)-24s - %(levelname)-8s - "
        + "%(module)s.%(funcName)s.%(lineno)d - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    gdl.GRANTA_Logging.info = gdl.GRANTA_Logging.debug

    logger.info("-" * 100)
    return logger


list_get = lambda l, x, d=None: d if not l[x : x + 1] else l[x]
list_index = lambda l, x, d=None: l.index(x) if x in l else d
dict_slice = lambda d, start, end: dict(list(d.items())[start:end])
