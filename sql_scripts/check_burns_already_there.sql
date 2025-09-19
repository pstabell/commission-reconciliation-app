-- CHECK IF BURNS & WILCOX IS ALREADY THERE

-- 1. Current MGA count
SELECT 'CURRENT MGA COUNT:' as info;
SELECT COUNT(*) as total_mgas
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Check for Burns & Wilcox specifically
SELECT '';
SELECT 'BURNS & WILCOX CHECK:' as info;
SELECT mga_name, created_at
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND mga_name LIKE '%Burns%';

-- 3. List all MGAs to see what we have
SELECT '';
SELECT 'ALL DEMO MGAS:' as info;
SELECT mga_name
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY mga_name;