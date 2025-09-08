# Agent Commission Tracker - Project Structure Documentation

## Overview
This document clarifies the complete project structure of the Agent Commission Tracker application, including all components and deployment configurations.

**Last Updated**: January 2025  
**Version**: 4.3.0

## Project Repository Structure

### Main Application Repository
**Location**: `/commission-reconciliation-app` (GitHub: `pstabell/commission-reconciliation-app`)  
**Deployment**: Render.com (commission-tracker-app)

```
commission-reconciliation-app/
├── commission_app.py          # Main Streamlit application
├── webhook_server.py          # Stripe webhook handler (Flask app)
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (local only)
├── Logo/                     # Application branding assets
├── docs/                     # Comprehensive documentation
├── backups/                  # Versioned code backups
├── app_backups/              # Historical application backups
├── archive/                  # Archived code versions
├── migration_scripts/        # Database migration scripts
└── utils/                    # Utility modules
    ├── auth_helpers.py       # Authentication & subscription logic
    ├── email_utils.py        # Email sending functionality
    ├── column_mapping_config.py  # Data mapping configuration
    └── (other utility files)
```

## Important Notes About Project Structure

### 1. Single Repository Architecture
**CRITICAL**: Unlike many projects, this application uses a **single repository** for all components:
- Main Streamlit application (`commission_app.py`)
- Webhook server (`webhook_server.py`)
- All utility files and configurations

### 2. Webhook Server Location
The webhook server (`webhook_server.py`) is **NOT** a separate repository. It lives in the same repository as the main application:
- Path: `/webhook_server.py` (root level)
- Deployed as a separate web service on Render
- Shares utility files like `email_utils.py` and `auth_helpers.py`

### 3. Multiple Render Services from One Repository
From this single GitHub repository, we deploy **two separate services** on Render:

#### a. Main Application Service
- **Name**: commission-tracker-app
- **Type**: Web Service
- **Start Command**: `streamlit run commission_app.py --server.port $PORT`
- **URL**: https://commission-tracker-app.onrender.com

#### b. Webhook Service
- **Name**: commission-tracker-webhook
- **Type**: Web Service  
- **Start Command**: `gunicorn webhook_server:app`
- **URL**: https://commission-tracker-webhook.onrender.com

Both services:
- Pull from the same GitHub repository
- Auto-deploy on push to main branch
- Share the same codebase but run different entry points

## File Categories

### Core Application Files
- `commission_app.py` - Main application entry point
- `webhook_server.py` - Stripe webhook handler
- `requirements.txt` - Python dependencies
- `CLAUDE.md` - AI assistant guidelines

### Authentication & User Management
- `auth_helpers.py` - Login, registration, subscription checks
- `email_utils.py` - Email sending (welcome, password reset, etc.)

### Configuration
- `column_mapping_config.py` - Field mapping configurations
- `.env` (local only) - Environment variables

### Documentation (`/docs`)
- `/core` - Architecture, history, project structure
- `/features` - Feature documentation
- `/guides` - User and developer guides
- `/operations` - Development and deployment guides
- `/production` - SaaS and production documentation
- `/legal` - Terms of service, privacy policy

### Backup Directories
- `/backups` - Recent timestamped backups
- `/app_backups` - Historical application versions
- `/archive` - Deprecated code versions

## Environment Variables

### Production Environment
Required for both services:
```
# Database
PRODUCTION_SUPABASE_URL=your_supabase_url
PRODUCTION_SUPABASE_ANON_KEY=your_supabase_key

# Stripe (for webhook service)
STRIPE_SECRET_KEY=your_stripe_secret
STRIPE_WEBHOOK_SECRET=your_webhook_secret
STRIPE_PRICE_ID=your_price_id

# Email (SMTP)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=your_sendgrid_api_key
FROM_EMAIL=Support@AgentCommissionTracker.com

# Application
APP_ENVIRONMENT=PRODUCTION
RENDER_APP_URL=https://commission-tracker-app.onrender.com
```

## Common Confusion Points

### 1. Webhook Server is NOT External
The webhook server code (`webhook_server.py`) is part of the main repository, not a separate project. When debugging webhook issues:
- Edit `webhook_server.py` in the main repository
- Commit and push to GitHub
- Render will auto-deploy the webhook service

### 2. Shared Utility Files
Both the main app and webhook server import from the same utility files:
- `from email_utils import send_password_setup_email`
- `from auth_helpers import generate_setup_token`

This is why they must be in the same repository.

### 3. Deployment Flow
1. Make changes to any file (e.g., `webhook_server.py`)
2. Commit and push to GitHub: `git push`
3. Both Render services detect the push
4. Each service rebuilds and deploys independently
5. Main app updates if `commission_app.py` or dependencies changed
6. Webhook updates if `webhook_server.py` or dependencies changed

## Development Best Practices

### 1. Testing Webhook Changes Locally
```bash
# Run webhook server locally
python webhook_server.py

# Test with curl or Postman
curl http://localhost:10000/health
```

### 2. Testing Main App Locally
```bash
# Run Streamlit app
streamlit run commission_app.py
```

### 3. Making Changes
- Always check which file contains the code you need to modify
- Remember that webhook logic is in `webhook_server.py`, not the main app
- Utility functions shared between services go in their respective files

### 4. Debugging Webhook Issues
1. Check Render webhook service logs
2. Verify environment variables are set in Render
3. Ensure webhook URL in Stripe matches Render URL
4. Test the `/health` endpoint to verify deployment

## Version History
- **v4.3.0** (2025-01) - SaaS implementation with Stripe integration
- **v4.2.0** (2025-01) - Free trial and password setup flow
- **v4.1.0** (2024-12) - Multi-tenancy preparation
- **v3.9.32** (2024-08) - Commission rules management
- **v3.5.x** (2024-07) - Reconciliation system enhancements

## Support
For issues or questions about the project structure:
1. Check this documentation first
2. Review `/docs/operations/TROUBLESHOOTING_GUIDE.md`
3. Check GitHub issues
4. Contact development team

---
*This document helps prevent confusion about the project's single-repository architecture where multiple services are deployed from the same codebase.*