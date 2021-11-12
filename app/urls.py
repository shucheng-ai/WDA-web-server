#!/usr/bin/env python3
# coding:utf-8

import os
from config import APP_PATH, ROOT_PATH
from importlib import import_module
from libs.logger import logger, get_traceback

viewspath = os.path.abspath(os.path.join(APP_PATH, "views"))


def get_urls():
    views = []
    res = []
    for _, dir_names, _ in os.walk(viewspath, topdown=True):
        views = dir_names
        break

    for viewname in views:
        if viewname[0] == '_':
            continue
        pathname = os.path.abspath(os.path.join(viewspath, viewname))
        urlname = os.path.abspath(os.path.join(pathname, 'urls'))
        urlname = urlname.replace(APP_PATH, "")[1:].replace("/", ".").replace("\\", ".")
        try:
            url_module = import_module(urlname)
            urls = getattr(url_module, 'urls', [])
            res += urls
        except:
            get_traceback()

    return res


def init_urls(app):
    url_list = get_urls()
    count = 0
    for item in url_list:
        count += 1
        try:
            name = "router-{}".format(count)
            app.add_url_rule(item[0], view_func=item[1].as_view(name))
            logger.info(f"name:{name}, url:{item[0]}")
        except:
            get_traceback()
