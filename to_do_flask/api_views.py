from flask import request
from to_do_flask import logic


def get_users_list():
    return logic.user.list_users()


def get_user_by_id(user_id):
    return logic.user.get_by_user_id(user_id)


def get_user_by_username(username):
    return logic.user.get_by_username(username)


def add_user():
    username = request.form.get('username')
    return logic.user.add(username)


def update_user():
    user_id = int(request.form.get('user_id'))
    username = request.form.get('username')
    return logic.user.update(user_id, username)


def delete_user():
    user_id = int(request.form.get('user_id'))
    return logic.user.delete(user_id)


def get_tasks_list():
    return logic.task.list_tasks()


def get_task_by_id(task_id):
    return logic.task.get_by_task_id(task_id)


def complete_task():
    task_id = int(request.form.get('task_id'))
    return logic.task.complete_task(task_id)


def add_task():
    task = request.form.get('task')
    deadline = request.form.get('deadline')
    usernames = request.form.get('usernames[]')
    return logic.task.add(task, usernames, deadline)


def delete_task():
    task_id = int(request.form.get('task_id'))
    return logic.task.delete(task_id)


def delete_task_user():
    user_id = int(request.form.get('user_id'))
    task_id = int(request.form.get('task_id'))
    return logic.user.delete_task(user_id, task_id)
