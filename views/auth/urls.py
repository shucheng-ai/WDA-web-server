#!/usr/bin/env python3
# coding:utf-8
from .auth import AuthHandler, AuthProjectHandler, CheckPorjectHandler

_api = '/api/auth'

urls = [
    [f'{_api}/', AuthHandler],
    [f'{_api}/project', AuthProjectHandler],
    [f'{_api}/project/check', CheckPorjectHandler],
]
