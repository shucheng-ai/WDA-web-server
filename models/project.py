#!/usr/bin/env python3
# coding:utf-8
from sqlalchemy import Integer, Column, String, DateTime
from .base import Base, BaseModel
import datetime
from config import CONFIG

BASE_TITLE = CONFIG.ENV_LAYOUT2.lower().replace("-", "_")


class Project(Base, BaseModel):
    _keys = ["id", "uid", "creat_date", "name"]
    __tablename__ = f'{BASE_TITLE}_project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(64), nullable=True)
    creat_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    master = Column(String(32), nullable=True)
    type = Column(String(64), nullable=True)
    name = Column(String(256), nullable=True)
    note = Column(String(256), nullable=True)
    status = Column(String(32), nullable=True)
    version = Column(String(64), nullable=True, default="default")
    delete = Column(Integer, nullable=True, default=0)


Project.init()

for id_ in [0]:
    if not Project.find_byid(_id=id_):
        new = Project(
            id=id_,
            name="project0",
            update_date=datetime.datetime.utcnow()
        )
        Project.add(new)
