#!/usr/bin/env python3
# coding:utf-8
from .ipua import IpTableHandler, IpEventHandler

_api = '/api/util'

urls = [
    [f'{_api}/ip', IpTableHandler],
    [f'{_api}/ip/event', IpEventHandler],
]
