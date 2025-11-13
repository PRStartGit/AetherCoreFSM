# Quick Start Guide - RiskProof

## Prerequisites

- Python 3.8+ with pip
- Node.js 16+ with npm
- Git

## Initial Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create initial super admin
python seed_initial_admin.py
```

**Expected Output**:
```
🚀 RiskProof Initial Setup
=================================================================
Creating super admin account...

📊 Creating database tables...
✓ Database tables created successfully

👤 Creating super admin user...
   Email: hello@prstart.co.uk
✓ Super admin user created successfully!

📧 WELCOME EMAIL
=====================================================================
To: hello@prstart.co.uk
Subject: Welcome to RiskProof - Your Super Admin Account

🔐 Login Credentials:
   Email: hello@prstart.co.uk
   Password: ChangeMe123!
   Login URL: http://localhost:4200/login
=====================================================================
```

### 2. Start Backend Server

```bash
# Make sure you're in the backend directory with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Interactive API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

Frontend will be available at: http://localhost:4200

## Login

1. Open http://localhost:4200/login
2. Enter credentials:
   - **Organization ID**: Can use any value for super admin (e.g., "admin")
   - **Email**: hello@prstart.co.uk
   - **Password**: ChangeMe123!
3. Click "Login"
4. You'll be redirected to the Super Admin Dashboard

## Default Credentials

### Super Admin
- Email: hello@prstart.co.uk
- Password: ChangeMe123!
- Access: Full system access

**⚠️ IMPORTANT**: Change the default password after first login!

## First Steps After Login

1. **Change Your Password** (Security > Account Settings)
2. **Create Your First Organization**
   - Navigate to "Organizations" in the sidebar
   - Click "Add Organization"
   - Fill in organization details
3. **Add Sites to the Organization**
   - Navigate to "Sites"
   - Click "Add Site"
   - Assign to the organization
4. **Create Organization Admins**
   - Navigate to "Users"
   - Click "Add User"
   - Set role to "Organization Admin"
   - Assign to the organization

## Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed: `python --version`
- Ensure venv is activated (you should see `(venv)` in terminal)
- Check all dependencies installed: `pip list`
- Check port 8000 is not in use: `netstat -ano | findstr :8000` (Windows) or `lsof -i :8000` (Mac/Linux)

### Frontend won't start
- Ensure Node.js is installed: `node --version`
- Ensure npm dependencies are installed: `ls node_modules`
- Check port 4200 is not in use
- Try clearing npm cache: `npm cache clean --force`

### Database errors
- Delete the database file: `rm backend/riskproof.db`
- Run seed script again: `python seed_initial_admin.py`

### Login fails
- Check backend is running (visit http://localhost:8000/docs)
- Check browser console for errors (F12)
- Verify credentials are correct
- Try resetting super admin password: `python seed_initial_admin.py --reset-password`

## Development Workflow

### Backend Development
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm start
```

### Database Migrations
```bash
cd backend
# Create migration
alembic revision --autogenerate -m "Description of changes"

# Apply migration
alembic upgrade head
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
AetherCoreFSM/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Core functionality (auth, db, security)
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── alembic/            # Database migrations
│   ├── seed_initial_admin.py  # Super admin creation script
│   └── requirements.txt    # Python dependencies
├── frontend/               # Angular frontend
│   ├── src/app/
│   │   ├── core/          # Auth, guards, services
│   │   ├── features/      # Feature modules (dashboards, etc.)
│   │   └── shared/        # Shared components
│   ├── package.json       # Node dependencies
│   └── angular.json       # Angular configuration
└── SECURITY.md            # Security documentation
```

## Support

For issues or questions:
- Check the logs (backend terminal and browser console)
- Review SECURITY.md for security-related questions
- Check PROJECT_STATUS.md for current development status

## Next Steps

- Explore the dashboards for each user role
- Create test organizations and sites
- Configure categories and tasks for your sites
- Set up checklists and start tracking compliance
- Review defect management features

Happy building! 🚀
