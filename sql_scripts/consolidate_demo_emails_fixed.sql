-- CONSOLIDATE ALL DEMO DATA TO LOWERCASE EMAIL
-- This script fixes the data split between different email cases
-- Run this ONCE to consolidate all demo data

-- First, show what we're about to update
SELECT 'BEFORE UPDATE - policies table:' as status;
SELECT user_email, COUNT(*) as record_count
FROM policies 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
GROUP BY user_email
ORDER BY user_email;

-- Update all mixed-case emails to lowercase in all tables
UPDATE policies 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

UPDATE carriers 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

UPDATE mgas 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

UPDATE commission_rules 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Only update these tables if they have user_email column
-- (Some might not have it)
UPDATE reconciliations 
SET user_email = 'demo@agentcommissiontracker.com'
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Verify the consolidation
SELECT 'AFTER UPDATE - policies table:' as status;
SELECT user_email, COUNT(*) as record_count
FROM policies 
WHERE LOWER(user_email) = 'demo@agentcommissiontracker.com'
GROUP BY user_email;

-- Show counts from other tables
SELECT 'Carriers:' as table_name, COUNT(*) as count FROM carriers WHERE user_email = 'demo@agentcommissiontracker.com'
UNION ALL
SELECT 'MGAs:' as table_name, COUNT(*) as count FROM mgas WHERE user_email = 'demo@agentcommissiontracker.com'
UNION ALL  
SELECT 'Commission Rules:' as table_name, COUNT(*) as count FROM commission_rules WHERE user_email = 'demo@agentcommissiontracker.com';

-- Expected result: Only one row with demo@agentcommissiontracker.com and total count of 466 in policies table