from bs4 import BeautifulSoup
import textwrap
import typer
from simple_term_menu import TerminalMenu

from bc3 import get_projects, get_project_by_name, get_todos

app = typer.Typer()


def project_preview(projects, index):
	if int(index) == 0:
		return None

	try:
		project = projects[int(index) - 1]
	except:
		return None

	return project.description


def todo_list_preview(todo_lists, index):
	if int(index) == 0:
		return None

	try:
		todo_list = todo_lists[int(index) - 1]
	except:
		return None

	todos = [todo for todo in todo_list.list()]
	todo_titles = ['- [ ] {}'.format(todo.title) for todo in todos]

	return '\n'.join(todo_titles)


def todo_preview(todos, index):
	if int(index) == 0:
		return None

	try:
		todo = todos[int(index) - 1]
	except:
		return None

	return todo.description


def message_preview(messages, index):
	if int(index) == 0:
		return None

	try:
		message = messages[int(index) - 1]
	except:
		return None

	content = BeautifulSoup(message.content, 'html.parser').get_text()

	return textwrap.fill(content, width=100)


def menu(
	items,
	backFunc = exit,
	preview_command = None,
	preview_size = 0.25,
	title = None
):
	items.insert(0, '<--')
	items = ['{} | {}'.format(item, str(index)) for index, item in enumerate(items)]

	terminal_menu = TerminalMenu(items, title,
		show_search_hint=True,
		preview_command=preview_command,
		preview_size=preview_size,
		clear_screen=True)
	selected_index = terminal_menu.show()

	if selected_index == 0:
		backFunc()

	if not selected_index:
		exit()

	return selected_index - 1


def projects_menu():
	projects = get_projects()
	project_names = [project.name for project in projects]

	selected_index = menu(
		project_names,
		title='BC',
		preview_command=lambda index: project_preview(projects, index))

	if selected_index is not None:
		selected_project = projects[selected_index]
		project_menu(selected_project)


def project_menu(project):
	selected_index = menu(
		['TODOS', 'Message board'],
		backFunc=projects_menu,
		title='BC > ' + project.name,
	)

	if selected_index == 0:
		todo_list_menu(project)
	elif selected_index == 1:
		message_board_menu(project)


def message_board_menu(project):
	messages = [message for message in project.message_board.list()]
	message_titles = [message.subject for message in messages]

	selected_index = menu(
		message_titles,
		title='BC > ' + project.name + ' > Message board',
		preview_command=lambda index: message_preview(messages, index),
		backFunc=lambda: project_menu(project))

	if selected_index is not None:
		selected_message = messages[selected_index]
		message_menu(selected_message, project)


def message_menu(message, project):
	selected_index = menu(
		[],
		title='BC > ' + project.name + ' > Message board > ' + message.subject,
		preview_command=lambda x: message_preview([message], 1),
		preview_size=0.95,
		backFunc=lambda: message_board_menu(project))


def todo_list_menu(project):
	todo_lists = [list for list in project.todoset.list()]
	todo_list_titles = [todo_list.title for todo_list in todo_lists]

	selected_index = menu(
		todo_list_titles,
		backFunc=lambda: project_menu(project),
		title='BC3 > ' + project.name + '> TODOS',
		preview_command=lambda index: todo_list_preview(todo_lists, index))

	if selected_index is not None:
		selected_todo_list = todo_lists[selected_index]
		todos_menu(selected_todo_list, project)


def todos_menu(todo_list, project):
	todos = [todo for todo in todo_list.list()]
	todo_titles = ['- [ ] {}'.format(todo.title) for todo in todos]

	selected_index = menu(
		todo_titles + ['+ Add a TODO'],
		backFunc=lambda: todo_list_menu(project),
		title='BC3 > ' + project.name + ' > TODOS > ' + todo_list.title,
		preview_command=lambda index: todo_preview(todos, index))

	if selected_index is not None:
		if selected_index == len(todos):
			title = input('BC3 > ' + project.name + ' > ' + todo_list.title + '\n- [ ] ')
			todo_list.create(title)
			new_todo_list = get_todos(todo_list.title, todo_list.project_id)
			todos_menu(new_todo_list, project)
		else:
			selected_todo = todos[selected_index]
			todo_menu(selected_todo, todo_list, project)


def todo_menu(todo, todo_list, project):
	selected_index = menu(
		['Mark as complete', 'Move', 'Archive'],
		backFunc=lambda: todos_menu(todo_list, project),
		title='BC3 > ' + project.name + ' > TODOS > ' + todo_list.title + ' > ' + todo.title)


	if selected_index == 0:
		todo.check()
		new_todo_list = get_todos(todo_list.title, todo.project_id)
		todos_menu(new_todo_list, project)
	elif selected_index == 1:
		move_todo_menu(todo, todo_list, project)
	elif selected_index == 2:
		todo.archive()
		new_todo_list = get_todos(todo_list.title, todo.project_id)
		todos_menu(new_todo_list, project)


def move_todo_menu(todo, todo_list, project):
	todo_lists = [list for list in project.todoset.list()]
	todo_list_titles = [todo_list.title for todo_list in todo_lists]

	selected_index = menu(
		todo_list_titles,
		backFunc=lambda: todo_menu(todo, todo_list, project),
		title='Move from ' + todo_list.title,
		preview_command=lambda index: todo_list_preview(todo_lists, index))

	todo_lists[selected_index].create(todo.title, description=todo.description)
	todo.archive()

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
		projects_menu()


if __name__ == '__main__':
	app()
