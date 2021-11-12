#!/usr/bin/env python3
# coding:utf-8
from .cad import WdaCadHandler

_api = '/api/wda_cad'

urls = [
    [f'{_api}', WdaCadHandler],
    [f'{_api}/', WdaCadHandler],
]
