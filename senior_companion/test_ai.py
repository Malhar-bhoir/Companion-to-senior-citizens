import joblib
import pandas as pd
import os
from datetime import date, datetime

# --- IMPORTANT: PLACE YOUR MODEL FILE HERE ---
# Create a folder named 'ml_models' next to manage.py
# Place your .joblib file inside that folder.
MODEL_PATH = os.path.join('ml_models', 'rf_pipeline.joblib')

# --- Utility Functions (Mimic the logic in the original service) ---
# ... (Functions remain the same) ...
def _calculate_age(dob_str):
    """Calculates age based on birth date string (YYYY-MM-DD)."""
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        today = date.today()
        # Simple age calculation
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except ValueError:
        return 35 # Default safe age for test

def _encode_category(value, categories):
    """Encodes a categorical string into a numerical score (0 to N-1)."""
    # This is a mock function, as the original service likely handles this
    # You will need to check your original mlservice.py if encoding is complex
    return categories.get(value, 0)

def run_test():
    print(f"--- Attempting to load model from: {MODEL_PATH} ---")
    
    # --- Load the Model ---
    try:
        model = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded successfully. Type: {type(model)}")
    except FileNotFoundError:
        print("❌ Error: MODEL NOT FOUND.")
        print("Please ensure you have run 'pip install joblib' and placed your '.joblib' file in the 'ml_models' folder.")
        return
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return

    # --- Define Sample Input Data ---
    MOCK_ENCODERS = {
        'income': {'0lakh-5lakh': 0, '5lakh-8lakh': 1, '8lakh+': 2},
        'coverage': {'10lakh-25lakh': 0, '50lakh-75lakh': 1},
        'premium': {'0-5000': 0, '5000-8000': 1},
        'risk': {'low': 0, 'moderate': 1, 'high': 2},
        'smoking': {'never': 0, 'occasional': 1, 'daily': 2},
        'exercise': {'low': 0, 'moderate': 1, 'high': 2}
    }
    
    # Mocking the data flow from the original service's output variables:
    test_data = {
        # Feature 1: Age (calculated from DOB)
        'age': _calculate_age('1958-05-15'), # Senior age, e.g., 67
        
        # Features 2-7 (Encoded scores from your data)
        'income_score': _encode_category('5lakh-8lakh', MOCK_ENCODERS['income']),
        'coverage_score': _encode_category('50lakh-75lakh', MOCK_ENCODERS['coverage']),
        'premium_score': _encode_category('5000-8000', MOCK_ENCODERS['premium']),
        'risk_score': _encode_category('moderate', MOCK_ENCODERS['risk']),
        'smoking_score': _encode_category('never', MOCK_ENCODERS['smoking']),
        'exercise_score': _encode_category('moderate', MOCK_ENCODERS['exercise']),
        
        # --- FIX: ADD THREE PLACEHOLDER REGION FEATURES (Set to 0) ---
        # The model is expecting 10 features total. These are likely OHE features.
        'region_northwest': 0, 
        'region_southeast': 0, 
        'region_southwest': 0,
    }
    
    # Check if the list of features is correct
    feature_names = [
        'age', 
        'income_score', 
        'coverage_score', 
        'premium_score', 
        'risk_score', 
        'smoking_score', 
        'exercise_score',
        # --- FIX: ADD PLACEHOLDER NAMES TO THE LIST (Total 10) ---
        'region_northwest',
        'region_southeast',
        'region_southwest',
    ]
    
    # Prepare the DataFrame for prediction
    df = pd.DataFrame([test_data], columns=feature_names)

    print("\n--- Input DataFrame for Model ---")
    print(df)
    print("---------------------------------")

    # --- Make a Prediction ---
    try:
        prediction = model.predict(df)
        print(f"🎉 Prediction Result (Raw): {prediction}")
        
        # Format the output for the user
        recommendation = "High Coverage Policy - Tier A" if prediction[0] > 0 else "Basic Coverage Policy - Tier B"
        print(f"🏆 Recommendation: {recommendation}")

    except Exception as e:
        print(f"❌ Prediction Failed: {e}")
        print("\nHINT: The model prediction failed.")
        print("1. Check the error message (e.g., 'X missing 1 features').")
        print("2. Adjust the keys in 'test_data' and 'feature_names' to match the model's exact requirements.")

if __name__ == "__main__":
    run_test()