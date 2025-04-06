import pytest
from django.urls import reverse
from rest_framework import status
from accounts.api_views import *


BASE_PATH = '/ACCOUNT-SERVICE'

@pytest.mark.django_db
class TestUserApi:
    def test_user_registration(self, api_client):
        url = reverse('accounts:signup-list')

        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'

        }

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data['user']
        assert response.data['user']['data']['email'] == 'new@example.com'



    def test_user_login(self, api_client):
        url = reverse('accounts:login-list')

        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data['data']


    def test_get_users_unauthorized(self, api_client):
        url = reverse('accounts:users-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK



    def test_user_logout(self, authenticated_regular_client):
        url = reverse('accounts:users-logout')
        response = authenticated_regular_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'success'


    
@pytest.mark.django_db
class TestAdminAPI:
    def test_admin_access(self, authenticated_admin_client):
        url = reverse('accounts:admins-list')
        response = authenticated_admin_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    def test_admin_access_denied_for_regular_user(self, authenticated_regular_client):
        url = reverse('accounts:admins-list')
        response = authenticated_regular_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN





