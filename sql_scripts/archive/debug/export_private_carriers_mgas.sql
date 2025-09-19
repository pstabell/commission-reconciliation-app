-- EXPORT CARRIERS AND MGAS FROM PRIVATE DATABASE
-- Run this in your PRIVATE/LOCAL database to get the data

-- 1. Export Carriers as INSERT statements
SELECT 'Carriers Export:' as info;
SELECT 
    'INSERT INTO carriers (carrier_name, naic_code, producer_code, status, notes, user_email) VALUES (' ||
    QUOTE(carrier_name) || ', ' ||
    COALESCE(QUOTE(naic_code), 'NULL') || ', ' ||
    COALESCE(QUOTE(producer_code), 'NULL') || ', ' ||
    QUOTE(COALESCE(status, 'Active')) || ', ' ||
    COALESCE(QUOTE(notes), 'NULL') || ', ' ||
    '''Demo@AgentCommissionTracker.com'');'
    as insert_statement
FROM carriers
ORDER BY carrier_name;

-- 2. Export MGAs as INSERT statements
SELECT 'MGAs Export:' as info;
SELECT 
    'INSERT INTO mgas (mga_name, status, notes, user_email) VALUES (' ||
    QUOTE(mga_name) || ', ' ||
    QUOTE(COALESCE(status, 'Active')) || ', ' ||
    COALESCE(QUOTE(notes), 'NULL') || ', ' ||
    '''Demo@AgentCommissionTracker.com'');'
    as insert_statement
FROM mgas
ORDER BY mga_name;

-- 3. Count what we're exporting
SELECT 'Export Summary:' as info;
SELECT 'Total Carriers: ' || COUNT(*) as count FROM carriers
UNION ALL
SELECT 'Total MGAs: ' || COUNT(*) FROM mgas
UNION ALL
SELECT 'Total Commission Rules: ' || COUNT(*) FROM commission_rules;