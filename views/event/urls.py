#!/usr/bin/env python3
# coding:utf-8
from .cad import CadEventHandler, GreenFieldHandler
from .calculate import CalculateStockAreaEventHandler
from .project import ProjectEventHandler, ProjectPlanEventHandler
from .region import RegionHandler
from .connection import ConnectionItemHandler

_api = '/api/event'

urls = [
    [f'{_api}/project', ProjectEventHandler],

    [f'{_api}/project/plan', ProjectPlanEventHandler],

    [f'{_api}/calculate/stock_area', CalculateStockAreaEventHandler],

    [f'{_api}/cad', CadEventHandler],
    [f'{_api}/greenfield', GreenFieldHandler],

    [f'{_api}/region', RegionHandler],
    [f'{_api}/connection', ConnectionItemHandler],
]
