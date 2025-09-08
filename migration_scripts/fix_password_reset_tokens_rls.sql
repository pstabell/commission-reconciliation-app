-- Migration: Fix Row Level Security for password_reset_tokens table
-- Date: January 2025
-- Purpose: Allow webhook and app to create password reset/setup tokens

-- Option 1: Disable RLS on password_reset_tokens table (simplest for MVP)
ALTER TABLE password_reset_tokens DISABLE ROW LEVEL SECURITY;

-- OR Option 2: Create proper RLS policies (more secure)
-- First, ensure RLS is enabled
-- ALTER TABLE password_reset_tokens ENABLE ROW LEVEL SECURITY;

-- Then create policies
-- DROP POLICY IF EXISTS "Enable insert for service role" ON password_reset_tokens;
-- CREATE POLICY "Enable insert for service role" ON password_reset_tokens
-- FOR INSERT
-- TO authenticated, anon
-- WITH CHECK (true);

-- DROP POLICY IF EXISTS "Enable read for token validation" ON password_reset_tokens;
-- CREATE POLICY "Enable read for token validation" ON password_reset_tokens
-- FOR SELECT
-- TO authenticated, anon
-- USING (true);

-- DROP POLICY IF EXISTS "Enable update for marking tokens used" ON password_reset_tokens;
-- CREATE POLICY "Enable update for marking tokens used" ON password_reset_tokens
-- FOR UPDATE
-- TO authenticated, anon
-- USING (true)
-- WITH CHECK (true);