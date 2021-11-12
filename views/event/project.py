#!/usr/bin/env python3
# coding:utf-8
from flask import request
from views.base import BaseHandler
from libs.layout_tools import LayoutTools
from project import Project
from project.room import Room

from models.project import Project as ProjectModel
from models.ip import add_ip_event


class ProjectEventHandler(BaseHandler):

    def get(self):
        return self.json_response(status=1, data="data")


class ProjectPlanEventHandler(BaseHandler):
    """
    """
    default_sotrage_data = {
        'info': {},
        'data': []
    }
    default_moving_path = {
        "moving_paths": [],
        "blocks": []
    }

    def _get(self):
        data = LayoutTools.render(plan=None)
        return 1, "", data, {}

    def _post(self):
        self.get_formdata()
        project_id = self.formdata.get('project_id', '0')

        _project = Project(project_id=project_id)
        _project_room = Room(project_id=project_id, project_path=_project.path)

        storage_data = self.formdata.get("storage_data")

        if not storage_data:
            storage_data = self.formdata.get("sotrage_data", self.default_sotrage_data)

        connection_item = self.formdata.get("connection_item")
        if connection_item:
            moving_path = connection_item
        else:
            moving_path = self.formdata.get("moving_path", self.default_moving_path)

        storage_info = storage_data['info']
        storage_rack_data = storage_data['data']
        rack_info = format_params(storage_rack_data)
        storage_id = storage_info.get("storage_id", "storage-test")
        storage_group_id = storage_info.get("storage_group_id", "storage-test")
        # print(storage_id, storage_group_id, type(storage_group_id))

        _project_storage_input = _project.get_storage_input_data()
        _project_storage_input[storage_group_id] = storage_data
        _project.save_storage_input_data(_project_storage_input)

        region_data = self.formdata['region']
        room_data = self.formdata['room']
        room_id = self.formdata.get("room_id", "room-test")
        region_info = self.formdata.get("region_info", [])
        algorithm_info = self.formdata.get("algorithm_info", [])

        # print(room_data)
        # print(moving_path)

        base_rack = storage_info['base_rack']

        # room = room + room addition
        _room = _project.get_json_data('room')  # room.json
        room = room_data

        # room = {
        #     "bbox": room_data["bbox"],
        #     "obstacles": room_data.get('obstacles', []),
        #     "guards": room_data.get('guards', []),
        #     "isolates": room_data.get('isolates', []),
        #     "evitables": room_data.get('evitables', []),
        # }

        _room[room_id] = room
        _project.save_json_data('room', _room)  # save room.json

        room_formdata = _project_room.get_room_formdata(room_id, _room)

        # movint_path
        _project.save_json_data('moving_path', moving_path)

        region = region_data['bbox']

        _history = _project.get_history()
        history = {}

        for k, v in _history.items():
            history[k] = v['plan_history']
        # print(history)
        print("uiouiouioui")
        print(algorithm_info)
        render_data = LayoutTools.render(
            path=_project.path,
            storage_id=storage_id,
            room=room_formdata,
            region=region,
            moving_path=moving_path,
            history=history,
            base_rack=base_rack,
            region_info=format_data_info(region_info),
            algorithm_info=format_data_info(algorithm_info),
            rack_info=rack_info,
        )
        if render_data["status"] == 1:
            if region_data:
                k_keys = ["plan_history", "plan_render", "plan_addition"]
                new_history = {}
                new_history["storage_id"] = storage_id
                new_history["storage_group_id"] = storage_group_id
                new_history["room_id"] = room_id
                new_history["region_info"] = region_info
                new_history["algorithm_info"] = algorithm_info
                for k in k_keys:
                    new_history[k] = render_data[k]
                _history[storage_id] = new_history
                _project.save_history(_history)

            res_data = {}
            res_data.update(render_data["plan_render"])
            res_data.update(render_data["plan_addition"])

            _project.get_json_data('room')

            # add ip event
            _project_obj = ProjectModel.find_byid(f'{project_id}')

            add_ip_event(
                project_id=project_id,
                project_name=_project_obj.name,
                event_name="caculate_project",
                ip=request.environ.get('HTTP_X_REAL_IP', ''),
                ip2=request.remote_addr,
            )

            return 1, "", res_data, {"errors": render_data["errors"]}
        else:
            msg = "caculate fail"
            errors = render_data["errors"]
            if len(errors) > 0:
                msg = errors[0]['msg']
            return -1, msg, {}, {"errors": errors}


def format_params(data):
    res = {}
    for i in data:
        res[i['id']] = i

    return res


def format_data_info(data):
    res = {}
    for _data in data:
        try:
            _id = _data['id']
            _data.pop('id')
            res[_id] = _data
        except Exception as e:
            res[_data['name']] = _data;
    return res
