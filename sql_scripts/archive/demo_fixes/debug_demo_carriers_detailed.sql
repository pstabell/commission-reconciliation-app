-- DETAILED DEBUG OF DEMO CARRIERS

-- 1. Check exact email match
SELECT 'CHECKING EXACT EMAIL MATCHES:' as info;
SELECT DISTINCT user_email, LENGTH(user_email) as email_length
FROM carriers
WHERE LOWER(user_email) LIKE '%demo%'
ORDER BY user_email;

-- 2. Count by exact email
SELECT '';
SELECT 'CARRIER COUNT BY EMAIL:' as info;
SELECT user_email, COUNT(*) as count
FROM carriers
WHERE user_email IS NOT NULL
GROUP BY user_email
ORDER BY count DESC;

-- 3. Check for Demo with exact case
SELECT '';
SELECT 'DEMO CARRIERS (exact match):' as info;
SELECT COUNT(*) as total_count,
       SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 4. Show sample carriers for demo
SELECT '';
SELECT 'SAMPLE DEMO CARRIERS:' as info;
SELECT carrier_id, carrier_name, status, user_email
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
LIMIT 5;

-- 5. Check case variations
SELECT '';
SELECT 'CHECKING CASE VARIATIONS:' as info;
SELECT user_email, COUNT(*) as count
FROM carriers
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
GROUP BY user_email;

-- 6. Check if app might be using different email
SELECT '';
SELECT 'ALL UNIQUE USER EMAILS:' as info;
SELECT DISTINCT user_email
FROM carriers
WHERE user_email IS NOT NULL
ORDER BY user_email;