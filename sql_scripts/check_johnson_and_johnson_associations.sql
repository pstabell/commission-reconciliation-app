-- CHECK JOHNSON AND JOHNSON ASSOCIATIONS IN PRIVATE DATABASE
-- Run this in your PRIVATE database

-- 1. Confirm Johnson and Johnson MGA exists
SELECT 'JOHNSON AND JOHNSON MGA:' as info;
SELECT mga_id, mga_name
FROM mgas
WHERE mga_name = 'Johnson and Johnson';

-- 2. Check commission rules for Johnson and Johnson
SELECT '';
SELECT 'COMMISSION RULES FOR JOHNSON AND JOHNSON:' as info;
SELECT 
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.is_active
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE m.mga_name = 'Johnson and Johnson'
ORDER BY c.carrier_name;

-- 3. Count rules by carrier
SELECT '';
SELECT 'CARRIER COUNT FOR JOHNSON AND JOHNSON:' as info;
SELECT 
    COUNT(DISTINCT c.carrier_name) as carrier_count,
    STRING_AGG(DISTINCT c.carrier_name, ', ') as carrier_names
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE m.mga_name = 'Johnson and Johnson';

-- 4. Check if the 5 expected carriers have any rules
SELECT '';
SELECT 'EXPECTED J&J CARRIERS STATUS:' as info;
SELECT 
    carrier_name,
    CASE 
        WHEN carrier_name IN (
            SELECT DISTINCT c.carrier_name
            FROM commission_rules cr
            JOIN carriers c ON cr.carrier_id = c.carrier_id
            JOIN mgas m ON cr.mga_id = m.mga_id
            WHERE m.mga_name = 'Johnson and Johnson'
        ) THEN 'Has Johnson and Johnson rules'
        ELSE 'No Johnson and Johnson rules'
    END as status
FROM carriers
WHERE carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
ORDER BY carrier_name;

-- 5. Check all rules for these 5 carriers
SELECT '';
SELECT 'ALL RULES FOR J&J CARRIERS:' as info;
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct/No MGA') as mga_name,
    COUNT(*) as rule_count
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE c.carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
AND cr.is_active = true
GROUP BY c.carrier_name, m.mga_name
ORDER BY c.carrier_name, m.mga_name;