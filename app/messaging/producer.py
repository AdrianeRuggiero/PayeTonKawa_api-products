import pika
from app.messaging.rabbitmq import get_connection

def publish_message(queue_name: str, message: str):
    """
    Publishes a message to a specified RabbitMQ queue.
    - queue_name: Name of the RabbitMQ queue to publish the message to.
    - message: The message to be published.
    - This function establishes a connection to RabbitMQ, declares the queue if it doesn't exist,
      and publishes the message with persistent delivery mode.
    """
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message.encode('utf-8'),
        properties=pika.BasicProperties(delivery_mode=2)  # persistant
    )

    connection.close()
