from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()
class SignInViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', user_type='CUSTOMER')
        self.url = '/api/v1/auth/signin/'  # Replace with your actual signin URL
    
    def test_signin_success(self):
        # Test a successful sign-in
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(self.url, data, format='json')

        # Check if the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the token is returned
        self.assertIn('token', response.data)

        # Check if the user_id is correct
        self.assertEqual(response.data['user_id'], self.user.pk)

        # Check if the user_type is correct
        self.assertEqual(response.data['user_type'], self.user.user_type)

        # Check if the username is correct
        self.assertEqual(response.data['username'], self.user.username)

        # Check if the token is created in the database
        token_exists = Token.objects.filter(user=self.user).exists()
        self.assertTrue(token_exists)

    def test_signin_invalid_credentials(self):
        # Test sign-in with invalid credentials
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = self.client.post(self.url, data, format='json')

        # Check if the status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains errors
        self.assertIn('non_field_errors', response.data)

    def test_signin_missing_fields(self):
        # Test sign-in with missing fields
        data = {'username': 'testuser'}  # Missing password
        response = self.client.post(self.url, data, format='json')

        # Check if the status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains errors
        self.assertIn('password', response.data)

    def test_signin_no_data(self):
        # Test sign-in with no data
        response = self.client.post(self.url, {}, format='json')

        # Check if the status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the response contains errors
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
