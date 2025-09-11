# Row Level Security (RLS) Troubleshooting Guide

**Created**: January 11, 2025  
**Purpose**: Document and resolve Row Level Security issues affecting data visibility

## Overview

Row Level Security (RLS) is a PostgreSQL feature that restricts which rows users can access in a table. While powerful for multi-tenant applications, it can cause unexpected data visibility issues when policies are missing or misconfigured.

## The Problem: Empty Dropdowns and Missing Data

### Symptoms
- Carrier dropdown shows no options
- MGA dropdown is empty
- Commission rules don't load
- "Could not find carrier" errors when saving policies
- Debug logs show "0 carriers found" or "0 MGAs found"

### Root Cause
RLS was enabled on the `carriers`, `mgas`, and `commission_rules` tables without creating corresponding access policies. This effectively blocks ALL access to these tables, even for authenticated users.

### Affected Tables
- `carriers` - Insurance carrier reference data
- `mgas` - Managing General Agent reference data
- `commission_rules` - Commission rate configurations

## Solution: Disable RLS on Reference Tables

### Step 1: Run the Fix Script
Execute this SQL in your Supabase SQL Editor:

```sql
-- =====================================================
-- FIX RLS ISSUE - DISABLE RLS ON REFERENCE TABLES
-- =====================================================

-- 1. Disable RLS on carriers table
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;

-- 2. Disable RLS on mgas table  
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;

-- 3. Disable RLS on commission_rules table
ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;

-- 4. Verify RLS is now disabled
SELECT 
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS ENABLED - Data blocked'
        ELSE '🔓 RLS DISABLED - Data accessible'
    END as status
FROM pg_tables 
WHERE tablename IN ('carriers', 'mgas', 'commission_rules')
    AND schemaname = 'public';
```

### Step 2: Verify Data Access
Confirm the data is now accessible:

```sql
-- Should return counts > 0
SELECT 
    (SELECT COUNT(*) FROM carriers) as carrier_count,
    (SELECT COUNT(*) FROM mgas) as mga_count,
    (SELECT COUNT(*) FROM commission_rules) as rule_count;
```

### Step 3: Test in Application
1. Refresh the Streamlit app
2. Navigate to Admin Panel → Contacts
3. Verify Carriers and MGAs dropdowns populate
4. Test adding a new policy - carrier dropdown should work

## Understanding RLS Best Practices

### When to Use RLS
Enable RLS on tables containing:
- User-specific data (policies, transactions)
- Sensitive business data
- Multi-tenant data requiring isolation

### When NOT to Use RLS
Disable RLS on:
- Reference/lookup tables (carriers, MGAs, policy types)
- Shared configuration data
- System-wide settings

### Proper RLS Implementation
If you need RLS on reference tables:

```sql
-- Example: Allow all authenticated users to read carriers
CREATE POLICY "authenticated_users_read_carriers" ON carriers
    FOR SELECT
    USING (auth.role() = 'authenticated');

-- Then enable RLS
ALTER TABLE carriers ENABLE ROW LEVEL SECURITY;
```

## Diagnostic Queries

### Check All Tables RLS Status
```sql
-- Show all tables and their RLS status
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 ENABLED'
        ELSE '🔓 DISABLED'
    END as rls_status
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY rowsecurity DESC, tablename;
```

### Check Existing Policies
```sql
-- List all RLS policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd as operation
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
```

### Debug Access Issues
```sql
-- Test what current user can see
SELECT current_user, auth.uid(), auth.role();

-- Count accessible rows per table
SELECT 
    'carriers' as table_name, COUNT(*) as accessible_rows FROM carriers
UNION ALL
SELECT 'mgas', COUNT(*) FROM mgas
UNION ALL  
SELECT 'commission_rules', COUNT(*) FROM commission_rules;
```

## Prevention

### Development Checklist
- [ ] Document which tables need RLS
- [ ] Create policies BEFORE enabling RLS
- [ ] Test with different user roles
- [ ] Have rollback plan ready

### Migration Safety
```sql
-- Safe approach: Create policy first, then enable RLS
BEGIN;
    -- Create policy
    CREATE POLICY "policy_name" ON table_name ...;
    
    -- Test the policy would work
    -- Run test queries
    
    -- Only then enable RLS
    ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;
COMMIT;
```

## Emergency Rollback

If RLS causes widespread issues:

```sql
-- Disable RLS on all tables
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN 
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        AND rowsecurity = true
    LOOP
        EXECUTE format('ALTER TABLE %I DISABLE ROW LEVEL SECURITY', r.tablename);
        RAISE NOTICE 'Disabled RLS on %', r.tablename;
    END LOOP;
END $$;
```

## Related Documentation
- [Database Migrations Guide](DATABASE_MIGRATIONS.md)
- [Security System Documentation](../features/SECURITY_SYSTEM.md)
- [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md)

## Key Takeaways

1. **RLS without policies = Complete lockout**: Always create policies before enabling RLS
2. **Reference tables usually don't need RLS**: Keep shared data accessible
3. **Test thoroughly**: RLS issues can be subtle and role-dependent
4. **Document your approach**: Future developers need to understand the security model

---

*Remember: RLS is a powerful security feature, but with great power comes great responsibility to configure it correctly!*