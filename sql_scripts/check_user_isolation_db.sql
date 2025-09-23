-- User Data Isolation Database Check Script
-- Tests that all tables have proper user isolation columns and RLS policies

-- 1. Check which tables have user_id and user_email columns
SELECT 
    t.table_name,
    EXISTS(SELECT 1 FROM information_schema.columns 
           WHERE table_name = t.table_name 
           AND column_name = 'user_id') as has_user_id,
    EXISTS(SELECT 1 FROM information_schema.columns 
           WHERE table_name = t.table_name 
           AND column_name = 'user_email') as has_user_email
FROM information_schema.tables t
WHERE t.table_schema = 'public' 
AND t.table_type = 'BASE TABLE'
AND t.table_name NOT IN ('schema_migrations', 'password_reset_tokens')
ORDER BY t.table_name;

-- 2. Check RLS status on all tables
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;

-- 3. Check for any records without user isolation
-- Policies table
SELECT 'policies' as table_name, COUNT(*) as records_without_user
FROM policies 
WHERE user_id IS NULL AND user_email IS NULL;

-- Carriers table
SELECT 'carriers' as table_name, COUNT(*) as records_without_user
FROM carriers 
WHERE user_id IS NULL AND user_email IS NULL;

-- MGAs table
SELECT 'mgas' as table_name, COUNT(*) as records_without_user
FROM mgas 
WHERE user_id IS NULL AND user_email IS NULL;

-- Commission rules table
SELECT 'commission_rules' as table_name, COUNT(*) as records_without_user
FROM commission_rules 
WHERE user_id IS NULL AND user_email IS NULL;

-- 4. Check distinct users in each table
SELECT 'policies' as table_name, 
       COUNT(DISTINCT user_id) as unique_user_ids,
       COUNT(DISTINCT user_email) as unique_emails
FROM policies;

SELECT 'carriers' as table_name, 
       COUNT(DISTINCT user_id) as unique_user_ids,
       COUNT(DISTINCT user_email) as unique_emails
FROM carriers;

SELECT 'mgas' as table_name, 
       COUNT(DISTINCT user_id) as unique_user_ids,
       COUNT(DISTINCT user_email) as unique_emails
FROM mgas;

SELECT 'commission_rules' as table_name, 
       COUNT(DISTINCT user_id) as unique_user_ids,
       COUNT(DISTINCT user_email) as unique_emails
FROM commission_rules;

-- 5. Check RLS policies detail
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE schemaname = 'public'
AND tablename IN ('policies', 'carriers', 'mgas', 'commission_rules')
ORDER BY tablename, policyname;

-- 6. Sample check - Get 5 records from each table to verify user fields
-- Policies
SELECT 'policies' as source_table, 
       policy_id,
       user_id,
       user_email,
       client_name
FROM policies 
LIMIT 5;

-- Carriers  
SELECT 'carriers' as source_table,
       carrier_id,
       user_id,
       user_email,
       carrier_name
FROM carriers 
LIMIT 5;

-- MGAs
SELECT 'mgas' as source_table,
       mga_id,
       user_id,
       user_email,
       mga_name
FROM mgas 
LIMIT 5;

-- Commission Rules
SELECT 'commission_rules' as source_table,
       rule_id,
       user_id,
       user_email,
       carrier_id,
       mga_id
FROM commission_rules 
LIMIT 5;

-- 7. Check for potential cross-user data access
-- This would show if any user_id has multiple user_emails (data inconsistency)
SELECT 
    user_id,
    COUNT(DISTINCT user_email) as email_count,
    ARRAY_AGG(DISTINCT user_email) as emails
FROM policies
WHERE user_id IS NOT NULL
GROUP BY user_id
HAVING COUNT(DISTINCT user_email) > 1;

-- 8. Check user preferences isolation
SELECT 
    COUNT(*) as total_preferences,
    COUNT(DISTINCT user_id) as unique_users_with_prefs,
    COUNT(CASE WHEN user_id IS NULL THEN 1 END) as prefs_without_user_id
FROM user_preferences;

-- 9. Summary of isolation status
WITH isolation_check AS (
    SELECT 
        'policies' as table_name,
        COUNT(*) as total_records,
        COUNT(CASE WHEN user_id IS NOT NULL OR user_email IS NOT NULL THEN 1 END) as isolated_records
    FROM policies
    UNION ALL
    SELECT 
        'carriers' as table_name,
        COUNT(*) as total_records,
        COUNT(CASE WHEN user_id IS NOT NULL OR user_email IS NOT NULL THEN 1 END) as isolated_records
    FROM carriers
    UNION ALL
    SELECT 
        'mgas' as table_name,
        COUNT(*) as total_records,
        COUNT(CASE WHEN user_id IS NOT NULL OR user_email IS NOT NULL THEN 1 END) as isolated_records
    FROM mgas
    UNION ALL
    SELECT 
        'commission_rules' as table_name,
        COUNT(*) as total_records,
        COUNT(CASE WHEN user_id IS NOT NULL OR user_email IS NOT NULL THEN 1 END) as isolated_records
    FROM commission_rules
)
SELECT 
    table_name,
    total_records,
    isolated_records,
    CASE 
        WHEN total_records = 0 THEN 'No data'
        WHEN isolated_records = total_records THEN '✓ Fully isolated'
        ELSE '❌ NOT isolated (' || (total_records - isolated_records) || ' records without user)'
    END as isolation_status
FROM isolation_check
ORDER BY table_name;