# SendGrid Email Service Setup Guide

This guide explains how to configure SendGrid for the Zynthio platform to send transactional emails (welcome emails, password resets, weekly reports, etc.).

## Why SendGrid?

SendGrid is a reliable email service provider that:
- Provides better deliverability than Gmail SMTP
- Handles high email volumes without throttling
- Provides detailed analytics and tracking
- Offers domain authentication for improved inbox placement
- Has a generous free tier (100 emails/day)

## Prerequisites

1. **SendGrid Account**
   - Sign up at https://sendgrid.com/ if you don't have an account
   - Complete the account verification process

2. **Domain Authentication**
   - You need to authenticate your sending domain (zynthio.com)
   - This requires adding DNS records to your domain provider

## Step-by-Step Setup

### 1. Get Your SendGrid API Key

1. Log into SendGrid: https://app.sendgrid.com/
2. Navigate to **Settings** → **API Keys**
3. Click **Create API Key**
4. Name your key (e.g., "Zynthio Production")
5. Select **Full Access** or at minimum:
   - Mail Send → Full Access
6. Click **Create & View**
7. **IMPORTANT:** Copy the API key immediately - you won't see it again!

### 2. Authenticate Your Domain

1. Go to **Settings** → **Sender Authentication** → **Domains**
2. Click **Authenticate Your Domain**
3. Select your DNS provider
4. Enter `zynthio.com` as your domain
5. SendGrid will generate CNAME records
6. Add these records to your DNS provider (see DNS Records section below)
7. Wait for DNS propagation (can take 24-48 hours)
8. Click **Verify** in SendGrid once DNS records are live

### 3. Configure Your Application

#### Local Development (.env file)

Add these lines to your `backend/.env` file:

```env
# SendGrid Configuration (Primary Email Service)
SENDGRID_API_KEY=SG.your_actual_api_key_here

# Email Settings
FROM_EMAIL=hello@zynthio.com
FROM_NAME=Zynthio Site Monitoring

# Optional: Keep SMTP as fallback
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_gmail@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_TLS=True
SMTP_SSL=False
```

#### Production (.env file on server)

SSH into your production server and update the `.env` file:

```bash
ssh root@your-server-ip
cd AetherCoreFSM/backend
nano .env
```

Add the same configuration as above, then restart the backend:

```bash
cd ..
docker compose restart backend
```

### 4. Verify DNS Records

You need to add these DNS records to your domain provider (the exact values will be provided by SendGrid):

**Example DNS Records** (your actual values will be different):

| Type  | Host/Name                          | Value                                      | TTL  |
|-------|-----------------------------------|-------------------------------------------|------|
| CNAME | em1234.zynthio.com                | u1234567.wl123.sendgrid.net               | 3600 |
| CNAME | s1._domainkey.zynthio.com         | s1.domainkey.u1234567.wl123.sendgrid.net  | 3600 |
| CNAME | s2._domainkey.zynthio.com         | s2.domainkey.u1234567.wl123.sendgrid.net  | 3600 |

**Important Notes:**
- DNS records should be added to the **root domain** (zynthio.com), not the www subdomain
- DNS propagation can take 24-48 hours
- You can check DNS propagation at https://dnschecker.org/

### 5. Test Your Configuration

Run the test script to verify everything is working:

```bash
# Navigate to backend directory
cd backend

# Run the test script
python test_sendgrid_email.py
```

The script will:
1. Check if SendGrid API key is configured
2. Check if SMTP is configured (fallback)
3. Optionally send a test email to verify it works

## How It Works

The email service now works with automatic fallback:

1. **Primary**: If `SENDGRID_API_KEY` is configured, use SendGrid API
2. **Fallback**: If SendGrid not configured, use SMTP (Gmail)
3. **Error**: If neither configured, email sending will be disabled (with warnings in logs)

### Code Changes

The following files were modified to add SendGrid support:

- `backend/app/core/email.py:91-127` - Added `send_email_sendgrid()` method
- `backend/app/core/email.py:143-148` - Modified `send_template_email()` to prefer SendGrid
- `backend/app/core/config.py:46` - SendGrid API key configuration already existed

### Email Functions Available

All existing email functions now use SendGrid automatically:

- `send_welcome_email()` - Welcome email for new site users
- `send_org_admin_welcome_email()` - Welcome email for organization admins
- `send_super_admin_welcome_email()` - Welcome email for super admin
- `send_password_reset_email()` - Password reset emails
- `send_weekly_performance_email()` - Weekly performance reports
- `send_defect_report_email()` - Defect list reports

## Troubleshooting

### "SendGrid API key not configured" Error

**Solution:** Check your `.env` file has `SENDGRID_API_KEY=your_key_here` and restart the backend.

### "Domain not authenticated" Error

**Solution:**
1. Verify DNS records are correctly added to your domain provider
2. Wait 24-48 hours for DNS propagation
3. Check propagation at https://dnschecker.org/
4. Click "Verify" in SendGrid dashboard

### Emails Going to Spam

**Solution:**
1. Ensure domain authentication is complete
2. Set up SPF, DKIM, and DMARC records (SendGrid provides these)
3. Warm up your sending domain by starting with low volume
4. Ensure your FROM_EMAIL matches your authenticated domain

### Rate Limits

**Free Tier Limits:**
- 100 emails per day
- Good for development and small deployments

**If you need more:**
- Upgrade to SendGrid Essentials: $19.95/month for 50,000 emails/month
- Or use SMTP fallback for some emails

## Monitoring

### Check Email Delivery

1. Log into SendGrid: https://app.sendgrid.com/
2. Go to **Activity** to see all sent emails
3. Check delivery status, opens, clicks, bounces, etc.

### Application Logs

Check backend logs for email sending attempts:

```bash
docker logs zynthio-backend | grep -i email
```

## Security Best Practices

1. **Never commit `.env` files to git** - they contain secrets
2. **Use separate API keys** for development and production
3. **Rotate API keys** regularly (every 90 days recommended)
4. **Restrict API key permissions** - only give Mail Send access
5. **Monitor API usage** in SendGrid dashboard for unusual activity

## Support

- **SendGrid Documentation**: https://docs.sendgrid.com/
- **SendGrid Support**: https://support.sendgrid.com/
- **DNS Checker**: https://dnschecker.org/
- **MX Toolbox (Email Testing)**: https://mxtoolbox.com/

## Quick Reference

### Environment Variables

```env
SENDGRID_API_KEY=SG.your_api_key
FROM_EMAIL=hello@zynthio.com
FROM_NAME=Zynthio Site Monitoring
```

### Test Email Sending

```bash
python backend/test_sendgrid_email.py
```

### Restart Backend

```bash
docker compose restart backend
```

### Check Logs

```bash
docker logs zynthio-backend -f
```

## Next Steps

1. ✅ Get SendGrid API key
2. ✅ Add API key to `.env` file
3. ✅ Authenticate domain in SendGrid
4. ✅ Add DNS records to domain provider
5. ✅ Wait for DNS propagation
6. ✅ Run test script to verify
7. ✅ Deploy to production
8. ✅ Monitor email delivery in SendGrid dashboard

---

**Last Updated:** 2025-11-17
**Version:** 1.0
**Commit:** 262e94e
