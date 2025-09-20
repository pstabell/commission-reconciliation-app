-- Check current database structure

-- 1. Does users table exist?
SELECT 'Users table exists?' as check;
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = 'users'
) as users_table_exists;

-- 2. What columns does users table have?
SELECT 'Users table columns:' as check;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- 3. What's in the users table?
SELECT 'Users table data:' as check;
SELECT * FROM users LIMIT 5;

-- 4. What columns does policies table have?
SELECT 'Policies table columns (showing relevant ones):' as check;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'policies'
AND column_name LIKE '%user%' OR column_name LIKE '%email%'
ORDER BY column_name;

-- 5. How is data currently isolated?
SELECT 'Current data isolation method:' as check;
SELECT DISTINCT user_email, COUNT(*) as record_count
FROM policies
WHERE user_email IS NOT NULL
GROUP BY user_email
ORDER BY COUNT(*) DESC
LIMIT 10;