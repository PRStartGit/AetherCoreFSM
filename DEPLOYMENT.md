# Zynthio - Digital Ocean Deployment Guide

This guide will walk you through deploying Zynthio to Digital Ocean using Docker.

## Prerequisites

- Digital Ocean account
- Domain name registered and configured
- Docker and Docker Compose installed locally (for testing)
- Git repository access

## Architecture Overview

The application consists of 5 Docker containers:

1. **Frontend** (nginx) - Serves the Angular application
2. **Backend** (FastAPI) - REST API server
3. **Database** (PostgreSQL) - Primary data store
4. **Redis** - Cache and message broker
5. **Celery Worker** - Background task processor

## Pre-Deployment Checklist

### 1. Digital Ocean Setup

1. Create a Droplet (recommended: 4GB RAM, 2 vCPUs)
2. Choose Ubuntu 22.04 LTS
3. Enable monitoring and backups
4. Add your SSH key

### 2. Domain Configuration

1. Point your domain to your droplet's IP address
2. Add DNS A record: `@` → `your-droplet-ip`
3. Add DNS A record: `www` → `your-droplet-ip`

### 3. Email Configuration (SMTP)

Choose one of these options:

#### Option A: Gmail SMTP (Free)
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use these settings:
   - `SMTP_HOST=smtp.gmail.com`
   - `SMTP_PORT=587`
   - `SMTP_USER=your-email@gmail.com`
   - `SMTP_PASSWORD=your-app-password`

#### Option B: Office 365 SMTP
- `SMTP_HOST=smtp.office365.com`
- `SMTP_PORT=587`
- `SMTP_USER=your-email@yourdomain.com`
- `SMTP_PASSWORD=your-password`

#### Option C: Custom Domain SMTP
Contact your domain/hosting provider for SMTP details.

## Deployment Steps

### Step 1: Connect to Your Droplet

```bash
ssh root@your-droplet-ip
```

### Step 2: Install Docker

```bash
# Update system
apt-get update && apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt-get install docker-compose -y

# Start Docker
systemctl start docker
systemctl enable docker
```

### Step 3: Clone Repository

```bash
# Install Git if not present
apt-get install git -y

# Clone your repository
cd /opt
git clone https://github.com/your-username/AetherCoreFSM.git
cd AetherCoreFSM
```

### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit environment file
nano .env
```

Fill in these required values:

```env
# Domain
DOMAIN=your-domain.com

# Database (use strong passwords!)
POSTGRES_DB=zynthio
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password-here

# Security (generate with: openssl rand -hex 32)
SECRET_KEY=your-random-secret-key-here

# SMTP Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_TLS=True

# Email Settings
FROM_EMAIL=noreply@your-domain.com
FROM_NAME=Zynthio Site Monitoring
```

**Important**: Generate a secure SECRET_KEY:
```bash
openssl rand -hex 32
```

### Step 5: Build and Start Services

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 6: Initialize Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Create first super admin (optional)
docker-compose exec backend python -c "
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
db = SessionLocal()
admin = User(
    email='admin@your-domain.com',
    full_name='Super Admin',
    hashed_password=get_password_hash('changeme123'),
    role='super_admin',
    is_active=True
)
db.add(admin)
db.commit()
print('Admin user created: admin@your-domain.com / changeme123')
"
```

### Step 7: Configure SSL (HTTPS)

```bash
# Install Certbot
apt-get install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal is configured automatically
certbot renew --dry-run
```

## Post-Deployment

### Verify Services

```bash
# Check all containers are running
docker-compose ps

# Check backend health
curl http://localhost:8000/api/v1/health

# Check frontend
curl http://localhost/

# Test database connection
docker-compose exec backend python -c "
from app.core.database import engine
with engine.connect() as conn:
    print('Database connection successful!')
"
```

### Test Email Sending

```bash
docker-compose exec backend python -c "
from app.core.email import email_service
result = email_service.send_email_smtp(
    to_email='your-test-email@gmail.com',
    subject='Test Email',
    html_content='<h1>Email works!</h1>'
)
print('Email sent!' if result else 'Email failed!')
"
```

## Maintenance

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d

# Run new migrations
docker-compose exec backend alembic upgrade head
```

### Backup Database

```bash
# Create backup
docker-compose exec database pg_dump -U postgres zynthio > backup_$(date +%Y%m%d).sql

# Restore backup
docker-compose exec -T database psql -U postgres zynthio < backup_20240101.sql
```

## Monitoring

### Check Resource Usage

```bash
# Container stats
docker stats

# Disk usage
df -h

# Memory usage
free -m
```

### Setup Automated Backups

```bash
# Create backup script
cat > /opt/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/opt/backups
mkdir -p $BACKUP_DIR

# Database backup
docker-compose -f /opt/AetherCoreFSM/docker-compose.yml exec -T database pg_dump -U postgres zynthio > $BACKUP_DIR/db_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete

echo "Backup completed: db_$DATE.sql"
EOF

chmod +x /opt/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/backup.sh") | crontab -
```

## Troubleshooting

### Backend not starting

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Database not ready - wait a few seconds
# 2. Environment variables missing - check .env
# 3. Port already in use - check with: netstat -tulpn | grep 8000
```

### Frontend not accessible

```bash
# Check nginx logs
docker-compose logs frontend

# Verify nginx config
docker-compose exec frontend nginx -t

# Common issues:
# 1. Port 80 already in use
# 2. SSL certificate issues
```

### Email not sending

```bash
# Test SMTP connection
docker-compose exec backend python -c "
import smtplib
from app.core.config import settings
try:
    server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
    server.starttls()
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    server.quit()
    print('SMTP connection successful!')
except Exception as e:
    print(f'SMTP error: {e}')
"
```

### Database connection issues

```bash
# Check database logs
docker-compose logs database

# Test connection
docker-compose exec database psql -U postgres -d zynthio -c "SELECT 1;"
```

## Security Recommendations

1. **Change default passwords** immediately after deployment
2. **Enable firewall**:
   ```bash
   ufw allow OpenSSH
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable
   ```
3. **Regular updates**:
   ```bash
   apt-get update && apt-get upgrade -y
   ```
4. **Monitor logs** for suspicious activity
5. **Enable 2FA** for admin accounts
6. **Regular backups** - test restore process

## Performance Optimization

### Increase Worker Processes

Edit `docker-compose.yml`:
```yaml
backend:
  command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 8
```

### Add Redis Caching

Already configured in docker-compose.yml and ready to use.

### Database Optimization

```bash
# Connect to database
docker-compose exec database psql -U postgres -d zynthio

# Add indexes for common queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_sites_org_id ON sites(organization_id);
CREATE INDEX idx_tasks_site_id ON tasks(site_id);
```

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Review configuration: `cat .env`
- Verify services: `docker-compose ps`
- Contact support: support@zynthio.com

## Quick Reference

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart service
docker-compose restart backend

# Run migrations
docker-compose exec backend alembic upgrade head

# Database backup
docker-compose exec database pg_dump -U postgres zynthio > backup.sql

# Update code
git pull && docker-compose up -d --build
```

## Cost Optimization

**Digital Ocean Droplet**: $24/month (4GB RAM)
**Managed PostgreSQL** (optional): $15/month (1GB)
**Domain**: $10-15/year
**Email**: Free (SMTP with Gmail/Office365)

**Total**: ~$24-39/month
