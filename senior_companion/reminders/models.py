from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Medication(models.Model):
    """
    A specific medication a user needs to take.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="medications"
    )
    name = models.CharField(max_length=255, help_text="e.g., Vitamin D, Aspirin, etc.")
    dosage = models.CharField(max_length=100, blank=True, help_text="e.g., 1 tablet, 50mg, etc.")
    
    def __str__(self):
        return self.name

class Reminder(models.Model):
    """
    A specific reminder time for a medication.
    A single medication can have multiple reminders (e.g., 8am and 8pm).
    """
    medication = models.ForeignKey(
        Medication, 
        on_delete=models.CASCADE,
        related_name="reminders"
    )
    # We only store the time, as this is a daily reminder
    reminder_time = models.TimeField()
    last_sent = models.DateField(null=True, blank=True, help_text="The date this reminder was last sent.")

    def __str__(self):
        return f"Take {self.medication.name} at {self.reminder_time.strftime('%I:%M %p')}"