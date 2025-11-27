# AetherCoreFSM (Zynthio) - Complete System Documentation

**Version:** 1.0
**Last Updated:** 2025-01-22
**System:** Food Safety Management & Monitoring Platform

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Database Schema](#database-schema)
4. [API Documentation](#api-documentation)
5. [Frontend Components](#frontend-components)
6. [Authentication & Authorization](#authentication--authorization)
7. [User Workflows](#user-workflows)
8. [Email Service](#email-service)
9. [File Upload System](#file-upload-system)
10. [Monitoring & Checklists](#monitoring--checklists)
11. [Security](#security)
12. [Deployment](#deployment)

---

## System Overview

### Purpose
AetherCoreFSM (branded as Zynthio) is a comprehensive food safety management platform designed for multi-site food businesses. It enables organizations to manage compliance, temperature monitoring, checklist completion, and safety protocols across multiple locations.

### Key Features
- Multi-tenant organization management
- Role-based access control (Super Admin, Org Admin, Site User)
- Dynamic checklist system with custom fields
- Temperature monitoring with photo evidence
- Real-time compliance tracking
- Activity logging and audit trails
- Trial account system with automatic expiration
- Email notifications via SendGrid
- Mobile-responsive design

### Technology Stack
- **Frontend:** Angular 18 (Standalone Components)
- **Backend:** FastAPI (Python 3.11)
- **Database:** PostgreSQL 15
- **Cache:** Redis 7
- **Email:** SendGrid API
- **Containerization:** Docker + Docker Compose
- **Web Server:** Nginx (reverse proxy)
- **Version Control:** Git

---

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Nginx (Port 80)    │
              │  Reverse Proxy       │
              └──────────┬───────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌─────────────────┐            ┌─────────────────┐
│  Angular App    │            │  FastAPI App    │
│  (Port 4200)    │◄──────────►│  (Port 8000)    │
│  Frontend       │            │  Backend API    │
└─────────────────┘            └────────┬────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                         ▼                             ▼
                ┌─────────────────┐        ┌─────────────────┐
                │  PostgreSQL     │        │     Redis       │
                │  (Port 5432)    │        │  (Port 6379)    │
                │  Database       │        │  Cache          │
                └─────────────────┘        └─────────────────┘
```

### Directory Structure

#### Backend (`/backend`)
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py              # Authentication endpoints
│   │       ├── organizations.py     # Organization CRUD
│   │       ├── sites.py            # Site management
│   │       ├── users.py            # User management
│   │       ├── checklists.py       # Checklist management
│   │       ├── monitoring.py       # Temperature monitoring
│   │       ├── reports.py          # Reporting endpoints
│   │       ├── activity_logs.py    # Activity logging
│   │       └── utils.py            # Utility endpoints (photo upload)
│   ├── core/
│   │   ├── database.py             # Database connection
│   │   ├── security.py             # Password hashing, JWT
│   │   ├── dependencies.py         # FastAPI dependencies
│   │   ├── email.py                # SendGrid email service
│   │   └── config.py               # Configuration
│   ├── models/
│   │   ├── user.py                 # User ORM model
│   │   ├── organization.py         # Organization model
│   │   ├── site.py                 # Site model
│   │   ├── checklist.py            # Checklist models
│   │   ├── task_field.py           # Dynamic field models
│   │   ├── task_field_response.py  # Response models
│   │   ├── activity_log.py         # Activity log model
│   │   └── password_reset_token.py # Password reset tokens
│   ├── schemas/
│   │   ├── auth.py                 # Auth request/response schemas
│   │   ├── user.py                 # User schemas
│   │   ├── organization.py         # Organization schemas
│   │   ├── site.py                 # Site schemas
│   │   └── monitoring.py           # Monitoring schemas
│   ├── templates/
│   │   └── emails/                 # Email HTML templates
│   │       ├── base.html
│   │       ├── org_admin_welcome.html
│   │       └── password_reset.html
│   └── main.py                     # FastAPI application entry
├── uploads/
│   └── photos/                     # Photo storage directory
├── Dockerfile
├── requirements.txt
└── alembic/                        # Database migrations
```

#### Frontend (`/frontend`)
```
frontend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── auth/
│   │   │   │   ├── auth.service.ts          # Authentication service
│   │   │   │   ├── auth.guard.ts            # Route guard
│   │   │   │   └── auth.interceptor.ts      # JWT interceptor
│   │   │   ├── models/
│   │   │   │   ├── index.ts                 # Model exports
│   │   │   │   ├── user.model.ts
│   │   │   │   ├── organization.model.ts
│   │   │   │   ├── site.model.ts
│   │   │   │   └── monitoring.model.ts
│   │   │   └── services/
│   │   │       ├── organization.service.ts
│   │   │       ├── site.service.ts
│   │   │       ├── user.service.ts
│   │   │       ├── checklist.service.ts
│   │   │       └── task-field.service.ts
│   │   ├── features/
│   │   │   ├── landing/                     # Landing page
│   │   │   ├── login/                       # Login page
│   │   │   ├── dashboard/                   # Main dashboard
│   │   │   ├── organizations/               # Org management
│   │   │   ├── sites/                       # Site management
│   │   │   ├── users/                       # User management
│   │   │   ├── checklists/                  # Checklist module
│   │   │   │   ├── checklist-list/
│   │   │   │   ├── checklist-detail/
│   │   │   │   ├── checklist-completion/
│   │   │   │   ├── dynamic-task-form/       # Dynamic form component
│   │   │   │   └── task-field-builder/      # Field builder
│   │   │   └── reports/                     # Reporting module
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   │   ├── navbar/
│   │   │   │   └── sidebar/
│   │   │   └── pipes/
│   │   └── app.routes.ts                    # Application routes
│   ├── environments/
│   │   ├── environment.ts                   # Dev environment
│   │   └── environment.prod.ts              # Prod environment
│   └── styles.scss                          # Global styles
├── Dockerfile
└── package.json
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────────┐
│   organizations     │
├─────────────────────┤
│ id (PK)            │
│ org_id (unique)    │◄─────┐
│ name               │      │
│ is_trial           │      │
│ subscription_tier  │      │
│ subscription_end   │      │
│ is_active          │      │
└─────────────────────┘      │
          ▲                  │
          │                  │
          │ 1:N              │
          │                  │
┌─────────┴───────────┐      │
│       sites         │      │
├─────────────────────┤      │
│ id (PK)            │      │
│ organization_id FK │──────┘
│ name               │
│ site_code          │
│ location           │
│ is_active          │
└─────────────────────┘
          ▲
          │
          │ 1:N
          │
┌─────────┴───────────┐
│       users         │
├─────────────────────┤
│ id (PK)            │
│ email (unique)     │
│ hashed_password    │
│ first_name         │
│ last_name          │
│ role (enum)        │
│ organization_id FK │
│ site_id FK         │
│ is_active          │
│ must_change_pwd    │
└─────────────────────┘
          ▲
          │
          │ 1:N
          │
┌─────────┴────────────────┐
│   activity_logs          │
├──────────────────────────┤
│ id (PK)                 │
│ log_type (enum)         │
│ message                 │
│ user_id FK              │
│ organization_id FK      │
│ created_at              │
└──────────────────────────┘

┌─────────────────────────┐
│     checklists          │
├─────────────────────────┤
│ id (PK)                │
│ site_id FK             │──────┐
│ name                   │      │
│ description            │      │
│ frequency (enum)       │      │
│ is_active              │      │
└─────────────────────────┘      │
          ▲                      │
          │                      │
          │ 1:N                  │
          │                      │
┌─────────┴───────────────┐      │
│   checklist_items       │      │
├─────────────────────────┤      │
│ id (PK)                │      │
│ checklist_id FK        │      │
│ task_id FK             │      │
│ item_order             │      │
└─────────────────────────┘      │
          ▲                      │
          │                      │
          │ 1:N                  │
          │                      │
┌─────────┴───────────────┐      │
│  checklist_completions  │      │
├─────────────────────────┤      │
│ id (PK)                │      │
│ checklist_id FK        │      │
│ completed_by FK        │      │
│ completed_at           │      │
│ status (enum)          │      │
└─────────────────────────┘      │
                                 │
┌─────────────────────────┐      │
│        tasks            │      │
├─────────────────────────┤      │
│ id (PK)                │      │
│ site_id FK             │──────┘
│ name                   │
│ description            │
│ category (enum)        │
│ is_template            │
└─────────────────────────┘
          ▲
          │
          │ 1:N
          │
┌─────────┴───────────────┐
│     task_fields         │
├─────────────────────────┤
│ id (PK)                │
│ task_id FK             │
│ field_name             │
│ field_type (enum)      │
│ field_order            │
│ is_required            │
│ validation_rules JSON  │
└─────────────────────────┘
          ▲
          │
          │ 1:N
          │
┌─────────┴──────────────────┐
│  task_field_responses      │
├────────────────────────────┤
│ id (PK)                   │
│ checklist_item_id FK      │
│ task_field_id FK          │
│ text_value                │
│ number_value              │
│ boolean_value             │
│ file_url                  │
│ json_value JSON           │
│ created_at                │
└────────────────────────────┘

┌─────────────────────────────┐
│  password_reset_tokens      │
├─────────────────────────────┤
│ id (PK)                    │
│ token (unique)             │
│ user_id FK                 │
│ expires_at                 │
│ used (boolean)             │
│ created_at                 │
└─────────────────────────────┘
```

### Key Tables

#### organizations
Primary tenant table for multi-organization support.
- `org_id`: Unique identifier used in login (e.g., "zynthio")
- `is_trial`: Boolean flag for trial accounts
- `subscription_end_date`: Automatic expiration for trials

#### users
User accounts with role-based access.
- **Roles:** `SUPER_ADMIN`, `ORG_ADMIN`, `SITE_USER`
- `must_change_password`: Forces password change on next login
- Super admins have `organization_id = NULL`

#### task_fields
Dynamic field definitions for checklists.
- **Field Types:** NUMBER, TEXT, TEMPERATURE, YES_NO, DROPDOWN, PHOTO, REPEATING_GROUP
- `validation_rules`: JSON column for field-specific rules (min/max, options, repeat templates)

#### task_field_responses
Stores actual data from completed checklists.
- Multiple value columns to support different data types
- `json_value`: Used for complex data like repeating groups
- Links to checklist_item (not checklist directly)

---

## API Documentation

### Base URL
- **Development:** `http://localhost:8000/api/v1`
- **Production:** `http://165.22.122.116/api/v1`

### Authentication Endpoints

#### POST `/login`
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "organization_id": "zynthio",
  "email": "admin@example.com",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "must_change_password": false
}
```

**Error Responses:**
- `401`: Invalid credentials or organization ID
- `403`: User account inactive

#### GET `/me`
Get current authenticated user details.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "admin@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "role": "ORG_ADMIN",
  "organization_id": 1,
  "site_id": null,
  "is_active": true,
  "must_change_password": false
}
```

#### POST `/forgot-password`
Request password reset email.

**Request Body:**
```json
{
  "organization_id": "zynthio",
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "If an account exists with that email, a password reset link has been sent."
}
```

**Notes:**
- Always returns success (security measure)
- Sends email via SendGrid with reset link
- Token expires in 1 hour

#### POST `/reset-password`
Reset password using token from email.

**Request Body:**
```json
{
  "token": "cXlhO7KYk8MZB5AVSXqYA7kZ9laChia7SXD93P4QKIQ",
  "new_password": "newSecurePassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Password has been successfully reset. You can now login with your new password."
}
```

**Error Responses:**
- `400`: Invalid or expired token

#### POST `/change-password`
Change password for authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "old_password": "currentPassword",
  "new_password": "newPassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

**Error Responses:**
- `400`: Current password incorrect

#### POST `/register`
Register new trial organization.

**Request Body:**
```json
{
  "company_name": "Acme Foods Ltd",
  "org_id": "acmefoods",
  "contact_person": "Jane Smith",
  "contact_email": "jane@acmefoods.com",
  "contact_phone": "+44 1234 567890",
  "address": "123 Food Street, Edinburgh",
  "admin_first_name": "Jane",
  "admin_last_name": "Smith",
  "admin_email": "jane@acmefoods.com",
  "admin_password": "tempPassword123"
}
```

**Response (201 Created):**
```json
{
  "message": "Registration successful! Check your email for login credentials.",
  "organization_id": "acmefoods",
  "trial_end_date": "2025-02-21T10:30:00Z"
}
```

**Error Responses:**
- `400`: Organization ID or email already exists

### Organization Endpoints

#### GET `/organizations`
List all organizations (Super Admin only).

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Zynthio Demo",
    "org_id": "zynthio",
    "is_trial": true,
    "subscription_tier": "premium",
    "subscription_end_date": "2025-02-15T00:00:00Z",
    "is_active": true,
    "created_at": "2025-01-15T10:00:00Z"
  }
]
```

#### POST `/organizations`
Create new organization (Super Admin only).

**Request Body:**
```json
{
  "name": "New Company Ltd",
  "org_id": "newcompany",
  "subscription_tier": "basic",
  "is_trial": false
}
```

#### GET `/organizations/{id}`
Get single organization details.

#### PUT `/organizations/{id}`
Update organization.

#### DELETE `/organizations/{id}`
Deactivate organization (soft delete).

### Site Endpoints

#### GET `/sites`
List all sites for organization.

**Query Parameters:**
- `organization_id` (optional): Filter by organization

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Edinburgh Central",
    "site_code": "EDI-001",
    "location": "123 Main St, Edinburgh",
    "organization_id": 1,
    "is_active": true
  }
]
```

#### POST `/sites`
Create new site.

**Request Body:**
```json
{
  "name": "Glasgow West",
  "site_code": "GLA-002",
  "location": "456 West St, Glasgow",
  "organization_id": 1
}
```

### User Endpoints

#### GET `/users`
List users (filtered by organization/site based on role).

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "email": "manager@zynthio.com",
    "first_name": "Sarah",
    "last_name": "Johnson",
    "full_name": "Sarah Johnson",
    "role": "SITE_USER",
    "organization_id": 1,
    "site_id": 1,
    "is_active": true
  }
]
```

#### POST `/users`
Create new user (Org Admin or Super Admin).

**Request Body:**
```json
{
  "email": "newuser@zynthio.com",
  "first_name": "Mike",
  "last_name": "Brown",
  "role": "SITE_USER",
  "site_id": 1,
  "password": "temporaryPassword123",
  "must_change_password": true
}
```

### Checklist Endpoints

#### GET `/checklists`
List checklists for site.

**Query Parameters:**
- `site_id`: Required

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "AM Temperature Check",
    "description": "Morning fridge/freezer temperatures",
    "frequency": "DAILY",
    "site_id": 1,
    "is_active": true,
    "items": [
      {
        "id": 1,
        "task_id": 5,
        "task_name": "Fridge Temperature",
        "item_order": 1
      }
    ]
  }
]
```

#### POST `/checklists/{id}/complete`
Submit completed checklist.

**Request Body:**
```json
{
  "checklist_id": 1,
  "responses": [
    {
      "checklist_item_id": 1,
      "task_field_id": 10,
      "number_value": 3.5
    },
    {
      "checklist_item_id": 1,
      "task_field_id": 11,
      "file_url": "/uploads/photos/12345.jpg"
    }
  ]
}
```

### Task Field Endpoints

#### GET `/task-fields/{task_id}`
Get all fields for a task.

**Response (200 OK):**
```json
[
  {
    "id": 10,
    "task_id": 5,
    "field_name": "Number of Fridges",
    "field_type": "NUMBER",
    "field_order": 1,
    "is_required": true,
    "validation_rules": {
      "min": 1,
      "max": 10
    }
  },
  {
    "id": 11,
    "task_id": 5,
    "field_name": "Fridge Temperatures",
    "field_type": "REPEATING_GROUP",
    "field_order": 2,
    "is_required": true,
    "validation_rules": {
      "repeat_count_field_id": 10,
      "repeat_label": "Fridge",
      "repeat_template": [
        {
          "type": "temperature",
          "label": "Temperature (°C)",
          "required": true
        },
        {
          "type": "photo",
          "label": "Photo Evidence",
          "required": false
        }
      ]
    }
  }
]
```

### Utility Endpoints

#### POST `/utils/upload-photo`
Upload photo for checklist evidence.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `file` field

**Response (200 OK):**
```json
{
  "file_url": "/uploads/photos/1737546789_abc123.jpg",
  "original_filename": "temp_reading.jpg",
  "file_size": 245678
}
```

**Notes:**
- Images auto-resized to max 1920px width
- JPEG quality set to 85%
- Filenames prefixed with timestamp

---

## Frontend Components

### Core Services

#### AuthService (`auth.service.ts`)
Manages authentication state and API calls.

**Key Methods:**
- `login(credentials)`: Authenticate and store JWT
- `logout()`: Clear auth state and redirect
- `getCurrentUser()`: Fetch authenticated user details
- `isAuthenticated()`: Check if user logged in
- `hasRole(role)`: Check user permission level
- `requestPasswordReset(data)`: Send reset email
- `resetPassword(data)`: Complete password reset
- `changePassword(data)`: Update password for authenticated user

**State Management:**
Uses RxJS `BehaviorSubject` for reactive auth state:
```typescript
interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
}
```

#### OrganizationService
CRUD operations for organizations (Super Admin only).

#### SiteService
Manage sites within organizations.

#### UserService
User management with role-based filtering.

#### ChecklistService
Checklist creation, assignment, and completion tracking.

#### TaskFieldService
Dynamic field management for tasks.

**Key Methods:**
- `getAllFields(taskId)`: Get field definitions
- `submitResponses(submission)`: Submit completed form data

### Feature Components

#### DynamicTaskFormComponent
Renders forms dynamically based on task field definitions.

**Key Features:**
- Runtime form generation from JSON configs
- Repeating group support (e.g., N fridges with N temps)
- Photo upload integration
- Real-time validation with visual feedback
- Out-of-range warnings for temperature fields

**Critical Code Pattern:**
```typescript
updateRepeatingGroups(countFieldId: number, count: number): void {
  // Find repeating fields linked to count field
  const repeatingFields = this.taskFields.filter(f =>
    f.field_type === TaskFieldType.REPEATING_GROUP &&
    f.validation_rules?.repeat_count_field_id === countFieldId
  );

  repeatingFields.forEach(field => {
    // Generate N instances
    const instances = [];
    for (let i = 0; i < count; i++) {
      instances.push({ index: i, label: `Item ${i + 1}` });
    }
    this.repeatingGroups.set(field.id, instances);

    // Create form controls for each instance
    field.validation_rules.repeat_template.forEach((template: any) => {
      for (let i = 0; i < count; i++) {
        const controlName = `field_${field.id}_${i}_${template.type}`;

        // CRITICAL: Preserve existing value during recreation
        let existingValue = '';
        if (this.dynamicForm.contains(controlName)) {
          existingValue = this.dynamicForm.get(controlName)?.value || '';
          this.dynamicForm.removeControl(controlName);
        }

        this.dynamicForm.addControl(controlName, this.fb.control(existingValue, validators));
      }
    });
  });
}
```

**Photo Upload Flow:**
1. User selects photo → triggers `onPhotoSelectedRepeating()`
2. File sent to `/api/v1/utils/upload-photo`
3. Server returns URL: `/uploads/photos/timestamp_hash.jpg`
4. URL stored in form control
5. On submit, URL saved to `task_field_responses.file_url` or `json_value.photo`

#### ChecklistCompletionComponent
Display and interact with checklists.

**Features:**
- Mark items complete/incomplete
- View completion history
- Display photos from previous completions

#### UserListComponent
User management interface.

**Features:**
- Create/edit/delete users
- Password reset functionality
- Role assignment
- Filter by site/organization

---

## Authentication & Authorization

### JWT Token Structure

Tokens contain:
```json
{
  "user_id": 1,
  "email": "admin@example.com",
  "role": "ORG_ADMIN",
  "organization_id": 1,
  "exp": 1737633600
}
```

### Token Flow

1. **Login:**
   - User submits credentials + org_id
   - Backend validates and creates JWT
   - Frontend stores token in localStorage
   - Token attached to all subsequent requests via interceptor

2. **Request Authentication:**
   - `AuthInterceptor` adds `Authorization: Bearer <token>` header
   - Backend validates token in `get_current_user()` dependency
   - Expired tokens return 401, trigger re-login

3. **Logout:**
   - Token removed from localStorage
   - Auth state cleared
   - User redirected to login page

### Role-Based Access Control

#### Super Admin (`SUPER_ADMIN`)
- Full system access
- Manage all organizations
- Create/delete organizations
- View cross-organization data

#### Org Admin (`ORG_ADMIN`)
- Manage own organization
- Create/manage sites
- Create/manage users (except super admins)
- View organization-wide reports

#### Site User (`SITE_USER`)
- Access assigned site only
- Complete checklists
- View own site data
- Cannot manage users

### Route Guards

Frontend uses `AuthGuard` to protect routes:
```typescript
{
  path: 'organizations',
  component: OrganizationListComponent,
  canActivate: [AuthGuard],
  data: { roles: ['SUPER_ADMIN'] }
}
```

Backend uses dependency injection:
```python
@router.get("/organizations")
def list_organizations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")
```

---

## User Workflows

### 1. Trial Registration Workflow

```
User visits landing page
    ↓
Fills registration form
    ↓
POST /api/v1/register
    ↓
Backend creates:
  - Organization (is_trial=true, 30-day expiry)
  - Admin user (ORG_ADMIN role)
    ↓
SendGrid welcome email sent
    ↓
User receives credentials
    ↓
User logs in with temp password
    ↓
Forced to change password (must_change_password=true)
```

### 2. Daily Temperature Check Workflow

```
Site user logs in
    ↓
Views dashboard → "AM Temperature Check" checklist
    ↓
Clicks "Start Checklist"
    ↓
Form loads with dynamic fields:
  - "How many fridges?" (NUMBER field)
  - User enters "3"
  - onCountChange() fires
    ↓
  - Repeating group generates 3 instances
  - Each instance has:
    * Temperature input (required)
    * Photo upload (optional)
    ↓
User fills in:
  - Fridge 1: 3°C, uploads photo
  - Fridge 2: 2°C, uploads photo
  - Fridge 3: -19°C, uploads photo
    ↓
Clicks "Submit"
    ↓
POST /api/v1/task-field-responses
Body includes:
{
  "checklist_item_id": 5,
  "responses": [
    {
      "task_field_id": 11,
      "json_value": [
        {"temperature": 3, "photo": "/uploads/photos/12345.jpg"},
        {"temperature": 2, "photo": "/uploads/photos/12346.jpg"},
        {"temperature": -19, "photo": "/uploads/photos/12347.jpg"}
      ]
    }
  ]
}
    ↓
Backend saves to database
    ↓
Checklist marked complete
    ↓
Activity log created
```

### 3. Password Reset Workflow

```
User clicks "Forgot Password" on login page
    ↓
Enters org_id + email
    ↓
POST /api/v1/forgot-password
    ↓
Backend:
  - Generates secure token (secrets.token_urlsafe(32))
  - Saves token to password_reset_tokens table
  - Sends email via SendGrid
    ↓
User receives email with reset link:
http://165.22.122.116/reset-password?token=abc123xyz
    ↓
User clicks link, enters new password
    ↓
POST /api/v1/reset-password
    ↓
Backend:
  - Validates token (not expired, not used)
  - Updates user.hashed_password
  - Marks token as used
    ↓
User redirected to login with new password
```

---

## Email Service

### SendGrid Integration

Configuration in `backend/app/core/email.py`:

```python
class EmailService:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@zynthio.com')
        self.from_name = os.getenv('FROM_NAME', 'Zynthio')
```

### Email Templates

Located in `backend/app/templates/emails/`:

1. **base.html**: Shared layout with Zynthio branding
2. **org_admin_welcome.html**: Trial registration welcome
3. **password_reset.html**: Password reset with link and code

### Email Functions

#### send_org_admin_welcome_email()
Sent on trial registration.

**Parameters:**
- `admin_email`: Recipient
- `contact_person`: Name
- `organization_name`: Company name
- `org_id`: Organization identifier
- `subscription_tier`: Subscription level
- `temporary_password`: Initial password
- `reset_password_url`: Login URL

#### send_password_reset_email()
Sent when user requests password reset.

**Parameters:**
- `user_email`: Recipient
- `user_name`: User's full name
- `reset_url`: Full reset link with token
- `reset_code`: First 8 chars of token (for manual entry)
- `expiry_hours`: Token validity period (default 1 hour)

### Environment Variables

Required in `.env`:
```
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxx
FROM_EMAIL=noreply@zynthio.com
FROM_NAME=Zynthio
FRONTEND_URL=http://165.22.122.116
```

---

## File Upload System

### Photo Upload Endpoint

**Location:** `backend/app/api/v1/utils.py`

**Function:** `upload_photo(file: UploadFile)`

**Process:**
1. Validate file type (image/jpeg, image/png, image/webp)
2. Generate unique filename: `{timestamp}_{random_string}.{ext}`
3. Resize image if width > 1920px (maintain aspect ratio)
4. Compress JPEG to quality=85
5. Save to `backend/uploads/photos/`
6. Return URL: `/uploads/photos/{filename}`

**Code:**
```python
from PIL import Image
import secrets
import time

@router.post("/upload-photo")
async def upload_photo(file: UploadFile = File(...)):
    # Validate content type
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Generate unique filename
    timestamp = int(time.time())
    random_str = secrets.token_hex(8)
    file_ext = file.filename.split('.')[-1]
    new_filename = f"{timestamp}_{random_str}.{file_ext}"

    # Save and optimize
    file_path = f"uploads/photos/{new_filename}"

    # Read and process image
    image = Image.open(file.file)

    # Resize if needed
    max_width = 1920
    if image.width > max_width:
        ratio = max_width / image.width
        new_size = (max_width, int(image.height * ratio))
        image = image.resize(new_size, Image.LANCZOS)

    # Save with compression
    image.save(file_path, quality=85, optimize=True)

    return {
        "file_url": f"/uploads/photos/{new_filename}",
        "original_filename": file.filename
    }
```

### Storage Structure

```
backend/uploads/photos/
├── 1737546789_abc123def456.jpg
├── 1737546790_xyz789uvw012.jpg
└── ...
```

### Nginx Configuration

Photos served by nginx:
```nginx
location /uploads/ {
    alias /app/uploads/;
    access_log off;
    expires 30d;
}
```

---

## Monitoring & Checklists

### Task Field Types

#### 1. NUMBER
Simple numeric input.
```json
{
  "field_type": "NUMBER",
  "validation_rules": {
    "min": 0,
    "max": 100
  }
}
```

#### 2. TEXT
Free text input.
```json
{
  "field_type": "TEXT",
  "validation_rules": {
    "max_length": 500
  }
}
```

#### 3. TEMPERATURE
Numeric input with temperature-specific validation.
```json
{
  "field_type": "TEMPERATURE",
  "validation_rules": {
    "min": -20,
    "max": 10
  }
}
```

#### 4. YES_NO
Boolean choice rendered as buttons.
```json
{
  "field_type": "YES_NO"
}
```

#### 5. DROPDOWN
Select from predefined options.
```json
{
  "field_type": "DROPDOWN",
  "validation_rules": {
    "options": ["Good", "Fair", "Poor"]
  }
}
```

#### 6. PHOTO
Image upload.
```json
{
  "field_type": "PHOTO"
}
```

#### 7. REPEATING_GROUP
Dynamic set of fields based on count.
```json
{
  "field_type": "REPEATING_GROUP",
  "validation_rules": {
    "repeat_count_field_id": 10,
    "repeat_label": "Fridge",
    "repeat_template": [
      {
        "type": "temperature",
        "label": "Temperature (°C)",
        "required": true
      },
      {
        "type": "photo",
        "label": "Photo Evidence",
        "required": false
      }
    ]
  }
}
```

### Response Storage

Regular fields use typed columns:
- `text_value`: TEXT, DROPDOWN
- `number_value`: NUMBER, TEMPERATURE
- `boolean_value`: YES_NO
- `file_url`: PHOTO

Repeating groups use `json_value`:
```json
[
  {
    "temperature": 3,
    "photo": "/uploads/photos/12345.jpg"
  },
  {
    "temperature": 2,
    "photo": "/uploads/photos/12346.jpg"
  }
]
```

---

## Security

### Password Security
- **Hashing:** bcrypt with automatic salt
- **Strength:** No enforced complexity (user discretion)
- **Reset Tokens:** 32-byte URL-safe random tokens
- **Token Expiry:** 1 hour for password resets
- **One-time Use:** Tokens marked as used after reset

### JWT Security
- **Algorithm:** HS256
- **Secret:** Stored in environment variable `SECRET_KEY`
- **Expiry:** 30 days (configurable)
- **Claims:** user_id, email, role, organization_id

### File Upload Security
- **Type Validation:** MIME type check (image/jpeg, image/png, image/webp)
- **Filename Sanitization:** Random generated names (prevents path traversal)
- **Size Limit:** 10MB max (FastAPI default)
- **Storage:** Outside web root, served via Nginx

### SQL Injection Prevention
- **ORM:** SQLAlchemy with parameterized queries
- **No Raw SQL:** All queries use ORM methods

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://165.22.122.116"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables
Sensitive data stored in `.env`:
- `DATABASE_URL`
- `SECRET_KEY`
- `SENDGRID_API_KEY`

**Never commit `.env` to Git!**

---

## Deployment

### Production Server

**Host:** 165.22.122.116
**OS:** Ubuntu 22.04 LTS
**Access:** SSH via Digital Ocean

### Docker Compose Services

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/zynthio
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
```

### Deployment Process

#### 1. SSH to Server
```bash
ssh root@165.22.122.116
cd /root/AetherCoreFSM
```

#### 2. Pull Latest Code
```bash
git pull origin main
```

#### 3. Rebuild Containers
```bash
# Full rebuild (after code changes)
docker compose down
docker compose build --no-cache
docker compose up -d

# Quick restart (config changes only)
docker compose restart
```

#### 4. View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

#### 5. Database Access
```bash
# Connect to PostgreSQL
docker compose exec db psql -U zynthio -d zynthio

# Example queries
SELECT * FROM organizations;
SELECT * FROM users WHERE email = 'admin@zynthio.com';
SELECT * FROM task_field_responses WHERE json_value IS NOT NULL;
```

### Environment Setup

**Backend `.env`:**
```
DATABASE_URL=postgresql://zynthio:securepassword@db:5432/zynthio
SECRET_KEY=your-secret-key-here-minimum-32-chars
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxx
FROM_EMAIL=noreply@zynthio.com
FROM_NAME=Zynthio
FRONTEND_URL=http://165.22.122.116
```

**Frontend `environment.prod.ts`:**
```typescript
export const environment = {
  production: true,
  apiUrl: 'http://165.22.122.116/api/v1'
};
```

### Nginx Configuration

**Frontend Container (`nginx.conf`):**
```nginx
server {
    listen 80;
    server_name _;

    # Frontend static files
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API proxy
    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Photo uploads proxy
    location /uploads/ {
        proxy_pass http://backend:8000/uploads/;
        access_log off;
        expires 30d;
    }
}
```

### Database Migrations

Using Alembic:
```bash
# Create migration
docker compose exec backend alembic revision --autogenerate -m "Description"

# Apply migrations
docker compose exec backend alembic upgrade head

# Rollback
docker compose exec backend alembic downgrade -1
```

### Backup Procedures

#### Database Backup
```bash
# Create backup
docker compose exec db pg_dump -U zynthio zynthio > backup_$(date +%Y%m%d).sql

# Restore backup
docker compose exec -T db psql -U zynthio zynthio < backup_20250122.sql
```

#### Photo Backup
```bash
# Copy photos from container
docker compose cp backend:/app/uploads/photos ./photos_backup_$(date +%Y%m%d)

# Restore photos
docker compose cp ./photos_backup_20250122 backend:/app/uploads/photos
```

### Monitoring

#### Health Checks
```bash
# Backend health
curl http://165.22.122.116/api/v1/health

# Database connection
docker compose exec backend python -c "from app.core.database import engine; print(engine.connect())"
```

#### Resource Usage
```bash
# Container stats
docker stats

# Disk usage
df -h
docker system df
```

---

## Troubleshooting

### Common Issues

#### 1. Photos Not Displaying
**Symptom:** Photo URLs in database but images not loading

**Check:**
```bash
# Verify files exist
docker compose exec backend ls -la /app/uploads/photos/

# Check nginx logs
docker compose logs frontend | grep uploads
```

**Solution:** Ensure nginx proxy configuration includes `/uploads/` location

#### 2. Password Reset Email Not Sending
**Symptom:** Reset requested but no email received

**Check:**
```bash
# Backend logs
docker compose logs backend | grep "PASSWORD RESET"

# Verify SendGrid API key
docker compose exec backend printenv SENDGRID_API_KEY
```

**Solution:** Ensure `SENDGRID_API_KEY` set in backend `.env`

#### 3. 401 Unauthorized Errors
**Symptom:** Requests fail with 401 after login

**Check:**
- Token in localStorage: Browser DevTools → Application → Local Storage
- Token in request headers: Network tab → Headers

**Solution:**
- Clear localStorage and re-login
- Check `AuthInterceptor` is properly configured
- Verify `SECRET_KEY` matches between backend instances

#### 4. Database Connection Refused
**Symptom:** Backend crashes with "connection refused"

**Check:**
```bash
# Database container running?
docker compose ps

# Connection string correct?
docker compose exec backend printenv DATABASE_URL
```

**Solution:** Restart database container, verify credentials

#### 5. Browser Caching After Deployment
**Symptom:** Code changes not visible after deployment

**Solution:**
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- Clear browser cache
- Implement cache-busting with versioned filenames (future improvement)

---

## Performance Considerations

### Database Indexing
Key indexes:
- `users.email` (unique)
- `organizations.org_id` (unique)
- `task_field_responses.checklist_item_id`
- `task_field_responses.task_field_id`
- `activity_logs.user_id`

### Query Optimization
- Use `select_related()` for foreign keys
- Paginate large lists (implement offset/limit)
- Filter at database level, not in Python

### Frontend Optimization
- Lazy load feature modules
- Implement virtual scrolling for long lists
- Cache static assets (Nginx expires headers)
- Minimize bundle size (check with `ng build --stats-json`)

### Image Optimization
- Resize on upload (max 1920px)
- JPEG compression (quality 85)
- Consider WebP format for modern browsers

---

## Future Enhancements

### Short Term
1. **Notifications:** Browser push notifications for incomplete checklists
2. **Reporting:** PDF export of compliance reports
3. **Mobile App:** Native iOS/Android apps using Ionic/React Native
4. **Offline Mode:** Service workers for offline checklist completion

### Medium Term
1. **Multi-language:** i18n support for international clients
2. **Custom Branding:** White-label options for enterprise clients
3. **Advanced Analytics:** Dashboard with charts and trends
4. **Integration:** API webhooks for third-party systems

### Long Term
1. **AI-Powered:** Anomaly detection for temperature readings
2. **IoT Integration:** Direct sensor feeds for automated monitoring
3. **Blockchain:** Immutable audit trail for compliance
4. **Mobile SDK:** Embed checklist functionality in client apps

---

## Glossary

**Organization:** Top-level tenant in multi-tenant system
**Site:** Physical location (e.g., restaurant, kitchen) within organization
**Checklist:** Set of tasks to be completed regularly (daily, weekly, etc.)
**Task:** Individual item within checklist (e.g., "Check fridge temperature")
**Task Field:** Input element within task (e.g., number input, photo upload)
**Repeating Group:** Dynamic field set that scales based on count (e.g., N fridges)
**Activity Log:** Audit trail of user actions
**Trial Account:** Time-limited organization with automatic expiration
**Super Admin:** System administrator with cross-organization access
**Org Admin:** Organization administrator with site/user management
**Site User:** Regular user limited to assigned site

---

## Support & Contact

**Developer:** Claude (Anthropic AI)
**Project Owner:** hello@prstart.co.uk
**Production Server:** 165.22.122.116
**Repository:** Private Git repository

For technical support or feature requests, contact the project owner.

---

**Document Version:** 1.0
**Last Updated:** 2025-01-22
**Next Review:** As needed for major system changes
