#!/usr/bin/env python3
# coding:utf-8
import os
from libs.utils import save_json, get_json


class Fixture(object):

    def __init__(self, project_id, project_path):
        self.project_id = project_id
        self.fixture_json = os.path.abspath(os.path.join(project_path, 'fixture.json'))
        self.static_fixtures_json = os.path.abspath(os.path.join(project_path, 'output', 'static_fixtures.json'))

    def get(self):
        return get_json(self.fixture_json, [])

    def save(self, data):
        save_json(self.fixture_json, data)

    def get_static_fixtures(self):
        return get_json(self.static_fixtures_json, {})
