# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ShortPlay is an AI short drama generation platform built with FastAPI + React + TailwindCSS + PostgreSQL. It covers the full workflow from text input to video generation: text input → info extraction → character/scene asset generation → storyboard management → video generation.

## Development Commands

### Backend (Python 3.11+)
```bash
cd backend
pip install -e .              # Install dependencies
uvicorn app.main:app --reload # Run dev server (port 8080)
pytest                       # Run all tests
pytest tests/api/            # Run API tests only
pytest tests/services/       # Run service tests only
pytest --cov=app             # Run with coverage
```

### Frontend (Node.js)
```bash
cd frontend
npm install                   # Install dependencies
npm run dev                   # Run dev server (port 3000)
npm run build                 # Production build
npm test                      # Run tests (vitest)
npm run lint                  # ESLint check
```

### Docker (Infrastructure)
```bash
cd docker
docker compose up -d                    # Start infra (postgres, redis, rabbitmq, minio, es, qdrant)
docker compose -f docker-compose.prod.yml up -d  # Full production stack
```

## Architecture

### Backend: Layered Architecture
```
API Routes (app/api/v1/*.py)
    ↓
Services (app/services/*.py)     # Business logic
    ↓
Repositories (app/repositories/*.py)  # Data access
    ↓
Models (app/models/*.py)         # SQLAlchemy ORM
```

- **Schemas** (app/schemas/): Pydantic models for request/response validation
- **Core** (app/core/): Config, database session, security (JWT), websocket manager
- **Settings**: Environment variables via pydantic-settings, cached with @lru_cache

### Frontend: React 18 + TypeScript
- State: Zustand for global state, React Query for server state
- Routing: React Router v6
- API: Axios client with response interceptor in `src/api/index.ts`
- UI Components: Custom shadcn/ui-style components in `src/components/ui/`

### API Response Format
All responses use `{ code: 200, data: {...}, message: "success" }` format.

### Key Files
- `backend/app/main.py`: FastAPI app entry, CORS setup, router registration
- `backend/app/core/config.py`: All settings via pydantic-settings, env file support
- `frontend/src/api/index.ts`: Axios instance with interceptors, typed API functions
- `frontend/src/App.tsx`: Route definitions with React Router

## Database

PostgreSQL with SQLAlchemy 2.0. All tables use soft delete (`is_deleted` column) and timestamp mixins. Key tables: project, episode, character, scene, storyboard, model_instance, prompt_template.

## Testing

- Backend: pytest with SQLite test database (in-memory), fixtures in `tests/conftest.py`
- Frontend: vitest + React Testing Library (configured but tests not yet written)
- Coverage target: 80%+

## Environment Variables

Copy `.env.example` to `.env` in both backend and frontend directories. Key vars:
- Backend: `DATABASE_URL`, `REDIS_URL`, `RABBITMQ_URL`, `JWT_SECRET_KEY`
- Frontend: `VITE_API_BASE_URL` (defaults to `/api/v1` for Vite proxy)
