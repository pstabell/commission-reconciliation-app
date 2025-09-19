-- =====================================================
-- CHECK FOR EXISTING COMMISSION RULES
-- =====================================================

-- 1. Count how many commission rules exist
SELECT COUNT(*) as total_commission_rules FROM commission_rules;

-- 2. Show all commission rules with carrier names
SELECT 
    cr.rule_id,
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.state,
    cr.rule_description,
    cr.is_active,
    cr.is_default,
    cr.effective_date,
    cr.created_at
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
ORDER BY c.carrier_name, cr.policy_type;

-- 3. Check if commission_rules table has any user-specific columns
SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'commission_rules'
    AND table_schema = 'public'
ORDER BY ordinal_position;

-- 4. Group rules by carrier to see what you have
SELECT 
    c.carrier_name,
    COUNT(*) as number_of_rules,
    STRING_AGG(DISTINCT cr.policy_type, ', ') as policy_types
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
GROUP BY c.carrier_name
ORDER BY c.carrier_name;

-- 5. Check for any default rules
SELECT 
    c.carrier_name,
    cr.new_rate,
    cr.renewal_rate,
    cr.rule_description
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE cr.is_default = true
ORDER BY c.carrier_name;