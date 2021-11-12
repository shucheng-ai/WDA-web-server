#!/usr/bin/env python3
# coding:utf-8
"""
手动倒入cad解析
"""
import os
import json
import datetime
from libs.utils import get_json, save_json
from project.project import Project
from project.cad import Cad
from project.room import Room
from project.connection_item import ConnectionItem

cad_name = "Jinshan Layout.dxf"
project_id = "23"
output = "wda.output.json"

project = Project(project_id=project_id)
cad = Cad(project_id=project_id, project_path=project.path)
cad.init_cad()
cad.clean_output()
room = Room(project_id=project_id, project_path=project.path)
connection_item = ConnectionItem(project_id=project_id, project_path=project.path)

import_file = os.path.abspath(os.path.join(project.path, output))

data = {}
with open(import_file, "r") as f:
    data = eval(f.read())

room_data = {}
rooms = data["rooms"]
scene = data["scene"]
print(data.keys())
print(rooms.keys())
# cad.reload_decode(data)
# cad.reload_project_cad()
save_json(cad.cad_output_data_json, scene)
save_json(cad.cad_output_room_json, rooms)
cad.reload_project_cad()

room.reload_project_room()
room.reload_room_addition()
connection_item.reload()
project.save_json_data('history', {})

project_cad_info = os.path.abspath(os.path.join(project.path, 'cad', 'cad.info.json'))
with open(project_cad_info, "w") as f:
    f.write(json.dumps({
        "base_name": cad_name,
        "cad_name": cad_name,
        "cad_type": 'dxf',
        "cad_hash": '',
        "datetime": f"{datetime.datetime.now()}",
    }))

print(project.path)
print(cad.path)
print(import_file)

print("ok")
