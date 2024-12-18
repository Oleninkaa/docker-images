from celery import shared_task
import pika

@shared_task
def send_message_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Створення черги
    channel.queue_declare(queue='order_queue', durable=True)

    # Відправка повідомлення в чергу
    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Встановлює повідомлення як стійке
        )
    )
    connection.close()
