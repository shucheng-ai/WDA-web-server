#!/usr/bin/env python3
# coding:utf-8
import os
import json
import zipfile
import datetime
import requests
from shutil import copyfile
from flask import request, send_file

from ..base import BaseHandler
from project import Project
from project.cad import Cad
from config import TMP_PATH, BASE_PROJECT_PATH, DWG_PATH, DWG2DXF_SERVER, TMP_INPUT_PATH
from libs.utils import mkdir, make_session_id, generate_md5

from models.project import Project as ProjectModel
from models.ip import add_ip_event

BASE_CAD_PATH = os.path.abspath(os.path.join(BASE_PROJECT_PATH, 'cad'))
CAD_ZIP_PATH = os.path.abspath(os.path.join(TMP_PATH, 'zip'))

mkdir(BASE_CAD_PATH)


def reload_path():
    mkdir(TMP_PATH)
    mkdir(TMP_INPUT_PATH)
    mkdir(CAD_ZIP_PATH)


reload_path()


class UploadHandler(BaseHandler):
    def save_file(self, content):
        today = datetime.datetime.now().strftime("%Y%m%d")
        rand = make_session_id()[:8]
        name = f'{today}.{rand}.zip'
        path = os.path.abspath(os.path.join(CAD_ZIP_PATH, name))
        with open(path, "wb") as f:
            f.write(content)
        return name, path

    def decompress(self, zippath, filetype="dxf"):
        fz = zipfile.ZipFile(zippath, 'r')
        dir_path = f"{zippath}.dir"
        for file in fz.namelist():
            fz.extract(file, dir_path)
        fz.close()
        path = os.path.abspath(os.path.join(dir_path, f'wda.{filetype}'))
        return path

    def save_cad(self, cad_path, cad_type='dxf'):
        with open(cad_path, "rb") as f:
            content = f.read()
        cad_hash = generate_md5(content)
        new_path = os.path.abspath(os.path.join(BASE_CAD_PATH, f'{cad_hash}.{cad_type}'))
        with open(new_path, "wb") as f2:
            f2.write(content)
        return new_path, cad_hash

    def save_project_cad(self, cad_path, project):
        project_cad = os.path.abspath(os.path.join(project.path, 'cad'))
        mkdir(project_cad)
        project_cad_path = os.path.abspath(os.path.join(project_cad, 'wda.dxf'))
        copyfile(cad_path, project_cad_path)

    def save_project_cad_info(self, cad_name, cad_hash, cad_type, project_path, base_name):
        project_cad = os.path.abspath(os.path.join(project_path, 'cad'))
        project_cad_info = os.path.abspath(os.path.join(project_path, 'cad', 'cad.info.json'))
        with open(project_cad_info, "w") as f:
            f.write(json.dumps({
                "base_name": base_name,
                "cad_name": cad_name,
                "cad_type": cad_type,
                "cad_hash": cad_hash,
                "datetime": f"{datetime.datetime.now()}",
            }))

    def save_dwg(self, path):
        with open(path, "rb") as f:
            content = f.read()
        dwg_hash = generate_md5(content)
        save_path = os.path.abspath(os.path.join(DWG_PATH, f'{dwg_hash}.dwg'))
        with open(save_path, "wb") as f2:
            f2.write(content)

    def dwg2dxf(self, cadpath):
        outcadpath = cadpath.replace('dwg', 'dxf')
        # save dwg
        self.save_dwg(cadpath)
        with open(cadpath, "rb") as f:
            data = f.read()
            url = DWG2DXF_SERVER
            files = {'file': data}
            r = requests.post(url, files=files)
            with open(outcadpath, 'wb') as f2:
                f2.write(r.content)
        return outcadpath

    def _post(self):
        file = request.files['file']
        filecontent = file.read()

        reload_path()

        project_id = self.get_arg("project_id")
        filename = self.get_arg("filename")
        base_name = self.get_arg("filename")
        # cad_type = self.get_arg("cad_type")
        cad_type = filename.split(".")[-1]
        # B2_多层_方形.dxf dxf
        # Sample_5YX.dwg dwg

        zipname, zippath = self.save_file(filecontent)
        zip_cad_path = self.decompress(zippath, cad_type)

        if cad_type == "dwg":
            # dwg to dxf
            zip_cad_path = self.dwg2dxf(zip_cad_path)

        cad_path, cad_hash = self.save_cad(
            cad_path=zip_cad_path,
            cad_type="dxf",
        )

        _project = Project(project_id=project_id)
        self.save_project_cad(cad_path, _project)

        filename = filename.replace("dwg", "dxf")
        self.save_project_cad_info(filename, cad_hash, cad_type, _project.path, base_name)

        data = {
            "id": project_id,
            "filename": filename,
            "z": zipname,
            "p": _project.path,
            "d": cad_path,
            "ch": cad_hash
        }

        # add ip event
        _project_obj = ProjectModel.find_byid(f'{project_id}')

        add_ip_event(
            project_id=project_id,
            project_name=_project_obj.name,
            event_name="upload_cad",
            note=f"{filename}",
            ip=request.environ.get('HTTP_X_REAL_IP', ''),
            ip2=request.remote_addr,
        )

        return 1, "", data, {}


class FileHandler(BaseHandler):

    def get(self):
        project_id = self.get_arg('id')
        project_file = self.get_arg('file')
        filename = project_file.split("/")[-1]

        _project = Project(project_id=f'{project_id}')
        _cad = Cad(project_id=f'{project_id}', project_path=_project.path)
        cad_name = _cad.name(cad_name="design.dxf")
        cad_name = f'original_{cad_name}'

        if project_file == "/cad/wda.dxf":
            filename = cad_name

        filepath = _project.get_filename(project_file)

        return send_file(
            filepath,
            as_attachment=True,
            attachment_filename=filename
        )
