-- Check if user_id migration has been completed

-- 1. Check if user_id columns exist
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name IN ('policies', 'carriers', 'mgas', 'commission_rules', 'reconciliations', 'carrier_mga_relationships')
AND column_name = 'user_id'
ORDER BY table_name;

-- 2. Check if user_id values are populated
SELECT 
    'policies' as table_name,
    COUNT(*) as total_records,
    COUNT(user_id) as records_with_user_id,
    COUNT(*) - COUNT(user_id) as missing_user_id
FROM policies
WHERE user_email IS NOT NULL
UNION ALL
SELECT 
    'carriers',
    COUNT(*),
    COUNT(user_id),
    COUNT(*) - COUNT(user_id)
FROM carriers
WHERE user_email IS NOT NULL;

-- 3. Check demo user specifically
SELECT * FROM users WHERE email = 'demo@agentcommissiontracker.com';