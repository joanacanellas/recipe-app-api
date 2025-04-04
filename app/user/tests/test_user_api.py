"""
Tests for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """ Create and return a new user """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Test public features (no authentication) of the user API. """
    
    def setUp(self):
        self.client = APIClient()
        
    def test_create_user_success(self):
        """ Test creating a user is successful. """
        payload = {
            'email': 'test@example.com',
            'password': 'tespass123',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data) # We make sure the pwd is not sent in the response for security issues
        
    def test_user_with_email_exists_error(self):
        """ Test error is returned if user with email exists. """
        payload = {
            'email': 'test@example.com',
            'password': 'tespass123',
            'name': 'Test Name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        """ Test error is returned if password is less than 5 charts. """
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Ensure that the user is not created in database
        user_created = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_created)
    