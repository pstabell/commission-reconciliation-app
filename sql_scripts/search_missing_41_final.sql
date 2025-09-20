-- Find the missing 41 transactions - corrected query

-- 1. Count for each exact demo email variation
SELECT 'Demo email variations:' as check;
SELECT user_email, COUNT(*) as count
FROM policies
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
   OR user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY user_email;

-- 2. Get TOTAL count in entire policies table
SELECT 'TOTAL policies in database:' as check;
SELECT COUNT(*) as total_all_users_policies
FROM policies;

-- 3. Check if there are policies without ANY user_email
SELECT 'Policies with NULL or empty email:' as check;
SELECT COUNT(*) as no_email_count
FROM policies
WHERE user_email IS NULL 
   OR user_email = ''
   OR TRIM(user_email) = '';

-- 4. Look for policies updated today
SELECT 'Recently updated demo policies:' as check;
SELECT 
    DATE(updated_at) as update_date,
    COUNT(*) as count
FROM policies
WHERE LOWER(user_email) LIKE '%demo%'
  AND updated_at > NOW() - INTERVAL '1 day'
GROUP BY DATE(updated_at);

-- 5. Search for any email containing 'agent' or 'commission'
SELECT 'Other possible demo emails:' as check;
SELECT user_email, COUNT(*) as count
FROM policies
WHERE (LOWER(user_email) LIKE '%agent%' 
   OR LOWER(user_email) LIKE '%commission%'
   OR LOWER(user_email) LIKE '%test%'
   OR LOWER(user_email) LIKE '%example%')
   AND LOWER(user_email) != 'demo@agentcommissiontracker.com'
GROUP BY user_email
ORDER BY count DESC;

-- 6. Total unique user_emails in system
SELECT 'Total unique emails:' as check;
SELECT COUNT(DISTINCT user_email) as unique_emails
FROM policies
WHERE user_email IS NOT NULL;