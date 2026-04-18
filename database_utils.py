"""
Database utility module for Loan AI System
Supports MongoDB and SQLite databases
"""

import pymongo
import sqlite3
import json
from config import MONGODB_CONFIG, DATABASE_TYPE
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_type = DATABASE_TYPE
        self.mongo_client = None
        self.mongo_db = None
        self.sqlite_conn = None
        
    def get_connection(self):
        """Get database connection based on configuration"""
        try:
            if self.db_type == 'mongodb':
                return self._get_mongodb_connection()
            elif self.db_type == 'sqlite':
                return self._get_sqlite_connection()
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}. Supported types: 'mongodb', 'sqlite'")
        except Exception as e:
            print(f"Database connection error: {e}")
            raise e
    
    def _get_mongodb_connection(self):
        """Create MongoDB connection"""
        try:
            # Build connection string
            if MONGODB_CONFIG['username'] and MONGODB_CONFIG['password']:
                connection_string = f"mongodb://{MONGODB_CONFIG['username']}:{MONGODB_CONFIG['password']}@{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}?authSource={MONGODB_CONFIG['auth_source']}"
            else:
                connection_string = f"mongodb://{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/{MONGODB_CONFIG['database']}"
            
            self.mongo_client = pymongo.MongoClient(connection_string)
            self.mongo_db = self.mongo_client[MONGODB_CONFIG['database']]
            
            # Test connection
            self.mongo_client.admin.command('ping')
            print("MongoDB connection established successfully!")
            return self.mongo_db
            
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            raise e
    
    def _get_sqlite_connection(self):
        """Create SQLite connection"""
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'predictions.db')
            self.sqlite_conn = sqlite3.connect(db_path, check_same_thread=False)
            self.sqlite_conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            print("SQLite connection established successfully!")
            return self.sqlite_conn
        except Exception as e:
            print(f"SQLite connection failed: {e}")
            raise e
    
    def insert_document(self, collection_name, document):
        """Insert a document into MongoDB collection or SQLite table"""
        try:
            if self.db_type == 'mongodb':
                collection = self.mongo_db[collection_name]
                result = collection.insert_one(document)
                return result.inserted_id
            elif self.db_type == 'sqlite':
                # For SQLite, use execute_query method
                if collection_name == 'predictions':
                    query = '''
                        INSERT INTO predictions (timestamp, applicant_data, prediction, probability, risk_level)
                        VALUES (?, ?, ?, ?, ?)
                    '''
                    params = (
                        document.get('timestamp', datetime.now().isoformat()),
                        json.dumps(document.get('applicant_data', {})),
                        document.get('prediction', 0),
                        document.get('probability', 0.0),
                        document.get('risk_level', 'Unknown')
                    )
                    cursor = self.sqlite_conn.execute(query, params)
                    self.sqlite_conn.commit()
                    return cursor.lastrowid
                else:
                    raise ValueError(f"Unsupported collection/table: {collection_name}")
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            print(f"Insert error: {e}")
            raise e

    def execute_query(self, query, params=None, fetch_all=False):
        """Execute SQL query for SQLite database"""
        try:
            if self.db_type == 'sqlite':
                cursor = self.sqlite_conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if fetch_all:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
                
                # For INSERT, UPDATE, DELETE operations, commit the transaction
                if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE')):
                    self.sqlite_conn.commit()
                
                return result
            else:
                raise ValueError(f"execute_query is only supported for SQLite, not {self.db_type}")
        except Exception as e:
            print(f"SQL query error: {e}")
            raise e
    
    def find_documents(self, collection_name, query=None, sort=None, limit=None):
        """Find documents in MongoDB collection or SQLite table"""
        try:
            if self.db_type == 'mongodb':
                collection = self.mongo_db[collection_name]
                
                mongo_query = {}
                if query:
                    mongo_query = query
                
                cursor = collection.find(mongo_query)
                
                if sort:
                    cursor = cursor.sort(sort)
                
                if limit:
                    cursor = cursor.limit(limit)
                
                return list(cursor)
            elif self.db_type == 'sqlite':
                if collection_name == 'predictions':
                    sql_query = "SELECT timestamp, applicant_data, prediction, probability, risk_level FROM predictions"
                    params = []
                    
                    # Add WHERE clause if query is provided
                    if query:
                        # Simple query support - can be extended
                        pass  # For now, ignore query for SQLite
                    
                    # Add ORDER BY for sort
                    if sort:
                        for field, direction in sort:
                            order = "DESC" if direction == -1 else "ASC"
                            sql_query += f" ORDER BY {field} {order}"
                    
                    # Add LIMIT
                    if limit:
                        sql_query += f" LIMIT {limit}"
                    
                    cursor = self.sqlite_conn.execute(sql_query, params)
                    rows = cursor.fetchall()
                    
                    # Convert to list of dictionaries
                    result = []
                    for row in rows:
                        result.append({
                            'timestamp': row['timestamp'],
                            'applicant_data': json.loads(row['applicant_data']),
                            'prediction': row['prediction'],
                            'probability': row['probability'],
                            'risk_level': row['risk_level']
                        })
                    
                    return result
                else:
                    raise ValueError(f"Unsupported collection/table: {collection_name}")
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            print(f"Find error: {e}")
            raise e
    
    def delete_documents(self, collection_name, query=None):
        """Delete documents from MongoDB collection or SQLite table"""
        try:
            if self.db_type == 'mongodb':
                collection = self.mongo_db[collection_name]
                mongo_query = query if query else {}
                result = collection.delete_many(mongo_query)
                return result.deleted_count
            elif self.db_type == 'sqlite':
                if collection_name == 'predictions':
                    sql_query = "DELETE FROM predictions"
                    params = []
                    
                    # Add WHERE clause if query is provided
                    if query:
                        # Simple query support - can be extended
                        pass  # For now, delete all records for SQLite
                    
                    cursor = self.sqlite_conn.execute(sql_query, params)
                    self.sqlite_conn.commit()
                    return cursor.rowcount
                else:
                    raise ValueError(f"Unsupported collection/table: {collection_name}")
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            print(f"Delete error: {e}")
            raise e
    
    def count_documents(self, collection_name, query=None):
        """Count documents in MongoDB collection or SQLite table"""
        try:
            if self.db_type == 'mongodb':
                collection = self.mongo_db[collection_name]
                mongo_query = query if query else {}
                return collection.count_documents(mongo_query)
            elif self.db_type == 'sqlite':
                if collection_name == 'predictions':
                    sql_query = "SELECT COUNT(*) FROM predictions"
                    params = []
                    
                    # Add WHERE clause if query is provided
                    if query:
                        # Simple query support - can be extended
                        pass  # For now, count all records for SQLite
                    
                    cursor = self.sqlite_conn.execute(sql_query, params)
                    result = cursor.fetchone()
                    return result[0] if result else 0
                else:
                    raise ValueError(f"Unsupported collection/table: {collection_name}")
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            print(f"Count error: {e}")
            raise e

# Create a singleton instance
db_manager = DatabaseManager()
