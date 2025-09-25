-- Comprehensive diagnosis of policy types issue

-- 1. Check exact structure in database
SELECT 
    'Database Structure Check' as test,
    user_email,
    user_id,
    jsonb_typeof(policy_types) as data_type,
    jsonb_array_length(policy_types) as array_length,
    policy_types->0 as first_item,
    pg_column_size(policy_types::text) as data_size
FROM user_policy_types
WHERE user_email = 'patrickstabell@outlook.com';

-- 2. Check if query with user_id works
SELECT 
    'User ID Query Test' as test,
    COUNT(*) as records_found
FROM user_policy_types
WHERE user_id = '89a3d8d1-bbe2-4cce-961e-e765c0598237';

-- 3. Check case sensitivity
SELECT 
    'Email Case Test' as test,
    user_email,
    user_email = 'patrickstabell@outlook.com' as exact_match,
    LOWER(user_email) = LOWER('patrickstabell@outlook.com') as case_insensitive_match
FROM user_policy_types
WHERE LOWER(user_email) = LOWER('patrickstabell@outlook.com');

-- 4. Check what the app would see with simplified structure
SELECT 
    'Simplified Structure Test' as test,
    jsonb_build_object(
        'policy_types', policy_types,
        'default', 'GL',
        'categories', '[]'::jsonb
    ) as expected_structure
FROM user_policy_types
WHERE user_email = 'patrickstabell@outlook.com';

-- 5. Force reset to known good structure
-- ONLY RUN THIS IF NOTHING ELSE WORKS
/*
UPDATE user_policy_types
SET policy_types = '[
    {"code": "GL", "name": "General Liability", "active": true, "category": "Commercial"},
    {"code": "WC", "name": "Workers Compensation", "active": true, "category": "Commercial"},
    {"code": "BOP", "name": "Business Owners Policy", "active": true, "category": "Commercial"},
    {"code": "AUTO", "name": "Auto", "active": true, "category": "Personal Auto"},
    {"code": "HOME", "name": "Homeowners", "active": true, "category": "Personal Property"},
    {"code": "UMBR", "name": "Umbrella", "active": true, "category": "Personal"}
]'::jsonb
WHERE user_email = 'patrickstabell@outlook.com';
*/