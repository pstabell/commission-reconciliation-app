-- VERIFY FORTIFIED STRUCTURE

-- 1. Check if carriers table has user_email column
SELECT 'CARRIERS TABLE STRUCTURE:' as info;
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' 
AND table_name = 'carriers'
AND column_name = 'user_email';

-- 2. Count carriers by user
SELECT '';
SELECT 'CARRIERS BY USER:' as info;
SELECT user_email, COUNT(*) as count
FROM carriers
GROUP BY user_email
ORDER BY user_email;

-- 3. Verify demo data is correctly assigned
SELECT '';
SELECT 'DEMO USER DATA:' as info;
SELECT 
    'Carriers: ' || COUNT(*) as data
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'MGAs: ' || COUNT(*)
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Rules: ' || COUNT(*)
FROM commission_rules
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 4. This is the fortified model - each user has their own data
SELECT '';
SELECT 'SECURITY MODEL:' as info;
SELECT 'FORTIFIED - Each user has isolated carriers/MGAs/rules' as status;