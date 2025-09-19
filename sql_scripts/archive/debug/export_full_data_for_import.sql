-- EXPORT ALL DATA IN INSERT STATEMENT FORMAT
-- This will generate the SQL statements needed to recreate all data

-- 1. Generate INSERT statements for Carriers
SELECT 'INSERT INTO carriers (carrier_id, carrier_name, naic_code, producer_code, status, notes) VALUES' as sql_statement
UNION ALL
SELECT 
    '(' || 
    '''' || carrier_id || ''', ' ||
    '''' || REPLACE(carrier_name, '''', '''''') || ''', ' ||
    COALESCE('''' || REPLACE(naic_code, '''', '''''') || '''', 'NULL') || ', ' ||
    COALESCE('''' || REPLACE(producer_code, '''', '''''') || '''', 'NULL') || ', ' ||
    COALESCE('''' || status || '''', '''Active''') || ', ' ||
    COALESCE('''' || REPLACE(notes, '''', '''''') || '''', 'NULL') || 
    ')' || CASE WHEN ROW_NUMBER() OVER (ORDER BY carrier_name) = COUNT(*) OVER () THEN ';' ELSE ',' END
FROM carriers
ORDER BY carrier_name;

-- 2. Generate INSERT statements for MGAs
SELECT '';
SELECT 'INSERT INTO mgas (mga_id, mga_name, status, notes) VALUES' as sql_statement
UNION ALL
SELECT 
    '(' || 
    '''' || mga_id || ''', ' ||
    '''' || REPLACE(mga_name, '''', '''''') || ''', ' ||
    COALESCE('''' || status || '''', '''Active''') || ', ' ||
    COALESCE('''' || REPLACE(notes, '''', '''''') || '''', 'NULL') || 
    ')' || CASE WHEN ROW_NUMBER() OVER (ORDER BY mga_name) = COUNT(*) OVER () THEN ';' ELSE ',' END
FROM mgas
ORDER BY mga_name;

-- 3. Generate INSERT statements for Commission Rules
SELECT '';
SELECT 'INSERT INTO commission_rules (carrier_id, mga_id, state, policy_type, term_months, new_rate, renewal_rate, payment_terms, rule_description, rule_priority, is_default) VALUES' as sql_statement
UNION ALL
SELECT 
    '(' || 
    '''' || carrier_id || ''', ' ||
    COALESCE('''' || mga_id || '''', 'NULL') || ', ' ||
    COALESCE('''' || state || '''', 'NULL') || ', ' ||
    COALESCE('''' || REPLACE(policy_type, '''', '''''') || '''', 'NULL') || ', ' ||
    COALESCE(term_months::text, 'NULL') || ', ' ||
    new_rate || ', ' ||
    COALESCE(renewal_rate::text, 'NULL') || ', ' ||
    COALESCE('''' || REPLACE(payment_terms, '''', '''''') || '''', 'NULL') || ', ' ||
    COALESCE('''' || REPLACE(rule_description, '''', '''''') || '''', 'NULL') || ', ' ||
    COALESCE(rule_priority::text, '100') || ', ' ||
    CASE WHEN is_default THEN 'true' ELSE 'false' END ||
    ')' || CASE WHEN ROW_NUMBER() OVER (ORDER BY carrier_id, mga_id, rule_priority) = COUNT(*) OVER () THEN ';' ELSE ',' END
FROM commission_rules
WHERE is_active = true
ORDER BY carrier_id, mga_id, rule_priority;