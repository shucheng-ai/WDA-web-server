#!/usr/bin/env python3
# coding:utf-8
from .project import ProjectHandler, ProjectCadHandler, ProjectListHandler, ProjectSorageInputHandler, \
    ProjectInfoHandler, ProjectRoomHandler, ProjectMovingPathHandler, ProjectFixturesHandler
from .history import ProjectHistoryHandler
from .file import UploadHandler, FileHandler
from .info import SomeInfoHandler
from .download import DownloadCadHandler, Download3DHandler, DownloadPngHandler, DownloadCADDwgHandler

from .newproject import RoomDataHandler

_api = '/api/project'

urls = [
    [f'{_api}', ProjectHandler],
    [f'{_api}/', ProjectHandler],
    [f'{_api}/project', ProjectHandler],

    [f'{_api}/list', ProjectListHandler],

    [f'{_api}/cad', ProjectCadHandler],

    [f'{_api}/storage_input', ProjectSorageInputHandler],
    [f'{_api}/room', ProjectRoomHandler],

    [f'{_api}/moving_path', ProjectMovingPathHandler],
    [f'{_api}/connection_item', ProjectMovingPathHandler],
    [f'{_api}/fixtures', ProjectFixturesHandler],

    [f'{_api}/history', ProjectHistoryHandler],

    [f'{_api}/info', ProjectInfoHandler],

    [f'{_api}/some/info', SomeInfoHandler],

    [f'{_api}/upload', UploadHandler],
    [f'{_api}/file', FileHandler],

    [f'{_api}/downloadCad', DownloadCadHandler],
    [f'{_api}/download3D', Download3DHandler],
    [f'{_api}/downloadPng', DownloadPngHandler],
    [f'{_api}/downloadDwg', DownloadCADDwgHandler],

    [f'{_api}/room_data', RoomDataHandler]
]
