#!/usr/bin/env python3
# coding:utf-8
from views.storage.storage import StorageHandler, StorageImgHandler

_api = '/api/storage'

urls = [
    [f'{_api}', StorageHandler],
    [f'{_api}/', StorageHandler],

    [f'{_api}/img', StorageImgHandler],
]
