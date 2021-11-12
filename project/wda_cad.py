#!/usr/bin/env python3
# coding:utf-8
import os
import shutil
from libs.utils import mkdir, cleandir, save_json, get_json
from libs.logger import get_traceback

from libs.layout_cad import LayoutCad

from config import WDA_CAD_PROJECT_PATH

print(WDA_CAD_PROJECT_PATH)


class WdaCad(object):

    def __init__(self, project_id):
        self.project_id = project_id
        self.path = os.path.abspath(os.path.join(WDA_CAD_PROJECT_PATH, f'{project_id}'))
        self.cad_dir = os.path.abspath(os.path.join(WDA_CAD_PROJECT_PATH, f'{project_id}', 'cad'))
        # self.project_cad = os.path.abspath(os.path.join(project_path, 'cad.data.json'))
        # self.output_path = os.path.abspath(os.path.join(project_path, 'cad', 'output'))
        # self.cad_info_json = os.path.abspath(os.path.join(project_path, 'cad', 'cad.info.json'))
        # self.cad_output_json = os.path.abspath(os.path.join(self.path, 'cad.output.json'))
        # self.cad_output_room_json = os.path.abspath(os.path.join(self.path, 'cad.room.json'))
        # self.cad_output_data_json = os.path.abspath(os.path.join(self.path, 'cad.data.json'))
