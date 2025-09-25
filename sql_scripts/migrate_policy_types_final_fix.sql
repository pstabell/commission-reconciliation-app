-- Final fixed migration for policy types

-- 1. Show current data structure
SELECT 'Before migration:' as status, user_email, policy_type, policy_types
FROM user_policy_types 
ORDER BY user_email;

-- 2. Remove NOT NULL constraints from old columns
ALTER TABLE user_policy_types ALTER COLUMN policy_type DROP NOT NULL;
ALTER TABLE user_policy_types ALTER COLUMN display_order DROP NOT NULL;
ALTER TABLE user_policy_types ALTER COLUMN is_active DROP NOT NULL;

-- 3. Create backup of existing data
CREATE TEMP TABLE policy_types_backup AS
SELECT * FROM user_policy_types;

-- 4. Update the policy_types JSONB column with migrated data
UPDATE user_policy_types ut
SET policy_types = (
    SELECT jsonb_agg(
        jsonb_build_object(
            'code', UPPER(REPLACE(policy_type, ' ', '_')),
            'name', policy_type,
            'active', COALESCE(is_active, true)
        ) ORDER BY display_order
    )
    FROM policy_types_backup b
    WHERE b.user_email = ut.user_email
);

-- 5. Add default policy types to each user's array
UPDATE user_policy_types
SET policy_types = COALESCE(policy_types, '[]'::jsonb) || '[
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

-- 6. Drop the old columns
ALTER TABLE user_policy_types DROP COLUMN IF EXISTS policy_type;
ALTER TABLE user_policy_types DROP COLUMN IF EXISTS display_order;
ALTER TABLE user_policy_types DROP COLUMN IF EXISTS is_active;

-- 7. Clean up duplicate rows (keep the first row for each user by created_at)
DELETE FROM user_policy_types a
USING user_policy_types b
WHERE a.user_id = b.user_id
AND a.created_at > b.created_at;

-- 8. Verify the migration
SELECT 
    'After migration:' as status,
    user_email, 
    jsonb_array_length(policy_types) as total_types,
    LEFT(policy_types::text, 100) || '...' as policy_types_preview
FROM user_policy_types
ORDER BY user_email;

-- Show final status
SELECT 
    COUNT(*) as total_users,
    COUNT(DISTINCT user_id) as unique_users,
    'Migration complete!' as status
FROM user_policy_types;