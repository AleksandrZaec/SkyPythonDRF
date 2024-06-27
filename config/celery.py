from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

# Запуск beat scheduler вместе с worker
app.conf.beat_schedule = {
    'block_inactive_users': {
        'task': 'myapp.tasks.block_inactive_users_task',
        'schedule': crontab(hour=0, minute=0),  # Запускать каждый день в полночь
    },
}
