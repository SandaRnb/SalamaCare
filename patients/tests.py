from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


class RegisterPatientWithoutUsernameTests(TestCase):
    def test_register_patient_accepts_email_only_payload(self):
        client = APIClient()

        response = client.post(
            '/api/patients/inscription/',
            {
                'email': 'patient@example.com',
                'password': 'Azerty123',
                'password2': 'Azerty123',
                'date_naissance': '2000-01-01',
                'adresse': 'Avenue Habib Bourguiba, Tunis',
                'telephone': '0601020304',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(User.objects.filter(email='patient@example.com').exists())

        user = User.objects.get(email='patient@example.com')
        self.assertEqual(user.username, 'patient')
        self.assertEqual(user.role, User.Role.PATIENT)
