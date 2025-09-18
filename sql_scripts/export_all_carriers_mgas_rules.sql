-- SAFE EXPORT OF ALL CARRIERS, MGAS, AND COMMISSION RULES FROM SUPABASE
-- This script only READS data, it doesn't modify anything

-- 1. Export ALL Carriers (for all users)
SELECT 'ALL CARRIERS:' as section;
SELECT 
    carrier_id,
    carrier_name,
    naic_code,
    producer_code,
    status,
    notes,
    user_email
FROM carriers
ORDER BY user_email, carrier_name;

-- 2. Export ALL MGAs (for all users)
SELECT '';
SELECT 'ALL MGAS:' as section;
SELECT 
    mga_id,
    mga_name,
    status,
    notes,
    user_email
FROM mgas
ORDER BY user_email, mga_name;

-- 3. Export ALL Commission Rules (for all users)
SELECT '';
SELECT 'ALL COMMISSION RULES:' as section;
SELECT 
    cr.rule_id,
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.payment_terms,
    cr.rule_description,
    cr.user_email
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
ORDER BY cr.user_email, c.carrier_name, m.mga_name;

-- 4. Summary counts by user
SELECT '';
SELECT 'SUMMARY BY USER:' as section;
SELECT 
    user_email,
    'Carriers: ' || COUNT(DISTINCT carrier_id) || 
    ', MGAs: ' || (SELECT COUNT(*) FROM mgas WHERE mgas.user_email = carriers.user_email) ||
    ', Rules: ' || (SELECT COUNT(*) FROM commission_rules WHERE commission_rules.user_email = carriers.user_email) as counts
FROM carriers
GROUP BY user_email
ORDER BY user_email;