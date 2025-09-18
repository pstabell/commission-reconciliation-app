-- EXPORT ALL CARRIERS, MGAS, AND COMMISSION RULES FROM SUPABASE
-- Note: No user_email column exists, so this will export ALL data

-- 1. Export ALL Carriers
SELECT 'ALL CARRIERS:' as section;
SELECT 
    carrier_id,
    carrier_name,
    naic_code,
    producer_code,
    status,
    notes
FROM carriers
ORDER BY carrier_name;

-- 2. Export ALL MGAs
SELECT '';
SELECT 'ALL MGAS:' as section;
SELECT 
    mga_id,
    mga_name,
    status,
    notes
FROM mgas
ORDER BY mga_name;

-- 3. Export ALL Commission Rules with carrier/MGA names
SELECT '';
SELECT 'ALL COMMISSION RULES:' as section;
SELECT 
    cr.rule_id,
    c.carrier_name,
    m.mga_name,
    cr.state,
    cr.policy_type,
    cr.term_months,
    cr.new_rate,
    cr.renewal_rate,
    cr.payment_terms,
    cr.rule_description,
    cr.rule_priority,
    cr.is_default
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.is_active = true
ORDER BY c.carrier_name, m.mga_name, cr.rule_priority;

-- 4. Count summary
SELECT '';
SELECT 'SUMMARY:' as section;
SELECT 
    'Total Carriers: ' || COUNT(*) as count
FROM carriers
UNION ALL
SELECT 
    'Total MGAs: ' || COUNT(*)
FROM mgas
UNION ALL
SELECT 
    'Total Active Commission Rules: ' || COUNT(*)
FROM commission_rules
WHERE is_active = true;