-- VERIFY DEMO DATA ACCESS

-- 1. Count all demo data
SELECT 'DEMO DATA COUNTS:' as info;
SELECT 
    'Carriers' as type,
    COUNT(*) as total,
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'MGAs',
    COUNT(*),
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END)
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Rules',
    COUNT(*),
    SUM(CASE WHEN is_active = true THEN 1 ELSE 0 END)
FROM commission_rules
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Check if tables have any RLS policies
SELECT '';
SELECT 'RLS POLICIES:' as info;
SELECT 
    schemaname,
    tablename,
    policyname,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename IN ('carriers', 'mgas', 'commission_rules')
ORDER BY tablename, policyname;

-- 3. Test with a simple query
SELECT '';
SELECT 'SIMPLE TEST - First 5 carriers:' as info;
SELECT carrier_id, carrier_name, status, user_email
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
LIMIT 5;

-- 4. Check for any permission issues
SELECT '';
SELECT 'TABLE PERMISSIONS:' as info;
SELECT 
    grantee,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public' 
AND table_name IN ('carriers', 'mgas', 'commission_rules')
AND grantee IN ('anon', 'authenticated', 'public')
ORDER BY table_name, grantee, privilege_type;