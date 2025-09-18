-- EXPORT AND GENERATE INSERT STATEMENTS FOR DEMO ACCOUNT
-- First, let's see the carriers and MGAs data

-- 1. Show all carriers
SELECT 'CARRIERS:' as section;
SELECT * FROM carriers ORDER BY carrier_name;

-- 2. Show all MGAs  
SELECT '';
SELECT 'MGAS:' as section;
SELECT * FROM mgas ORDER BY mga_name;

-- 3. Check if user_email column exists
SELECT '';
SELECT 'CHECKING FOR USER_EMAIL COLUMN:' as section;
SELECT 
    table_name,
    column_name
FROM information_schema.columns
WHERE table_name IN ('carriers', 'mgas', 'commission_rules')
AND column_name = 'user_email';