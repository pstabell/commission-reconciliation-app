-- VERIFY STATUS VALUES FOR DEMO ACCOUNT

-- 1. Check exact status values
SELECT 'CARRIER STATUS VALUES:' as info;
SELECT DISTINCT status, COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status
ORDER BY status;

-- 2. Check for Active with exact case
SELECT '';
SELECT 'CARRIERS WITH status = Active (exact match):' as info;
SELECT COUNT(*) as active_count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND status = 'Active';

-- 3. Sample carriers to see actual values
SELECT '';
SELECT 'SAMPLE CARRIERS:' as info;
SELECT carrier_name, status, LENGTH(status) as status_length
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
LIMIT 5;