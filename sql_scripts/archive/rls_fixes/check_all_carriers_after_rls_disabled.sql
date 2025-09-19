-- CHECK ALL CARRIERS AND MGAS AFTER RLS WAS DISABLED

-- 1. Current RLS status
SELECT 'RLS Status After Fix:' as check;
SELECT 
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS Still ON!' 
        ELSE '✅ RLS OFF - All data visible' 
    END as status
FROM pg_tables 
WHERE tablename IN ('carriers', 'mgas', 'commission_rules')
ORDER BY tablename;

-- 2. Count ALL carriers (including any with user_email)
SELECT 'All Carriers Breakdown:' as check;
SELECT 
    COUNT(*) as total_carriers,
    COUNT(CASE WHEN user_email IS NULL THEN 1 END) as global_carriers,
    COUNT(CASE WHEN user_email IS NOT NULL THEN 1 END) as user_specific_carriers
FROM carriers;

-- 3. Show carriers by user_email
SELECT 'Carriers by User:' as check;
SELECT 
    COALESCE(user_email, 'GLOBAL/SHARED') as owner,
    COUNT(*) as carrier_count,
    STRING_AGG(carrier_name, ', ' ORDER BY carrier_name) as carrier_names
FROM carriers
GROUP BY user_email
ORDER BY user_email;

-- 4. Same for MGAs
SELECT 'All MGAs Breakdown:' as check;
SELECT 
    COUNT(*) as total_mgas,
    COUNT(CASE WHEN user_email IS NULL THEN 1 END) as global_mgas,
    COUNT(CASE WHEN user_email IS NOT NULL THEN 1 END) as user_specific_mgas
FROM mgas;

-- 5. Show MGAs by user
SELECT 'MGAs by User:' as check;
SELECT 
    COALESCE(user_email, 'GLOBAL/SHARED') as owner,
    COUNT(*) as mga_count,
    STRING_AGG(mga_name, ', ' ORDER BY mga_name) as mga_names
FROM mgas
GROUP BY user_email
ORDER BY user_email;

-- 6. Check if there are carriers/mgas with different created dates
SELECT 'Carriers by Creation Date:' as check;
SELECT 
    DATE(created_at) as created_date,
    COUNT(*) as count,
    STRING_AGG(carrier_name, ', ' ORDER BY carrier_name) as carriers
FROM carriers
GROUP BY DATE(created_at)
ORDER BY created_date;

-- 7. If RLS is still on, we need to disable it
-- Uncomment and run if status shows RLS is still enabled
/*
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;
*/