#!/usr/bin/env python3
# coding:utf-8
import os
import shutil
from libs.utils import mkdir, cleandir, save_json, get_json
from libs.logger import get_traceback

from libs.layout_cad import LayoutCad


class Cad(object):

    def __init__(self, project_id, project_path):
        self.project_id = project_id
        self.path = os.path.abspath(os.path.join(project_path, 'cad'))
        self.project_cad = os.path.abspath(os.path.join(project_path, 'cad.data.json'))
        self.output_path = os.path.abspath(os.path.join(project_path, 'cad', 'output'))
        self.cad_info_json = os.path.abspath(os.path.join(project_path, 'cad', 'cad.info.json'))
        self.cad_output_json = os.path.abspath(os.path.join(self.path, 'cad.output.json'))
        self.cad_output_room_json = os.path.abspath(os.path.join(self.path, 'cad.room.json'))
        self.cad_output_data_json = os.path.abspath(os.path.join(self.path, 'cad.data.json'))

    def info(self):
        return get_json(self.cad_info_json, {})

    def name(self, cad_name="default.dxf"):
        info = self.info()
        if info.get("cad_name"):
            cad_name = info["cad_name"].split(".")[0]
            cad_type = info["cad_name"].split(".")[-1]
            cad_date = info["datetime"].split(" ")[0]
            cad_name = f"{cad_name}-{cad_date}-{self.project_id}.{cad_type}".replace("-", "_")
        return cad_name

    def decode(self):
        try:
            data = LayoutCad.decode_cad(self.path)
            self.reload_decode(data)
            self.reload_project_cad()
            return 1, ""
        except Exception as e:
            get_traceback()
            return 0, f"{e}"

    def init_cad(self):
        mkdir(self.path)

    def clean_output(self):
        cleandir(self.output_path)

    def reload_decode(self, data):
        save_json(self.cad_output_json, data)
        save_json(self.cad_output_room_json, data[0])
        save_json(self.cad_output_data_json, data[1])

    def reload_project_cad(self):
        shutil.copyfile(self.cad_output_data_json, self.project_cad)
