-- FIND JOHNSON & JOHNSON AND ITS CARRIERS
-- Run in PRIVATE database

-- 1. Search for Johnson in ALL text fields in MGAs table
SELECT 'SEARCHING MGAS TABLE:' as info;
SELECT * FROM mgas 
WHERE mga_name LIKE '%Johnson%' 
   OR mga_name LIKE '%J&J%'
   OR mga_name LIKE '%J & J%';

-- 2. Search commission rules for Johnson & Johnson
SELECT '';
SELECT 'SEARCHING COMMISSION RULES:' as info;
SELECT DISTINCT 
    cr.mga_id,
    m.mga_name,
    c.carrier_name
FROM commission_rules cr
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE m.mga_name LIKE '%Johnson%' 
   OR EXISTS (
       SELECT 1 FROM carriers c2 
       WHERE c2.carrier_id = cr.carrier_id 
       AND c2.carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
   );

-- 3. Search for those specific carriers
SELECT '';
SELECT 'SEARCHING FOR J&J CARRIERS:' as info;
SELECT carrier_id, carrier_name
FROM carriers
WHERE carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
ORDER BY carrier_name;

-- 4. Could J&J be in carrier_mga_relationships table?
SELECT '';
SELECT 'CHECKING RELATIONSHIPS TABLE:' as info;
-- First check if table exists
SELECT COUNT(*) as relationship_records FROM carrier_mga_relationships;

-- 5. Check if J&J might be stored as something else
SELECT '';
SELECT 'ALL MGA NAMES TO FIND J&J:' as info;
SELECT mga_id, mga_name FROM mgas ORDER BY mga_name;