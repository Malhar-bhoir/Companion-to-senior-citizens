# This is the fix for Windows + eventlet
# import eventlet
# eventlet.monkey_patch()
# # --- END OF ADDED LINES ---


import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senior_companion_project.settings')

app = Celery('senior_companion_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# (Add this new code at the bottom of the file)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Sets up the periodic (scheduled) tasks for our application.
    """
    # --- Register our task ---
    # This tells Celery to run the 'reminders.tasks.check_reminders' task
    # every 60 seconds.
    sender.add_periodic_task(
        60.0,  # Run every 60 seconds
        'reminders.tasks.check_reminders',
        name='check reminders every minute'
    )