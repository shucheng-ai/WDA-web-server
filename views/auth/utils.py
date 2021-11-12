#!/usr/bin/env python3
# coding:utf-8
from project import Project
from project.fixture import Fixture
from models.project import Project as ProjectModel


def create_project(project_id, uid):
    project_name = f"project-{project_id}"
    _new = {
        'id': project_id,
        'name': project_name,
        'uid': uid
    }
    new_session = ProjectModel(**_new)
    ProjectModel.add(new_session)
    Project.create(project_id)
    _project = Project(project_id)
    _fixture = Fixture(project_id=project_id, project_path=_project.path)
    _fixture.save([])
    return True
