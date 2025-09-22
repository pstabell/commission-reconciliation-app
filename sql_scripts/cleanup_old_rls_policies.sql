-- CLEANUP SCRIPT - RUN ONLY AFTER VERIFYING NEW POLICIES WORK
-- This removes old user_email-based RLS policies

-- Step 1: Show what we're about to drop
SELECT 'Policies to be dropped:' as status;
SELECT schemaname, tablename, policyname, cmd
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename IN ('policies', 'carriers', 'mgas', 'commission_rules')
AND (policyname LIKE '%user_email%' OR policyname LIKE 'Anyone can%')
ORDER BY tablename, policyname;

-- Step 2: Drop old user_email-based policies
DROP POLICY IF EXISTS "Anyone can view their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can insert with user_email" ON policies;
DROP POLICY IF EXISTS "Anyone can update their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can delete their own data" ON policies;

DROP POLICY IF EXISTS "Users can view their own carriers" ON carriers;
DROP POLICY IF EXISTS "Users can manage their own carriers" ON carriers;

DROP POLICY IF EXISTS "Users can view their own MGAs" ON mgas;
DROP POLICY IF EXISTS "Users can manage their own MGAs" ON mgas;

DROP POLICY IF EXISTS "Users can view their own rules" ON commission_rules;
DROP POLICY IF EXISTS "Users can manage their own rules" ON commission_rules;

-- Step 3: Verify only user_id policies remain
SELECT 'Remaining policies after cleanup:' as status;
SELECT schemaname, tablename, policyname, cmd
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename IN ('policies', 'carriers', 'mgas', 'commission_rules')
ORDER BY tablename, policyname;