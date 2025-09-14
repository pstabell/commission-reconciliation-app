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

### 3. Known Recurring Issues
- **UnboundLocalError with datetime**: Check `/docs/changelogs/2025-01-09-webhook-datetime-fix.md`
- **Mobile data visibility**: Check `/docs/troubleshooting/MOBILE_FIX_SUMMARY_2025.md`
- **CSV Import / RLS**: Check `/docs/troubleshooting/CSV_IMPORT_RLS_ISSUES_2025.md`

## Policy Term Transaction Rules

- Transactions can only exist in ONE policy term to avoid duplication
- A transaction is unique and cannot physically exist in two policy terms
- Transactions falling on an X-DATE should go on the renewing policy term (Policy term 2)
- ALL transactions with an effective date within a policy term must follow consistent rules
- Master Policy Term Rules are designed to be unbreakable

## CRITICAL SECURITY FIXES (January 13, 2025)

### Cache Poisoning Issue - RESOLVED
- **Problem**: Users could see other users' data due to global caching
- **Solution**: Removed ALL caching from `load_policies_data()`
- **Impact**: Slightly slower but 100% secure data isolation
- **Lesson**: NEVER use `@st.cache_data` for user-specific data

### RLS and CSV Import Issues - RESOLVED
- **Problem**: RLS blocking imports due to auth mismatch
- **Solution**: Modified RLS policies to work with anon key
- **Key Learning**: App uses custom auth, not Supabase Auth
- **Service Role Key Issue**: Still unresolved in Render

**Full Details**: See `/docs/troubleshooting/CSV_IMPORT_RLS_ISSUES_2025.md`

## Recent Updates (v4.1.0 - January 6, 2025)

1. **Configurable Default Agent Commission Rates**:
   - Added "Default Agent Rates" tab in Admin Panel
   - Users can now modify default new business (50%) and renewal (25%) rates
   - Rates stored in config_files/default_agent_commission_rates.json
   - Add New Policy form loads rates from config instead of hardcoding

2. **Mobile Sidebar Fix**: 
   - Disabled all custom CSS to allow Streamlit's native mobile behavior
   - Mobile users can now properly collapse/expand sidebar