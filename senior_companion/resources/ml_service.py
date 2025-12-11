import joblib
import pandas as pd
import os
from datetime import date, datetime
from django.conf import settings
import numpy as np # Import fix from last step

# --- Configuration ---
MODEL_DIR = os.path.join(settings.BASE_DIR, 'ml_models')
MODEL_PATH = os.path.join(MODEL_DIR, 'rf_pipeline.joblib')

# Define the exact 10 features the model expects in the correct order
EXPECTED_FEATURES = [
    'age', 'income_score', 'coverage_score', 'premium_score', 
    'risk_score', 'smoking_score', 'exercise_score',
    # Derived features used in the original service file's synthetic logic
    'family_score',
    'health_score',
    'dependents_score',
]

# --- MAPPING FUNCTIONS (From the original ml_service.py) ---

def _calculate_age(dob_str):
    try:
        birth_date = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return 65

def _encode_income_level(income_level: str):
    income_mapping = {
        'under-3lakh': 0.2, '3lakh-5lakh': 0.4, '5lakh-8lakh': 0.6,
        '8lakh-12lakh': 0.7, '12lakh-20lakh': 0.8, '20lakh-30lakh': 0.9,
        'over-30lakh': 1.0
    }
    return income_mapping.get(income_level, 0.5)

def _encode_coverage_amount(coverage_amount: str):
    coverage_mapping = {
        '10lakh-25lakh': 0.3, '25lakh-50lakh': 0.5, '50lakh-75lakh': 0.7,
        '75lakh-1crore': 0.8, '1crore-1.5crore': 0.9, '1.5crore-2crore': 0.95,
        'over-2crore': 1.0
    }
    return coverage_mapping.get(coverage_amount, 0.5)

def _encode_premium_budget(premium_budget: str):
    premium_mapping = {
        'under-2000': 0.2, '2000-5000': 0.4, '5000-8000': 0.6,
        '8000-12000': 0.7, '12000-20000': 0.8, '20000-30000': 0.9,
        'over-30000': 1.0
    }
    return premium_mapping.get(premium_budget, 0.5)

def _encode_risk_tolerance(risk_tolerance: str):
    risk_mapping = {'conservative': 0.3, 'moderate': 0.6, 'aggressive': 0.9}
    return risk_mapping.get(risk_tolerance, 0.5)

def _encode_smoking_status(smoking_status: str):
    smoking_mapping = {'never': 1.0, 'former': 0.7, 'current': 0.3}
    return smoking_mapping.get(smoking_status, 0.5)

def _encode_exercise_frequency(exercise_frequency: str):
    exercise_mapping = {'none': 0.2, 'light': 0.5, 'moderate': 0.8, 'intense': 1.0}
    return exercise_mapping.get(exercise_frequency, 0.5)

# --- NEW: Policy Ranking Function ---

def get_insurance_recommendation(user_input):
    """
    Loads the RF model, makes a prediction score (0.1-1.0), and ranks policies.
    """
    # 1. Load Model
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return "ERROR: Model file not found. AI suggestion is unavailable."
    except Exception as e:
        return f"ERROR: Failed to load model. {e}"

    # 2. Prepare 10 Features (Complex step)
    
    # Primary Inputs
    age = _calculate_age(user_input.get('dateOfBirth'))
    income_score = _encode_income_level(user_input.get('annualIncome'))
    coverage_score = _encode_coverage_amount(user_input.get('coverageAmount'))
    premium_score = _encode_premium_budget(user_input.get('premiumBudget'))
    risk_score = _encode_risk_tolerance(user_input.get('riskTolerance'))
    smoking_score = _encode_smoking_status(user_input.get('smokingStatus'))
    exercise_score = _encode_exercise_frequency(user_input.get('exerciseFrequency'))

    # Derived/Synthetic Inputs
    family_size = int(user_input.get('familySize', '2'))
    family_score = min(1.0, family_size / 4.0)
    
    medical_conditions_count = len(user_input.get('medicalConditions', []))
    health_score = max(0.1, 1.0 - (medical_conditions_count * 0.2))
    
    dependents = user_input.get('dependents', 'no')
    dependents_score = 0.8 if dependents == 'yes' else 0.5

    # Create the final input feature vector
    data = {
        'age': age,
        'income_score': income_score,
        'coverage_score': coverage_score,
        'premium_score': premium_score,
        'risk_score': risk_score,
        'smoking_score': smoking_score,
        'exercise_score': exercise_score,
        'family_score': family_score,
        'health_score': health_score,
        'dependents_score': dependents_score,
    }

    # 3. Predict the raw score
    try:
        df = pd.DataFrame([data], columns=EXPECTED_FEATURES)
        raw_score = model.predict(df)[0]
        # Normalize the score between 0.1 and 1.0
        ml_score = max(0.1, min(1.0, raw_score)) 
    except Exception as e:
        return f"Prediction execution failed: {e}. Check features."

    # 4. Generate policy recommendations with ML scoring - Indian Insurance Companies
    policies = [
        {
            "id": 1,
            "name": "Term Life Insurance",
            "company": "LIC (Life Insurance Corporation)",
            "premium": 2500,  # Monthly premium in ₹
            "coverage": 5000000,  # Coverage in ₹ (50 lakhs)
            "term": "20 years",
            "features": ["Death benefit", "Accelerated death benefit", "Convertible"],
            "rating": 4.8,
            "description": "Affordable term life insurance from India's most trusted insurer with comprehensive coverage.",
            "score": ml_score * 0.9  # Adjusted score
        },
        {
            "id": 2,
            "name": "Whole Life Insurance",
            "company": "HDFC Life",
            "premium": 8000,  # Monthly premium in ₹
            "coverage": 3000000,  # Coverage in ₹ (30 lakhs)
            "term": "Lifetime",
            "features": ["Death benefit", "Cash value accumulation", "Guaranteed premiums"],
            "rating": 4.6,
            "description": "Permanent life insurance with cash value growth and guaranteed benefits from HDFC Life.",
            "score": ml_score * 1.1  # Adjusted score
        },
        {
            "id": 3,
            "name": "Universal Life Insurance",
            "company": "ICICI Prudential",
            "premium": 6000,  # Monthly premium in ₹
            "coverage": 4000000,  # Coverage in ₹ (40 lakhs)
            "term": "Flexible",
            "features": ["Death benefit", "Flexible premiums", "Investment options"],
            "rating": 4.7,
            "description": "Flexible universal life insurance with adjustable premiums and benefits from ICICI Prudential.",
            "score": ml_score # Base score
        },
        {
            "id": 4,
            "name": "Endowment Plan",
            "company": "SBI Life",
            "premium": 4000,  # Monthly premium in ₹
            "coverage": 2500000,  # Coverage in ₹ (25 lakhs)
            "term": "15 years",
            "features": ["Death benefit", "Maturity benefit", "Bonus", "Tax benefits"],
            "rating": 4.5,
            "description": "Traditional endowment plan with guaranteed returns and tax benefits under Section 80C.",
            "score": ml_score * 0.8  # Adjusted score
        },
        {
            "id": 5,
            "name": "ULIP (Unit Linked Insurance Plan)",
            "company": "Bajaj Allianz",
            "premium": 5000,  # Monthly premium in ₹
            "coverage": 3500000,  # Coverage in ₹ (35 lakhs)
            "term": "Flexible",
            "features": ["Death benefit", "Investment growth", "Flexible fund options", "Partial withdrawal"],
            "rating": 4.4,
            "description": "Unit Linked Insurance Plan combining insurance with investment opportunities.",
            "score": ml_score * 0.85  # Adjusted score
        }
    ]
    
    # Sort the policies based on the derived score
    policies.sort(key=lambda x: x['score'], reverse=True)
    
    return policies 