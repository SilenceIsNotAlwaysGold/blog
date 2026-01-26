# Personal Blog - Docker Deployment Guide

## Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### 1. Clone and Configure

```bash
# Clone repository
git clone <repository-url>
cd personal-blog

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Start Services

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 3. Access Application

- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Initialize Database

```bash
# Create admin user (first time only)
docker-compose exec backend python -m app.scripts.create_admin
```

## Services

### MongoDB
- Port: 27017 (configurable)
- Data persistence: `mongodb_data` volume
- Health check: ping command

### Backend (FastAPI)
- Port: 8000 (configurable)
- Image uploads: `./backend/uploads` volume
- Health check: `/health` endpoint

### Frontend (Nginx)
- Port: 80 (configurable)
- SPA routing enabled
- API proxy to backend
- Gzip compression
- Static file caching

## Management Commands

### Start/Stop

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose stop

# Restart services
docker-compose restart

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

### Logs

```bash
# View all logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Service-specific logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongodb
```

### Database Backup

```bash
# Backup MongoDB
docker-compose exec mongodb mongodump --out=/data/backup

# Restore MongoDB
docker-compose exec mongodb mongorestore /data/backup
```

### Updates

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# View updated logs
docker-compose logs -f
```

## Production Deployment

### Security Checklist

1. **Change default passwords**
   - MongoDB root password
   - JWT secret key

2. **Configure HTTPS**
   - Use reverse proxy (Nginx/Traefik)
   - Obtain SSL certificate (Let's Encrypt)

3. **Set strong secrets**
   - Generate random SECRET_KEY
   - Use strong MONGO_ROOT_PASSWORD

4. **Configure firewall**
   - Only expose necessary ports
   - Restrict MongoDB access

5. **Enable monitoring**
   - Set up health checks
   - Configure log aggregation

### Environment Variables

Required:
- `MONGO_ROOT_PASSWORD`: MongoDB admin password
- `SECRET_KEY`: JWT signing key

Optional:
- `SMTP_*`: Email notification settings
- `FRONTEND_PORT`: Frontend port (default: 80)
- `BACKEND_PORT`: Backend port (default: 8000)

### Scaling

```bash
# Scale backend instances
docker-compose up -d --scale backend=3

# Use load balancer (Nginx/HAProxy)
# Configure in docker-compose.override.yml
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs <service-name>

# Check container status
docker-compose ps

# Restart service
docker-compose restart <service-name>
```

### Database connection issues

```bash
# Check MongoDB health
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"

# Verify connection string
docker-compose exec backend env | grep MONGODB_URL
```

### Frontend can't reach backend

```bash
# Check network
docker network inspect personal-blog_blog-network

# Test backend from frontend
docker-compose exec frontend wget -O- http://backend:8000/health
```

## Development Mode

```bash
# Use docker-compose.dev.yml for development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Enable hot reload
# Mount source code as volumes
```

## Maintenance

### Clean up

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Full cleanup
docker system prune -a --volumes
```

### Update images

```bash
# Pull latest base images
docker-compose pull

# Rebuild with latest
docker-compose build --no-cache

# Restart with new images
docker-compose up -d
```

## Support

For issues and questions:
- Check logs: `docker-compose logs`
- Review documentation
- Open GitHub issue
