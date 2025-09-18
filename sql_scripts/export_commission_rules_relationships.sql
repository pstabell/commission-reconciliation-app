-- EXPORT COMMISSION RULES AND RELATIONSHIPS FROM PRIVATE DATABASE
-- Run this AFTER importing carriers/MGAs to production

-- Step 1: First, you need to create a mapping between private and production IDs
-- This query helps you see the carriers/MGAs to manually map
SELECT 'Carrier Mapping Needed:' as info;
SELECT 
    c.carrier_name,
    c.carrier_id as private_carrier_id,
    '-- Find production ID for: ' || c.carrier_name as action
FROM carriers c
WHERE EXISTS (
    SELECT 1 FROM commission_rules cr 
    WHERE cr.carrier_id = c.carrier_id
)
ORDER BY c.carrier_name;

SELECT 'MGA Mapping Needed:' as info;
SELECT 
    m.mga_name,
    m.mga_id as private_mga_id,
    '-- Find production ID for: ' || m.mga_name as action
FROM mgas m
WHERE EXISTS (
    SELECT 1 FROM commission_rules cr 
    WHERE cr.mga_id = m.mga_id
)
ORDER BY m.mga_name;

-- Step 2: Export commission rules with names (not IDs)
SELECT 'Commission Rules Export:' as info;
SELECT 
    'INSERT INTO commission_rules (carrier_id, mga_id, policy_type, new_rate, renewal_rate, payment_terms, rule_description, user_email) ' ||
    'SELECT ' ||
    '(SELECT carrier_id FROM carriers WHERE carrier_name = ' || QUOTE(c.carrier_name) || ' AND user_email = ''Demo@AgentCommissionTracker.com''), ' ||
    CASE 
        WHEN m.mga_name IS NOT NULL 
        THEN '(SELECT mga_id FROM mgas WHERE mga_name = ' || QUOTE(m.mga_name) || ' AND user_email = ''Demo@AgentCommissionTracker.com''), '
        ELSE 'NULL, '
    END ||
    COALESCE(QUOTE(cr.policy_type), 'NULL') || ', ' ||
    cr.new_rate || ', ' ||
    COALESCE(cr.renewal_rate::text, 'NULL') || ', ' ||
    COALESCE(QUOTE(cr.payment_terms), 'NULL') || ', ' ||
    COALESCE(QUOTE(cr.rule_description), 'NULL') || ', ' ||
    '''Demo@AgentCommissionTracker.com'';'
    as insert_statement
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
ORDER BY c.carrier_name, m.mga_name, cr.policy_type;

-- Step 3: Export carrier-MGA relationships
SELECT 'Carrier-MGA Relationships Export:' as info;
SELECT 
    'INSERT INTO carrier_mga_relationships (carrier_id, mga_id, is_direct, user_email) ' ||
    'SELECT ' ||
    '(SELECT carrier_id FROM carriers WHERE carrier_name = ' || QUOTE(c.carrier_name) || ' AND user_email = ''Demo@AgentCommissionTracker.com''), ' ||
    '(SELECT mga_id FROM mgas WHERE mga_name = ' || QUOTE(m.mga_name) || ' AND user_email = ''Demo@AgentCommissionTracker.com''), ' ||
    CASE WHEN cmr.is_direct THEN 'true' ELSE 'false' END || ', ' ||
    '''Demo@AgentCommissionTracker.com'';'
    as insert_statement
FROM carrier_mga_relationships cmr
JOIN carriers c ON cmr.carrier_id = c.carrier_id
JOIN mgas m ON cmr.mga_id = m.mga_id
ORDER BY c.carrier_name, m.mga_name;