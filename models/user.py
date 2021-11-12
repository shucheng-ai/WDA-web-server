#!/usr/bin/env python3
# coding:utf-8
from sqlalchemy import Integer, Column, String, DateTime, Boolean
from .base import Base, BaseModel
import datetime
from config import CONFIG

BASE_TITLE = CONFIG.ENV_LAYOUT2.lower().replace("-", "_")


class User(Base, BaseModel):
    __tablename__ = f'{BASE_TITLE}_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creat_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_login_date = Column(DateTime, nullable=True)
    last_update_date = Column(DateTime, nullable=True)
    username = Column(String(256), nullable=False, unique=True)
    password = Column(String(256), nullable=False, unique=True)
    is_active = Column(Boolean, default=False)
    is_super = Column(Boolean, default=False)
    email = Column(String(64), nullable=True)
    phone = Column(String(64), nullable=True)
    nickname = Column(String(256), nullable=True)


User.init()
if not User.find_byid(_id=1):
    new = User(
        id=1,
        username="test",
        password="test",
    )
    User.add(new)
