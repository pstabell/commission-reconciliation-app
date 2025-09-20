-- CONSOLIDATE ALL DEMO DATA TO LOWERCASE EMAIL
-- This script fixes the data split between different email cases
-- Run this ONCE to consolidate all demo data

-- First, show what we're about to update
SELECT user_email, COUNT(*) as record_count
FROM policies 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
GROUP BY user_email
ORDER BY user_email;

-- Update all mixed-case emails to lowercase
UPDATE policies 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Also update any other tables with user_email
UPDATE carriers 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

UPDATE mgas 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

UPDATE carrier_commission_rules 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

UPDATE reconciliation_history 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

UPDATE report_templates 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Verify the consolidation
SELECT 'After update:' as status;
SELECT user_email, COUNT(*) as record_count
FROM policies 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
GROUP BY user_email;

-- Expected result: Only one row with demo@agentcommissiontracker.com and total count of 466