import pytest
import django
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from accounts.models import User

from django.urls import reverse, resolve, clear_url_caches
from importlib import import_module
import uuid

import os


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
    
    # Minimal settings configuration if needed
    if not settings.configured:
        settings.configure(
            FORCE_SCRIPT_NAME='/ACCOUNT-SERVICE',  # Add this
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'rest_framework',
                'accounts',  # your app name
            ],
            REST_FRAMEWORK={
                'TEST_REQUEST_RENDERER_CLASSES': [
                    'rest_framework.renderers.JSONRenderer',
                ],
                'TEST_REQUEST_DEFAULT_FORMAT': 'json'
            },
            ROOT_URLCONF='api.urls'
        )
        django.setup()

    # Reload URLs to ensure they're available in tests
    clear_url_caches()
    import_module('api.urls')

@pytest.fixture(scope='session')
def django_db_setup():
    """Avoid creating/setting up the test database"""
    pass







@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    client = APIClient()
    # Set the script name header
    return client

@pytest.fixture
def regular_user(db):
    from accounts.models import User

    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

    return user


@pytest.fixture
def admin_user(db):
    from accounts.models import User

    user = User.objects.create_superuser(
        username=f'adminuser',  # Unique username
        email=f'admin@example.com',  # Unique email
        password='adminpass123'
    )
    return user



@pytest.fixture
def regular_user_token(regular_user):  # Request regular_user as parameter
    token, _ = Token.objects.get_or_create(user=regular_user)
    return token

@pytest.fixture
def admin_user_token(admin_user):  # Request admin_user as parameter
    token, _ = Token.objects.get_or_create(user=admin_user)
    return token

@pytest.fixture
def authenticated_regular_client(regular_user_token, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {regular_user_token.key}')
    return api_client

@pytest.fixture
def authenticated_admin_client(admin_user_token, api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user_token.key}')
    return api_client