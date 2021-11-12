#!/usr/bin/env python3
# coding:utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db import engine

Base = declarative_base()

DBSession = sessionmaker(bind=engine)


class BaseModel(object):
    _keys = []

    @classmethod
    def init(cls):
        if not cls.is_table_exists():
            cls.__table__.create(engine)

    @classmethod
    def is_table_exists(cls):
        name = cls.__tablename__
        res = engine.dialect.has_table(engine, name)
        return res

    @classmethod
    def get_maxid(cls):
        dbsession = DBSession()
        maxid = dbsession.query(cls).order_by(cls.id.desc()).first()
        dbsession.close()
        if maxid:
            return maxid.id
        else:
            return 0

    @classmethod
    def add(cls, new):
        res = {}
        dbsession = DBSession()
        dbsession.add(new)
        dbsession.commit()
        res['id'] = new.id
        dbsession.close()
        return res

    @classmethod
    def delete(cls, _id):
        dbsession = DBSession()
        dbsession.query(cls).filter(cls.id == int(_id)).delete()
        dbsession.commit()
        dbsession.close()
        return

    @classmethod
    def find_byid(cls, _id):
        dbsession = DBSession()
        obj = dbsession.query(cls).get(_id)
        dbsession.close()
        return obj

    @classmethod
    def find(cls, filters={}, offset=0, limit=10, order_by='id', reverse=False):
        dbsession = DBSession()
        if reverse:
            results = dbsession.query(cls).filter_by(**filters).order_by(getattr(cls, order_by).desc()).limit(
                limit).offset(offset).all()
        else:
            results = dbsession.query(cls).filter_by(**filters).order_by(getattr(cls, order_by)).limit(limit).offset(
                offset).all()
        dbsession.close()
        return results

    @classmethod
    def filter_update(cls, filters={}, props={}):
        dbsession = DBSession()
        obj = dbsession.query(cls).filter_by(**filters).update(props)
        dbsession.commit()
        dbsession.flush()
        dbsession.close()
        return obj

    @classmethod
    def get_count(cls, filters={}):
        dbsession = DBSession()
        count = dbsession.query(cls).filter_by(**filters).count()
        dbsession.close()
        return count

    def json(self):
        data = {}
        for k in self._keys:
            data[k] = getattr(self, k, "")
        return data
