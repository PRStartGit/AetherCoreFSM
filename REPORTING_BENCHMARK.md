# Reporting System Benchmark

## ✅ WORKING - Reporting Features Stable

**Date:** November 19, 2025
**Status:** Reporting system functional and tested

---

## Working Features

### 1. ✅ Daily Reports
- **Endpoint:** `POST /api/v1/reports/daily/{site_id}`
- **Authentication:** Requires super admin token
- **Functionality:**
  - Generates report for yesterday's data
  - Sends to all recipients in `site.report_recipients`
  - Shows accurate completion rates and task counts
  - Lists defects from yesterday
  - Category performance breakdown

### 2. ✅ Weekly Reports
- **Endpoint:** `POST /api/v1/reports/weekly/{site_id}`
- **Authentication:** Requires super admin token
- **Functionality:**
  - Generates report for current week (last 7 days ending today)
  - Sends to all recipients in `site.report_recipients`
  - Shows accurate completion rates and task counts
  - Lists defects from the week
  - Category performance breakdown

### 3. ✅ Test Report Endpoint
- **Endpoint:** `POST /api/v1/reports/test-weekly-email`
- **Functionality:** Sends sample report with dummy data for testing

### 4. ✅ Email Subjects
- **Daily:** "Daily Performance Report - Monday, 18th November 2025"
- **Weekly:** "Weekly Performance Report - 2025-11-13 to 2025-11-19"
- Format automatically adjusts based on date range

### 5. ✅ Data Accuracy
- **Fixed:** Status enum comparison bug (was comparing string to enum)
- **Solution:** Using `ChecklistStatus.COMPLETED` instead of `'COMPLETED'`
- Reports now show correct completion counts

### 6. ✅ Dynamic Completion Colors
- **Red** (< 80%): Red background and border (#fee2e2, #ef4444)
- **Orange** (80-99%): Orange background and border (#fed7aa, #f97316)
- **Green/Blue** (100%): Success background and border
- Colors automatically adjust based on completion rate

### 7. ✅ Site Profile Configuration
- Daily report enable/disable toggle
- Daily report time picker
- Weekly report enable/disable toggle
- Weekly report day selector (Monday-Sunday)
- Weekly report time picker
- Report recipients field (comma-separated emails)

---

## Test Data - Test Site (ID: 11)

### Report Date: November 18, 2025
- **Site:** Test site
- **Checklists:** 6 out of 14 completed (42.9%)
- **Items:** 12 out of 31 completed
- **Defects:** 1 reported
- **Recipients:** hello@prstart.co.uk

### Manual Test Script
To send a test daily report:
```bash
ssh zynthio "docker exec zynthio-backend python /app/send_daily_report_fixed.py"
```

---

## File Locations

### Backend Files
- **Reports API:** `backend/app/api/v1/reports.py`
- **Email Service:** `backend/app/core/email.py`
- **Email Template:** `backend/app/email_templates/weekly_performance_overall.html`
- **Checklist Model:** `backend/app/models/checklist.py` (ChecklistStatus enum)

### Frontend Files
- **Site Form:** `frontend/src/app/features/org-admin/sites-form/`
  - Component: `sites-form.component.ts`
  - Template: `sites-form.component.html` (lines 213-308: Email Reporting section)

### Test Scripts
- **Daily Report Script:** `/tmp/send_daily_report_fixed.py` (on server)

---

## Database Configuration

### Sites Table - Report Fields
```sql
daily_report_enabled    BOOLEAN
daily_report_time       VARCHAR  (HH:MM format)
weekly_report_enabled   BOOLEAN
weekly_report_day       INTEGER  (1-7 for Mon-Sun)
weekly_report_time      VARCHAR  (HH:MM format)
report_recipients       TEXT     (comma-separated emails)
```

### Example Query
```sql
SELECT id, name, daily_report_enabled, daily_report_time,
       weekly_report_enabled, weekly_report_day, weekly_report_time,
       report_recipients
FROM sites WHERE id = 11;
```

---

## Known Issues

### 1. ⚠️ Email Template Colors
- **Issue:** Email client caching may show green colors instead of blue
- **Workaround:** Colors are configurable via template, need to verify client-side rendering
- **Status:** Deferred for now

### 2. ⚠️ Scheduled Reports Not Yet Implemented
- **Current:** Manual API calls only
- **Needed:** Celery scheduled tasks to send reports automatically at configured times
- **Status:** Feature planned, not implemented

---

## API Usage Examples

### Send Daily Report
```bash
# Get auth token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password","organization_id":"org_code"}' \
  | jq -r .access_token)

# Send daily report for site 11
curl -X POST "http://localhost:8000/api/v1/reports/daily/11" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

### Send Weekly Report
```bash
curl -X POST "http://localhost:8000/api/v1/reports/weekly/11" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

---

## Email Template Features

### Layout
- Email-client compatible HTML (table-based layout)
- Inline styles only (no external CSS)
- ZYNTHIO logo as text (email-safe)
- Responsive width (600px)

### Sections
1. **Header:** Brand colors, logo, organization name, date
2. **Completion Rate Card:** Large percentage with dynamic colors
3. **Progress Bar:** Visual completion indicator
4. **Stats Grid:** Completed tasks and defects count
5. **Category Performance:** Breakdown by category
6. **Defects List:** Up to 5 recent defects
7. **Key Insights:** Recommendations and summary
8. **Footer:** Branding and copyright

---

## Testing Checklist

- [x] Daily report generates with correct date (yesterday)
- [x] Weekly report generates with correct date range (current week)
- [x] Email subject line correct for daily vs weekly
- [x] Completion rate calculates correctly
- [x] Completion colors change based on percentage
- [x] Progress bar displays correctly
- [x] Category performance shows accurate percentages
- [x] Defects list includes correct defects
- [x] Email sends to all recipients in comma-separated list
- [x] Site form includes all report configuration fields
- [ ] Scheduled automated reports (not yet implemented)

---

## Next Steps (Not Implemented)

1. **Automated Scheduling**
   - Create Celery scheduled tasks
   - Read site configuration (daily_report_time, weekly_report_day, etc.)
   - Automatically send reports at configured times

2. **Email Template Refinement**
   - Finalize brand colors (blue vs green)
   - Test across multiple email clients
   - Add company logo image (if available)

3. **Enhanced Reporting**
   - Add charts/graphs (if email client supports)
   - Trend analysis (week-over-week comparisons)
   - Customizable report sections

---

## Critical Notes

- **Do not modify** `ChecklistStatus` enum comparison logic without testing
- **Always test** email templates in multiple clients (Gmail, Outlook, Apple Mail)
- **Backup before changes** to email template or report endpoints
- **Status field** is an enum - use `ChecklistStatus.COMPLETED`, not string `'COMPLETED'`

---

**Generated:** November 19, 2025, 18:45 UTC
**Last Tested:** November 19, 2025
**Test Site:** Test site (ID: 11)
**Test Email:** hello@prstart.co.uk
