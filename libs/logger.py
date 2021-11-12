#!/usr/bin/env python3
# coding:utf-8
import logging
import traceback
from config import LOG_PATH, LOG_LEVER, LOG_NAME, APP_PATH, DEBUG
import sys


def configure_logging():
    fmt = "%(asctime)s | %(levelname)s | %(message)s | %(filename)s/%(funcName)s/%(lineno)d"
    datefmt = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        # DEBUG,INFO,WARNING,ERROR,CRITICAL
        level=LOG_LEVER,
        format=fmt,
        datefmt=datefmt,
        filename=LOG_PATH,
        filemode='w'
    )

    logger = logging.getLogger(LOG_NAME)

    return logger


logger = configure_logging()
logger.warning("logger:")
logger.warning(f"logger level:{LOG_LEVER}")
logger.warning(f"logger path:{LOG_PATH}")
logger.warning((f"app path: {APP_PATH}"))

logger.info(f'path:{sys.path}')


def get_traceback():
    logger.error('%s', traceback.format_exc())
    traceback.print_exc()


def logger_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if DEBUG:
                print(e)
            get_traceback()
            return None
    return wrapper
