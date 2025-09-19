-- EXPORT ALL DATA FROM PRIVATE DATABASE FOR DEMO IMPORT
-- Run this in your PRIVATE database to generate SQL for production

-- 1. Count what we're exporting
SELECT 'DATA TO EXPORT:' as info;
SELECT 'Total Active Commission Rules: ' || COUNT(*) as count
FROM commission_rules
WHERE is_active = true;

-- 2. Get unique carriers from commission rules
SELECT '';
SELECT 'UNIQUE CARRIERS TO EXPORT:' as info;
SELECT DISTINCT c.carrier_id, c.carrier_name
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE cr.is_active = true
ORDER BY c.carrier_name;

-- 3. Get unique MGAs from commission rules
SELECT '';
SELECT 'UNIQUE MGAS TO EXPORT:' as info;
SELECT DISTINCT m.mga_id, m.mga_name
FROM commission_rules cr
JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.is_active = true
ORDER BY m.mga_name;

-- 4. Generate carrier INSERT statements
SELECT '';
SELECT '-- CARRIER INSERT STATEMENTS:' as sql_statement;
SELECT 'INSERT INTO carriers (carrier_id, carrier_name, status, user_email) VALUES (''' 
    || c.carrier_id || ''', ''' 
    || REPLACE(c.carrier_name, '''', '''''') || ''', ''Active'', ''Demo@AgentCommissionTracker.com'');' as sql
FROM (
    SELECT DISTINCT c.carrier_id, c.carrier_name
    FROM commission_rules cr
    JOIN carriers c ON cr.carrier_id = c.carrier_id
    WHERE cr.is_active = true
) c
ORDER BY c.carrier_name;

-- 5. Generate MGA INSERT statements
SELECT '';
SELECT '-- MGA INSERT STATEMENTS:' as sql_statement;
SELECT 'INSERT INTO mgas (mga_id, mga_name, status, user_email) VALUES (''' 
    || m.mga_id || ''', ''' 
    || REPLACE(m.mga_name, '''', '''''') || ''', ''Active'', ''Demo@AgentCommissionTracker.com'');' as sql
FROM (
    SELECT DISTINCT m.mga_id, m.mga_name
    FROM commission_rules cr
    JOIN mgas m ON cr.mga_id = m.mga_id
    WHERE cr.is_active = true
) m
ORDER BY m.mga_name;

-- 6. Generate commission rule INSERT statements
SELECT '';
SELECT '-- COMMISSION RULE INSERT STATEMENTS:' as sql_statement;
SELECT 'INSERT INTO commission_rules (carrier_id, mga_id, state, policy_type, new_rate, renewal_rate, payment_terms, rule_description, user_email, is_default, is_active) VALUES (''' 
    || cr.carrier_id || ''', '
    || CASE WHEN cr.mga_id IS NULL THEN 'NULL' ELSE '''' || cr.mga_id || '''' END || ', '
    || CASE WHEN cr.state IS NULL THEN 'NULL' ELSE '''' || cr.state || '''' END || ', '
    || CASE WHEN cr.policy_type IS NULL THEN 'NULL' ELSE '''' || REPLACE(cr.policy_type, '''', '''''') || '''' END || ', '
    || cr.new_rate || ', '
    || COALESCE(cr.renewal_rate::text, 'NULL') || ', '
    || CASE WHEN cr.payment_terms IS NULL THEN 'NULL' ELSE '''' || REPLACE(cr.payment_terms, '''', '''''') || '''' END || ', '
    || CASE WHEN cr.rule_description IS NULL THEN 'NULL' ELSE '''' || REPLACE(cr.rule_description, '''', '''''') || '''' END || ', '
    || '''Demo@AgentCommissionTracker.com'', '
    || CASE WHEN cr.is_default THEN 'true' ELSE 'false' END || ', '
    || 'true);' as sql
FROM commission_rules cr
WHERE cr.is_active = true
ORDER BY cr.carrier_id, cr.mga_id;