from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser23',
            email='test@example.com',
            password='testpass123'
        )

        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser23')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(username='')
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')


    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='admin56',
            email='admin@example.com',
            password='adminpass123'
        )

        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.username, 'admin56')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='admin67',
                email='admin2@example.com',
                password='adminpass123',
                is_superuser=False
            )