-- Remove ONLY the confirmed old user_email-based policies
-- Keeping the new user_id policies and other necessary policies

-- First, show what we're removing
SELECT 'Removing these old policies:' as action;
SELECT policyname, cmd 
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename = 'policies'
AND policyname IN (
    'Anyone can delete their own data',
    'Anyone can insert with user_email', 
    'Anyone can update their own data',
    'Anyone can view their own data'  -- In case it exists
);

-- Remove the old policies
DROP POLICY IF EXISTS "Anyone can delete their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can insert with user_email" ON policies;
DROP POLICY IF EXISTS "Anyone can update their own data" ON policies;
DROP POLICY IF EXISTS "Anyone can view their own data" ON policies;

-- Verify what remains
SELECT 'Remaining policies after cleanup:' as status;
SELECT 
    policyname,
    cmd as operation,
    CASE 
        WHEN qual LIKE '%user_id%' THEN 'Uses user_id'
        WHEN qual LIKE '%user_email%' THEN 'Uses user_email' 
        ELSE 'Other'
    END as filter_type
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename = 'policies'
ORDER BY policyname;