from django.test import TestCase
from accounts.serializers import UserSerializer, AdminSerializer, LoginSerializer, SignUpSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializerTests(TestCase):
    def test_user_serializer_create(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertFalse(user.is_superuser)


    def test_admin_serializer_create(self):
        data = {
            'username': 'admin237',
            'email': 'admin@example.com',
            'password': 'adminpass123'
        }    

        serializer = AdminSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.is_superuser)


    

class LoginSerializerTests(TestCase):
    def test_login_serializer(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user= serializer.save()
        self.assertEqual(serializer.validated_data['email'], 'test@example.com')
        self.assertEqual(serializer.validated_data['password'], 'testpass123')





class SignUpSerializerTests(TestCase):
        def test_signup_serializer(self):
            data = {
                  'username': 'newuser',
                  'email': 'new@example.com',
                  'password': 'newpass123'
            }

        
            serializer = SignUpSerializer(data=data)
            self.assertTrue(serializer.is_valid())
            user = serializer.save()
            self.assertEqual(user.email, 'new@example.com')
            self.assertEqual(user.username, 'newuser')
                        

            self.assertEqual(user.email, 'new@example.com')
            self.assertEqual(user.username, 'newuser')
