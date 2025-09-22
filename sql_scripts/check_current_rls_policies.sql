-- Check current RLS policies before cleanup
-- This is a READ-ONLY script to see what's currently in place

-- Show all policies on our main tables
SELECT 
    tablename,
    policyname,
    cmd as operation,
    qual as using_clause,
    with_check as with_check_clause
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename IN ('policies', 'carriers', 'mgas', 'commission_rules')
ORDER BY tablename, policyname;

-- Check if both user_email and user_id policies exist
SELECT 
    tablename,
    COUNT(CASE WHEN policyname LIKE '%user_id%' THEN 1 END) as user_id_policies,
    COUNT(CASE WHEN policyname LIKE '%user_email%' OR policyname LIKE 'Anyone can%' THEN 1 END) as user_email_policies,
    COUNT(*) as total_policies
FROM pg_policies 
WHERE schemaname = 'public' 
AND tablename IN ('policies', 'carriers', 'mgas', 'commission_rules')
GROUP BY tablename
ORDER BY tablename;

-- Check RLS status on tables
SELECT 
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('policies', 'carriers', 'mgas', 'commission_rules')
ORDER BY tablename;