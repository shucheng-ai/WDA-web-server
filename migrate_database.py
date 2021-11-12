#!/usr/bin/env python3
# coding:utf-8
"""
初始化 1-400 project

6.21:
469
"""
from models.project import Project as ProjectModel

from project import Project
from project.fixture import Fixture

count = 20

for i in range(count):
    print(i)
    project = ProjectModel.find_byid(f"{i}")
    print(project)
    if not project:
        project_id = f"{i}"
        _new = {
            'id': f'{i}',
            'name': f"project-{i}",
        }
        new_session = ProjectModel(**_new)
        new = ProjectModel.add(new_session)
        Project.create(project_id)
        _project = Project(project_id)
        _fixture = Fixture(project_id=project_id, project_path=_project.path)
        _fixture.save([])
