# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

星语诗词平台 (Xingyu Poetry Platform) - A multi-platform poetry appreciation, learning, and social platform featuring AI-powered poetry generation and analysis. Built with FastAPI backend and Vue 3 frontend (H5).

**Key Technologies:**
- Backend: Python 3.11+ with FastAPI, SQLAlchemy 2.0 (async), Alembic
- Frontend: Vue 3, TypeScript, Vite, Pinia
- Database: MySQL 8.0, Redis 7, Elasticsearch 7.17
- AI Integration: Third-party APIs (通义千问/Tongyi Qianwen via dashscope SDK)
- Deployment: Docker Compose

## Common Development Commands

### Backend (Python FastAPI)

Located in `server/` directory:

```bash
# Start development server (from server/ directory)
uvicorn app.main:app --reload

# Alternative start method
python app/main.py

# Database migrations
alembic upgrade head                    # Apply migrations
alembic revision --autogenerate -m "description"  # Create new migration
alembic downgrade -1                    # Rollback one migration

# Import poetry data
python scripts/import_poetry.py

# Code quality
black app/                              # Format code
ruff check app/                         # Lint code
mypy app/                               # Type checking
pytest tests/                           # Run tests
pytest --cov=app tests/                 # Run tests with coverage
```

### Frontend (Vue 3 H5)

Located in `client-app/` directory:

```bash
# Start development server (from client-app/ directory)
npm run dev                             # Start on port 5173

# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker Operations

From project root directory:

```bash
# Start all services (recommended for development)
./start.sh                              # Automated startup with health checks

# Manual docker-compose commands
docker-compose up -d                    # Start all services
docker-compose down                     # Stop all services
docker-compose ps                       # View service status
docker-compose logs -f api              # View backend logs
docker-compose logs -f web              # View frontend logs
docker-compose restart api              # Restart backend service

# Database operations in container
docker exec -it poetry-api bash
alembic upgrade head
python scripts/import_poetry.py
exit

# Stop services and clean data
./stop.sh                               # Interactive cleanup
```

### Service URLs (when running)

- Frontend H5: http://localhost:8080 (via Docker) or http://localhost:5173 (dev mode)
- Backend API: http://localhost:8000
- API Swagger Docs: http://localhost:8000/docs
- API ReDoc: http://localhost:8000/redoc
- MySQL: localhost:3306
- Redis: localhost:6380 (mapped from container 6379)
- Elasticsearch: http://localhost:9200

## Architecture & Code Structure

### High-Level Architecture

```
┌─────────────────┐
│  Vue 3 Frontend │ (client-app/)
│  TypeScript     │
└────────┬────────┘
         │ HTTP/WebSocket
         ↓
┌─────────────────┐
│  FastAPI        │ (server/app/)
│  Python 3.11+   │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬────────────┐
    ↓         ↓          ↓            ↓
 MySQL 8   Redis 7   Elasticsearch  Third-party AI APIs
(primary) (cache)    (search)       (Tongyi Qianwen)
```

### Backend Architecture (server/)

**Layered Architecture:**
- `api/v1/` - API endpoints (controllers/routes)
- `services/` - Business logic layer
- `models/` - SQLAlchemy ORM models (database entities)
- `schemas/` - Pydantic models for request/response validation
- `core/` - Core configuration (settings, security, database connection)
- `utils/` - Utility functions (Elasticsearch client, etc.)

**Key Patterns:**
- Dependency injection via FastAPI's `Depends()`
- Async/await throughout (async database operations with aiomysql)
- JWT-based authentication (see `app/core/security.py` and `app/api/deps.py`)
- Centralized configuration via Pydantic Settings (`app/core/config.py`)

**Database Models (SQLAlchemy 2.0):**
- `users` - User accounts with WeChat integration support
- `poetries` - Poetry entries with metadata (dynasty, type, tags)
- `authors` - Poet/author information
- `user_poetry_interactions` - Likes, collects, reads (polymorphic interactions)
- `comments` - Comments on poetry/posts
- `follows` - User follow relationships
- `posts` - User-generated content (square/plaza feature)
- `messages` - In-app messaging system

**Important Database Notes:**
- All migrations are in `server/alembic/versions/`
- Use Alembic for schema changes - never modify database directly
- All datetime fields use server-side defaults (CURRENT_TIMESTAMP)
- Tables use utf8mb4 charset for proper emoji/Chinese character support

### Frontend Architecture (client-app/)

**Vue 3 Composition API with TypeScript:**
- `src/pages/` - Page components (route views)
- `src/components/` - Reusable components
- `src/api/` - API client modules (axios-based)
- `src/stores/` - Pinia state management
- `src/utils/` - Utility functions
- `src/styles/` - SCSS global styles and variables

**Key Pages:**
- `index/` - Homepage with daily poetry recommendations
- `poetry-list/`, `poetry-detail/` - Poetry browsing
- `author-list/`, `author-detail/` - Author browsing
- `square/` - Social plaza with user posts
- `profile/` - User profile and settings
- `search/` - Search functionality
- `discover/` - Discovery/explore page

**State Management:**
- Uses Pinia for state management
- API calls centralized in `src/api/` modules
- Each API module corresponds to backend router (auth, poetry, comment, etc.)

**API Integration:**
- Base URL configured via Vite proxy: `/api` → `http://localhost:8000/api`
- Uses axios for HTTP requests
- TypeScript interfaces define API request/response shapes

### AI Integration Approach

**Third-Party API Model (NOT local AI deployment):**
- Uses external AI services via SDK (dashscope for Tongyi Qianwen)
- Configured via environment variables: `TONGYI_API_KEY`, `TONGYI_MODEL`
- Cost-effective: ~2元/month for moderate usage vs 1200+元/month for GPU server
- No large model files (~100MB dependencies vs 5GB+ for local models)

**AI Features (planned):**
- Poetry generation based on themes
- Poetry analysis (translation, appreciation, sentiment)
- Intelligent Q&A about poetry
- AI opponent for "Flying Flower" game (飞花令)

### Critical Implementation Details

**Authentication Flow:**
1. Login via `POST /api/v1/auth/login` with username/password
2. Receives JWT token in response
3. Include token in Authorization header: `Bearer {token}`
4. Token validation happens in `app/api/deps.py::get_current_user()`

**Database Session Management:**
- Async sessions created per request via dependency injection
- See `app/core/database.py` for session factory
- Always use `async with` pattern for database operations
- Example in services: `async with get_session() as db:`

**Elasticsearch Integration:**
- Client singleton in `app/utils/elasticsearch_client.py`
- Index: `poetry_index` for poetry search
- Supports full-text search on title, content, author name
- Initialized on app startup in `app/main.py::startup_event()`

**CORS Configuration:**
- Configured in `app/core/config.py::CORS_ORIGINS`
- Supports comma-separated origins in environment variable
- Default allows localhost ports 3000, 5173, 5174, 5175, 8080

**Environment Configuration:**
- Backend: `server/.env` (based on `.env.example`)
- Frontend: Uses Vite's proxy for API calls (no separate .env needed for API URL)
- Docker: Environment variables passed via `docker-compose.yml`

## Development Workflow

### When Adding New Features

1. **Backend API:**
   - Create/update SQLAlchemy model in `server/app/models/`
   - Generate migration: `alembic revision --autogenerate -m "add_feature"`
   - Create Pydantic schemas in `server/app/schemas/`
   - Implement service logic in `server/app/services/`
   - Create API endpoints in `server/app/api/v1/`
   - Register router in `server/app/main.py`

2. **Frontend UI:**
   - Create page component in `client-app/src/pages/`
   - Create API client in `client-app/src/api/`
   - Add route in router configuration (if new page)
   - Update Pinia store if state management needed
   - Add navigation links/buttons

3. **Database Changes:**
   - ALWAYS use Alembic migrations
   - Review auto-generated migrations before applying
   - Test migrations with `alembic upgrade head` and `alembic downgrade -1`
   - Keep migration files in version control

### Testing Approach

- Backend: pytest with async support (`pytest-asyncio`)
- Tests location: `server/tests/`
- No comprehensive test suite yet - add tests when implementing critical features
- API can be tested interactively via Swagger UI at `/docs`

### Code Style

**Backend (Python):**
- Use `black` for formatting (line length 100)
- Follow FastAPI conventions: async def for endpoints
- Type hints required (use mypy for checking)
- Docstrings for public functions/classes

**Frontend (TypeScript/Vue):**
- Use TypeScript for type safety
- Composition API with `<script setup lang="ts">`
- SCSS for styling with variables in `src/styles/variables.scss`

## Important Notes for AI Development

When implementing AI features (poetry generation, analysis):
- API calls should be async and non-blocking
- Consider implementing Celery for long-running AI tasks (framework already in requirements)
- Cache AI responses in Redis to reduce API costs
- Handle rate limits and API errors gracefully
- Log AI API usage for cost monitoring

## Common Pitfalls

1. **Async/Await**: Backend is fully async - don't mix sync and async code
2. **Database Sessions**: Always use dependency injection for sessions, never create manually
3. **Migration Conflicts**: Pull latest migrations before creating new ones
4. **Port Conflicts**: Redis mapped to 6380 externally to avoid conflicts with local Redis on 6379
5. **CORS Issues**: Add frontend dev server URL to CORS_ORIGINS if getting CORS errors
6. **MySQL Connection**: Wait 30-60s for MySQL to fully initialize in Docker before backend can connect

## Quick Reference: File Locations

- API Documentation: Generated at http://localhost:8000/docs when running
- Environment Config: `server/.env.example` (copy to `.env`)
- Database Schema: `server/alembic/versions/` (migration files show schema)
- API Routes: `server/app/api/v1/` (one file per resource)
- Frontend Routes: Check `client-app/src/pages/` for available pages
- Docker Config: `docker-compose.yml` at project root
- Startup Script: `./start.sh` (Linux/Mac) at project root

## Key Documentation Files

- `README.md` - Project overview and tech stack
- `QUICKSTART.md` - Docker-based quick start guide
- `DEPLOYMENT.md` - Detailed deployment instructions
- `server/README.md` - Backend-specific documentation
- `需求分析文档.md` - Detailed requirements (Chinese)
- `最终开发计划.md` - Development plan and roadmap (Chinese)
- `第三方AI服务集成方案.md` - AI integration approach (Chinese)
