from flask import Flask
from sqlalchemy.exc import SQLAlchemyError

from to_do_flask import api_views, page_views
from to_do_flask import utils
from to_do_flask.db import db
from to_do_flask.models import create_tables


def configure_views(app: Flask):
    app.add_url_rule('/api/users', view_func=api_views.get_users_list)
    app.add_url_rule('/api/get_user/<int:user_id>', view_func=api_views.get_user_by_id)
    app.add_url_rule('/api/get_user/<string:username>', view_func=api_views.get_user_by_username)
    app.add_url_rule('/api/add_user', methods=['POST'], view_func=api_views.add_user)
    app.add_url_rule('/api/update_user', methods=['POST'], view_func=api_views.update_user)
    app.add_url_rule('/api/delete_user', methods=['POST'], view_func=api_views.delete_user)
    app.add_url_rule('/api/tasks', view_func=api_views.get_tasks_list)
    app.add_url_rule('/api/get_task/<int:task_id>', view_func=api_views.get_task_by_id)
    app.add_url_rule('/api/complete_task', methods=['POST'], view_func=api_views.complete_task)
    app.add_url_rule('/api/add_task', methods=['POST'], view_func=api_views.add_task)
    app.add_url_rule('/api/delete_task', methods=['POST'], view_func=api_views.delete_task)
    app.add_url_rule('/api/delete_task_user', methods=['POST'], view_func=api_views.delete_task_user)

    app.add_url_rule('/', view_func=page_views.home)
    app.add_url_rule('/tasks', endpoint='page_views.tasks', view_func=page_views.tasks)
    app.add_url_rule('/add_task_form', endpoint='page_views.add_task_form', view_func=page_views.add_task_form)
    app.add_url_rule('/add_task', endpoint='page_views.add_task', methods=['POST'], view_func=page_views.add_task)
    app.add_url_rule(
        '/delete_task', methods=['POST'], endpoint='page_views.delete_task', view_func=page_views.delete_task
    )
    app.add_url_rule(
        '/complete_task', methods=['POST'], endpoint='page_views.complete_task', view_func=page_views.complete_task
    )
    app.add_url_rule('/user_list', endpoint='page_views.users', view_func=page_views.users)
    app.add_url_rule('/add_user_form', endpoint='page_views.add_user_form', view_func=page_views.add_user_form)
    app.add_url_rule('/add_user', methods=['POST'], endpoint='page_views.add_user', view_func=page_views.add_user)
    app.add_url_rule('/single_user/<int:user_id>', endpoint='page_views.single_user', view_func=page_views.single_user)
    app.add_url_rule(
        '/delete_user', methods=['POST'], endpoint='page_views.delete_user', view_func=page_views.delete_user
    )
    app.add_url_rule(
        '/delete_task_user', methods=['POST'], endpoint='page_views.delete_task_user',
        view_func=page_views.delete_task_user
    )
    app.add_url_rule(
        '/update_user', methods=['POST'], endpoint='page_views.update_user', view_func=page_views.update_user
    )


def configure_error_handlers(app: Flask):
    app.register_error_handler(SQLAlchemyError, utils.handle_db_errors)
    app.register_error_handler(Exception, utils.handle_errors)


def configure_db(app: Flask, db_uri: str):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.init_app(app)
    app.db = db
    create_tables(app)


def create_app(db_uri: str) -> Flask:
    app = Flask(__name__)
    configure_db(app, db_uri)
    configure_views(app)
    configure_error_handlers(app)
    return app


if __name__ == "__main__":
    create_app('sqlite:///./todo_app.bd').run(debug=True)
