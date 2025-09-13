# Security Guidelines for Commission Tracker Development

**Created**: January 13, 2025
**Purpose**: Prevent security vulnerabilities discovered during development

## 1. NEVER Use Global Caching for User-Specific Data

### ❌ WRONG - Creates Data Leaks
```python
@st.cache_data(ttl=300)
def load_user_data():
    # This caches globally! All users share the same cache!
    return supabase.table('policies').select("*").eq('user_email', st.session_state['user_email']).execute()
```

### ✅ CORRECT - No Caching for Sensitive Data
```python
def load_user_data():
    # No caching - always fresh data per user
    return supabase.table('policies').select("*").eq('user_email', st.session_state['user_email']).execute()
```

### ✅ ALTERNATIVE - Cache with User Key
```python
@st.cache_data(ttl=300)
def load_user_data(user_email):
    # User email as parameter ensures separate cache per user
    return supabase.table('policies').select("*").eq('user_email', user_email).execute()

# Call with: load_user_data(st.session_state['user_email'])
```

## 2. Row Level Security (RLS) Considerations

### Authentication Mismatch
Our app uses **custom authentication** (email/password), NOT Supabase Auth.
This means:
- `auth.email()` in RLS policies will be NULL
- Cannot use standard Supabase RLS patterns
- Must rely on app-level filtering

### Current Working RLS Policies
```sql
-- Allow operations but app controls filtering
CREATE POLICY "Anyone can view their own data" 
ON policies FOR SELECT 
TO anon, authenticated
USING (user_email IS NOT NULL);

CREATE POLICY "Anyone can insert with user_email" 
ON policies FOR INSERT 
TO anon, authenticated
WITH CHECK (user_email IS NOT NULL);
```

### App-Level Security
Always filter by user_email in queries:
```python
# PRODUCTION must always filter
if os.getenv("APP_ENVIRONMENT") == "PRODUCTION":
    response = supabase.table('policies').select("*").eq('user_email', st.session_state['user_email']).execute()
```

## 3. Environment Variables Best Practices

### Service Role Key Issues
- Render may have issues with long environment variable names
- Always provide fallbacks
- Test environment variables are accessible

```python
# Use fallbacks for critical keys
service_key = os.getenv("PRODUCTION_SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_KEY")
```

## 4. Multi-Tenant Data Isolation

### Every Insert Must Include user_email
```python
def add_user_email_to_data(data_dict):
    """Add current user's email to data dictionary for multi-tenancy."""
    if "user_email" in st.session_state:
        data_dict["user_email"] = st.session_state["user_email"]
    return data_dict
```

### Test with Multiple Users
Always test features with at least 3 different user accounts:
1. Admin account
2. Demo account  
3. Regular user account

## 5. CSV Import Security

### Column Validation
- Always validate and map column names
- Remove non-existent columns before insert
- Handle all variations (spaces, underscores, case)

### User Attribution
- Never trust user_email from CSV
- Always use logged-in user's email
- Validate all data before insert

## 6. Session State Security

### Never Store Sensitive Data in URLs
```python
# ❌ WRONG
st.query_params['user_email'] = user_email

# ✅ CORRECT
st.session_state['user_email'] = user_email
```

### Clear Session on Logout
```python
def logout():
    for key in ['password_correct', 'user_email', 'user_data']:
        if key in st.session_state:
            del st.session_state[key]
```

## 7. Testing Checklist

Before deploying ANY changes:

- [ ] Test with multiple user accounts
- [ ] Verify data isolation between users
- [ ] Check no data in URLs or global caches
- [ ] Confirm RLS policies are active
- [ ] Test CSV imports with each user type
- [ ] Clear all caches and re-test
- [ ] Check for any hardcoded values

## 8. Emergency Procedures

### If Data Leak Detected
1. Immediately disable feature
2. Clear all caches
3. Re-enable RLS if disabled
4. Audit access logs
5. Notify affected users

### Quick Fixes
```sql
-- Re-enable RLS
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;

-- Block all access temporarily
CREATE POLICY "deny_all" ON policies
FOR ALL USING (false);
```

## 9. Architecture Decisions

### Why Not Supabase Auth?
- App started with custom auth
- Migration would be complex
- Current system works with proper safeguards

### Performance vs Security
- Always choose security over performance
- No caching > Fast but insecure
- Document performance trade-offs

## 10. Code Review Requirements

Every PR must verify:
1. No global caching of user data
2. All queries filtered by user_email
3. No sensitive data in URLs
4. Session state properly managed
5. Multi-user testing completed

---

**Remember**: When in doubt, don't cache. Security > Performance.