"""
Web-based Database Viewer for Loan AI System
View MongoDB database contents in your browser
"""

from flask import Flask, render_template_string, jsonify
import pymongo
from config import MONGODB_CONFIG
from datetime import datetime

app = Flask(__name__)

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
        return client, db
        
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None, None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loan AI Database Viewer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background-color: #f8f9fa; }
        .navbar { background-color: #343a40 !important; }
        .card { border: none; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .risk-low { color: #28a745; }
        .risk-medium { color: #ffc107; }
        .risk-high { color: #dc3545; }
        .stats-card { transition: transform 0.2s; }
        .stats-card:hover { transform: translateY(-5px); }
        .table-responsive { max-height: 400px; overflow-y: auto; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="#">
                <i class="fas fa-database me-2"></i>Loan AI Database Viewer
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        {% if error %}
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>
            {{ error }}
            <hr>
            <small><strong>Solution:</strong> Start MongoDB server with:<br>
            <code>mongod.exe --dbpath "C:\data\db"</code></small>
        </div>
        {% else %}
        <!-- Statistics Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card stats-card bg-primary text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h4 class="card-title">{{ stats.total_predictions }}</h4>
                                <p class="card-text">Total Predictions</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-chart-line fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card bg-success text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h4 class="card-title">{{ stats.low_risk_count }}</h4>
                                <p class="card-text">Low Risk</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-shield-alt fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card bg-warning text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h4 class="card-title">{{ stats.medium_risk_count }}</h4>
                                <p class="card-text">Medium Risk</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-exclamation-triangle fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card bg-danger text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h4 class="card-title">{{ stats.high_risk_count }}</h4>
                                <p class="card-text">High Risk</p>
                            </div>
                            <div class="align-self-center">
                                <i class="fas fa-times-circle fa-2x"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Risk Distribution Chart -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-pie me-2"></i>Risk Level Distribution</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="riskChart" width="400" height="200"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-bar me-2"></i>Prediction Outcomes</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="outcomeChart" width="400" height="200"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- Recent Predictions Table -->
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-history me-2"></i>Recent Predictions</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Age</th>
                                <th>Income</th>
                                <th>Credit Score</th>
                                <th>Prediction</th>
                                <th>Probability</th>
                                <th>Risk Level</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for prediction in recent_predictions %}
                            <tr>
                                <td>{{ prediction.timestamp }}</td>
                                <td>{{ prediction.applicant_data.age }}</td>
                                <td>{{ "{:,}".format(prediction.applicant_data.income) }}</td>
                                <td>{{ prediction.applicant_data.credit_score }}</td>
                                <td>
                                    {% if prediction.prediction == 1 %}
                                        <span class="badge bg-danger">Will Default</span>
                                    {% else %}
                                        <span class="badge bg-success">Will Not Default</span>
                                    {% endif %}
                                </td>
                                <td>{{ "%.3f"|format(prediction.probability) }}</td>
                                <td>
                                    <span class="risk-{{ prediction.risk_level.lower() }}">
                                        {{ prediction.risk_level }}
                                    </span>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    {% if not error %}
    <script>
        // Risk Distribution Chart
        const riskCtx = document.getElementById('riskChart').getContext('2d');
        new Chart(riskCtx, {
            type: 'doughnut',
            data: {
                labels: {{ risk_labels|tojson }},
                datasets: [{
                    data: {{ risk_data|tojson }},
                    backgroundColor: ['#28a745', '#ffc107', '#dc3545']
                }]
            }
        });

        // Prediction Outcomes Chart
        const outcomeCtx = document.getElementById('outcomeChart').getContext('2d');
        new Chart(outcomeCtx, {
            type: 'bar',
            data: {
                labels: {{ outcome_labels|tojson }},
                datasets: [{
                    label: 'Count',
                    data: {{ outcome_data|tojson }},
                    backgroundColor: ['#28a745', '#dc3545']
                }]
            }
        });
    </script>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def database_viewer():
    """Main database viewer page"""
    client, db = connect_to_mongodb()
    
    if not db:
        return render_template_string(HTML_TEMPLATE, 
            error="Cannot connect to MongoDB. Make sure MongoDB server is running.")
    
    try:
        predictions_collection = db['predictions']
        
        # Get statistics
        total_count = predictions_collection.count_documents({})
        
        # Risk distribution
        risk_pipeline = [
            {"$group": {"_id": "$risk_level", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        risk_distribution = list(predictions_collection.aggregate(risk_pipeline))
        
        # Prediction outcomes
        outcome_pipeline = [
            {"$group": {"_id": "$prediction", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        prediction_outcomes = list(predictions_collection.aggregate(outcome_pipeline))
        
        # Recent predictions
        recent = list(predictions_collection.find().sort("timestamp", -1).limit(10))
        
        # Prepare statistics
        stats = {
            'total_predictions': total_count,
            'low_risk_count': 0,
            'medium_risk_count': 0,
            'high_risk_count': 0
        }
        
        for item in risk_distribution:
            risk_level = item['_id'].lower()
            count = item['count']
            if 'low' in risk_level:
                stats['low_risk_count'] = count
            elif 'medium' in risk_level:
                stats['medium_risk_count'] = count
            elif 'high' in risk_level:
                stats['high_risk_count'] = count
        
        # Prepare chart data
        risk_labels = [item['_id'] for item in risk_distribution]
        risk_data = [item['count'] for item in risk_distribution]
        
        outcome_labels = ['Will Not Default', 'Will Default']
        outcome_data = [0, 0]
        for item in prediction_outcomes:
            if item['_id'] == 0:
                outcome_data[0] = item['count']
            else:
                outcome_data[1] = item['count']
        
        return render_template_string(HTML_TEMPLATE,
            stats=stats,
            recent_predictions=recent,
            risk_labels=risk_labels,
            risk_data=risk_data,
            outcome_labels=outcome_labels,
            outcome_data=outcome_data,
            error=None
        )
        
    except Exception as e:
        return render_template_string(HTML_TEMPLATE, 
            error=f"Error accessing database: {str(e)}")
    
    finally:
        if client:
            client.close()

@app.route('/api/stats')
def api_stats():
    """API endpoint for database statistics"""
    client, db = connect_to_mongodb()
    
    if not db:
        return jsonify({'error': 'Cannot connect to MongoDB'})
    
    try:
        predictions_collection = db['predictions']
        
        stats = {
            'total_predictions': predictions_collection.count_documents({}),
            'last_updated': datetime.now().isoformat()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)})
    
    finally:
        if client:
            client.close()

if __name__ == '__main__':
    print("🌐 Starting Database Viewer Web Interface...")
    print("📊 Open http://localhost:5001 in your browser")
    app.run(host='0.0.0.0', port=5001, debug=True)
