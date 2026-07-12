from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import User


class RegisterResponsableWithoutUsernameTests(TestCase):
    def test_register_responsable_accepts_email_only_payload(self):
        client = APIClient()

        response = client.post(
            '/api/users/register/responsable/',
            {
                'email': 'responsable@example.com',
                'password': 'Azerty123',
                'password2': 'Azerty123',
                'departement': 'Cardiologie',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(User.objects.filter(email='responsable@example.com').exists())

        user = User.objects.get(email='responsable@example.com')
        self.assertEqual(user.username, 'responsable')
        self.assertEqual(user.role, User.Role.RESPONSABLE)


class EmailTokenLoginTests(TestCase):
    def test_token_login_accepts_email_only_payload(self):
        User.objects.create_user(
            username='responsable',
            email='responsable@example.com',
            password='Azerty123',
            role=User.Role.RESPONSABLE,
        )

        client = APIClient()
        response = client.post(
            '/api/token/',
            {
                'email': 'responsable@example.com',
                'password': 'Azerty123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
