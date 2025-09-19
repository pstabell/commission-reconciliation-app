## CRITICAL DEVELOPMENT INSTRUCTIONS FOR CLAUDE

### 1. Troubleshooting Protocol
- **After 3 failed attempts** to solve any issue, ALWAYS search and read ALL .md files in the docs folder
- Use commands like: `grep -r "error_keyword" docs/` or `find docs -name "*.md" -exec grep -l "issue_pattern" {} \;`
- Previous issues and their solutions are documented - don't reinvent the wheel!

### 2. Documentation Requirements
- **When user confirms an issue is resolved**, IMMEDIATELY create or update the relevant .md file
- Location: `/docs/troubleshooting/` for bugs, `/docs/changelogs/` for fixes
- Include: Error message, root cause, solution, prevention tips
- Use format: `YYYY-MM-DD-brief-description.md`

### 3. Code Organization & Cleanup Standards
- **Temporary scripts**: Move to `archive/temp_scripts/` after use
- **Debug scripts**: Move to `archive/debug_scripts/` when done
- **SQL scripts**: Organize in `sql_scripts/archive/` by category (demo_fixes, rls_fixes, debug, migration)
- **Excel/CSV files**: Never commit user data files to repo
- **Backups**: Use timestamped backups in `app_backups/` folder
- **Clean regularly**: After resolving issues, archive all temporary files created

### 4. Development Best Practices
- **Never use `except: pass`**: Always log or handle exceptions properly
- **Test imports thoroughly**: When adding import/export features, verify ALL data transfers correctly
- **Debug exports first**: If import fails, check if export included all expected data
- **Email normalization**: Always use `get_normalized_user_email()` for user email comparisons
- **No hardcoded values**: Use config files for defaults (see config_files/ folder)

### 5. Known Recurring Issues
- **UnboundLocalError with datetime**: Check `/docs/changelogs/2025-01-09-webhook-datetime-fix.md`
- **Mobile data visibility**: Check `/docs/troubleshooting/MOBILE_FIX_SUMMARY_2025.md`
- **CSV Import / RLS**: Check `/docs/troubleshooting/CSV_IMPORT_RLS_ISSUES_2025.md`
- **Demo data isolation**: Check `/docs/changelogs/2025-01-19-contacts-import-export-feature.md`
- **Missing MGA associations**: Export logic must preserve mga_id relationships

## Policy Term Transaction Rules

- Transactions can only exist in ONE policy term to avoid duplication
- A transaction is unique and cannot physically exist in two policy terms
- Transactions falling on an X-DATE should go on the renewing policy term (Policy term 2)
- ALL transactions with an effective date within a policy term must follow consistent rules
- Master Policy Term Rules are designed to be unbreakable

## CRITICAL SECURITY FIXES (January 13-19, 2025)

### Cache Poisoning Issue - RESOLVED
- **Problem**: Users could see other users' data due to global caching
- **Solution**: Removed ALL caching from `load_policies_data()`
- **Impact**: Slightly slower but 100% secure data isolation
- **Lesson**: NEVER use `@st.cache_data` for user-specific data

### Complete User Isolation - RESOLVED
- **Problem**: Users shared carriers, MGAs, and commission rules
- **Solution**: Added user_email column to ALL tables with complete isolation
- **Implementation**: See `/docs/security/USER_ISOLATION_SECURITY_MODEL.md`
- **Import/Export**: Users can now manage their own contacts data independently

### RLS and CSV Import Issues - RESOLVED
- **Problem**: RLS blocking imports due to auth mismatch
- **Solution**: Modified RLS policies to work with anon key
- **Key Learning**: App uses custom auth, not Supabase Auth
- **Service Role Key Issue**: Still unresolved in Render

**Full Details**: See `/docs/troubleshooting/CSV_IMPORT_RLS_ISSUES_2025.md`

## Recent Updates (v4.2.0 - January 19, 2025)

1. **Contacts Import/Export Feature**:
   - Added new tab in Tools page for complete contacts management
   - Users can export/import carriers, MGAs, and commission rules
   - Full data isolation between users
   - See: `/docs/changelogs/2025-01-19-contacts-import-export-feature.md`

2. **Color Theme Preferences**:
   - Users can choose between light and dark blue color schemes
   - Preference saved per user in config_files/user_preferences.json
   - See: `/docs/changelogs/2025-01-18-color-theme-preferences.md`

3. **Configurable Default Agent Commission Rates**:
   - Added "Default Agent Rates" tab in Admin Panel
   - Users can now modify default new business (50%) and renewal (25%) rates
   - Rates stored in config_files/default_agent_commission_rates.json
   - Add New Policy form loads rates from config instead of hardcoding

4. **Mobile Sidebar Fix**: 
   - Disabled all custom CSS to allow Streamlit's native mobile behavior
   - Mobile users can now properly collapse/expand sidebar