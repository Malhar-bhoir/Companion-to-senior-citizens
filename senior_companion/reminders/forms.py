from django import forms
from .models import Medication, Reminder

class MedicationForm(forms.ModelForm):
    """
    A form for creating a new medication.
    """
    class Meta:
        model = Medication
        fields = ['name', 'dosage']
        widgets = {
            # --- FIX 1: Add 'class' attribute ---
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g., Vitamin D',
                'class': 'form-control'  # <-- ADDED
            }),
            # --- FIX 2: Add 'class' attribute ---
            'dosage': forms.TextInput(attrs={
                'placeholder': 'e.g., 1 tablet',
                'class': 'form-control'  # <-- ADDED
            }),
        }

class MedicationForm(forms.ModelForm):
    """
    A form for creating a new medication.
    """
    class Meta:
        model = Medication
        fields = ['name', 'dosage']
        widgets = {
            # --- FIX 1: Add 'class' attribute ---
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g., Vitamin D',
                'class': 'form-control'  # <-- ADDED
            }),
            # --- FIX 2: Add 'class' attribute ---
            'dosage': forms.TextInput(attrs={
                'placeholder': 'e.g., 1 tablet',
                'class': 'form-control'  # <-- ADDED
            }),
        }

class ReminderForm(forms.ModelForm):
    """
    A form for adding a new reminder time to a medication.
    """
    class Meta:
        model = Reminder
        fields = ['reminder_time']
        
        # --- FIX 3: Change widget to TextInput for better compatibility ---
        widgets = {
            'reminder_time': forms.TextInput(attrs={ # <-- CHANGED
                'type': 'text', # <-- CHANGED
                'class': 'form-control me-2', # <-- ADDED
                'placeholder': 'e.g., 8:30 AM or 14:30' # <-- ADDED
            }),
        }