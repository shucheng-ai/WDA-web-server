#!/usr/bin/env python3
# coding:utf-8
"""
配置 wda-auth && wda-cloud
"""
import datetime
from config import DEPLOY, AUTH_DB_HOST, AUTH_DB_PORT, AUTH_DB_USERNAME, AUTH_DB_PASSWORD, DB_HOST, DB_PORT, \
    DB_USERNAME, DB_PASSWORD

if DEPLOY == 1:
    from wda_decorators.wda import WDA as WDA_AUTH
    from wda_model.wda_model.wda import WDA as WDA_MODEL

    wdaauth = WDA_AUTH(
        db_host=AUTH_DB_HOST,
        db_port=AUTH_DB_PORT,
        db_username=AUTH_DB_USERNAME,
        db_password=AUTH_DB_PASSWORD,
    )

    wdamodel = WDA_MODEL(
        db_host=DB_HOST,
        db_port=DB_PORT,
        db_username=DB_USERNAME,
        db_password=DB_PASSWORD,
    )


    def get_projcet_bymodel(project_id):
        return wdamodel.project.get(id=project_id, engine=wdamodel.db_engine)


    def rename_bymodel(project_id, project_name):
        update_props = {
            'name': project_name,
            'update_date': datetime.datetime.utcnow(),
        }
        wdamodel.project.update(
            engine=wdamodel.db_engine,
            id=project_id,
            data=update_props
        )
        wdamodel.layout2_project.update(
            engine=wdamodel.db_engine,
            id=project_id,
            data=update_props
        )


    def create_project_bymodel(project):
        new_project = wdamodel.layout2_project(
            id=project.id,
            uid=project.uid,
            company=project.company,
            name=project.name,
            username=project.username,
            type='',
        )
        wdamodel.layout2_project.add(new_project, wdamodel.db_engine)

else:
    class DEMO(object):
        def wda_auth(self, func):
            def wda_wrapper(*args, **kwargs):
                kwargs["wda_user"] = {
                    "name": "test",
                    "uid": -1
                }
                return func(*args, **kwargs)

            wda_wrapper.__name__ = func.__name__
            return wda_wrapper


    def get_projcet_bymodel(project_id):
        return None


    def rename_bymodel(project_id, project_name):
        return None


    def create_project_bymodel(project):
        return None


    wdaauth = DEMO()
    wdamodel = DEMO()
