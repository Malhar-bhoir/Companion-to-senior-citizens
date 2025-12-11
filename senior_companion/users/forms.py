from django import forms
from django.contrib.auth.forms import UserCreationForm
# --- 1. IMPORT OUR MODELS ---
from .models import CustomUser, Profile, Hobby

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

# --- 2. ADD THIS NEW FORM ---
# This form lets a user edit their *Profile*
class ProfileUpdateForm(forms.ModelForm):
    # We will render the 'hobbies' field as checkboxes
    # This is much more user-friendly than a standard multi-select.
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False # It's okay if they select no hobbies
    )
    
    class Meta:
        model = Profile
        # These are the fields the user is allowed to edit
        fields = ('hobbies', 'emergency_contact_name', 'emergency_contact_phone','home_address_city','home_address_state',)
        
        # Add friendly labels
        labels = {
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_phone': 'Emergency Contact Phone',
            'home_address_city': 'Your Home City', # <-- New Label
            'home_address_state': 'Your Home State/Region', # <-- New Label
        
        }