from django import forms
from datetime import date

# Import the encoders and the full choice set
from .ml_service import _encode_income_level, _encode_coverage_amount, _encode_premium_budget, _encode_risk_tolerance, _encode_smoking_status, _encode_exercise_frequency

# Helper to get choices from the encoder maps (keys only)
def get_choices(encoder_func):
    """
    Retrieves the CHOICES DICTIONARY from the encoder function's mapping.
    It runs the function with a known key to access the internal map.
    """
    # The encoder functions return the MAPPING dictionary when called with the special
    # key 'CHOICES_ONLY' (or similar, since we can't access private variables easily).
    # Since we can't edit the ml_service.py to expose the map, we use a known key.
    
    # We will modify the encoder calls slightly to force it to return the map.
    # --- WARNING: We must update ml_service.py to handle this! ---
    
    # Temporarily bypass this with hardcoded names, and we MUST fix the ML service.
    # We will assume a fixed set of keys for now for the choices (this will be stable).
    
    # --- TEMPORARY FIX to get the list of keys and stop the crash ---
    if encoder_func.__name__ == '_encode_income_level':
        choice_keys = ['under-3lakh', '3lakh-5lakh', '5lakh-8lakh', '8lakh-12lakh', '12lakh-20lakh', '20lakh-30lakh', 'over-30lakh']
    elif encoder_func.__name__ == '_encode_coverage_amount':
        choice_keys = ['10lakh-25lakh', '25lakh-50lakh', '50lakh-75lakh', '75lakh-1crore', '1crore-1.5crore', '1.5crore-2crore', 'over-2crore']
    elif encoder_func.__name__ == '_encode_premium_budget':
        choice_keys = ['under-2000', '2000-5000', '5000-8000', '8000-12000', '12000-20000', '20000-30000', 'over-30000']
    elif encoder_func.__name__ == '_encode_risk_tolerance':
        choice_keys = ['conservative', 'moderate', 'aggressive']
    elif encoder_func.__name__ == '_encode_smoking_status':
        choice_keys = ['never', 'former', 'current']
    elif encoder_func.__name__ == '_encode_exercise_frequency':
        choice_keys = ['none', 'light', 'moderate', 'intense']
    else:
        return []
    
    return [(k, k) for k in choice_keys]


# --- Form for ML Inputs (Now includes Family/Health) ---
class RecommendationInputForm(forms.Form):
    """
    Form to collect data required for the insurance recommendation model (10 features total).
    """
    
    # --- PRIMARY INPUTS (From original 7) ---
    
    dateOfBirth = forms.DateField(
        label="Your Date of Birth (YYYY-MM-DD)",
        initial=date(1965, 1, 1),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    
    annualIncome = forms.ChoiceField(
        label="Current Annual Income",
        choices=get_choices(_encode_income_level),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    coverageAmount = forms.ChoiceField(
        label="Desired Coverage Amount",
        choices=get_choices(_encode_coverage_amount),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    premiumBudget = forms.ChoiceField(
        label="Monthly Premium Budget",
        choices=get_choices(_encode_premium_budget),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    riskTolerance = forms.ChoiceField(
        label="Risk Tolerance",
        choices=get_choices(_encode_risk_tolerance),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    smokingStatus = forms.ChoiceField(
        label="Smoking Status",
        choices=get_choices(_encode_smoking_status),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    exerciseFrequency = forms.ChoiceField(
        label="Exercise Frequency",
        choices=get_choices(_encode_exercise_frequency),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    
    # --- SECONDARY INPUTS (The 3 missing features needed for the model) ---
    
    familySize = forms.IntegerField(
        label="Family Size (Including yourself)",
        min_value=1,
        max_value=10,
        initial=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    dependents = forms.ChoiceField(
        label="Do you have financial dependents?",
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    
    medicalConditions = forms.MultipleChoiceField(
        label="Select Pre-Existing Medical Conditions",
        required=False,
        choices=[
            ('diabetes', 'Diabetes'), 
            ('heart', 'Heart Disease'), 
            ('bp', 'High Blood Pressure'), 
            ('none', 'None / Healthy')
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text="Select all that apply."
    )