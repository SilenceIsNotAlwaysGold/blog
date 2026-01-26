# Personal Blog System

A dual-board personal blog system with life (private) and tech (public) sections.

## Features

- **Dual Board System**: Separate life and tech content boards with different access controls
- **Rich Markdown Editor**: WYSIWYG Markdown editor with code highlighting
- **Personal Resume System**: Skills tree and project showcase
- **Article Interaction**: Like and email contact features
- **Responsive Design**: Mobile-first responsive layout
- **Search Functionality**: Full-text search for tech articles

## Tech Stack

### Frontend
- Vue 3 + TypeScript
- Element Plus UI
- Vditor Markdown Editor
- Pinia State Management
- Vue Router
- Axios

### Backend
- Python 3.10+ FastAPI
- MongoDB 4.4+
- Motor (Async MongoDB Driver)
- Beanie ODM
- JWT Authentication
- FastAPI-Mail

### Deployment
- Docker + Docker Compose
- Nginx

## Project Structure

```
personal-blog/
├── backend/          # FastAPI backend
│   ├── app/          # Application code
│   ├── tests/        # Backend tests
│   ├── uploads/      # Uploaded files
│   └── requirements.txt
├── frontend/         # Vue 3 frontend
│   ├── src/          # Frontend source
│   ├── public/       # Static assets
│   └── package.json
├── docs/             # Project documentation
│   └── dev/          # Development specs
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- MongoDB 4.4+
- Docker & Docker Compose (optional)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Run the server
python main.py
# Server will start at http://localhost:8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
# Server will start at http://localhost:5173
```

### Docker Setup

**Production Mode** (optimized builds):
```bash
# Build and start all services
docker-compose up -d

# Stop services
docker-compose down
```

**Development Mode** (with hot-reload, recommended for development):
```bash
# Start development environment with hot-reload
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop development environment
docker-compose -f docker-compose.dev.yml down
```

**Why use Development Mode?**
- No container rebuild needed for code changes
- Frontend: Vite HMR (Hot Module Replacement) for instant updates
- Backend: Uvicorn auto-reload on file changes
- Faster development workflow
- See changes immediately without waiting for builds

For detailed Docker documentation, see [DOCKER.md](./DOCKER.md).

## Development

### Backend Development

- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Frontend Development

- Development server: http://localhost:5173
- Hot module replacement enabled
- Proxy API requests to backend

### Testing

#### Backend Tests
```bash
cd backend
pytest
```

#### Frontend Tests
```bash
cd frontend
npm run test
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## License

This project is for personal use.

## Author

Personal Blog System
Generated with Spec-Driven Development workflow
