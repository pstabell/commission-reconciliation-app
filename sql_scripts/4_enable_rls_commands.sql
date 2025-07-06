-- =====================================================
-- ENABLE RLS ON EACH TABLE
-- Run these commands ONE AT A TIME and test after each
-- =====================================================

-- 1. Enable RLS on policies table
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;

-- Test immediately after enabling:
-- SELECT COUNT(*) FROM policies;
-- If this fails, immediately run: ALTER TABLE policies DISABLE ROW LEVEL SECURITY;

-- =====================================================

-- 2. Enable RLS on deleted_policies table (after policies works)
ALTER TABLE deleted_policies ENABLE ROW LEVEL SECURITY;

-- Test immediately after enabling:
-- SELECT COUNT(*) FROM deleted_policies;
-- If this fails, immediately run: ALTER TABLE deleted_policies DISABLE ROW LEVEL SECURITY;

-- =====================================================

-- 3. Enable RLS on manual_commission_entries table (after the others work)
ALTER TABLE manual_commission_entries ENABLE ROW LEVEL SECURITY;

-- Test immediately after enabling:
-- SELECT COUNT(*) FROM manual_commission_entries;
-- If this fails, immediately run: ALTER TABLE manual_commission_entries DISABLE ROW LEVEL SECURITY;

-- =====================================================
-- VERIFY ALL TABLES HAVE RLS ENABLED
-- =====================================================

SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM 
    pg_tables
WHERE 
    schemaname = 'public'
    AND tablename IN ('policies', 'deleted_policies', 'manual_commission_entries')
ORDER BY 
    tablename;