-- Find the 42 missing records (425 - 383 = 42)

-- 1. Let's check if this is a filtering issue
SELECT 'Total records in database (no filter):' as check;
SELECT COUNT(*) as total_unfiltered FROM policies;

-- 2. Check records for demo user specifically
SELECT 'Demo user records:' as check;
SELECT 
    COUNT(*) as count,
    COUNT(DISTINCT "Transaction ID") as unique_transactions
FROM policies
WHERE user_email ILIKE '%demo@agentcommission%';

-- 3. Check if records got assigned to wrong user
SELECT 'Records by email pattern:' as check;
SELECT 
    user_email,
    COUNT(*) as count
FROM policies
WHERE user_email LIKE '%agentcommission%'
GROUP BY user_email
ORDER BY count DESC;

-- 4. Check for case sensitivity issues again
SELECT 'Email case variations:' as check;
SELECT 
    LOWER(user_email) as normalized_email,
    COUNT(DISTINCT user_email) as variations,
    STRING_AGG(DISTINCT user_email, ', ') as all_variations,
    COUNT(*) as total_records
FROM policies
WHERE LOWER(user_email) LIKE '%demo%'
GROUP BY LOWER(user_email);

-- 5. Look for records with mismatched user_id
SELECT 'User ID check:' as check;
SELECT 
    user_id,
    user_email,
    COUNT(*) as count
FROM policies
WHERE user_email ILIKE '%demo%'
GROUP BY user_id, user_email
ORDER BY count DESC;

-- 6. Sample of actual data to see what's there
SELECT 'Sample records:' as check;
SELECT 
    "Transaction ID",
    "Customer",
    user_email,
    user_id,
    updated_at
FROM policies
ORDER BY updated_at DESC
LIMIT 20;