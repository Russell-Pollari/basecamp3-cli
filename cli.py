
import typer
from simple_term_menu import TerminalMenu

from bc3 import get_projects, get_project_by_name, get_todos

app = typer.Typer()


def menu(items, backFunc, title = None):
	items.insert(0, '<--')
	terminal_menu = TerminalMenu(items, title, show_search_hint=True)
	selected_index = terminal_menu.show()
	if selected_index == 0:
		backFunc()
	if not selected_index:
		exit()
	return selected_index - 1


def project_menu():
	projects = get_projects()
	project_names = [project.name for project in projects]

	selected_index = menu(project_names, exit, title='BC')

	if selected_index is not None:
		selected_project = projects[selected_index]
		todo_list_menu(selected_project)


def todo_list_menu(project):
	todo_lists = [list for list in project.todoset.list()]
	todo_list_titles = [todo_list.title for todo_list in todo_lists]

	selected_index = menu(
		todo_list_titles,
		project_menu,
		title='BC3 > ' + project.name)

	if selected_index is not None:
		selected_todo_list = todo_lists[selected_index]
		todos_menu(selected_todo_list, project)


def todos_menu(todo_list, project):
	todos = [todo for todo in todo_list.list()]
	todo_titles = ['- [ ] {}'.format(todo.title) for todo in todos]

	selected_index = menu(
		todo_titles + ['+ Add a TODO'],
		lambda: todo_list_menu(project),
		title='BC3 > ' + project.name + ' > ' + todo_list.title)

	if selected_index is not None:
		if selected_index == len(todos):
			title = input('Add a TODO:\n')
			todo_list.create(title)
			new_todo_list = get_todos(todo_list.title, todo_list.project_id)
			todos_menu(new_todo_list, project)
		else:
			selected_todo = todos[selected_index]
			todo_menu(selected_todo, todo_list, project)



def todo_menu(todo, todo_list, project):
	selected_index = menu(
		['Mark as complete', 'Exit'],
		lambda: todos_menu(todo_list, project),
		title='BC3 > ' + project.name + ' > ' + todo_list.title + ' > ' + todo.title)


	if selected_index == 0:
		todo.check()
		new_todo_list = get_todos(todo_list.title, todo.project_id)
		todos_menu(new_todo_list, project)


@app.command()
def main(project_name: str = typer.Option(None, '--project', '-p', help="Jump to a project by name")):
	if project_name:
		project = get_project_by_name(project_name)
		if not project:
			print('No project named', project_name)
			return
		todo_list_menu(project)
	else:
		project_menu()


if __name__ == '__main__':
	app()
