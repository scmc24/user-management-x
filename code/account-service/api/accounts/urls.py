from rest_framework import routers
from accounts.api_views import *
from django.conf.urls.static import static
from django.urls import path ,include

app_name = "accounts"

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'admins', AdminViewSet, basename='admins')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'signup', SignUpViewSet, basename='signup')

urlpatterns = router.urls
