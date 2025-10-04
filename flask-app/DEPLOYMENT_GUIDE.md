# Production Deployment Guide

## Overview

This guide covers deploying the Flask blog application to production with proper security, performance, and monitoring.

---

## Prerequisites

- Python 3.11+
- PostgreSQL (recommended) or SQLite
- Nginx or Apache (web server)
- SSL certificate (Let's Encrypt recommended)
- Domain name
- Server with at least 1GB RAM

---

## 1. Server Setup

### A. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### B. Install Dependencies
```bash
# Python and pip
sudo apt install python3.11 python3.11-venv python3-pip -y

# PostgreSQL (recommended)
sudo apt install postgresql postgresql-contrib -y

# Nginx
sudo apt install nginx -y

# Supervisor (process manager)
sudo apt install supervisor -y

# Certbot (SSL)
sudo apt install certbot python3-certbot-nginx -y
```

---

## 2. Application Setup

### A. Create Application User
```bash
sudo useradd -m -s /bin/bash flaskapp
sudo su - flaskapp
```

### B. Clone Repository
```bash
cd /home/flaskapp
git clone https://github.com/Napier40/Akademia-Studenta.git
cd Akademia-Studenta/flask-app
```

### C. Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### D. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

---

## 3. Database Setup

### A. PostgreSQL (Recommended)

#### Create Database:
```bash
sudo -u postgres psql

CREATE DATABASE flask_blog;
CREATE USER flaskapp WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE flask_blog TO flaskapp;
\q
```

#### Update Connection String:
```bash
# In .env file
DATABASE_URL=postgresql://flaskapp:your-secure-password@localhost/flask_blog
```

### B. SQLite (Development Only)
```bash
# Already configured by default
# Database will be created at instance/website.db
```

### C. Initialize Database
```bash
python init_db.py
```

---

## 4. Environment Configuration

### A. Create Production .env File
```bash
cat > .env << EOF
# Flask Configuration
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
FLASK_ENV=production
FLASK_APP=app.py

# Database
DATABASE_URL=postgresql://flaskapp:your-password@localhost/flask_blog

# Translation API
DEEPL_API_KEY=your-deepl-api-key
ENABLE_AUTO_TRANSLATION=True

# Logging
LOG_LEVEL=INFO

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
EOF
```

### B. Set Permissions
```bash
chmod 600 .env
```

---

## 5. Gunicorn Configuration

### A. Create Gunicorn Config
```bash
cat > gunicorn_config.py << EOF
import multiprocessing

# Server socket
bind = "127.0.0.1:5001"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/home/flaskapp/Akademia-Studenta/flask-app/logs/gunicorn-access.log"
errorlog = "/home/flaskapp/Akademia-Studenta/flask-app/logs/gunicorn-error.log"
loglevel = "info"

# Process naming
proc_name = "flask_blog"

# Server mechanics
daemon = False
pidfile = "/home/flaskapp/Akademia-Studenta/flask-app/gunicorn.pid"
user = "flaskapp"
group = "flaskapp"
umask = 0o007

# SSL (if terminating SSL at Gunicorn)
# keyfile = "/path/to/key.pem"
# certfile = "/path/to/cert.pem"
EOF
```

### B. Create Logs Directory
```bash
mkdir -p logs
```

---

## 6. Supervisor Configuration

### A. Create Supervisor Config
```bash
sudo cat > /etc/supervisor/conf.d/flask_blog.conf << EOF
[program:flask_blog]
command=/home/flaskapp/Akademia-Studenta/flask-app/venv/bin/gunicorn -c gunicorn_config.py app:app
directory=/home/flaskapp/Akademia-Studenta/flask-app
user=flaskapp
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/flask_blog.err.log
stdout_logfile=/var/log/flask_blog.out.log
environment=PATH="/home/flaskapp/Akademia-Studenta/flask-app/venv/bin"
EOF
```

### B. Start Application
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start flask_blog
```

### C. Check Status
```bash
sudo supervisorctl status flask_blog
```

---

## 7. Nginx Configuration

### A. Create Nginx Config
```bash
sudo cat > /etc/nginx/sites-available/flask_blog << 'EOF'
# Rate limiting
limit_req_zone $binary_remote_addr zone=flask_limit:10m rate=10r/s;

# Upstream
upstream flask_blog {
    server 127.0.0.1:5001 fail_timeout=0;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/flask_blog_access.log;
    error_log /var/log/nginx/flask_blog_error.log;

    # Max upload size
    client_max_body_size 10M;

    # Static files
    location /static {
        alias /home/flaskapp/Akademia-Studenta/flask-app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Application
    location / {
        # Rate limiting
        limit_req zone=flask_limit burst=20 nodelay;

        # Proxy settings
        proxy_pass http://flask_blog;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF
```

### B. Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/flask_blog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 8. SSL Certificate

### A. Obtain Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### B. Auto-renewal
```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot automatically sets up cron job
```

---

## 9. Firewall Configuration

### A. UFW Setup
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
sudo ufw status
```

---

## 10. Monitoring & Logging

### A. Application Logs
```bash
# View application logs
tail -f /home/flaskapp/Akademia-Studenta/flask-app/logs/app.log

# View Gunicorn logs
tail -f /home/flaskapp/Akademia-Studenta/flask-app/logs/gunicorn-access.log
tail -f /home/flaskapp/Akademia-Studenta/flask-app/logs/gunicorn-error.log

# View Supervisor logs
tail -f /var/log/flask_blog.out.log
tail -f /var/log/flask_blog.err.log

# View Nginx logs
tail -f /var/log/nginx/flask_blog_access.log
tail -f /var/log/nginx/flask_blog_error.log
```

### B. Log Rotation
```bash
sudo cat > /etc/logrotate.d/flask_blog << EOF
/home/flaskapp/Akademia-Studenta/flask-app/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 flaskapp flaskapp
    sharedscripts
    postrotate
        supervisorctl restart flask_blog > /dev/null
    endscript
}
EOF
```

---

## 11. Backup Strategy

### A. Database Backup Script
```bash
cat > /home/flaskapp/backup_db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/flaskapp/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump -U flaskapp flask_blog > $BACKUP_DIR/db_backup_$DATE.sql

# Compress
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: db_backup_$DATE.sql.gz"
EOF

chmod +x /home/flaskapp/backup_db.sh
```

### B. Schedule Backups
```bash
# Add to crontab
crontab -e

# Add this line (daily at 2 AM)
0 2 * * * /home/flaskapp/backup_db.sh >> /home/flaskapp/backup.log 2>&1
```

---

## 12. Performance Optimization

### A. Enable Gzip Compression (Nginx)
```nginx
# Add to nginx config
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
```

### B. Enable Caching
```bash
# Install Redis
sudo apt install redis-server -y

# Update .env
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379/0
```

---

## 13. Security Checklist

- [x] SSL certificate installed
- [x] Firewall configured
- [x] Strong SECRET_KEY
- [x] Database password secured
- [x] .env file permissions (600)
- [x] Rate limiting enabled
- [x] Security headers configured
- [x] Regular backups scheduled
- [x] Log rotation configured
- [x] Non-root user for application
- [x] CSRF protection enabled
- [x] SQL injection prevention (ORM)
- [x] XSS protection (auto-escaping)

---

## 14. Deployment Checklist

### Pre-Deployment:
- [ ] Run tests: `pytest`
- [ ] Check code quality: `flake8 .`
- [ ] Update dependencies: `pip list --outdated`
- [ ] Review security settings
- [ ] Backup current production

### Deployment:
- [ ] Pull latest code: `git pull origin main`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run migrations (if any)
- [ ] Restart application: `sudo supervisorctl restart flask_blog`
- [ ] Check logs for errors
- [ ] Test critical functionality

### Post-Deployment:
- [ ] Monitor logs for 1 hour
- [ ] Check error rates
- [ ] Verify SSL certificate
- [ ] Test from different locations
- [ ] Update documentation

---

## 15. Troubleshooting

### Application Won't Start
```bash
# Check supervisor status
sudo supervisorctl status flask_blog

# Check logs
tail -f /var/log/flask_blog.err.log

# Check Gunicorn
ps aux | grep gunicorn

# Restart
sudo supervisorctl restart flask_blog
```

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -U flaskapp -d flask_blog -h localhost

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Check PostgreSQL status
sudo systemctl status postgresql
```

### Nginx Issues
```bash
# Test configuration
sudo nginx -t

# Check logs
tail -f /var/log/nginx/error.log

# Restart
sudo systemctl restart nginx
```

### SSL Certificate Issues
```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew

# Check Nginx SSL config
sudo nginx -t
```

---

## 16. Maintenance Tasks

### Daily:
- Monitor error logs
- Check application status
- Review access logs

### Weekly:
- Review security logs
- Check disk space
- Update dependencies (if needed)
- Review performance metrics

### Monthly:
- Security audit
- Performance optimization
- Backup verification
- SSL certificate check

---

## 17. Rollback Procedure

### If Deployment Fails:
```bash
# 1. Stop application
sudo supervisorctl stop flask_blog

# 2. Revert code
git reset --hard HEAD~1

# 3. Restore database (if needed)
gunzip -c /home/flaskapp/backups/db_backup_YYYYMMDD_HHMMSS.sql.gz | psql -U flaskapp flask_blog

# 4. Restart application
sudo supervisorctl start flask_blog

# 5. Verify
curl https://your-domain.com
```

---

## 18. Support & Resources

### Documentation:
- Application docs in repository
- Flask documentation: https://flask.palletsprojects.com/
- Nginx documentation: https://nginx.org/en/docs/
- Gunicorn documentation: https://docs.gunicorn.org/

### Monitoring:
- Application logs: `/home/flaskapp/Akademia-Studenta/flask-app/logs/`
- System logs: `/var/log/`
- Supervisor: `sudo supervisorctl status`

---

**Deployment Complete!** 🚀

Your Flask blog application is now running in production with:
- ✅ SSL encryption
- ✅ Rate limiting
- ✅ Security headers
- ✅ Automated backups
- ✅ Log rotation
- ✅ Process management
- ✅ Performance optimization

**Next Steps:**
1. Monitor logs for 24 hours
2. Set up uptime monitoring
3. Configure email alerts
4. Plan regular maintenance