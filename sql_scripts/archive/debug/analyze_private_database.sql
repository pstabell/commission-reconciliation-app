-- ANALYZE PRIVATE DATABASE STRUCTURE AND DATA
-- Run this in your PRIVATE database to understand what tables and data exist

-- 1. List all tables in the database
SELECT 'ALL TABLES IN DATABASE:' as info;
SELECT name FROM sqlite_master 
WHERE type='table' 
ORDER BY name;

-- 2. Check if carriers table exists and count records
SELECT '';
SELECT 'CARRIERS TABLE:' as info;
SELECT COUNT(*) as total_carriers 
FROM carriers
WHERE 1=1;  -- This will error if table doesn't exist

-- 3. Check if mgas table exists and count records
SELECT '';
SELECT 'MGAS TABLE:' as info;
SELECT COUNT(*) as total_mgas 
FROM mgas
WHERE 1=1;  -- This will error if table doesn't exist

-- 4. Check if commission_rules table exists and count records
SELECT '';
SELECT 'COMMISSION_RULES TABLE:' as info;
SELECT COUNT(*) as total_rules 
FROM commission_rules
WHERE 1=1;  -- This will error if table doesn't exist

-- 5. If above queries fail, check policies table structure
SELECT '';
SELECT 'POLICIES TABLE STRUCTURE (first row):' as info;
SELECT * FROM policies LIMIT 1;

-- 6. Get unique carriers from policies table
SELECT '';
SELECT 'UNIQUE CARRIERS IN POLICIES:' as info;
SELECT COUNT(DISTINCT carrier) as unique_carriers FROM policies;
SELECT DISTINCT carrier FROM policies ORDER BY carrier LIMIT 20;

-- 7. Get unique MGAs from policies table (if column exists)
SELECT '';
SELECT 'UNIQUE MGAS IN POLICIES:' as info;
SELECT COUNT(DISTINCT mga) as unique_mgas FROM policies WHERE mga IS NOT NULL;
SELECT DISTINCT mga FROM policies WHERE mga IS NOT NULL ORDER BY mga LIMIT 20;