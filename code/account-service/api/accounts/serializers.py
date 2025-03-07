from urllib import request
from accounts.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
import logging


# Get a logger for accounts
logger = logging.getLogger('accounts')




class UserSerializer(serializers.ModelSerializer):
   
    class Meta:

        model = User
        fields = ["id","username","email",
                  "password", "is_superuser"]
        
        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "is_superuser" : {
                "read_only": True
            }
        }
    
    def create(self, validated_data, *args, **kwargs):
      
        user = self.Meta.model.objects.create_user(**validated_data)
        
        return user


class AdminSerializer(UserSerializer):
    def create(self, validated_data, *args, **kwargs):
        user = self.Meta.model.objects.create_superuser(**validated_data)
        return user
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "password"]
    
    def create_user(self, validated_data, *args, **kwargs):
        
        user = authenticate(
             request,
             username=validated_data["email"],
             password=validated_data["password"],
        )
    

class SignUpSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = User
        fields = ["id","username","email",
                  "password", "is_superuser"]
        
        extra_kwargs = {
          
            "password": {
                "write_only": True,
            },
            "is_superuser" : {
                "read_only": True
            }
        }
    
    def create(self, validated_data, *args, **kwargs):
     
        logger.info(validated_data)
        user = User.objects.create_user(**validated_data)
       
        return user


