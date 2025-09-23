-- Fix user_policy_types table structure to match Python code expectations
-- The Python code expects JSONB columns, not individual rows per policy type

-- First, backup existing data if any
CREATE TABLE IF NOT EXISTS user_policy_types_backup AS 
SELECT * FROM user_policy_types;

-- Drop the old table
DROP TABLE IF EXISTS user_policy_types CASCADE;

-- Create the correct table structure that matches the Python code
CREATE TABLE user_policy_types (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    policy_types JSONB NOT NULL DEFAULT '[]'::jsonb,
    default_type TEXT DEFAULT 'HO3',
    categories JSONB DEFAULT '["Personal Property", "Personal Auto", "Commercial", "Specialty", "Personal", "Other"]'::jsonb,
    version TEXT DEFAULT '1.0.0',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_id UNIQUE(user_id),
    CONSTRAINT unique_user_email UNIQUE(user_email)
);

-- Create indexes
CREATE INDEX idx_user_policy_types_user_id ON user_policy_types(user_id);
CREATE INDEX idx_user_policy_types_user_email ON user_policy_types(user_email);

-- Grant permissions if needed
GRANT ALL ON user_policy_types TO authenticated;
GRANT ALL ON user_policy_types TO anon;

-- Initialize default policy types for existing users
-- This will give each user the full set of 34 default policy types
INSERT INTO user_policy_types (user_id, user_email, policy_types, default_type, categories, version)
SELECT 
    id as user_id,
    email as user_email,
    '[
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
    ]'::jsonb as policy_types,
    'HO3' as default_type,
    '["Personal Property", "Personal Auto", "Commercial", "Specialty", "Personal", "Other"]'::jsonb as categories,
    '1.0.0' as version
FROM users
ON CONFLICT (user_id) DO NOTHING;

-- Verify the fix
SELECT 
    'Fixed user_policy_types table' as status,
    COUNT(*) as users_with_policy_types,
    (SELECT COUNT(*) FROM users) as total_users
FROM user_policy_types;

-- Show sample data
SELECT 
    user_email,
    jsonb_array_length(policy_types) as policy_type_count,
    default_type,
    version
FROM user_policy_types
LIMIT 5;