from celery import shared_task
from .models import Reminder
import datetime
from django.utils import timezone
from django.core.mail import send_mail
from resources.models import UserInsurancePolicy # <-- Add this import
from datetime import timedelta
# @shared_task
# def check_reminders():
#     """
#     This is the background task that will run on a schedule.
#     It finds all reminders that are due and prints them.
#     """
#     #print(f"--- Running Reminder Check at {timezone.now().strftime('%Y-%m-%d %I:%M %p')} ---")
#     print(f"--- Running Reminder Check at {timezone.localtime(timezone.now()).strftime('%Y-%m-%d %I:%M %p')} ---")
#     # # Get the current time, e.g., "14:30"
#     # current_time = timezone.now().time()
    
#     # # Get today's date
#     # today = timezone.now().date()

#     # Get the current time, e.g., "14:30"
#     # --- FIX: Use localtime() to get the time in our TIME_ZONE ---
#     current_local_time = timezone.localtime(timezone.now())
#     current_time = current_local_time.time()
    
#     # Get today's date
#     today = current_local_time.date()

#     # Find reminders that are due to be sent
#     # 1. The reminder time is in the past minute
#     #    (e.g., current time is 14:30, find reminders for 14:30)
#     # 2. We have NOT sent a reminder for it today
#     reminders_due = Reminder.objects.filter(
#         reminder_time__hour=current_time.hour,
#         reminder_time__minute=current_time.minute,
#     ).exclude(
#         last_sent=today # Exclude if last_sent is today
#     )

#     if not reminders_due.exists():
#         print("No reminders due right now.")
#         return

#     for reminder in reminders_due:
#         # For now, we just print to the console.
#         # In a future step, we could send an email or push notification.
#         user_email = reminder.medication.user.email
#         med_name = reminder.medication.name
        
#         print(f"!!! REMINDER: Time for {user_email} to take {med_name} !!!")
        
#         # Mark as sent for today
#         reminder.last_sent = today
#         reminder.save()

#     print("--- Reminder Check Complete ---")

@shared_task
def check_reminders():
    """
    This background task runs every minute, finds due reminders,
    and sends an email to the user.
    """
    
    # Get the current local time (respecting our TIME_ZONE setting)
    current_local_time = timezone.localtime(timezone.now())
    current_time = current_local_time.time()
    today = current_local_time.date()

    print(f"--- Running Reminder Check at {current_local_time.strftime('%Y-%m-%d %I:%M %p')} ---")

    # Find reminders that are due
    reminders_due = Reminder.objects.filter(
        reminder_time__hour=current_time.hour,
        reminder_time__minute=current_time.minute,
    ).exclude(
        last_sent=today
    )

    if not reminders_due.exists():
        print("No reminders due right now.")
        return

    # Loop through all reminders that are due
    for reminder in reminders_due:
        # Get the user and medication details
        user = reminder.medication.user
        med_name = reminder.medication.name
        dosage = reminder.medication.dosage
        
        # --- As you requested: use username! ---
        username = user.username  # For the greeting
        email_address = user.email  # For sending

        # Build the email content
        subject = f"Friendly Reminder: Time for your medication!"
        
        message_body = f"""
Hello, {username}!
This is a friendly reminder to take your medication:

  Medication: {med_name}
  Dosage:     {dosage}

Have a wonderful day!

- The Senior Companion Team
"""

        try:
            # Send the email
            send_mail(
                subject,
                message_body,
                'reminders@senior-companion.com', # From (matches settings.py)
                [email_address],                  # To
                fail_silently=False,
            )
            
            # Print a success message in our Celery Worker terminal
            print(f"!!! SUCCESSFULLY SENT email to {email_address} for {med_name} !!!")
            
            # Mark as sent for today
            reminder.last_sent = today
            reminder.save()

        except Exception as e:
            # If the email fails, print the error
            print(f"!!! FAILED to send email to {email_address}: {e} !!!")

    print("--- Reminder Check Complete ---")
# --- END OF REPLACEMENT ---

@shared_task
def check_insurance_expiries():
    """
    Checks for insurance policies expiring in 30 days and 7 days.
    Sends an email reminder.
    """
    # Get today's date in the current timezone
    current_local_time = timezone.localtime(timezone.now())
    today = current_local_time.date()
    
    print(f"--- Running Insurance Expiry Check at {current_local_time.strftime('%Y-%m-%d %I:%M %p')} ---")

    # Define our reminder windows
    # We want to remind people 30 days before and 7 days before
    target_dates = [
        today + timedelta(days=30),
        today + timedelta(days=7)
    ]

    for target_date in target_dates:
        # Find policies expiring on this exact target date
        policies_due = UserInsurancePolicy.objects.filter(expiry_date=target_date)
        
        for policy in policies_due:
            user = policy.user
            days_left = (target_date - today).days
            
            subject = f"Action Required: Your {policy.policy_name} expires in {days_left} days"
            
            message_body = f"""
Hello, {user.username}!

This is an important reminder that your insurance policy is expiring soon.

  Policy Name:   {policy.policy_name}
  Provider:      {policy.provider_name}
  Policy Number: {policy.policy_number}
  Expiry Date:   {policy.expiry_date.strftime('%B %d, %Y')}
  
  Days Remaining: {days_left} days

Please review your policy or contact your provider to renew it.

- The Senior Companion Team
"""
            try:
                send_mail(
                    subject,
                    message_body,
                    'reminders@senior-companion.com',
                    [user.email],
                    fail_silently=False,
                )
                print(f"!!! SENT INSURANCE REMINDER to {user.email} for {policy.policy_name} !!!")
                
            except Exception as e:
                print(f"!!! FAILED to send insurance email: {e} !!!")

    print("--- Insurance Check Complete ---")
