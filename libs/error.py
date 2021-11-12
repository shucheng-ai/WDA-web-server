#!/usr/bin/env python3
# coding:utf-8

"""
status: -1 未捕获到具体异常，而拿不到数据
status: 1 捕获到具体异常
"""


class Error(object):
    _keys = [
        "error_id",
        "app",
        "msg",
        "handler",
        "level",
        "error_type",
        "status"
    ]

    def __init__(self,
                 handler: str = "",
                 app: str = "",
                 msg: str = "",
                 level: str = "error",
                 error_type: str = "default",
                 status: int = 1,
                 e: object = None
                 ):
        self.handler = handler
        self.app = app
        self.msg = msg
        self.level = level
        self.status = status
        self.e = e
        self.error_type = error_type
        self.generate()

    def generate(self):
        self.error_id = f"{self.handler}:{self.app}:{self.error_type}"
        _msg = 'No active exception to reraise'
        if self.e and f"{self.e}" != _msg:
            self.msg = f"{self.e}"
        if not self.msg:
            self.msg = f"{self.handler}, {self.app}, {self.error_type}, error.".lower()

    def json(self):
        data = {}
        for k in self._keys:
            data[k] = getattr(self, k)
        return data
