#!/usr/bin/env python3
# coding:utf-8
from libs.logger import logger_wrapper, logger, get_traceback
import os
import json
import base64
from config import TMP_INPUT_PATH, PROJECT_LOG_PATH
from libs.utils import mkdir, generate_md5, dic_to_list
from libs.error import Error

from tools.renderer import render, side_view, front_view
from tools.utils import estimate_area_from_stock
# from tools.cad_decoder import decode_dxf, decode_dwg
from tools import analysis as layoutAnalysis

import demo

try:
    import layout as baseLayout
    from layout import base_rack_setting, base_rack_list, generate_plan_within_region, base_rack_setting, \
        base_region_setting, base_algorithm_setting, base_region_connection_setting
    from layout import error as layoutError

    layout_flag = True
except Exception as e:
    get_traceback()
    logger.error("beaver core import fail!")
    base_rack_setting = None
    base_rack_list = None
    layout_flag = False

DEFAULT_ROOM = demo.room
DEFAULT_REGION = demo.region
DEFAULT_MOVINT_PATH = demo.moving_path
DEFAULT_HISTORY = demo.history
DEFAULT_BASE_RACK = demo.base_rack
DEFAULT_INFO = demo.info

DEFAULT_REGION_INFO, _ = base_region_setting("")
DEFAULT_ALGORITHMN_INFO, _ = base_algorithm_setting("")
DEFAULT_REGION_CONNECTION_INFO, _ = base_region_connection_setting("")


def set_layout_log(path):
    try:
        baseLayout.set_log_path(path)
    except:
        get_traceback()


set_layout_log(f"{PROJECT_LOG_PATH}/")


class LayoutTools(object):
    default_region_info = {**DEFAULT_REGION_INFO, **DEFAULT_REGION_CONNECTION_INFO}
    default_algorithm_info = DEFAULT_ALGORITHMN_INFO

    @staticmethod
    def render(
            path=None,
            storage_id=0,
            room=DEFAULT_ROOM,
            region=DEFAULT_REGION,
            moving_path=DEFAULT_MOVINT_PATH,
            history=DEFAULT_HISTORY,
            base_rack=DEFAULT_BASE_RACK,
            region_info=DEFAULT_REGION_INFO,
            algorithm_info=DEFAULT_ALGORITHMN_INFO,
            rack_info=None,
    ):
        # output_path = os.path.abspath(os.path.join(path, 'output'))
        # output_sotrage_path = os.path.abspath(os.path.join(path, 'output', f'{storage_id}'))
        # logger.info(f"{output_sotrage_path}")
        # mkdir(output_sotrage_path)
        # output_sotrage_path = f'{output_sotrage_path}/'
        project_log_path = os.path.abspath(os.path.join(path, 'log'))
        mkdir(project_log_path)
        set_layout_log(f"{project_log_path}/")

        if not region_info:
            region_info = DEFAULT_REGION_INFO
        if not algorithm_info:
            algorithm_info = DEFAULT_ALGORITHMN_INFO

        info = {**region_info, **algorithm_info}
        if not rack_info:
            rack_info, _ = base_rack_setting(base_rack)

        data = {}
        errors = []
        # room = {}
        try:
            # raise
            region_form = baseLayout.region_in_room(region, room)
            if not moving_path.get("soft_moving_paths"):
                moving_path["soft_moving_paths"] = []
            connection_item = baseLayout.region_connection(region, moving_path, base_rack, rack_info, info)
            """
            http://gitlab.shucheng-ai.com/layout/main/issues/5
            layout.generate_plan_within_region(room, region, connection_item, history, base_rack, rack_info, info)
            connection_item = layout.region_connection(region, _connection_item, type, params, info)
            """
            plan = generate_plan_within_region(room,
                                               region_form,
                                               connection_item,
                                               history,
                                               base_rack,
                                               rack_info,
                                               info
                                               )
        except layoutError.InterfaceError as e:
            get_traceback()
            data["status"] = -1
            data["errors"] = [
                Error(
                    app="core",
                    handler="calculate_plan",
                    error_type="InterfaceError",
                    e=e,
                ).json()
            ]
            return data
        except layoutError.MethodError as e:
            get_traceback()
            data["status"] = -1
            data["errors"] = [
                Error(
                    app="core",
                    handler="calculate_plan",
                    error_type="MethodError",
                    e=e,
                ).json()
            ]
            return data
        except layoutError.StorageError as e:
            get_traceback()
            data["status"] = -1
            data["errors"] = [
                Error(
                    app="core",
                    handler="calculate_plan",
                    error_type="StorageError",
                    e=e,
                ).json()
            ]
            return data
        except layoutError.ParameterError as e:
            get_traceback()
            data["status"] = -1
            data["errors"] = [
                Error(
                    app="core",
                    handler="calculate_plan",
                    error_type="ParameterError",
                    e=e,
                ).json()
            ]
            return data
        except layoutError.UnknownError as e:
            get_traceback()
            data["status"] = -1
            data["errors"] = [
                Error(
                    app="core",
                    handler="calculate_plan",
                    error_type="UnknownError",
                    e=e,
                ).json()
            ]
            return data
        except Exception as e:
            get_traceback()
            data["status"] = -1
            data["errors"] = [
                Error(
                    app="core",
                    handler="calculate_plan",
                    error_type="None",
                    msg="[core] caculate plan error.",
                    e=e
                ).json()
            ]
            return data

        try:
            plan_info_res = layoutAnalysis.plan_info(plan, base_rack, rack_info)
            plan_info_res = dic_to_list(plan_info_res)
        except Exception as e:
            get_traceback()
            data["status"] = -1
            data["errors"] = [
                Error(
                    app="tools",
                    handler="calculate_plan",
                    error_type="plan_info",
                    msg="[tools] caculate plan info error.",
                    e=e,
                ).json()
            ]
            return data

        render_res = render(plan, base_rack, rack_info)
        # rack_params = rackinfo_to_params(rack_info)
        # rack_params = {base_rack: rack_params}
        # print(rack_info)
        try:
            # raise
            # side_view_res = side_view(base_rack, rack_info, thumbnail=512, path=output_sotrage_path)
            side_view_res = LayoutTools.some_view(base_rack, rack_info, t="side_view")
        except Exception as e:
            # side_view_res = []
            data["status"] = -1
            data["errors"] = [
                Error(
                    app="tools",
                    handler="calculate_plan",
                    error_type="side_view",
                    msg="[tools] side view error.",
                    e=e,
                ).json()
            ]
            return data

        try:
            front_view_res = LayoutTools.some_view(base_rack, rack_info, t="front_view")
        except Exception as e:
            data["status"] = -1
            data["errors"] = [
                Error(
                    app="tools",
                    handler="calculate_plan",
                    error_type="front_view",
                    msg="[tools] front view error.",
                    e=e,
                ).json()
            ]
            return data

        # data["history"] = plan
        # data["data"] = render_res
        addition = {
            "side_view": side_view_res,
            "front_view": front_view_res,
            "plan_info": plan_info_res,
        }

        # data["formdata"] = {
        #     "rack_info": rack_info,
        #     "rack_params": rack_params,
        # }
        data["status"] = 1
        data["errors"] = errors
        data["plan_addition"] = addition
        data["plan_render"] = render_res
        data["plan_history"] = plan
        # with open(f"{DEMO_PATH}/test.render.out.json", "w") as writefile:
        #     json.dump(render_res, writefile)

        return data

    @staticmethod
    def some_view(base_rack, rack_info, thumbnail=256, t="side_view"):
        formdata = {
            'base_rank': base_rack,
            'rack_info': rack_info,
        }
        hash = generate_md5(formdata)
        _path = os.path.abspath(os.path.join(TMP_INPUT_PATH, hash))
        _path += "/"
        mkdir(_path)
        img_path = os.path.abspath(os.path.join(_path, f'{t}.png'))
        if not os.path.exists(img_path):
            # generate png
            if t == "side_view":
                print(f"generate side view img {t}")
                side_view(base_rack, rack_info, thumbnail=thumbnail, path=_path)
            else:
                print(f"generate front view img {t}")
                front_view(base_rack, rack_info, thumbnail=thumbnail, path=_path)
        else:
            print("img exist")

        with open(img_path, 'rb') as image_file:
            encoded_string = base64.b64encode(
                image_file.read()).decode('utf-8')
            data = f'data:image/png;base64,{encoded_string}'
            return data

    @staticmethod
    @logger_wrapper
    def estimate_area_from_stock(stock=None):
        return estimate_area_from_stock(stock=stock)

    @staticmethod
    @logger_wrapper
    def decode_dxf(path=None):
        # return decode_dxf(path=path)
        pass

    @staticmethod
    @logger_wrapper
    def decode_dwg(path=None):
        # return decode_dxf(path=path)
        pass

    @staticmethod
    @logger_wrapper
    def rack_data(t=None):
        d = (None, None)
        l = []
        try:
            l = base_rack_list()
            if t:
                d = base_rack_setting(t)
        except Exception as e:
            print(e)
        return {'list': l, 'data': d[0], 'priority' : d[1]}


def rackinfo_to_params(data):
    res = {}
    for k, v in data.items():
        res[k] = v['value']
    return res


def test_side_view():
    t = 'apr'
    p = {'apr': {'aisle_width': 3000, 'allow_involvded_column': 1, 'apr_depth': 1, 'beam_height': 120,
                 'floor_clearance': 0, 'max_pallet_per_face': 3, 'moving_path_width': 3000, 'package_depth': 1200,
                 'package_gap': 100, 'package_height': 1000, 'package_width': 1000, 'pallet_per_face': 2,
                 'shortcut_width': 3000, 'storage_depth': 1000, 'storage_gap': 300, 'storage_width': 2300,
                 'underpass_for_moving_path': 1, 'underpass_for_shortcut': 1, 'underpass_height': 2500,
                 'underpass_pallet_per_face': 3, 'upright_depth': 90, 'upright_height': 6000,
                 'upright_top_reserved_end': 300, 'upright_width': 90, 'upward_clearance': 150}}
    print(t, p)
    try:
        r = front_view(t, p, thumbnail=512, path=None)
        print(r)
    except Exception as e:
        print(e)

# test_side_view()
