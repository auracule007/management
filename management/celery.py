import os
from django.conf import settings
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management.settings')

app = Celery('management')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)


# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')