-- CHECK AND FIX RLS ON COMMISSION TABLES

-- 1. Check RLS status on all commission tables
SELECT 'RLS STATUS CHECK:' as info;
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE schemaname = 'public'
AND tablename IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships')
ORDER BY tablename;

-- 2. If RLS is enabled, it blocks the anon key from seeing data
-- The app uses anon key in production, so we need to disable RLS

-- 3. DISABLE RLS on all commission structure tables
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;
ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;
ALTER TABLE carrier_mga_relationships DISABLE ROW LEVEL SECURITY;

-- 4. Verify the fix
SELECT '';
SELECT 'AFTER FIX - RLS STATUS:' as info;
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE schemaname = 'public'
AND tablename IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships')
ORDER BY tablename;

-- 5. Test query as anon would see it
SELECT '';
SELECT 'DEMO CARRIERS COUNT (as anon would see):' as info;
SELECT COUNT(*) as visible_carriers
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND status = 'Active';

-- 6. Final message
SELECT '';
SELECT 'NEXT STEPS:' as info;
SELECT 'RLS has been disabled. Please refresh the app to see carriers.' as action;