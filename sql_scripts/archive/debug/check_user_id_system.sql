-- CHECK USER ID VS EMAIL SYSTEM

-- 1. Check if carriers table has user_id column
SELECT 'CARRIERS TABLE COLUMNS:' as info;
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' 
AND table_name = 'carriers'
AND column_name IN ('user_id', 'user_email')
ORDER BY column_name;

-- 2. Check users table for demo user
SELECT '';
SELECT 'DEMO USER IN USERS TABLE:' as info;
SELECT id, email, created_at
FROM users
WHERE email = 'demo@agentcommissiontracker.com';

-- 3. Check if we're using user_id or user_email in carriers
SELECT '';
SELECT 'CARRIERS DATA SAMPLE:' as info;
SELECT 
    CASE 
        WHEN user_id IS NOT NULL THEN 'Using user_id'
        WHEN user_email IS NOT NULL THEN 'Using user_email'
        ELSE 'Neither'
    END as system_type,
    COUNT(*) as count
FROM carriers
GROUP BY system_type;

-- 4. If using user_id, find demo user's ID and check carriers
SELECT '';
SELECT 'DEMO USER ID AND CARRIERS:' as info;
WITH demo_user AS (
    SELECT id 
    FROM users 
    WHERE email = 'demo@agentcommissiontracker.com'
)
SELECT 
    'Demo User ID: ' || COALESCE(du.id::text, 'NOT FOUND') as info,
    COUNT(c.*) as carriers_with_this_id
FROM demo_user du
LEFT JOIN carriers c ON c.user_id = du.id
GROUP BY du.id;

-- 5. Check what's in the carriers table
SELECT '';
SELECT 'SAMPLE CARRIERS DATA:' as info;
SELECT user_id, user_email, carrier_name
FROM carriers
LIMIT 5;