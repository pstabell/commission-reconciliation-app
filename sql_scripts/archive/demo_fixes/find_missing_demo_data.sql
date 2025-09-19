-- FIND MISSING DEMO DATA
-- Based on our chat history, we should have:
-- 63 carriers (including Burlington)
-- 16 MGAs (but Burns & Wilcox wasn't in the original list)
-- 78 commission rules

-- 1. Current demo counts
SELECT 'CURRENT DEMO COUNTS:' as info;
SELECT 
    (SELECT COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com') as carriers,
    (SELECT COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com') as mgas,
    (SELECT COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com') as rules;

-- 2. List all demo carriers to compare with private list
SELECT '';
SELECT 'ALL DEMO CARRIERS:' as info;
SELECT carrier_name
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name;

-- 3. Check for Burlington specifically
SELECT '';
SELECT 'BURLINGTON CHECK:' as info;
SELECT carrier_name
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND LOWER(carrier_name) LIKE '%burlington%';

-- Note: Burns & Wilcox was NOT in the original 16 MGAs list, so it's expected to be missing