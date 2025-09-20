-- Check if user_id system is already implemented

-- 1. Check if users table exists and has data
SELECT 'Users table status:' as check;
SELECT COUNT(*) as user_count FROM users;

-- 2. Check if policies table has user_id column
SELECT 'Columns in policies table:' as check;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'policies' 
AND column_name IN ('user_id', 'user_email')
ORDER BY column_name;

-- 3. Check if user_id is populated
SELECT 'User ID population in policies:' as check;
SELECT 
    COUNT(*) as total_records,
    COUNT(user_id) as records_with_user_id,
    COUNT(user_email) as records_with_user_email
FROM policies;

-- 4. Check demo user specifically
SELECT 'Demo user in users table:' as check;
SELECT id, email 
FROM users 
WHERE LOWER(email) = 'demo@agentcommissiontracker.com';

-- 5. Check if demo's policies have user_id
SELECT 'Demo policies with user_id:' as check;
SELECT COUNT(*) as demo_policies_with_user_id
FROM policies p
JOIN users u ON p.user_id = u.id
WHERE LOWER(u.email) = 'demo@agentcommissiontracker.com';