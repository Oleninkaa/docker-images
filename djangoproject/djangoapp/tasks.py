import pika
from celery import shared_task

@shared_task
def send_message_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Declare queue if it does not exist
    channel.queue_declare(queue='task_queue', durable=True)

    # Publish message to queue
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )

    connection.close()

@shared_task
def consume_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Declare queue if it does not exist
    channel.queue_declare(queue='task_queue', durable=True)

    def callback(ch, method, properties, body):
        print(f"Received {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Consume messages from the queue
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print('Waiting for messages...')
    channel.start_consuming()
