from flask import render_template, request, redirect, url_for
from to_do_flask import logic


def home():
    return render_template("home.html")


def tasks():
    return render_template("task_list.html", task_list=logic.task.list_tasks(), user_list=logic.user.list_users())


def add_task_form():
    return render_template("add_task.html", user_list=logic.user.list_users())


def add_task():
    task = request.form.get('task')
    deadline = request.form.get('deadline')
    usernames = request.form.getlist('usernames[]')
    logic.task.add(task, usernames, deadline)
    return redirect(url_for('page_views.tasks'))


def delete_task():
    task_id = int(request.form.get('task_id'))
    current_page = request.form.get('current_page')
    logic.task.delete(task_id)
    return redirect(current_page)


def complete_task():
    task_id = int(request.form.get('task_id'))
    current_page = request.form.get('current_page')
    logic.task.complete_task(task_id)
    return redirect(current_page)


def users():
    return render_template("user_list.html", user_list=logic.user.list_users())


def single_user(user_id):
    return render_template("user.html", user=logic.user.get_by_user_id(user_id))


def add_user_form():
    return render_template("add_user.html")


def add_user():
    username = request.form.get('username')
    logic.user.add(username)
    return redirect(url_for('page_views.users'))


def delete_user():
    user_id = int(request.form.get('user_id'))
    logic.user.delete(user_id)
    return redirect(url_for('page_views.users'))


def delete_task_user():
    user_id = int(request.form.get('user_id'))
    task_id = int(request.form.get('task_id'))
    logic.user.delete_task(user_id, task_id)
    return redirect(url_for('page_views.single_user', user_id=user_id))


def update_user():
    user_id = int(request.form.get('user_id'))
    new_username = request.form.get('username')
    logic.user.update(user_id, username=new_username)
    return redirect(url_for('page_views.users'))
