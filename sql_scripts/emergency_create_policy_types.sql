-- Emergency script to create policy types directly in database
-- This bypasses any column issues by only using essential columns

-- First, check what columns actually exist
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'user_policy_types'
ORDER BY ordinal_position;

-- Create policy types for the current user
-- Replace 'YOUR_USER_EMAIL' with your actual email
INSERT INTO user_policy_types (user_email, policy_types)
VALUES (
    'YOUR_USER_EMAIL', 
    '[
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
    ]'::jsonb
)
ON CONFLICT (user_email) 
DO UPDATE SET policy_types = EXCLUDED.policy_types;

-- Verify it worked
SELECT user_email, jsonb_array_length(policy_types) as type_count
FROM user_policy_types
WHERE user_email = 'YOUR_USER_EMAIL';