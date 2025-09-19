-- =====================================================
-- CHECK CARRIERS, MGAs, AND COMMISSION RULES IN SUPABASE
-- Modified version - no user_email in carriers/mgas
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
    notes,
    created_at
FROM carriers
ORDER BY carrier_name
LIMIT 50;

-- 4. Show all MGAs
SELECT 
    mga_id,
    mga_name,
    status,
    notes,
    created_at
FROM mgas
ORDER BY mga_name;

-- 5. Show commission rules (with carrier names)
-- Check if commission_rules has user_email
SELECT 
    cr.rule_id,
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.rule_description,
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'commission_rules' 
            AND column_name = 'user_email'
        ) 
        THEN cr.user_email 
        ELSE 'N/A' 
    END as user_email,
    cr.created_at
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
ORDER BY c.carrier_name, cr.policy_type
LIMIT 50;

-- 6. Check which tables have user_email columns
SELECT 
    table_name,
    'YES' as has_user_email
FROM information_schema.columns
WHERE table_name IN ('carriers', 'mgas', 'commission_rules', 'policies')
    AND column_name = 'user_email'
GROUP BY table_name;

-- 7. Show sample carriers to see if data exists
SELECT 
    'Sample Carriers:' as info;
SELECT * FROM carriers LIMIT 10;

-- 8. Show sample MGAs to see if data exists
SELECT 
    'Sample MGAs:' as info;
SELECT * FROM mgas LIMIT 10;

-- 9. Check Row Level Security (RLS) policies
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

-- 10. Check if RLS is enabled on these tables
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE tablename IN ('carriers', 'mgas', 'commission_rules', 'carrier_mga_relationships');

-- 11. Show sample of carrier-MGA relationships
SELECT 
    c.carrier_name,
    m.mga_name,
    cmr.created_at
FROM carrier_mga_relationships cmr
JOIN carriers c ON cmr.carrier_id = c.carrier_id
JOIN mgas m ON cmr.mga_id = m.mga_id
ORDER BY c.carrier_name, m.mga_name
LIMIT 20;

-- 12. Quick check - Are the tables completely empty?
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM carriers) = 0 THEN 'EMPTY - No carriers found!'
        ELSE 'Has ' || (SELECT COUNT(*) FROM carriers)::text || ' carriers'
    END as carriers_status,
    CASE 
        WHEN (SELECT COUNT(*) FROM mgas) = 0 THEN 'EMPTY - No MGAs found!'
        ELSE 'Has ' || (SELECT COUNT(*) FROM mgas)::text || ' MGAs'
    END as mgas_status,
    CASE 
        WHEN (SELECT COUNT(*) FROM commission_rules) = 0 THEN 'EMPTY - No commission rules found!'
        ELSE 'Has ' || (SELECT COUNT(*) FROM commission_rules)::text || ' commission rules'
    END as rules_status;