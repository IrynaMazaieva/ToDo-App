from flask import current_app
from typing import List, Dict
from to_do_flask.models import User


def get_user_task_list(user: User) -> List:
    task_list = []
    for task in user.task:
        usernames = [user.username for user in task.user]
        task_list.append({'task_id': task.id,
                          'task': task.task,
                          'username': usernames,
                          'deadline': task.deadline,
                          'completed': task.completed})
    return task_list


def list_users() -> Dict:
    users_list = []
    users_query = current_app.db.session.query(User).all()
    for user in users_query:
        task_list = get_user_task_list(user)
        users_list.append({'user_id': user.id,
                           'username': user.username,
                           'tasks': task_list})
    return {'users': users_list}


def get_by_user_id(user_id: int) -> Dict:
    user = current_app.db.session.query(User).filter(User.id == user_id).one()
    task_list = get_user_task_list(user)
    return {'user_id': user.id,
            'username': user.username,
            'tasks': task_list}


def get_by_username(username: str) -> Dict:
    user = current_app.db.session.query(User).filter(User.username == username).one()
    task_list = get_user_task_list(user)
    return {'user_id': user.id,
            'username': user.username,
            'tasks': task_list}


def add(username: str) -> Dict:
    new_user = User(username=username)
    current_app.db.session.add(new_user)
    current_app.db.session.commit()
    return get_by_username(username)


def update(user_id: int, username: str) -> Dict:
    current_app.db.session.query(User).filter(User.id == user_id).update({'username': username})
    current_app.db.session.commit()
    return get_by_username(username)


def delete(user_id: int) -> Dict:
    current_app.db.session.query(User).filter(User.id == user_id).delete()
    current_app.db.session.commit()
    return {'status': 'OK'}


def delete_task(user_id: int, task_id: int) -> Dict:
    user = current_app.db.session.query(User).filter(User.id == user_id).one()
    new_tasks = []
    for task in user.task:
        if task.id != task_id:
            new_tasks.append(task)
    user.task = new_tasks
    current_app.db.session.commit()
    return get_by_user_id(user_id)
