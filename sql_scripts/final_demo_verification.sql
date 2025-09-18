-- FINAL VERIFICATION FOR DEMO ACCOUNT

-- 1. Exact counts with correct status
SELECT 'DEMO ACCOUNT SUMMARY:' as info;
SELECT 
    'Active Carriers: ' || COUNT(*) as count
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com' 
AND status = 'Active'
UNION ALL
SELECT 
    'Active MGAs: ' || COUNT(*)
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com' 
AND status = 'Active'
UNION ALL
SELECT 
    'Active Commission Rules: ' || COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com' 
AND is_active = true;

-- 2. Check for any email variations
SELECT '';
SELECT 'ALL USER EMAILS IN DATABASE:' as info;
SELECT DISTINCT user_email
FROM (
    SELECT user_email FROM carriers WHERE user_email LIKE '%Demo%' OR user_email LIKE '%demo%'
    UNION
    SELECT user_email FROM mgas WHERE user_email LIKE '%Demo%' OR user_email LIKE '%demo%'
    UNION
    SELECT user_email FROM commission_rules WHERE user_email LIKE '%Demo%' OR user_email LIKE '%demo%'
) emails
ORDER BY user_email;

-- 3. Force update timestamps (in case sorting by updated_at is the issue)
UPDATE carriers 
SET updated_at = NOW() 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND updated_at IS NULL;

UPDATE mgas 
SET updated_at = NOW() 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND updated_at IS NULL;

-- 4. Final check
SELECT '';
SELECT 'Ready for demo!' as status;
SELECT 'Please logout and login as Demo@AgentCommissionTracker.com' as action;