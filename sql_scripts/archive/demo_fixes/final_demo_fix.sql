-- FINAL COMPREHENSIVE FIX FOR DEMO ACCOUNT

-- 1. Fix all status values to exactly 'Active' with capital A
UPDATE carriers 
SET status = 'Active'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

UPDATE mgas 
SET status = 'Active'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Check current commission rules count
SELECT 'Current commission rules: ' || COUNT(*) as count
FROM commission_rules
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND is_active = true;

-- 3. Verify all carriers have 'Active' status
SELECT 'Carriers with Active status: ' || COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND status = 'Active';

-- 4. Show first 5 carriers to verify
SELECT 'Sample carriers:' as info;
SELECT carrier_name, status, updated_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 5;

-- 5. Force update timestamps if needed
UPDATE carriers 
SET updated_at = NOW()
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND updated_at IS NULL;

UPDATE mgas 
SET updated_at = NOW()
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND updated_at IS NULL;

-- 6. Final counts
SELECT '';
SELECT 'FINAL VERIFICATION:' as status;
SELECT 'Active Carriers: ' || COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com' AND status = 'Active'
UNION ALL
SELECT 'Active MGAs: ' || COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com' AND status = 'Active'
UNION ALL
SELECT 'Active Rules: ' || COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com' AND is_active = true;

SELECT '';
SELECT 'IMPORTANT: Logout and login again after running this!' as reminder;