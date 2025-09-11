-- =====================================================
-- TEST WHY APP CAN'T SEE CARRIERS/MGAs
-- =====================================================

-- 1. Verify data exists (we know it does, but let's confirm counts)
SELECT 
    'Carriers in database:' as check_item,
    COUNT(*) as count
FROM carriers
UNION ALL
SELECT 
    'MGAs in database:' as check_item,
    COUNT(*) as count
FROM mgas
UNION ALL
SELECT 
    'Commission rules:' as check_item,
    COUNT(*) as count
FROM commission_rules;

-- 2. Check current user
SELECT 
    'Current user:' as info,
    current_user as username,
    session_user as session_username;

-- 3. Check RLS policies in detail
SELECT 
    tablename,
    policyname,
    permissive,
    roles,
    cmd as operation,
    qual as policy_condition
FROM pg_policies
WHERE tablename IN ('carriers', 'mgas')
ORDER BY tablename, policyname;

-- 4. Test what happens with a simple query (what the app would run)
-- This mimics what the Streamlit app does
SELECT 
    'Testing basic carrier query:' as test;
SELECT carrier_id, carrier_name FROM carriers ORDER BY carrier_name LIMIT 5;

SELECT 
    'Testing basic MGA query:' as test;
SELECT mga_id, mga_name FROM mgas ORDER BY mga_name LIMIT 5;

-- 5. Check if there are any permission issues
SELECT 
    'Table permissions:' as check_type,
    schemaname,
    tablename,
    tableowner,
    has_table_privilege(current_user, schemaname||'.'||tablename, 'SELECT') as can_select,
    has_table_privilege(current_user, schemaname||'.'||tablename, 'INSERT') as can_insert
FROM pg_tables 
WHERE tablename IN ('carriers', 'mgas', 'commission_rules')
    AND schemaname = 'public';

-- 6. The key issue - check if RLS is blocking
WITH rls_check AS (
    SELECT 
        tablename,
        rowsecurity as rls_enabled
    FROM pg_tables 
    WHERE tablename IN ('carriers', 'mgas')
        AND schemaname = 'public'
)
SELECT 
    tablename,
    CASE 
        WHEN rls_enabled THEN '🔒 RLS ENABLED - This might be blocking the app!'
        ELSE '🔓 RLS DISABLED - App should see data'
    END as status
FROM rls_check;

-- 7. Final diagnosis
SELECT 
    '=== DIAGNOSIS ===' as summary,
    CASE 
        WHEN EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'carriers' AND rowsecurity = true)
        THEN 'RLS is enabled on carriers/mgas but there are no policies defined. The app cannot see the data!'
        ELSE 'RLS is not the issue. Check app connection/credentials.'
    END as diagnosis;