-- Find the exact demo user email

-- Check all unique user emails that might be demo
SELECT DISTINCT user_email, COUNT(*) as record_count
FROM policies
WHERE 
    LOWER(user_email) LIKE '%demo%'
    OR LOWER(user_email) LIKE '%agentcommissiontracker%'
    OR user_email ILIKE '%demo%'
GROUP BY user_email
ORDER BY record_count DESC;

-- Also check for any emails with 'STMT' transaction patterns
SELECT DISTINCT user_email, COUNT(*) as stmt_count
FROM policies
WHERE "Transaction ID" LIKE '%-STMT-%'
GROUP BY user_email
ORDER BY stmt_count DESC
LIMIT 10;