-- GET CURRENT FULL LIST FROM PRIVATE DATABASE
-- Run this in your PRIVATE database

-- 1. Count everything
SELECT 'CURRENT PRIVATE DATABASE TOTALS:' as info;
SELECT 
    (SELECT COUNT(*) FROM carriers) as total_carriers,
    (SELECT COUNT(*) FROM mgas) as total_mgas,
    (SELECT COUNT(*) FROM commission_rules WHERE is_active = true) as active_rules;

-- 2. List ALL carriers
SELECT '';
SELECT '=== ALL CARRIERS ===' as info;
SELECT carrier_id, carrier_name
FROM carriers
ORDER BY carrier_name;

-- 3. List ALL MGAs
SELECT '';
SELECT '=== ALL MGAS ===' as info;
SELECT mga_id, mga_name
FROM mgas
ORDER BY mga_name;

-- 4. Check specifically for the ones we're missing
SELECT '';
SELECT 'BURLINGTON CHECK:' as info;
SELECT * FROM carriers WHERE carrier_name LIKE '%Burlington%';

SELECT '';
SELECT 'BURNS & WILCOX CHECK:' as info;
SELECT * FROM mgas WHERE mga_name LIKE '%Burns%' OR mga_name LIKE '%Wilcox%';