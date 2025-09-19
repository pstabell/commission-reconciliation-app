-- COMPREHENSIVE DIAGNOSIS FOR DEMO CARRIER VISIBILITY

-- 1. Confirm demo data exists
SELECT 'DEMO DATA CONFIRMATION:' as info;
SELECT 
    (SELECT COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com') as carriers,
    (SELECT COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com') as mgas,
    (SELECT COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com') as rules;

-- 2. Check exact email case in all tables
SELECT '';
SELECT 'EMAIL CASE CHECK:' as info;
SELECT DISTINCT user_email, 'carriers' as source
FROM carriers 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
UNION
SELECT DISTINCT user_email, 'mgas'
FROM mgas 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
UNION
SELECT DISTINCT user_email, 'commission_rules'
FROM commission_rules 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com';

-- 3. Test the EXACT query the app runs
SELECT '';
SELECT 'EXACT APP QUERY TEST:' as info;
-- This is exactly what the Supabase client does:
SELECT * FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
LIMIT 1;

-- 4. Check permissions for anon
SELECT '';
SELECT 'ANON PERMISSIONS:' as info;
SELECT has_table_privilege('anon', 'carriers', 'SELECT') as can_select_carriers,
       has_table_privilege('anon', 'mgas', 'SELECT') as can_select_mgas,
       has_table_privilege('anon', 'commission_rules', 'SELECT') as can_select_rules;

-- 5. Check RLS status one more time
SELECT '';
SELECT 'RLS STATUS:' as info;
SELECT tablename, rowsecurity as rls_enabled
FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('carriers', 'mgas', 'commission_rules');

-- 6. Test what anon role sees
SET LOCAL ROLE anon;
SELECT '';
SELECT 'ANON VIEW TEST:' as info;
SELECT COUNT(*) as anon_can_see_carriers
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';
RESET ROLE;

-- 7. Check for any active RLS policies
SELECT '';
SELECT 'ACTIVE RLS POLICIES:' as info;
SELECT COUNT(*) as policy_count
FROM pg_policies
WHERE tablename IN ('carriers', 'mgas', 'commission_rules');

-- 8. Force fix permissions again
GRANT ALL PRIVILEGES ON carriers TO anon;
GRANT ALL PRIVILEGES ON mgas TO anon;  
GRANT ALL PRIVILEGES ON commission_rules TO anon;
GRANT ALL PRIVILEGES ON carrier_mga_relationships TO anon;

SELECT '';
SELECT 'DIAGNOSIS COMPLETE' as status;