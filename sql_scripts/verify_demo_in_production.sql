-- VERIFY DEMO DATA IS IN PRODUCTION DATABASE
-- Run this in your PRODUCTION Supabase database

-- 1. Check for demo user
SELECT 'DEMO USER CHECK:' as info;
SELECT COUNT(*) as demo_user_exists
FROM users
WHERE email = 'demo@agentcommissiontracker.com';

-- 2. Check for demo carriers
SELECT '';
SELECT 'DEMO CARRIERS CHECK:' as info;
SELECT COUNT(*) as demo_carriers
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 3. Show sample carriers
SELECT '';
SELECT 'SAMPLE DEMO CARRIERS:' as info;
SELECT carrier_name, status, created_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY created_at DESC
LIMIT 5;

-- 4. Check which database this is
SELECT '';
SELECT 'DATABASE CHECK:' as info;
SELECT current_database() as database_name;