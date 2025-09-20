-- SHOW CARRIERS AND MGAS DATA WITH USER_EMAIL

-- 1. Show first 10 carriers to see the structure
SELECT 'SAMPLE CARRIERS (first 10):' as section;
SELECT carrier_id, carrier_name, user_email 
FROM carriers 
ORDER BY carrier_name 
LIMIT 10;

-- 2. Show first 10 MGAs
SELECT '';
SELECT 'SAMPLE MGAS (first 10):' as section;
SELECT mga_id, mga_name, user_email 
FROM mgas 
ORDER BY mga_name 
LIMIT 10;

-- 3. Count by user_email
SELECT '';
SELECT 'DATA COUNT BY USER:' as section;
SELECT 
    user_email,
    COUNT(*) as carrier_count
FROM carriers
GROUP BY user_email
ORDER BY user_email;

SELECT '';
SELECT 
    user_email,
    COUNT(*) as mga_count
FROM mgas
GROUP BY user_email
ORDER BY user_email;

SELECT '';
SELECT 
    user_email,
    COUNT(*) as rule_count
FROM commission_rules
GROUP BY user_email
ORDER BY user_email;