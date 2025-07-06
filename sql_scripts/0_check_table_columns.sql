-- =====================================================
-- Check Table Structure Before Enabling RLS
-- Run this FIRST to verify your table columns
-- =====================================================

-- Check columns in policies table
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_name = 'policies'
    AND table_schema = 'public'
ORDER BY 
    ordinal_position;

-- Check if transaction_id column exists specifically
SELECT 
    COUNT(*) as transaction_id_exists
FROM 
    information_schema.columns
WHERE 
    table_name = 'policies'
    AND table_schema = 'public'
    AND column_name = 'transaction_id';

-- Get a sample of actual data (column names will be shown)
SELECT * FROM policies LIMIT 1;