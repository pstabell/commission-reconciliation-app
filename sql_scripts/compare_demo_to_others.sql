-- COMPARE DEMO RULES TO OTHER USERS

-- 1. Show commission rules count by user
SELECT 'COMMISSION RULES BY USER:' as info;
SELECT 
    user_email,
    COUNT(*) as total_rules,
    COUNT(DISTINCT carrier_id) as unique_carriers,
    COUNT(DISTINCT CONCAT(carrier_id, '-', COALESCE(mga_id::text, 'direct'))) as unique_combinations
FROM commission_rules
WHERE is_active = true
GROUP BY user_email
ORDER BY total_rules DESC;

-- 2. Show what rules other users have that demo doesn't
SELECT '';
SELECT 'RULES OTHER USERS HAVE (not in demo):' as info;
WITH demo_rules AS (
    SELECT 
        c.carrier_name,
        COALESCE(m.mga_name, 'Direct Appointment') as mga_name,
        cr.policy_type,
        cr.state
    FROM commission_rules cr
    JOIN carriers c ON cr.carrier_id = c.carrier_id
    LEFT JOIN mgas m ON cr.mga_id = m.mga_id
    WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
    AND cr.is_active = true
),
other_rules AS (
    SELECT DISTINCT
        c2.carrier_name,
        COALESCE(m2.mga_name, 'Direct Appointment') as mga_name,
        cr2.policy_type,
        cr2.state,
        cr2.new_rate,
        cr2.renewal_rate,
        cr2.rule_description
    FROM commission_rules cr2
    JOIN carriers c2 ON cr2.carrier_id = c2.carrier_id
    LEFT JOIN mgas m2 ON cr2.mga_id = m2.mga_id
    WHERE cr2.user_email != 'Demo@AgentCommissionTracker.com'
    AND cr2.is_active = true
)
SELECT 
    o.carrier_name,
    o.mga_name,
    o.policy_type,
    o.new_rate,
    o.renewal_rate,
    o.rule_description
FROM other_rules o
WHERE NOT EXISTS (
    SELECT 1 
    FROM demo_rules d 
    WHERE d.carrier_name = o.carrier_name 
    AND d.mga_name = o.mga_name
    AND COALESCE(d.policy_type, '') = COALESCE(o.policy_type, '')
    AND COALESCE(d.state, 'FL') = COALESCE(o.state, 'FL')
)
ORDER BY o.carrier_name, o.mga_name
LIMIT 30;

-- 3. Count how many unique rules demo is missing
SELECT '';
SELECT 'UNIQUE RULES DEMO IS MISSING:' as info;
WITH demo_combos AS (
    SELECT DISTINCT
        c.carrier_name || '-' || COALESCE(m.mga_name, 'Direct') || '-' || COALESCE(cr.policy_type, 'ALL') as combo
    FROM commission_rules cr
    JOIN carriers c ON cr.carrier_id = c.carrier_id
    LEFT JOIN mgas m ON cr.mga_id = m.mga_id
    WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
    AND cr.is_active = true
),
other_combos AS (
    SELECT DISTINCT
        c2.carrier_name || '-' || COALESCE(m2.mga_name, 'Direct') || '-' || COALESCE(cr2.policy_type, 'ALL') as combo
    FROM commission_rules cr2
    JOIN carriers c2 ON cr2.carrier_id = c2.carrier_id
    LEFT JOIN mgas m2 ON cr2.mga_id = m2.mga_id
    WHERE cr2.user_email != 'Demo@AgentCommissionTracker.com'
    AND cr2.is_active = true
)
SELECT COUNT(*) as missing_combinations
FROM other_combos o
WHERE o.combo NOT IN (SELECT combo FROM demo_combos);