# Production Configuration for Loan AI System
import os

# Database Configuration
DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')
MONGODB_CONFIG = {
    'host': os.getenv('MONGODB_HOST', 'localhost'),
    'port': int(os.getenv('MONGODB_PORT', 27017)),
    'database': os.getenv('MONGODB_DATABASE', 'loan_ai_db'),
    'username': os.getenv('MONGODB_USERNAME', ''),
    'password': os.getenv('MONGODB_PASSWORD', ''),
    'auth_source': os.getenv('MONGODB_AUTH_SOURCE', 'admin'),
    'connection_string': os.getenv('MONGODB_CONNECTION_STRING', '')
}

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes']
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Security Configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'app.log')

# Rate Limiting
RATE_LIMIT = os.getenv('RATE_LIMIT', '100 per hour')

# Model Configuration
MODEL_PATH = os.getenv('MODEL_PATH', 'models/loan_predictor.pkl')
DATA_PATH = os.getenv('DATA_PATH', 'data/train_data.csv')

# SSL Configuration (for HTTPS)
SSL_CERT = os.getenv('SSL_CERT', '')
SSL_KEY = os.getenv('SSL_KEY', '')
