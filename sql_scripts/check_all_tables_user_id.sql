-- Check if user_id columns exist and are populated in all tables

-- 1. Show which tables have user_id column
SELECT 
    'Table Structure Check' as check_type,
    table_name,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = t.table_name 
            AND column_name = 'user_id'
        ) THEN 'YES'
        ELSE 'NO'
    END as has_user_id_column
FROM (
    SELECT 'policies' as table_name
    UNION ALL SELECT 'carriers'
    UNION ALL SELECT 'mgas'
    UNION ALL SELECT 'commission_rules'
    UNION ALL SELECT 'reconciliations'
    UNION ALL SELECT 'carrier_mga_relationships'
) t
ORDER BY table_name;

-- 2. Check if data is populated
SELECT 
    'Data Population Check' as check_type,
    'policies' as table_name,
    COUNT(*) as total_rows,
    COUNT(user_id) as rows_with_user_id,
    COUNT(*) - COUNT(user_id) as missing_user_id
FROM policies
UNION ALL
SELECT 
    'Data Population Check',
    'carriers',
    COUNT(*),
    COUNT(user_id),
    COUNT(*) - COUNT(user_id)
FROM carriers
UNION ALL
SELECT 
    'Data Population Check',
    'mgas',
    COUNT(*),
    COUNT(user_id),
    COUNT(*) - COUNT(user_id)
FROM mgas
UNION ALL
SELECT 
    'Data Population Check',
    'commission_rules',
    COUNT(*),
    COUNT(user_id),
    COUNT(*) - COUNT(user_id)
FROM commission_rules;