-- Remove ALL user_email-based policies now that user_id policies are confirmed working
-- This completes the migration from user_email to user_id

-- Show what we're removing
SELECT 'Removing these user_email-based policies:' as action;
SELECT policyname, cmd, qual
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename = 'policies'
AND policyname IN (
    'Users see only their own data',      -- SELECT using user_email
    'Anyone can insert with user_email',  -- INSERT  
    'Anyone can update their own data',   -- UPDATE
    'Anyone can delete their own data',   -- DELETE
    'Anyone can view their own data'      -- Just in case
);

-- Remove all old user_email-based policies
DROP POLICY IF EXISTS "Users see only their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can insert with user_email" ON policies;
DROP POLICY IF EXISTS "Anyone can update their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can delete their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can view their own data" ON policies;

-- Verify final state - should only have user_id policies and service role policy
SELECT 'Final RLS configuration:' as status;
SELECT 
    policyname,
    cmd as operation,
    roles,
    CASE 
        WHEN qual LIKE '%user_id%' THEN '✓ Uses user_id'
        WHEN policyname LIKE '%service%' OR policyname LIKE '%Service%' THEN '✓ Service role'
        ELSE 'CHECK THIS: ' || COALESCE(qual, 'no filter')
    END as policy_type
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename = 'policies'
ORDER BY 
    CASE cmd 
        WHEN 'SELECT' THEN 1 
        WHEN 'INSERT' THEN 2 
        WHEN 'UPDATE' THEN 3 
        WHEN 'DELETE' THEN 4 
        ELSE 5 
    END,
    policyname;