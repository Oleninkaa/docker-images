from pika import BlockingConnection, ConnectionParameters, BasicProperties
from pika.exceptions import AMQPConnectionError
import time


# Параметри підключення
connection_params = ConnectionParameters(
    host='rabbitmq',
    port=5672,
)

def consume_messages():
    """
    Споживає повідомлення з черги RabbitMQ.
    """
    try:
        with BlockingConnection(connection_params) as connection:
            channel = connection.channel()
            channel.queue_declare(queue='order_queue', durable=True)

            def callback(ch, method, properties, body):
                try:
                    print(f" [x] Received {body.decode()}")
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    print(f"Помилка при обробці повідомлення: {e}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            channel.basic_consume(
                queue='order_queue',
                on_message_callback=callback,
                auto_ack=False,
            )

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

    except AMQPConnectionError as e:
        raise ConnectionError(f"Помилка підключення до RabbitMQ: {e}")

if __name__ == '__main__':
    while True:
        try:
            consume_messages()
        except KeyboardInterrupt:
            print("Споживач зупинений вручну.")
            break
        except ConnectionError as e:
            print(f"{e}. Очікування 5 секунд перед повтором...")
            time.sleep(5)  # Затримка перед повторною спробою
        except Exception as e:
            print(f"Неочікувана помилка: {e}. Перезапуск...")