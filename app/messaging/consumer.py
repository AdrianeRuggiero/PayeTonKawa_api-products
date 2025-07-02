from app.messaging.rabbitmq import get_connection

def consume_messages(queue_name: str, callback):
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    def on_message(ch, method, properties, body):
        callback(body.decode('utf-8'))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=on_message)

    print(f"[*] Waiting for messages in {queue_name}. To exit press CTRL+C")
    channel.start_consuming()
