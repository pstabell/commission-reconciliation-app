-- INVESTIGATE MISSING CARRIERS

-- 1. Count carriers by user_email
SELECT 'CARRIERS BY USER:' as info;
SELECT 
    COALESCE(user_email, 'NULL') as user_email,
    COUNT(*) as carrier_count,
    SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_count
FROM carriers
GROUP BY user_email
ORDER BY carrier_count DESC;

-- 2. Check for carriers without user_email
SELECT '';
SELECT 'CARRIERS WITHOUT USER_EMAIL:' as info;
SELECT COUNT(*) as count
FROM carriers
WHERE user_email IS NULL;

-- 3. Show sample carriers without user_email
SELECT '';
SELECT 'SAMPLE CARRIERS WITHOUT USER_EMAIL:' as info;
SELECT carrier_name, status, created_at
FROM carriers
WHERE user_email IS NULL
ORDER BY carrier_name
LIMIT 10;

-- 4. Count MGAs by user
SELECT '';
SELECT 'MGAS BY USER:' as info;
SELECT 
    COALESCE(user_email, 'NULL') as user_email,
    COUNT(*) as mga_count
FROM mgas
GROUP BY user_email
ORDER BY mga_count DESC;

-- 5. Count commission rules by user
SELECT '';
SELECT 'COMMISSION RULES BY USER:' as info;
SELECT 
    COALESCE(user_email, 'NULL') as user_email,
    COUNT(*) as rule_count
FROM commission_rules
GROUP BY user_email
ORDER BY rule_count DESC;