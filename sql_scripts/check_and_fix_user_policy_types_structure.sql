-- Check current structure of user_policy_types table
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'user_policy_types'
ORDER BY ordinal_position;

-- If the table has wrong structure (individual rows per type), we need to recreate it
-- First, let's see if we have the normalized structure
SELECT COUNT(*) as row_count, COUNT(DISTINCT user_email) as user_count
FROM user_policy_types;

-- Option 1: Add the missing policy_types column if table exists but column is missing
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'user_policy_types' 
        AND column_name = 'policy_types'
    ) THEN
        ALTER TABLE user_policy_types 
        ADD COLUMN policy_types JSONB NOT NULL DEFAULT '[]'::jsonb;
        
        RAISE NOTICE 'Added policy_types column to user_policy_types table';
    END IF;
END $$;

-- Option 2: If table doesn't exist at all, create it with correct structure
CREATE TABLE IF NOT EXISTS user_policy_types (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID,
    user_email TEXT NOT NULL,
    policy_types JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_email UNIQUE(user_email)
);

-- Create indexes if they don't exist
CREATE INDEX IF NOT EXISTS idx_user_policy_types_user_email 
ON user_policy_types(user_email);

-- Grant permissions
GRANT ALL ON user_policy_types TO authenticated;
GRANT ALL ON user_policy_types TO anon;

-- Now verify the structure
SELECT 
    column_name, 
    data_type
FROM information_schema.columns 
WHERE table_name = 'user_policy_types'
ORDER BY ordinal_position;