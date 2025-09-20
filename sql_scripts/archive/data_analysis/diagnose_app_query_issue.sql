-- DIAGNOSE WHY APP CAN'T SEE CARRIERS

-- 1. Confirm carriers exist with correct email
SELECT 'CARRIERS WITH DEMO EMAIL:' as info;
SELECT COUNT(*) as total, 
       SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Show sample carriers
SELECT '';
SELECT 'SAMPLE DEMO CARRIERS:' as info;
SELECT carrier_id, carrier_name, status, user_email
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
LIMIT 5;

-- 3. Check if there's a view or different table the app might use
SELECT '';
SELECT 'ALL TABLES/VIEWS WITH "CARRIER" IN NAME:' as info;
SELECT table_schema, table_name, table_type
FROM information_schema.tables
WHERE table_name LIKE '%carrier%'
AND table_schema = 'public'
ORDER BY table_name;

-- 4. Check session state issue - are there any triggers?
SELECT '';
SELECT 'TRIGGERS ON CARRIERS TABLE:' as info;
SELECT trigger_name, event_manipulation, action_timing
FROM information_schema.triggers
WHERE event_object_table = 'carriers';

-- 5. Try exact app simulation with role
SET ROLE anon;
SELECT '';
SELECT 'SIMULATING APP QUERY AS ANON:' as info;
SELECT COUNT(*) as count_as_anon FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com';
RESET ROLE;

-- 6. Check for any active RLS policies
SELECT '';
SELECT 'ACTIVE RLS POLICIES:' as info;
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies
WHERE tablename IN ('carriers', 'mgas', 'commission_rules');

-- 7. Double-check RLS is disabled
SELECT '';
SELECT 'RLS STATUS:' as info;
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('carriers', 'mgas', 'commission_rules');