-- Fix empty policy_types for Patrick Stabell's account
-- This will populate the empty array with default policy types

-- First, check current status
SELECT 
    id,
    user_id,
    user_email,
    jsonb_array_length(policy_types) as policy_types_count,
    created_at,
    updated_at
FROM user_policy_types
WHERE user_id = '89a3d8d1-bbe2-4cce-961e-e765c0598237';

-- Update with default policy types if empty
UPDATE user_policy_types 
SET policy_types = '[
    {"code": "AUTOP", "name": "AUTOP", "active": true, "category": "Other"},
    {"code": "HOME", "name": "HOME", "active": true, "category": "Personal Property"},
    {"code": "DFIRE", "name": "DFIRE", "active": true, "category": "Personal Property"},
    {"code": "WC", "name": "WC", "active": true, "category": "Other"},
    {"code": "AUTOB", "name": "AUTOB", "active": true, "category": "Other"},
    {"code": "GL", "name": "GL", "active": true, "category": "Other"},
    {"code": "FLOOD", "name": "FLOOD", "active": true, "category": "Specialty"},
    {"code": "BOAT", "name": "BOAT", "active": true, "category": "Specialty"},
    {"code": "CONDO", "name": "CONDO", "active": true, "category": "Personal Property"},
    {"code": "PROP-C", "name": "PROP-C", "active": true, "category": "Other"},
    {"code": "PACKAGE-P", "name": "PACKAGE-P", "active": true, "category": "Other"},
    {"code": "UMB-P", "name": "UMB-P", "active": true, "category": "Other"},
    {"code": "IM-C", "name": "IM-C", "active": true, "category": "Other"},
    {"code": "GARAGE", "name": "GARAGE", "active": true, "category": "Other"},
    {"code": "UMB-C", "name": "UMB-C", "active": true, "category": "Other"},
    {"code": "OCEAN MARINE", "name": "OCEAN MARINE", "active": true, "category": "Other"},
    {"code": "WIND-P", "name": "WIND-P", "active": true, "category": "Other"},
    {"code": "PL", "name": "PL", "active": true, "category": "Other"},
    {"code": "COLLECTOR", "name": "COLLECTOR", "active": true, "category": "Other"},
    {"code": "PACKAGE-C", "name": "PACKAGE-C", "active": true, "category": "Commercial"},
    {"code": "FLOOD-C", "name": "FLOOD-C", "active": true, "category": "Other"},
    {"code": "BOP", "name": "BOP", "active": true, "category": "Commercial"},
    {"code": "BPP", "name": "BPP", "active": true, "category": "Other"},
    {"code": "EXCESS", "name": "EXCESS", "active": true, "category": "Other"},
    {"code": "CYBER", "name": "CYBER", "active": true, "category": "Commercial"},
    {"code": "D&O", "name": "D&O", "active": true, "category": "Other"},
    {"code": "CYCLE", "name": "CYCLE", "active": true, "category": "Personal Auto"},
    {"code": "AUTO", "name": "AUTO", "active": true, "category": "Personal Auto"},
    {"code": "RV", "name": "RV", "active": true, "category": "Personal Auto"},
    {"code": "RENTERS", "name": "RENTERS", "active": true, "category": "Personal Property"},
    {"code": "UMBRELLA", "name": "UMBRELLA-C", "active": true, "category": "Commercial"},
    {"code": "MOBILE", "name": "MOBILE", "active": true, "category": "Personal Property"},
    {"code": "WIND", "name": "WIND", "active": true, "category": "Specialty"},
    {"code": "UMBRELLA-P", "name": "UMBRELLA-P", "active": true, "category": "Personal"}
]'::jsonb,
updated_at = now()
WHERE user_id = '89a3d8d1-bbe2-4cce-961e-e765c0598237'
  AND (policy_types IS NULL OR policy_types = '[]'::jsonb OR jsonb_array_length(policy_types) = 0);

-- Verify the update
SELECT 
    id,
    user_id,
    user_email,
    jsonb_array_length(policy_types) as policy_types_count,
    policy_types->0->>'code' as first_policy_type,
    updated_at
FROM user_policy_types
WHERE user_id = '89a3d8d1-bbe2-4cce-961e-e765c0598237';