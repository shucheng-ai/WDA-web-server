#!/isr/bin/env python3
# coding:utf-8
from flask import request
from ..base import BaseHandler

from project import Project
from project.connection_item import ConnectionItem

class RoomDataHandler(BaseHandler) :
    
    def _get(self) :
        pass

    def _delete(self) :
        self.get_formdata()
        project_id = self.formdata['project_id']
        _project = Project(project_id = project_id)
        _connection_item = ConnectionItem(project_id = project_id, project_path= _project.path)

        _connection_item.clear()

        return 1, '', {}, {}

