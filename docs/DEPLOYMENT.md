# Deployment Guide

This guide covers deploying the News MCP Server to various cloud platforms for production use.

## Deployment Options

1. [Railway](#railway-recommended)
2. [Render](#render)
3. [Fly.io](#flyio)
4. [AWS EC2](#aws-ec2)
5. [Google Cloud Run](#google-cloud-run)
6. [Docker](#docker-deployment)

## Prerequisites

- MongoDB Atlas account with cluster created
- GitHub account with your repository
- Cloud platform account

## Railway (Recommended)

### Why Railway?
- Simple deployment from GitHub
- Free tier available
- Automatic HTTPS
- Easy environment variable management

### Steps

1. **Sign Up**
   - Go to [Railway.app](https://railway.app/)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `chatgpt-mcp-news-widget`

3. **Configure Build**
   - Railway auto-detects Python
   - No additional configuration needed

4. **Set Environment Variables**
   - Click on your service
   - Go to "Variables" tab
   - Add:
     ```
     MONGODB_URI=your_mongodb_atlas_uri
     MONGODB_DATABASE=news_db
     MONGODB_COLLECTION=articles
     MCP_SERVER_PORT=3000
     LOG_LEVEL=INFO
     ENVIRONMENT=production
     ```

5. **Deploy**
   - Railway automatically deploys
   - Get your deployment URL from the "Deployments" tab
   - Example: `https://your-app.railway.app`

6. **Update OpenAI App**
   - Update `app_manifest.json` with your Railway URL
   - Redeploy the OpenAI app configuration

### Railway Configuration File

Create `railway.toml` in project root:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python src/mcp_server.py"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

## Render

### Steps

1. **Sign Up**
   - Go to [Render.com](https://render.com/)
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Select `chatgpt-mcp-news-widget`

3. **Configure Service**
   - Name: `news-mcp-server`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python src/mcp_server.py`

4. **Environment Variables**
   - Add the same variables as Railway

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your URL: `https://news-mcp-server.onrender.com`

## Fly.io

### Steps

1. **Install Flyctl**
   ```bash
   # Mac/Linux
   curl -L https://fly.io/install.sh | sh

   # Windows
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login**
   ```bash
   flyctl auth login
   ```

3. **Create App**
   ```bash
   flyctl launch
   ```

4. **Configure fly.toml**
   ```toml
   app = "news-mcp-server"
   primary_region = "iad"

   [build]

   [http_service]
     internal_port = 3000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0

   [[vm]]
     cpu_kind = "shared"
     cpus = 1
     memory_mb = 256
   ```

5. **Set Secrets**
   ```bash
   flyctl secrets set MONGODB_URI="your_uri"
   flyctl secrets set MONGODB_DATABASE="news_db"
   flyctl secrets set MONGODB_COLLECTION="articles"
   ```

6. **Deploy**
   ```bash
   flyctl deploy
   ```

## AWS EC2

### Steps

1. **Launch EC2 Instance**
   - Choose Ubuntu 22.04 LTS
   - t2.micro (free tier)
   - Configure security group: Allow ports 22, 80, 443, 3000

2. **Connect via SSH**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3.10 python3-pip git -y
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/vikkysarswat/chatgpt-mcp-news-widget.git
   cd chatgpt-mcp-news-widget
   ```

5. **Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure .env**
   ```bash
   nano .env
   # Add your environment variables
   ```

7. **Run with systemd**
   Create `/etc/systemd/system/mcp-server.service`:
   ```ini
   [Unit]
   Description=MCP News Server
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/chatgpt-mcp-news-widget
   Environment="PATH=/home/ubuntu/chatgpt-mcp-news-widget/venv/bin"
   ExecStart=/home/ubuntu/chatgpt-mcp-news-widget/venv/bin/python src/mcp_server.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

8. **Start Service**
   ```bash
   sudo systemctl enable mcp-server
   sudo systemctl start mcp-server
   sudo systemctl status mcp-server
   ```

## Google Cloud Run

### Steps

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   CMD ["python", "src/mcp_server.py"]
   ```

2. **Build and Push**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/news-mcp-server
   ```

3. **Deploy**
   ```bash
   gcloud run deploy news-mcp-server \
     --image gcr.io/YOUR_PROJECT/news-mcp-server \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **Set Environment Variables**
   ```bash
   gcloud run services update news-mcp-server \
     --set-env-vars MONGODB_URI=your_uri,MONGODB_DATABASE=news_db
   ```

## Docker Deployment

### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 3000

# Run server
CMD ["python", "src/mcp_server.py"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    ports:
      - "3000:3000"
    environment:
      - MONGODB_URI=${MONGODB_URI}
      - MONGODB_DATABASE=${MONGODB_DATABASE}
      - MONGODB_COLLECTION=${MONGODB_COLLECTION}
      - MCP_SERVER_PORT=3000
      - LOG_LEVEL=INFO
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t news-mcp-server .

# Run container
docker run -d \
  -p 3000:3000 \
  -e MONGODB_URI="your_uri" \
  -e MONGODB_DATABASE="news_db" \
  -e MONGODB_COLLECTION="articles" \
  --name mcp-server \
  news-mcp-server

# Or use docker-compose
docker-compose up -d
```

## Post-Deployment

### 1. Seed Database

After deployment, seed the production database:

```bash
# Locally, with production MongoDB URI in .env
python scripts/seed_mongodb.py
```

### 2. Test Deployment

```bash
curl https://your-deployment-url.com/health
```

### 3. Update OpenAI App

Update `openai_app/app_manifest.json`:

```json
{
  "api": {
    "url": "https://your-deployment-url.com"
  }
}
```

Reupload to OpenAI Platform.

### 4. Monitor

- Check logs regularly
- Set up uptime monitoring (e.g., UptimeRobot)
- Monitor MongoDB Atlas metrics

## Security Best Practices

1. **Environment Variables**: Never commit `.env` to Git
2. **MongoDB**: Use strong passwords and IP whitelisting
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Monitoring**: Set up error tracking (e.g., Sentry)

## Scaling Considerations

### Horizontal Scaling
- Deploy multiple instances behind a load balancer
- Use Redis for caching frequently accessed news

### Database Optimization
- Create appropriate indexes
- Use MongoDB connection pooling
- Implement caching layer

### CDN
- Use CDN for static assets and images
- Cache API responses when appropriate

## Troubleshooting Deployment

### Server Not Starting
- Check logs: `flyctl logs` or platform-specific command
- Verify environment variables are set
- Check MongoDB connection

### High Memory Usage
- Reduce connection pool size
- Implement pagination for large result sets
- Add memory limits in deployment config

### Slow Response Times
- Add database indexes
- Implement caching
- Optimize MongoDB queries
- Use connection pooling

## Cost Optimization

- Use free tiers when possible
- Scale down during low-traffic periods
- Optimize database queries to reduce reads
- Use MongoDB Atlas free tier (M0) for development

## Backup and Recovery

- Enable MongoDB Atlas automated backups
- Export critical configuration files
- Document deployment process
- Keep deployment scripts in version control