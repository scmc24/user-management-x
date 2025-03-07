from rest_framework import status, viewsets
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from accounts.models import User

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import *
from rest_framework import filters


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    


class UserViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "username",
        "email"
        
    ]
    ordering_fields = [
        "username",
        "email"
      
    ]

    @action(detail=False,url_path='logout')
    def logout_user(self, request):
        logout(request)
        response = {
            "status": status.HTTP_200_OK,
            "message": "success",
        }
        return Response(response, status=status.HTTP_200_OK)
    

class AdminViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.filter(is_superuser=True)
    serializer_class = AdminSerializer
    permission_classes = [IsSuperUser,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "username",
        "email"
        
    ]
    ordering_fields = [
        "username",
        "email"
      
    ]
class LoginViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = []
    
    def create(self, request):
        serializers = self.serializer_class(data=request.data)
        
        if serializers.is_valid():
            email = serializers.validated_data["email"]
            password = serializers.validated_data["password"]
            
            
            # Authenticate the user
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                   pass
            except User.DoesNotExist:
                user = None
            #user = authenticate(request=None, username="manuelsokoudjou@gmail.com", password=password)
            if user is not None:
                token,token_created = Token.objects.get_or_create(user=user)
                login(request=request, user=user)
                
                response = {
                    "status": status.HTTP_200_OK,
                    "message": "Successfully authenticated",
                    "data": {
                        "token": token.key,
                        "admin": user.is_superuser,
                        "user": UserSerializer(user).data
                        
                    },
                }
                
            
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Accès refusé"
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Erreur",
            "data": serializers.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        return Response({}, status=status.HTTP_200_OK)


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    
    def create(self, request):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get_or_create(user=user)
            response = {
                    "status": status.HTTP_200_OK,
                    "message": "Account in review process.",
                    "user": {
                        "token": token[0].key,
                        "data": self.serializer_class(user).data
                    } 

                }
            logger.info(serializer.data)
            
            return Response(response, status=status.HTTP_200_OK)
        
        response = {
            "status" : status.HTTP_400_BAD_REQUEST,
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        return Response({}, status=status.HTTP_204_NO_CONTENT)


