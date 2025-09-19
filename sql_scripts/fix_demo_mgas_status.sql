-- FIX DEMO MGAS STATUS

-- 1. Check current MGA status values
SELECT 'CURRENT MGA STATUS:' as info;
SELECT status, COUNT(*) as count
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status;

-- 2. Update any non-Active MGAs to Active
UPDATE mgas
SET status = 'Active'
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND (status IS NULL OR status != 'Active');

-- 3. Verify the fix
SELECT '';
SELECT 'AFTER UPDATE:' as info;
SELECT COUNT(*) as active_mgas
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND status = 'Active';

-- 4. Show all MGAs
SELECT '';
SELECT 'ALL DEMO MGAS NOW:' as info;
SELECT mga_name, status
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY mga_name;