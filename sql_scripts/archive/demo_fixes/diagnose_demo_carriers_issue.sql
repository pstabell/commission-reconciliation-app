-- DIAGNOSE DEMO USER CARRIERS/MGAS ISSUE
-- Run this in Supabase SQL Editor

-- 1. Check if tables have RLS enabled
SELECT 
    'RLS Status Check' as check_type,
    tablename,
    rowsecurity as has_rls,
    CASE 
        WHEN rowsecurity THEN '🔒 BLOCKED BY RLS' 
        ELSE '✅ OK - No RLS' 
    END as status
FROM pg_tables 
WHERE tablename IN ('carriers', 'mgas', 'commission_rules')
ORDER BY tablename;

-- 2. Check if commission_rules has user_email column
SELECT 
    'Column Check' as check_type,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'commission_rules'
AND column_name = 'user_email';

-- 3. Count data in each table
SELECT 'Carriers count:' as info, COUNT(*) FROM carriers
UNION ALL
SELECT 'MGAs count:' as info, COUNT(*) FROM mgas
UNION ALL
SELECT 'Total commission rules:' as info, COUNT(*) FROM commission_rules
UNION ALL
SELECT 'Demo user rules:' as info, COUNT(*) 
FROM commission_rules 
WHERE user_email IN ('demo@agentcommissiontracker.com', 'Demo@AgentCommissionTracker.com')
ORDER BY info;

-- 4. Check specific demo user data
SELECT 
    'Demo Commission Rules' as check_type,
    rule_id,
    carrier_id,
    mga_id,
    new_rate,
    renewal_rate,
    user_email
FROM commission_rules
WHERE user_email IN ('demo@agentcommissiontracker.com', 'Demo@AgentCommissionTracker.com')
LIMIT 5;

-- 5. Quick fix if RLS is the issue
-- ONLY run this section after reviewing the results above
/*
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;
-- Do NOT disable RLS on commission_rules if it has user_email column
*/