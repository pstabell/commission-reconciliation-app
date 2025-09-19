-- CHECK JOHNSON & JOHNSON CARRIERS

-- 1. Check if Johnson & Johnson MGA exists
SELECT 'JOHNSON & JOHNSON MGA:' as info;
SELECT mga_id, mga_name, status
FROM mgas
WHERE mga_name LIKE '%Johnson%'
ORDER BY mga_name;

-- 2. Check for the 5 carriers that should be associated
SELECT '';
SELECT 'CHECKING FOR J&J CARRIERS:' as info;
SELECT carrier_name,
       CASE 
           WHEN carrier_name IN (SELECT carrier_name FROM carriers) THEN 'EXISTS'
           ELSE 'MISSING'
       END as status
FROM (VALUES 
    ('Voyager'),
    ('Great Lakes'),
    ('ICW'),
    ('Mount Vernon'),
    ('Evanston')
) AS j_carriers(carrier_name);

-- 3. Check what carriers actually exist
SELECT '';
SELECT 'ACTUAL CARRIERS IN DATABASE:' as info;
SELECT carrier_name
FROM carriers
WHERE carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
ORDER BY carrier_name;

-- 4. Add the missing carriers
-- Uncomment and run these if carriers are missing
/*
INSERT INTO carriers (carrier_id, carrier_name, status, created_at, updated_at)
VALUES 
    (gen_random_uuid(), 'Voyager', 'Active', NOW(), NOW()),
    (gen_random_uuid(), 'Mount Vernon', 'Active', NOW(), NOW()),
    (gen_random_uuid(), 'Evanston', 'Active', NOW(), NOW())
ON CONFLICT (carrier_name) DO NOTHING;
*/

-- 5. Check commission rules for Johnson & Johnson
SELECT '';
SELECT 'J&J COMMISSION RULES:' as info;
SELECT 
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE m.mga_name LIKE '%Johnson%'
ORDER BY c.carrier_name;