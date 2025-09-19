-- ANALYZE ALL COMMISSION RULES IN THE DATABASE

-- 1. Total active rules in the entire database
SELECT 'TOTAL ACTIVE COMMISSION RULES:' as info;
SELECT COUNT(*) as total_active_rules
FROM commission_rules
WHERE is_active = true;

-- 2. Distribution by user
SELECT '';
SELECT 'RULES BY USER EMAIL:' as info;
SELECT 
    user_email,
    COUNT(*) as rule_count
FROM commission_rules
WHERE is_active = true
GROUP BY user_email
ORDER BY rule_count DESC;

-- 3. Show all rules (not just demo) - first 30
SELECT '';
SELECT 'SAMPLE OF ALL COMMISSION RULES (first 30):' as info;
SELECT 
    cr.user_email,
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.rule_description
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.is_active = true
ORDER BY cr.user_email, c.carrier_name
LIMIT 30;

-- 4. Count unique carrier/MGA combinations across all users
SELECT '';
SELECT 'UNIQUE CARRIER/MGA COMBINATIONS:' as info;
SELECT COUNT(DISTINCT CONCAT(c.carrier_name, '-', COALESCE(m.mga_name, 'Direct'))) as unique_combinations
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.is_active = true;