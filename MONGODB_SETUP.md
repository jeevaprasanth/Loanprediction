# MongoDB Database Setup for Loan AI System

This guide will help you set up MongoDB database for the Loan AI application.

## Prerequisites

1. MongoDB Server installed and running
2. Python 3.8+ installed
3. Access to MongoDB server

## Setup Instructions

### Option 1: Automatic Setup (Recommended)

1. **Install MongoDB Connector**
   ```bash
   cd c:\LoanAI
   pip install pymongo==4.6.1
   ```

2. **Run Setup Script**
   ```bash
   python mongodb_setup.py
   ```

3. **Test the Connection**
   ```bash
   python mongodb_setup.py test
   ```

4. **Create Sample Data (Optional)**
   ```bash
   python mongodb_setup.py sample
   ```

### Option 2: Manual Setup

1. **Start MongoDB Server**
   ```bash
   # Windows
   mongod.exe --dbpath "C:\data\db"
   
   # Linux/Mac
   mongod --dbpath /var/lib/mongodb
   ```

2. **Update Configuration**
   Edit `config.py` and update the MongoDB configuration:
   ```python
   MONGODB_CONFIG = {
       'host': 'localhost',
       'port': 27017,
       'database': 'loan_ai_db',
       'username': '',  # Set your MongoDB username here
       'password': '',  # Set your MongoDB password here
       'auth_source': 'admin',  # Authentication database
       'connection_string': ''  # Will be constructed automatically
   }
   ```

3. **Set Database Type**
   In `config.py`, set:
   ```python
   DATABASE_TYPE = 'mongodb'
   ```

## Configuration Options

### Database Type Selection
In `config.py`, you can choose between:
- `'mongodb'` - Use MongoDB database (recommended for production)
- `'mysql'` - Use MySQL database
- `'sqlite'` - Use SQLite database (fallback option)

### MongoDB Configuration Options
```python
MONGODB_CONFIG = {
    'host': 'localhost',          # MongoDB server host
    'port': 27017,                # MongoDB port
    'database': 'loan_ai_db',      # Database name
    'username': '',                # Username (leave empty for no auth)
    'password': '',                # Password (leave empty for no auth)
    'auth_source': 'admin',         # Authentication database
    'connection_string': ''         # Auto-constructed
}
```

### Connection String Examples

**Without Authentication:**
```
mongodb://localhost:27017/loan_ai_db
```

**With Authentication:**
```
mongodb://username:password@localhost:27017/loan_ai_db?authSource=admin
```

## Testing the Setup

1. **Test Database Connection**
   ```bash
   cd c:\LoanAI\backend
   python -c "from database_utils import db_manager; print('Database type:', db_manager.db_type); conn = db_manager.get_connection(); print('✅ Connection successful')"
   ```

2. **Run the Application**
   ```bash
   cd c:\LoanAI\backend
   python app.py
   ```

3. **Test Prediction API**
   ```bash
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
       "age": 35,
       "income": 600000,
       "loan_amount": 250000,
       "credit_score": 680,
       "employment_length": 5,
       "debt_to_income_ratio": 0.25,
       "home_ownership": "RENT",
       "loan_purpose": "debt_consolidation",
       "employment_status": "employed"
     }'
   ```

## Database Schema

MongoDB uses collections instead of tables. The application creates a `predictions` collection with the following document structure:

```json
{
    "_id": ObjectId("..."),
    "timestamp": "2024-04-06T10:30:00.000Z",
    "applicant_data": {
        "age": 35,
        "income": 600000,
        "credit_score": 680,
        "loan_amount": 250000,
        "employment_length": 5,
        "debt_to_income_ratio": 0.25,
        "home_ownership": "RENT",
        "loan_purpose": "debt_consolidation",
        "employment_status": "employed"
    },
    "prediction": 0,
    "probability": 0.246,
    "risk_level": "Low",
    "created_at": ISODate("2024-04-06T10:30:00.000Z")
}
```

## MongoDB Operations Used

### Insert Prediction
```python
document = {
    'timestamp': datetime.now().isoformat(),
    'applicant_data': applicant_data,
    'prediction': result['prediction'],
    'probability': result['probability'],
    'risk_level': result['risk_level']
}
db_manager.insert_document('predictions', document)
```

### Get Prediction History
```python
documents = db_manager.find_documents(
    collection_name='predictions',
    sort=[('timestamp', -1)],  # Sort by timestamp descending
    limit=50
)
```

### Clear History
```python
deleted_count = db_manager.delete_documents('predictions')
```

### Count Documents
```python
total_predictions = db_manager.count_documents('predictions')
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if MongoDB server is running
   - Verify port 27017 is available
   - Check firewall settings

2. **Authentication Failed**
   - Verify username and password
   - Check if authentication is enabled
   - Ensure auth_source is correct

3. **Database Not Found**
   - Create the database using setup script
   - Verify database name in configuration

4. **Permission Denied**
   - Check user permissions
   - Verify user has read/write access
   - Check if authentication is required

### MongoDB Server Commands

**Start MongoDB:**
```bash
mongod --dbpath /path/to/data
```

**Connect to MongoDB Shell:**
```bash
mongo
# or with authentication
mongo -u username -p password --authenticationDatabase admin
```

**Check MongoDB Status:**
```bash
# Check if running
netstat -an | grep 27017

# Check logs
tail -f /var/log/mongodb/mongod.log
```

## Performance Considerations

1. **Indexing**
   The application automatically creates indexes on:
   - `timestamp` (for sorting)
   - `risk_level` (for filtering)
   - `prediction` (for analytics)

2. **Connection Pooling**
   PyMongo automatically manages connection pooling
   Consider adjusting pool size for high-traffic applications

3. **Document Size**
   - Keep applicant_data reasonable in size
   - Consider using references for large datasets
   - Monitor document size limits

## Backup and Recovery

1. **Export Database**
   ```bash
   mongodump --db loan_ai_db --out backup_$(date +%Y%m%d)
   ```

2. **Import Database**
   ```bash
   mongorestore --db loan_ai_db backup_20240406
   ```

3. **Automated Backups**
   ```bash
   # Create backup script
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   mongodump --db loan_ai_db --out /backups/mongodb_backup_$DATE
   ```

## Security Considerations

1. **Enable Authentication**
   ```bash
   # Create admin user
   mongo
   use admin
   db.createUser({
     user: "admin",
     pwd: "secure_password",
     roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]
   })
   ```

2. **Network Security**
   - Bind MongoDB to localhost only for development
   - Use SSL/TLS for production environments
   - Consider VPN access for remote connections

3. **Access Control**
   - Create application-specific users
   - Limit permissions to required operations
   - Use role-based access control

## Monitoring and Maintenance

1. **Monitor Database Performance**
   ```javascript
   // MongoDB monitoring query
   db.predictions.getIndexes()
   db.predictions.stats()
   ```

2. **Log Management**
   - Monitor MongoDB logs for errors
   - Set up log rotation
   - Track connection attempts

3. **Regular Maintenance**
   - Compact database periodically
   - Rebuild indexes if needed
   - Monitor storage usage

## Migration from SQL Databases

If you have existing data in MySQL or SQLite and want to migrate to MongoDB:

1. **Export SQL Data**
   - Use existing export functionality
   - Convert to JSON format
   - Preserve data types and relationships

2. **Import to MongoDB**
   - Use mongoimport or custom script
   - Map SQL schema to MongoDB documents
   - Validate data integrity

3. **Update Application**
   - Change DATABASE_TYPE to 'mongodb'
   - Test all functionality
   - Update configuration as needed

For assistance with migration, refer to the migration guide or contact support.
