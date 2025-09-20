-- TEST EXACTLY WHAT THE APP QUERIES

-- 1. Test the exact carrier query the app runs
SELECT 'APP CARRIER QUERY TEST:' as info;
SELECT * FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
LIMIT 5;

-- 2. Check if any carriers exist at all
SELECT '';
SELECT 'ANY CARRIERS IN TABLE:' as info;
SELECT COUNT(*) as total_carriers_in_table
FROM carriers;

-- 3. Check unique user emails
SELECT '';
SELECT 'USER EMAILS IN CARRIERS:' as info;
SELECT DISTINCT user_email, COUNT(*) as count
FROM carriers
GROUP BY user_email
ORDER BY COUNT(*) DESC;

-- 4. Case-insensitive search for demo
SELECT '';
SELECT 'DEMO VARIATIONS:' as info;
SELECT user_email, COUNT(*) as count
FROM carriers
WHERE LOWER(user_email) LIKE '%demo%'
GROUP BY user_email;

-- 5. Check if we have the wrong case
SELECT '';
SELECT 'EXACT CASE CHECK:' as info;
SELECT 
    CASE 
        WHEN EXISTS (SELECT 1 FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com') 
        THEN 'Found with expected case'
        WHEN EXISTS (SELECT 1 FROM carriers WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com')
        THEN 'Found but with different case'
        ELSE 'Not found at all'
    END as status;

-- 6. If wrong case, show what we have
SELECT '';
SELECT 'ACTUAL DEMO EMAILS:' as info;
SELECT DISTINCT user_email
FROM carriers
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com';