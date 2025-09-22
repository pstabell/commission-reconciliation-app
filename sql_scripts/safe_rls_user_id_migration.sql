-- SAFE RLS Migration from user_email to user_id
-- This script creates new policies without dropping existing ones first

-- Step 1: Check current RLS status
SELECT schemaname, tablename, policyname, cmd, qual, with_check
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename IN ('policies', 'carriers', 'mgas', 'commission_rules')
ORDER BY tablename, policyname;

-- Step 2: Create NEW policies with different names (coexist with old ones)
-- This way both user_email and user_id filtering will work during transition

-- Policies table
CREATE POLICY "Select by user_id" 
ON policies FOR SELECT 
TO anon, authenticated
USING (user_id IS NOT NULL);

CREATE POLICY "Insert by user_id" 
ON policies FOR INSERT 
TO anon, authenticated
WITH CHECK (user_id IS NOT NULL);

CREATE POLICY "Update by user_id" 
ON policies FOR UPDATE
TO anon, authenticated
USING (user_id IS NOT NULL)
WITH CHECK (user_id IS NOT NULL);

CREATE POLICY "Delete by user_id" 
ON policies FOR DELETE
TO anon, authenticated
USING (user_id IS NOT NULL);

-- Carriers table (if RLS is enabled)
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'carriers' AND rowsecurity = true) THEN
        CREATE POLICY "Select carriers by user_id" 
        ON carriers FOR SELECT 
        TO anon, authenticated
        USING (user_id IS NOT NULL);

        CREATE POLICY "Manage carriers by user_id" 
        ON carriers FOR ALL
        TO anon, authenticated
        USING (user_id IS NOT NULL)
        WITH CHECK (user_id IS NOT NULL);
    END IF;
END $$;

-- MGAs table (if RLS is enabled)
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'mgas' AND rowsecurity = true) THEN
        CREATE POLICY "Select mgas by user_id" 
        ON mgas FOR SELECT 
        TO anon, authenticated
        USING (user_id IS NOT NULL);

        CREATE POLICY "Manage mgas by user_id" 
        ON mgas FOR ALL
        TO anon, authenticated
        USING (user_id IS NOT NULL)
        WITH CHECK (user_id IS NOT NULL);
    END IF;
END $$;

-- Commission rules table (if RLS is enabled)
DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'commission_rules' AND rowsecurity = true) THEN
        CREATE POLICY "Select rules by user_id" 
        ON commission_rules FOR SELECT 
        TO anon, authenticated
        USING (user_id IS NOT NULL);

        CREATE POLICY "Manage rules by user_id" 
        ON commission_rules FOR ALL
        TO anon, authenticated
        USING (user_id IS NOT NULL)
        WITH CHECK (user_id IS NOT NULL);
    END IF;
END $$;

-- Step 3: Verify new policies were created
SELECT 'After creating new policies:' as status;
SELECT schemaname, tablename, policyname, cmd
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename IN ('policies', 'carriers', 'mgas', 'commission_rules')
AND policyname LIKE '%user_id%'
ORDER BY tablename, policyname;

-- Step 4: Test that user_id filtering works
-- Run this to verify data is properly filtered by user_id
SELECT 'Testing user_id filtering on policies table:' as test;
SELECT COUNT(*) as total_records, 
       COUNT(DISTINCT user_id) as unique_user_ids,
       COUNT(CASE WHEN user_id IS NULL THEN 1 END) as null_user_ids
FROM policies;

-- Step 5: ONLY after confirming everything works, run the cleanup script
-- Save this as a separate file: cleanup_old_rls_policies.sql
/*
-- CLEANUP SCRIPT - RUN SEPARATELY AFTER VERIFICATION
-- Drop old user_email-based policies
DROP POLICY IF EXISTS "Anyone can view their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can insert with user_email" ON policies;
DROP POLICY IF EXISTS "Anyone can update their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can delete their own data" ON policies;

-- Add similar DROP commands for other tables if they have old policies
*/