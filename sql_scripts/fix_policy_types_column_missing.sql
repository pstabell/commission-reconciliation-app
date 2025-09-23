-- Fix for missing policy_types column error
-- Run this script to add the missing column to your user_policy_types table

-- 1. First check current table structure
\echo 'Current table structure:'
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'user_policy_types'
ORDER BY ordinal_position;

-- 2. Add the missing policy_types column if it doesn't exist
DO $$ 
BEGIN
    -- Check if column exists
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'user_policy_types' 
        AND column_name = 'policy_types'
    ) THEN
        -- Add the column
        ALTER TABLE user_policy_types 
        ADD COLUMN policy_types JSONB NOT NULL DEFAULT '[]'::jsonb;
        
        RAISE NOTICE 'Successfully added policy_types column';
    ELSE
        RAISE NOTICE 'policy_types column already exists';
    END IF;
END $$;

-- 3. If you have existing data in a different format, migrate it
-- This handles the case where policy types were stored as individual rows
DO $$
DECLARE
    user_record RECORD;
    policy_types_array JSONB;
BEGIN
    -- For each user, collect their policy types into an array
    FOR user_record IN 
        SELECT DISTINCT user_email, user_id 
        FROM user_policy_types 
        WHERE policy_types = '[]'::jsonb OR policy_types IS NULL
    LOOP
        -- Collect all policy types for this user
        SELECT jsonb_agg(
            jsonb_build_object(
                'code', COALESCE(code, policy_type, type_code, ''),
                'name', COALESCE(name, policy_name, type_name, code, policy_type, type_code, ''),
                'active', COALESCE(active, true)
            )
        )
        INTO policy_types_array
        FROM user_policy_types
        WHERE user_email = user_record.user_email
        AND (code IS NOT NULL OR policy_type IS NOT NULL OR type_code IS NOT NULL);
        
        -- Update the user's record with the array
        IF policy_types_array IS NOT NULL THEN
            UPDATE user_policy_types 
            SET policy_types = policy_types_array
            WHERE user_email = user_record.user_email;
        END IF;
    END LOOP;
END $$;

-- 4. Clean up any duplicate rows if we migrated from normalized structure
-- Keep only one row per user with all their policy types
DELETE FROM user_policy_types a
USING user_policy_types b
WHERE a.id < b.id 
AND a.user_email = b.user_email
AND jsonb_array_length(b.policy_types) > 0;

-- 5. Verify the fix
\echo ''
\echo 'After fix - table structure:'
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'user_policy_types'
AND column_name = 'policy_types';

\echo ''
\echo 'Sample data:'
SELECT user_email, jsonb_array_length(policy_types) as type_count
FROM user_policy_types
LIMIT 5;

-- 6. Create unique constraint if missing
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.table_constraints
        WHERE constraint_name = 'unique_user_email'
        AND table_name = 'user_policy_types'
    ) THEN
        ALTER TABLE user_policy_types
        ADD CONSTRAINT unique_user_email UNIQUE(user_email);
    END IF;
END $$;

\echo ''
\echo 'Fix completed! You can now use the Initialize Default Policy Types button.'