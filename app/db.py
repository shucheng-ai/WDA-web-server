#!/usr/bin/env python3
# coding:utf-8
from sqlalchemy import create_engine
from config import DB_FILE, CONFIG

from libs.logger import logger


def use_sqlite():
    engine = create_engine(DB_FILE)
    return engine


def init_engine(host, port, username, password, dbname):
    db_config = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}"
    logger.warning(db_config)
    engine = create_engine(
        db_config
    )
    return engine


if CONFIG.ENV_DB_TYPE == 'sqlite':
    engine = use_sqlite()
else:
    engine = init_engine(
        CONFIG.ENV_DB_HOST,
        CONFIG.ENV_DB_PORT,
        CONFIG.ENV_DB_USERNAME,
        CONFIG.ENV_DB_PASSWORD,
        CONFIG.ENV_DB_DBNAME,
    )
