#!/usr/bin/env python3
# coding:utf-8
from flask import request
import os
import sys
import json

from ..base import BaseHandler
from libs.utils import mkdir
from libs.layout_tools import LayoutTools
from config import STORAGE_PATH, TEST_ID
from project import Project


class StorageHandler(BaseHandler):

    def _get(self):
        t = request.args.get('type', 'storage')
        name = request.args.get('name', 'name')
        project_id = request.args.get('project_id', TEST_ID)
        save_type = request.args.get('save_type', 'global')  # base, global, project
        _project = Project(project_id=project_id)

        data = []
        info = {}

        if t == 'list':
            _data = LayoutTools.rack_data()
            for name in _data['list']:
                base_rank = get_base_storage_info(name)
                base_rank["save_type"] = "base"
                data.append(base_rank)
            data += get_all_storages()
            data += _project.get_all_storages()
        else:
            _data = LayoutTools.rack_data(name)
            basestorages = _data['list']
            if name in basestorages:
                for key in _data['priority']:
                    sotrage_data = _data['data'][key]
                    sotrage_data['id'] = sotrage_data['name']
                    sotrage_data['value'] = sotrage_data.get('value', '')
                    sotrage_data['value_type'] = get_value_type(
                        sotrage_data['value'])
                    if sotrage_data['value_type'] in ['int', 'float']:
                        sotrage_data['range'] = sotrage_data.get(
                            'range', get_range())
                    sotrage_data['input_type'] = get_intput_type(sotrage_data)
                    data.append(sotrage_data)
                info = get_base_storage_info(name)
            elif save_type == "project":
                storage_data = _project.get_storage_info(name)
                info = storage_data.get("info", {})
                data = storage_data.get("data", [])
            else:
                storage_data = get_storage_data(name)
                info = storage_data.get("info", {})
                data = storage_data.get("data", [])

        return 1, '', data, {'info': info}

    def _post(self):
        res = {}

        self.get_formdata()
        _type = self.formdata.get('type', 0)  # 1:global, 0:project
        project_id = self.formdata.get('project_id', TEST_ID)
        save_as_new = self.formdata["save_as_new"]
        storage_id = self.formdata["info"]["id"]
        base_rack = self.formdata["info"]["base_rack"]

        baselist = LayoutTools.rack_data()
        baselist = baselist['list']

        if storage_id in baselist or save_as_new == 1:
            if _type == 1:
                #  save to global
                count = 1
                while 1:
                    new_id = f'{base_rack}_{count}'
                    storage_config_path = os.path.abspath(
                        os.path.join(STORAGE_PATH, f"{new_id}.json"))
                    if not os.path.exists(storage_config_path):
                        storage_id = new_id
                        break
                    count += 1
            else:
                # save to project
                count = 1
                _project = Project(project_id=project_id)
                _project_storage_path = os.path.abspath(os.path.join(_project.path, "storage"))
                mkdir(_project_storage_path)
                while 1:
                    new_id = f'{base_rack}_{count}'
                    storage_config_path = os.path.abspath(
                        os.path.join(_project_storage_path, f"{new_id}.json"))
                    if not os.path.exists(storage_config_path):
                        storage_id = new_id
                        break
                    count += 1
        else:
            storage_config_path = os.path.abspath(
                os.path.join(STORAGE_PATH, f"{storage_id}.json"))

        with open(storage_config_path, "w") as f:
            self.formdata["info"]["id"] = storage_id
            f.write(json.dumps(self.formdata))

        res["id"] = storage_id

        return 1, '', res, {}

    def _delete(self):
        self.get_formdata()
        storage_id = self.formdata["info"]["id"]
        save_type = self.formdata["info"].get("save_type", "global")  # global, project
        project_id = self.formdata.get("project_id")
        delete = False

        # # test
        # save_type = "project"
        # project_id = "2"
        # storage_id = "shelf_1"

        if save_type == "global":
            # delete global storage
            storage_config_path = os.path.abspath(
                os.path.join(STORAGE_PATH, f"{storage_id}.json"))
        else:
            # delete project storage
            _project = Project(project_id=project_id)
            storage_config_path = os.path.abspath(
                os.path.join(_project.path, "storage", f"{storage_id}.json"))

        if os.path.exists(storage_config_path):
            os.remove(storage_config_path)
            delete = True

        return 1, '', {"id": storage_id, "delete": delete, "path":storage_config_path}, {}


class StorageImgHandler(BaseHandler):
    def _post(self):
        formdata = request.get_json()
        p = (
            {'aisle_width': {'name': 'aisle_width', 'description': '', 'value': 900, 'range': (1, 100000)},
             'beam_height': {'name': 'beam_height', 'description': '', 'value': 60, 'range': (1, 100000)},
             'floor_clearance': {'name': 'floor_clearance', 'description': '', 'value': 40, 'range': (0, 100000)},
             'max_storage_width': {'name': 'max_storage_width', 'description': '', 'value': 2400, 'range': (1, 100000)},
             'moving_path_width': {'name': 'moving_path_width', 'description': '', 'value': 1500, 'range': (1, 100000)},
             'package_depth': {'name': 'package_depth', 'description': '', 'value': 600, 'range': (1, 100000)},
             'package_gap': {'name': 'package_gap', 'description': '', 'value': 50, 'range': (1, 100000)},
             'package_height': {'name': 'package_height', 'description': '', 'value': 400, 'range': (1, 100000)},
             'package_layers': {'name': 'package_layers', 'description': '', 'value': 2, 'range': (1, 10),
                                'choices': [1, 2]},
             'package_width': {'name': 'package_width', 'description': '', 'value': 400, 'range': (1, 100000)},
             'pallet_per_face': {'name': 'pallet_per_face', 'description': '', 'value': 4, 'range': (1, 10)},
             'storage_width': {'name': 'storage_width', 'description': '', 'value': 1800, 'range': (
                 1, 100000)},
             'shelf_depth': {'name': 'shelf_depth', 'description': '', 'value': 1, 'range': (1, 10), 'choices': [1, 2]},
             'shortcut_width': {'name': 'shortcut_width', 'description': '', 'value': 900, 'range': (1, 100000)},
             'storage_depth': {'name': 'storage_depth', 'description': '', 'value': 600, 'range': (1, 100000)},
             'storage_gap': {'name': 'storage_gap', 'description': '', 'value': 20, 'range': (1, 100000)},
             'upright_depth': {'name': 'upright_depth', 'description': '', 'value': 30, 'range': (1, 100000)},
             'upright_height': {'name': 'upright_height', 'description': '', 'value': 6000, 'range': (1, 100000)},
             'upright_width': {'name': 'upright_width', 'description': '', 'value': 55, 'range': (1, 100000)},
             'upward_clearance': {'name': 'upward_clearance', 'description': '', 'value': 20, 'range': (1, 100000)}}
        )

        # s = LayoutTools.side_view(formdata['base_rack'], p)
        # f = LayoutTools.front_view(formdata['base_rack'], p)
        data = {
            # "list": s + f
        }
        return 1, "", data, {}


def get_intput_type(data):
    if data.get('choices'):
        return "select"
    else:
        return "input"


def get_value_type(value):
    if type(value) == int:
        return "int"
    elif type(value) == float:
        return "float"
    else:
        return "str"


def get_range():
    return [-sys.maxsize, sys.maxsize]


def get_all_storages():
    sotrages = []
    for _, _, file_list in os.walk(STORAGE_PATH):
        for f in file_list:
            data = get_storage_data(f.split(".")[0])
            ftype = f.split(".")[-1]
            if ftype == "json":
                _data = data['info']
                _data["save_type"] = "global"
                sotrages.append(_data)
        break
    return sotrages


def get_storage_data(name):
    storage_config_path = os.path.abspath(
        os.path.join(STORAGE_PATH, f"{name}.json"))
    try:
        with open(storage_config_path, "r") as f:
            data = json.loads(f.read())
            return data
    except:
        return {}


def get_base_storage_info(name):
    return {
        "id": name,
        "name": name,
        "base_rack": name,
    }
