from rest_framework import status, exceptions
from rest_framework.test import APITestCase
from authentication.models import User
from todo.models import Task

register_url = '/users/register'
task_creation_url = '/tasks'

class TaskCreationTests(APITestCase):
    """
    Contains tests for task creation
    """
    def create_user_1(self):
        """
        Common function for creating user
        """
        self.assertEqual(User.objects.count(), 0)
        register_user = {
            'name': 'Test',
            'email': 'test@gmail.com',
            'password': 'password',
            'password_check': 'password',
        }
        response = self.client.post(register_url, register_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        return response.data

    def create_user_2(self):
        """
        Common function for creating user
        """
        register_user = {
            'name': 'Test',
            'email': 'test1@gmail.com',
            'password': 'password',
            'password_check': 'password',
        }
        response = self.client.post(register_url, register_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def create_task(self):
        """
        Common function for creating task
        """
        access_token = self.create_user_1()
        headers = {
           'Authorization': 'Bearer ' + access_token['token']['access']
        }
        task_data = {
            'title': 'Clean Room',
            'description': 'Need to clean my room and change bed sheets',
        }
        self.assertEqual(Task.objects.count(), 0)
        # check task creation validation
        response = self.client.post(task_creation_url, task_data, format='json', headers = headers)
        self.assertEqual(Task.objects.count(), 1)
        assert response.status_code == 201
        self.assertEqual(response.data, {
            'data' : {
                'id': 1,
                'title': 'Clean Room',
                'description': 'Need to clean my room and change bed sheets',
                'status' : Task.TaskStatus.PENDING,
                'user': 1
            },
            'msg' : 'Task created'
        })


    def test_authentication_credentials(self):
        """
        Ensure we get an error for required field.
        """
        task_data = {
            'title': 'Clean Room',
        }
        # check task creation validation
        response = self.client.post(task_creation_url, task_data, format='json')
        assert response.status_code == 401
        self.assertEqual(response.data, {
            'detail' : exceptions.ErrorDetail(
                string='Authentication credentials were not provided.',
                code='not_authenticated'
            )
        })

    def test_required_field_validation(self):
        """
        Ensure we get an error for required field.
        """
        access_token = self.create_user_1()
        headers = {
           'Authorization': 'Bearer ' + access_token['token']['access']
        }
        task_data = {
            'title': 'Clean Room',
        }
        # check task creation validation
        response = self.client.post(task_creation_url, task_data, format='json', headers = headers)
        assert response.status_code == 400
        self.assertEqual(response.data, {
            'description' : [
                exceptions.ErrorDetail(
                    string='This field is required.',
                    code='required'
                )
            ]
        })

    def test_task_created(self):
        """
        Ensure we can create a new task.
        """
        self.create_task()

    def test_non_complete_duplicate_task_validation(self):
        """
        Ensure we cannot create a non-complete new task with an older task title for same user.
        """
        access_token = self.create_user_1()
        headers = {
           'Authorization': 'Bearer ' + access_token['token']['access']
        }
        task_data = {
            'title': 'Clean Room',
            'description': 'Need to clean my room and change bed sheets',
        }
        self.assertEqual(Task.objects.count(), 0)
        # check task creation validation
        response = self.client.post(task_creation_url, task_data, format='json', headers = headers)
        self.assertEqual(Task.objects.count(), 1)
        assert response.status_code == 201
        self.assertEqual(response.data, {
            'data' : {
                'id': 1,
                'title': 'Clean Room',
                'description': 'Need to clean my room and change bed sheets',
                'status' : Task.TaskStatus.PENDING,
                'user': 1
            },
            'msg' : 'Task created'
        })
        response = self.client.post(task_creation_url, task_data, format='json', headers = headers)
        assert response.status_code == 400
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(response.data, {
            'errors': {
                'non_field_errors': [
                    'There is already a non complete task'
                ]
            }
        })

    def test_non_complete_duplicate_task_validation_for_different_users(self):
        """
        Ensure we can create a same title tasks for 2 different users.
        """
        access_token_1 = self.create_user_1()
        access_token_2 = self.create_user_2()
        headers1 = {
           'Authorization': 'Bearer ' + access_token_1['token']['access']
        }
        headers2 = {
           'Authorization': 'Bearer ' + access_token_2['token']['access']
        }
        task_data = {
            'title': 'Clean Room',
            'description': 'Need to clean my room and change bed sheets',
        }
        self.assertEqual(Task.objects.count(), 0)
        # check task creation validation
        self.client.post(task_creation_url, task_data, format='json', headers = headers1)
        self.client.post(task_creation_url, task_data, format='json', headers = headers2)

        self.assertEqual(Task.objects.count(), 2)