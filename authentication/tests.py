from rest_framework import status, exceptions
from rest_framework.test import APITestCase
from authentication.models import User

class AuthenticationTests(APITestCase):
    """
    Contains tests for user registration
    """
    url = '/users/register'

    def test_required_validation(self):
        """
        Ensure validation error occurs for no password_check.
        """
        self.assertEqual(User.objects.count(), 0)
        data = {
            'name': 'Test',
            'email': 'test@gmail.com',
            'password': 'password',
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 400
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data, {
            'password_check' : [
                exceptions.ErrorDetail(string='This field is required.', code='required')
            ]
        })

    def test_password_check_validation(self):
        """
        Ensure validation error occurs for mismatch passwords.
        """
        self.assertEqual(User.objects.count(), 0)
        data = {
            'name': 'Test',
            'email': 'test@gmail.com',
            'password': 'password',
            'password_check': 'password1',
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 400
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data, {
            'non_field_errors' : [
                exceptions.ErrorDetail(
                    string='Password and Confirm Password doesn\'t match',
                    code='invalid'
                )
            ]
        })

    def test_user_registration(self):
        """
        Ensure we can register a new user.
        """
        self.assertEqual(User.objects.count(), 0)
        data = {
            'name': 'Test',
            'email': 'test@gmail.com',
            'password': 'password',
            'password_check': 'password',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        # check duplicate user validation
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        assert response.status_code == 400
        self.assertEqual(response.data, {
            'email' : [
                exceptions.ErrorDetail(
                    string='user with this Email already exists.',
                    code='unique'
                )
            ]
        })
