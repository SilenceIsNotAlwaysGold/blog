# Personal Blog Development Tasks

## Overview
Improve development workflow by adding hot-reload support to avoid rebuilding containers on every change.

## Task List

### T-001: Add Hot-Reload Support for Frontend Development
**Priority**: High
**Estimated Effort**: 30 minutes
**Dependencies**: None

**Description**:
Modify docker-compose.yml to support hot-reload for frontend development by mounting source code as volumes and using Vite's dev server instead of building static files.

**Acceptance Criteria**:
- Frontend container runs `npm run dev` instead of building static files
- Source code changes reflect immediately without container rebuild
- Vite HMR (Hot Module Replacement) works properly
- Development environment remains isolated in Docker

**Implementation Notes**:
- Add volume mounts for frontend source code
- Override CMD to run dev server
- Ensure proper port mapping for Vite dev server
- Update documentation

### T-002: Add Hot-Reload Support for Backend Development
**Priority**: High
**Estimated Effort**: 30 minutes
**Dependencies**: None

**Description**:
Modify docker-compose.yml to support hot-reload for backend development by mounting source code and using uvicorn's reload flag.

**Acceptance Criteria**:
- Backend container auto-reloads on code changes
- Source code mounted as volume
- No container rebuild needed for code changes
- Development environment remains isolated in Docker

**Implementation Notes**:
- Add volume mounts for backend source code
- Use uvicorn with --reload flag
- Ensure proper file watching works in Docker
- Update documentation

### T-003: Create Development-Specific Docker Compose Configuration
**Priority**: Medium
**Estimated Effort**: 20 minutes
**Dependencies**: T-001, T-002

**Description**:
Create a separate docker-compose.dev.yml for development with hot-reload, keeping docker-compose.yml for production builds.

**Acceptance Criteria**:
- docker-compose.dev.yml exists with hot-reload configuration
- docker-compose.yml remains unchanged for production
- Clear documentation on when to use each file
- Easy switching between dev and prod modes

**Implementation Notes**:
- Use docker-compose override pattern
- Document usage in README or DOCKER.md
- Add npm scripts for convenience

### T-004: Update Documentation
**Priority**: Medium
**Estimated Effort**: 15 minutes
**Dependencies**: T-001, T-002, T-003

**Description**:
Update DOCKER.md and README.md with instructions for development workflow using hot-reload.

**Acceptance Criteria**:
- Clear instructions for development mode
- Clear instructions for production mode
- Troubleshooting section for common issues
- Performance comparison notes

**Implementation Notes**:
- Add "Development Workflow" section
- Add "Production Deployment" section
- Include examples of both modes
