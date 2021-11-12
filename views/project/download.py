#!usr/bin/env python3
# coding:utf-8
import os
import requests
from flask import send_from_directory, send_file
from flask import request

from ..base import BaseHandler
from project import Project
from project.cad import Cad
from project.fixture import Fixture
from libs.utils import mkdir
from config import DXF2DWG_SERVER

from tools.generate import generate3d, static
from tools.renderer import generateCad, models_on_cad, dxf2png


class DownloadCadHandler(BaseHandler):
    def get(self):
        project_id = self.get_arg('project_id')
        _project = Project(project_id=f'{project_id}')
        generate_dxf(project_id)
        #
        _cad = Cad(project_id=f'{project_id}', project_path=_project.path)
        # _cad_info = _cad.info()
        #
        # _fixture = Fixture(project_id=project_id, project_path=_project.path)
        #
        cad_name = _cad.name(cad_name="design.dxf")
        #
        # filename = check_backup(self, _project, 'design.dxf')
        #
        # if not os.path.exists(filename):
        #     history, scene = get_input(_project)
        #     generateCad(scene, history, dxfpath=_project.cad_path, outpath=_project.output_path)
        #     models_on_cad(jsonfile=_fixture.fixture_json,
        #                   outpath=_project.output_path,
        #                   dxfpath=_project.cad_output_path)

        return send_from_directory(_project.output_path, 'design.dxf', as_attachment=True, attachment_filename=cad_name)


class DownloadCADDwgHandler(BaseHandler):

    def get(self):
        project_id = self.get_arg('project_id')
        _project = Project(project_id=f'{project_id}')
        _cad = Cad(project_id=f'{project_id}', project_path=_project.path)
        cad_name = _cad.name(cad_name="design.dxf").replace("dxf", "dwg")

        dxf_path = os.path.join(_project.output_path, 'design.dxf')

        if not os.path.exists(dxf_path):
            generate_dxf(project_id)

        dwg_path = os.path.join(_project.output_path, 'design.dwg')

        with open(dxf_path, "rb") as f:
            data = f.read()
            url = DXF2DWG_SERVER
            files = {'file': data}
            r = requests.post(url, files=files)
            with open(dwg_path, 'wb') as f2:
                f2.write(r.content)

        # return dwg_path
        return send_from_directory(_project.output_path,
                                   'design.dwg',
                                   as_attachment=True,
                                   attachment_filename=cad_name)


class Download3DHandler(BaseHandler):
    def get(self):
        project_id = self.get_arg('project_id')
        _project = Project(project_id=f'{project_id}')
        _fixture = Fixture(project_id=project_id, project_path=_project.path)

        mkdir(_project.output_path)
        if not os.path.exists(_fixture.fixture_json):
            _fixture.save([])
        static(jsonfile=_fixture.fixture_json, outpath=_project.output_path)

        filename = check_backup(self, _project, 'design.gltf')
        if not os.path.exists(filename):
            history, scene = get_input(_project)
            generate3d(scene, history, outpath=_project.output_path)
        return send_from_directory(_project.output_path, 'design.gltf', as_attachment=True)


class DownloadPngHandler(BaseHandler):
    def get(self):
        project_id = self.get_arg('project_id')
        _project = Project(project_id=f'{project_id}')

        mkdir(_project.output_path)
        history, scene = get_input(_project)
        dxf2png(scene, history, outpath=f'{_project.output_path}/', thumbnail=2048)
        pngname = "thumbnail.png"
        return send_from_directory(_project.output_path,
                                   pngname,
                                   as_attachment=True,
                                   attachment_filename=pngname)


def generate_dxf(project_id):
    _project = Project(project_id=f'{project_id}')

    _cad = Cad(project_id=f'{project_id}', project_path=_project.path)
    _cad_info = _cad.info()

    _fixture = Fixture(project_id=project_id, project_path=_project.path)

    filename = check_backup(None, _project, 'design.dxf')

    if not os.path.exists(filename):
        history, scene = get_input(_project)
        generateCad(scene, history, dxfpath=_project.cad_path, outpath=_project.output_path)
        models_on_cad(jsonfile=_fixture.fixture_json,
                      outpath=_project.output_path,
                      dxfpath=_project.cad_output_path)


def get_input(_project):
    _history = _project.get_history()
    history = {}
    for k, v in _history.items():
        history[k] = v['plan_history']

    scene = _project.get_cad_data()
    del scene['navigation']

    return history, scene


def check_backup(obj, _project, filename):
    mkdir(_project.output_path)
    backup = request.args.get('backup', '0')
    filename = os.path.join(_project.output_path, filename)
    if os.path.exists(filename) and backup == '0':
        os.remove(filename)
    return filename
