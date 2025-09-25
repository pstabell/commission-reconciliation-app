-- Fix user_policy_types table to use proper user_id constraints
-- Following the January 22, 2025 security migration to user_id

-- 1. Check current table structure
\echo 'Current table structure and constraints:'
SELECT 
    c.column_name, 
    c.data_type, 
    c.is_nullable,
    c.column_default
FROM information_schema.columns c
WHERE c.table_name = 'user_policy_types'
ORDER BY c.ordinal_position;

\echo ''
\echo 'Current constraints:'
SELECT 
    con.conname as constraint_name,
    con.contype as constraint_type,
    pg_get_constraintdef(con.oid) as definition
FROM pg_constraint con
JOIN pg_class rel ON rel.oid = con.conrelid
JOIN pg_namespace nsp ON nsp.oid = rel.relnamespace
WHERE rel.relname = 'user_policy_types';

-- 2. Add missing columns if they don't exist
DO $$ 
BEGIN
    -- Add policy_types column if missing
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'user_policy_types' AND column_name = 'policy_types'
    ) THEN
        ALTER TABLE user_policy_types 
        ADD COLUMN policy_types JSONB NOT NULL DEFAULT '[]'::jsonb;
        RAISE NOTICE 'Added policy_types column';
    END IF;

    -- Add user_id column if missing (shouldn't be, but just in case)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'user_policy_types' AND column_name = 'user_id'
    ) THEN
        ALTER TABLE user_policy_types 
        ADD COLUMN user_id UUID REFERENCES users(id);
        RAISE NOTICE 'Added user_id column';
    END IF;
END $$;

-- 3. Drop incorrect constraints
DO $$
BEGIN
    -- Drop unique_user_email if it exists (wrong approach)
    IF EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'unique_user_email'
    ) THEN
        ALTER TABLE user_policy_types DROP CONSTRAINT unique_user_email;
        RAISE NOTICE 'Dropped incorrect unique_user_email constraint';
    END IF;

    -- Drop any other email-based unique constraints
    IF EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'user_policy_types_user_email_key'
    ) THEN
        ALTER TABLE user_policy_types DROP CONSTRAINT user_policy_types_user_email_key;
        RAISE NOTICE 'Dropped email-based constraint';
    END IF;
END $$;

-- 4. Add correct constraints
DO $$
BEGIN
    -- Add unique constraint on user_id (primary identifier)
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'unique_user_id'
    ) THEN
        ALTER TABLE user_policy_types 
        ADD CONSTRAINT unique_user_id UNIQUE(user_id);
        RAISE NOTICE 'Added correct unique_user_id constraint';
    END IF;
END $$;

-- 5. Create proper indexes for performance
CREATE INDEX IF NOT EXISTS idx_user_policy_types_user_id 
ON user_policy_types(user_id);

CREATE INDEX IF NOT EXISTS idx_user_policy_types_user_email 
ON user_policy_types(user_email);

-- 6. Update any NULL user_ids from user_email if possible
UPDATE user_policy_types upt
SET user_id = u.id
FROM users u
WHERE upt.user_id IS NULL 
AND LOWER(upt.user_email) = LOWER(u.email);

-- 7. Verify the structure is correct
\echo ''
\echo 'After fix - constraints:'
SELECT 
    con.conname as constraint_name,
    pg_get_constraintdef(con.oid) as definition
FROM pg_constraint con
JOIN pg_class rel ON rel.oid = con.conrelid
WHERE rel.relname = 'user_policy_types'
ORDER BY con.conname;

\echo ''
\echo 'Table status:'
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT user_id) as unique_user_ids,
    COUNT(DISTINCT user_email) as unique_emails,
    COUNT(CASE WHEN user_id IS NULL THEN 1 END) as null_user_ids
FROM user_policy_types;

\echo ''
\echo 'Sample data:'
SELECT 
    user_id,
    user_email,
    jsonb_array_length(COALESCE(policy_types, '[]'::jsonb)) as policy_type_count,
    CASE 
        WHEN policy_types IS NULL THEN 'NULL'
        WHEN policy_types = '[]'::jsonb THEN 'Empty'
        ELSE 'Has Data'
    END as data_status
FROM user_policy_types
LIMIT 5;

\echo ''
\echo '✅ Table structure fixed to use user_id as primary identifier!'
\echo 'Following security best practices from January 22, 2025 migration.'