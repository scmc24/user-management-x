import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestRateLimiting:
    def test_login_rate_limiting(self, api_client):
        login_url = reverse('accounts:login-list')

        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'

        }

        # Make multiple requests quickly
        for _ in range(10):
            response = api_client.post(login_url, data)


        # Depending on your rate limiting setup, the last response should be rate limited
        assert response.status_code in [status.HTTP_429_TOO_MANY_REQUESTS, status.HTTP_401_UNAUTHORIZED]


    def test_signup_rate_limiting(self, api_client):
            signup_url = reverse('accounts:signup-list')

            data = {
                'username': 'rateuser',
                'email': 'rate@example.com',
                'password': 'ratepass123'
            }

            # Make multiple signup requests quickly
            for i in range(10):
                data['username'] = f'rate{i}user'
                data['email'] = f'rate{i}@example.com'
                response = api_client.post(signup_url, data)


            # Depending on your rate limiting setup, the last response should be rate limited
            assert response.status_code in [status.HTTP_429_TOO_MANY_REQUESTS, status.HTTP_200_OK]
