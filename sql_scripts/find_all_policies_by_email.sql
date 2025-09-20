-- Find ALL policies grouped by email to locate the missing 41

-- Show ALL unique user_emails in policies table
SELECT 'All unique emails with policy counts:' as check;
SELECT user_email, COUNT(*) as policy_count
FROM policies
WHERE user_email IS NOT NULL
GROUP BY user_email
ORDER BY policy_count DESC;

-- Check for null emails
SELECT 'Policies with NULL email:' as check;
SELECT COUNT(*) as null_email_count
FROM policies
WHERE user_email IS NULL;

-- Total count in policies table
SELECT 'Total policies in database:' as check;
SELECT COUNT(*) as total_all_policies
FROM policies;

-- Check for any variations of demo/Demo/DEMO
SELECT 'Any demo variations (case insensitive):' as check;
SELECT user_email, COUNT(*) as count
FROM policies
WHERE LOWER(user_email) LIKE '%demo%' 
   OR LOWER(user_email) LIKE '%agent%'
   OR user_email ILIKE '%Demo%'
GROUP BY user_email;

-- Check if there are policies with similar customer names but different emails
SELECT 'Top customers by name:' as check;
SELECT "Customer", COUNT(*) as policy_count, COUNT(DISTINCT user_email) as different_emails
FROM policies
GROUP BY "Customer"
HAVING COUNT(*) > 10
ORDER BY policy_count DESC
LIMIT 20;