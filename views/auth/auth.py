#!/usr/bin/env python3
# coding:utf-8
from flask import redirect

from views.base import BaseHandler
from config import DEPLOY
from app.wda import wdaauth, get_projcet_bymodel, create_project_bymodel
from models.project import Project as ProjectModel

from .utils import create_project


class AuthHandler(BaseHandler):

    @wdaauth.wda_auth
    def _get(self, **kwargs):
        res = {
            "is_auth": None,
            "user": kwargs.get("wda_user", None)
        }
        return 1, "", res, {}


class AuthProjectHandler(BaseHandler):

    @wdaauth.wda_auth
    def _get(self, **kwargs):
        """
        1. 验证project合法性
        /api/auth/project?project_id=xxx&
        """
        user = kwargs.get("wda_user", None)
        project_id = self.get_arg("project_id", "")
        res = {
            "is_auth": None,
            "user": user,
            "errpage": "/404"
        }
        _project = ProjectModel.find_byid(f'{project_id}')
        if not _project:
            res["is_auth"] = False
            return 1, "", res, {}

        if DEPLOY == 0:
            # 单机模式跳过验证
            res["is_auth"] = True
        else:
            uid = user["uid"]
            if f'{_project.uid}' == f'{uid}':
                res["is_auth"] = True
            else:
                res["is_auth"] = False
                res["errpage"] = "/401"

        return 1, "", res, {}


class CheckPorjectHandler(BaseHandler):
    """
    验证project有效性并重定向 & 初始化
    http://layout2.shucheng-ai.com/api/auth/project/check?project_id=1&
    http://127.0.0.1:8008/api/auth/project/check?project_id=11&
    """

    @wdaauth.wda_auth
    def get(self, **kwargs):
        user = kwargs.get("wda_user", None)
        project_id = self.get_arg("project_id", "")

        res = f"/v2/project/step2?id={project_id}&step=1"

        if DEPLOY == 0:
            # 单机模式无效api
            return "无效 api（403）", 403
        else:
            _project_bymodel = get_projcet_bymodel(project_id)
            if not _project_bymodel:
                return "404 no project", 404

            if f"{user['uid']}" == f"{_project_bymodel.uid}":
                _project = ProjectModel.find_byid(f'{project_id}')
                if not _project:
                    # 创建新项目
                    create_project_bymodel(_project_bymodel)
                    create_project(project_id, user['uid'])
                    return redirect(res, code=302)
                else:
                    # 重定向到项目
                    return redirect(res, code=302)
            else:
                return "操作不合法（401）", 401
