#!/usr/bin/env python3
# coding:utf-8
from sqlalchemy import Integer, Column, String, DateTime
from .base import Base, BaseModel
import datetime
from config import CONFIG

BASE_TITLE = CONFIG.ENV_LAYOUT2.lower().replace("-", "_")


class IpTable(Base, BaseModel):
    _keys = ["id", "ip", "text"]
    __tablename__ = f'{BASE_TITLE}_ip_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(128), nullable=True)
    text = Column(String(128), nullable=True)


class IpEvent(Base, BaseModel):
    _keys = ["id", "ip", "text", "username", "uid", "project_id", "project_name", "note",
             "event_type", "event_name", "event_status", "ip", "ip2", "ip3"]
    __tablename__ = f'{BASE_TITLE}_ip_event'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(64), nullable=True)
    username = Column(String(128), nullable=True)
    project_id = Column(String(64), nullable=True)
    project_name = Column(String(128), nullable=True)
    creat_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, nullable=True)
    note = Column(String(512), nullable=True)
    event_type = Column(String(64), nullable=True)
    event_name = Column(String(64), nullable=True)
    event_status = Column(String(32), nullable=True)
    ip = Column(String(128), nullable=True)  # request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip2 = Column(String(128), nullable=True)  # remote_addr
    ip3 = Column(String(128), nullable=True)  # other


IpTable.init()
IpEvent.init()


def add_ip_event(event_name, ip, ip2,
                 ip3="",
                 project_id="",
                 project_name="",
                 event_status="",
                 note="",
                 uid="",
                 username=""):
    if not ip:
        ip = ip2
    new_session = IpEvent(
        project_id=f"{project_id}",
        project_name=project_name,
        event_name=event_name,
        event_status=event_status,
        ip=f"{ip}",
        ip2=f"{ip2}",
        ip3=f"{ip3}",
        note=note,
        uid=uid,
        username=username,
        update_date=datetime.datetime.utcnow(),
    )
    new = IpEvent.add(new_session)
    return new
