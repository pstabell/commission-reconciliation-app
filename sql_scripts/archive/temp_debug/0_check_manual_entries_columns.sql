-- Check columns in manual_commission_entries table
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_name = 'manual_commission_entries'
    AND table_schema = 'public'
ORDER BY 
    ordinal_position;

-- Check if table exists
SELECT 
    COUNT(*) as table_exists
FROM 
    information_schema.tables
WHERE 
    table_name = 'manual_commission_entries'
    AND table_schema = 'public';

-- Get a sample of actual data (column names will be shown)
SELECT * FROM manual_commission_entries LIMIT 1;