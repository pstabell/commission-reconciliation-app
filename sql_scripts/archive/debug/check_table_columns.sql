-- CHECK WHAT COLUMNS EXIST IN CARRIERS, MGAS, AND COMMISSION_RULES TABLES

-- 1. Check carriers table structure
SELECT 'CARRIERS TABLE COLUMNS:' as info;
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'carriers'
ORDER BY ordinal_position;

-- 2. Check mgas table structure
SELECT '';
SELECT 'MGAS TABLE COLUMNS:' as info;
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'mgas'
ORDER BY ordinal_position;

-- 3. Check commission_rules table structure
SELECT '';
SELECT 'COMMISSION_RULES TABLE COLUMNS:' as info;
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'commission_rules'
ORDER BY ordinal_position;

-- 4. Quick data check (first 5 rows from each table)
SELECT '';
SELECT 'SAMPLE CARRIERS DATA:' as info;
SELECT * FROM carriers LIMIT 5;

SELECT '';
SELECT 'SAMPLE MGAS DATA:' as info;
SELECT * FROM mgas LIMIT 5;

SELECT '';
SELECT 'SAMPLE COMMISSION RULES DATA:' as info;
SELECT * FROM commission_rules LIMIT 5;