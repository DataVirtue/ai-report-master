import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def send_report_email(
    self, to_email_id, subject, message, filename, report_query, mimetype
):
    from ai.services.email_service import EmailService
    from ai.services.report_generation_service import ReportGenerationService

    generator = ReportGenerationService()
    service = EmailService()
    try:
        file = generator.get_report_csv(report_query)
        service.send_email([to_email_id], subject, message, file, filename, mimetype)
    except Exception as e:
        print(f"Could Not send an email, Following exception occured {e}")
        raise Exception(e)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
