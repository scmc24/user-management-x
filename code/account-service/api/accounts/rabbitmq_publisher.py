
from aio_pika import ExchangeType, connect_robust # type: ignore

from django.conf import settings
import logging

logger = logging.getLogger('accounts')


async def publisher(message) -> None: 

    # Perform connection
    username = settings.RABBITMQ.get("username")
    password = settings.RABBITMQ.get("password")
    host = settings.RABBITMQ.get("host")

    connection = await connect_robust(f"amqp://{username}:{password}@{host}/")

    async with connection:
        channel = await connection.channel()

        account_exchange = await channel.declare_exchange(
            "accountExchange", ExchangeType.FANOUT,durable=True
        )
        
        account_notification_queue = await channel.declare_queue(name="accountNotificationQueue",durable=True)
        account_subscription_queue = await channel.declare_queue(name="accountSubscriptionQueue",durable=True)
        
        await account_notification_queue.bind(account_exchange)
        await account_subscription_queue.bind(account_exchange)
        
        await account_exchange.publish(message, routing_key="account_crud")
        logger.info(f"[x] sent {message}")

        

    
