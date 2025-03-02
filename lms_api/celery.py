import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_api.settings")

# Create the Celery application
app = Celery("lms_api")

# Load configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")