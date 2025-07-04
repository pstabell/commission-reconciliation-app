# Project Rules and Conventions

## 📁 Backup File Management

### Rule: All backup files MUST be stored in the `app_backups/` folder

**Why:** Keeps the main project directory clean and organized.

**How to create backups:**
```bash
# ❌ DON'T do this:
cp commission_app.py commission_app_backup_20250703.py

# ✅ DO this instead:
cp commission_app.py app_backups/commission_app_backup_$(date +%Y%m%d_%H%M%S).py
```

**What goes in app_backups/:**
- All `commission_app*.py` backup files
- Database backup files (`*.db`)
- Folder backups (like `pages_backup_*`)
- Any other timestamped backups

**Naming convention for backups:**
- Python files: `commission_app_backup_YYYYMMDD_HHMMSS.py`
- Database files: `commissions_backup_YYYYMMDD_HHMMSS.db`
- Folders: `foldername_backup_YYYYMMDD_HHMMSS/`

## 📝 Documentation Standards

### Consolidated Documentation
- Avoid creating multiple files for the same topic
- Update existing documentation rather than creating new files
- Use these main documentation files:
  - `CURRENT_STATE.md` - Current status and setup
  - `PROJECT_HISTORY.md` - All updates and changes
  - `SUPABASE_MIGRATION_GUIDE.md` - Database documentation
  - Specific feature files as needed

## 🔐 Security Rules

### Environment Variables
- **NEVER** commit `.env` files to version control
- Always use environment variables for sensitive data
- Document required environment variables in setup guides

### Database Credentials
- Store in `.env` file only
- Never hardcode credentials in source files
- Use `.gitignore` to exclude sensitive files

## 🎨 Code Style

### Python Code
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and single-purpose

### Streamlit Specific
- Use `st.cache_data` for data caching
- Clear cache after data modifications
- Use session state sparingly
- Provide user feedback for all actions

## 🗄️ Database Operations

### Data Integrity
- Always generate unique Transaction IDs for new records
- Archive deleted records before removal
- Validate data before database operations
- Use transactions for multi-step operations

### Backup Strategy
- Regular backups before major changes
- Archived deletions in `deleted_policies` table
- Export functionality for user data backup

## 📂 Project Structure

```
SALES COMMISSIONS APP/
├── commission_app.py          # Main application
├── column_mapping_config.py   # Column configuration
├── .env                       # Environment variables (not in git)
├── commissions.db            # SQLite database (legacy)
├── backup_app.sh             # Backup utility script
├── start_app.bat             # Windows startup script
├── requirements.txt          # Python dependencies
├── packages.txt              # System packages
├── *.md                      # Documentation files
├── app_backups/              # All backup files (18 files)
│   ├── commission_app_backup_*.py
│   ├── commissions_backup_*.db
│   └── pages_backup_*/
├── sql_scripts/              # SQL schemas and migrations (13 files)
│   ├── schema_postgresql*.sql
│   ├── create_deleted_policies_table.sql
│   └── [other SQL files]
├── migration_scripts/        # Database migration tools (9 files)
│   ├── migrate_to_supabase.py
│   ├── supabase_config.py
│   └── [other migration scripts]
├── utility_scripts/          # Fix scripts and utilities (21 files)
│   ├── fix_*.py
│   ├── check_*.py
│   ├── test_*.py
│   └── [other utility scripts]
├── archive/                  # Old versions and deprecated files (10 files)
│   ├── commission_app_original.py
│   ├── commission_app_v2_refactored.py
│   ├── start_modular_app.bat
│   └── [other old versions]
├── config_files/             # Configuration files
│   ├── column_mapping.json
│   └── schema_info.json
├── logs_and_temp/            # Log files and temporary files
│   └── commission_app.log
├── chromedriver-win64/       # Chrome driver for automation
├── help_content/             # Help documentation
├── utils/                    # Utility modules
└── venv/                     # Python virtual environment
```

## 📁 Folder Organization Rules

### What goes where:
- **Root directory**: Only active, essential files
- **app_backups/**: All timestamped backups
- **sql_scripts/**: SQL files for schemas, migrations, imports
- **migration_scripts/**: Python scripts for database migrations
- **utility_scripts/**: One-time fixes, tests, analysis tools
- **archive/**: Old versions, deprecated code
- **config_files/**: JSON configuration files, schema exports
- **logs_and_temp/**: Log files, temporary files, lock files

## 🚀 Development Workflow

1. **Before making changes:** Create a timestamped backup in `app_backups/`
2. **During development:** Test all changes thoroughly
3. **After changes:** Update relevant documentation
4. **Before committing:** Ensure no sensitive data is included

---
*Last updated: July 3, 2025*