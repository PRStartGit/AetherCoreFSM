# Setup Instructions

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
python -m pip install -r requirements.txt
```

### 2. Seed the Database

```bash
python seed_db.py
```

### 3. Run the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### 4. Test Login Credentials

**Super Admin:**
- Organization ID: `vig` (or any org)
- Email: `admin@riskproof.com`
- Password: `admin123`

**Viva Italia Group Admin:**
- Organization ID: `vig`
- Email: `admin@vivaitaliagroup.com`
- Password: `password123`

**Best Restaurants Ltd Admin:**
- Organization ID: `brl`
- Email: `admin@bestrestaurants.co.uk`
- Password: `password123`

**Safe Food Chain Admin:**
- Organization ID: `sfc`
- Email: `admin@safefoodchain.com`
- Password: `password123`

## Frontend Setup (Angular)

### 1. Create Angular Project

```bash
cd frontend
npm install -g @angular/cli
ng new . --routing --style=scss
```

### 2. Install Angular Material

```bash
ng add @angular/material
```

### 3. Run Development Server

```bash
ng serve
```

The app will be available at `http://localhost:4200`

## Testing the API

### Example Login Request

```bash
curl -X POST "http://localhost:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": "vig",
    "email": "admin@vivaitaliagroup.com",
    "password": "password123"
  }'
```

This will return a JWT token that you can use for authenticated requests.

### Example Authenticated Request

```bash
curl -X GET "http://localhost:8000/api/v1/organizations" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Database

The SQLite database file (`riskproof.db`) will be created in the `backend` directory when you run the seed script or start the server.

## Next Steps

1. Test all API endpoints using the interactive docs at `/docs`
2. Set up the Angular frontend
3. Implement the Monitoring Module (Phase 2)
4. Build the dashboards (Phase 3)
5. Add subscription management (Phase 4)
6. Deploy to production (Phase 5)
