-- EXPORT CARRIERS AND MGAS FROM PRIVATE DATABASE (PostgreSQL version)
-- Run this in your PRIVATE/LOCAL database to get the data

-- 1. Export Carriers as INSERT statements
SELECT 'Carriers Export:' as info;
SELECT 
    'INSERT INTO carriers (carrier_name, naic_code, producer_code, status, notes, user_email) VALUES (' ||
    quote_literal(carrier_name) || ', ' ||
    COALESCE(quote_literal(naic_code), 'NULL') || ', ' ||
    COALESCE(quote_literal(producer_code), 'NULL') || ', ' ||
    quote_literal(COALESCE(status, 'Active')) || ', ' ||
    COALESCE(quote_literal(notes), 'NULL') || ', ' ||
    '''Demo@AgentCommissionTracker.com'');'
    as insert_statement
FROM carriers
ORDER BY carrier_name;

-- 2. Export MGAs as INSERT statements
SELECT '';
SELECT 'MGAs Export:' as info;
SELECT 
    'INSERT INTO mgas (mga_name, status, notes, user_email) VALUES (' ||
    quote_literal(mga_name) || ', ' ||
    quote_literal(COALESCE(status, 'Active')) || ', ' ||
    COALESCE(quote_literal(notes), 'NULL') || ', ' ||
    '''Demo@AgentCommissionTracker.com'');'
    as insert_statement
FROM mgas
ORDER BY mga_name;

-- 3. Count what we're exporting
SELECT '';
SELECT 'Export Summary:' as info;
SELECT 'Total Carriers: ' || COUNT(*) as count FROM carriers
UNION ALL
SELECT 'Total MGAs: ' || COUNT(*) FROM mgas
UNION ALL
SELECT 'Total Commission Rules: ' || COUNT(*) FROM commission_rules;