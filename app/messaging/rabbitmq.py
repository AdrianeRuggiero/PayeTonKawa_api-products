"""
RabbitMQ messaging utilities for product events.
"""

import logging
import json
import pika
from app.config import settings

from app.messaging.schemas import (
    ProductCreatedMessage, ProductUpdatedMessage, ProductDeletedMessage,
)

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_channel():
    """
    Establish and return a RabbitMQ channel with declared product queues.
    """
    connection_params = pika.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    # Déclaration des différentes queues pour les produits
    channel.queue_declare(queue='product_created', durable=True)
    channel.queue_declare(queue='product_updated', durable=True)
    channel.queue_declare(queue='product_deleted', durable=True)
    return channel

def publish_product_created(product_data: dict, channel=None):
    """
    Publish a product created event to RabbitMQ.
    """
    validated = ProductCreatedMessage(**product_data)
    if channel is None:
        channel = get_channel()
    logger.info("[RabbitMQ] Publication dans 'product_created' : %s", validated.model_dump())
    channel.basic_publish(
        exchange='',
        routing_key='product_created',
        body=validated.model_dump_json(),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    channel.close()

def publish_product_updated(product_data: dict, channel=None):
    """
    Publish a product updated event to RabbitMQ.
    """
    validated = ProductUpdatedMessage(**product_data)
    if channel is None:
        channel = get_channel()
    logger.info("[RabbitMQ] Publication dans 'product_updated' : %s", validated.model_dump())
    channel.basic_publish(
        exchange='',
        routing_key='product_updated',
        body=validated.model_dump_json(),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    channel.close()

def publish_product_deleted(product_id: str, channel=None):
    """
    Publish a product deleted event to RabbitMQ.
    """
    validated = ProductDeletedMessage(_id=product_id)
    if channel is None:
        channel = get_channel()
    logger.info("[RabbitMQ] Publication dans 'product_deleted' : %s", validated.model_dump())
    channel.basic_publish(
        exchange='',
        routing_key='product_deleted',
        body=validated.model_dump_json(),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    channel.close()

def consume_product_created(callback):
    """
    Consume product created events from RabbitMQ and process with callback.
    """
    channel = get_channel()

    def wrapper(ch, method, _, body):
        data = json.loads(body)
        logger.info("[RabbitMQ] Message reçu de 'product_created' : %s", data)
        callback(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='product_created', on_message_callback=wrapper)
    logger.info("[RabbitMQ] En attente de messages sur 'product_created'. CTRL+C pour arrêter.")
    channel.start_consuming()
