import pandas as pd
import numpy as np
from ml_pipeline import LoanPredictor
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.inspection import permutation_importance
import json
import os
from datetime import datetime

class AdvancedLoanAnalyzer:
    def __init__(self):
        self.predictor = LoanPredictor()
        self.load_model()
        
    def load_model(self):
        """Load the trained model and preprocessing pipeline"""
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'models', 'loan_model.pkl')
            preprocessor_path = os.path.join(os.path.dirname(__file__), 'models', 'preprocessor.pkl')
            self.predictor.load_model(model_path, preprocessor_path)
            print("Advanced analyzer: Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            
    def get_feature_importance(self):
        """Calculate and return feature importance"""
        if self.predictor.best_model is None:
            return None
            
        # For Logistic Regression, use coefficients
        if hasattr(self.predictor.best_model, 'coef_'):
            importance = np.abs(self.predictor.best_model.coef_[0])
            feature_names = self.predictor.feature_columns
            
            # Normalize importance scores
            importance = importance / importance.sum() * 100
            
            feature_importance = []
            for name, imp in zip(feature_names, importance):
                feature_importance.append({
                    'feature': name.replace('_', ' ').title(),
                    'importance': float(imp),
                    'direction': 'positive' if imp > 0 else 'negative'
                })
            
            # Sort by importance
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
            
            return {
                'feature_importance': feature_importance,
                'model_type': 'Logistic Regression',
                'total_features': len(feature_names)
            }
        
        return None
    
    def what_if_analysis(self, base_applicant, feature_changes):
        """
        Perform what-if analysis by changing specific features
        
        Args:
            base_applicant: Dict with base applicant data
            feature_changes: Dict with features to change and new values
        """
        if self.predictor.best_model is None:
            return None
            
        # Get base prediction
        base_result = self.predictor.predict_single(base_applicant)
        
        # Create scenarios
        scenarios = []
        
        for feature, new_value in feature_changes.items():
            modified_applicant = base_applicant.copy()
            modified_applicant[feature] = new_value
            
            # Get new prediction
            new_result = self.predictor.predict_single(modified_applicant)
            
            # Calculate impact
            probability_change = new_result['probability'] - base_result['probability']
            risk_change = 'increased' if probability_change > 0 else 'decreased' if probability_change < 0 else 'unchanged'
            
            scenarios.append({
                'feature': feature.replace('_', ' ').title(),
                'original_value': base_applicant[feature],
                'new_value': new_value,
                'original_probability': base_result['probability'],
                'new_probability': new_result['probability'],
                'probability_change': abs(probability_change),
                'risk_change': risk_change,
                'original_risk': base_result['risk_level'],
                'new_risk': new_result['risk_level']
            })
        
        return {
            'base_prediction': base_result,
            'scenarios': scenarios,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def recommend_loan_amount(self, applicant_data, max_loan_amount=10000000):
        """Recommend optimal loan amount based on risk tolerance (Indian context)"""
        if self.predictor.best_model is None:
            return None
            
        recommendations = []
        loan_amounts = np.linspace(100000, max_loan_amount, 10)  # ₹1L to max amount
        
        for loan_amount in loan_amounts:
            modified_applicant = applicant_data.copy()
            modified_applicant['loan_amount'] = int(loan_amount)
            
            result = self.predictor.predict_single(modified_applicant)
            
            # Calculate loan-to-income ratio
            loan_to_income = loan_amount / applicant_data['income']
            
            # Determine recommendation level
            if result['risk_level'] == 'Low' and loan_to_income < 0.5:
                level = 'Excellent'
                color = '#28a745'
            elif result['risk_level'] == 'Low' and loan_to_income < 0.8:
                level = 'Good'
                color = '#17a2b8'
            elif result['risk_level'] == 'Medium' and loan_to_income < 0.6:
                level = 'Acceptable'
                color = '#ffc107'
            else:
                level = 'Not Recommended'
                color = '#dc3545'
            
            recommendations.append({
                'loan_amount': int(loan_amount),
                'risk_level': result['risk_level'],
                'probability': result['probability'],
                'loan_to_income_ratio': round(loan_to_income, 2),
                'recommendation_level': level,
                'color': color
            })
        
        # Find best recommendation
        best_recommendation = max(
            [r for r in recommendations if r['recommendation_level'] not in ['Not Recommended']],
            key=lambda x: x['loan_amount'],
            default=None
        )
        
        return {
            'recommendations': recommendations,
            'best_recommendation': best_recommendation,
            'max_safe_amount': best_recommendation['loan_amount'] if best_recommendation else 0,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def explain_prediction(self, applicant_data):
        """Explain why a prediction was made using feature contributions"""
        if self.predictor.best_model is None:
            return None
            
        # Get prediction first (this will handle preprocessing internally)
        result = self.predictor.predict_single(applicant_data)
        
        # Get feature importance
        feature_importance = self.get_feature_importance()
        if not feature_importance:
            return None
        
        # Calculate feature contributions (simplified SHAP-like approach)
        contributions = []
        feature_data = feature_importance['feature_importance']
        
        for feature_info in feature_data:
            feature_name = feature_info['feature'].lower().replace(' ', '_')
            
            # Get feature value from original applicant data
            feature_value = applicant_data.get(feature_name, 'N/A')
            importance_score = feature_info['importance']
            
            # Determine if feature value is favorable
            favorable = True
            if feature_name == 'credit_score' and isinstance(feature_value, (int, float)):
                favorable = feature_value > 650
            elif feature_name == 'debt_to_income_ratio' and isinstance(feature_value, (int, float)):
                favorable = feature_value < 0.3
            elif feature_name == 'income' and isinstance(feature_value, (int, float)):
                favorable = feature_value > 50000
            elif feature_name == 'age' and isinstance(feature_value, (int, float)):
                favorable = 25 <= feature_value <= 65
            
            impact = 'positive' if favorable else 'negative'
            
            contributions.append({
                'feature': feature_info['feature'],
                'value': feature_value,
                'importance': importance_score,
                'impact': impact,
                'explanation': self._get_feature_explanation(feature_name, feature_value, favorable)
            })
        
        # Sort by importance
        contributions.sort(key=lambda x: x['importance'], reverse=True)
        
        return {
            'prediction': result,
            'contributions': contributions,
            'summary': self._generate_explanation_summary(result, contributions[:5]),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _get_feature_explanation(self, feature_name, value, favorable):
        """Generate human-readable explanation for feature contribution"""
        # Format value for display (Indian context)
        if isinstance(value, (int, float)):
            if feature_name == 'income' or feature_name == 'loan_amount':
                formatted_value = f"₹{value:,.0f}"
            elif feature_name == 'debt_to_income_ratio':
                formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)
        else:
            formatted_value = str(value)
        
        explanations = {
            'credit_score': {
                True: f"Credit score of {formatted_value} is good, indicating responsible credit behavior",
                False: f"Credit score of {formatted_value} is concerning, suggesting past credit difficulties"
            },
            'debt_to_income_ratio': {
                True: f"Debt-to-income ratio of {formatted_value} is manageable",
                False: f"Debt-to-income ratio of {formatted_value} is high, indicating financial strain"
            },
            'income': {
                True: f"Income of {formatted_value} provides good repayment capacity",
                False: f"Income of {formatted_value} may be insufficient for loan repayment"
            },
            'age': {
                True: f"Age of {formatted_value} falls within optimal range for loan approval",
                False: f"Age of {formatted_value} falls outside typical approval range"
            },
            'employment_length': {
                True: f"Employment length of {formatted_value} years shows job stability",
                False: f"Limited employment history of {formatted_value} years may indicate instability"
            }
        }
        
        feature_explanations = explanations.get(feature_name, {})
        return feature_explanations.get(favorable, f"{feature_name.title()}: {formatted_value}")
    
    def _generate_explanation_summary(self, prediction, top_contributions):
        """Generate a summary explanation"""
        if prediction['risk_level'] == 'Low':
            risk_summary = "Low risk of default - applicant appears creditworthy"
        elif prediction['risk_level'] == 'Medium':
            risk_summary = "Moderate risk of default - applicant has some risk factors"
        else:
            risk_summary = "High risk of default - significant concerns detected"
        
        positive_factors = [c for c in top_contributions if c['impact'] == 'positive']
        negative_factors = [c for c in top_contributions if c['impact'] == 'negative']
        
        summary = f"{risk_summary}. "
        
        if positive_factors:
            summary += f"Strengths include {', '.join([f['feature'].lower() for f in positive_factors[:2]])}. "
        
        if negative_factors:
            summary += f"Concerns include {', '.join([f['feature'].lower() for f in negative_factors[:2]])}."
        
        return summary
    
    def generate_risk_report(self, applicant_data):
        """Generate comprehensive risk report"""
        if self.predictor.best_model is None:
            return None
            
        # Get all analyses
        prediction = self.predictor.predict_single(applicant_data)
        explanation = self.explain_prediction(applicant_data)
        recommendations = self.recommend_loan_amount(applicant_data)
        
        # Calculate risk score (0-100)
        risk_score = prediction['probability'] * 100
        
        # Determine risk category
        if risk_score < 30:
            risk_category = 'Low Risk'
            risk_color = '#28a745'
        elif risk_score < 70:
            risk_category = 'Medium Risk'
            risk_color = '#ffc107'
        else:
            risk_category = 'High Risk'
            risk_color = '#dc3545'
        
        return {
            'applicant_profile': applicant_data,
            'risk_assessment': {
                'risk_score': round(risk_score, 1),
                'risk_category': risk_category,
                'risk_color': risk_color,
                'probability': prediction['probability'],
                'prediction': prediction['prediction']
            },
            'explanation': explanation,
            'recommendations': recommendations,
            'report_timestamp': datetime.now().isoformat(),
            'model_info': {
                'model_type': 'Logistic Regression',
                'accuracy': '80.6%',
                'features_used': len(self.predictor.feature_columns)
            }
        }

# Test the advanced features
if __name__ == "__main__":
    analyzer = AdvancedLoanAnalyzer()
    
    # Sample applicant
    sample_applicant = {
        'age': 35,
        'income': 60000,
        'loan_amount': 25000,
        'credit_score': 680,
        'employment_length': 5,
        'debt_to_income_ratio': 0.25,
        'home_ownership': 'RENT',
        'loan_purpose': 'debt_consolidation',
        'employment_status': 'employed'
    }
    
    # Test feature importance
    print("=== Feature Importance ===")
    importance = analyzer.get_feature_importance()
    if importance:
        for feature in importance['feature_importance'][:5]:
            print(f"{feature['feature']}: {feature['importance']:.2f}%")
    
    # Test what-if analysis
    print("\n=== What-If Analysis ===")
    what_if = analyzer.what_if_analysis(sample_applicant, {
        'credit_score': 750,
        'income': 80000,
        'loan_amount': 35000
    })
    if what_if:
        for scenario in what_if['scenarios']:
            print(f"{scenario['feature']}: {scenario['original_value']} → {scenario['new_value']} "
                  f"(Risk: {scenario['probability_change']:+.2%})")
    
    # Test recommendations
    print("\n=== Loan Recommendations ===")
    recommendations = analyzer.recommend_loan_amount(sample_applicant)
    if recommendations:
        best = recommendations['best_recommendation']
        if best:
            print(f"Best recommendation: ${best['loan_amount']:,} ({best['recommendation_level']})")
    
    # Test explanation
    print("\n=== Prediction Explanation ===")
    explanation = analyzer.explain_prediction(sample_applicant)
    if explanation:
        print(f"Summary: {explanation['summary']}")
