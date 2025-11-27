-- Migration: Add organization-wide email report fields
-- Date: 2025-11-27

-- Add org-wide email report fields to organizations table
ALTER TABLE organizations ADD COLUMN IF NOT EXISTS org_report_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE organizations ADD COLUMN IF NOT EXISTS org_report_day INTEGER DEFAULT 1;
ALTER TABLE organizations ADD COLUMN IF NOT EXISTS org_report_time VARCHAR(10) DEFAULT '09:00';
ALTER TABLE organizations ADD COLUMN IF NOT EXISTS org_report_recipients TEXT;

-- Add comment for documentation
COMMENT ON COLUMN organizations.org_report_enabled IS 'Enable organization-wide weekly reports';
COMMENT ON COLUMN organizations.org_report_day IS 'Day of week for org reports (1=Monday, 7=Sunday)';
COMMENT ON COLUMN organizations.org_report_time IS 'Time to send org reports (HH:MM format)';
COMMENT ON COLUMN organizations.org_report_recipients IS 'Comma-separated email addresses for org reports';
