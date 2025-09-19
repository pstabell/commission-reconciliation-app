-- CHECK FOR SPECIFIC CARRIER AND MGA

-- 1. Check for Burlington carrier
SELECT 'BURLINGTON CARRIER SEARCH:' as info;
SELECT carrier_id, carrier_name, status, user_email
FROM carriers
WHERE LOWER(carrier_name) LIKE '%burlington%'
ORDER BY user_email, carrier_name;

-- 2. Check for Burns & Wilcox MGA
SELECT '';
SELECT 'BURNS & WILCOX MGA SEARCH:' as info;
SELECT mga_id, mga_name, status, user_email
FROM mgas
WHERE LOWER(mga_name) LIKE '%burns%' OR LOWER(mga_name) LIKE '%wilcox%'
ORDER BY user_email, mga_name;

-- 3. Check specifically for demo user
SELECT '';
SELECT 'DEMO USER - BURLINGTON:' as info;
SELECT COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND LOWER(carrier_name) LIKE '%burlington%';

SELECT '';
SELECT 'DEMO USER - BURNS & WILCOX:' as info;
SELECT COUNT(*) as count
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND (LOWER(mga_name) LIKE '%burns%' OR LOWER(mga_name) LIKE '%wilcox%');

-- 4. If missing, we need to add them
SELECT '';
SELECT 'ACTION NEEDED:' as info;
SELECT 'If counts above are 0, we need to import these from private database' as action;