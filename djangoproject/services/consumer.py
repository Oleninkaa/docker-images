import pika
import json

# Параметри підключення до RabbitMQ
RABBITMQ_HOST = 'rabbitmq'  # Зазначте правильне ім'я хоста для RabbitMQ
QUEUE_NAME = 'order_queue'  # Назва черги

def callback(ch, method, properties, body):
    """
    Функція, яка обробляє отримані повідомлення.
    """
    print("Received message: ", body.decode())
    message = json.loads(body)

    # Виконати відповідну дію
    print("Processing message:", message)

    # Підтвердити обробку повідомлення
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    print("Connecting to RabbitMQ...")
    try:
        # Підключення до RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        print("Connected to RabbitMQ.")
    except Exception as e:
        print(f"Error connecting to RabbitMQ: {e}")
        return

    # Забезпечення існування черги
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    print(f"Waiting for messages in queue '{QUEUE_NAME}'. To exit press CTRL+C")

    # Споживання повідомлень
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    # Запуск нескінченного циклу для обробки повідомлень
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumer stopped.")
        connection.close()

if __name__ == "__main__":
    main()
