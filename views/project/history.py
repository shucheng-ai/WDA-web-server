#!/usr/bin/env python3
# coding:utf-8
from flask import request
from ..base import BaseHandler

from project import Project


class ProjectHistoryHandler(BaseHandler):

    def _get(self):
        project_id = request.args.get('id', '0')
        session_id = request.args.get('session_id')

        _project = Project(project_id=project_id)
        _data = dict_to_list(_project.get_history())
        data = []
        for d in _data:
            """
            new_history["room_id"] = room_id
            new_history["region_info"] = region_info
            new_history["algorithm_info"] = algorithm_info
            """
            # print(d["data"].keys())
            # dict_keys(['storage_id', 'storage_group_id', 'plan_history', 'plan_render', 'plan_addition'])
            render_data = d["data"]["plan_render"]
            render_data.update(d["data"]["plan_addition"])
            data.append({
                "id": d["id"],
                "data": {
                    "data": d["data"]["plan_render"],
                    "info": {"quantity": 0},
                    "storage_id": d["data"]["storage_id"],
                    "storage_group_id": d["data"]["storage_group_id"],
                    "room_id": d["data"].get("room_id", ""),
                    "region_info": d["data"].get("region_info", None),
                    "algorithm_info": d["data"].get("algorithm_info", None),
                }
            })
        info = {
            "project_id": project_id,
            "session_id": session_id
        }
        return 1, "", data, info

    def _post(self):
        return 1, "", {}, {}

    def _delete(self):
        self.get_formdata()
        project_id = self.formdata["project_id"]
        storage_id = self.formdata["storage_id"]
        storage_group_id = self.formdata.get("storage_group_id")
        _type = self.formdata.get("type", "storage")  # group/storage
        _project = Project(project_id=project_id)
        history = _project.get_history()
        res = {
            "storages": [],
            "groups": [],
            "del_storages": [],
            "del_groups": []
        }

        if storage_group_id:
            res["del_groups"].append(f"{storage_group_id}")

        for k, v in history.items():
            _storage_id = f'{v.get("storage_id")}'
            _storage_group_id = f'{v.get("storage_group_id")}'
            # print(_storage_id, _storage_group_id)
            if _type == "storage" and f'{_storage_id}' == f'{storage_id}':
                # print("delete storage")
                res["del_storages"].append(_storage_id)
            elif not _type == "storage" and f'{_storage_group_id}' == f'{storage_group_id}':
                # print("delete group")
                res["del_storages"].append(_storage_id)
                res["del_groups"].append(_storage_group_id)
            else:
                res["storages"].append(_storage_id)
                res["groups"].append(_storage_group_id)

        for k in res["del_storages"]:
            try:
                del history[k]
            except Exception as e:
                print(e)

        _project_storage_input = _project.get_storage_input_data()
        for k in res["del_groups"]:
            try:
                if _project_storage_input.get(k):
                    del _project_storage_input[k]
            except Exception as e:
                print(e)

        _project.save_storage_input_data(_project_storage_input)
        _project.save_history(history)

        return 1, "", res, {}


def dict_to_list(dic):
    res = []
    for k, v in dic.items():
        try:
            res.append({
                "id": k,
                "data": v
            })
        except:
            continue
    return res
