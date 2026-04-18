#!/usr/bin/env python3
"""
Script to clear all prediction history data from the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_utils import DatabaseManager
import config

def clear_all_history():
    """Clear all prediction history from the database"""
    try:
        print("Connecting to database...")
        db_manager = DatabaseManager()
        
        # Initialize database connection
        connection = db_manager.get_connection()
        if not connection:
            print("Failed to connect to database")
            return False
        
        if db_manager.db_type == 'mongodb':
            print("Clearing MongoDB history...")
            deleted_count = db_manager.delete_documents('predictions')
            print(f"Deleted {deleted_count} documents from MongoDB")
            
        elif db_manager.db_type == 'mysql':
            print("Clearing MySQL history...")
            delete_query = "DELETE FROM predictions"
            db_manager.execute_query(delete_query)
            print("All records deleted from MySQL")
            
        elif db_manager.db_type == 'sqlite':
            print("Clearing SQLite history...")
            delete_query = "DELETE FROM predictions"
            db_manager.execute_query(delete_query)
            print("All records deleted from SQLite")
            
        else:
            print("Unknown database type")
            return False
            
        print("History cleared successfully!")
        return True
        
    except Exception as e:
        print(f"Error clearing history: {e}")
        return False

if __name__ == "__main__":
    print("=== Clear All Prediction History ===")
    print("This will permanently delete all prediction history data.")
    print("Type 'yes' to confirm:")
    
    confirmation = input().strip().lower()
    if confirmation == 'yes':
        success = clear_all_history()
        if success:
            print("Operation completed successfully.")
        else:
            print("Operation failed.")
    else:
        print("Operation cancelled.")
