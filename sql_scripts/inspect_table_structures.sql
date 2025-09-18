-- CHECK EXACT COLUMN NAMES IN ALL TABLES

-- 1. Show all columns in carriers table
SELECT 'CARRIERS TABLE STRUCTURE:' as info;
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'carriers'
AND table_schema = 'public'
ORDER BY ordinal_position;

-- 2. Show all columns in mgas table
SELECT '';
SELECT 'MGAS TABLE STRUCTURE:' as info;
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'mgas'
AND table_schema = 'public'
ORDER BY ordinal_position;

-- 3. Show all columns in commission_rules table
SELECT '';
SELECT 'COMMISSION_RULES TABLE STRUCTURE:' as info;
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'commission_rules'
AND table_schema = 'public'
ORDER BY ordinal_position;

-- 4. Show first row from each table to see actual data
SELECT '';
SELECT 'SAMPLE CARRIER:' as info;
SELECT * FROM carriers LIMIT 1;

SELECT '';
SELECT 'SAMPLE MGA:' as info;
SELECT * FROM mgas LIMIT 1;

SELECT '';
SELECT 'SAMPLE RULE:' as info;
SELECT * FROM commission_rules LIMIT 1;