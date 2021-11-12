#!/usr/bin/env python3
# coding:utf-8
import os
import json
import shutil
from libs.utils import mkdir, cleandir, save_json, get_json
from libs.logger import get_traceback


class ConnectionItem(object):

    def __init__(self, project_id, project_path):
        self.project_id = project_id
        self.project_path = project_path
        self.connection_item = os.path.abspath(os.path.join(project_path, 'moving_path.json'))
        self.cad_path = os.path.abspath(os.path.join(project_path, 'cad'))
        self.cad_output_json = os.path.abspath(os.path.join(self.cad_path, 'cad.output.json'))
        self.cad_output_room_json = os.path.abspath(os.path.join(self.cad_path, 'cad.room.json'))
        self.cad_output_data_json = os.path.abspath(os.path.join(self.cad_path, 'cad.data.json'))

    def reload(self):
        """
        blocks
        moving_paths = moving_paths + soft_moving_paths
        """
        data = {
            "soft_moving_paths":[],
            "moving_paths": [],
            "blocks": [],
        }
        try:
            cad_data = get_json(self.cad_output_room_json)
            for _, room in cad_data.items():
                room_connection_item = room["connection_item"]
                moving_paths = room_connection_item["moving_paths"] + room_connection_item["soft_moving_paths"]
                blocks = room_connection_item["blocks"]

                data["moving_paths"] += moving_paths
                data["blocks"] += blocks

                soft_moving_paths = room_connection_item["soft_moving_paths"]
                data["soft_moving_paths"] += soft_moving_paths
        except:
            get_traceback()
        finally:
            save_json(self.connection_item, data)

    def clear(self) :
        save_json(self.connection_item, {
            "soft_moving_paths":[],
            "moving_paths": [],
            "blocks": [],
        })
