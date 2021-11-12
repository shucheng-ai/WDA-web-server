#!/usr/bin/env python3
# coding:utf-8
from views.base import BaseHandler
import os
import json

from project.project import Project
from project.cad import Cad
from project.room import Room
from project.connection_item import ConnectionItem
from tools.renderer import generateCad


class CadEventHandler(BaseHandler):
    """
    api: /api/event/cad
    """

    def _post(self):
        self.get_formdata()
        project_id = self.formdata["project_id"]
        command = self.formdata["command"]
        status = 0
        msg = ""

        _project = Project(project_id=project_id)
        _cad = Cad(project_id=project_id, project_path=_project.path)
        _room = Room(project_id=project_id, project_path=_project.path)
        _connection_item = ConnectionItem(project_id=project_id, project_path=_project.path)

        with open(_project.storage_input, "w") as _file:
            json.dump({}, _file)

        if command == "encode" or command == "decode":
            # decode cad
            _cad.init_cad()
            _cad.clean_output()
            status, msg = _cad.decode()

            if status == 1:
                _room.reload_project_room()
                _room.reload_room_addition()

                _connection_item.reload()

                _project.save_json_data('history', {})

        return status, msg, {}, {}


class GreenFieldHandler(BaseHandler):
    def _post(self):
        self.get_formdata()
        project_id = self.formdata['project_id']

        _project = Project(project_id=project_id)
        _cad = Cad(project_id=project_id, project_path=_project.path)
        _room = Room(project_id=project_id, project_path=_project.path)
        _connection_item = ConnectionItem(project_id=project_id, project_path=_project.path)

        rooms = self.formdata['scene']

        _cad.init_cad()
        _cad.clean_output()
        generateCad(rooms, {}, outpath=_cad.path)
        os.rename(os.path.abspath(os.path.join(_cad.path, 'design.dxf')), _project.cad_path)

        status, msg = _cad.decode()

        if status == 1:
            _room.reload_project_room()
            _room.reload_room_addition()

            _connection_item.reload()

            _project.save_json_data('history', {})

        return status, msg, {}, {}
