-- TEST WHAT ANON ROLE SEES

-- 1. Switch to anon role (as app would see)
SET ROLE anon;

-- 2. Try to query carriers
SELECT 'AS ANON ROLE - CARRIERS:' as info;
SELECT COUNT(*) as visible_count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 3. Try without filter
SELECT '';
SELECT 'AS ANON ROLE - ALL CARRIERS:' as info;
SELECT COUNT(*) as total_visible
FROM carriers;

-- 4. Reset to normal role
RESET ROLE;

-- 5. Compare with normal role
SELECT '';
SELECT 'AS NORMAL ROLE - CARRIERS:' as info;
SELECT COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';