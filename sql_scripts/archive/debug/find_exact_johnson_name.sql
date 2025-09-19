-- FIND THE EXACT JOHNSON & JOHNSON NAME IN PRIVATE DATABASE
-- Run this in your PRIVATE database

-- 1. Find all MGAs with "johnson" in the name (case insensitive)
SELECT 'ALL MGAS WITH JOHNSON IN NAME:' as info;
SELECT mga_id, mga_name
FROM mgas
WHERE LOWER(mga_name) LIKE '%johnson%'
ORDER BY mga_name;

-- 2. List all MGA names to find it
SELECT '';
SELECT 'ALL MGA NAMES IN DATABASE:' as info;
SELECT mga_name
FROM mgas
ORDER BY mga_name;

-- 3. Check if it might be under different spelling
SELECT '';
SELECT 'CHECKING VARIATIONS:' as info;
SELECT mga_name
FROM mgas
WHERE LOWER(mga_name) LIKE '%j%j%'
   OR LOWER(mga_name) LIKE '%j&j%'
   OR LOWER(mga_name) LIKE '%jj%'
   OR LOWER(mga_name) LIKE '%john%'
ORDER BY mga_name;