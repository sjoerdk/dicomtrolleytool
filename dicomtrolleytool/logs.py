import logging

import coloredlogs

ROOT_LOGGER_NAME = "trolleytool"


def get_module_logger(name):
    """Any logger used in dicomtrolleytool gets its loggers from here.
    Ensures everything is neatly logged under the trollytool root logger
    """
    return logging.getLogger(f"{ROOT_LOGGER_NAME}.{name}")


def install_colouredlogs(level):
    """Use coloured logs"""
    coloredlogs.install(level=level)
