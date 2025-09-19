-- GET ABSOLUTELY EVERYTHING FROM PRIVATE DATABASE
-- Run this in your PRIVATE database

-- 1. Get TOTAL counts first
SELECT '=== TOTAL COUNTS IN PRIVATE DATABASE ===' as info;
SELECT 
    (SELECT COUNT(*) FROM carriers) as total_carriers,
    (SELECT COUNT(*) FROM mgas) as total_mgas,
    (SELECT COUNT(*) FROM commission_rules WHERE is_active = true) as active_rules;

-- 2. Export ALL carriers with their IDs
SELECT '';
SELECT '=== ALL CARRIERS FOR EXPORT ===' as info;
SELECT 
    'INSERT INTO carriers (carrier_id, carrier_name, status, user_email, created_at, updated_at) VALUES (''' 
    || carrier_id || ''', ''' 
    || REPLACE(carrier_name, '''', '''''') || ''', '''
    || COALESCE(status, 'Active') || ''', ''Demo@AgentCommissionTracker.com'', NOW(), NOW());' as sql_insert
FROM carriers
ORDER BY carrier_name;

-- 3. Export ALL MGAs with their IDs
SELECT '';
SELECT '=== ALL MGAS FOR EXPORT ===' as info;
SELECT 
    'INSERT INTO mgas (mga_id, mga_name, status, user_email, created_at, updated_at) VALUES (''' 
    || mga_id || ''', ''' 
    || REPLACE(mga_name, '''', '''''') || ''', '''
    || COALESCE(status, 'Active') || ''', ''Demo@AgentCommissionTracker.com'', NOW(), NOW());' as sql_insert
FROM mgas
ORDER BY mga_name;

-- 4. Just to be sure, let's specifically check for the ones you mentioned
SELECT '';
SELECT '=== SPECIFIC CHECKS ===' as info;
SELECT 'Burlington: ' || COUNT(*) as check FROM carriers WHERE carrier_name LIKE '%Burlington%'
UNION ALL
SELECT 'Burns & Wilcox: ' || COUNT(*) FROM mgas WHERE mga_name LIKE '%Burns%'
UNION ALL  
SELECT 'Johnson & Johnson: ' || COUNT(*) FROM mgas WHERE mga_name LIKE '%Johnson%';

-- 5. Get the TRUE count
SELECT '';
SELECT '=== THIS IS THE REAL COUNT ===' as info;
SELECT 'You should have ' || COUNT(*) || ' carriers in total' as reality FROM carriers
UNION ALL
SELECT 'You should have ' || COUNT(*) || ' MGAs in total' FROM mgas;