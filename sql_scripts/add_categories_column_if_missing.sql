-- Add categories column to user_policy_types table if it's missing
-- This handles the case where the table was created without the categories column

-- Check if categories column exists and add it if not
DO $$
BEGIN
    -- Check if the categories column exists
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'user_policy_types' 
        AND column_name = 'categories'
    ) THEN
        -- Add the categories column with default value
        ALTER TABLE user_policy_types 
        ADD COLUMN categories JSONB DEFAULT '["Personal Property", "Personal Auto", "Commercial", "Specialty", "Personal", "Other"]'::jsonb;
        
        RAISE NOTICE 'Added categories column to user_policy_types table';
    ELSE
        RAISE NOTICE 'Categories column already exists in user_policy_types table';
    END IF;
END $$;

-- Verify the column was added
SELECT 
    column_name,
    data_type,
    column_default
FROM information_schema.columns
WHERE table_name = 'user_policy_types'
ORDER BY ordinal_position;

-- Show current table structure
\d user_policy_types