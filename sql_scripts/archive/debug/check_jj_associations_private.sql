-- CHECK JOHNSON & JOHNSON ASSOCIATIONS IN PRIVATE DATABASE
-- Run this in your PRIVATE database to see what should have been exported

-- 1. Check if Johnson & Johnson MGA exists
SELECT 'JOHNSON & JOHNSON IN PRIVATE:' as info;
SELECT mga_id, mga_name
FROM mgas
WHERE mga_name LIKE '%Johnson%';

-- 2. Check commission rules for J&J
SELECT '';
SELECT 'COMMISSION RULES FOR JOHNSON & JOHNSON:' as info;
SELECT 
    c.carrier_name,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.is_active
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE m.mga_name LIKE '%Johnson%'
ORDER BY c.carrier_name;

-- 3. Check if those 5 carriers have rules without MGAs
SELECT '';
SELECT 'RULES FOR J&J CARRIERS:' as info;
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct/No MGA') as mga_name,
    COUNT(*) as rule_count
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE c.carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
GROUP BY c.carrier_name, m.mga_name
ORDER BY c.carrier_name, m.mga_name;

-- 4. Get the specific rule details
SELECT '';
SELECT 'DETAILED RULES FOR J&J CARRIERS:' as info;
SELECT 
    cr.rule_id,
    c.carrier_name,
    cr.mga_id,
    m.mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.is_active
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE c.carrier_name IN ('Voyager', 'Great Lakes', 'ICW', 'Mount Vernon', 'Evanston')
ORDER BY c.carrier_name;