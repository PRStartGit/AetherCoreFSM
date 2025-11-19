# Fallback Commit Reference Point

## ⚠️ STABLE BASELINE - USE THIS IF THINGS GO WRONG

**Commit Hash**: `252aa27`
**Date**: November 19, 2025
**Branch**: `main`
**Message**: "Fix: Correct email service parameters in test weekly report endpoint"

## Status at This Commit:

### ✅ Working Features:
1. **Super Admin Dashboard** - Fully functional, showing all metrics
2. **Org Admin Dashboard** - Displaying site details, RAG status, completion rates
3. **Site User Dashboard** - Working with multi-site dropdown selector
4. **User Management** - All CRUD operations working for super admin and org admin
5. **Navigation Menus** - Correct menu items for all user roles
6. **Multi-Site Support** - Site users can switch between assigned sites

### ⚠️ Known Issues:
1. **Weekly Email Reports** - Template syntax mismatch (Mustache vs Jinja2)
   - Template uses `{{#top_sites}}` (Mustache syntax)
   - Email service uses Jinja2 which requires `{% for %}` syntax
   - Error: "unexpected char '#' at 7554" in weekly_performance_overall.html
   - **Action Needed**: Convert email templates from Mustache to Jinja2 syntax

2. **Organization Reports Email** - Field not yet implemented
   - Current: Only `contact_email` field exists in organizations table
   - **Action Needed**: May need to add `reports_email` field or clarify if using `contact_email`

### How to Revert to This Commit:

```bash
# On local machine
cd AetherCoreFSM
git checkout 252aa27

# On production server
ssh zynthio
cd /root/AetherCoreFSM
git fetch origin
git reset --hard 252aa27
docker compose build backend frontend
docker compose up -d
```

### File Versions at This Commit:
- **Dashboard Components**: All three dashboards stable and tested
- **Navigation**: `frontend/src/app/shared/components/main-layout/main-layout.component.ts`
- **Site User Dashboard**: `frontend/src/app/features/site-user/site-user-dashboard/`
- **User Management**: `frontend/src/app/features/super-admin/users/`
- **Reports Endpoint**: `backend/app/api/v1/reports.py`
- **Email Service**: `backend/app/core/email.py`

### Critical Notes:
- All dashboards are STABLE - do not modify without thorough testing
- See `DASHBOARD_STABILITY.md` for detailed dashboard documentation
- Email templates need Jinja2 conversion before weekly reports will work
- Backend uses Jinja2 (`Template` from `jinja2`)
- Email templates use Mustache syntax (incompatible)

---

**Generated**: November 19, 2025
**Last Verified**: November 19, 2025, 16:55 UTC
