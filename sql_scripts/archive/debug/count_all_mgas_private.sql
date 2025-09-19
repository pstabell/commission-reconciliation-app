-- COUNT ALL MGAS IN PRIVATE DATABASE
-- Run this in your PRIVATE database

-- 1. Count total MGAs in mgas table
SELECT 'TOTAL MGAS IN TABLE:' as info;
SELECT COUNT(*) as total_mgas FROM mgas;

-- 2. Count unique MGAs referenced in commission rules
SELECT '';
SELECT 'UNIQUE MGAS IN COMMISSION RULES:' as info;
SELECT COUNT(DISTINCT mga_id) as unique_mgas 
FROM commission_rules 
WHERE mga_id IS NOT NULL 
AND is_active = true;

-- 3. List all MGAs from mgas table
SELECT '';
SELECT 'ALL MGAS IN DATABASE:' as info;
SELECT mga_id, mga_name, status
FROM mgas
ORDER BY mga_name;

-- 4. Check for MGAs in commission rules that might not be in mgas table
SELECT '';
SELECT 'MGA IDS IN COMMISSION RULES:' as info;
SELECT DISTINCT cr.mga_id, m.mga_name
FROM commission_rules cr
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.mga_id IS NOT NULL
AND cr.is_active = true
ORDER BY m.mga_name;

-- 5. Count rules with and without MGAs
SELECT '';
SELECT 'COMMISSION RULES BREAKDOWN:' as info;
SELECT 
    'Rules with MGA: ' || COUNT(*) as count
FROM commission_rules 
WHERE mga_id IS NOT NULL 
AND is_active = true
UNION ALL
SELECT 
    'Rules without MGA (Direct): ' || COUNT(*)
FROM commission_rules 
WHERE mga_id IS NULL 
AND is_active = true;