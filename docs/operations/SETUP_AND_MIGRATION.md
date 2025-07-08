# Setup and Migration Guide
**Last Updated**: July 7, 2025  
**Purpose**: Comprehensive guide for setting up and migrating the Sales Commission App

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Supabase Migration](#supabase-migration)
3. [Git Setup](#git-setup)
4. [Environment Configuration](#environment-configuration)
5. [Data Migration](#data-migration)
6. [Troubleshooting Setup Issues](#troubleshooting-setup-issues)

---

## Initial Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Supabase account (free tier works)
- Windows with WSL2 (recommended) or Mac/Linux

### Quick Start
```bash
# Clone the repository
git clone https://github.com/pstabell/commission-reconciliation-app.git
cd commission-reconciliation-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.template .env
# Edit .env with your credentials

# Run the app
streamlit run commission_app.py
```

---

## Supabase Migration

### Why Supabase?
- Free tier supports our needs
- Real-time capabilities
- Better than local SQLite for team access
- Automatic backups

### Migration Steps

#### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create new project "Sales Commission Tracker"
3. Save your credentials:
   - Project URL
   - Anon Key
   - Service Role Key (keep secure!)

#### 2. Import Schema
```sql
-- Run in Supabase SQL Editor
CREATE TABLE policies (
    _id TEXT PRIMARY KEY,
    "Client ID" TEXT,
    "Customer" TEXT,
    "Policy Number" TEXT,
    "Transaction ID" TEXT UNIQUE,
    "Premium Sold" NUMERIC,
    "Agency Estimated Comm/Revenue (CRM)" NUMERIC,
    "Policy Gross Comm %" NUMERIC,
    "Agent Estimated Comm $" NUMERIC,
    -- ... (full schema in archive)
);

-- Create indexes
CREATE INDEX idx_transaction_id ON policies("Transaction ID");
CREATE INDEX idx_customer ON policies("Customer");
CREATE INDEX idx_policy_number ON policies("Policy Number");
```

#### 3. Configure Environment
```bash
# .env file
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
APP_PASSWORD=YourSecurePassword
```

#### 4. Migrate Data
```python
# Use migration script
python migration_scripts/migrate_to_supabase.py
```

### Verification
1. Check Supabase dashboard for data
2. Run app and verify connectivity
3. Test CRUD operations

---

## Git Setup

### Repository Structure
```
commission-reconciliation-app/
├── commission_app.py          # Main application
├── requirements.txt           # Dependencies
├── .env.template             # Environment template
├── .gitignore               # Git ignore rules
├── docs/                    # Documentation
├── utils/                   # Utility modules
├── config_files/           # Configuration files
└── help_content/          # User help files
```

### Git Configuration
```bash
# Set up git
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create feature branch
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "feat: Description of changes"

# Push to GitHub
git push origin feature/your-feature
```

### Important Git Rules
- **NEVER commit .env file**
- Always use .gitignore
- Create backups before major changes
- Use meaningful commit messages

---

## Environment Configuration

### Required Environment Variables
```bash
# Supabase Configuration
SUPABASE_URL=your_project_url
SUPABASE_ANON_KEY=your_anon_key

# App Security
APP_PASSWORD=YourSecurePassword

# Optional
DEBUG=false
LOG_LEVEL=INFO
```

### Streamlit Configuration
Create `.streamlit/secrets.toml`:
```toml
[supabase]
url = "your_project_url"
key = "your_anon_key"

[app]
password = "YourSecurePassword"
```

### Virtual Environment Best Practices
```bash
# Always activate venv before working
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Update requirements after installing packages
pip freeze > requirements.txt
```

---

## Data Migration

### From Excel/CSV
1. Prepare your data:
   - Ensure column headers match expected format
   - Clean data (no special characters in headers)
   - Save as CSV

2. Use Import Feature:
   - Go to "Import Data" in app
   - Upload CSV file
   - Map columns
   - Review and import

### From Legacy Database
```python
# Example migration script
import pandas as pd
from sqlalchemy import create_engine

# Read from old database
old_engine = create_engine('sqlite:///old_commissions.db')
df = pd.read_sql('SELECT * FROM policies', old_engine)

# Transform data
df['Transaction ID'] = df['Transaction ID'].apply(generate_id)
df['_id'] = df['Transaction ID']  # Supabase primary key

# Upload to Supabase
# (Use the app's import feature or direct API)
```

### Data Validation
- Check for duplicate Transaction IDs
- Verify numeric fields
- Ensure required fields populated
- Test formulas calculate correctly

---

## Troubleshooting Setup Issues

### Common Issues

#### 1. Module Import Errors
```bash
# Error: ModuleNotFoundError
# Solution:
pip install -r requirements.txt
```

#### 2. Streamlit Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall streamlit
pip uninstall streamlit
pip install streamlit==1.28.0
```

#### 3. Database Connection Failed
- Verify .env file exists
- Check Supabase credentials
- Ensure no extra spaces in .env
- Test connection separately

#### 4. Permission Denied Errors
```bash
# Windows WSL issues
chmod +x start_app.sh

# Or use Python directly
python -m streamlit run commission_app.py
```

### Environment-Specific Issues

#### Windows
- Use WSL2 for better compatibility
- Path issues: use forward slashes
- Long path names: enable in Windows

#### Mac
- Install Xcode command line tools
- Use homebrew for Python

#### Linux
- Install python3-dev package
- May need additional system libraries

### Getting Help
1. Check [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)
2. Review [KNOWN_ISSUES_AND_FIXES.md](KNOWN_ISSUES_AND_FIXES.md)
3. Create GitHub issue with:
   - Error message
   - Environment details
   - Steps to reproduce

---

*This guide consolidates SUPABASE_MIGRATION_GUIDE.md, GIT_GUIDE.md, and setup instructions from various sources.*