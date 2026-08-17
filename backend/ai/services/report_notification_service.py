from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

class ReportNotificationService:
    def schedule_report(self, hour:int, min:int, task_name:str, day:int, *args, **kwargs):
        if day and day > 7:
            raise ValueError("Invalid Day of the Week")
        cron_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=min,
            hour=hour,
            day_of_week=day,  # 1 denotes Monday
            day_of_month="*",
            month_of_year="*",
        )
        PeriodicTask.objects.create(
            crontab=cron_schedule,
            name=task_name,  # Unique name for the task
            task="backend.celery.send_report_email",  # Full path to the task
            args=json.dumps(args),
            kwargs=json.dumps(kwargs)
        )
