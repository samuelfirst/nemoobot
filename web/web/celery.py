import os

from dotenv import load_dotenv
from celery import Celery

project_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(project_folder, '.env.dev'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_routes = {'accounts.tasks.*': {'queue': 'accounts'}}

app.autodiscover_tasks()

# celery beat tasks
app.conf.beat_schedule = {
    "check-access-token-freshness": {
        "task": "accounts.tasks.check_twitch_access_token_freshness",
        "schedule": 60.0,
    },
}
