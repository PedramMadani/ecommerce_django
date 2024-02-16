from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookamin_store.settings')


app = Celery('Bookamin_store')

app.conf.update(
    result_backend='django-db'  # Use Django database as result backend
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
