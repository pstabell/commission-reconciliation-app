-- COPY ALL UNIQUE COMMISSION RULES TO DEMO ACCOUNT

-- First, let's see what we're going to copy
SELECT 'PREVIEW - Unique rules to copy:' as info;
WITH unique_rules AS (
    SELECT DISTINCT ON (c.carrier_name, COALESCE(m.mga_name, 'Direct'), cr.policy_type, cr.state)
        c.carrier_name,
        COALESCE(m.mga_name, 'Direct Appointment') as mga_name,
        cr.state,
        cr.policy_type,
        cr.new_rate,
        cr.renewal_rate,
        cr.payment_terms,
        cr.rule_description,
        cr.is_default
    FROM commission_rules cr
    JOIN carriers c ON cr.carrier_id = c.carrier_id
    LEFT JOIN mgas m ON cr.mga_id = m.mga_id
    WHERE cr.is_active = true
    AND cr.user_email != 'Demo@AgentCommissionTracker.com'
    ORDER BY c.carrier_name, COALESCE(m.mga_name, 'Direct'), cr.policy_type, cr.state, cr.created_at DESC
)
SELECT COUNT(*) as rules_to_add FROM unique_rules;

-- Now insert the missing rules
WITH unique_rules AS (
    SELECT DISTINCT ON (c.carrier_name, COALESCE(m.mga_name, 'Direct'), cr.policy_type, cr.state)
        c.carrier_name,
        COALESCE(m.mga_name, 'Direct Appointment') as mga_name,
        cr.state,
        cr.policy_type,
        cr.new_rate,
        cr.renewal_rate,
        cr.payment_terms,
        cr.rule_description,
        cr.is_default
    FROM commission_rules cr
    JOIN carriers c ON cr.carrier_id = c.carrier_id
    LEFT JOIN mgas m ON cr.mga_id = m.mga_id
    WHERE cr.is_active = true
    AND cr.user_email != 'Demo@AgentCommissionTracker.com'
    ORDER BY c.carrier_name, COALESCE(m.mga_name, 'Direct'), cr.policy_type, cr.state, cr.created_at DESC
)
INSERT INTO commission_rules (
    carrier_id,
    mga_id,
    state,
    policy_type,
    new_rate,
    renewal_rate,
    payment_terms,
    rule_description,
    user_email,
    is_default,
    is_active
)
SELECT 
    dc.carrier_id,
    dm.mga_id,
    ur.state,
    ur.policy_type,
    ur.new_rate,
    ur.renewal_rate,
    ur.payment_terms,
    ur.rule_description,
    'Demo@AgentCommissionTracker.com',
    ur.is_default,
    true
FROM unique_rules ur
JOIN carriers dc ON dc.carrier_name = ur.carrier_name 
    AND dc.user_email = 'Demo@AgentCommissionTracker.com'
LEFT JOIN mgas dm ON dm.mga_name = ur.mga_name 
    AND dm.user_email = 'Demo@AgentCommissionTracker.com'
WHERE NOT EXISTS (
    SELECT 1 
    FROM commission_rules existing
    WHERE existing.carrier_id = dc.carrier_id
    AND COALESCE(existing.mga_id, '00000000-0000-0000-0000-000000000000') = COALESCE(dm.mga_id, '00000000-0000-0000-0000-000000000000')
    AND COALESCE(existing.policy_type, '') = COALESCE(ur.policy_type, '')
    AND existing.user_email = 'Demo@AgentCommissionTracker.com'
);

-- Verify the results
SELECT '';
SELECT 'AFTER COPY - Demo account totals:' as info;
SELECT 
    'Carriers: ' || COUNT(DISTINCT carrier_id) as count
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'MGAs: ' || COUNT(DISTINCT mga_id)
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Commission Rules: ' || COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND is_active = true;