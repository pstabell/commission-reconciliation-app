-- Migrate from normalized structure (one row per type) to JSONB array structure
-- This converts existing rows into a single row per user with all types in an array

-- 1. Show current data structure
SELECT 'Before migration:' as status, user_id, user_email, policy_type, display_order, is_active 
FROM user_policy_types 
ORDER BY user_email, display_order;

-- 2. Create temporary table with migrated data
CREATE TEMP TABLE migrated_policy_types AS
SELECT 
    user_id,
    user_email,
    jsonb_agg(
        jsonb_build_object(
            'code', UPPER(REPLACE(policy_type, ' ', '_')),  -- Convert "Personal Lines" to "PERSONAL_LINES"
            'name', policy_type,
            'active', COALESCE(is_active, true)
        ) ORDER BY display_order
    ) as policy_types
FROM user_policy_types
GROUP BY user_id, user_email;

-- 3. Show what will be migrated
SELECT 'Migration preview:' as status, user_email, jsonb_array_length(policy_types) as type_count, policy_types
FROM migrated_policy_types;

-- 4. Clear existing data and insert migrated data
TRUNCATE user_policy_types;

INSERT INTO user_policy_types (user_id, user_email, policy_types)
SELECT user_id, user_email, policy_types
FROM migrated_policy_types;

-- 5. Add default policy types to each user's array
UPDATE user_policy_types
SET policy_types = policy_types || '[
    {"code": "GL", "name": "General Liability", "active": true},
    {"code": "WC", "name": "Workers Compensation", "active": true},
    {"code": "BOP", "name": "Business Owners Policy", "active": true},
    {"code": "CPK", "name": "Commercial Package", "active": true},
    {"code": "CARGO", "name": "Cargo", "active": true},
    {"code": "AUTO", "name": "Auto", "active": true},
    {"code": "AUTOP", "name": "Auto Personal", "active": true},
    {"code": "AUTOB", "name": "Auto Business", "active": true},
    {"code": "EXCESS", "name": "Excess/Umbrella", "active": true},
    {"code": "CYBER", "name": "Cyber Liability", "active": true},
    {"code": "D&O", "name": "Directors & Officers", "active": true},
    {"code": "E&O", "name": "Errors & Omissions", "active": true},
    {"code": "EPLI", "name": "Employment Practices", "active": true},
    {"code": "HOME", "name": "Homeowners", "active": true},
    {"code": "CONDO", "name": "Condo", "active": true},
    {"code": "RENTERS", "name": "Renters", "active": true},
    {"code": "FLOOD", "name": "Flood", "active": true},
    {"code": "WIND", "name": "Wind/Hurricane", "active": true},
    {"code": "BOAT", "name": "Boat/Marine", "active": true},
    {"code": "RV", "name": "Recreational Vehicle", "active": true},
    {"code": "CYCLE", "name": "Motorcycle", "active": true},
    {"code": "UMBR", "name": "Umbrella Personal", "active": true},
    {"code": "LIFE", "name": "Life Insurance", "active": true},
    {"code": "HEALTH", "name": "Health Insurance", "active": true},
    {"code": "OTHER", "name": "Other", "active": true}
]'::jsonb;

-- 6. Drop the old columns that are no longer needed
ALTER TABLE user_policy_types DROP COLUMN IF EXISTS policy_type;
ALTER TABLE user_policy_types DROP COLUMN IF EXISTS display_order;
ALTER TABLE user_policy_types DROP COLUMN IF EXISTS is_active;

-- 7. Verify the migration
SELECT 
    'After migration:' as status,
    user_email, 
    jsonb_array_length(policy_types) as total_types,
    policy_types->0 as first_type_example
FROM user_policy_types;