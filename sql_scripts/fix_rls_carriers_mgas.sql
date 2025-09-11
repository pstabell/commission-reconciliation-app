-- =====================================================
-- FIX RLS ISSUE - DISABLE RLS ON CARRIERS AND MGAS
-- =====================================================
-- The issue: RLS is enabled but no policies exist, blocking all access

-- 1. Check current RLS status
SELECT 
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE tablename IN ('carriers', 'mgas')
    AND schemaname = 'public';

-- 2. DISABLE RLS on carriers table
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;

-- 3. DISABLE RLS on mgas table  
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;

-- 4. Verify RLS is now disabled
SELECT 
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS ENABLED'
        ELSE '🔓 RLS DISABLED - App can now see data!'
    END as status
FROM pg_tables 
WHERE tablename IN ('carriers', 'mgas')
    AND schemaname = 'public';

-- 5. Test that data is accessible
SELECT 'Testing carriers access:' as test;
SELECT COUNT(*) as carrier_count FROM carriers;

SELECT 'Testing MGAs access:' as test;
SELECT COUNT(*) as mga_count FROM mgas;

-- 6. Success message
SELECT 
    '✅ RLS has been disabled on carriers and mgas tables!' as success,
    'The Streamlit app should now be able to see your carriers and MGAs.' as message;