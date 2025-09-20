-- DIAGNOSE WHY DEMO ACCOUNT HAS DUPLICATION ISSUES

-- 1. Check how many different user_emails and user_ids we have for demo data
SELECT 
    'User isolation check' as check_type,
    COUNT(DISTINCT user_email) as unique_emails,
    COUNT(DISTINCT user_id) as unique_user_ids,
    COUNT(*) as total_records
FROM policies
WHERE user_email ILIKE '%demo%' OR user_email ILIKE '%agentcommission%';

-- 2. Show the different email variations for demo
SELECT DISTINCT
    user_email,
    user_id,
    COUNT(*) as record_count
FROM policies
WHERE user_email ILIKE '%demo%' OR user_email ILIKE '%agentcommission%'
GROUP BY user_email, user_id
ORDER BY user_email;

-- 3. Check if we have any records without user_id
SELECT 
    'Records without user_id' as check_type,
    COUNT(*) as count
FROM policies
WHERE user_id IS NULL
  AND (user_email ILIKE '%demo%' OR user_email ILIKE '%agentcommission%');

-- 4. See if there are timing patterns in duplicates
SELECT 
    DATE_TRUNC('hour', updated_at) as update_hour,
    COUNT(*) as records_updated,
    COUNT(DISTINCT "Transaction ID") as unique_transactions
FROM policies
WHERE user_email ILIKE '%demo%' OR user_email ILIKE '%agentcommission%'
GROUP BY DATE_TRUNC('hour', updated_at)
ORDER BY update_hour DESC
LIMIT 10;

-- 5. Check for case sensitivity issues
SELECT 
    LOWER(user_email) as normalized_email,
    COUNT(DISTINCT user_email) as email_variations,
    STRING_AGG(DISTINCT user_email, ', ') as all_variations,
    COUNT(*) as total_records
FROM policies
WHERE LOWER(user_email) LIKE '%demo@agentcommission%'
GROUP BY LOWER(user_email);