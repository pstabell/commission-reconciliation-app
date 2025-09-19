-- TEST DEMO USER SESSION

-- 1. Simple count test
SELECT COUNT(*) as demo_carriers FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Show first few carriers with all details
SELECT 'FIRST 3 CARRIERS:' as info;
SELECT 
    carrier_id,
    carrier_name,
    status,
    user_email,
    created_at,
    updated_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 3;

-- 3. Test if it's a status filtering issue
SELECT 'STATUS BREAKDOWN:' as info;
SELECT status, COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status;

-- 4. Quick permission test
SET LOCAL ROLE anon;
SELECT 'ANON TEST:' as info, COUNT(*) as visible FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com';
RESET ROLE;