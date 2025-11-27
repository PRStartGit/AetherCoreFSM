# AetherCoreFSM (Zynthio) - Updated Handover Document

**Last Updated:** November 22, 2025 (Session 2)
**Current Status:** Production-ready with recent critical fixes deployed

---

## 🚨 Recent Critical Fixes (November 22, 2025 - Session 2)

### 1. Photo Upload Fix for Temperature Records
**Issue:** Photos uploaded to fridge/freezer temperature fields were saving as `null` in database
**Root Cause:** Form controls were deleted and recreated on every temperature input, wiping out photo URLs
**Fix:** Modified `dynamic-task-form.component.ts` to preserve existing values when recreating controls
**Status:** ✅ Deployed to production
**Commit:** `df6afcf`

### 2. Password Reset Button Fix
**Issue:** Password reset button returned 404 error
**Root Cause:** Frontend called `/api/v1/auth/forgot-password`, backend endpoint was `/api/v1/forgot-password`
**Fix:** Updated `auth.service.ts` to remove `/auth` prefix from URL
**Status:** ✅ Deployed to production
**Commit:** `34ea4bc`

### 3. Password Reset Email Integration
**Issue:** Password reset emails weren't being sent (only logged to console)
**Root Cause:** Email service wasn't being called by forgot-password endpoint
**Fix:** Updated `auth.py` to call `send_password_reset_email()` using SendGrid
**Status:** ✅ Deployed to production
**Commit:** `1797a76`

### 4. Profile Dropdown Feature
**Issue:** Super admin mobile menu too tall, logout button cut off
**Solution:** Added dropdown to header profile icon with Profile and Logout options
**Status:** ✅ Deployed to production
**Commit:** `399504c`

---

## Server & Infrastructure

### Remote Server Access
- **Server IP:** `165.22.122.116`
- **SSH Alias:** `zynthio` (configured in SSH config)
- **SSH Command:** `ssh zynthio` (connects as root)
- **Project Path:** `/root/AetherCoreFSM`
- **Docker Containers:**
  - `zynthio-frontend` (nginx:alpine, port 80)
  - `zynthio-backend` (python:3.11-slim, port 8000)
  - `zynthio-database` (postgres:15, port 5432)
  - `zynthio-redis` (redis:alpine, port 6379)

### SSH Configuration
Add to `~/.ssh/config`:
```
Host zynthio
    HostName 165.22.122.116
    User root
    IdentityFile ~/.ssh/id_rsa
```

### Essential Server Commands
```bash
# Connect to server
ssh zynthio

# Navigate to project
cd /root/AetherCoreFSM

# View container status
docker compose ps

# View logs (live)
docker compose logs -f backend
docker compose logs -f frontend

# Restart specific service
docker compose restart backend

# Rebuild and restart (REQUIRED after code changes)
docker compose build backend && docker compose up -d backend
docker compose build frontend && docker compose up -d frontend

# Access database
docker exec -it zynthio-database psql -U postgres -d zynthio

# Check uploads directory
docker exec zynthio-backend ls -la /app/uploads/photos/
```

---

## Git Repository

### Repository Details
- **GitHub:** `PRStartGit/AetherCoreFSM`
- **Main Branch:** `main` (production)
- **Current Commit:** `1797a76` (as of Nov 22, 2025)

### Active Branches
- `main` - Production-ready code (always deployable)
- `front-page` - Enhanced landing page (merged to main)
- `reports` - Exportable reports feature (in development)
- `feature-fix` - Profile dropdown (merged to main)

### Git Workflow
```bash
# Check current status
git status
git branch

# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "Description of changes"
git push origin feature/my-feature

# Merge to main
git checkout main
git merge feature/my-feature
git push origin main

# Deploy to production (IMPORTANT!)
docker compose build [service] && docker compose up -d [service]
```

### Git Credentials
- Configured on server with GitHub SSH keys
- Pull/push works automatically from server
- Local development: use your own GitHub credentials

---

## Application Architecture

### Backend (FastAPI + PostgreSQL)
- **Framework:** FastAPI (Python 3.11)
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Background Jobs:** Celery + Redis
- **Email:** SendGrid API
- **File Storage:** Local filesystem (`/app/uploads`)
- **API Documentation:** `http://165.22.122.116:8000/docs`

**Key Backend Paths:**
```
/root/AetherCoreFSM/backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── api/v1/                 # API endpoints
│   │   ├── auth.py            # Authentication (login, register, password reset)
│   │   ├── users.py           # User management
│   │   ├── organizations.py   # Organization CRUD
│   │   ├── sites.py           # Site management
│   │   ├── checklists.py      # Checklist operations
│   │   ├── task_fields.py     # Dynamic form fields
│   │   ├── defects.py         # Defect tracking
│   │   └── utils.py           # Photo upload, postcode lookup
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   │   └── storage.py         # File upload service
│   ├── core/
│   │   ├── config.py          # Settings and environment variables
│   │   ├── database.py        # Database connection
│   │   ├── security.py        # Password hashing, JWT tokens
│   │   └── email.py           # SendGrid email service
│   └── email_templates/       # Jinja2 HTML email templates
├── migrations/                # SQL migration scripts
├── requirements.txt           # Python dependencies
└── Dockerfile
```

### Frontend (Angular 18)
- **Framework:** Angular 18 (standalone components)
- **UI Library:** Tailwind CSS + Font Awesome icons
- **State Management:** RxJS + Services
- **Build:** Production optimized with AOT compilation

**Key Frontend Paths:**
```
/root/AetherCoreFSM/frontend/
├── src/app/
│   ├── core/
│   │   ├── auth/
│   │   │   └── auth.service.ts        # Authentication service
│   │   ├── guards/                    # Route guards (auth, role)
│   │   ├── interceptors/              # HTTP interceptors
│   │   └── services/                  # Shared services
│   ├── features/
│   │   ├── landing-page/              # Public landing page
│   │   ├── super-admin/               # Super admin dashboard
│   │   │   ├── users/                 # User management
│   │   │   ├── organizations/         # Org management
│   │   │   └── promotions/            # Promo codes
│   │   ├── org-admin/                 # Organization admin dashboard
│   │   │   ├── sites/                 # Site management
│   │   │   └── users/                 # User management
│   │   ├── site-user/                 # Site user dashboard
│   │   └── checklists/
│   │       ├── checklist-completion/  # Complete checklists
│   │       └── dynamic-task-form/     # Dynamic form renderer
│   ├── shared/
│   │   └── components/
│   │       └── main-layout/           # Header, sidebar, profile dropdown
│   └── environments/                  # Environment configs
├── nginx.conf                         # Nginx configuration
├── package.json                       # Node dependencies
└── angular.json                       # Angular config
```

### Database Schema
**Primary Tables:**
- `organizations` - Multi-tenant organizations
- `sites` - Physical locations
- `users` - User accounts (super_admin, org_admin, site_user)
- `categories` - Checklist categories (Daily, PM, etc.)
- `tasks` - Task definitions
- `task_fields` - Dynamic form fields (temperature, photo, etc.)
- `checklists` - Daily checklist instances
- `checklist_items` - Individual checklist tasks
- `task_field_responses` - User responses (including photos)
- `defects` - Issues and defects
- `password_reset_tokens` - Password reset tokens (1-hour expiry)
- `system_messages` - Broadcast messages

**Database Access:**
```bash
# Connect to database
docker exec -it zynthio-database psql -U postgres -d zynthio

# Run query
\dt  # List tables
SELECT * FROM users LIMIT 5;
SELECT * FROM sites WHERE name ILIKE '%dunfermline%';

# Check photo data
SELECT count(*) FROM task_field_responses WHERE json_value::text LIKE '%photo%';
```

---

## Environment Variables

### Backend (.env location: `/root/AetherCoreFSM/backend/.env`)
```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@database:5432/zynthio

# Security
SECRET_KEY=[GENERATED-SECRET-KEY]

# Email (SendGrid)
SENDGRID_API_KEY=[SENDGRID-API-KEY]
FROM_EMAIL=noreply@zynthio.com
FROM_NAME=Zynthio Site Monitoring

# Frontend URL (for email links)
FRONTEND_URL=http://165.22.122.116

# Redis
REDIS_URL=redis://redis:6379

# Optional: SMTP fallback
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
```

### Frontend (environment.ts)
```typescript
export const environment = {
  production: true,
  apiUrl: 'http://165.22.122.116:8000/api/v1'
};
```

---

## Deployment Workflow

### Standard Deployment Process
```bash
# 1. Make changes locally in C:\Projects\AetherCoreFSM

# 2. Copy files to server
scp "C:\Projects\AetherCoreFSM\path\to\file" zynthio:/root/AetherCoreFSM/path/to/file

# 3. Rebuild container (CRITICAL - code is copied during build!)
ssh zynthio "cd /root/AetherCoreFSM && docker compose build backend && docker compose up -d"

# 4. Verify deployment
ssh zynthio "docker logs zynthio-backend --tail 50"

# 5. Commit to Git
ssh zynthio "cd /root/AetherCoreFSM && git add . && git commit -m 'Description' && git push origin main"
```

### Quick Reference
- **Frontend changes:** Rebuild frontend container (takes ~40 seconds)
- **Backend changes:** Rebuild backend container (takes ~5 seconds)
- **Database changes:** Run migration script via `psql`
- **Restart only:** Use `docker compose restart [service]` (for config changes)
- **Rebuild:** Use `docker compose build [service]` (for code changes)

---

## Common Issues & Solutions

### Issue: Changes not visible after restart
**Cause:** Code is copied during Docker build, not at runtime
**Solution:** REBUILD the container, don't just restart
```bash
docker compose build backend
docker compose up -d backend
```

### Issue: Photos not displaying
**Causes & Solutions:**
1. Browser cache → Hard refresh (Ctrl+Shift+R)
2. Form control wiping values → Fixed in commit `df6afcf`
3. Nginx not proxying → Check `/uploads/` proxy in `nginx.conf`
4. Files not uploaded → Check `/app/uploads/photos/` directory

### Issue: Password reset not working
**Causes & Solutions:**
1. Wrong API URL → Fixed in commit `34ea4bc`
2. Email not sending → Fixed in commit `1797a76`
3. SendGrid not configured → Check `SENDGRID_API_KEY` in backend `.env`
4. Email in spam → Check user's spam folder

### Issue: Database connection failed
**Solution:**
```bash
# Check database is running
docker compose ps

# View database logs
docker compose logs database

# Restart database
docker compose restart database
```

### Issue: Git merge conflicts
**Solution:**
```bash
# Stash local changes
git stash

# Pull latest
git pull origin main

# Apply stashed changes
git stash pop

# Resolve conflicts manually
# Then commit
git add .
git commit -m "Merge conflicts resolved"
```

---

## Key Features & How They Work

### 1. Dynamic Form System
- Tasks can have custom fields (temperature, photo, yes/no, etc.)
- Repeating groups for multiple entries (e.g., 3 fridges)
- Real-time validation with temperature range checking
- Auto-defect creation for out-of-range values

**Files:**
- `backend/app/models/task_field.py` - Field definitions
- `frontend/src/app/features/checklists/dynamic-task-form/` - Form renderer

### 2. Photo Upload & Storage
- Upload endpoint: `POST /api/v1/utils/upload-photo`
- Storage: `/app/uploads/photos/` (inside backend container)
- Image optimization: Resize to max 800x800, JPEG quality 85%
- URL format: `/uploads/photos/{uuid}.jpg`

**Files:**
- `backend/app/services/storage.py` - Upload handling
- `backend/app/api/v1/utils.py` - Upload endpoint
- `frontend/nginx.conf` - Proxy `/uploads/` to backend

### 3. Email System (SendGrid)
**Available Email Types:**
- Welcome email (new users)
- Org admin welcome (new organizations)
- Password reset
- Weekly performance reports
- Defect reports

**Files:**
- `backend/app/core/email.py` - Email service
- `backend/app/email_templates/` - HTML templates

**Testing Email:**
```bash
# From server
docker exec -it zynthio-backend python -c "
from app.core.email import send_password_reset_email
send_password_reset_email(
    user_email='test@example.com',
    user_name='Test User',
    reset_url='http://example.com/reset',
    reset_code='TEST123',
    expiry_hours=1
)
"
```

### 4. Multi-Tenancy
- Organizations identified by `org_id` (e.g., "prs", "zyn")
- Sites belong to organizations
- Users belong to organizations (except super admins)
- Data isolation enforced at API level

### 5. Role-Based Access Control
**Roles:**
- `super_admin` - Full system access, manage all organizations
- `org_admin` - Manage own organization, sites, users
- `site_user` - Complete checklists, report defects

**Implementation:**
- JWT tokens with role claim
- Route guards in frontend
- API-level permission checks in backend

---

## Testing & Debugging

### Frontend Testing
```bash
# Local development
cd C:\Projects\AetherCoreFSM\frontend
npm install
ng serve

# Access at http://localhost:4200
```

### Backend Testing
```bash
# Run API tests
docker exec -it zynthio-backend pytest

# Test specific endpoint
curl -X POST http://165.22.122.116:8000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{"organization_id":"prs","username":"admin@prstart.co.uk","password":"yourpassword"}'
```

### Common Debug Commands
```bash
# Check backend logs for errors
docker logs zynthio-backend --tail 100 | grep -i error

# Check frontend build errors
docker logs zynthio-frontend --tail 50

# Monitor live logs
docker logs -f zynthio-backend

# Check database for photo data
docker exec -i zynthio-database psql -U postgres -d zynthio -c \
  "SELECT id, json_value FROM task_field_responses WHERE json_value::text LIKE '%photo%' LIMIT 5;"
```

---

## Code Style & Preferences

### General Rules
- ❌ NO emojis in code or UI (except documentation)
- ✅ Use Font Awesome icons only
- ✅ Keep trying on errors - don't give up
- ✅ Test in incognito mode to avoid cache issues
- ✅ Commit regularly with descriptive messages
- ✅ Be honest in marketing claims

### Backend Standards
- Use Pydantic schemas for validation
- Use SQLAlchemy ORM (avoid raw SQL)
- Add proper error handling and HTTP status codes
- Document endpoints with docstrings
- Use `joinedload()` for eager loading relationships
- Log important operations

### Frontend Standards
- Angular 18+ standalone components
- Component-scoped CSS (avoid global styles)
- Reactive forms for user input
- Proper loading states and error handling
- Mobile-first responsive design
- Use Tailwind utility classes

---

## Performance Optimization

### Frontend
- Production build uses AOT compilation
- Code splitting with lazy-loaded routes
- Image optimization (max 800x800, quality 85%)
- Gzip compression via nginx
- Cache static assets for 1 year

### Backend
- Connection pooling for database
- Redis caching for session data
- Async file upload with optimization
- Eager loading to prevent N+1 queries

---

## Security Considerations

### Authentication
- JWT tokens with 7-day expiration
- Password hashing with bcrypt
- Password reset tokens expire in 1 hour
- Passwords must be changed on first login

### File Upload
- Max file size: 10MB
- Allowed types: jpg, jpeg, png, gif, webp
- Files sanitized and optimized
- Unique filename (UUID) prevents overwrites

### API Security
- CORS configured for specific origins
- Rate limiting (planned)
- SQL injection prevention via ORM
- XSS prevention via Angular sanitization

---

## Backup & Recovery

### Database Backup
```bash
# Create backup
docker exec zynthio-database pg_dump -U postgres zynthio > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
docker exec -i zynthio-database psql -U postgres -d zynthio < backup_20251122.sql
```

### File Backup
```bash
# Backup uploads directory
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz /root/AetherCoreFSM/backend/uploads/

# Restore uploads
tar -xzf uploads_backup_20251122.tar.gz -C /root/AetherCoreFSM/backend/
```

### Full System Backup
```bash
# Backup everything
cd /root
tar -czf aethercore_full_backup_$(date +%Y%m%d).tar.gz AetherCoreFSM/

# Exclude node_modules and Docker volumes
tar -czf aethercore_code_backup.tar.gz \
  --exclude='node_modules' \
  --exclude='dist' \
  --exclude='__pycache__' \
  AetherCoreFSM/
```

---

## Next Steps / Roadmap

### Planned Features
- [ ] **Exportable Reports Module** (on `reports` branch)
  - PDF generation for EHO inspections
  - Date range filtering
  - Site and category filtering
  - Include photos and defect logs

- [ ] **Email Service Enhancements**
  - Daily/weekly performance reports
  - Defect notifications
  - Overdue checklist alerts

- [ ] **Mobile App**
  - React Native or Flutter
  - Offline mode for checklists
  - Push notifications

- [ ] **Advanced Analytics**
  - Compliance trends
  - Performance dashboards
  - Predictive insights

### Known Issues
- Site-user dashboard CSS exceeds budget (13.74 kB vs 12 kB) - cosmetic warning
- Optional chaining warning in main-layout component - cosmetic

---

## Support & Resources

### Documentation Locations
- **Backend README:** `/root/AetherCoreFSM/backend/README.md`
- **Frontend README:** `/root/AetherCoreFSM/frontend/README.md`
- **This Handover:** `C:\Users\neshd\Desktop\AetherCoreFSM_Handover_Updated.md`

### Quick Reference URLs
- **Production App:** http://165.22.122.116
- **API Docs (Swagger):** http://165.22.122.116:8000/docs
- **GitHub Repository:** https://github.com/PRStartGit/AetherCoreFSM

### Contact
- **Email:** hello@prstart.co.uk
- **Developer:** Claude Code (AI Assistant)

---

## Session Summary

**Date:** November 22, 2025
**Duration:** ~3 hours
**Tasks Completed:**
1. ✅ Fixed photo upload for temperature records (preserving form values)
2. ✅ Fixed password reset button URL (removed `/auth` prefix)
3. ✅ Integrated SendGrid email sending for password resets
4. ✅ Added profile dropdown to header (all user roles)
5. ✅ Updated landing page with mobile optimizations and typography fixes
6. ✅ Created comprehensive handover documentation

**Commits Made:** 4 commits to main branch
**Branches Merged:** `feature-fix`, `front-page`
**Production Deployments:** Frontend rebuilt 5 times, Backend rebuilt 2 times

---

**Document Version:** 2.0
**Last Updated By:** Claude Code
**Next Session:** Continue with Reports Module implementation
