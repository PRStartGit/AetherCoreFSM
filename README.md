# RiskProof Clone - Safety Management Platform

A comprehensive multi-tenant safety management platform for organizations to manage checklists, defects, and compliance across multiple sites.

## Features

- Multi-tenant architecture with organization isolation
- Three user roles: Super Admin, Organization Admin, Site User
- Monitoring Module with dynamic checklists
- Defect tracking with photo uploads
- RAG status (Red/Amber/Green) reporting
- Automated email reports
- Subscription management
- Responsive dashboard for all user types

## Tech Stack

**Backend:**
- Python 3.8+
- FastAPI
- SQLAlchemy
- Alembic (migrations)
- JWT Authentication
- SQLite (dev) / PostgreSQL (prod)

**Frontend:**
- Angular 17+
- Angular Material
- TypeScript
- RxJS

## Project Structure

```
AetherCoreFSM/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/            # Config, security, database
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utilities
│   ├── alembic/             # Database migrations
│   ├── tests/               # Backend tests
│   └── requirements.txt
└── frontend/
    └── src/app/
        ├── core/            # Auth, guards, services
        ├── shared/          # Shared components
        └── features/        # Feature modules
```

## Setup Instructions

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the development server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
ng serve
```

3. Open browser to `http://localhost:4200`

## Development Phases

- **Phase 1 (Days 1-3):** MVP Foundation - Auth, user management, basic setup
- **Phase 2 (Days 4-7):** Monitoring Module - Categories, tasks, checklists, defects
- **Phase 3 (Days 8-10):** Dashboards & Reporting - Email reports, analytics
- **Phase 4 (Days 11-14):** Subscription & Polish - Billing, UI/UX refinement
- **Phase 5 (Days 15-21):** Deployment - Docker, DigitalOcean, production

## License

Proprietary - All rights reserved
