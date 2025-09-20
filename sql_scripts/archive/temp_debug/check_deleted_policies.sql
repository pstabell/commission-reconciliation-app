-- Check the deleted_policies table for our missing 41 transactions

-- 1. Count deleted policies for demo user
SELECT 'Deleted demo policies count:' as check;
SELECT COUNT(*) as deleted_count
FROM deleted_policies
WHERE LOWER(user_email) LIKE '%demo%';

-- 2. Show deleted policies details
SELECT 'Deleted policies details:' as check;
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Premium Sold",
    user_email,
    deleted_at
FROM deleted_policies
WHERE LOWER(user_email) LIKE '%demo%'
ORDER BY deleted_at DESC
LIMIT 50;

-- 3. Group by email to see variations
SELECT 'Deleted policies by email:' as check;
SELECT user_email, COUNT(*) as count
FROM deleted_policies
WHERE LOWER(user_email) LIKE '%demo%'
GROUP BY user_email;

-- 4. When were they deleted?
SELECT 'Deletion timeline:' as check;
SELECT 
    DATE(deleted_at) as deletion_date,
    COUNT(*) as policies_deleted
FROM deleted_policies
WHERE LOWER(user_email) LIKE '%demo%'
GROUP BY DATE(deleted_at)
ORDER BY deletion_date DESC;

-- 5. Total in deleted_policies
SELECT 'Total in deleted_policies table:' as check;
SELECT COUNT(*) as total_deleted
FROM deleted_policies;

-- 6. Check if these can be restored (look for restore-related columns)
SELECT 'Deleted_policies table structure:' as check;
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'deleted_policies'
ORDER BY ordinal_position
LIMIT 10;