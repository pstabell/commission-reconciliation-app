-- Check the structure of policy_types data for patrickstabell@outlook.com
-- This will help us understand why the app shows "No policy types found"

-- First, check the raw data
SELECT 
    user_email,
    user_id,
    pg_typeof(policy_types) as policy_types_type,
    policy_types IS NULL as is_null,
    jsonb_typeof(policy_types) as jsonb_type,
    jsonb_array_length(policy_types) as array_length,
    policy_types::text as raw_text_value
FROM user_policy_types
WHERE user_email = 'patrickstabell@outlook.com';

-- Check the first element of the array to see its structure
SELECT 
    user_email,
    policy_types->0 as first_element,
    jsonb_typeof(policy_types->0) as first_element_type,
    policy_types->0->>'code' as first_code,
    policy_types->0->>'name' as first_name
FROM user_policy_types
WHERE user_email = 'patrickstabell@outlook.com';

-- Check if the array contains strings instead of objects
SELECT 
    user_email,
    jsonb_array_elements_text(policy_types) as element_value
FROM user_policy_types
WHERE user_email = 'patrickstabell@outlook.com'
LIMIT 5;

-- If the above fails, try this to see the structure
SELECT 
    user_email,
    jsonb_pretty(policy_types) as pretty_policy_types
FROM user_policy_types
WHERE user_email = 'patrickstabell@outlook.com';