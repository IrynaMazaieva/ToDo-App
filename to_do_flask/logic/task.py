import datetime
from flask import current_app
from typing import List, Dict
from to_do_flask.models import Task, User


def form_JSON_data(task: Task) -> Dict:
    usernames = get_usernames_list(task)
    data = {'task_id': task.id,
            'task': task.task,
            'deadline': task.deadline,
            'username': usernames,
            'completed': task.completed}
    return data


def get_usernames_list(task: Task) -> List:
    usernames = []
    for user in task.user:
        usernames.append(user.username)
    return usernames


def list_tasks() -> Dict:
    task_list = []
    task_query = current_app.db.session.query(Task).all()
    for task in task_query:
        task_list.append(form_JSON_data(task))
    return {'tasks': task_list}


def get_by_task_id(task_id: int) -> Dict:
    task = current_app.db.session.query(Task).filter(Task.id == task_id).one()
    return form_JSON_data(task)


def complete_task(task_id: int) -> Dict:
    current_app.db.session.query(Task).filter(Task.id == task_id).update({'completed': True})
    current_app.db.session.commit()
    return get_by_task_id(task_id)


def add(task: str, usernames: str, deadline: str) -> Dict:
    deadline = datetime.datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
    users = []
    if type(usernames) == str:
        usernames = usernames.split()
    for username in usernames:
        user = current_app.db.session.query(User).filter(User.username == username).one()
        users.append(user)
    new_task = Task(task=task, user=users, deadline=deadline)
    current_app.db.session.add(new_task)
    current_app.db.session.commit()
    current_app.db.session.flush()
    return get_by_task_id(new_task.id)


def delete(task_id: int) -> Dict:
    current_app.db.session.query(Task).filter(Task.id == task_id).delete()
    current_app.db.session.commit()
    return {'status': 'OK'}
