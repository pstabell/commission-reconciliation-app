-- INVESTIGATE WHERE THESE CARRIERS CAME FROM

-- 1. Check who owns carriers like "21st Century", "AAA", etc
SELECT 'CARRIER OWNERSHIP:' as info;
SELECT DISTINCT user_email, COUNT(*) as carrier_count
FROM carriers
WHERE carrier_name IN ('21st Century', 'AAA', 'Allstate', 'Auto-Owners', 'USAA')
GROUP BY user_email
ORDER BY user_email;

-- 2. Check if demo has carriers from multiple sources
SELECT '';
SELECT 'ALL USER EMAILS FOR DEMO CARRIERS:' as info;
SELECT DISTINCT user_email, COUNT(*) as count
FROM carriers
WHERE carrier_name IN (
    SELECT carrier_name 
    FROM carriers 
    WHERE user_email = 'Demo@AgentCommissionTracker.com'
)
GROUP BY user_email
ORDER BY count DESC;

-- 3. Find Burlington across all users
SELECT '';
SELECT 'WHERE IS BURLINGTON?:' as info;
SELECT user_email, carrier_id, carrier_name, created_at
FROM carriers
WHERE LOWER(carrier_name) LIKE '%burlington%'
ORDER BY created_at;

-- 4. This looks like demo has generic/default carriers, not your specific ones!
SELECT '';
SELECT 'HYPOTHESIS:' as info;
SELECT 'Demo account has generic insurance carriers, NOT the ones from your private database!' as finding;