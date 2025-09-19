-- CHECK JOHNSON AND JOHNSON IN DEMO/PRODUCTION
-- Run this in PRODUCTION database

-- 1. Check if Johnson and Johnson MGA exists for demo
SELECT 'JOHNSON AND JOHNSON FOR DEMO:' as info;
SELECT mga_id, mga_name, user_email
FROM mgas
WHERE mga_name = 'Johnson and Johnson'
AND user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Check commission rules for Johnson and Johnson
SELECT '';
SELECT 'J&J COMMISSION RULES FOR DEMO:' as info;
SELECT 
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.user_email
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE m.mga_name = 'Johnson and Johnson'
AND cr.user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY c.carrier_name;

-- 3. Check if all 5 carriers exist for demo
SELECT '';
SELECT 'J&J CARRIERS FOR DEMO:' as info;
SELECT carrier_name, 
       EXISTS(
           SELECT 1 FROM commission_rules cr2
           JOIN mgas m ON cr2.mga_id = m.mga_id
           WHERE cr2.carrier_id = carriers.carrier_id
           AND m.mga_name = 'Johnson and Johnson'
       ) as has_jj_rules
FROM carriers
WHERE carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
AND user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name;

-- 4. Let's manually add the missing associations
-- Uncomment and run if needed:
/*
-- First get the MGA ID for Johnson and Johnson
WITH jj_mga AS (
    SELECT mga_id 
    FROM mgas 
    WHERE mga_name = 'Johnson and Johnson' 
    AND user_email = 'Demo@AgentCommissionTracker.com'
),
carrier_ids AS (
    SELECT carrier_id, carrier_name
    FROM carriers
    WHERE carrier_name IN ('Voyager', 'Great Lakes', 'Mount Vernon', 'Evanston')
    AND user_email = 'Demo@AgentCommissionTracker.com'
)
INSERT INTO commission_rules (rule_id, carrier_id, mga_id, policy_type, new_rate, is_active, user_email)
SELECT 
    gen_random_uuid(),
    c.carrier_id,
    j.mga_id,
    'All',
    15.0,
    true,
    'Demo@AgentCommissionTracker.com'
FROM carrier_ids c
CROSS JOIN jj_mga j
WHERE NOT EXISTS (
    SELECT 1 FROM commission_rules cr
    WHERE cr.carrier_id = c.carrier_id
    AND cr.mga_id = j.mga_id
    AND cr.user_email = 'Demo@AgentCommissionTracker.com'
);
*/