# Email Templates Documentation

This directory contains HTML email templates for Zynthio Site Monitoring Platform. These templates are designed to be populated with dynamic data using a template engine like Jinja2 or Mustache.

## Available Templates

### 1. Organization Admin Welcome (`org_admin_welcome.html`)
**Purpose**: Welcome email sent when a new organization is created and an admin account is set up.

**Variables**:
- `contact_person` - Name of the contact person
- `organization_name` - Name of the organization
- `org_id` - Unique organization identifier
- `subscription_tier` - Subscription plan (e.g., "Professional", "Enterprise")
- `contact_email` - Organization contact email
- `admin_email` - Admin user's login email
- `temporary_password` - Initial password for first login
- `reset_password_url` - URL to password reset page

**Use Case**: Triggered when super admin creates a new organization.

---

### 2. User Welcome (`user_welcome.html`)
**Purpose**: Welcome email sent when a new user account is created.

**Variables**:
- `user_name` - Full name of the user
- `organization_name` - Name of their organization
- `user_role` - Role (e.g., "Org Admin", "Site User")
- `assigned_sites` - List of sites they're assigned to
- `user_email` - User's login email
- `temporary_password` - Initial password
- `login_url` - URL to login page
- `role_permissions` - HTML list of permissions based on role

**Use Case**: Triggered when org admin or super admin creates a new user.

---

### 3. Password Reset (`password_reset.html`)
**Purpose**: Email sent when user requests a password reset.

**Variables**:
- `user_name` - User's full name
- `user_email` - User's email
- `reset_url` - Password reset link with token
- `reset_code` - Numeric code (optional, for 2FA)
- `expiry_hours` - How long the reset link is valid (e.g., "24")

**Use Case**: Triggered when user clicks "Forgot Password".

---

### 4. Weekly Performance Overall (`weekly_performance_overall.html`)
**Purpose**: Comprehensive weekly report for organization administrators showing overall performance across all sites.

**Variables**:
- `recipient_name` - Recipient's name
- `organization_name` - Organization name
- `week_start` - Start date (e.g., "Jan 15, 2025")
- `week_end` - End date
- `completion_rate` - Overall completion percentage
- `completion_trend` - "positive" or "negative"
- `completion_change` - Change text (e.g., "+5%")
- `total_tasks` - Total tasks assigned
- `completed_tasks` - Number completed
- `active_defects` - Number of open defects
- `defects_severity` - CSS class ("warning" or "danger")
- `new_defects` - New defects this week
- `total_sites` - Total sites monitored
- `active_sites` - Number of active sites
- `top_sites` - Array of top performing sites
- `attention_sites` - Array of sites needing attention
- `category_stats` - Array of task categories with stats
- `insights` - Array of AI-generated insights
- `dashboard_url` - Link to dashboard
- `report_date` - Report generation date

**Use Case**: Sent automatically every Monday morning to org admins.

---

### 5. Weekly Performance Per Site (`weekly_performance_per_site.html`)
**Purpose**: Detailed weekly report for a specific site.

**Variables**:
- `recipient_name` - Recipient's name
- `site_name` - Name of the site
- `organization_name` - Organization name
- `week_start` - Start date
- `week_end` - End date
- `completion_rate` - Site completion percentage
- `completion_class` - CSS class based on performance
- `tasks_completed` - Tasks completed
- `total_tasks` - Total tasks
- `active_defects` - Number of defects
- `defects_class` - CSS class for defect status
- `tasks_pending` - Pending tasks count
- `tasks_overdue` - Overdue tasks count
- `category_breakdown` - Array of categories with stats
- `recent_tasks` - Array of recently completed tasks
- `has_defects` - Boolean flag
- `defects` - Array of active defects
- `upcoming_tasks` - Array of scheduled tasks
- `recommendations` - Array of improvement suggestions
- `site_dashboard_url` - Link to site dashboard
- `report_date` - Report generation date

**Use Case**: Sent weekly to site managers and org admins.

---

### 6. Defect List Report (`defect_list_report.html`)
**Purpose**: Comprehensive defects report organized by priority and date.

**Variables**:
- `recipient_name` - Recipient's name
- `organization_name` - Organization name
- `report_period` - Report period (e.g., "Weekly", "Monthly")
- `critical_count` - Number of critical defects
- `high_count` - Number of high priority defects
- `medium_count` - Number of medium priority defects
- `low_count` - Number of low priority defects
- `total_defects` - Total active defects
- `new_this_week` - New defects this week
- `resolved_this_week` - Resolved defects this week
- `avg_resolution_time` - Average resolution time in days
- `critical_defects` - Array of critical priority defects
- `high_defects` - Array of high priority defects
- `medium_defects` - Array of medium priority defects
- `low_defects` - Array of low priority defects
- `defects_dashboard_url` - Link to defects dashboard
- `total_sites` - Total sites in organization
- `report_date` - Report generation date

**Defect Object Structure**:
```javascript
{
  defect_id: "1234",
  title: "Broken door lock",
  site_name: "Main Office",
  reported_date: "Jan 10, 2025",
  age_days: "5",
  status: "open" | "in-progress" | "resolved",
  status_class: "open" | "in-progress" | "resolved",
  description: "Full description text",
  reported_by: "John Doe",
  category: "Safety & Security"
}
```

**Use Case**: Sent weekly to org admins, or on-demand.

---

## Template Engine Integration

### Using with Jinja2 (Python)

```python
from jinja2 import Environment, FileSystemLoader
import os

# Setup Jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'email_templates')
env = Environment(loader=FileSystemLoader(template_dir))

# Load and render template
template = env.get_template('org_admin_welcome.html')
html_content = template.render(
    contact_person="John Doe",
    organization_name="Acme Corp",
    org_id="ACME001",
    # ... other variables
)

# Send email (using your email service)
send_email(
    to="admin@acme.com",
    subject="Welcome to Zynthio!",
    html_body=html_content
)
```

### Using with Mustache (JavaScript)

```javascript
const Mustache = require('mustache');
const fs = require('fs');

// Load template
const template = fs.readFileSync('./email_templates/user_welcome.html', 'utf8');

// Render
const html = Mustache.render(template, {
  user_name: "Jane Smith",
  organization_name: "Acme Corp",
  user_role: "Site User",
  // ... other variables
});

// Send email
sendEmail({
  to: 'jane@acme.com',
  subject: 'Welcome to Zynthio!',
  html: html
});
```

## Color Scheme

The templates use a consistent color scheme:

- **Primary Blue**: `#3b82f6` (Organizations, general)
- **Success Green**: `#10b981` (Completions, positive metrics)
- **Warning Orange**: `#f59e0b` (Alerts, moderate issues)
- **Danger Red**: `#ef4444` (Critical issues, defects)
- **Purple**: `#8b5cf6` (Site-specific reports)
- **Indigo**: `#6366f1` (Performance reports)

## Styling Notes

- All templates are responsive and mobile-friendly
- Inline CSS for maximum email client compatibility
- Tested with major email clients (Gmail, Outlook, Apple Mail)
- Dark mode optimized
- Print-friendly styles included

## Future Enhancements

Consider adding:
- Multi-language support
- Organization branding customization
- Custom logo integration
- White-label options
- SMS templates for critical alerts
- Slack/Teams integration templates

## Maintenance

When updating templates:
1. Test across multiple email clients
2. Validate HTML (inline CSS required for emails)
3. Update this README with new variables
4. Version control all changes
5. Test with sample data before deployment

---

**Last Updated**: 2025-01-15
**Maintainer**: Development Team
**Contact**: dev@zynthio.com
