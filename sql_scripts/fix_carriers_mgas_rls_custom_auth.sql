-- FIX CARRIERS/MGAS FOR CUSTOM AUTH (NOT SUPABASE AUTH)
-- The app uses custom auth, so auth.email() is always NULL
-- This makes RLS policies fail

-- 1. Check current situation
SELECT 'Current Status:' as info;
SELECT 
    'Carriers without user_email:' as item, 
    COUNT(*) as count 
FROM carriers 
WHERE user_email IS NULL;

SELECT 
    'MGAs without user_email:' as item, 
    COUNT(*) as count 
FROM mgas 
WHERE user_email IS NULL;

-- 2. OPTION A: Disable RLS (Simplest - carriers/MGAs are shared reference data)
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;

-- 3. Verify you can now see the data
SELECT 'After disabling RLS:' as info;
SELECT 'Carriers visible:' as item, COUNT(*) as count FROM carriers;
SELECT 'MGAs visible:' as item, COUNT(*) as count FROM mgas;

-- 4. Show the carriers that were hidden
SELECT 'Restored Carriers:' as info;
SELECT carrier_name, status FROM carriers ORDER BY carrier_name;

-- 5. Show the MGAs that were hidden
SELECT 'Restored MGAs:' as info;
SELECT mga_name, status FROM mgas ORDER BY mga_name;

-- ALTERNATIVE OPTION B: Update carriers/MGAs to be "global" (NULL user_email)
-- This would work with the RLS policy "user_email IS NULL OR user_email = auth.email()"
/*
UPDATE carriers SET user_email = NULL WHERE user_email IS NOT NULL;
UPDATE mgas SET user_email = NULL WHERE user_email IS NOT NULL;
*/

-- NOTE: Since your app uses custom auth, not Supabase Auth:
-- - auth.email() is always NULL
-- - RLS policies checking auth.email() will always fail
-- - This is why disabling RLS is the correct solution for shared reference tables