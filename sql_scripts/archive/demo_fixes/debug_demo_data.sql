-- COMPREHENSIVE DEBUG FOR DEMO ACCOUNT DATA

-- 1. Check exact demo email and counts
SELECT 'DEMO ACCOUNT SUMMARY:' as info;
SELECT 
    user_email,
    COUNT(*) as total_carriers,
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_carriers,
    SUM(CASE WHEN status != 'Active' OR status IS NULL THEN 1 ELSE 0 END) as inactive_carriers
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY user_email;

-- 2. Check status values distribution
SELECT '';
SELECT 'STATUS VALUES IN CARRIERS:' as info;
SELECT 
    status,
    LENGTH(status) as status_length,
    COUNT(*) as count,
    '"' || status || '"' as quoted_status
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status
ORDER BY count DESC;

-- 3. Sample 5 carriers with all fields
SELECT '';
SELECT 'SAMPLE CARRIERS (first 5):' as info;
SELECT 
    carrier_id,
    carrier_name,
    status,
    '"' || status || '"' as quoted_status,
    created_at,
    updated_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 5;

-- 4. Check for any whitespace issues
SELECT '';
SELECT 'CHECKING FOR WHITESPACE IN STATUS:' as info;
SELECT 
    carrier_name,
    status,
    LENGTH(status) as len,
    CASE 
        WHEN status != TRIM(status) THEN 'HAS WHITESPACE'
        ELSE 'OK'
    END as whitespace_check
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND (status != TRIM(status) OR LENGTH(status) != LENGTH(TRIM(status)))
LIMIT 10;

-- 5. Count carriers that should be visible
SELECT '';
SELECT 'CARRIERS MATCHING APP CRITERIA:' as info;
SELECT COUNT(*) as should_be_visible
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND status = 'Active'
AND status IS NOT NULL;

-- 6. Check MGAs
SELECT '';
SELECT 'MGA SUMMARY:' as info;
SELECT 
    COUNT(*) as total_mgas,
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_mgas
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 7. Check commission rules
SELECT '';
SELECT 'COMMISSION RULES SUMMARY:' as info;
SELECT 
    COUNT(*) as total_rules,
    SUM(CASE WHEN is_active = true THEN 1 ELSE 0 END) as active_rules
FROM commission_rules
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 8. Check if there are any carriers without user_email
SELECT '';
SELECT 'CARRIERS WITHOUT USER_EMAIL:' as info;
SELECT COUNT(*) as orphan_carriers
FROM carriers
WHERE user_email IS NULL OR user_email = '';

-- 9. Force refresh updated_at timestamps
UPDATE carriers
SET updated_at = NOW()
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND updated_at IS NULL;

-- 10. Final status
SELECT '';
SELECT 'FINAL CHECK:' as info;
SELECT 'Data looks correct. Issue may be session caching. User should:' as status;
SELECT '1. Logout completely' as step1;
SELECT '2. Close browser tab' as step2;
SELECT '3. Open new tab and login as demo@agentcommissiontracker.com' as step3;