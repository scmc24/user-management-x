import pytest
from django.urls import reverse
from rest_framework.test import APIClient
import time

@pytest.mark.django_db
class TestPerformance:
    @pytest.mark.parametrize('num_requests', [10, 50, 100])
    def test_login_performance(self, num_requests, regular_user):
        client = APIClient()
        url = reverse('accounts:login-list')

        data = {
            'email': regular_user.email,
            'password': 'testpass123'  # Must match fixture password
        }

        for _ in range(num_requests):
            response = client.post(url, data)
            assert response.status_code == 200

    
    @pytest.mark.parametrize('num_users', [10, 50, 100])
    def test_user_list_performance(self, authenticated_admin_client, num_users):

        # Create test users
        from django.contrib.auth import get_user_model
        User = get_user_model()
        for i in range(num_users):
            User.objects.create_user(
                username=f'perfuser{i}',
                email=f'perfuser{i}@example.com',
                password=f'perfpass{i}'
            )

        url = reverse('accounts:users-list')

        start_time = time.time()
        response = authenticated_admin_client.get(url)
        end_time = time.time()

        assert response.status_code == 200
        response_time = end_time - start_time
        print(f'\nUser list with {num_users} users response time: {response_time:.4f} seconds')
        assert response_time < 1.0


