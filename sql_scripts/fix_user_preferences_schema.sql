-- Fix for user_preferences table schema issue
-- This script ensures the user_preferences table has the correct schema
-- and removes any invalid columns that might have been accidentally added

-- First, let's check what columns exist in user_preferences
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'user_preferences' 
ORDER BY ordinal_position;

-- If there are extra columns like 'default_type' or 'policy_types' in user_preferences,
-- we need to remove them as they belong to user_policy_types table

-- Option 1: If the table has wrong columns, recreate it with correct schema
-- WARNING: This will drop existing data, so backup first!
/*
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

-- Re-populate with default data
INSERT INTO user_preferences (user_id, user_email, color_theme)
SELECT 
    id as user_id,
    email as user_email,
    'light' as color_theme
FROM users
ON CONFLICT (user_id) DO NOTHING;
*/

-- Option 2: If you want to preserve existing data and just remove wrong columns
-- (Uncomment the ALTER TABLE statements for columns that shouldn't exist)
/*
ALTER TABLE user_preferences DROP COLUMN IF EXISTS default_type;
ALTER TABLE user_preferences DROP COLUMN IF EXISTS policy_types;
ALTER TABLE user_preferences DROP COLUMN IF EXISTS categories;
ALTER TABLE user_preferences DROP COLUMN IF EXISTS version;
*/

-- Verify the user_policy_types table has the correct schema
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'user_policy_types' 
ORDER BY ordinal_position;

-- The user_policy_types table should have these columns:
-- id, user_id, user_email, policy_types, default_type, categories, version, created_at, updated_at