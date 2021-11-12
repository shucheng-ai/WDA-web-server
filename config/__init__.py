#!/usr/bin/env python3
# coding:utf-8
import os
import sys
from .config import Config
from .v1 import *

"""
config 2.0
"""
CONFIG = Config()
CONFIG.set("ENV_TITLE", "WDA-LAYOUT2")
CONFIG.set("ENV_LAYOUT2", "WDA-LAYOUT2")
CONFIG.set("ENV_CAD", "WDA-CAD")
CONFIG.set("ENV_DB_TYPE", "pg")  # sqlite, pg

# db use cloud db || local use 15434
CONFIG.set("ENV_DB_HOST", "172.17.0.1")
CONFIG.set("ENV_DB_PORT", "15434")
CONFIG.set("ENV_DB_USERNAME", "admin")
CONFIG.set("ENV_DB_PASSWORD", "admin")
CONFIG.set("ENV_DB_DBNAME", "shucheng-layout2")

# auth db
CONFIG.set("ENV_AUTH_DB_HOST", "172.17.0.1")
CONFIG.set("ENV_AUTH_DB_PORT", "15432")
CONFIG.set("ENV_AUTH_DB_USERNAME", "admin")
CONFIG.set("ENV_AUTH_DB_PASSWORD", "admin")
CONFIG.set("ENV_AUTH_DB_DBNAME", "shucheng")

# cloud db
CONFIG.set("ENV_CLOUD_DB_HOST", "172.17.0.1")
CONFIG.set("ENV_CLOUD_DB_PORT", "15433")
CONFIG.set("ENV_CLOUD_DB_USERNAME", "admin")
CONFIG.set("ENV_CLOUD_DB_PASSWORD", "admin")
CONFIG.set("ENV_CLOUD_DB_DBNAME", "shucheng")

# redis
CONFIG.set("ENV_REDIS_HOST", "172.17.0.1")
CONFIG.set("ENV_REDIS_PORT", 15479, "int")  # 6379
CONFIG.set("ENV_REDIS_DB", 0, "int")

print(CONFIG.__dict__)
