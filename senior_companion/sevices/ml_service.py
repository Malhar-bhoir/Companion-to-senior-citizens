import random
import math
import os
from typing import List, Dict, Any

import numpy as np
from joblib import dump, load
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Basic ML Model for 4th Year CSE Students
# This is a rule-based recommendation system - perfect for learning ML concepts
class InsuranceRecommendationModel:
    def __init__(self):
        # Rule-based baseline and optional RandomForest model
        self.is_trained = False
        self.model_path = os.path.join(os.path.dirname(__file__), "rf_pipeline.joblib")
        self.pipeline: Pipeline | None = None
        # Try to load a persisted model if present
        try:
            if os.path.exists(self.model_path):
                self.pipeline = load(self.model_path)
                self.is_trained = True
                print("RandomForest pipeline loaded from disk.")
            else:
                # Train on synthetic data once at startup
                self._train_on_synthetic_data(n_samples=1500, random_state=42)
        except Exception as exc:
            print(f"Warning: failed to load/train RF model: {exc}")
            self.pipeline = None
            self.is_trained = False
        print("ML Model initialized - Ready for predictions!")
        
    def _calculate_age(self, date_of_birth: str):
        """Calculate age from date of birth string"""
        try:
            from datetime import datetime
            birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except:
            return 35  # Default age if parsing fails
    
    def _encode_income_level(self, income_level: str):
        """Convert income level to numeric score - Feature Engineering"""
        # This is feature engineering - converting text to numbers for ML
        income_mapping = {
            'under-3lakh': 0.2,      # Under 3 lakhs per year
            '3lakh-5lakh': 0.4,      # 3-5 lakhs per year
            '5lakh-8lakh': 0.6,      # 5-8 lakhs per year
            '8lakh-12lakh': 0.7,     # 8-12 lakhs per year
            '12lakh-20lakh': 0.8,    # 12-20 lakhs per year
            '20lakh-30lakh': 0.9,    # 20-30 lakhs per year
            'over-30lakh': 1.0       # Over 30 lakhs per year
        }
        return income_mapping.get(income_level, 0.5)
    
    def _encode_coverage_amount(self, coverage_amount: str):
        """Convert coverage amount to numeric score - Indian Context"""
        # Coverage amounts in Indian Rupees (lakhs)
        coverage_mapping = {
            '10lakh-25lakh': 0.3,      # 10-25 lakhs coverage
            '25lakh-50lakh': 0.5,      # 25-50 lakhs coverage
            '50lakh-75lakh': 0.7,      # 50-75 lakhs coverage
            '75lakh-1crore': 0.8,      # 75 lakhs - 1 crore coverage
            '1crore-1.5crore': 0.9,    # 1-1.5 crore coverage
            '1.5crore-2crore': 0.95,   # 1.5-2 crore coverage
            'over-2crore': 1.0         # Over 2 crore coverage
        }
        return coverage_mapping.get(coverage_amount, 0.5)
    
    def _encode_premium_budget(self, premium_budget: str):
        """Convert premium budget to numeric score - Monthly Premium in Rupees"""
        # Monthly premium budget in Indian Rupees
        premium_mapping = {
            'under-2000': 0.2,        # Under ₹2,000 per month
            '2000-5000': 0.4,         # ₹2,000-5,000 per month
            '5000-8000': 0.6,         # ₹5,000-8,000 per month
            '8000-12000': 0.7,        # ₹8,000-12,000 per month
            '12000-20000': 0.8,       # ₹12,000-20,000 per month
            '20000-30000': 0.9,       # ₹20,000-30,000 per month
            'over-30000': 1.0         # Over ₹30,000 per month
        }
        return premium_mapping.get(premium_budget, 0.5)
    
    def _encode_risk_tolerance(self, risk_tolerance: str):
        """Convert risk tolerance to numeric score"""
        risk_mapping = {
            'conservative': 0.3,
            'moderate': 0.6,
            'aggressive': 0.9
        }
        return risk_mapping.get(risk_tolerance, 0.5)
    
    def _encode_smoking_status(self, smoking_status: str):
        """Convert smoking status to numeric score (lower is better for insurance)"""
        smoking_mapping = {
            'never': 1.0,
            'former': 0.7,
            'current': 0.3
        }
        return smoking_mapping.get(smoking_status, 0.5)
    
    def _encode_exercise_frequency(self, exercise_frequency: str):
        """Convert exercise frequency to numeric score (higher is better)"""
        exercise_mapping = {
            'none': 0.2,
            'light': 0.5,
            'moderate': 0.8,
            'intense': 1.0
        }
        return exercise_mapping.get(exercise_frequency, 0.5)
    
    def predict_policy_score(self, user_input):
        """
        ML Model Prediction Function - Perfect for 4th Year CSE Students!
        
        This is a rule-based recommendation system that demonstrates:
        1. Feature Engineering - Converting text to numbers
        2. Weighted Scoring - Different features have different importance
        3. Normalization - Scaling values between 0 and 1
        4. Business Logic - Insurance-specific rules
        
        In real ML projects, you would use:
        - Decision Trees, Random Forest, or Neural Networks
        - Training data from historical insurance claims
        - Cross-validation and model evaluation
        """
        
        # STEP 1: Feature Engineering - Convert user input to numerical features
        print("🔍 Extracting features from user input...")
        age = self._calculate_age(user_input.get('dateOfBirth', '1990-01-01'))
        income_score = self._encode_income_level(user_input.get('annualIncome', '5lakh-8lakh'))
        coverage_score = self._encode_coverage_amount(user_input.get('coverageAmount', '50lakh-75lakh'))
        premium_score = self._encode_premium_budget(user_input.get('premiumBudget', '5000-8000'))
        risk_score = self._encode_risk_tolerance(user_input.get('riskTolerance', 'moderate'))
        smoking_score = self._encode_smoking_status(user_input.get('smokingStatus', 'never'))
        exercise_score = self._encode_exercise_frequency(user_input.get('exerciseFrequency', 'moderate'))
        
        # STEP 2: Family and Health Factors
        family_size = int(user_input.get('familySize', '2')) if str(user_input.get('familySize', '2')).isdigit() else 2
        family_score = min(1.0, family_size / 4.0)  # Normalize family size (max 4 = score 1.0)
        
        medical_conditions = user_input.get('medicalConditions', [])
        medical_conditions_count = len(medical_conditions) if isinstance(medical_conditions, list) else 0
        health_score = max(0.1, 1.0 - (medical_conditions_count * 0.2))  # Each condition reduces score by 0.2
        
        dependents = user_input.get('dependents', 'no')
        dependents_score = 0.8 if dependents == 'yes' else 0.5
        
        # STEP 3: Age Factor (Insurance companies prefer ages 30-50)
        age_score = 1.0 if 30 <= age <= 50 else max(0.3, 1.0 - abs(age - 40) / 30)
        
        # STEP 4: Predict with RandomForest (sole model)
        if not (self.pipeline is not None and self.is_trained):
            # Train if needed (first run or failed load)
            self._train_on_synthetic_data(n_samples=1500, random_state=42)
        features = np.array([[
            age,
            income_score,
            coverage_score,
            premium_score,
            risk_score,
            smoking_score,
            exercise_score,
            family_score,
            health_score,
            dependents_score
        ]])
        rf_pred = float(self.pipeline.predict(features)[0]) if self.pipeline is not None else 0.5
        # Normalize to 0-1 range
        final_score = max(0.1, min(1.0, rf_pred))
        print(f"📊 ML Score calculated: {final_score:.3f}")
        return final_score

    # --------- RandomForest utilities ---------
    def _generate_feature_vector(self, sample: Dict[str, Any]) -> List[float]:
        age = self._calculate_age(sample.get('dateOfBirth', '1990-01-01'))
        income_score = self._encode_income_level(sample.get('annualIncome', '5lakh-8lakh'))
        coverage_score = self._encode_coverage_amount(sample.get('coverageAmount', '50lakh-75lakh'))
        premium_score = self._encode_premium_budget(sample.get('premiumBudget', '5000-8000'))
        risk_score = self._encode_risk_tolerance(sample.get('riskTolerance', 'moderate'))
        smoking_score = self._encode_smoking_status(sample.get('smokingStatus', 'never'))
        exercise_score = self._encode_exercise_frequency(sample.get('exerciseFrequency', 'moderate'))
        family_size = int(sample.get('familySize', '2')) if str(sample.get('familySize', '2')).isdigit() else 2
        family_score = min(1.0, family_size / 4.0)
        medical_conditions = sample.get('medicalConditions', [])
        medical_conditions_count = len(medical_conditions) if isinstance(medical_conditions, list) else 0
        health_score = max(0.1, 1.0 - (medical_conditions_count * 0.2))
        dependents = sample.get('dependents', 'no')
        dependents_score = 0.8 if dependents == 'yes' else 0.5
        return [
            age,
            income_score,
            coverage_score,
            premium_score,
            risk_score,
            smoking_score,
            exercise_score,
            family_score,
            health_score,
            dependents_score,
        ]

    def _synthetic_target(self, sample: Dict[str, Any]) -> float:
        # Realistic synthetic target: balances affordability, protection needs, and lifestyle risk
        vec = self._generate_feature_vector(sample)
        age, income, coverage, premium, risk, smoking, exercise, family, health, dependents = vec
        # Nonlinearities
        age_pref = 1.0 if 30 <= age <= 50 else max(0.4, 1.0 - abs(age - 40) / 30)
        affordability = 1.0 - abs(premium - (0.6 * (1.1 - income)))  # lower premium preferred for low income
        affordability = max(0.1, min(1.0, affordability))
        lifestyle = (exercise * 0.55 + health * 0.45)
        habit = smoking
        needs = min(1.0, (coverage * 0.65 + family * 0.35))
        risk_alignment = 1.0 - min(1.0, abs(risk - 0.6) * 1.2)  # prefer moderate
        score = (
            0.20 * income +
            0.18 * needs +
            0.16 * affordability +
            0.14 * habit +
            0.14 * lifestyle +
            0.10 * age_pref +
            0.08 * risk_alignment
        )
        return max(0.1, min(1.0, score))

    def _random_choice(self, options: List[str]) -> str:
        return random.choice(options)

    def _synthesize_user(self, rng: random.Random) -> Dict[str, Any]:
        # Generate synthetic user profiles within expected value spaces
        age_year = rng.randint(1960, 2004)  # ages roughly 21-65
        month = rng.randint(1, 12)
        day = rng.randint(1, 28)
        sample = {
            'dateOfBirth': f"{age_year:04d}-{month:02d}-{day:02d}",
            'annualIncome': self._random_choice(['under-3lakh','3lakh-5lakh','5lakh-8lakh','8lakh-12lakh','12lakh-20lakh','20lakh-30lakh','over-30lakh']),
            'coverageAmount': self._random_choice(['10lakh-25lakh','25lakh-50lakh','50lakh-75lakh','75lakh-1crore','1crore-1.5crore','1.5crore-2crore','over-2crore']),
            'premiumBudget': self._random_choice(['under-2000','2000-5000','5000-8000','8000-12000','12000-20000','20000-30000','over-30000']),
            'riskTolerance': self._random_choice(['conservative','moderate','aggressive']),
            'smokingStatus': self._random_choice(['never','former','current']),
            'exerciseFrequency': self._random_choice(['none','light','moderate','intense']),
            'familySize': str(rng.randint(1, 6)),
            'medicalConditions': ["cond"] * rng.randint(0, 3),
            'dependents': self._random_choice(['yes','no'])
        }
        return sample

    def _train_on_synthetic_data(self, n_samples: int = 1000, random_state: int | None = None) -> None:
        rng = random.Random(random_state)
        feature_rows: List[List[float]] = []
        targets: List[float] = []
        groups: List[int] = []  # grouping for debiasing (e.g., smoking status bucket 0/1/2)

        # Generate balanced base distributions by sampling in strata
        smoking_options = ['never','former','current']
        risk_options = ['conservative','moderate','aggressive']
        income_bins = ['under-3lakh','3lakh-5lakh','5lakh-8lakh','8lakh-12lakh','12lakh-20lakh','20lakh-30lakh','over-30lakh']

        for _ in range(n_samples):
            sample = self._synthesize_user(rng)
            # induce correlation: higher income tends to higher coverage and premium range selection
            inc_idx = income_bins.index(sample['annualIncome'])
            if inc_idx >= 4 and rng.random() < 0.6:
                sample['coverageAmount'] = rng.choice(['75lakh-1crore','1crore-1.5crore','1.5crore-2crore','over-2crore'])
            if inc_idx <= 2 and rng.random() < 0.6:
                sample['premiumBudget'] = rng.choice(['under-2000','2000-5000','5000-8000'])
            if sample['smokingStatus'] == 'current' and rng.random() < 0.7:
                # current smokers more likely to have lower exercise and health
                sample['exerciseFrequency'] = rng.choice(['none','light'])
                sample['medicalConditions'] = ["cond"] * max(1, rng.randint(1, 2))

            features = self._generate_feature_vector(sample)
            feature_rows.append(features)
            y = self._synthetic_target(sample) * rng.uniform(0.98, 1.02)
            targets.append(y)

            # Group by (smoking, risk) for reweighting
            s_idx = smoking_options.index(sample['smokingStatus'])
            r_idx = risk_options.index(sample['riskTolerance'])
            groups.append(s_idx * 3 + r_idx)

        X = np.array(feature_rows, dtype=float)
        y = np.array(targets, dtype=float)

        # Debiasing via inverse-frequency sample weights across groups
        unique, counts = np.unique(np.array(groups), return_counts=True)
        freq = {int(g): int(c) for g, c in zip(unique, counts)}
        weights = np.array([1.0 / freq[g] for g in groups], dtype=float)
        # Normalize weights to mean 1.0
        weights *= (len(weights) / weights.sum())

        # Preprocessing + model pipeline
        model = RandomForestRegressor(
            n_estimators=300,
            max_depth=10,
            min_samples_leaf=3,
            random_state=42,
            n_jobs=-1
        )
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('model', model)
        ])

        pipe.fit(X, y, model__sample_weight=weights)
        self.pipeline = pipe
        self.is_trained = True
        try:
            dump(pipe, self.model_path)
            print(f"RandomForest pipeline trained and saved to {self.model_path}")
        except Exception as exc:
            print(f"Warning: failed to save RF pipeline: {exc}")

# Global model instance
ml_model = InsuranceRecommendationModel()

def rank_policies(user_input):
    """Rank policies based on user input using ML model"""
    # Get ML score
    ml_score = ml_model.predict_policy_score(user_input)
    
    # Generate policy recommendations with ML scoring - Indian Insurance Companies
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
            "score": ml_score * 0.9  # Slightly lower score for term life
        },
        {
            "id": 2,
            "name": "Whole Life Insurance",
            "company": "HDFC Life",
            "premium": 8000,  # Monthly premium in ₹
            "coverage": 3000000,  # Coverage in ₹ (30 lakhs)
            "term": "Lifetime",
            "features": ["Death benefit", "Cash value accumulation", "Dividends", "Guaranteed premiums"],
            "rating": 4.6,
            "description": "Permanent life insurance with cash value growth and guaranteed benefits from HDFC Life.",
            "score": ml_score * 1.1  # Higher score for whole life
        },
        {
            "id": 3,
            "name": "Universal Life Insurance",
            "company": "ICICI Prudential",
            "premium": 6000,  # Monthly premium in ₹
            "coverage": 4000000,  # Coverage in ₹ (40 lakhs)
            "term": "Flexible",
            "features": ["Death benefit", "Flexible premiums", "Cash value", "Investment options"],
            "rating": 4.7,
            "description": "Flexible universal life insurance with adjustable premiums and benefits from ICICI Prudential.",
            "score": ml_score  # Base score for universal life
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
            "score": ml_score * 0.8  # Lower score for endowment
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
            "score": ml_score * 0.85  # Moderate score for ULIP
        }
    ]
    
    # Sort by ML score
    policies.sort(key=lambda x: x['score'], reverse=True)
    
    return policies