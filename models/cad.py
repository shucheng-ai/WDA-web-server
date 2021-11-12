#!/usr/bin/env python3
# coding:utf-8
"""
cad library database model
"""
import json
import datetime
from sqlalchemy import Integer, Column, String, DateTime
from .base import Base, BaseModel
from config import CONFIG

BASE_TITLE = CONFIG.ENV_CAD.lower().replace("-", "_")


class BaseCADProject(object):
    _keys = ["id", "uid", "username", "name", "company", "type", "note", "status",
             "version", "descript", "background", "other1", "other2", "other3"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(64), nullable=True)
    username = Column(String(256), nullable=True)
    group = Column(String(256), nullable=True)
    company = Column(String(256), nullable=True)
    creat_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)
    master = Column(String(64), nullable=True)
    type = Column(String(64), nullable=True)
    name = Column(String(256), nullable=True)
    note = Column(String(1000), nullable=True)  # json.dump({status})
    status = Column(String(32), nullable=True)  # '', 'pending', 'success', 'fail', 'waiting', 'processing'
    version = Column(String(64), nullable=True, default="0")
    delete = Column(Integer, nullable=True, default=0)
    descript = Column(String(512), nullable=True)
    background = Column(String(512), nullable=True)  # 背景图片
    other1 = Column(String(64), nullable=True)  # hash: '': hidden; 'hash': visible unique
    other2 = Column(String(64), nullable=True)  # api token
    other3 = Column(String(64), nullable=True)

    def get_note(self):
        note = {}
        if self.note:
            try:
                note = json.loads(self.note)
            except:
                pass
        return note


class CadProject(Base, BaseCADProject, BaseModel):
    __tablename__ = f'{BASE_TITLE}_project'

    @classmethod
    def create(cls, user, project_id=None):
        if not project_id:
            res = cls.add(cls(
                name="new project",
                update_date=datetime.datetime.utcnow(),
                uid=user.get("uid", ""),
                username=user.get("name", ""),
                status='empty',
            ))
        else:
            res = cls.add(cls(
                id=project_id,
                name="new project",
                update_date=datetime.datetime.utcnow(),
                uid=user.get("uid", ""),
                username=user.get("name", ""),
                status='empty',
            ))
        project_id = res["id"]
        cls.update(project_id, {
            "name": f"project-{project_id}"
        })
        return res

    def set_satus(self, status, status_detail):
        note = self.get_note()
        note.update(status_detail)
        CadProject.update(self.id, {
            "status": status,
            "note": json.dumps(note),
            "update_date": datetime.datetime.now()
        })


CadProject.init()
