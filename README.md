# Loan Default Prediction System

An AI-powered loan default prediction system that uses machine learning to assess loan risk based on applicant data. The system includes data preprocessing, model training, a Flask backend API, and a responsive web frontend.

## Features

- **Machine Learning Models**: Trains and compares Logistic Regression, Decision Tree, and Random Forest models
- **Data Preprocessing**: Handles missing values, categorical encoding, and feature scaling
- **Web Interface**: Responsive frontend with real-time form validation
- **REST API**: Flask backend with prediction endpoints
- **MongoDB Database**: NoSQL database for storing prediction history
- **Real-time Predictions**: Instant loan risk assessment
- **Risk Classification**: Categorizes applicants into Low, Medium, and High risk levels

## Project Structure

```
LoanAI/
├── backend/
│   └── app.py                 # Flask application
├── data/
│   ├── loan_data.csv          # Complete dataset
│   ├── train_data.csv         # Training data
│   └── test_data.csv          # Test data
├── models/
│   ├── loan_model.pkl         # Trained model
│   └── preprocessor.pkl       # Data preprocessor
├── static/
│   ├── css/
│   │   └── style.css         # Custom styles
│   └── js/
│       └── script.js         # Frontend JavaScript
├── templates/
│   ├── index.html            # Main application page
│   └── analytics.html        # Analytics dashboard
├── config.py                  # Database configuration
├── database_utils.py          # MongoDB database utilities
├── mongodb_setup.py           # MongoDB setup script
└── requirements.txt            # Python dependencies
```

## Installation

1. **Clone or download the project** to your local machine

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Generate Training Data

The system uses synthetic loan data for training. Generate the dataset:

```bash
python generate_dataset.py
```

This will create:
- `data/loan_data.csv` - Complete dataset (5000 samples)
- `data/train_data.csv` - Training set (4000 samples)
- `data/test_data.csv` - Test set (1000 samples)

### Step 2: Train the ML Models

Train and evaluate the machine learning models:

```bash
python ml_pipeline.py
```

This will:
- Train Logistic Regression, Decision Tree, and Random Forest models
- Select the best performing model (based on cross-validation)
- Save the trained model to `models/loan_model.pkl`
- Save preprocessing pipeline to `models/preprocessor.pkl`

### Step 3: Run the Web Application

Start the Flask web server:

```bash
cd backend
python app.py
```

The application will be available at: `http://localhost:5000`

## API Endpoints

### POST `/predict`
Make loan default predictions.

**Request Body:**
```json
{
  "age": 35,
  "income": 60000,
  "loan_amount": 25000,
  "credit_score": 680,
  "employment_length": 5,
  "debt_to_income_ratio": 0.25,
  "home_ownership": "RENT",
  "loan_purpose": "debt_consolidation",
  "employment_status": "employed"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "prediction": 0,
    "probability": 0.272,
    "risk_level": "Low"
  },
  "message": "Prediction completed successfully. Risk level: Low"
}
```

### GET `/history`
Retrieve prediction history.

**Response:**
```json
{
  "success": true,
  "history": [...],
  "count": 42
}
```

### GET `/model_info`
Get model information and statistics.

**Response:**
```json
{
  "success": true,
  "model_name": "Logistic Regression",
  "features": ["age", "income", ...],
  "accuracy": "80.6%",
  "auc_score": "0.852"
}
```

### GET `/health`
Health check endpoint.

## Model Performance

The best performing model (Logistic Regression) achieves:
- **Cross-validation accuracy**: 77.0%
- **Test accuracy**: 80.6%
- **AUC-ROC score**: 0.852

### Feature Importance

The model uses the following features:
1. **Personal Information**: Age, Income, Credit Score
2. **Employment Details**: Employment Status, Employment Length, Home Ownership
3. **Loan Information**: Loan Amount, Debt-to-Income Ratio, Loan Purpose

## Risk Classification

- **Low Risk** (Probability < 30%): Applicant likely to repay loan
- **Medium Risk** (30% ≤ Probability ≤ 70%): Moderate risk, requires careful consideration
- **High Risk** (Probability > 70%): High likelihood of default

## Web Interface Features

- **Real-time Form Validation**: Input validation with helpful error messages
- **Interactive Results**: Visual risk assessment with probability bars
- **Prediction History**: View and analyze past predictions
- **Statistics Dashboard**: Track risk distribution over time
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Model Information**: View model details and performance metrics

## Database Schema

The SQLite database stores prediction history:

```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    applicant_data TEXT NOT NULL,
    prediction INTEGER NOT NULL,
    probability REAL NOT NULL,
    risk_level TEXT NOT NULL
);
```

## Development

### Adding New Features

1. **New ML Models**: Add to `ml_pipeline.py` in the `train_models()` method
2. **New API Endpoints**: Add to `backend/app.py`
3. **Frontend Features**: Modify `static/js/script.js` and `templates/index.html`

### Model Retraining

To retrain the model with new data:

1. Update the dataset files in the `data/` directory
2. Run `python ml_pipeline.py` to retrain
3. Restart the Flask server

### Customization

- **Risk Thresholds**: Modify risk level thresholds in `static/js/script.js`
- **Model Selection**: Change model selection criteria in `ml_pipeline.py`
- **UI Styling**: Update `static/css/style.css`

## Technologies Used

- **Backend**: Python, Flask, scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite
- **Machine Learning**: Logistic Regression, Decision Tree, Random Forest
- **Data Processing**: Pandas, NumPy

## Limitations

- Uses synthetic data for demonstration purposes
- Model should be retrained with real loan data for production use
- Risk predictions are for educational purposes only
- Always consult with financial experts for real loan decisions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with local regulations when using for real financial applications.

## Support

For questions or issues:
1. Check the documentation above
2. Review the code comments
3. Test with the provided example data
4. Ensure all dependencies are properly installed

---

**Disclaimer**: This system is for educational and demonstration purposes only. Actual loan decisions should consider additional factors and comply with relevant financial regulations.
