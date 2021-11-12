#!/usr/bin/env python3
# coding:utf-8
import datetime
from flask import request
from models.ip import IpTable, IpEvent
from views.base import BaseHandler


class IpEventHandler(BaseHandler):
    """
    http://127.0.0.1:8008/api/util/ip/event?
    """

    def _get(self, **kwargs):
        ip = request.args.get('ip')
        data = {
            "data": [],
            "count": IpEvent.get_count({})
        }
        filters = {}
        if ip:
            filters["ip"] = ip
        datas = IpEvent.find(filters, limit=100, reverse=True)
        for d in datas:
            _data = d.json()
            _data['creat_date'] = f'{d.creat_date + datetime.timedelta(hours=8)}'[:19]
            data["data"].append(_data)

        return 1, "success", data, {}


class IpTableHandler(BaseHandler):
    """
    http://127.0.0.1:8008/api/util/ip
    """

    def _get(self, **kwargs):
        data = {}
        filters = {}
        datas = IpTable.find(filters, limit=100)
        for ip in datas:
            data[ip.ip] = ip.text

        return 1, "success", data, {}

    def _post(self):
        self.get_formdata()
        ip = self.formdata['ip']
        text = self.formdata['text']
        datas = IpTable.find({'ip': ip}, limit=100)

        if datas:
            update_props = {
                "ip": ip,
                "text": text,
            }
            IpTable.filter_update({"ip": ip}, update_props)
        else:
            new_session = IpTable(
                ip=ip,
                text=text,
            )
            IpTable.add(new_session)

        return 1, "success", {}, {}
