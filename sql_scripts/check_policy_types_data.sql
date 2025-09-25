-- Check policy types data structure and content
-- This script investigates why policy types aren't displaying in Admin Panel

-- 1. Check if user_policy_types table has any data
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT user_email) as unique_users
FROM user_policy_types;

-- 2. Look at the structure of policy_types column for a few records
SELECT 
    id,
    user_email,
    user_id,
    LENGTH(policy_types::text) as policy_types_length,
    CASE 
        WHEN policy_types IS NULL THEN 'NULL'
        WHEN policy_types::text = '[]' THEN 'EMPTY_ARRAY'
        WHEN policy_types::text = '{}' THEN 'EMPTY_OBJECT'
        WHEN LENGTH(policy_types::text) < 10 THEN policy_types::text
        ELSE 'HAS_DATA'
    END as policy_types_status,
    SUBSTRING(policy_types::text, 1, 100) as policy_types_preview
FROM user_policy_types
LIMIT 10;

-- 3. Check for specific user's data
SELECT 
    id,
    user_email,
    policy_types,
    default_type,
    created_at,
    updated_at
FROM user_policy_types
WHERE user_email = 'patricksweetman@mac.com'
LIMIT 1;

-- 4. Count records by policy_types status
SELECT 
    CASE 
        WHEN policy_types IS NULL THEN 'NULL'
        WHEN policy_types::text = '[]' THEN 'EMPTY_ARRAY'
        WHEN policy_types::text = '{}' THEN 'EMPTY_OBJECT'
        WHEN LENGTH(policy_types::text) < 3 THEN 'ALMOST_EMPTY'
        ELSE 'HAS_DATA'
    END as status,
    COUNT(*) as count
FROM user_policy_types
GROUP BY status
ORDER BY count DESC;

-- 5. Sample a record that has data to see the structure
SELECT 
    user_email,
    policy_types
FROM user_policy_types
WHERE LENGTH(policy_types::text) > 100
LIMIT 1;

-- 6. Check if any records have the expected default policy types
SELECT 
    user_email,
    policy_types::text LIKE '%AUTOP%' as has_autop,
    policy_types::text LIKE '%HOME%' as has_home,
    policy_types::text LIKE '%WC%' as has_wc
FROM user_policy_types
WHERE policy_types IS NOT NULL
LIMIT 10;