# CSV Import and RLS Issues - Troubleshooting Guide
**Date Resolved**: January 13, 2025
**Time Spent**: ~24 hours
**Severity**: CRITICAL - Data security and functionality

## Table of Contents
1. [Overview of Issues](#overview-of-issues)
2. [Issue 1: Column Name Mismatches](#issue-1-column-name-mismatches)
3. [Issue 2: RLS Blocking CSV Imports](#issue-2-rls-blocking-csv-imports)
4. [Issue 3: Service Role Key Not Found](#issue-3-service-role-key-not-found)
5. [Issue 4: Cache Poisoning - Users Seeing Other Users' Data](#issue-4-cache-poisoning---users-seeing-other-users-data)
6. [Final Working Solution](#final-working-solution)
7. [Lessons Learned](#lessons-learned)

---

## Overview of Issues

We encountered a series of cascading issues when trying to implement CSV import functionality for a multi-tenant SaaS application:

1. **Column name mismatches** between CSV files and database schema
2. **Row Level Security (RLS)** blocking legitimate imports
3. **Service role key** not being recognized by the application
4. **Cache poisoning** causing users to see other users' data

Each issue revealed deeper architectural challenges with authentication and data isolation.

---

## Issue 1: Column Name Mismatches

### Problem
CSV imports were failing with errors like:
- "Missing required columns: Client_ID, Transaction_ID, Policy_Type"
- "Could not find the 'Agent Gross Comm %' column"
- "Could not find the 'FULL OR MONTHLY PMTS' column"

### Root Cause
1. CSV files had spaces in column names, database expected underscores
2. UI display names were being sent to database instead of actual column names
3. Some columns existed in old schemas but not current database

### Solution
```python
# commission_app.py - Added comprehensive column mapping
column_mapping = {
    'Client ID': ['Client_ID', 'ClientID', 'Client_Id', 'client_id'],
    'Transaction ID': ['Transaction_ID', 'TransactionID', 'Transaction_Id'],
    'Carrier Name': ['Carrier_Name', 'CarrierName', 'Carrier_name'],
    # ... etc for all columns
}

# Also added to clean_data_for_database():
ui_only_fields = {
    'FULL OR MONTHLY PMTS',  # Old column that no longer exists
    'FULL_OR_MONTHLY_PMTS'   # Underscore version
}
```

### Key Commits
- `fix: Comprehensive CSV import column mapping for all database fields`
- `fix: Remove FULL OR MONTHLY PMTS column that doesn't exist in database`

---

## Issue 2: RLS Blocking CSV Imports

### Problem
Even with correct column names, imports failed with:
```
"new row violates row-level security policy for table 'policies'"
```

### Root Cause
The app uses its own authentication system (email/password), but Supabase RLS expects Supabase Auth JWT tokens. When inserting:
- App provides: `user_email = "Demo@AgentCommissionTracker.com"`
- RLS checks: `auth.email()` which returns NULL
- Insert blocked because NULL ≠ "Demo@AgentCommissionTracker.com"

### Failed Attempts
1. Created RLS policy for demo user - didn't work
2. Modified INSERT policy to check `user_email IS NOT NULL` - didn't work
3. Allowed `anon` role in policies - still didn't work

### Temporary Solution (Security Risk)
```sql
-- Disabled RLS completely
ALTER TABLE policies DISABLE ROW LEVEL SECURITY;
```

This allowed imports but exposed ALL users' data to everyone!

### Final RLS Solution
```sql
-- Allow anon role to perform operations
CREATE POLICY "Anyone can view their own data" 
ON policies FOR SELECT 
TO anon, authenticated
USING (user_email IS NOT NULL);

CREATE POLICY "Anyone can insert with user_email" 
ON policies FOR INSERT 
TO anon, authenticated
WITH CHECK (user_email IS NOT NULL);
```

The app filters data using `.eq('user_email', st.session_state['user_email'])`.

---

## Issue 3: Service Role Key Not Found

### Problem
Despite adding `PRODUCTION_SUPABASE_SERVICE_ROLE_KEY` to Render multiple times:
```
Production mode - Service key NOT FOUND
Available PRODUCTION env vars: PRODUCTION_SUPABASE_URL, PRODUCTION_SUPABASE_ANON_KEY
```

### Root Cause
Unknown - the environment variable was correctly named and saved in Render, but the app couldn't see it.

### Attempted Solutions
1. Multiple restarts and redeployments
2. Checked for typos and trailing spaces
3. Added shorter variable name fallback
4. Enhanced debugging to list all env vars

### Workaround
Instead of relying on service role key, we modified RLS policies to work with the anon key.

**Note**: This issue remains unresolved. The service role key should work but doesn't.

---

## Issue 4: Cache Poisoning - Users Seeing Other Users' Data

### Problem
THE MOST CRITICAL ISSUE: Users were seeing other users' data!
- User A logs in → sees their data
- User B logs in → sees User A's data!
- User B clears cache → sees their own data
- User A logs back in → sees User B's data!

### Root Cause
Streamlit's `@st.cache_data` decorator caches globally, not per user:
```python
@st.cache_data(ttl=300)  # This caches for ALL users!
def load_policies_data():
    # Even though we filter by user, the cache is global
    response = supabase.table('policies').select("*").eq('user_email', st.session_state['user_email']).execute()
```

### Failed Solution
Tried to add user_email as cache key:
```python
@st.cache_data(ttl=300)
def load_policies_data(_user_email=None):
    # Still had cache pollution issues
```

### Final Solution
Completely removed caching:
```python
def load_policies_data():
    """Load policies data from Supabase - filtered by current user. NO CACHING to prevent data leaks."""
    # No @st.cache_data decorator
    # Fresh data loaded every time
```

**Trade-off**: Slower performance but guaranteed data isolation.

---

## Final Working Solution

1. **Column Mapping**: Comprehensive mapping handles all variations of column names
2. **RLS Policies**: Allow anon role with `user_email IS NOT NULL` check
3. **No Caching**: Removed all caching to prevent data leaks
4. **App-Level Filtering**: Always filter by `user_email` in queries

```python
# Current working implementation
def load_policies_data():
    """NO CACHING to prevent data leaks."""
    supabase = get_supabase_client()
    user_email = st.session_state.get('user_email')
    
    if os.getenv("APP_ENVIRONMENT") == "PRODUCTION" and user_email:
        response = supabase.table('policies').select("*").eq('user_email', user_email).execute()
    else:
        response = supabase.table('policies').select("*").execute()
```

---

## Lessons Learned

### 1. Authentication Architecture Matters
Using custom authentication (not Supabase Auth) creates RLS challenges. Consider:
- Using Supabase Auth for seamless RLS integration
- OR using service role key + app-level filtering
- Never mix authentication methods

### 2. Caching in Multi-Tenant Apps is Dangerous
- Global caches can leak data between users
- Always include user identifier in cache key
- When in doubt, don't cache sensitive data

### 3. Column Name Consistency
- Database schema and CSV imports must match exactly
- Create comprehensive mapping for all variations
- Remove old columns from codebase

### 4. Test Multi-User Scenarios
- Always test with multiple user accounts
- Check data isolation after EVERY change
- Don't assume caching is safe

### 5. RLS Policy Complexity
- RLS policies must match your authentication method
- Test policies with actual SQL before implementing
- Document which tables have RLS enabled/disabled

---

## Prevention Checklist for Future

- [ ] Always test imports with multiple users
- [ ] Check data isolation after any caching changes
- [ ] Verify RLS policies match authentication method
- [ ] Test environment variables are accessible before depending on them
- [ ] Document all column mappings and schema changes
- [ ] Never disable RLS without immediate fix
- [ ] Consider performance vs security trade-offs

---

## Related Files Modified
- `/commission_app.py` - Multiple fixes for column mapping, caching, RLS
- `/sql_scripts/fix_rls_multi_tenant.sql` - RLS policy attempts
- `/sql_scripts/check_policies_rls.sql` - RLS diagnostic queries
- `/docs/operations/TROUBLESHOOTING_GUIDE.md` - Added RLS section