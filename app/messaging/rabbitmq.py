import pika
from app.config import settings

def get_connection():
    parameters = pika.ConnectionParameters(host='localhost')  # ou settings.RABBITMQ_HOST
    connection = pika.BlockingConnection(parameters)
    return connection
