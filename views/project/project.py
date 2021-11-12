#!/usr/bin/env python3
# coding:utf-8
from flask import request

from ..base import BaseHandler

from libs.layout_tools import LayoutTools
from libs.utils import make_session_id

from project import Project
from project.fixture import Fixture
from project.cad import Cad

from models.project import Project as ProjectModel
from models.ip import add_ip_event

from app.wda import rename_bymodel

import json
import datetime


class ProjectListHandler(BaseHandler):
    def _get(self):
        """
        api: /api/project/list?page=1&limit=10&order_by=update_date&reverse=true
        method: get

        page: 页数， 默认为1
        limit: 返回数量限制，范围 [1,100]， 默认为10
        order_by: 排序选择， 默认为 update_date
        reverse: 倒序排序， 默认为 true

        :return:
        {
          status: 1,
          msg: "",
          data: {
            list:[
              {
                id: 4796, // project id
                name: "09-03-11", // project name
                creat_date: "GMT+8 2020-09-03 11:20", // 项目创建时间
                update_date: "GMT+8 2020-09-03 11:31" // 项目最后更改时间
              }
              ...
            ],
            pageinfo:{
              total: 100, // 总 poject 数量，
              limit: 10,  // 每页限制，同request limit参数
              page: 1     // 当前页面
            }
          }
        }
        """
        _page = request.args.get('page', 1)
        limit = request.args.get('limit', 10)
        order_by = request.args.get('order_by', 'update_date')
        reverse = request.args.get('reverse', True)
        project_session_id = request.cookies.get("project_session_id")
        if project_session_id is None:
            project_session_id = f'{datetime.datetime.utcnow().strftime("%Y%m%d")}-{make_session_id()}'

        page = int(_page) - 1
        limit = int(limit)
        props = {
            'offset': limit * page,
            'limit': limit,
            'order_by': order_by,
            'reverse': reverse,
        }
        projects = ProjectModel.find(**props)
        data = {
            'list': [],
            'pageinfo': {
                'limit': limit,
                'page': _page,
            }
        }
        for el in projects:
            creat_date = f'GMT+8 {el.creat_date + datetime.timedelta(hours=8)}'[:22]
            update_date = f'GMT+8 {el.update_date + datetime.timedelta(hours=8)}'[:22]
            data["list"].append({
                'id': el.id,
                'name': el.name,
                'creat_date': creat_date,
                'update_date': update_date
            })
        total = ProjectModel.get_count()
        data['pageinfo']['total'] = total
        return 1, 'ok', data, {}


class ProjectHandler(BaseHandler):

    def _get(self):
        # project db data
        project_id = request.args.get('id', '0')
        # TODO error
        try:
            data = get_protect_by_id(project_id)
            return 1, '', data, {}
        except:
            return 0, '', {}, {}

    def _post(self):
        # create new project db data
        # create new project file data
        # create new project from exist project
        self.get_formdata()
        master_id = None
        if self.formdata:
            master_id = self.formdata.get('master')  # copy a exist project id

        project_name = "new project"
        _new = {
            'name': project_name,
            'id': ProjectModel.get_maxid() + 1
            # 'update_date': datetime.datetime.utcnow()
        }
        new_session = ProjectModel(**_new)
        # insert data to database
        new = ProjectModel.add(new_session)
        project_id = new['id']

        # rename project-projectid
        filters = {'id': project_id}
        values = {'name': f'project-{project_id}'}
        ProjectModel.filter_update(filters, values)

        data = get_protect_by_id(project_id)
        # create file
        Project.create(project_id, master_id=master_id)
        _project = Project(project_id)
        # create fixture
        _fixture = Fixture(project_id=project_id, project_path=_project.path)
        _fixture.save([])

        # add ip event
        add_ip_event(
            project_id=project_id,
            project_name=f'project-{project_id}',
            event_name="create_project",
            ip=request.environ.get('HTTP_X_REAL_IP', ''),
            ip2=request.remote_addr,
        )

        return 1, '', data, {}

    def _put(self):
        self.get_formdata()
        formdata = self.formdata
        try:
            id = formdata.get('id')
            name = formdata.get('name')
            filters = {'id': id}
            values = {'name': name}
            data = ProjectModel.filter_update(filters, values)
            # rename wda model
            rename_bymodel(project_id=id, project_name=name)
            return 1, 'ok', data, {}
        except Exception as e:
            print(e)
            return 0, 'err', {}, {}

    def _delete(self):
        self.get_formdata()
        formdata = self.formdata
        try:
            id = formdata.get('id')
            filters = {'id': id}
            values = {'delete': True}
            data = ProjectModel.filter_update(filters, values)
            return 1, '', data, {}
        except:
            return 0, 'err', {}, {}


class ProjectCadHandler(BaseHandler):

    def _get(self):
        project_id = request.args.get('id', '0')

        res = {
            'project_id': project_id,
            'data': {},
        }

        if Project(project_id=project_id).get_cad_data():
            res['data'] = Project(project_id=project_id).get_cad_data()

        # cad 绘图数据 LayoutTools.decode_dxf(path=None)[0]
        # rooms 房间数据，额外进行存储，前端不需要使用 LayoutTools.decode_dxf(path=None)[1]
        # _project = Project(project_id=1)
        # _project.init_project()

        # data = {
        #     'project_id': project_id,
        #     'data': LayoutTools.decode_dxf(path=None)[0],
        # }

        # generate default cad data json file
        # import json
        # with open('cad.data.json', 'w') as f:
        #     f.write(json.dumps(data['data']))

        return 1, '', res, {}


class ProjectSorageInputHandler(BaseHandler):

    def _get(self):
        project_id = request.args.get('id', '0')

        if Project(project_id=project_id).get_cad_data():
            data = Project(project_id=project_id).get_storage_input_data()

        res = dict_to_list(data)
        return 1, '', res, {}

    def _post(self):
        self.get_formdata()
        project_id = self.formdata.get('project_id', '0')
        storage_data = self.formdata.get("storage_data")
        is_save = self.formdata.get('is_save', True)

        _project = Project(project_id=project_id)

        storage_info = storage_data.get("info")
        storage_rack_data = storage_data['data']
        storage_group_id = str(storage_info.get("storage_group_id", "0"))
        base_rack = storage_info['base_rack']
        rack_info = list_to_dict(storage_rack_data)

        side_view = LayoutTools.some_view(base_rack, rack_info, t="side_view")
        front_view = LayoutTools.some_view(base_rack, rack_info, t="front_view")
        thumbnail = {
            "side_view": side_view,
            "front_view": front_view,
        }
        storage_data["thumbnail"] = thumbnail

        if is_save:
            _project_storage_input = _project.get_storage_input_data()
            _project_storage_input[storage_group_id] = storage_data
            _project.save_storage_input_data(_project_storage_input)

        return 1, '', thumbnail, {}

    def _delete(self):
        self.get_formdata()
        project_id = self.formdata.get('project_id', '0')
        storage_data = self.formdata.get("storage_data")
        storage_info = storage_data.get("info")
        storage_group_id = str(storage_info.get("storage_group_id", "0"))

        _project = Project(project_id=project_id)
        _project_storage_input = _project.get_storage_input_data()

        if _project_storage_input.get(storage_group_id):
            _project_storage_input.pop(storage_group_id)
            _project.save_storage_input_data(_project_storage_input)

        return 1, '', _project_storage_input, {}


class ProjectRoomHandler(BaseHandler):
    """
    api: /api/project/room
    """

    def _get(self):
        project_id = request.args.get('id', '0')

        if Project(project_id=project_id).get_cad_data():
            data = Project(project_id=project_id).get_json_data('room')

        res = dict_to_list(data)
        return 1, '', res, {}

    def _post(self):
        self.get_formdata()
        project_id = self.formdata.get('project_id', '0')
        room_id = self.formdata.get('room_id')
        room_data = self.formdata.get('room', {})

        if not room_id:
            return -1, 'no room id', {}, {}

        room_history = Project(project_id=project_id).get_json_data('room')
        room_history[room_id] = room_data
        Project(project_id=project_id).save_json_data('room', room_history)

        _project = Project(project_id=project_id)
        return 1, 'success', room_history, {}


class ProjectMovingPathHandler(BaseHandler):
    """
    api: /api/project/moving_path
    api: /api/project/connection_item
    """

    def _get(self):
        project_id = request.args.get('id', '0')

        if Project(project_id=project_id).get_cad_data():
            data = Project(project_id=project_id).get_json_data('moving_path')

        res = data
        return 1, '', res, {}

    def _post(self):
        self.get_formdata()
        project_id = self.formdata.get('project_id', '0')
        connection_item = self.formdata.get('connection_item')
        if connection_item:
            moving_path = connection_item
        else:
            moving_path = self.formdata.get('moving_path')
        if not moving_path:
            return -1, 'no moving_path', {}, {}

        Project(project_id=project_id).save_json_data('moving_path', moving_path)

        return 1, 'success', moving_path, {}


class ProjectFixturesHandler(BaseHandler):
    def _get(self):
        """
        get fixture.json
        - /api/project/fixtures?id=5
        get output/static_fixtures.json
        - /api/project/fixtures?id=5&type=static_fixtures
        """
        project_id = self.get_arg('id')
        _type = self.get_arg('type', 'fixtures')
        project = Project(project_id=project_id)
        fixture = Fixture(project_id=project_id, project_path=project.path)
        if _type == 'static_fixtures':
            data = fixture.get_static_fixtures()
        else:
            data = fixture.get()
        return 1, 'success', data, {}

    def _post(self):
        self.get_formdata()
        project_id = self.formdata.get('project_id')
        fixtures = self.formdata.get('fixtures')
        project = Project(project_id=project_id)
        fixture = Fixture(project_id=project_id, project_path=project.path)
        fixture.save(fixtures)
        return 1, 'success', {}, {}


class ProjectInfoHandler(BaseHandler):

    def _get(self):
        _type = request.args.get('type')  # region algorithm cad

        res = {}
        if _type == 'region':
            res['region_info'] = format_info(LayoutTools.default_region_info, _type)
        elif _type == 'algorithm':
            res['algorithm_info'] = format_info(LayoutTools.default_algorithm_info, _type)
        elif _type == 'cad':
            project_ids = self.get_arg('ids', [])
            if not type(project_ids) == list:
                project_ids = json.loads(project_ids)
            res = []
            for project_id in project_ids:
                _res = {'project_id': project_id}
                _project = Project(project_id=project_id)
                _cad = Cad(project_id=project_id, project_path=_project.path)
                _res['cad'] = _cad.info()
                res.append(_res)

        return 1, '', res, {}


def get_protect_by_id(project_id):
    project = ProjectModel.find_byid(f'{project_id}')
    # filters = {'id': project.id}
    # values = {'update_date': datetime.datetime.utcnow()}
    # ProjectModel.filter_update(filters, values)
    data = {
        'id': project.id,
        'name': f'{project.name}',
        'creat_date': f'GMT+8 {project.creat_date + datetime.timedelta(hours=8)}'[:22],
        'update_date': f'GMT+8 {project.update_date + datetime.timedelta(hours=8)}'[:22]
    }
    return data


def format_info(data, t):
    res = []
    for k, v in data.items():
        if v.get('choices'):
            v['input_type'] = 'select'
        else:
            v['input_type'] = 'input'
        if type(v['value']) == int:
            v['value_type'] = 'int'
        elif type(v['value']) == float:
            v['value_type'] = 'float'
        else:
            v['value_type'] = 'str'
        v['id'] = k
        res.append(v)
    return res


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


def list_to_dict(data):
    res = {}
    for i in data:
        res[i['id']] = i

    return res
