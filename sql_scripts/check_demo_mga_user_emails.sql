-- Check the exact user_email values for MGAs and compare with expected demo email

-- 1. Check all unique user_email values in mgas table that might be demo
SELECT DISTINCT user_email, COUNT(*) as mga_count
FROM mgas
WHERE 
    user_email ILIKE '%demo%'
    OR user_email ILIKE '%agentcommissiontracker%'
GROUP BY user_email
ORDER BY mga_count DESC;

-- 2. Check if there are MGAs with the exact case-sensitive email
SELECT COUNT(*) as exact_match_count
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 3. Check if there are MGAs with case-insensitive match
SELECT COUNT(*) as case_insensitive_count
FROM mgas
WHERE LOWER(user_email) = LOWER('Demo@AgentCommissionTracker.com');

-- 4. Show sample MGAs for any demo-like emails
SELECT mga_id, mga_name, user_email, status, created_at
FROM mgas
WHERE 
    LOWER(user_email) LIKE '%demo%'
    OR LOWER(user_email) LIKE '%agentcommissiontracker%'
ORDER BY created_at DESC
LIMIT 10;

-- 5. Check what exact email the demo user has in users table
SELECT email, subscription_status
FROM users
WHERE LOWER(email) LIKE '%demo%';

-- 6. Compare user emails between tables
SELECT 
    'Users table' as source,
    email as user_email,
    COUNT(*) as record_count
FROM users
WHERE LOWER(email) LIKE '%demo%'
GROUP BY email

UNION ALL

SELECT 
    'MGAs table' as source,
    user_email,
    COUNT(*) as record_count
FROM mgas
WHERE LOWER(user_email) LIKE '%demo%'
GROUP BY user_email

UNION ALL

SELECT 
    'Carriers table' as source,
    user_email,
    COUNT(*) as record_count
FROM carriers
WHERE LOWER(user_email) LIKE '%demo%'
GROUP BY user_email

ORDER BY source, user_email;