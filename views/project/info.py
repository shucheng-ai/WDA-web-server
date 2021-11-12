#!/usr/bin/env python3
# coding:utf-8
from ..base import BaseHandler
from libs.utils import dic_to_list
from layout import base_rack_list
from tools import analysis as baseLayoutAnalysis

connection_info = ['moving_path', 'block']
collision_info = ['obstacle', 'guard', 'evitable']
region_info = ['region']
room_info = ['room']
plan_info = base_rack_list()

class SomeInfoHandler(BaseHandler):

    def get_data(self, d, t, p):
        data = None
        msg = ""
        try:
            if t in region_info:
                data = baseLayoutAnalysis.region_info(d, t, p)
            elif t in collision_info:
                data = baseLayoutAnalysis.collision_info(d, t, p)
            elif t in connection_info:
                data = baseLayoutAnalysis.connection_info(d, t, p)
            elif t in room_info:
                data = baseLayoutAnalysis.room_info(d, t, p)
            elif t in plan_info :
                data = baseLayoutAnalysis.plan_info(d, t, p)
            status = 1
        except Exception as e:
            status = -1
            msg = f"{e}"
        return status, msg, data

    def _post(self):
        """
        http://gitlab.shucheng-ai.com/layout/tools/issues/4
        type: "" / "moving_path" / "obstacle" / "room"

        - region_info(([0, 0],[1000, 1000]), "", {})
        - connection_info({"box" : ([0, 0],[100, 100]), "direction" : [0,1]}, "moving_path", {})
        - collision_info([[0, 0],[1000, 1000]], "obstacle", {})
        - room_info(test_room, type = "room", params = {})

        # data = baseLayoutAnalysis.region_info(([0, 0], [1000, 1000]), "", {})
        # data = baseLayoutAnalysis.collision_info([[0, 0], [1000, 1000]], "obstacle", {})
        # data = baseLayoutAnalysis.connection_info({"box": ([0, 0], [100, 100]), "direction": [0, 1]}, "moving_path", {})
        # data = baseLayoutAnalysis.room_info(test_room, "room", {})

        test_room = {
                "bbox": [[-368992, -551579], [-318302, -442808]],
                "connection_item": {},
                "evitables": [],
                "guards": [[[-368492, -442809], [-367992, -545066]], [[-368492, -545066], [-367442, -544680]]],
                "obstacles": [[[-368557, -551579], [-368491, -550908]], [[-345702, -478407], [-334781, -477986]]]
        }
        """
        self.get_formdata()
        formdata_data = self.formdata["data"]
        formdata_type = self.formdata["type"]
        formdata_params = self.formdata.get("params", {})

        status, msg, data = self.get_data(formdata_data, formdata_type, formdata_params)
        data = dic_to_list(data)

        return status, msg, data, {}
