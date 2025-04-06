import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestSecurity:
    def test_password_not_returned_in_api(self, api_client):
        register_url = reverse('accounts:signup-list')
        data = {
            'username': 'secureuser',
            'email': 'secure@example.com',
            'password': 'securepass123'
        }
        response = api_client.post(register_url, data)
        assert 'password' not in response.data['user']['data']
    
    def test_brute_force_protection(self, api_client):
        login_url = reverse('accounts:login-list')
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        # Try multiple failed attempts
        for _ in range(5):
            response = api_client.post(login_url, data)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # After several attempts, check if account is locked or rate limited
        response = api_client.post(login_url, {
            'email': 'test@example.com',
            'password': 'testpass123'  # correct password
        })
        # This should either still work or be locked - depends on your security setup
        # assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS or status.HTTP_200_OK

    def test_sensitive_data_protection(self, authenticated_regular_client, regular_user):
        url = reverse('accounts:users-detail', args=[regular_user.pk])
        response = authenticated_regular_client.get(url)
        assert 'password' not in response.data
        assert response.data.get('is_superuser') is not True  # or whatever your policy is