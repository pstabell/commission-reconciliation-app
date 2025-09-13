# Security Notice - Commission Tracker

**Last Updated**: January 13, 2025

## ⚠️ CRITICAL SECURITY INFORMATION

### Multi-Tenant Data Isolation

This application uses custom authentication (NOT Supabase Auth) with the following security measures:

1. **NO GLOBAL CACHING** - `load_policies_data()` does not use `@st.cache_data` to prevent data leaks
2. **App-Level Filtering** - All queries filter by `user_email` from session state
3. **RLS Policies** - Modified to work with anon key since we don't use Supabase Auth

### Known Security Considerations

1. **Service Role Key** - Currently not working in Render (unresolved issue)
2. **RLS Limitations** - Cannot use standard Supabase RLS patterns due to custom auth
3. **Performance Trade-off** - No caching means slightly slower but 100% secure

### Before Making Changes

**MUST READ**:
- `/docs/development/SECURITY_GUIDELINES.md`
- `/docs/troubleshooting/CSV_IMPORT_RLS_ISSUES_2025.md`

### Testing Requirements

Every change MUST be tested with multiple user accounts:
1. Log in as User A - verify data isolation
2. Log in as User B - verify data isolation
3. Switch between users - verify no data leaks
4. Test imports - verify user attribution

### Emergency Procedures

If data leak detected:
```sql
-- Immediately re-enable RLS
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;

-- Block all access
CREATE POLICY "emergency_deny_all" ON policies
FOR ALL USING (false);
```

Then check `/docs/troubleshooting/ISSUE_SUMMARY_JAN_2025.md` for fixes.

---

**Remember**: Security > Performance. When in doubt, don't cache!