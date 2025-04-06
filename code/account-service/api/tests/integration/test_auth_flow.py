import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAuthenticationFlow:
    def test_full_auth_flow(self, api_client):

        # Registration
        register_url = '/api/signup/'
        register_data = {
            'username': 'flowuser',
            'email': 'flow@example.com',
            'password': 'flowpass123'
        }

        register_response = api_client.post(register_url, register_data)
        assert register_response.status_code == status.HTTP_200_OK
        token = register_response.data['user']['token']

        # Login
        login_url = '/api/login/'
        login_data = {
            'email': 'flow@example.com',
            'password': 'flowpass123'
        }

        login_response = api_client.post(login_url, login_data)
        assert login_response.status_code == status.HTTP_200_OK


        # Access protected resource
        api_client.credentials(HTTP_AUTHORIZATION=f'token {token}')
        user_url = reverse('accounts:users-list')
        user_response = api_client.get(user_url)
        assert user_response.status_code == status.HTTP_200_OK


        # Logout
        logout_url = reverse('accounts:users-logout')
        logout_response = api_client.post(logout_url)
        assert logout_response.status_code == status.HTTP_200_OK

