-- =====================================================
-- Enable RLS on reconciliations table after migration
-- Run this AFTER running the reconciliation migration
-- =====================================================

-- Check if reconciliations table exists and has RLS
SELECT 
    tablename,
    rowsecurity as "RLS Enabled",
    CASE 
        WHEN rowsecurity THEN '✅ Already Protected'
        ELSE '❌ Needs RLS Enabled'
    END as "Status"
FROM 
    pg_tables
WHERE 
    schemaname = 'public'
    AND tablename = 'reconciliations';

-- If the table shows "Needs RLS Enabled", run this:
ALTER TABLE reconciliations ENABLE ROW LEVEL SECURITY;

-- Verify RLS is now enabled
SELECT 
    tablename,
    rowsecurity as "RLS Enabled"
FROM 
    pg_tables
WHERE 
    schemaname = 'public'
    AND tablename = 'reconciliations';