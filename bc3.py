from basecampy3 import Basecamp3

bc3 = Basecamp3()


def get_projects():
	return [project for project in bc3.projects.list()]


def get_project_by_name(project_name):
	for project in bc3.projects.list():
		if project.name == project_name:
			return project

	return None


def get_todos(title, project_id):
	project = bc3.projects.get(project_id)
	for list in project.todoset.list():
		if list.title == title:
			return list
