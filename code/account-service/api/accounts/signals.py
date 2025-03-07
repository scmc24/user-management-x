from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from accounts.rabbitmq_publisher import publisher
from accounts.serializers import UserSerializer
from aio_pika import DeliveryMode , Message 
import asyncio
import json

@receiver(post_save, sender=User)
def create_client_auth_token(sender, instance, created, **kwargs):
    
    if created:

        user_message = {
            "type": "CREATE",
            "user": UserSerializer(instance).data
        }

        message = Message(
            json.dumps(user_message).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            type="CREATE"
        )
        
        #asyncio.run(publisher(message))
        
        

    else:

        user_message = {
            "type": "UPDATE",
            "user": UserSerializer(instance).data
        }

        message = Message(
            json.dumps(user_message).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            type="UPDATE"
        )

        #asyncio.run(publisher(message))

    


@receiver(post_delete, sender=User)
def send_delete_message(sender, instance, created, **kwargs):
    user_message = {
            "type": "DELETE",
            "user": instance.pk
        }

    message = Message(
            json.dumps(user_message).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            type="DELETE"
        )
        
    #asyncio.run(publisher(message))
        


