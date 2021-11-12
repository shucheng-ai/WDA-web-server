#!/usr/bin/env python3
# coding:utf-8
import os
import sys

"""
config 1.0
"""
DEBUG = True
HOST = '0.0.0.0'
PORT = 8000
NAME = 'layout'
DEPLOY = 0  # 0： 单机部署 ； 1: 接入云服务器
HOMEPAGE = "/projects"
ERRPAGE = "/404"

TEST_ID = 0

# path
_PATH = os.path.abspath(os.path.dirname(__file__))
APP_PATH = os.path.abspath(os.path.dirname(_PATH))

ROOT_PATH = os.path.abspath(os.path.dirname(APP_PATH))

WEB_PATH = os.path.abspath(os.path.join(ROOT_PATH, "web"))
DIST_PATH = os.path.abspath(os.path.join(WEB_PATH, "dist"))
DIST_STATIC_PATH = os.path.abspath(os.path.join(WEB_PATH, "dist"))
DIST_INDEX_PATH = os.path.abspath(os.path.join(WEB_PATH, "dist", "index.html"))

WEB_3D_PATH = os.path.abspath(os.path.join(ROOT_PATH, "3d"))
DIST_3D_PATH = os.path.abspath(os.path.join(WEB_3D_PATH, "dist"))
DIST_3D_INDEX = os.path.abspath(os.path.join(DIST_3D_PATH, "index.html"))

# sqlite
DB_FILE_PATH = os.path.abspath(os.path.join(ROOT_PATH, f"{NAME}.db"))
DB_FILE = f'sqlite:///{DB_FILE_PATH}'

# PROJECT PATH
BASE_PROJECT_PATH = os.path.abspath(os.path.join(ROOT_PATH, "project"))
PROJECT_PATH = os.path.abspath(os.path.join(BASE_PROJECT_PATH, "project"))
DWG_PATH = os.path.abspath(os.path.join(BASE_PROJECT_PATH, "dwg"))

# WDA CAD PATH
WDA_CAD_PROJECT_PATH = os.path.abspath(os.path.join(ROOT_PATH, "cad-project", "storage"))

PROJECT_LOG_PATH = os.path.abspath(os.path.join(BASE_PROJECT_PATH, "log"))
GLOBAL_PATH = os.path.abspath(os.path.join(BASE_PROJECT_PATH, "global"))
STORAGE_PATH = os.path.abspath(os.path.join(GLOBAL_PATH, "storage"))

TMP_PATH = os.path.abspath(os.path.join(BASE_PROJECT_PATH, "tmp"))
TMP_INPUT_PATH = os.path.abspath(os.path.join(TMP_PATH, "input"))

DEMO_PATH = os.path.abspath(os.path.join(APP_PATH, "demo"))
DEMO_JSON_PATH = os.path.abspath(os.path.join(DEMO_PATH, "json"))

# tool v2
LIB_TOOL_PATH = os.path.abspath(os.path.join(ROOT_PATH, "tools"))
sys.path.insert(0, LIB_TOOL_PATH)

# core v2
LIB_CORE_PATH = os.path.abspath(os.path.join(ROOT_PATH, "core"))
sys.path.insert(0, LIB_CORE_PATH)

# cad v2
LIB_CAD_PATH = os.path.abspath(os.path.join(ROOT_PATH, "cad"))
sys.path.insert(0, LIB_CAD_PATH)

# auth wda-auth-decorators
AUTH_DECORATORS_PATH = os.path.abspath(os.path.join(ROOT_PATH, "wda-auth-decorators"))

# auth database
AUTH_DB_HOST = "172.17.0.1"
AUTH_DB_PORT = 15432
AUTH_DB_USERNAME = "admin"
AUTH_DB_PASSWORD = "admin"

# model
MODEL_PATH = os.path.abspath(os.path.join(ROOT_PATH, "wda-cloud"))

# model database 172.17.0.1
DB_HOST = "172.17.0.1"
DB_PORT = 15433
DB_USERNAME = "admin"
DB_PASSWORD = "admin"

# logger
LOG_NAME = f"{NAME}"
LOG_LEVER = "INFO"  # "WARNING"
LOG_PATH = os.path.abspath(os.path.join(APP_PATH, f"{NAME}.log"))

# dwg2dxf
DWG2DXF_SERVER = "http://172.17.0.1:8001/dwg2dxf/"
DXF2DWG_SERVER = "http://172.17.0.1:8001/dxf2dwg/"

try:
    from local_config import *
except:
    pass

try:
    from config.cloud import *
except:
    pass

if DEPLOY == 1:
    sys.path.append(AUTH_DECORATORS_PATH)
    sys.path.append(MODEL_PATH)

print("deploy", DEPLOY)
print("homepage", HOMEPAGE)
print(sys.path)
