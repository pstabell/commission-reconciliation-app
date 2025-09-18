-- ADD MISSING COMMISSION RULES FOR DEMO CARRIERS

-- 1. Check which carriers don't have ANY rules
SELECT 'CARRIERS WITHOUT ANY COMMISSION RULES:' as info;
SELECT c.carrier_name
FROM carriers c
WHERE c.user_email = 'Demo@AgentCommissionTracker.com'
AND NOT EXISTS (
    SELECT 1 
    FROM commission_rules cr 
    WHERE cr.carrier_id = c.carrier_id 
    AND cr.user_email = 'Demo@AgentCommissionTracker.com'
    AND cr.is_active = true
)
ORDER BY c.carrier_name;

-- 2. Count how many carriers are missing rules
SELECT '';
SELECT 'MISSING RULES COUNT:' as info;
SELECT COUNT(*) as carriers_without_rules
FROM carriers c
WHERE c.user_email = 'Demo@AgentCommissionTracker.com'
AND NOT EXISTS (
    SELECT 1 
    FROM commission_rules cr 
    WHERE cr.carrier_id = c.carrier_id 
    AND cr.user_email = 'Demo@AgentCommissionTracker.com'
    AND cr.is_active = true
);

-- 3. Add default commission rules for carriers that don't have any
INSERT INTO commission_rules (
    carrier_id,
    mga_id,
    state,
    policy_type,
    new_rate,
    renewal_rate,
    rule_description,
    user_email,
    is_default,
    is_active
)
SELECT 
    c.carrier_id,
    (SELECT mga_id FROM mgas WHERE mga_name = 'Direct Appointment' AND user_email = 'Demo@AgentCommissionTracker.com'),
    'FL',
    NULL,
    12.0,  -- Default 12% new business
    10.0,  -- Default 10% renewal
    c.carrier_name || ' standard rate',
    'Demo@AgentCommissionTracker.com',
    true,
    true
FROM carriers c
WHERE c.user_email = 'Demo@AgentCommissionTracker.com'
AND NOT EXISTS (
    SELECT 1 
    FROM commission_rules cr 
    WHERE cr.carrier_id = c.carrier_id 
    AND cr.user_email = 'Demo@AgentCommissionTracker.com'
    AND cr.is_active = true
);

-- 4. Verify the new total
SELECT '';
SELECT 'AFTER ADDING DEFAULT RULES:' as info;
SELECT 
    'Total Commission Rules: ' || COUNT(*) as count
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND is_active = true;

-- 5. Show sample of newly added rules
SELECT '';
SELECT 'SAMPLE NEW RULES ADDED:' as info;
SELECT 
    c.carrier_name,
    m.mga_name,
    cr.new_rate,
    cr.renewal_rate,
    cr.rule_description
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
AND cr.is_default = true
AND cr.rule_description LIKE '% standard rate'
ORDER BY c.carrier_name
LIMIT 10;