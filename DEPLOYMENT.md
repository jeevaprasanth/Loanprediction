# Loan AI System - Deployment Guide

## 🚀 Quick Deployment

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd LoanAI

# Run the deployment script
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Docker Deployment

```bash
# Build the Docker image
docker build -t loan-ai-system .

# Run the container
docker run -p 5000:5000 -d --name loan-ai loan-ai-system
```

### Option 3: Docker Compose (with MongoDB)

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🌐 Access Points

- **Main Application**: `http://localhost:5000`
- **Health Check**: `http://localhost:5000/health`
- **API Documentation**: `http://localhost:5000/api` (if available)

## 📋 Prerequisites

- Docker 20.10+
- Docker Compose 1.29+
- 2GB RAM minimum
- 1GB disk space

## 🔧 Environment Variables

Create a `.env` file for production:

```env
# Database
DATABASE_TYPE=sqlite
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=loan_ai_db
MONGODB_USERNAME=admin
MONGODB_PASSWORD=password

# Flask
SECRET_KEY=your-secret-key-here
DEBUG=False
HOST=0.0.0.0
PORT=5000

# Security
CORS_ORIGINS=*
MAX_CONTENT_LENGTH=16777216

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │   Flask API     │    │   Database      │
│                 │◄──►│                 │◄──►│                 │
│   HTML/JS/CSS   │    │   Python        │    │   SQLite/MongoDB│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Features

- ✅ **Loan Risk Assessment**: AI-powered predictions
- ✅ **Credit Score Analysis**: 300-850 range support
- ✅ **Real-time Results**: Instant predictions
- ✅ **History Tracking**: Prediction history storage
- ✅ **Health Monitoring**: Built-in health checks
- ✅ **Containerized**: Docker deployment ready
- ✅ **Scalable**: Production-ready architecture

## 🔍 Monitoring

### Health Check Endpoint

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "database": "healthy",
  "model": "loaded",
  "version": "1.0.0"
}
```

### Logs

```bash
# View application logs
docker logs loan-ai-system

# View Docker Compose logs
docker-compose logs -f
```

## 🔒 Security Considerations

- Change default passwords in production
- Use HTTPS in production environments
- Implement rate limiting
- Secure database connections
- Regular security updates

## 🚀 Cloud Deployment

### AWS ECS

1. Push Docker image to ECR
2. Create ECS task definition
3. Deploy to ECS cluster

### Google Cloud Run

1. Build and push to GCR
2. Deploy to Cloud Run
3. Configure environment variables

### Azure Container Instances

1. Push to ACR
2. Deploy to ACI
3. Configure networking

## 📞 Support

For deployment issues:
1. Check health endpoint
2. Review application logs
3. Verify database connectivity
4. Check resource usage

## 🔄 Updates

To update the application:

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```
