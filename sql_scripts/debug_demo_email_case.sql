-- DEBUG: Check all demo email variations in the database

-- 1. Check all unique user emails containing 'demo'
SELECT 'ALL DEMO EMAIL VARIATIONS:' as info;
SELECT DISTINCT user_email, COUNT(*) as count
FROM (
    SELECT user_email FROM carriers WHERE LOWER(user_email) LIKE '%demo%'
    UNION ALL
    SELECT user_email FROM mgas WHERE LOWER(user_email) LIKE '%demo%'
    UNION ALL
    SELECT user_email FROM commission_rules WHERE LOWER(user_email) LIKE '%demo%'
) all_emails
GROUP BY user_email
ORDER BY user_email;

-- 2. Check carriers for specific email cases
SELECT '';
SELECT 'CARRIERS BY EMAIL CASE:' as info;
SELECT 
    user_email,
    COUNT(*) as carrier_count,
    COUNT(CASE WHEN status = 'Active' THEN 1 END) as active_count
FROM carriers 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
GROUP BY user_email;

-- 3. Show exact email the app expects
SELECT '';
SELECT 'APP EXPECTS THIS EXACT EMAIL:' as info;
SELECT 'Demo@AgentCommissionTracker.com' as expected_email;

-- 4. Count carriers for the exact email app expects
SELECT '';
SELECT 'CARRIERS FOR EXPECTED EMAIL:' as info;
SELECT COUNT(*) as count
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 5. If mismatch, show what needs to be updated
SELECT '';
SELECT 'FIX NEEDED?' as info;
SELECT 
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM carriers 
            WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com' 
            AND user_email != 'Demo@AgentCommissionTracker.com'
        )
        THEN 'YES - Email case mismatch detected!'
        ELSE 'NO - Email case is correct'
    END as status;