-- GET CARRIERS FROM PRIVATE DATABASE
-- Run this in your PRIVATE database

-- Count unique carriers first
SELECT 'TOTAL UNIQUE CARRIERS: ' || COUNT(DISTINCT c.carrier_id) as count
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE cr.is_active = true;

-- Generate carrier INSERT statements
SELECT '';
SELECT '-- CARRIER INSERT STATEMENTS:' as info;
SELECT DISTINCT 
    'INSERT INTO carriers (carrier_id, carrier_name, status, user_email) VALUES (''' 
    || c.carrier_id || ''', ''' 
    || REPLACE(c.carrier_name, '''', '''''') || ''', ''Active'', ''Demo@AgentCommissionTracker.com'');' as sql
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE cr.is_active = true
ORDER BY c.carrier_name;