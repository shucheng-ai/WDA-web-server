#!/usr/bin/env python3
# coding:utf-8
import os

class Config(object):
    def __init__(self):
        pass

    def set(self, key, default, t="str"):
        if t == "int":
            try:
                value = os.environ.get(key, default)
                value = int(value)
            except:
                value = default
        else:
            value = os.environ.get(key, default)
        setattr(self, key, value)