# SmartSpec Autopilot - Admin Guide

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Audience:** System Administrators

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [User Management](#user-management)
5. [Monitoring](#monitoring)
6. [Backup & Recovery](#backup--recovery)
7. [Security](#security)
8. [Troubleshooting](#troubleshooting)
9. [Maintenance](#maintenance)

---

## 🎯 Introduction

This guide covers system administration tasks for SmartSpec Autopilot.

**Responsibilities:**
- System installation and configuration
- User and access management
- System monitoring and maintenance
- Backup and disaster recovery
- Security and compliance
- Performance optimization

---

## 🔧 Installation

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8 GB
- Storage: 50 GB SSD
- OS: Ubuntu 22.04 LTS

**Recommended:**
- CPU: 8 cores
- RAM: 16 GB
- Storage: 100 GB SSD
- OS: Ubuntu 22.04 LTS

### Installation Steps

#### 1. Prepare Environment

```bash
# Create user
sudo useradd -m -s /bin/bash smartspec

# Create directories
sudo mkdir -p /opt/smartspec
sudo mkdir -p /var/lib/smartspec/checkpoints
sudo mkdir -p /var/log/smartspec
sudo chown -R smartspec:smartspec /opt/smartspec /var/lib/smartspec /var/log/smartspec
```

#### 2. Install Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3.11
sudo apt-get install -y python3.11 python3-pip

# Install PostgreSQL
sudo apt-get install -y postgresql-14

# Install Redis
sudo apt-get install -y redis-server

# Install Nginx
sudo apt-get install -y nginx
```

#### 3. Clone Repository

```bash
# Clone
sudo -u smartspec git clone https://github.com/naibarn/SmartSpec.git /opt/smartspec
cd /opt/smartspec

# Create virtual environment
sudo -u smartspec python3.11 -m venv venv

# Install Python packages
sudo -u smartspec ./venv/bin/pip install -r requirements.txt
```

#### 4. Configure Database

```bash
# Create database
sudo -u postgres createdb smartspec
sudo -u postgres createuser smartspec

# Set password
sudo -u postgres psql -c "ALTER USER smartspec WITH PASSWORD 'your_secure_password';"

# Grant permissions
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE smartspec TO smartspec;"
```

#### 5. Configure Application

```bash
# Create .env file
sudo -u smartspec cat > /opt/smartspec/.env <<EOF
SMARTSPEC_ENV=production
SMARTSPEC_DB_URL=postgresql://smartspec:your_secure_password@localhost/smartspec
SMARTSPEC_LOG_LEVEL=INFO
SMARTSPEC_MAX_WORKERS=4
SMARTSPEC_CHECKPOINT_DIR=/var/lib/smartspec/checkpoints
SMARTSPEC_LOG_DIR=/var/log/smartspec
EOF
```

#### 6. Setup Systemd Service

```bash
# Create service file
sudo cat > /etc/systemd/system/smartspec.service <<EOF
[Unit]
Description=SmartSpec Autopilot
After=network.target postgresql.service

[Service]
Type=simple
User=smartspec
Group=smartspec
WorkingDirectory=/opt/smartspec
Environment="PATH=/opt/smartspec/venv/bin"
EnvironmentFile=/opt/smartspec/.env
ExecStart=/opt/smartspec/venv/bin/python -m smartspec.ss_autopilot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable smartspec
sudo systemctl start smartspec
```

#### 7. Verify Installation

```bash
# Check service status
sudo systemctl status smartspec

# Check logs
sudo journalctl -u smartspec -n 50

# Test connection
curl http://localhost:8000/health
```

---

## ⚙️ Configuration

### Environment Variables

**Required:**
- `SMARTSPEC_ENV`: Environment (development/staging/production)
- `SMARTSPEC_DB_URL`: Database connection string
- `SMARTSPEC_LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

**Optional:**
- `SMARTSPEC_MAX_WORKERS`: Number of worker threads (default: 4)
- `SMARTSPEC_CHECKPOINT_DIR`: Checkpoint directory
- `SMARTSPEC_LOG_DIR`: Log directory
- `SMARTSPEC_ENABLE_PROFILING`: Enable profiling (true/false)

### Database Configuration

**PostgreSQL (Recommended):**
```bash
# /opt/smartspec/.env
SMARTSPEC_DB_URL=postgresql://user:pass@localhost/smartspec
```

**SQLite (Development):**
```bash
# /opt/smartspec/.env
SMARTSPEC_DB_URL=sqlite:///smartspec.db
```

### Logging Configuration

**Log Levels:**
- `DEBUG`: Detailed debugging information
- `INFO`: General information
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

**Log Rotation:**
- Max size: 10 MB
- Max backups: 5
- Automatic rotation

### Performance Configuration

**Worker Threads:**
```bash
# Low load
SMARTSPEC_MAX_WORKERS=2

# Medium load
SMARTSPEC_MAX_WORKERS=4

# High load
SMARTSPEC_MAX_WORKERS=8
```

**Caching:**
```bash
# Enable caching
SMARTSPEC_ENABLE_CACHING=true

# Cache TTL (seconds)
SMARTSPEC_CACHE_TTL=3600
```

---

## 👥 User Management

### Creating Users

```bash
# Via CLI
./venv/bin/python -m smartspec.ss_autopilot user create \
    --username john.doe \
    --email john@example.com \
    --role user

# Via API
curl -X POST http://localhost:8000/api/users \
    -H "Content-Type: application/json" \
    -d '{"username": "john.doe", "email": "john@example.com", "role": "user"}'
```

### User Roles

**admin:**
- Full system access
- User management
- System configuration
- All workflow operations

**user:**
- Create/manage own workflows
- View own specs
- No admin access

**viewer:**
- Read-only access
- View workflows
- No create/edit

### Modifying Users

```bash
# Change role
./venv/bin/python -m smartspec.ss_autopilot user update \
    --username john.doe \
    --role admin

# Reset password
./venv/bin/python -m smartspec.ss_autopilot user reset-password \
    --username john.doe
```

### Deleting Users

```bash
# Delete user
./venv/bin/python -m smartspec.ss_autopilot user delete \
    --username john.doe

# Delete with workflows
./venv/bin/python -m smartspec.ss_autopilot user delete \
    --username john.doe \
    --delete-workflows
```

---

## 📊 Monitoring

### System Metrics

**CPU & Memory:**
```bash
# Check resource usage
top
htop

# Check SmartSpec process
ps aux | grep smartspec
```

**Disk Usage:**
```bash
# Check disk space
df -h

# Check checkpoint directory
du -sh /var/lib/smartspec/checkpoints

# Check log directory
du -sh /var/log/smartspec
```

### Application Metrics

**Workflows:**
```bash
# Active workflows
./venv/bin/python -m smartspec.ss_autopilot stats workflows --status running

# Completed today
./venv/bin/python -m smartspec.ss_autopilot stats workflows --date today

# Failed workflows
./venv/bin/python -m smartspec.ss_autopilot stats workflows --status failed
```

**Performance:**
```bash
# View profiling data
./venv/bin/python -m smartspec.ss_autopilot stats performance

# Cache statistics
./venv/bin/python -m smartspec.ss_autopilot stats cache

# Database statistics
./venv/bin/python -m smartspec.ss_autopilot stats database
```

### Log Monitoring

**View Logs:**
```bash
# Systemd logs
sudo journalctl -u smartspec -f

# Application logs
tail -f /var/log/smartspec/smartspec.log

# Error logs
tail -f /var/log/smartspec/error.log
```

**Search Logs:**
```bash
# Search for errors
grep ERROR /var/log/smartspec/smartspec.log

# Search for specific workflow
grep "workflow-123" /var/log/smartspec/smartspec.log
```

### Prometheus & Grafana

**Setup Prometheus:**
```bash
# Install
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*

# Configure
cat > prometheus.yml <<EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'smartspec'
    static_configs:
      - targets: ['localhost:8000']
EOF

# Start
./prometheus --config.file=prometheus.yml &
```

**Setup Grafana:**
```bash
# Install
sudo apt-get install -y grafana

# Start
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

# Access: http://localhost:3000
# Default: admin/admin
```

---

## 💾 Backup & Recovery

### Backup Strategy

**What to Backup:**
- Database
- Checkpoints
- Logs
- Configuration

**Frequency:**
- Database: Daily
- Checkpoints: Daily
- Logs: Weekly
- Configuration: On change

### Backup Script

```bash
#!/bin/bash
# /opt/smartspec/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/var/backups/smartspec

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump smartspec | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup checkpoints
tar czf $BACKUP_DIR/checkpoints_$DATE.tar.gz /var/lib/smartspec/checkpoints

# Backup logs
tar czf $BACKUP_DIR/logs_$DATE.tar.gz /var/log/smartspec

# Backup configuration
cp /opt/smartspec/.env $BACKUP_DIR/env_$DATE

# Keep only last 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

**Schedule Backup:**
```bash
# Add to crontab
sudo crontab -e

# Add line (daily at 2 AM):
0 2 * * * /opt/smartspec/backup.sh
```

### Recovery

**Restore Database:**
```bash
# Stop service
sudo systemctl stop smartspec

# Restore
gunzip < /var/backups/smartspec/db_20251226_020000.sql.gz | psql smartspec

# Start service
sudo systemctl start smartspec
```

**Restore Checkpoints:**
```bash
# Stop service
sudo systemctl stop smartspec

# Restore
tar xzf /var/backups/smartspec/checkpoints_20251226_020000.tar.gz -C /

# Start service
sudo systemctl start smartspec
```

---

## 🔒 Security

### Firewall

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow SmartSpec (internal only)
sudo ufw allow from 10.0.0.0/8 to any port 8000

# Enable firewall
sudo ufw enable
```

### SSL/TLS

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d smartspec.example.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### Access Control

**Database:**
```bash
# Restrict to localhost
# /etc/postgresql/14/main/pg_hba.conf
local   smartspec   smartspec   md5
host    smartspec   smartspec   127.0.0.1/32   md5
```

**Application:**
```bash
# Enable authentication
SMARTSPEC_ENABLE_AUTH=true
SMARTSPEC_JWT_SECRET=your_secret_key_here
```

### Audit Logging

```bash
# Enable audit logs
SMARTSPEC_ENABLE_AUDIT=true
SMARTSPEC_AUDIT_LOG=/var/log/smartspec/audit.log

# View audit logs
tail -f /var/log/smartspec/audit.log
```

---

## 🐛 Troubleshooting

### Service Won't Start

**Check logs:**
```bash
sudo journalctl -u smartspec -n 50
```

**Common causes:**
- Missing dependencies
- Database connection failed
- Port already in use
- Permission issues

**Solutions:**
```bash
# Check dependencies
./venv/bin/pip install -r requirements.txt

# Test database connection
psql -U smartspec -d smartspec -c "SELECT 1"

# Check port
sudo netstat -tulpn | grep 8000

# Fix permissions
sudo chown -R smartspec:smartspec /opt/smartspec
```

### High Memory Usage

**Check memory:**
```bash
free -h
ps aux --sort=-%mem | head -10
```

**Solutions:**
```bash
# Reduce workers
SMARTSPEC_MAX_WORKERS=2

# Restart service
sudo systemctl restart smartspec
```

### Database Issues

**Check connection:**
```bash
psql -U smartspec -d smartspec -c "SELECT 1"
```

**Check performance:**
```bash
psql smartspec -c "SELECT * FROM pg_stat_activity"
```

**Optimize:**
```bash
# Vacuum
psql smartspec -c "VACUUM ANALYZE"

# Reindex
psql smartspec -c "REINDEX DATABASE smartspec"
```

---

## 🔧 Maintenance

### Regular Tasks

**Daily:**
- Check system status
- Review error logs
- Monitor disk space

**Weekly:**
- Review performance metrics
- Check backup success
- Update security patches

**Monthly:**
- Database optimization
- Log rotation
- Capacity planning

### Updates

**Update Application:**
```bash
# Stop service
sudo systemctl stop smartspec

# Backup
/opt/smartspec/backup.sh

# Pull updates
cd /opt/smartspec
sudo -u smartspec git pull

# Update dependencies
sudo -u smartspec ./venv/bin/pip install -r requirements.txt

# Start service
sudo systemctl start smartspec
```

**Update System:**
```bash
# Update packages
sudo apt-get update
sudo apt-get upgrade -y

# Reboot if needed
sudo reboot
```

---

## 📞 Support

**Internal:**
- DevOps Team: devops@company.com
- Security Team: security@company.com

**External:**
- SmartSpec Support: support@smartspec.io
- GitHub Issues: https://github.com/naibarn/SmartSpec/issues

---

**Admin Guide Version:** 1.0.0  
**Last Updated:** 2025-12-26  
**Next Review:** 2026-01-26
