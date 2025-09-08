-- Migration: Add password-related columns to users table
-- Date: January 2025
-- Purpose: Support password setup flow for new users

-- Add password_hash column if it doesn't exist
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS password_hash TEXT;

-- Add password_set flag if it doesn't exist
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS password_set BOOLEAN DEFAULT FALSE;

-- Add comment for documentation
COMMENT ON COLUMN users.password_hash IS 'User password (temporarily plain text, needs hashing for production)';
COMMENT ON COLUMN users.password_set IS 'Flag indicating if user has set their password';

-- Verify the columns were added
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM 
    information_schema.columns
WHERE 
    table_name = 'users'
    AND column_name IN ('password_hash', 'password_set')
ORDER BY 
    column_name;