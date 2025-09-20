-- Check columns in deleted_policies table
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_name = 'deleted_policies'
    AND table_schema = 'public'
ORDER BY 
    ordinal_position;

-- Get a sample of actual data (column names will be shown)
SELECT * FROM deleted_policies LIMIT 1;