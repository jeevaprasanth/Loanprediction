"""
Database Viewer for Loan AI System
View MongoDB database contents and statistics
"""

import pymongo
from config import MONGODB_CONFIG
from datetime import datetime

def connect_to_mongodb():
    """Connect to MongoDB"""
    try:
        # Build connection string
        if MONGODB_CONFIG['username'] and MONGODB_CONFIG['password']:
            connection_string = f"mongodb://{MONGODB_CONFIG['username']}:{MONGODB_CONFIG['password']}@{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}?authSource={MONGODB_CONFIG['auth_source']}"
        else:
            connection_string = f"mongodb://{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}"
        
        client = pymongo.MongoClient(connection_string)
        db = client[MONGODB_CONFIG['database']]
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        return client, db
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\n💡 Make sure MongoDB server is running:")
        print("   - Windows: mongod.exe --dbpath \"C:\\data\\db\"")
        print("   - Linux/Mac: mongod --dbpath /var/lib/mongodb")
        return None, None

def view_database():
    """View database contents"""
    client, db = connect_to_mongodb()
    
    if not db:
        return
    
    try:
        print("\n" + "="*60)
        print("📊 LOAN AI DATABASE VIEWER")
        print("="*60)
        
        # Get all collections
        collections = db.list_collection_names()
        print(f"\n📁 Collections in '{MONGODB_CONFIG['database']}':")
        for collection in collections:
            print(f"   - {collection}")
        
        if not collections:
            print("   No collections found (database is empty)")
            return
        
        # Show predictions collection details
        if 'predictions' in collections:
            print(f"\n📈 Predictions Collection:")
            predictions_collection = db['predictions']
            
            # Get statistics
            total_count = predictions_collection.count_documents({})
            print(f"   Total predictions: {total_count}")
            
            if total_count > 0:
                # Get risk level distribution
                pipeline = [
                    {"$group": {"_id": "$risk_level", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}}
                ]
                risk_distribution = list(predictions_collection.aggregate(pipeline))
                
                print(f"\n🎯 Risk Level Distribution:")
                for item in risk_distribution:
                    risk_level = item['_id']
                    count = item['count']
                    percentage = (count / total_count) * 100
                    print(f"   {risk_level}: {count} ({percentage:.1f}%)")
                
                # Get prediction outcomes
                pipeline = [
                    {"$group": {"_id": "$prediction", "count": {"$sum": 1}}},
                    {"$sort": {"_id": 1}}
                ]
                prediction_outcomes = list(predictions_collection.aggregate(pipeline))
                
                print(f"\n📋 Prediction Outcomes:")
                for item in prediction_outcomes:
                    prediction = item['_id']
                    count = item['count']
                    outcome = "Will Default" if prediction == 1 else "Will Not Default"
                    print(f"   {outcome}: {count}")
                
                # Show recent predictions
                print(f"\n🕐 Recent Predictions (last 5):")
                recent = list(predictions_collection.find().sort("timestamp", -1).limit(5))
                
                for i, doc in enumerate(recent, 1):
                    timestamp = doc.get('timestamp', 'N/A')
                    risk_level = doc.get('risk_level', 'N/A')
                    probability = doc.get('probability', 0)
                    applicant_data = doc.get('applicant_data', {})
                    
                    # Extract key info
                    age = applicant_data.get('age', 'N/A')
                    income = applicant_data.get('income', 'N/A')
                    credit_score = applicant_data.get('credit_score', 'N/A')
                    
                    print(f"\n   {i}. {timestamp}")
                    print(f"      Risk Level: {risk_level} ({probability:.3f})")
                    print(f"      Age: {age}, Income: {income}, Credit Score: {credit_score}")
        
        # Show database statistics
        print(f"\n📊 Database Statistics:")
        db_stats = db.command("dbStats")
        data_size = db_stats.get('dataSize', 0)
        storage_size = db_stats.get('storageSize', 0)
        index_size = db_stats.get('indexSize', 0)
        
        print(f"   Data Size: {data_size / 1024:.2f} KB")
        print(f"   Storage Size: {storage_size / 1024:.2f} KB")
        print(f"   Index Size: {index_size / 1024:.2f} KB")
        
        # Show indexes
        print(f"\n🔍 Indexes on 'predictions' collection:")
        indexes = predictions_collection.list_indexes()
        for index in indexes:
            name = index.get('name', 'N/A')
            keys = index.get('key', {})
            print(f"   - {name}: {keys}")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"❌ Error viewing database: {e}")
    
    finally:
        if client:
            client.close()
            print("\n🔌 MongoDB connection closed")

def show_sample_data():
    """Show sample prediction data"""
    client, db = connect_to_mongodb()
    
    if not db:
        return
    
    try:
        print("\n📝 Sample Prediction Documents:")
        print("-" * 40)
        
        predictions_collection = db['predictions']
        samples = list(predictions_collection.find().limit(3))
        
        if not samples:
            print("No prediction data found in database")
            return
        
        for i, doc in enumerate(samples, 1):
            print(f"\nSample {i}:")
            print(f"  Timestamp: {doc.get('timestamp', 'N/A')}")
            print(f"  Prediction: {doc.get('prediction', 'N/A')}")
            print(f"  Probability: {doc.get('probability', 'N/A')}")
            print(f"  Risk Level: {doc.get('risk_level', 'N/A')}")
            print(f"  Applicant Data: {doc.get('applicant_data', {})}")
        
    except Exception as e:
        print(f"❌ Error showing sample data: {e}")
    
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    print("🚀 Loan AI - Database Viewer")
    print("=" * 50)
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "sample":
            show_sample_data()
        elif command == "stats":
            view_database()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: stats, sample")
    else:
        view_database()
