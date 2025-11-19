# Dashboard Stability Notice

## ⚠️ CRITICAL: DO NOT MODIFY DASHBOARD CODE WITHOUT THOROUGH TESTING

All three dashboard implementations are now **stable and working correctly** as of November 19, 2025.

### Working Dashboards:

1. **Super Admin Dashboard** (`/super-admin`)
   - Location: `frontend/src/app/features/super-admin/dashboard/`
   - Shows: Organizations, sites, users, checklists, defects, performance metrics
   - Schema: `backend/app/schemas/dashboard.py` - `SuperAdminDashboard`

2. **Org Admin Dashboard** (`/org-admin`)
   - Location: `frontend/src/app/features/org-admin/org-admin-dashboard/`
   - Shows: Site details, RAG status, completion rates, defects, recent activity
   - Schema: `backend/app/schemas/dashboard.py` - `OrgAdminDashboard`

3. **Site User Dashboard** (`/site-user`)
   - Location: `frontend/src/app/features/site-user/site-user-dashboard/`
   - Shows: Checklists, tasks, defects, multi-site selection dropdown
   - Schema: Standard checklist/defect models

### Important Notes:

- **Schema Consistency**: The backend schemas in `backend/app/schemas/dashboard.py` have been carefully aligned with what the endpoints return. Changing field names or adding/removing fields can break the frontend.

- **Multi-Site Support**: Site user dashboard now supports users with multiple sites via a dropdown selector. This required careful initialization flow: `loadUserSites()` → `loadCategories()` → `loadChecklists()`.

- **Navigation Menu**: Each role has specific menu items in `frontend/src/app/shared/components/main-layout/main-layout.component.ts`. Super Admin and Org Admin have different user management routes.

### Before Making Changes:

1. **Test on development branch first**
2. **Verify all three dashboards still load and display data**
3. **Check browser console for errors**
4. **Test with users of different roles (super_admin, org_admin, site_user)**
5. **If schema changes are needed, update BOTH backend AND frontend simultaneously**

### Common Issues to Avoid:

- ❌ Adding fields to schemas without providing them in the API response
- ❌ Changing field names in schemas without updating frontend components
- ❌ Modifying navigation menu without checking all role types
- ❌ Breaking the initialization flow in site-user dashboard
- ❌ Using hardcoded site index instead of selectedSiteId in site-user dashboard

### Recent Fixes Applied:

- Fixed SuperAdminDashboard schema having incorrect fields (removed `sites_by_rag`, `total_checklists_today`)
- Added multi-site dropdown to site-user dashboard
- Fixed duplicate Users menu item for super admin
- Fixed organization dropdown for org admins when creating users
- Resolved Python module caching issues requiring container rebuild

---

**If you must modify dashboard code, create a backup branch first and test thoroughly!**

Generated: November 19, 2025
