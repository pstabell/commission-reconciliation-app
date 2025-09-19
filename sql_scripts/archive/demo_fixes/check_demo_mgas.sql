-- CHECK DEMO MGAS

-- 1. Count MGAs for demo user
SELECT 'DEMO MGAS COUNT:' as info;
SELECT COUNT(*) as total_mgas
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Show all demo MGAs
SELECT '';
SELECT 'ALL DEMO MGAS:' as info;
SELECT mga_id, mga_name, status
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY mga_name;

-- 3. Check if any MGAs exist without proper user_email
SELECT '';
SELECT 'MGAS WITHOUT DEMO EMAIL:' as info;
SELECT COUNT(*) as orphan_mgas
FROM mgas
WHERE user_email IS NULL 
   OR user_email = ''
   OR (LOWER(user_email) LIKE '%demo%' AND user_email != 'Demo@AgentCommissionTracker.com');