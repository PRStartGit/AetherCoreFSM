# Security Documentation

## Overview

RiskProof implements enterprise-grade security features to protect sensitive data and ensure secure multi-tenant operations.

## Security Features

### 1. Password Security
- **Bcrypt Hashing**: All passwords are hashed using bcrypt with automatic salt generation
- **Password Complexity**: Enforced through application-level validation
- **No Plain Text Storage**: Passwords are never stored in plain text
- **Implementation**: `app/core/security.py` using `passlib` with bcrypt

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

### 2. Authentication & Authorization

#### JWT Token-Based Authentication
- **Token Generation**: Secure JWT tokens with configurable expiration
- **Token Storage**: Client-side secure storage (localStorage with HttpOnly consideration)
- **Token Validation**: Every API request validates the JWT token
- **Implementation**: `app/core/security.py` using `python-jose`

**Token Payload**:
```json
{
  "user_id": 123,
  "exp": "2024-01-01T12:00:00Z"
}
```

#### Role-Based Access Control (RBAC)
Three distinct user roles with hierarchical permissions:

1. **Super Admin** (`super_admin`)
   - Full system access
   - Manage all organizations
   - Create/edit/delete any resource
   - Not tied to any specific organization

2. **Organization Admin** (`org_admin`)
   - Full access within their organization
   - Manage sites, users, and monitoring data
   - Create categories and tasks
   - View organization-wide reports
   - **Multiple org admins per organization supported**

3. **Site User** (`site_user`)
   - Access limited to assigned sites
   - Complete checklists
   - Report defects
   - View site-specific data

**Permission Enforcement**:
```python
# Super Admin only
@router.get("/organizations")
def get_organizations(current_user: User = Depends(get_current_super_admin)):
    ...

# Org Admin or above
@router.get("/sites")
def get_sites(current_user: User = Depends(get_current_org_admin)):
    ...
```

### 3. Multi-Tenant Data Isolation

#### Organization-Level Isolation
- Each organization's data is completely isolated
- Database queries automatically filter by `organization_id`
- Cross-organization data access is prevented at the database level

#### Implementation Strategy:
1. **Database Model Level**:
   - All tenant-specific tables include `organization_id` foreign key
   - Super admin resources have `organization_id = NULL`

2. **API Level**:
   - Automatic organization filtering in query parameters
   - User's organization validated against requested resources
   - Super admins bypass organization filtering

3. **Code Examples**:
```python
# Sites endpoint - automatic organization filtering
def get_sites(
    organization_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Site)

    # Non-super admins can only see their org's sites
    if current_user.role != UserRole.SUPER_ADMIN:
        query = query.filter(Site.organization_id == current_user.organization_id)
    elif organization_id:
        query = query.filter(Site.organization_id == organization_id)

    return query.all()
```

### 4. API Security

#### HTTP Interceptor (Frontend)
- Automatically injects JWT token in all API requests
- Handles 401 Unauthorized responses
- Redirects to login on authentication failure

```typescript
// auth.interceptor.ts
intercept(request, next) {
  const token = this.authService.getToken();
  if (token) {
    request = request.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }
  return next.handle(request);
}
```

#### CORS Configuration
- Configured to allow frontend origin
- Credentials support enabled
- Secure headers enforced

```python
# FastAPI CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. Input Validation

#### Pydantic Schemas
- All API inputs validated using Pydantic models
- Type checking and data validation
- SQL injection prevention through ORM

```python
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    full_name: str
    role: UserRole
```

### 6. Session Management

- JWT tokens have configurable expiration (default: 60 minutes)
- Refresh token mechanism can be implemented
- Logout clears client-side tokens
- Server-side token blacklist can be added for enhanced security

### 7. Database Security

#### SQLAlchemy ORM
- Prevents SQL injection through parameterized queries
- Prepared statements for all database operations
- Input sanitization at ORM level

#### Connection Security
- Connection strings stored in environment variables
- No credentials in source code
- `.env` file excluded from version control

### 8. Multiple Org Admins Support

The system fully supports multiple organization administrators per organization:

**Database Design**:
- No unique constraint on `organization_id` for org_admin role
- Multiple users can have `role = 'org_admin'` for the same organization

**Use Cases**:
- Large organizations with multiple administrators
- Regional admins for different geographical areas
- Functional admins (safety, quality, operations)

**Creating Additional Org Admins**:
```python
# Via API (Super Admin or existing Org Admin)
POST /api/v1/users
{
  "email": "admin2@organization.com",
  "password": "SecurePassword123!",
  "first_name": "Second",
  "last_name": "Admin",
  "role": "org_admin",
  "organization_id": 1
}
```

### 9. Audit Trail (Future Enhancement)

Planned security features:
- User action logging
- Login attempt tracking
- Data change history
- Suspicious activity detection

## Initial Setup Security

### Super Admin Creation

The initial super admin is created using a secure seed script:

```bash
python backend/seed_initial_admin.py
```

**Credentials**:
- Email: hello@prstart.co.uk
- Initial Password: ChangeMe123!
- **MUST be changed on first login**

**Email Notification**:
- Welcome email sent with credentials
- Security best practices included
- Password change reminder

## Security Checklist

### Development
- [x] Passwords hashed with bcrypt
- [x] JWT authentication implemented
- [x] Role-based access control active
- [x] Multi-tenant isolation enforced
- [x] Input validation with Pydantic
- [x] SQL injection prevention (ORM)
- [ ] Rate limiting (TODO)
- [ ] Request logging (TODO)

### Production Deployment
- [ ] HTTPS/SSL enabled
- [ ] Environment variables secured
- [ ] Database credentials rotated
- [ ] SendGrid API key configured
- [ ] CORS origins restricted
- [ ] JWT secret key randomized
- [ ] Database backups enabled
- [ ] Monitoring and alerting setup

## Security Contacts

For security concerns or vulnerability reports:
- Email: security@riskproof.com
- Response Time: 24 hours

## Compliance

RiskProof is designed to support:
- GDPR data protection requirements
- ISO 27001 security controls
- SOC 2 compliance requirements
- Industry-specific safety regulations

## Updates

This security documentation is maintained alongside code updates. Last reviewed: 2025-11-13
