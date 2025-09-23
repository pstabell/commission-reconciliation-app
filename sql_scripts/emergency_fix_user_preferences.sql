-- Emergency fix for user_preferences table column error
-- This ensures the tables have the correct structure

-- Step 1: Check current structure of user_preferences
SELECT 
    'Current user_preferences columns:' as info,
    column_name, 
    data_type,
    column_default
FROM information_schema.columns 
WHERE table_name = 'user_preferences'
ORDER BY ordinal_position;

-- Step 2: If user_preferences has wrong columns, we need to fix it
-- First backup any existing data
CREATE TABLE IF NOT EXISTS user_preferences_backup AS 
SELECT * FROM user_preferences;

-- Step 3: Drop and recreate user_preferences with correct schema
DROP TABLE IF EXISTS user_preferences CASCADE;

CREATE TABLE user_preferences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    color_theme TEXT DEFAULT 'light',
    other_preferences JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_preferences_user_id UNIQUE(user_id),
    CONSTRAINT unique_user_preferences_user_email UNIQUE(user_email)
);

-- Step 4: Restore data from backup (only valid columns)
INSERT INTO user_preferences (id, user_id, user_email, color_theme, other_preferences, created_at, updated_at)
SELECT 
    id,
    user_id,
    user_email,
    COALESCE(color_theme, 'light'),
    COALESCE(other_preferences, '{}'::jsonb),
    created_at,
    updated_at
FROM user_preferences_backup
WHERE user_email IS NOT NULL
ON CONFLICT (user_id) DO NOTHING;

-- Step 5: Ensure user_policy_types has correct structure
SELECT 
    'Current user_policy_types columns:' as info,
    column_name, 
    data_type,
    column_default
FROM information_schema.columns 
WHERE table_name = 'user_policy_types'
ORDER BY ordinal_position;

-- Step 6: Create user_policy_types if it doesn't exist
CREATE TABLE IF NOT EXISTS user_policy_types (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_email TEXT NOT NULL,
    policy_types JSONB NOT NULL DEFAULT '[]'::jsonb,
    default_type TEXT DEFAULT 'HO3',
    categories JSONB DEFAULT '["Personal Property", "Personal Auto", "Commercial", "Specialty", "Personal", "Other"]'::jsonb,
    version TEXT DEFAULT '1.0.0',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_policy_types_user_id UNIQUE(user_id),
    CONSTRAINT unique_user_policy_types_user_email UNIQUE(user_email)
);

-- Step 7: Initialize default data for any users without preferences
INSERT INTO user_preferences (user_id, user_email, color_theme)
SELECT 
    id as user_id,
    email as user_email,
    'light' as color_theme
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM user_preferences up 
    WHERE up.user_id = u.id OR up.user_email = u.email
)
ON CONFLICT DO NOTHING;

-- Step 8: Initialize default policy types for any users without them
INSERT INTO user_policy_types (user_id, user_email, policy_types, default_type)
SELECT 
    id as user_id,
    email as user_email,
    '[{"code": "HO3", "name": "HO3", "active": true, "category": "Personal Property"}]'::jsonb,
    'HO3'
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM user_policy_types upt 
    WHERE upt.user_id = u.id OR upt.user_email = u.email
)
ON CONFLICT DO NOTHING;

-- Step 9: Clean up backup table (uncomment when ready)
-- DROP TABLE IF EXISTS user_preferences_backup;

-- Step 10: Verify the fix
SELECT 
    'Final user_preferences structure:' as info,
    COUNT(*) as row_count
FROM user_preferences;

SELECT 
    'Final user_policy_types structure:' as info,
    COUNT(*) as row_count
FROM user_policy_types;