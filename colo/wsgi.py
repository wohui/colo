"""
WSGI config for colo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
from cron_mange.test_task import TestTask
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colo.settings')

application = get_wsgi_application()


# test_task = TestTask.instance()
# test_task.start_scheduler()