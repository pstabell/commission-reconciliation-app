-- CHECK AND FIX CARRIER/MGA STATUS FOR DEMO USER

-- 1. Check current status values
SELECT 'CURRENT CARRIER STATUS VALUES:' as info;
SELECT status, COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status
ORDER BY count DESC;

-- 2. Check MGA status values
SELECT '';
SELECT 'CURRENT MGA STATUS VALUES:' as info;
SELECT status, COUNT(*) as count
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status
ORDER BY count DESC;

-- 3. Fix carriers - set all to 'Active' (capital A)
UPDATE carriers
SET status = 'Active'
WHERE user_email = 'Demo@AgentCommissionTracker.com'
  AND (status IS NULL OR status != 'Active');

-- 4. Fix MGAs - set all to 'Active' (capital A)
UPDATE mgas
SET status = 'Active'
WHERE user_email = 'Demo@AgentCommissionTracker.com'
  AND (status IS NULL OR status != 'Active');

-- 5. Verify the fix
SELECT '';
SELECT 'AFTER FIX - Active carriers and MGAs:' as info;
SELECT 
    'Active Carriers: ' || COUNT(*) as count
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
  AND status = 'Active'
UNION ALL
SELECT 
    'Active MGAs: ' || COUNT(*)
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
  AND status = 'Active';

-- 6. Show sample active carriers
SELECT '';
SELECT 'Sample Active Carriers:' as info;
SELECT carrier_name, status
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
  AND status = 'Active'
ORDER BY carrier_name
LIMIT 5;

SELECT '';
SELECT 'Done! Logout and login again to see the changes.' as reminder;