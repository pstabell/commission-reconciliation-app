-- Find the missing 41 transactions with different email cases

-- First, let's see ALL email variations in policies table
SELECT 'All email variations in policies:' as check;
SELECT user_email, COUNT(*) as count
FROM policies
WHERE LOWER(user_email) LIKE '%demo%'
GROUP BY user_email
ORDER BY count DESC;

-- Find policies WITHOUT user_id that belong to demo
SELECT 'Policies without user_id:' as check;
SELECT COUNT(*) as missing_user_id_count
FROM policies
WHERE user_id IS NULL
AND LOWER(user_email) LIKE '%demo%';

-- Show sample of policies without user_id
SELECT 'Sample policies missing user_id:' as check;
SELECT "Transaction ID", "Customer", user_email, "Policy Number", "Premium Sold"
FROM policies
WHERE user_id IS NULL
AND LOWER(user_email) LIKE '%demo%'
LIMIT 10;

-- Get the demo user_id we need to assign
SELECT 'Demo user_id to use:' as check;
SELECT id, email
FROM users
WHERE email = 'demo@agentcommissiontracker.com';

-- Count total demo policies across ALL email variations
SELECT 'Total demo policies (all email variations):' as check;
SELECT COUNT(*) as total_demo_policies
FROM policies
WHERE LOWER(user_email) LIKE '%demo%';