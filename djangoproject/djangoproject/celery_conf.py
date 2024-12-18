from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# встановлюємо Django налаштування
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

app = Celery('djangoproject')

# використовуємо строку конфігурації для підключення до RabbitMQ
app.config_from_object('django.conf:settings', namespace='CELERY')


# Вказуємо використання черги 'order_queue'
app.conf.task_routes = {
    'djangoapp.tasks.send_message_to_queue': {'queue': 'order_queue'},
}

# автоматичне виявлення задач в кожному з встановлених додатків
app.autodiscover_tasks()
