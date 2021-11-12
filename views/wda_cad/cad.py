#!/usr/bin/env python3
# coding:utf-8
import datetime
from views.base import BaseHandler

from models.cad import CadProject
from models.project import Project as ProjectModel

from project import Project
from project.fixture import Fixture
from project.cad import Cad
from project.room import Room
from project.connection_item import ConnectionItem
from project.wda_cad import WdaCad

from app.wda import wdaauth, get_projcet_bymodel, create_project_bymodel

from libs.utils import copy_dir, save_json


class WdaCadHandler(BaseHandler):
    """
    url: http://127.0.0.1:8008/api/wda_cad/
    """

    @wdaauth.wda_auth
    def _get(self, **kwargs):
        """
            return:
                {
                "id": 1,
                "uid": "-1",
                "username": "test",
                "name": "房山.dxf",
                "company": null,
                "type": null,
                "note": "{\"is_upload\": \"success\", \"filename\": \"\\u623f\\u5c71.dxf\", \"is_decode\": \"success\", \"is_3d\": \"success\"}",
                "status": "success",
                "version": "0",
                "descript": null,
                "background": "/api/project/project?type=file&project_id=1&filename=cad/output/0/thumbnail.png&",
                "other1": "",
                "other2": null,
                "other3": null
                }
        """
        user = kwargs.get("wda_user", None)
        status = 0
        data = []
        if not user:
            return status, "login require", {}, {}
        uid = user["uid"]
        # username = user["name"]
        # print(uid)

        cads = CadProject.find(limit=100,
                               filters={
                                   "uid": f"{uid}",
                                   "status": "success",
                               },
                               reverse=True)
        for cad in cads:
            data.append(cad.json())
        status = 1

        return status, "", data, {}

    @wdaauth.wda_auth
    def _post(self, **kwargs):
        """
        use wda_cad cad
        """
        user = kwargs.get("wda_user", None)
        uid = user["uid"]
        # username = user["name"]
        status = 0
        data = {}
        self.get_formdata()
        cad_id = self.formdata["id"]

        _new = {
            'name': "new project",
            'id': ProjectModel.get_maxid() + 1
        }
        new_session = ProjectModel(**_new)
        new = ProjectModel.add(new_session)
        project_id = new['id']
        filters = {'id': project_id}
        values = {'name': f'project-{project_id}'}
        ProjectModel.filter_update(filters, values)
        data["new_id"] = project_id

        Project.create(project_id)
        _project = Project(project_id)
        _fixture = Fixture(project_id=project_id, project_path=_project.path)
        _fixture.save([])
        _cad = Cad(project_id=project_id, project_path=_project.path)
        _cad.init_cad()
        _room = Room(project_id=project_id, project_path=_project.path)
        _connection_item = ConnectionItem(project_id=project_id, project_path=_project.path)

        wda_cad = WdaCad(cad_id)
        wda_cad_data = CadProject.find_byid(cad_id)
        """
        {'id': 4, 'uid': '-1', 'username': 'test', 
        'name': '未标注_A2_单层_横向_方形.dxf', 'company': None, 
        'type': None, 'note': '{"is_upload": "success", "filename": "\\u672a\\u6807\\u6ce8_A2_\\u5355\\u5c42_\\u6a2a\\u5411_\\u65b9\\u5f62.dxf", "is_decode": "success", "is_3d": "success"}', 'status': 'success', 'version': '0', 'descript': None, 'background': '/api/project/project?type=file&project_id=4&filename=cad/output/0/thumbnail.png&', 'other1': '', 'other2': None, 'other3': None}
        """
        copy_dir(wda_cad.cad_dir, _project.cad_dir)
        # _cad.clean_output()
        # _cad.decode()
        _cad.reload_project_cad()
        _room.reload_project_room()
        _room.reload_room_addition()
        _connection_item.reload()
        _project.save_json_data('history', {})

        save_json(_cad.cad_info_json, {
            "base_name": wda_cad_data.name,
            "cad_name": wda_cad_data.name,
            "cad_type": "dxf",
            "cad_hash": "",
            "datetime": f"{datetime.datetime.now()}",
        })

        status = 1

        return status, "", data, {}
