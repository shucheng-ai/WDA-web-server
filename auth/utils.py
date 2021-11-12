#!/usr/bin/env python3
# coding:utf-8
from flask import request
from config import CONFIG


def get_auth(user, groups):
    uid = user.get('uid', 0)
    auth = False
    admin = False
    if uid > 0:
        auth = True
    if groups.get("admin"):
        admin = True
    if not CONFIG.ENV_DEPLOY == 1:
        # 单机部署非云端
        admin = True
        auth = True
    return auth, admin


def check_project_auth(project, uid, admin):
    if admin:
        return True
    else:
        if f"{project.uid}" == f"{uid}":
            return True
        else:
            return False
