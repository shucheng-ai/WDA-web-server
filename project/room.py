#!/usr/bin/env python3
# coding:utf-8
import os
import json
import shutil
from libs.utils import mkdir, cleandir, save_json, get_json
from libs.logger import get_traceback

import layout as baseLayout


class Room(object):

    def __init__(self, project_id, project_path):
        self.project_id = project_id
        self.room = os.path.abspath(os.path.join(project_path, 'room.json'))
        self.room_addition = os.path.abspath(os.path.join(project_path, 'room.addition.json'))
        self.cad_path = os.path.abspath(os.path.join(project_path, 'cad'))
        self.cad_output_json = os.path.abspath(os.path.join(self.cad_path, 'cad.output.json'))
        self.cad_output_room_json = os.path.abspath(os.path.join(self.cad_path, 'cad.room.json'))
        self.cad_output_data_json = os.path.abspath(os.path.join(self.cad_path, 'cad.data.json'))

    def reset(self):
        save_json(self.room, {})
        save_json(self.room_addition, {})

    def reload_project_room(self):
        shutil.copyfile(self.cad_output_room_json, self.room)

    def reload_room_addition(self):
        data = get_json(self.cad_output_room_json)
        room_addition = {}
        for k, v in data.items():
            room_addition[k] = {}
            _walls = v['walls']
            _data = baseLayout.convert_wall(_walls)
            room_addition[k]['obstacles'] = _data
        save_json(self.room_addition, room_addition)

    def get_data(self):
        try:
            data = get_json(self.room)
        except:
            data = {}
            get_traceback()
        return data

    def get_addition(self):
        try:
            data = get_json(self.room_addition)
        except:
            data = {}
            get_traceback()
        return data

    def get_room_formdata(self, room_id, room):
        data = room[room_id]
        obstacles = data.get("obstacles", [])
        data["obstacles"] = obstacles
        room_addition = self.get_addition()
        room_addition = room_addition.get(room_id, {})
        obstacles_addition = room_addition.get("obstacles", [])
        data["obstacles"] = data["obstacles"] + obstacles_addition
        return data
