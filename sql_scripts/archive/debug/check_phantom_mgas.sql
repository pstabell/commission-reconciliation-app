-- CHECK FOR PHANTOM MGAS (MGAs referenced in rules but not in MGA table)
-- Run in PRIVATE database

-- 1. Find all unique MGA IDs referenced in commission rules
SELECT 'MGA IDS IN COMMISSION RULES:' as info;
SELECT DISTINCT 
    cr.mga_id,
    m.mga_name as mga_name_from_table,
    CASE 
        WHEN m.mga_id IS NULL THEN 'PHANTOM MGA - NOT IN TABLE!'
        ELSE 'Exists in MGA table'
    END as status
FROM commission_rules cr
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.mga_id IS NOT NULL
ORDER BY status DESC, m.mga_name;

-- 2. Count phantom MGAs
SELECT '';
SELECT 'PHANTOM MGA COUNT:' as info;
SELECT COUNT(DISTINCT cr.mga_id) as phantom_mgas
FROM commission_rules cr
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.mga_id IS NOT NULL 
  AND m.mga_id IS NULL;

-- 3. If we have phantoms, what carriers use them?
SELECT '';
SELECT 'CARRIERS USING PHANTOM MGAS:' as info;
SELECT DISTINCT
    c.carrier_name,
    cr.mga_id as phantom_mga_id
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.mga_id IS NOT NULL 
  AND m.mga_id IS NULL
ORDER BY c.carrier_name;