-- =====================================================
-- CHECK FOR POLICY-TYPE-SPECIFIC COMMISSION RULES
-- =====================================================

-- 1. Show ALL commission rules (not just defaults)
SELECT 
    c.carrier_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.is_default,
    cr.rule_description
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE cr.is_default = false  -- Only non-default rules
ORDER BY c.carrier_name, cr.policy_type;

-- 2. Count total rules vs default rules
SELECT 
    COUNT(*) as total_rules,
    SUM(CASE WHEN is_default = true THEN 1 ELSE 0 END) as default_rules,
    SUM(CASE WHEN is_default = false THEN 1 ELSE 0 END) as policy_specific_rules
FROM commission_rules;

-- 3. Show carriers with multiple rules (have policy-type-specific rates)
SELECT 
    c.carrier_name,
    COUNT(*) as rule_count,
    STRING_AGG(
        CASE 
            WHEN cr.is_default THEN 'DEFAULT: ' || cr.new_rate || '/' || cr.renewal_rate || '%'
            ELSE cr.policy_type || ': ' || cr.new_rate || '/' || cr.renewal_rate || '%'
        END, 
        ' | ' ORDER BY cr.is_default DESC, cr.policy_type
    ) as all_rules
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
GROUP BY c.carrier_name
HAVING COUNT(*) > 1
ORDER BY c.carrier_name;

-- 4. Show sample rules for carriers that typically have policy-type-specific rates
SELECT 
    c.carrier_name,
    cr.policy_type,
    cr.new_rate || '% / ' || cr.renewal_rate || '%' as rates,
    cr.rule_description
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE c.carrier_name IN ('AAA', 'Progressive', 'Mercury', 'CNA')
ORDER BY c.carrier_name, cr.policy_type;