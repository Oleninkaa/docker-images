from celery import shared_task
from pika import ConnectionParameters, BlockingConnection

# Параметри підключення
connection_params = ConnectionParameters(
    host='rabbitmq',
    port=5672,
)

@shared_task
def send_message_to_queue(message):
    """
    Відправляє повідомлення до RabbitMQ.
    """
    try:
        # Використання контекстного менеджера для безпечного закриття з'єднання та каналу
        with BlockingConnection(connection_params) as conn:
            with conn.channel() as ch:
                # Створення черги
                ch.queue_declare(queue='order_queue', durable=True)
                
                # Відправка повідомлення
                ch.basic_publish(
                    exchange='',
                    routing_key='order_queue',
                    body=message,
                )
                print(f" [x] Sent {message} to order_queue")
    except Exception as e:
        print(f"Помилка при відправці повідомлення: {e}")