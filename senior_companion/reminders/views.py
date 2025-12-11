from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medication, Reminder
from .forms import MedicationForm, ReminderForm
from django.views.decorators.http import require_POST

@login_required
def medication_list(request):
    """
    This is the main page for reminders.
    It displays all the user's medications.
    It also handles the POST request for adding a NEW medication.
    """
    # Get all medications for the currently logged-in user
    medications = Medication.objects.filter(user=request.user)
    
    # This is the form for adding a NEW medication
    medication_form = MedicationForm()

    # This is the form for adding a NEW reminder time (re-used)
    reminder_form = ReminderForm()

    # Handle the "Add New Medication" form submission
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            # Don't save yet...
            medication = form.save(commit=False)
            # ...set the user to the logged-in user
            medication.user = request.user
            medication.save()
            messages.success(request, f'Medication "{medication.name}" added successfully.')
            return redirect('medication_list')
        else:
            messages.error(request, 'There was an error adding your medication.')

    context = {
        'medications': medications,
        'medication_form': medication_form,
        'reminder_form': reminder_form,
    }
    return render(request, 'reminders/medication_list.html', context)


@require_POST # This view only accepts POST requests
@login_required
def add_reminder(request, medication_id):
    """
    Handles adding a new reminder time to an existing medication.
    """
    medication = get_object_or_404(Medication, id=medication_id, user=request.user)
    form = ReminderForm(request.POST)
    if form.is_valid():
        reminder = form.save(commit=False)
        reminder.medication = medication
        reminder.save()
        messages.success(request, f"Reminder added for {medication.name}.")
    else:
        messages.error(request, "Please enter a valid time.")
    
    return redirect('medication_list')


@require_POST
@login_required
def delete_medication(request, medication_id):
    """
    Deletes an entire medication and all its reminders.
    """
    medication = get_object_or_404(Medication, id=medication_id, user=request.user)
    med_name = medication.name
    medication.delete()
    messages.success(request, f'Medication "{med_name}" and all its reminders were deleted.')
    return redirect('medication_list')


@require_POST
@login_required
def delete_reminder(request, reminder_id):
    """
    Deletes a single reminder time.
    """
    reminder = get_object_or_404(Reminder, id=reminder_id, medication__user=request.user)
    med_name = reminder.medication.name
    reminder.delete()
    messages.success(request, f"Reminder for {med_name} was deleted.")
    return redirect('medication_list')