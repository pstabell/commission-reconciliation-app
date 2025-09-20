-- FINAL DEBUG - WHY CAN'T APP SEE CARRIERS

-- 1. Confirm data exists
SELECT 'DATA EXISTS CHECK:' as info;
SELECT 
    'Carriers for Demo@AgentCommissionTracker.com: ' || COUNT(*) as status
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Test EXACTLY what Streamlit app would query
SELECT '';
SELECT 'EXACT APP QUERY:' as info;
SELECT * FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 10;

-- 3. Check if problem is with status filtering
SELECT '';
SELECT 'STATUS DISTRIBUTION:' as info;
SELECT 
    status,
    COUNT(*) as count,
    CASE 
        WHEN status = 'Active' THEN 'Will show in app'
        ELSE 'Hidden in app'
    END as visibility
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status;

-- 4. Test query without any filters
SELECT '';
SELECT 'TOTAL CARRIERS IN TABLE:' as info;
SELECT COUNT(*) FROM carriers;

-- 5. List all demo variations
SELECT '';
SELECT 'ALL DEMO EMAILS IN DATABASE:' as info;
SELECT DISTINCT user_email
FROM (
    SELECT user_email FROM carriers WHERE LOWER(user_email) LIKE '%demo%'
    UNION
    SELECT user_email FROM mgas WHERE LOWER(user_email) LIKE '%demo%'
    UNION
    SELECT user_email FROM commission_rules WHERE LOWER(user_email) LIKE '%demo%'
) all_emails
ORDER BY user_email;

-- 6. One more permissions check
GRANT ALL ON carriers TO anon;
GRANT ALL ON mgas TO anon;
GRANT ALL ON commission_rules TO anon;

SELECT '';
SELECT 'NEXT STEPS:' as info;
SELECT '1. Check browser console for errors (F12)' as step1;
SELECT '2. Try incognito/private browsing mode' as step2;
SELECT '3. Clear browser cache and cookies' as step3;