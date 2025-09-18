-- VERIFY DEMO IMPORT DETAILS

-- 1. List all carriers
SELECT 'DEMO CARRIERS:' as section;
SELECT carrier_name, status
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name;

-- 2. List all MGAs
SELECT '';
SELECT 'DEMO MGAS:' as section;
SELECT mga_name, status
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY mga_name;

-- 3. List all commission rules with details
SELECT '';
SELECT 'DEMO COMMISSION RULES:' as section;
SELECT 
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.rule_description
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY c.carrier_name, m.mga_name;