import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import joblib
import warnings
warnings.filterwarnings('ignore')

class LoanPredictor:
    def __init__(self):
        self.models = {}
        self.preprocessor = None
        self.best_model = None
        self.best_model_name = None
        self.feature_columns = None
        
    def load_data(self, filepath):
        """Load and prepare the dataset"""
        df = pd.read_csv(filepath)
        return df
    
    def preprocess_and_train(self, df):
        """Complete preprocessing and training pipeline"""
        # Separate features and target (exclude applicant_name)
        feature_columns = [col for col in df.columns if col not in ['loan_default', 'applicant_name']]
        X = df[feature_columns]
        y = df['loan_default']
        
        # Identify numerical and categorical columns
        numerical_features = ['age', 'income', 'loan_amount', 'credit_score', 
                            'employment_length', 'debt_to_income_ratio']
        categorical_features = ['home_ownership', 'loan_purpose', 'employment_status']
        
        # Handle missing values
        # Numerical columns - fill with median
        numerical_columns = X.select_dtypes(include=['int64', 'float64']).columns
        for col in numerical_columns:
            X[col].fillna(X[col].median(), inplace=True)
        
        # Categorical columns - fill with mode
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            X[col].fillna(X[col].mode()[0], inplace=True)
        
        # Encode categorical variables
        X_encoded = self.encode_categorical(X)
        
        # Scale numerical features
        self.scaler = StandardScaler()
        numerical_cols = X_encoded.select_dtypes(include=['int64', 'float64']).columns
        X_encoded[numerical_cols] = self.scaler.fit_transform(X_encoded[numerical_cols])
        
        self.feature_columns = X_encoded.columns
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_encoded, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train models
        self.train_models(self.X_train, self.y_train)
        
        # Return the full processed dataframe with target
        df_processed = X_encoded.copy()
        df_processed['loan_default'] = y.values
        return df_processed
    
    def encode_categorical(self, df, fit=True):
        """Handle categorical encoding"""
        df_encoded = df.copy()
        
        if fit:
            self.encoders = {}
            for feature in df.select_dtypes(include=['object']).columns:
                self.encoders[feature] = LabelEncoder()
                df_encoded[feature] = self.encoders[feature].fit_transform(df[feature])
        else:
            for feature in df.select_dtypes(include=['object']).columns:
                if feature in self.encoders:
                    # Handle unseen categories
                    unique_values = set(self.encoders[feature].classes_)
                    processed_values = df[feature].apply(
                        lambda x: x if x in unique_values else self.encoders[feature].classes_[0]
                    )
                    df_encoded[feature] = self.encoders[feature].transform(processed_values)
        
        return df_encoded
    
    def train_models(self, X_train, y_train):
        """Train multiple models and compare performance"""
        # Define models
        models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
            'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100)
        }
        
        # Train and evaluate each model
        results = {}
        
        for name, model in models.items():
            print(f"\nTraining {name}...")
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            
            # Train on full training set
            model.fit(X_train, y_train)
            
            results[name] = {
                'model': model,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
            
            print(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Select best model
        best_name = max(results.keys(), key=lambda x: results[x]['cv_mean'])
        self.best_model = results[best_name]['model']
        self.best_model_name = best_name
        self.models = results
        
        print(f"\nBest model: {best_name} with CV accuracy: {results[best_name]['cv_mean']:.4f}")
        
        return results
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the best model on test set"""
        if self.best_model is None:
            raise ValueError("No model trained yet!")
        
        y_pred = self.best_model.predict(X_test)
        y_prob = self.best_model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        auc_score = roc_auc_score(y_test, y_prob)
        
        print(f"\n=== {self.best_model_name} Test Results ===")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"AUC-ROC: {auc_score:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return {
            'accuracy': accuracy,
            'auc_score': auc_score,
            'predictions': y_pred,
            'probabilities': y_prob
        }
    
    def save_model(self, model_path='models/loan_model.pkl', preprocessor_path='models/preprocessor.pkl'):
        """Save the best model and preprocessing pipeline"""
        joblib.dump(self.best_model, model_path)
        joblib.dump({
            'encoders': self.encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'model_name': self.best_model_name
        }, preprocessor_path)
        print(f"\nModel saved to {model_path}")
        print(f"Preprocessor saved to {preprocessor_path}")
    
    def load_model(self, model_path='models/loan_model.pkl', preprocessor_path='models/preprocessor.pkl'):
        """Load saved model and preprocessing pipeline"""
        self.best_model = joblib.load(model_path)
        preprocessing_data = joblib.load(preprocessor_path)
        self.encoders = preprocessing_data['encoders']
        self.scaler = preprocessing_data['scaler']
        self.feature_columns = preprocessing_data['feature_columns']
        self.best_model_name = preprocessing_data['model_name']
        print(f"Model loaded: {self.best_model_name}")
    
    def predict_single(self, applicant_data):
        """Make prediction for a single applicant"""
        if self.best_model is None:
            raise ValueError("No model loaded!")
        
        # Convert to DataFrame if needed
        if isinstance(applicant_data, dict):
            df = pd.DataFrame([applicant_data])
        else:
            df = applicant_data.copy()
        
        # Remove applicant_name if present (not used for ML)
        if 'applicant_name' in df.columns:
            df = df.drop('applicant_name', axis=1)
        
        # Ensure all required columns are present
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0  # Default value
        
        # Select only feature columns
        df_features = df[self.feature_columns]
        
        # Handle missing values
        numerical_features = ['age', 'income', 'loan_amount', 'credit_score', 
                            'employment_length', 'debt_to_income_ratio']
        categorical_features = ['home_ownership', 'loan_purpose', 'employment_status']
        
        # Fill missing numerical values with median (using training statistics)
        for feature in numerical_features:
            if df_features[feature].isnull().any():
                df_features[feature].fillna(0, inplace=True)  # Simple fallback
        
        # Fill missing categorical values with mode
        for feature in categorical_features:
            if df_features[feature].isnull().any():
                df_features[feature].fillna('unknown', inplace=True)
        
        # Encode categorical variables
        if categorical_features:
            df_features = self.encode_categorical(df_features, fit=False)
        
        # Scale numerical features only
        numerical_cols_to_scale = df_features.select_dtypes(include=['int64', 'float64']).columns
        df_features[numerical_cols_to_scale] = self.scaler.transform(df_features[numerical_cols_to_scale])
        
        # Make prediction
        prediction = self.best_model.predict(df_features)[0]
        probability = self.best_model.predict_proba(df_features)[0][1]
        
        # Determine risk level based on credit score
        credit_score = applicant_data.get('credit_score', 0)
        if credit_score >= 600:
            risk_level = 'Low'
        elif credit_score >= 400:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': risk_level
        }

def main():
    # Initialize predictor
    predictor = LoanPredictor()
    
    # Load data
    print("Loading data...")
    df = predictor.load_data('data/train_data.csv')
    
    # Preprocess data
    print("Preprocessing data...")
    df_processed = predictor.preprocess_and_train(df)
    
    # Prepare features and target
    X = df_processed[predictor.feature_columns]
    y = df_processed['loan_default']
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train models
    results = predictor.train_models(X_train, y_train)
    
    # Evaluate on validation set
    evaluation = predictor.evaluate_model(X_val, y_val)
    
    # Save model
    predictor.save_model()
    
    # Test with a sample prediction
    print("\n=== Sample Prediction ===")
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
    
    prediction = predictor.predict_single(sample_applicant)
    print(f"Sample applicant prediction: {prediction}")

if __name__ == "__main__":
    main()
