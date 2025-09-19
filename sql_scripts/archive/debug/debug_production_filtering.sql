-- DEBUG PRODUCTION FILTERING ISSUE

-- 1. Verify demo data exists
SELECT 'DEMO DATA EXISTS:' as info;
SELECT COUNT(*) as carrier_count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Check what the app would see with exact query
SELECT '';
SELECT 'APP QUERY RESULT:' as info;
SELECT carrier_id, carrier_name, status, user_email
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY updated_at DESC NULLS LAST
LIMIT 5;

-- 3. Test if it's a timestamp issue
SELECT '';
SELECT 'CARRIERS WITH NULL TIMESTAMPS:' as info;
SELECT COUNT(*) as null_updated_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND updated_at IS NULL;

-- 4. Fix any null timestamps
UPDATE carriers
SET updated_at = COALESCE(updated_at, created_at, NOW())
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND updated_at IS NULL;

-- 5. Check if demo user is logged in correctly
SELECT '';
SELECT 'USERS TABLE CHECK:' as info;
SELECT id, email 
FROM users 
WHERE LOWER(email) = 'demo@agentcommissiontracker.com';

-- 6. Force clear any potential caching by updating all demo carriers
UPDATE carriers
SET updated_at = NOW()
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND carrier_id IN (
    SELECT carrier_id 
    FROM carriers 
    WHERE user_email = 'Demo@AgentCommissionTracker.com'
    LIMIT 1
);

-- 7. Final verification
SELECT '';
SELECT 'FINAL STATUS:' as info;
SELECT 
    'Total Demo Carriers: ' || COUNT(*) as status
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';