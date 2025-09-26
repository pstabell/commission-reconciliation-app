# Commission Tracker Documentation Index

Welcome to the Commission Tracker documentation! This index helps you quickly find the information you need.

## 📁 Documentation Structure

### Core Documentation
- [Project Architecture](core/APP_ARCHITECTURE.md) - System design and structure
- [Project History](core/PROJECT_HISTORY.md) - Development timeline
- [Change Log](core/CHANGELOG.md) - Version history and updates
- [Project Structure](core/PROJECT_STRUCTURE.md) - File and folder organization

### 🔧 Development & Operations
- [CLAUDE.md](/CLAUDE.md) - **CRITICAL: Development instructions for AI assistants**
- [Development Standards](operations/DEVELOPMENT_STANDARDS.md) - Code quality guidelines
- [Database Migrations](operations/DATABASE_MIGRATIONS.md) - Schema change procedures
- [Troubleshooting Guide](operations/TROUBLESHOOTING_GUIDE.md) - Common issues and solutions
- [Known Issues](operations/KNOWN_ISSUES_AND_FIXES.md) - Current bugs and workarounds

### 🛡️ Security
- [User Isolation Model](security/USER_ISOLATION_SECURITY_MODEL.md) - Multi-tenant security
- [RLS Troubleshooting](operations/RLS_TROUBLESHOOTING.md) - Row Level Security issues
- [Security Guidelines](development/SECURITY_GUIDELINES.md) - Best practices

### 📋 Features
- [Contacts Import/Export](features/CONTACTS_COMMISSION_STRUCTURE.md) - Manage carriers/MGAs
- [Policy Term Rules](features/MASTER_POLICY_TERM_RULES.md) - Transaction assignment logic
- [Reconciliation System](features/RECONCILIATION_SYSTEM.md) - Statement matching
- [Commission Rules](features/COMMISSION_RULES_MANAGEMENT.md) - Rate configuration
- [Color Theme Preferences](features/COLOR_THEME_PREFERENCES.md) - UI customization
- [Empty Data Handling](features/EMPTY_DATA_HANDLING_SUMMARY.md) - New user experience
- [Formula System](features/FORMULA_SYSTEM.md) - Commission calculations
- [Policy Revenue Ledger](features/Policy Revenue Ledger Reports.md) - Financial reporting

### 🐛 Troubleshooting (Recent Issues)
- [Mobile Data Visibility](troubleshooting/MOBILE_FIX_SUMMARY_2025.md) - Sidebar issues
- [CSV Import/RLS Issues](troubleshooting/CSV_IMPORT_RLS_ISSUES_2025.md) - Import failures
- [Missing Carriers/MGAs](troubleshooting/MISSING_CARRIERS_MGAS_2025.md) - Data visibility
- [Contacts Data Issues](troubleshooting/contacts-data-visibility-issues.md) - Demo account

### 📅 Recent Changes (2025)
- [2025-09-22: Complete User Isolation & Security Overhaul v5.0.0](changelogs/2025-09-22-complete-user-isolation-security-overhaul.md) - **MAJOR UPDATE**
- [2025-09-19: Contacts Import/Export Fix](changelogs/2025-09-19-contacts-import-export-fix.md)
- [2025-09-18: Color Theme Preferences](changelogs/2025-09-18-color-theme-preferences.md)
- [2025-09-18: Demo User MGA Fix](changelogs/2025-09-18-demo-user-mga-visibility-fix.md)
- [2025-09-14: Reconciliation DateTime Fix](changelogs/2025-09-14-reconciliation-datetime-fix.md)
- [2025-09-09: Webhook DateTime Fix](changelogs/2025-09-09-webhook-datetime-fix.md)
- [2025-09-07: Carrd AI Bot Integration](changelogs/2025-09-07-carrd-ai-bot-integration.md)
- [2025-09-07: Free Trial Password Flow](changelogs/2025-09-07-free-trial-password-flow.md)

### 📚 Help Content
- [Getting Started](../help_content/01_getting_started.md)
- [Features Guide](../help_content/02_features_guide.md)  
- [Tips and Tricks](../help_content/03_tips_and_tricks.md)
- [Troubleshooting](../help_content/04_troubleshooting.md)
- [Formulas](../help_content/05_formulas.md)
- [FAQ](../help_content/06_faq.md)
- [Data Protection](../help_content/07_data_protection.md)
- [Roadmap](../help_content/08_roadmap.md)

### 🏢 Production/SaaS
- [Multi-Tenancy Implementation](production/MULTI_TENANCY_IMPLEMENTATION.md)
- [SaaS Master Plan](production/SAAS_MASTER_PLAN_STATUS.md)

### 📐 Design
- [UI Design Standards](design/UI_DESIGN_STANDARDS.md)
- [Add Policy Form Redesign](design/ADD_POLICY_FORM_REDESIGN.md)
- [Page Designs](design/PAGE_DESIGNS/) - Individual page specifications

### 📜 Legal
- [Privacy Policy](legal/privacy_policy.md)
- [Terms of Service](legal/terms_of_service.md)

## 🚀 Quick Links

### For Developers
1. **START HERE**: [CLAUDE.md](/CLAUDE.md) for critical development instructions
2. Review [Development Standards](operations/DEVELOPMENT_STANDARDS.md)
3. Check [Known Issues](operations/KNOWN_ISSUES_AND_FIXES.md) before starting
4. Understand [User Isolation Model](security/USER_ISOLATION_SECURITY_MODEL.md)

### For Troubleshooting
1. Check [Recent Changelogs](changelogs/) for similar issues
2. Review [Troubleshooting Guide](operations/TROUBLESHOOTING_GUIDE.md)
3. Search specific issue in [troubleshooting/](troubleshooting/) folder
4. Check [CLAUDE.md](/CLAUDE.md) for known recurring issues

### For New Features
1. Review existing [Features Documentation](features/)
2. Follow [Development Standards](operations/DEVELOPMENT_STANDARDS.md)
3. Document in appropriate changelog when complete
4. Update this README if adding major features

## 🔍 Search Tips

Use grep to search across all documentation:
```bash
# Search for a specific term
grep -r "search_term" docs/

# Search for files containing a pattern
find docs -name "*.md" -exec grep -l "pattern" {} \;

# Search in specific folders
grep -r "RLS" docs/troubleshooting/
```

## 📝 Documentation Standards

1. **Changelogs**: Use format `YYYY-MM-DD-brief-description.md`
2. **Troubleshooting**: Include error message, root cause, solution, prevention
3. **Features**: Include overview, technical details, usage examples
4. **Always update** documentation when resolving issues or adding features
5. **Archive old files** instead of deleting to preserve history

## 🗂️ Archive Organization

Historical documentation is preserved in:
- `/archive/daily_summaries/` - Daily development logs
- `/archive/old_versions/` - Superseded documentation
- `/archive/phase0_implementation/` - Historical implementation details

Temporary scripts are archived in:
- `/archive/temp_scripts/` - One-time use scripts
- `/archive/debug_scripts/` - Debugging and analysis scripts
- `/sql_scripts/archive/` - Organized by category (demo_fixes, rls_fixes, etc.)

---

Last updated: 2025-01-19 (Complete reorganization and cleanup)