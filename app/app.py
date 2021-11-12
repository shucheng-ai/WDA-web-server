# !/usr/bin/env python3
# coding:utf-8
import json
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import DIST_STATIC_PATH, DIST_INDEX_PATH, PROJECT_PATH, STORAGE_PATH, LOG_PATH, TMP_PATH, \
    TMP_INPUT_PATH, BASE_PROJECT_PATH, GLOBAL_PATH, PROJECT_LOG_PATH, DIST_3D_PATH, DIST_3D_INDEX, DWG_PATH, DEPLOY, \
    HOMEPAGE, ERRPAGE
from app.urls import init_urls
from libs.utils import mkdir
# from models.task import Task
# from models.cad import CadProject

mkdir(BASE_PROJECT_PATH)
mkdir(PROJECT_PATH)
mkdir(GLOBAL_PATH)
mkdir(STORAGE_PATH)
mkdir(DWG_PATH)
mkdir(TMP_PATH)
mkdir(TMP_INPUT_PATH)
mkdir(PROJECT_LOG_PATH)

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder=DIST_STATIC_PATH,
    template_folder=DIST_STATIC_PATH
)
CORS(app)


@app.route('/project')
@app.route('/v2')
@app.route('/v2/project')
@app.route('/v2/cad')
@app.route('/v2/test')
def index():
    with open(DIST_INDEX_PATH, "r") as f:
        index_data = f.read()
    return index_data


@app.route('/')
@app.route('/index')
@app.route('/projects')
@app.route('/log')
@app.route('/test')
def index_projects():
    if DEPLOY == 0:
        with open(DIST_INDEX_PATH, "r") as f:
            index_data = f.read()
        return index_data
    else:
        return "404 not found.", 404


@app.route('/project/<path>')
@app.route('/v2/project/<path>')
def project_index(path):
    with open(DIST_INDEX_PATH, "r") as f:
        index_data = f.read()
    return index_data


if DEPLOY == 0:
    @app.route('/api/log')
    def log_handler():
        txt = ""
        with open(LOG_PATH, "r") as f:
            content = f.readlines()
        for _content in content:
            print(_content)
            txt += f"<div>{_content}</div>"
        txt = f"""
            <html>
                {txt}
            </html>
        """
        return txt


@app.route('/3d')
@app.route('/3d/')
def index_3d():
    with open(DIST_3D_INDEX, "r") as f:
        text = f.read()
        return text


@app.route('/static-3d/<path:path>')
def static_3d(path):
    return send_from_directory(DIST_3D_PATH, path)


@app.route('/api/config')
def index_config():
    return json.dumps({
        "status": 1,
        "deploy": DEPLOY,
        "homepage": HOMEPAGE,
        "errpage": ERRPAGE
    })


@app.route('/404')
def index_404():
    return "404 not found.", 404


@app.route('/401')
def index_401():
    return "操作不合法（401）.", 401


init_urls(app)
