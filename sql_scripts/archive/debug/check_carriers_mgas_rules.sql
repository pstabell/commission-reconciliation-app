-- =====================================================
-- CHECK CARRIERS, MGAs, AND COMMISSION RULES IN SUPABASE
-- =====================================================

-- 1. Check if tables exist and their structure
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships')
ORDER BY table_name, ordinal_position;

-- 2. Count records in each table
SELECT 
    'carriers' as table_name, 
    COUNT(*) as record_count 
FROM carriers
UNION ALL
SELECT 
    'mgas' as table_name, 
    COUNT(*) as record_count 
FROM mgas
UNION ALL
SELECT 
    'commission_rules' as table_name, 
    COUNT(*) as record_count 
FROM commission_rules
UNION ALL
SELECT 
    'carrier_mga_relationships' as table_name, 
    COUNT(*) as record_count 
FROM carrier_mga_relationships;

-- 3. Show all carriers (first 50)
SELECT 
    carrier_id,
    carrier_name,
    status,
    created_at,
    user_email
FROM carriers
ORDER BY carrier_name
LIMIT 50;

-- 4. Show all MGAs
SELECT 
    mga_id,
    mga_name,
    status,
    created_at,
    user_email
FROM mgas
ORDER BY mga_name;

-- 5. Show commission rules (with carrier names)
SELECT 
    cr.rule_id,
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.rule_description,
    cr.user_email,
    cr.created_at
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
ORDER BY c.carrier_name, cr.policy_type
LIMIT 50;

-- 6. Check if user_email columns exist
SELECT 
    table_name,
    column_name
FROM information_schema.columns
WHERE table_name IN ('carriers', 'mgas', 'commission_rules')
    AND column_name = 'user_email';

-- 7. If you're logged in as a specific user, check YOUR data
-- Replace 'your-email@example.com' with your actual email
SELECT 
    'Your carriers' as data_type,
    COUNT(*) as count
FROM carriers
WHERE user_email = 'your-email@example.com'
UNION ALL
SELECT 
    'Your MGAs' as data_type,
    COUNT(*) as count
FROM mgas
WHERE user_email = 'your-email@example.com'
UNION ALL
SELECT 
    'Your commission rules' as data_type,
    COUNT(*) as count
FROM commission_rules
WHERE user_email = 'your-email@example.com';

-- 8. Check Row Level Security (RLS) policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships')
ORDER BY tablename, policyname;

-- 9. Check if RLS is enabled on these tables
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE tablename IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships');

-- 10. Show sample of carrier-MGA relationships
SELECT 
    c.carrier_name,
    m.mga_name,
    cmr.created_at
FROM carrier_mga_relationships cmr
JOIN carriers c ON cmr.carrier_id = c.carrier_id
JOIN mgas m ON cmr.mga_id = m.mga_id
ORDER BY c.carrier_name, m.mga_name
LIMIT 20;