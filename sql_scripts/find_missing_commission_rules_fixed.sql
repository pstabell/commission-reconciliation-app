-- FIND MISSING COMMISSION RULES (FIXED)

-- 1. Count total rules by user
SELECT 'COMMISSION RULES BY USER:' as info;
SELECT 
    COALESCE(user_email, 'NULL') as user_email,
    COUNT(*) as rule_count
FROM commission_rules
WHERE is_active = true
GROUP BY user_email
ORDER BY rule_count DESC;

-- 2. Show all unique carrier/MGA combinations that have rules
SELECT '';
SELECT 'ALL UNIQUE CARRIER/MGA COMBINATIONS WITH RULES:' as info;
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct Appointment') as mga_name,
    COUNT(*) as rule_count
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.is_active = true
GROUP BY c.carrier_name, COALESCE(m.mga_name, 'Direct Appointment')
ORDER BY c.carrier_name, COALESCE(m.mga_name, 'Direct Appointment');

-- 3. Show sample rules not assigned to any user
SELECT '';
SELECT 'SAMPLE RULES WITHOUT USER (first 20):' as info;
SELECT 
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.rule_description
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email IS NULL
AND cr.is_active = true
ORDER BY c.carrier_name, m.mga_name
LIMIT 20;

-- 4. Count rules without user_email
SELECT '';
SELECT 'TOTAL RULES WITHOUT USER:' as info;
SELECT COUNT(*) as count
FROM commission_rules
WHERE user_email IS NULL
AND is_active = true;