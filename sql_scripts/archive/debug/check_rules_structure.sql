-- =====================================================
-- CHECK COMMISSION RULES TABLE STRUCTURE
-- =====================================================

-- 1. Show all columns in commission_rules table
SELECT 
    'Commission Rules Table Columns:' as info;
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'commission_rules'
    AND table_schema = 'public'
ORDER BY ordinal_position;

-- 2. Count all commission rules
SELECT 
    'Total commission rules:' as info,
    COUNT(*) as count
FROM commission_rules;

-- 3. Show sample rules
SELECT 
    'Sample commission rules (first 5):' as info;
SELECT * FROM commission_rules LIMIT 5;

-- 4. Check RLS status
SELECT 
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables 
WHERE tablename = 'commission_rules'
    AND schemaname = 'public';

-- 5. The issue
SELECT 
    '⚠️ ISSUE FOUND' as status,
    'The app is trying to filter by user_email but the column does not exist!' as problem,
    'This is why you cannot see your commission rules.' as reason;