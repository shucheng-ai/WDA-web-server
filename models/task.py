#!/usr/bin/env python3
# coding:utf-8
from sqlalchemy import Integer, Column, String, DateTime
from .base import Base, BaseModel
import datetime
from config import CONFIG

BASE_TITLE = CONFIG.ENV_LAYOUT2.lower().replace("-", "_")


class Task(Base, BaseModel):
    """
    task id
    pid
    start
    end
    timeout : ms
    status : wait, processing, success, fail, break
    type
    project_id
    input_path
    output_path
    python3 xxx input output params
    """
    _keys = ["id"]
    __tablename__ = f'{BASE_TITLE}_task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, nullable=True)
    timeout = Column(Integer, nullable=True)
    start = Column(DateTime, default=datetime.datetime.utcnow)
    end = Column(DateTime, nullable=True)
    type = Column(String(256), nullable=True)
    status = Column(String(64), nullable=True)
    note = Column(String(256), nullable=True)
    project_id = Column(String(256), nullable=True)
    input_path = Column(String(256), nullable=True)
    output_path = Column(String(256), nullable=True)
    params = Column(String(512), nullable=True)
    other1 = Column(String(256), nullable=True)
    other2 = Column(String(256), nullable=True)
    other3 = Column(String(256), nullable=True)


Task.init()
