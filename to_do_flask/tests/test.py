import unittest
from typing import List
from to_do_flask.tests.base_test import BaseCase
from to_do_flask.utils import bytes_to_json


class ToDoAppTestCase(BaseCase):

    def test_add_user(self):
        """
        test user's base API (CRUD)
        """

        app = self.app.test_client()

        # add user with username
        username = 'my first user'
        add_data = app.post('/api/add_user', data={'username': username})
        add_data_json = bytes_to_json(add_data)
        assert add_data.status_code == 200
        assert 'username' in add_data_json, f'Something went wrong:\n{add_data_json}'
        assert add_data_json['username'] == username

        # check that our user exist throw getting him by id
        get_by_id_data = app.get(f"/api/get_user/{add_data_json['user_id']}")
        get_by_id_data_json = bytes_to_json(get_by_id_data)
        assert get_by_id_data.status_code == 200
        assert 'username' in get_by_id_data_json, f'Something went wrong:\n{get_by_id_data_json}'
        assert get_by_id_data_json == add_data_json

        # check that we could get him by his username
        get_by_username_data = app.get(f"/api/get_user/{add_data_json['username']}")
        get_by_username_data_json = bytes_to_json(get_by_username_data)
        assert get_by_username_data.status_code == 200
        assert 'username' in get_by_username_data_json, f'Something went wrong:\n{get_by_username_data_json}'
        assert get_by_username_data_json == add_data_json

        # check that we could get list of users (in our case with single user)
        list_data = app.get('/api/users')
        list_data_json = bytes_to_json(list_data)
        assert list_data.status_code == 200
        assert 'users' in list_data_json, f'Something went wrong:\n{list_data_json}'
        assert isinstance(list_data_json['users'], List)
        assert len(list_data_json['users']) == 1

        # try to change username for our user
        new_username = 'new username'
        update_data = app.post('/api/update_user', data={'user_id': add_data_json['user_id'], 'username': new_username})
        update_data_json = bytes_to_json(update_data)
        assert update_data.status_code == 200
        assert 'username' in update_data_json, f'Something went wrong:\n{update_data_json}'
        assert update_data_json['username'] == new_username

        # in the end we are going to delete our user
        delete_data = app.post('/api/delete_user', data={'user_id': add_data_json['user_id']})
        delete_data_json = bytes_to_json(delete_data)
        assert delete_data.status_code == 200
        assert 'status' in delete_data_json, f'Something went wrong:\n{delete_data_json}'
        assert delete_data_json['status'] == 'OK'

    def test_get_task_list(self):
        """
        test task's base API (CRUD)
        """
        app = self.app.test_client()

        # for the first step lets create a couple of users for our future task
        user1 = app.post('/api/add_user', data={'username': 'user1'})
        user1_data = bytes_to_json(user1)
        user2 = app.post('/api/add_user', data={'username': 'user2'})
        user2_data = bytes_to_json(user2)

        # then add task for two users
        add_data = app.post('/api/add_task', data={'deadline': '2021-12-25T16:00', 'usernames[]': 'user1 user2',
                                                   'task': 'my test task'})
        add_data_json = bytes_to_json(add_data)
        assert add_data.status_code == 200
        assert 'task' in add_data_json, f'Something went wrong:\n{add_data_json}'
        assert add_data_json['task'] == 'my test task'
        assert len(add_data_json['username']) == 2, f"users: {add_data_json['username']}"

        # check that we could get list of tasks (in our case with single user)
        list_data = app.get('/api/tasks')
        list_data_json = bytes_to_json(list_data)
        assert list_data.status_code == 200
        assert 'tasks' in list_data_json, f'Something went wrong:\n{list_data_json}'
        assert isinstance(list_data_json['tasks'], List)
        assert len(list_data_json['tasks']) == 1

        # mark task as completed
        complete_task = app.post('/api/complete_task', data={'task_id': add_data_json['task_id']})
        complete_task_json = bytes_to_json(complete_task)
        assert complete_task.status_code == 200
        assert 'completed' in complete_task_json, f'Something went wrong:\n{complete_task_json}'
        assert complete_task_json['completed'] == True

        # delete task only for user1
        delete_task_user = app.post('/api/delete_task_user', data={'user_id': user1_data['user_id'],
                                                                   'task_id': add_data_json['task_id']})
        assert delete_task_user.status_code == 200

        # check that our task belongs only for user2
        get_data = app.get(f'/api/get_task/{add_data_json["task_id"]}')
        get_data_json = bytes_to_json(get_data)
        assert get_data.status_code == 200
        assert 'username' in get_data_json, f'Something went wrong:\n{get_data_json}'
        assert get_data_json['task'] == add_data_json['task']
        assert len(get_data_json['username']) == 1
        assert get_data_json['username'][0] == 'user2', get_data_json

        # in the end, lets delete our task
        delete_data = app.post('/api/delete_task', data={'task_id': add_data_json['task_id']})
        delete_data_json = bytes_to_json(delete_data)
        assert delete_data.status_code == 200
        assert 'status' in delete_data_json, f'Something went wrong:\n{delete_data_json}'
        assert delete_data_json['status'] == 'OK'


if __name__ == '__main__':
    unittest.main()
