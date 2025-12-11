from .models import PlaceToVisit, LearningResource, Hospital, InsurancePolicy, Event, PlaceCategory, PlaceImage,UserInsurancePolicy

from .models import (
    PlaceToVisit, LearningResource, Hospital, 
    InsurancePolicy, Event, PlaceCategory, PlaceImage  , Doctor , Game, GameSession
)
from django import forms
# --- 1. IMPORT THE NEW EVENT MODEL ---
from .models import PlaceToVisit, LearningResource, Hospital, InsurancePolicy, Event,Doctor

# Django's ModelForm will automatically create a form
# based on the fields in our model. It's magic!

# class PlaceForm(forms.ModelForm):
#     class Meta:
#         model = PlaceToVisit
#         fields = '__all__' # Include all fields from the model

class PlaceForm(forms.ModelForm):
    class Meta:
        model = PlaceToVisit
        # We explicitly list the fields so we can control the form layout
        fields = [
            'name', 
            'category', 
            'address', 
            'description', 
            'main_image',
            'is_wheelchair_accessible', 
            'has_restrooms',
            'has_seating',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        
# --- REPLACE THE LearningResourceForm CLASS ---
class LearningResourceForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        # Ensure all new fields are included here
        fields = [
            'title', 
            'description', 
            'category', 
            'content_type', 
            'difficulty', # NEW
            'external_link', # NEW
            'uploaded_file' # NEW
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'external_link': forms.URLInput(attrs={'placeholder': 'e.g., https://youtube.com/video-link'}),
        }

# --- REPLACE THE HospitalForm CLASS ---
class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g., +91 98765 43210'}),
        }
class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = [
            'policy_name',
            'provider_name',
            'description',
            'policy_type',
            'coverage_summary', # <-- ADD THIS LINE
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            # --- ADD THIS NEW WIDGET ---
            'coverage_summary': forms.Textarea(attrs={'rows': 3}),
        }

# --- 2. ADD THE NEW EVENTFORM CLASS ---
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        
        # We will exclude 'created_by' because we will
        # set that field automatically in the view.
        exclude = ['created_by']
        
        # We'll add a 'widget' to make the date field
        # use the browser's nice date/time picker.
        widgets = {
            'event_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    # This is an extra step for usability.
    # We must tell the form how to handle the datetime-local input.
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.event_date:
            self.initial['event_date'] = self.instance.event_date.strftime('%Y-%m-%dT%H:%M')

class PlaceImageForm(forms.ModelForm):
    """
    A simple form for uploading a new gallery image.
    """
    class Meta:
        model = PlaceImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional caption...'}),
        }

class UserPolicyForm(forms.ModelForm):
    """
    Form for seniors to add their own personal insurance policies.
    Includes file upload for policy documents.
    """
    class Meta:
        model = UserInsurancePolicy
        fields = [
            'policy_name', 'policy_number', 'provider_name', 
            'coverage_type', 'start_date', 'expiry_date', 
            'premium_amount', 'premium_frequency', 
            'policy_document', 'coverage_summary'
        ]
        widgets = {
            'policy_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. My Health Plan'}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. POL-123456789'}),
            'provider_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. LIC, Star Health'}),
            'coverage_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'premium_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'premium_frequency': forms.Select(attrs={'class': 'form-select'}),
            'policy_document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'coverage_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'My personal notes...'}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'languages_spoken': forms.TextInput(attrs={'placeholder': 'e.g., Hindi, English, Marathi'}),
            'visiting_hours': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Mon-Fri: 10 AM - 5 PM'}),
        }

        # --- ADD THIS NEW GAMEFORM CLASS ---
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'game_url': forms.TextInput(attrs={'placeholder': '/games/memory/'}),
        }
# --- END ADD ---