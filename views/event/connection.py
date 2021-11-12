from views.base import BaseHandler
from project import Project

class ConnectionItemHandler(BaseHandler) :
    
    def _post(self) :
        self.get_formdata()
        project_id = self.formdata['project_id']
        region = self.formdata['region']
        connection_item = self.formdata['connection_item']
        storage_parameter = self.formdata['storage_parameter']
        region_parameter = self.formdata['region_parameter']

        return 1, "", connection_item, {}
