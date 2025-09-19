-- =====================================================
-- SIMPLE CHECK FOR CARRIERS, MGAs, AND COMMISSION RULES
-- No user_email references
-- =====================================================

-- 1. Quick status check - ARE THE TABLES EMPTY?
SELECT 
    'CARRIERS' as table_name,
    CASE 
        WHEN COUNT(*) = 0 THEN '❌ EMPTY - No carriers found!'
        ELSE '✅ Has ' || COUNT(*)::text || ' carriers'
    END as status
FROM carriers
UNION ALL
SELECT 
    'MGAS' as table_name,
    CASE 
        WHEN COUNT(*) = 0 THEN '❌ EMPTY - No MGAs found!'
        ELSE '✅ Has ' || COUNT(*)::text || ' MGAs'
    END as status
FROM mgas
UNION ALL
SELECT 
    'COMMISSION_RULES' as table_name,
    CASE 
        WHEN COUNT(*) = 0 THEN '❌ EMPTY - No commission rules found!'
        ELSE '✅ Has ' || COUNT(*)::text || ' commission rules'
    END as status
FROM commission_rules
UNION ALL
SELECT 
    'CARRIER_MGA_RELATIONSHIPS' as table_name,
    CASE 
        WHEN COUNT(*) = 0 THEN '❌ EMPTY - No relationships found!'
        ELSE '✅ Has ' || COUNT(*)::text || ' relationships'
    END as status
FROM carrier_mga_relationships;

-- 2. Show table structure (what columns exist)
SELECT 
    '=== TABLE STRUCTURES ===' as info;
    
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name IN ('carriers', 'mgas', 'commission_rules')
    AND table_schema = 'public'
ORDER BY table_name, ordinal_position;

-- 3. If carriers table has data, show some
SELECT 
    '=== SAMPLE CARRIERS (if any) ===' as info;
    
SELECT * FROM carriers LIMIT 10;

-- 4. If MGAs table has data, show some
SELECT 
    '=== SAMPLE MGAs (if any) ===' as info;
    
SELECT * FROM mgas LIMIT 10;

-- 5. If commission_rules table has data, show some
SELECT 
    '=== SAMPLE COMMISSION RULES (if any) ===' as info;
    
SELECT * FROM commission_rules LIMIT 10;

-- 6. Check if Row Level Security is enabled
SELECT 
    '=== ROW LEVEL SECURITY STATUS ===' as info;
    
SELECT 
    tablename,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS is ENABLED'
        ELSE '🔓 RLS is DISABLED'
    END as security_status
FROM pg_tables
WHERE tablename IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships')
    AND schemaname = 'public';