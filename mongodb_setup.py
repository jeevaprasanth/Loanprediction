"""
MongoDB Database Setup Script for Loan AI System
Run this script to set up MongoDB database and test connection
"""

import pymongo
import sys
from datetime import datetime

def setup_mongodb_database():
    """Setup MongoDB database for Loan AI System"""
    
    # MongoDB configuration
    mongo_config = {
        'host': 'localhost',
        'port': 27017,
        'database': 'loan_ai_db',
        'username': '',  # Leave empty for no auth
        'password': '',  # Leave empty for no auth
        'auth_source': 'admin'
    }
    
    try:
        # Build connection string
        if mongo_config['username'] and mongo_config['password']:
            connection_string = f"mongodb://{mongo_config['username']}:{mongo_config['password']}@{mongo_config['host']}:{mongo_config['port']}/{mongo_config['database']}?authSource={mongo_config['auth_source']}"
        else:
            connection_string = f"mongodb://{mongo_config['host']}:{mongo_config['port']}/{mongo_config['database']}"
        
        print("Connecting to MongoDB...")
        print(f"Connection string: mongodb://{'***' if mongo_config['password'] else ''}@{mongo_config['host']}:{mongo_config['port']}/{mongo_config['database']}")
        
        # Connect to MongoDB
        client = pymongo.MongoClient(connection_string)
        db = client[mongo_config['database']]
        
        # Test connection
        client.admin.command('ping')
        
        # Test database operations
        print("\n🔍 Testing database operations...")
        
        # Test insert
        test_doc = {
            'timestamp': datetime.now().isoformat(),
            'test': True,
            'message': 'MongoDB setup test document'
        }
        
        result = db.predictions.insert_one(test_doc)
        print(f"✅ Insert test: Document ID {result.inserted_id}")
        
        # Test find
        found_docs = list(db.predictions.find({'test': True}))
        print(f"✅ Find test: Found {len(found_docs)} documents")
        
        # Test count
        count = db.predictions.count_documents({'test': True})
        print(f"✅ Count test: {count} documents")
        
        # Clean up test data
        db.predictions.delete_many({'test': True})
        print("✅ Cleanup test: Removed test documents")
        
        print(f"\n🎉 MongoDB setup completed successfully!")
        print(f"Database: {mongo_config['database']}")
        print(f"Host: {mongo_config['host']}:{mongo_config['port']}")
        
        # Create indexes for better performance
        print("\n📊 Creating indexes...")
        db.predictions.create_index([('timestamp', -1)])
        db.predictions.create_index([('risk_level', 1)])
        db.predictions.create_index([('prediction', 1)])
        print("✅ Indexes created successfully!")
        
        print(f"\nPlease update the config.py file with these settings:")
        print(f"MONGODB_CONFIG = {{")
        print(f"    'host': '{mongo_config['host']}',")
        print(f"    'port': {mongo_config['port']},")
        print(f"    'database': '{mongo_config['database']}',")
        print(f"    'username': '{mongo_config['username']}',")
        print(f"    'password': '{mongo_config['password']}',")
        print(f"    'auth_source': '{mongo_config['auth_source']}',")
        print(f"    'connection_string': ''  # Will be constructed automatically")
        print(f"}}")
        print(f"DATABASE_TYPE = 'mongodb'  # Set to 'mongodb'")
        
        return True
        
    except pymongo.errors.ConnectionFailure as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure MongoDB server is running")
        print("2. Check if MongoDB is installed and accessible")
        print("3. Verify host and port settings")
        print("4. Check authentication credentials if using auth")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
        
    finally:
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")

def test_connection():
    """Test the MongoDB connection with current config"""
    try:
        from config import MONGODB_CONFIG
        
        print("\n🔍 Testing MongoDB connection...")
        
        # Build connection string
        if MONGODB_CONFIG['username'] and MONGODB_CONFIG['password']:
            connection_string = f"mongodb://{MONGODB_CONFIG['username']}:{MONGODB_CONFIG['password']}@{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}?authSource={MONGODB_CONFIG['auth_source']}"
        else:
            connection_string = f"mongodb://{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}"
        
        client = pymongo.MongoClient(connection_string)
        db = client[MONGODB_CONFIG['database']]
        
        # Test connection
        client.admin.command('ping')
        
        # Get database stats
        collections = db.list_collection_names()
        doc_count = db.predictions.count_documents({})
        
        print(f"✅ Connected to MongoDB successfully!")
        print(f"✅ Database: {MONGODB_CONFIG['database']}")
        print(f"✅ Collections: {collections}")
        print(f"✅ Total predictions: {doc_count}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    try:
        from config import MONGODB_CONFIG
        
        # Build connection string
        if MONGODB_CONFIG['username'] and MONGODB_CONFIG['password']:
            connection_string = f"mongodb://{MONGODB_CONFIG['username']}:{MONGODB_CONFIG['password']}@{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}?authSource={MONGODB_CONFIG['auth_source']}"
        else:
            connection_string = f"mongodb://{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}"
        
        client = pymongo.MongoClient(connection_string)
        db = client[MONGODB_CONFIG['database']]
        
        print("\n📝 Creating sample data...")
        
        sample_predictions = [
            {
                'timestamp': datetime.now().isoformat(),
                'applicant_data': {
                    'age': 35,
                    'income': 600000,
                    'credit_score': 680,
                    'employment_length': 5
                },
                'prediction': 0,
                'probability': 0.25,
                'risk_level': 'Low',
                'created_at': datetime.now()
            },
            {
                'timestamp': datetime.now().isoformat(),
                'applicant_data': {
                    'age': 45,
                    'income': 400000,
                    'credit_score': 550,
                    'employment_length': 2
                },
                'prediction': 1,
                'probability': 0.85,
                'risk_level': 'High',
                'created_at': datetime.now()
            },
            {
                'timestamp': datetime.now().isoformat(),
                'applicant_data': {
                    'age': 28,
                    'income': 800000,
                    'credit_score': 720,
                    'employment_length': 8
                },
                'prediction': 0,
                'probability': 0.15,
                'risk_level': 'Low',
                'created_at': datetime.now()
            }
        ]
        
        result = db.predictions.insert_many(sample_predictions)
        print(f"✅ Created {len(result.inserted_ids)} sample predictions")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Loan AI - MongoDB Database Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            test_connection()
        elif command == "sample":
            create_sample_data()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: setup, test, sample")
    else:
        if setup_mongodb_database():
            print("\n🎉 Setup completed! You can now run the application.")
            print("To test the connection, run: python mongodb_setup.py test")
            print("To create sample data, run: python mongodb_setup.py sample")
        else:
            print("\n❌ Setup failed. Please check the error messages above.")
