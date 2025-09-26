-- Check user mappings initialization status
-- This script verifies which users have mappings and which don't

-- 1. Check how many users exist
SELECT 
    'Total Users' as metric,
    COUNT(*) as count
FROM users;

-- 2. Check users with policy type mappings
SELECT 
    'Users with Policy Mappings' as metric,
    COUNT(DISTINCT user_email) as count
FROM user_policy_type_mappings;

-- 3. Check users with transaction type mappings  
SELECT 
    'Users with Transaction Mappings' as metric,
    COUNT(DISTINCT user_email) as count
FROM user_transaction_type_mappings;

-- 4. Find users WITHOUT policy mappings
SELECT 
    'Users WITHOUT Policy Mappings' as category,
    u.email,
    u.created_at as user_created
FROM users u
LEFT JOIN user_policy_type_mappings pm ON u.email = pm.user_email
WHERE pm.id IS NULL
ORDER BY u.created_at DESC
LIMIT 10;

-- 5. Find users WITHOUT transaction mappings
SELECT 
    'Users WITHOUT Transaction Mappings' as category,
    u.email,
    u.created_at as user_created
FROM users u
LEFT JOIN user_transaction_type_mappings tm ON u.email = tm.user_email
WHERE tm.id IS NULL
ORDER BY u.created_at DESC
LIMIT 10;

-- 6. Check sample of existing mappings to verify structure
SELECT 
    'Policy Mappings Sample' as type,
    user_email,
    jsonb_pretty(mappings) as mappings,
    created_at
FROM user_policy_type_mappings
WHERE mappings IS NOT NULL
LIMIT 2;

SELECT 
    'Transaction Mappings Sample' as type,
    user_email,
    jsonb_pretty(mappings) as mappings,
    created_at
FROM user_transaction_type_mappings
WHERE mappings IS NOT NULL
LIMIT 2;