# MongoDB Database Configuration
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'loan_ai_db',
    'username': '',  # Set your MongoDB username here
    'password': '',  # Set your MongoDB password here
    'auth_source': 'admin',  # Authentication database
    'connection_string': ''  # Will be constructed automatically
}

# Database connection settings
DATABASE_TYPE = 'sqlite'  # SQLite database (fallback when MongoDB is not available)
