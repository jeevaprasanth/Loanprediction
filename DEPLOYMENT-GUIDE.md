# 🚀 Loan AI System - Deployment Guide

## 📋 Prerequisites

- Python 3.9+ installed
- Internet connection
- 2GB+ RAM
- 1GB+ disk space

## 🌐 Deployment Options

### Option 1: Local Development (Easiest)

```bash
# Navigate to backend directory
cd c:\LoanAI\backend

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

**Access**: http://localhost:5000

### Option 2: Production Server Setup

#### Step 1: Prepare Production Environment

```bash
# Install production dependencies
pip install gunicorn flask-cors

# Create production config
cp config.py production_config.py
```

#### Step 2: Configure Production Settings

Edit `production_config.py`:
```python
# Production settings
DEBUG = False
HOST = '0.0.0.0'  # Allow external access
PORT = 5000
SECRET_KEY = 'your-secret-key-here'
```

#### Step 3: Start Production Server

```bash
# Using Gunicorn (recommended for production)
cd c:\LoanAI\backend
gunicorn --bind 0.0.0.0:5000 app:app

# Or using Flask directly
python app.py
```

### Option 3: Cloud Deployment

#### A. Heroku (Free Tier)

1. **Install Heroku CLI**
2. **Create Heroku App**
```bash
heroku create your-app-name
```

3. **Create Procfile**
```bash
echo "web: gunicorn app:app" > Procfile
```

4. **Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### B. PythonAnywhere (Free)

1. **Sign up at pythonanywhere.com**
2. **Upload your project files**
3. **Configure web app**
4. **Install requirements**
5. **Set up WSGI file**

#### C. Vercel (Serverless)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Create vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend/app.py"
    }
  ]
}
```

3. **Deploy**
```bash
vercel --prod
```

### Option 4: Windows Service

#### Step 1: Create Service Script

Create `service.py`:
```python
import os
import sys
import time
from backend.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

#### Step 2: Install as Windows Service

```bash
# Install NSSM (Non-Sucking Service Manager)
# Download from: https://nssm.cc/download

# Install service
nssm install LoanAI "python" "c:\LoanAI\service.py"

# Start service
nssm start LoanAI
```

### Option 5: Docker (When Available)

```bash
# Build Docker image
docker build -t loan-ai-system .

# Run container
docker run -p 5000:5000 -d --name loan-ai loan-ai-system
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_TYPE=sqlite
HOST=0.0.0.0
PORT=5000
```

### Security Settings

```python
# In production_config.py
SECRET_KEY = 'your-very-secure-secret-key'
DEBUG = False
CORS_ORIGINS = ['https://yourdomain.com']
```

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:5000/health
```

### Logs

```bash
# View application logs
tail -f app.log

# Windows Event Viewer (for Windows Service)
```

## 🌍 Making Publicly Accessible

### Option 1: Port Forwarding (Router)

1. **Find your public IP**: https://whatismyipaddress.com
2. **Configure router**: Forward port 5000 to your computer
3. **Access**: `http://YOUR_PUBLIC_IP:5000`

### Option 2: Cloudflare Tunnel (Free)

1. **Install Cloudflared**
2. **Create tunnel**
```bash
cloudflared tunnel create loan-ai
cloudflared tunnel route dns loan-ai yourdomain.com
```

3. **Run tunnel**
```bash
cloudflared tunnel run loan-ai
```

### Option 3: Ngrok (Temporary)

```bash
# Install ngrok
# Download from: https://ngrok.com/download

# Start tunnel
ngrok http 5000
```

## 📱 Mobile Access

### QR Code for Easy Access

1. **Generate QR code**: Use online QR code generator
2. **URL**: `http://YOUR_IP:5000`
3. **Share**: Users can scan QR code to access

## 🔍 Testing Deployment

### Checklist

- [ ] Application starts without errors
- [ ] Health check returns 200 OK
- [ ] Prediction endpoint works
- [ ] History endpoint works
- [ ] Static files load correctly
- [ ] Database connections work

### Test Commands

```bash
# Test health
curl http://localhost:5000/health

# Test prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "income": 50000, "credit_score": 700, "loan_amount": 10000, "employment_length": 5, "debt_to_income_ratio": 0.3, "home_ownership": "RENT", "loan_purpose": "debt_consolidation", "employment_status": "employed", "applicant_name": "Test"}'
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

2. **Module not found**
```bash
# Install missing dependencies
pip install -r requirements.txt
```

3. **Database connection error**
```bash
# Check database file exists
ls predictions.db

# Recreate database
python clear_history.py
```

4. **Permission denied**
```bash
# Run as administrator
# Or change folder permissions
```

## 📞 Support

### Quick Help

1. **Check logs**: Look for error messages
2. **Test locally**: Ensure app works on localhost first
3. **Check firewall**: Allow port 5000
4. **Verify dependencies**: All packages installed

### Contact

- **Documentation**: Check `DEPLOYMENT.md`
- **Issues**: Create GitHub issue
- **Community**: Stack Overflow tag `loan-ai-system`

---

## 🎯 Recommended Deployment Path

### For Beginners:
1. **Local Development** → Test functionality
2. **Ngrok** → Share with others
3. **PythonAnywhere** → Free hosting

### For Production:
1. **Production Server** → VPS or dedicated
2. **Cloudflare Tunnel** → Secure access
3. **Domain Setup** → Professional appearance

Choose the option that best fits your needs and technical comfort level!
