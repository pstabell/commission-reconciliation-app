-- GET CARRIERS AND MGAS FROM PRIVATE DATABASE
-- Run this in your PRIVATE database

-- 1. Generate carrier INSERT statements
SELECT '-- CARRIER INSERT STATEMENTS:' as sql_statement;
SELECT DISTINCT 
    'INSERT INTO carriers (carrier_id, carrier_name, status, user_email) VALUES (''' 
    || c.carrier_id || ''', ''' 
    || REPLACE(c.carrier_name, '''', '''''') || ''', ''Active'', ''Demo@AgentCommissionTracker.com'');' as sql
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE cr.is_active = true
ORDER BY sql;

-- 2. Generate MGA INSERT statements (excluding NULLs)
SELECT '';
SELECT '-- MGA INSERT STATEMENTS:' as sql_statement;
SELECT DISTINCT 
    'INSERT INTO mgas (mga_id, mga_name, status, user_email) VALUES (''' 
    || m.mga_id || ''', ''' 
    || REPLACE(m.mga_name, '''', '''''') || ''', ''Active'', ''Demo@AgentCommissionTracker.com'');' as sql
FROM commission_rules cr
JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.is_active = true
ORDER BY sql;