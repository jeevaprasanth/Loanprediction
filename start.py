#!/usr/bin/env python3
"""
Production startup script for Loan AI System
"""

import os
import sys
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the application
from backend.app import app

# Configure for production
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

if __name__ == '__main__':
    # Production configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes']
    
    print(f"🚀 Starting Loan AI System on {host}:{port}")
    print(f"🌐 Access the application at: http://{host}:{port}")
    print(f"📊 Health check available at: http://{host}:{port}/health")
    
    app.run(host=host, port=port, debug=debug)
