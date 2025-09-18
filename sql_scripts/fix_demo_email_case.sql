-- FIX: Update all demo emails to match the app's expected case
-- The app expects: Demo@AgentCommissionTracker.com

-- 1. Show what will be updated
SELECT 'ITEMS TO UPDATE:' as info;
SELECT 
    'carriers' as table_name,
    COUNT(*) as count
FROM carriers 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
AND user_email != 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'mgas',
    COUNT(*)
FROM mgas 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
AND user_email != 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'commission_rules',
    COUNT(*)
FROM commission_rules 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
AND user_email != 'Demo@AgentCommissionTracker.com';

-- 2. Update carriers
UPDATE carriers 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
AND user_email != 'Demo@AgentCommissionTracker.com';

-- 3. Update MGAs
UPDATE mgas 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
AND user_email != 'Demo@AgentCommissionTracker.com';

-- 4. Update commission rules
UPDATE commission_rules 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
AND user_email != 'Demo@AgentCommissionTracker.com';

-- 5. Verify the fix
SELECT '';
SELECT 'VERIFICATION AFTER FIX:' as info;
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
AND status = 'Active'
UNION ALL
SELECT 
    'Active Commission Rules: ' || COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND is_active = true;

-- 6. Final instruction
SELECT '';
SELECT 'NEXT STEP:' as action;
SELECT 'Logout and login again as demo@agentcommissiontracker.com' as instruction;