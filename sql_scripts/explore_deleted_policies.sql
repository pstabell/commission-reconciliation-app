-- First, let's see what columns exist in deleted_policies table

-- 1. Show all columns in deleted_policies
SELECT 'Columns in deleted_policies table:' as check;
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'deleted_policies'
ORDER BY ordinal_position;

-- 2. Get a sample row to see the data
SELECT 'Sample deleted policy:' as check;
SELECT *
FROM deleted_policies
LIMIT 1;

-- 3. Count all deleted policies
SELECT 'Total deleted policies:' as check;
SELECT COUNT(*) as total_deleted
FROM deleted_policies;

-- 4. If user_email column exists, count demo deletions
SELECT 'Count by user (if user_email exists):' as check;
SELECT 
    CASE 
        WHEN user_email IS NULL THEN 'NULL email'
        ELSE user_email 
    END as email,
    COUNT(*) as count
FROM deleted_policies
GROUP BY user_email
ORDER BY count DESC;