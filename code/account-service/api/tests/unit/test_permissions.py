from django.test import TestCase, RequestFactory
from accounts.api_views import IsSuperUser
from django.contrib.auth import get_user_model

User = get_user_model()

class PermissionTests(TestCase):
    def setUp(self):
        
        self.factory = RequestFactory()
        self.regular_user = User.objects.create_user(
            username='testuser234',
            email='test24@example.com',
            password='testpass1235'
        )

        self.admin_user = User.objects.create_superuser(
            username='admin234',
            email='admin24@example.com',
            password='adminpass1236'
        )


    def test_is_superuser_permission(self):
        permission = IsSuperUser()

        # Create a mock request with regular user
        request = self.factory.get('/')
        request.user = self.regular_user
        self.assertFalse(permission.has_permission(request, None))


        # Create a mock request with admin user
        request.user = self.admin_user
        self.assertTrue(permission.has_permission(request, None))
