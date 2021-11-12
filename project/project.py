#!/usr/bin/env python3
# coding:utf-8
import os
import json
import shutil
from config import PROJECT_PATH, DEMO_JSON_PATH
from libs.utils import mkdir

import sysrsync


class Project(object):
    path = None
    history = None

    def __init__(self, project_id=0):
        self.project_id = project_id
        self.path = os.path.abspath(os.path.join(PROJECT_PATH, f'{project_id}'))
        self.history = os.path.abspath(os.path.join(self.path, 'history.json'))
        self.room = os.path.abspath(os.path.join(self.path, 'room.json'))
        self.moving_path = os.path.abspath(os.path.join(self.path, 'moving_path.json'))
        self.cad_data = os.path.abspath(os.path.join(self.path, 'cad.data.json'))
        self.storage_input = os.path.abspath(os.path.join(self.path, 'storage.input.json'))
        self.project_storage = os.path.abspath(os.path.join(self.path, 'storage'))
        self.output_path = os.path.abspath(os.path.join(self.path, 'output'))
        self.cad_dir = os.path.abspath(os.path.join(self.path, 'cad'))
        self.cad_path = os.path.abspath(os.path.join(self.path, 'cad', 'wda.dxf'))
        self.cad_output_path = os.path.abspath(os.path.join(self.path, 'output', 'design.dxf'))

    @classmethod
    def create(cls, project_id, master_id=None):
        # if master id, copy master to new
        path = os.path.abspath(os.path.join(PROJECT_PATH, f'{project_id}'))
        if not os.path.exists(path) and not master_id:
            print("create new project:")
            mkdir(path)
            cls.reload_demo(path)
        elif not os.path.exists(path):
            # copy master project to new
            print(f"coyp project from {master_id}:")
            source = os.path.abspath(os.path.join(PROJECT_PATH, f'{master_id}'))
            print(source)
            sysrsync.run(
                source=source,
                destination=path,
                options=['-a']
            )

    def init_project(self):
        mkdir(self.path)
        mkdir(self.project_storage)

    @staticmethod
    def reload_demo(path):
        filelist = [
            'history.json',
            'cad.data.json',
            'storage.input.json',
            'room.json',
            'moving_path.json',
        ]
        for filename in filelist:
            source = os.path.abspath(os.path.join(DEMO_JSON_PATH, filename))
            target = os.path.abspath(os.path.join(path, filename))
            shutil.copyfile(source, target)

    def get_json_file(self, path):
        try:
            with open(path, "r") as f:
                res = f.read()
                return json.loads(res)
        except:
            return None

    def save_json_file(self, path, data):
        with open(path, "w") as f:
            f.write(json.dumps(data))
            return True

    def get_history(self):
        try:
            return self.get_json_file(self.history)
        except Exception as e:
            print(e)
            return {}

    def save_history(self, data):
        self.save_json_file(self.history, data)

    def get_cad_data(self):
        return self.get_json_file(self.cad_data)

    def save_cad_data(self, data):
        self.save_json_file(self.cad_data, data)

    def get_storage_input_data(self):
        try:
            temp = self.get_json_file(self.storage_input)
            if temp == None:
                return {}
            else:
                return temp
        except Exception as e:
            print(e)
            return {}

    def save_storage_input_data(self, data):
        self.save_json_file(self.storage_input, data)

    def get_json_data(self, key):
        try:
            _path = getattr(self, key)
            return self.get_json_file(_path)
        except Exception as e:
            print(e)
            return {}

    def save_json_data(self, key, data):
        _path = getattr(self, key)
        self.save_json_file(_path, data)

    def get_all_storages(self):
        sotrages = []
        for _, _, file_list in os.walk(self.project_storage):
            for f in file_list:
                ftype = f.split(".")[-1]
                if ftype == "json":
                    storage_config_path = os.path.abspath(
                        os.path.join(self.project_storage, f))
                    with open(storage_config_path, "r") as f:
                        data = f.read()
                        data = json.loads(data)
                        data['info']["save_type"] = "project"
                        sotrages.append(data['info'])
            break
        return sotrages

    def get_storage_info(self, name):
        storage_config_path = os.path.abspath(
            os.path.join(self.project_storage, f'{name}.json'))
        with open(storage_config_path, "r") as f:
            data = f.read()
            data = json.loads(data)
            return data

    def get_filename(self, filename):
        if filename[0] == "/":
            filename = filename[1:]
        path = os.path.abspath(os.path.join(self.path, filename))
        return path


Project.create(project_id=0)
