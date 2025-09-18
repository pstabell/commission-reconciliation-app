-- CHECK IF DEMO DATA ACTUALLY EXISTS

-- 1. Count all data for demo user
SELECT 'DEMO USER DATA COUNT:' as info;
SELECT 
    'Carriers: ' || COUNT(*) || ' (Active: ' || SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) || ')' as count
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'MGAs: ' || COUNT(*) || ' (Active: ' || SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) || ')'
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Commission Rules: ' || COUNT(*) || ' (Active: ' || SUM(CASE WHEN is_active = true THEN 1 ELSE 0 END) || ')'
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Show first 10 carriers with all details
SELECT '';
SELECT 'FIRST 10 CARRIERS FOR DEMO:' as info;
SELECT carrier_name, status, created_at, updated_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 10;

-- 3. Check total table counts
SELECT '';
SELECT 'TOTAL RECORDS IN TABLES:' as info;
SELECT 'Total carriers in database: ' || COUNT(*) as count FROM carriers
UNION ALL
SELECT 'Total MGAs in database: ' || COUNT(*) FROM mgas
UNION ALL  
SELECT 'Total commission rules in database: ' || COUNT(*) FROM commission_rules;

-- 4. List all distinct statuses
SELECT '';
SELECT 'ALL CARRIER STATUSES FOR DEMO:' as info;
SELECT DISTINCT status, COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status;