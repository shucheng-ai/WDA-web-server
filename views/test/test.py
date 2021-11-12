#!/usr/bin/env python3
# coding:utf-8
from ..base import BaseHandler

# from libs.layout_tools import LayoutTools

from models.user import User

class TestHandler(BaseHandler):

    def get(self):
        data = {}
        # data['plan'] = LayoutTools.render(plan=None)
        # data['stock'] = LayoutTools.estimate_area_from_stock(stock=None)
        # data['dxf_path'] = LayoutTools.decode_dxf(path=None)
        # data['dwg_path'] = LayoutTools.decode_dwg(path=None)

        return self.json_response(status=1, data=data)
