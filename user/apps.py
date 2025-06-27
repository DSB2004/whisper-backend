from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import AppRegistryNotReady
import json

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):

        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        from .tasks import CRON_JOBS  

        try:
            for job in CRON_JOBS:
                schedule_data = job["schedule"]
                schedule, _ = CrontabSchedule.objects.get_or_create(**schedule_data)
                if not PeriodicTask.objects.filter(name=job["name"]).exists():
                    PeriodicTask.objects.create(
                        crontab=schedule,
                        name=job["name"],
                        task=job["task"],
                        args=json.dumps(job["args"]),
                        kwargs=json.dumps(job["kwargs"]),
                    )
        except (OperationalError, ProgrammingError, AppRegistryNotReady):
            pass