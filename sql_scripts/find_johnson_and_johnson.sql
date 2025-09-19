-- FIND JOHNSON AND JOHNSON (spelled out)
-- Run in PRIVATE database

-- 1. Search for Johnson and Johnson
SELECT 'SEARCHING FOR JOHNSON AND JOHNSON:' as info;
SELECT mga_id, mga_name, status, created_at
FROM mgas 
WHERE LOWER(mga_name) LIKE '%johnson and johnson%'
   OR LOWER(mga_name) LIKE '%johnson%johnson%';

-- 2. Count MGAs again but show names
SELECT '';
SELECT 'ALL 16 MGAS IN PRIVATE:' as info;
SELECT mga_name FROM mgas ORDER BY mga_name;

-- 3. If Johnson and Johnson isn't in the 16, where is it?
SELECT '';
SELECT 'CHECKING COMMISSION RULES FOR J&J:' as info;
SELECT DISTINCT 
    c.carrier_name,
    cr.mga_id,
    m.mga_name
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE c.carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
   OR LOWER(m.mga_name) LIKE '%johnson%';

-- 4. Maybe it's linked differently?
SELECT '';
SELECT 'CARRIERS THAT MIGHT BE J&J:' as info;
SELECT carrier_id, carrier_name
FROM carriers
WHERE carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston');