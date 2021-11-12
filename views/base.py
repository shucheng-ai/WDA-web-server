#!/usr/bin/env python3
# coding:utf-8
import json
from flask.views import MethodView
from flask import make_response, request

from config import DEBUG
from libs.logger import logger, get_traceback


def api_logger_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if DEBUG:
                print(e)
            get_traceback()
            res = {"status": -2, "data": {}, "msg": "api server error"}
            return json.dumps(res)

    return wrapper


class BaseHandler(MethodView):
    formdata = {}
    logger = logger

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__()

    def get_arg(self, k, default=None):
        return request.args.get(k, default)

    def get_formdata(self):
        try:
            self.formdata = request.get_json()
        except:
            self.formdata = {}

    def json_response(self, status, msg='', data={}, **kwargs):
        setkeys = ['cookie', 'headers']
        data = {
            'status': status,
            'msg': msg,
            'data': data,
        }
        data.update(kwargs)
        if not data.get('errors'):
            data['errors'] = []
        data = json.dumps(data)
        resp = make_response(data)
        for _key in setkeys:
            if kwargs.get(_key):
                set_data = kwargs[_key]
                for k, v in set_data.items():
                    if _key == 'cookie':
                        resp.set_cookie(k, v)
                    elif _key == 'headers':
                        resp.headers[k] = v
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Max-Age'] = 1678000
        return resp

    def _get(self):
        return 0, '', {}, {}

    @api_logger_wrapper
    def get(self):
        staus, msg, data, kwargs = self._get()
        return self.json_response(staus, msg, data, **kwargs)

    def _post(self):
        return 0, '', {}, {}

    @api_logger_wrapper
    def post(self):
        staus, msg, data, kwargs = self._post()
        return self.json_response(staus, msg, data, **kwargs)

    def _put(self):
        return 0, '', {}, {}

    @api_logger_wrapper
    def put(self):
        staus, msg, data, kwargs = self._put()
        return self.json_response(staus, msg, data, **kwargs)

    def _delete(self):
        return 0, '', {}, {}

    @api_logger_wrapper
    def delete(self):
        staus, msg, data, kwargs = self._delete()
        return self.json_response(staus, msg, data, **kwargs)
