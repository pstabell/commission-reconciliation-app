# Multi-Tenancy Implementation for Production SaaS

## Overview

This document describes the complete multi-tenancy implementation for the Commission Tracker SaaS application deployed on Render. The system provides complete data isolation between customers while maintaining a shared reference data model.

## Key Architecture Decisions

### 1. Dual Environment System

- **Personal Environment**: No multi-tenancy, full access to all data (original behavior preserved)
- **Production Environment**: Full multi-tenancy with user data isolation

The environment is determined by the `APP_ENVIRONMENT` variable:
```python
if os.getenv("APP_ENVIRONMENT") == "PRODUCTION" and "user_email" in st.session_state:
    # Apply multi-tenancy filters
else:
    # Personal mode - no restrictions
```

### 2. Data Classification

#### User-Specific Tables (Isolated)
- `policies` - Commission transactions
- `deleted_policies` - Archived policies  
- `commission_rules` - User-specific commission rates
- `commission_payments` - Payment records
- `manual_commission_entries` - Manual adjustments
- `reconciliations` - Bank reconciliations
- `renewal_history` - Policy renewal tracking

#### Shared Reference Tables (Read-Only)
- `carriers` - Insurance companies
- `mgas` - Managing General Agents
- `carrier_mga_relationships` - MGA-Carrier mappings

#### Hybrid Tables (Global + Private)
- `carriers` - NULL user_email = global, with user_email = private
- `mgas` - NULL user_email = global, with user_email = private

## Database Schema Changes

### 1. User Email Columns Added

All user-specific tables now include:
```sql
user_email TEXT -- Links data to authenticated user
```

### 2. Audit Trail Columns

All tables now include:
```sql
created_at TIMESTAMPTZ DEFAULT NOW()
updated_at TIMESTAMPTZ DEFAULT NOW()  
created_by TEXT DEFAULT auth.email()
updated_by TEXT
```

### 3. Audit Log Table

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    table_name TEXT,
    record_id TEXT,
    action TEXT, -- INSERT, UPDATE, DELETE
    user_email TEXT,
    old_values JSONB,
    new_values JSONB,
    changed_at TIMESTAMPTZ,
    ip_address TEXT,
    user_agent TEXT
);
```

## Row Level Security (RLS) Implementation

### User-Specific Tables Pattern

```sql
-- Users can only see their own data
CREATE POLICY "Users can view own data" ON [table_name]
  FOR SELECT TO authenticated
  USING (user_email = auth.email());

-- Users can only insert with their email
CREATE POLICY "Users can insert own data" ON [table_name]
  FOR INSERT TO authenticated
  WITH CHECK (user_email = auth.email());

-- Users can only update their own data
CREATE POLICY "Users can update own data" ON [table_name]
  FOR UPDATE TO authenticated
  USING (user_email = auth.email())
  WITH CHECK (user_email = auth.email());

-- Service role bypass for admin operations
CREATE POLICY "Service role full access" ON [table_name]
  FOR ALL TO service_role
  USING (true)
  WITH CHECK (true);
```

### Shared Reference Tables Pattern

```sql
-- Read-only for all authenticated users
CREATE POLICY "Read only access" ON [table_name]
  FOR SELECT TO authenticated
  USING (true);

-- Only service role can modify
CREATE POLICY "Service role only modifications" ON [table_name]
  FOR ALL TO service_role
  USING (true)
  WITH CHECK (true);
```

### Hybrid Tables Pattern

```sql
-- See global entries and own private entries
CREATE POLICY "See global and own entries" ON [table_name]
  FOR SELECT TO authenticated
  USING (user_email IS NULL OR user_email = auth.email());

-- Can only create/modify own entries
CREATE POLICY "Manage own entries" ON [table_name]
  FOR ALL TO authenticated
  USING (user_email = auth.email())
  WITH CHECK (user_email = auth.email());
```

## Application Code Changes

### 1. Data Loading Functions

```python
@st.cache_data(ttl=300)
def load_policies_data():
    """Load policies data - filtered by user in production."""
    supabase = get_supabase_client()
    
    if os.getenv("APP_ENVIRONMENT") == "PRODUCTION" and "user_email" in st.session_state:
        # Production: Filter by user
        response = supabase.table('policies').select("*").eq('user_email', st.session_state['user_email']).execute()
    else:
        # Personal: Show all data
        response = supabase.table('policies').select("*").execute()
```

### 2. Data Insertion Helper

```python
def add_user_email_to_data(data_dict):
    """Add current user's email to data for multi-tenancy."""
    if "user_email" in st.session_state:
        data_dict["user_email"] = st.session_state["user_email"]
    return data_dict

# Usage in insert operations:
cleaned_data = clean_data_for_database(insert_dict)
cleaned_data = add_user_email_to_data(cleaned_data)
supabase.table('policies').insert(cleaned_data).execute()
```

## Security Features

### 1. Complete Data Isolation
- Users cannot see or access other users' data
- RLS policies enforce isolation at database level
- Application layer adds additional filtering

### 2. Audit Trail
- All changes tracked with timestamps
- User attribution on all operations
- Audit log for investigation capabilities

### 3. Shared Data Protection
- Reference data is read-only for users
- Only admin scripts can modify shared data
- Private entries allow user customization

## Deployment Considerations

### Environment Variables

Production deployment requires:
```bash
APP_ENVIRONMENT=PRODUCTION
PRODUCTION_SUPABASE_URL=your_prod_url
PRODUCTION_SUPABASE_ANON_KEY=your_prod_key
```

### Database Migration

For existing data:
1. All existing records have NULL user_email
2. Must be assigned to appropriate users
3. Or designated as shared reference data

### Testing Multi-Tenancy

1. Create two test user accounts
2. Add data under each account
3. Verify complete isolation
4. Test shared reference data visibility

## Troubleshooting

### Common Issues

1. **"I can't see my data"**
   - Check user_email is set in session
   - Verify RLS policies are active
   - Confirm data has correct user_email

2. **"I can't add carriers/MGAs"**
   - These are shared by default
   - Private entries require user_email

3. **"Other users modified my data"**
   - Check audit_logs table
   - Verify RLS policies are enabled
   - Review user_activity_log view

### Investigation Queries

```sql
-- Check user's activity
SELECT * FROM user_activity_log 
WHERE user_email = 'user@example.com'
ORDER BY changed_at DESC;

-- Verify data integrity
SELECT * FROM check_user_data_integrity('user@example.com');

-- Check RLS status
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';
```

## Future Enhancements

1. **Organization Support**
   - Multiple users per company
   - Role-based permissions
   - Shared team data

2. **Advanced Audit**
   - IP tracking
   - Session recording
   - Compliance reporting

3. **Data Export**
   - User data backup
   - GDPR compliance
   - Account deletion

## Summary

The multi-tenancy implementation provides:
- ✅ Complete user data isolation
- ✅ Shared reference data model
- ✅ Audit trail for accountability
- ✅ Backwards compatibility for personal use
- ✅ Production-ready security model

Last Updated: {{ current_date }}