-- =====================================================
-- DIAGNOSE AND FIX MISSING CARRIERS AND MGAS
-- Run this in Supabase SQL Editor
-- =====================================================

-- 1. CHECK IF TABLES EXIST
SELECT 
    'Tables Check' as check_type,
    tablename,
    CASE WHEN tablename IS NOT NULL THEN '✅ Exists' ELSE '❌ Missing' END as status
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('carriers', 'mgas', 'carrier_mga_relationships', 'commission_rules')
ORDER BY tablename;

-- 2. CHECK ROW LEVEL SECURITY STATUS
SELECT 
    'RLS Check' as check_type,
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS Enabled (BLOCKING!)' 
        ELSE '🔓 RLS Disabled (Good)' 
    END as status
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('carriers', 'mgas', 'carrier_mga_relationships', 'commission_rules')
ORDER BY tablename;

-- 3. CHECK DATA COUNTS
SELECT 'Data Count Check' as check_type;
SELECT 'carriers' as table_name, COUNT(*) as row_count FROM carriers
UNION ALL
SELECT 'mgas' as table_name, COUNT(*) as row_count FROM mgas
UNION ALL
SELECT 'carrier_mga_relationships' as table_name, COUNT(*) as row_count FROM carrier_mga_relationships
UNION ALL
SELECT 'commission_rules' as table_name, COUNT(*) as row_count FROM commission_rules
ORDER BY table_name;

-- 4. FIX: DISABLE RLS ON ALL COMMISSION TABLES
ALTER TABLE carriers DISABLE ROW LEVEL SECURITY;
ALTER TABLE mgas DISABLE ROW LEVEL SECURITY;
ALTER TABLE carrier_mga_relationships DISABLE ROW LEVEL SECURITY;
ALTER TABLE commission_rules DISABLE ROW LEVEL SECURITY;

-- 5. VERIFY FIX
SELECT 
    'After Fix' as check_type,
    tablename,
    rowsecurity as rls_enabled,
    CASE 
        WHEN rowsecurity THEN '❌ Still has RLS!' 
        ELSE '✅ Fixed - No RLS' 
    END as status
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('carriers', 'mgas', 'carrier_mga_relationships', 'commission_rules')
ORDER BY tablename;

-- 6. IF TABLES ARE EMPTY, INSERT ESSENTIAL CARRIERS
-- Only run this section if carrier count is 0
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM carriers) = 0 THEN
        INSERT INTO carriers (carrier_name, status, notes) VALUES
        ('Citizens', 'Active', 'Citizens Property Insurance Corporation'),
        ('Progressive', 'Active', 'Auto insurance specialist'),
        ('AAA', 'Active', 'Multi-line carrier'),
        ('State Farm', 'Active', 'Multi-line carrier'),
        ('Tower Hill', 'Active', 'Florida property specialist')
        ON CONFLICT (carrier_name) DO NOTHING;
        
        RAISE NOTICE 'Inserted % carriers', (SELECT COUNT(*) FROM carriers);
    ELSE
        RAISE NOTICE 'Carriers already exist: %', (SELECT COUNT(*) FROM carriers);
    END IF;
END $$;

-- 7. FINAL CHECK
SELECT 
    'Final Status' as info,
    (SELECT COUNT(*) FROM carriers) as carriers_count,
    (SELECT COUNT(*) FROM mgas) as mgas_count,
    (SELECT COUNT(*) FROM commission_rules) as rules_count,
    CASE 
        WHEN (SELECT COUNT(*) FROM carriers) > 0 THEN '✅ Carriers Available!'
        ELSE '❌ Still No Carriers - Manual Insert Needed'
    END as status;