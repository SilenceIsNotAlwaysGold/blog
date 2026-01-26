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

### Quick Start for Development

For local development with hot-reload (no container rebuild needed):

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop development environment
docker-compose -f docker-compose.dev.yml down
```

### Development vs Production

| Feature | Development (docker-compose.dev.yml) | Production (docker-compose.yml) |
|---------|--------------------------------------|----------------------------------|
| Frontend | Vite dev server with HMR | Static build with Nginx |
| Backend | Uvicorn with --reload | Uvicorn production mode |
| Port | Frontend: 5173, Backend: 8000 | Frontend: 80, Backend: 8000 |
| Source Code | Mounted as volumes | Copied into image |
| Rebuild | Not needed for code changes | Required for every change |
| Performance | Slower (dev mode) | Faster (optimized) |

### Hot-Reload Features

**Frontend (Vite HMR)**:
- Instant updates on file save
- Preserves component state
- Fast refresh for Vue components
- No page reload needed

**Backend (Uvicorn --reload)**:
- Auto-restart on Python file changes
- Fast reload (< 1 second)
- Preserves database connections
- No container rebuild needed

### Development Workflow

1. **Start development environment**:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Edit code locally**:
   - Frontend: Edit files in `./frontend/src/`
   - Backend: Edit files in `./backend/app/` or `./backend/main.py`

3. **See changes immediately**:
   - Frontend: Browser auto-refreshes
   - Backend: Server auto-reloads

4. **No rebuild needed**:
   - Changes are reflected instantly
   - Only restart if you modify dependencies

### When to Rebuild

You only need to rebuild containers when:

**Frontend**:
- Adding/removing npm packages (`package.json` changes)
- Modifying build configuration (`vite.config.ts`)

```bash
docker-compose -f docker-compose.dev.yml up -d --build frontend
```

**Backend**:
- Adding/removing Python packages (`requirements.txt` changes)
- Modifying Dockerfile

```bash
docker-compose -f docker-compose.dev.yml up -d --build backend
```

### Switching Between Modes

**Development to Production**:
```bash
# Stop dev environment
docker-compose -f docker-compose.dev.yml down

# Start production environment
docker-compose up -d
```

**Production to Development**:
```bash
# Stop production environment
docker-compose down

# Start dev environment
docker-compose -f docker-compose.dev.yml up -d
```

### Troubleshooting Development Mode

**Frontend not updating**:
```bash
# Check if volume is mounted correctly
docker-compose -f docker-compose.dev.yml exec frontend ls -la /app/src

# Restart frontend container
docker-compose -f docker-compose.dev.yml restart frontend
```

**Backend not reloading**:
```bash
# Check if uvicorn reload is enabled
docker-compose -f docker-compose.dev.yml logs backend | grep reload

# Restart backend container
docker-compose -f docker-compose.dev.yml restart backend
```

**Port conflicts**:
```bash
# Check if ports are already in use
lsof -i :5173  # Frontend dev port
lsof -i :8000  # Backend port

# Kill conflicting processes or change ports in .env
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
