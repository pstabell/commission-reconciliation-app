-- =====================================================
-- SIMPLE CHECK - ARE YOUR RULES STILL THERE?
-- =====================================================

-- 1. Count your rules
SELECT COUNT(*) as total_commission_rules FROM commission_rules;

-- 2. Show first 10 rules with carrier names
SELECT 
    cr.rule_id,
    c.carrier_name,
    cr.policy_type,
    cr.new_rate || '% / ' || cr.renewal_rate || '%' as rates,
    cr.is_default
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
ORDER BY c.carrier_name, cr.policy_type
LIMIT 10;

-- 3. Check if commission_rules table has RLS enabled
SELECT 
    'Commission Rules RLS:' as check,
    CASE 
        WHEN rowsecurity THEN '🔒 RLS ENABLED - This might block access!'
        ELSE '🔓 RLS DISABLED - Should be accessible'
    END as status
FROM pg_tables 
WHERE tablename = 'commission_rules';

-- 4. Quick diagnosis
SELECT 
    '📊 Your ' || COUNT(*) || ' commission rules are still in the database' as status
FROM commission_rules;