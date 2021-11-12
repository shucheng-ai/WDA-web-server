#!/usr/bin/env python3
# coding:utf-8
from flask import request
from views.base import BaseHandler
from libs.layout_tools import LayoutTools


class CalculateStockAreaEventHandler(BaseHandler):

    def _get(self):
        event_id = request.args.get('id', '')
        print(event_id)

        data = LayoutTools.estimate_area_from_stock(stock=None)
        return 1, '', data, {}

    def _post(self):
        formdata = request.get_json()
        print(formdata)

        data = LayoutTools.estimate_area_from_stock(stock=None)
        return 1, '', data, {}
