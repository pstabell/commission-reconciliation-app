-- Check if Demo user's data still exists
SELECT 
    COUNT(*) as total_records,
    user_email,
    MIN(created_at) as oldest_record,
    MAX(created_at) as newest_record
FROM policies
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY user_email;

-- Check for any case sensitivity issues
SELECT DISTINCT user_email, COUNT(*) as count
FROM policies
WHERE LOWER(user_email) LIKE '%demo%'
GROUP BY user_email;

-- Check all user emails to see data distribution
SELECT 
    user_email,
    COUNT(*) as record_count
FROM policies
GROUP BY user_email
ORDER BY COUNT(*) DESC;

-- Check if there are any records at all
SELECT COUNT(*) as total_records_in_table FROM policies;