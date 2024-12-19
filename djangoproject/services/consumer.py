from pika import BlockingConnection, ConnectionParameters, BasicProperties


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

            # Оголошення черги (якщо вона ще не існує)
            channel.queue_declare(queue='order_queue', durable=True)

            def callback(ch, method, properties, body):
              try:
                  # Обробка отриманого повідомлення
                  print(f" [x] Received {body.decode()}")


                  # Виконання необхідних дій з повідомленням

                  # Підтвердження обробки повідомлення
                  ch.basic_ack(delivery_tag=method.delivery_tag)

              except Exception as e:
                  print(f"Помилка при обробці повідомлення: {e}")
                  # Відхилення повідомлення (можна використовувати requeue=True для повторної спроби)
                  ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


            # Споживання повідомлень з черги
            channel.basic_consume(
                queue='order_queue',
                on_message_callback=callback,
                auto_ack = False
            )

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

    except Exception as e:
        print(f"Помилка при підключенні до RabbitMQ: {e}")

if __name__ == '__main__':
    consume_messages()