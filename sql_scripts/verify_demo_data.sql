-- VERIFY DEMO ACCOUNT DATA

-- 1. Count all demo data
SELECT 'DEMO ACCOUNT SUMMARY:' as info;
SELECT 
    'Total Carriers: ' || COUNT(*) as count
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Total MGAs: ' || COUNT(*)
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Total Commission Rules: ' || COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Show some carriers
SELECT '';
SELECT 'SAMPLE CARRIERS (first 10):' as info;
SELECT carrier_name, status, naic_code
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 10;

-- 3. Show some MGAs
SELECT '';
SELECT 'SAMPLE MGAS:' as info;
SELECT mga_name, status
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY mga_name;

-- 4. Show commission rules with carrier names
SELECT '';
SELECT 'SAMPLE COMMISSION RULES (first 10):' as info;
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
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY c.carrier_name, m.mga_name
LIMIT 10;