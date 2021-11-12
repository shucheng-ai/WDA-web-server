#!/usr/bin/env python3
# coding:utf-8
from .test import TestHandler

_api = '/api/test'

urls = [
    [f'{_api}/', TestHandler],
]
