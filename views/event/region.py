#!/usr/bin/env python3
# coding:utf-8
from views.base import BaseHandler
import layout

class RegionHandler(BaseHandler) :
    def _post(self) :
        self.get_formdata()
        region = self.formdata['region']
        room = self.formdata['room']

        return 1, "", layout.region_in_room(region, room), {}
