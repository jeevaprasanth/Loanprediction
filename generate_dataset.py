import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import random

def generate_loan_dataset(n_samples=5000):
    """
    Generate a synthetic loan dataset with realistic patterns (Indian context)
    """
    np.random.seed(42)
    random.seed(42)
    
    # Generate Indian names for realism
    indian_first_names = ['Rahul', 'Priya', 'Amit', 'Anjali', 'Vikram', 'Sneha', 'Rajesh', 'Kavita', 'Sanjay', 'Meena',
                          'Arun', 'Pooja', 'Deepak', 'Neha', 'Manish', 'Rashmi', 'Vijay', 'Swati', 'Ajay', 'Divya',
                          'Suresh', 'Anita', 'Mukesh', 'Shweta', 'Ramesh', 'Geeta', 'Dinesh', 'Rekha', 'Naresh', 'Sunita']
    indian_last_names = ['Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Mishra', 'Agarwal', 'Jain', 'Patel', 'Shah',
                         'Reddy', 'Nair', 'Menon', 'Iyer', 'Pillai', 'Chatterjee', 'Mukherjee', 'Banerjee', 'Chakraborty', 'Ghosh']
    
    # Generate features with realistic distributions (Indian context)
    data = {
        'applicant_name': [f"{random.choice(indian_first_names)} {random.choice(indian_last_names)}" for _ in range(n_samples)],
        'age': np.random.normal(40, 12, n_samples).astype(int),
        'income': np.random.lognormal(13.0, 0.5, n_samples).astype(int),  # Indian Rupees (₹2L - ₹30L)
        'loan_amount': np.random.lognormal(12.0, 0.4, n_samples).astype(int),  # Indian Rupees (₹50K - ₹50L)
        'credit_score': np.random.normal(650, 100, n_samples).astype(int),
        'employment_length': np.random.exponential(5, n_samples).astype(int),
        'debt_to_income_ratio': np.random.beta(2, 5, n_samples) * 0.6,
        'home_ownership': np.random.choice(['RENT', 'OWN', 'MORTGAGE'], n_samples, p=[0.35, 0.25, 0.40]),
        'loan_purpose': np.random.choice(['debt_consolidation', 'home_improvement', 'business', 'education', 'other'], 
                                       n_samples, p=[0.35, 0.20, 0.15, 0.15, 0.15]),
        'employment_status': np.random.choice(['employed', 'self_employed', 'unemployed', 'retired'], 
                                           n_samples, p=[0.70, 0.15, 0.10, 0.05])
    }
    
    df = pd.DataFrame(data)
    
    # Clean up unrealistic values (Indian context)
    df['age'] = df['age'].clip(18, 80)
    df['income'] = df['income'].clip(200000, 30000000)  # ₹2L - ₹3Cr
    df['loan_amount'] = df['loan_amount'].clip(50000, 50000000)  # ₹50K - ₹5Cr
    df['credit_score'] = df['credit_score'].clip(300, 850)
    df['employment_length'] = df['employment_length'].clip(0, 40)
    df['debt_to_income_ratio'] = df['debt_to_income_ratio'].clip(0, 0.6)
    
    # Generate loan default target based on realistic patterns
    # Higher risk factors: low credit score, high debt-to-income, unemployed, large loan amount relative to income
    risk_score = (
        (850 - df['credit_score']) / 550 * 0.3 +
        df['debt_to_income_ratio'] / 0.6 * 0.25 +
        (df['employment_status'] == 'unemployed').astype(int) * 0.2 +
        (df['employment_status'] == 'self_employed').astype(int) * 0.1 +
        (df['loan_amount'] / df['income']).clip(0, 2) / 2 * 0.15
    )
    
    # Add some randomness and convert to binary
    probability = risk_score + np.random.normal(0, 0.1, n_samples)
    probability = probability.clip(0, 1)
    df['loan_default'] = (probability > 0.3).astype(int)
    
    # Add some missing values to simulate real data
    missing_indices = np.random.choice(n_samples, int(0.05 * n_samples), replace=False)
    df.loc[missing_indices, 'employment_length'] = np.nan
    
    missing_indices = np.random.choice(n_samples, int(0.03 * n_samples), replace=False)
    df.loc[missing_indices, 'debt_to_income_ratio'] = np.nan
    
    return df

if __name__ == "__main__":
    # Generate dataset
    df = generate_loan_dataset(5000)
    
    # Save to CSV
    df.to_csv('data/loan_data.csv', index=False)
    
    # Display basic statistics
    print("Dataset generated successfully!")
    print(f"Total samples: {len(df)}")
    print(f"Default rate: {df['loan_default'].mean():.2%}")
    print("\nFeature statistics:")
    print(df.describe())
    
    print("\nClass distribution:")
    print(df['loan_default'].value_counts(normalize=True))
    
    # Save train/test split
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['loan_default'])
    train_df.to_csv('data/train_data.csv', index=False)
    test_df.to_csv('data/test_data.csv', index=False)
    
    print(f"\nTraining set: {len(train_df)} samples")
    print(f"Test set: {len(test_df)} samples")
