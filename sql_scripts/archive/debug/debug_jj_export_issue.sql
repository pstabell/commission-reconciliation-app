-- DEBUG WHY J&J CARRIERS NOT EXPORTING
-- Run in PRIVATE database

-- 1. List ALL commission rules for the 5 J&J carriers
SELECT 'ALL RULES FOR J&J CARRIERS:' as info;
SELECT 
    c.carrier_name,
    cr.carrier_id,
    cr.mga_id,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.is_active,
    cr.rule_id
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE c.carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
ORDER BY c.carrier_name, m.mga_name;

-- 2. Check if there are duplicate carrier names
SELECT '';
SELECT 'CHECK FOR DUPLICATE CARRIER NAMES:' as info;
SELECT carrier_name, COUNT(*) as count, STRING_AGG(carrier_id::text, ', ') as carrier_ids
FROM carriers
WHERE carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
GROUP BY carrier_name
HAVING COUNT(*) > 1;

-- 3. Get the exact mga_id for Johnson and Johnson
SELECT '';
SELECT 'JOHNSON AND JOHNSON MGA ID:' as info;
SELECT mga_id, mga_name
FROM mgas
WHERE mga_name = 'Johnson and Johnson';

-- 4. Check rules by mga_id directly
SELECT '';
SELECT 'RULES FOR J&J MGA BY ID:' as info;
SELECT 
    cr.rule_id,
    c.carrier_name,
    cr.is_active
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE cr.mga_id = (SELECT mga_id FROM mgas WHERE mga_name = 'Johnson and Johnson')
ORDER BY c.carrier_name;

-- 5. Count all rules for J&J carriers broken down by MGA
SELECT '';
SELECT 'J&J CARRIERS RULE BREAKDOWN:' as info;
SELECT 
    c.carrier_name,
    CASE 
        WHEN cr.mga_id IS NULL THEN 'Direct (No MGA)'
        ELSE COALESCE(m.mga_name, 'MGA ID: ' || cr.mga_id::text)
    END as mga_association,
    COUNT(*) as rule_count
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE c.carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
GROUP BY c.carrier_name, cr.mga_id, m.mga_name
ORDER BY c.carrier_name, mga_association;

-- 6. Show only active rules
SELECT '';
SELECT 'ACTIVE J&J RULES ONLY:' as info;
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct') as mga_name,
    cr.policy_type,
    cr.new_rate
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE c.carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
AND cr.is_active = true
ORDER BY c.carrier_name, m.mga_name;