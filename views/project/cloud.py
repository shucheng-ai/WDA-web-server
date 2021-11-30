#!usr/bin/env python3
# coding:utf-8
import os
import shutil
import random

from ..base import BaseHandler
from project import Project
from project.cad import Cad


class InitPorjectByDemoHandler(BaseHandler):
    """
    /api/project/init_project_by_demo
    """

    def _post(self):
        self.get_formdata()
        project_id = self.formdata.get('project_id')
        v = self.formdata.get('v', 0)  # 0:empty 1: demo
        if not project_id:
            return -1, '', {}, {}

        project = Project(project_id=project_id)
        _cad = Cad(project_id=project_id, project_path=project.path)

        if _cad.is_upload():
            return -2, '', {}, {}

        if f'{v}' == '0':
            t = 'empty_demo'
        else:
            t = 'demo'

        old = f'old-{project_id}-{random.randint(1, 9999)}'
        old_project = Project(project_id=old)

        os.rename(project.path, old_project.path)
        # todo 删除old文件夹
        # shutil.rmtree(old_project.path)

        demo = Project(project_id=t)
        shutil.copytree(demo.path, project.path)

        return 1, 'success', {}, {}
