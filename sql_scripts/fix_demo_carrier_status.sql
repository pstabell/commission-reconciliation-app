-- Fix carrier status for demo user

-- First, check current status values
SELECT 
    status,
    COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status;

-- Update all carriers to have 'Active' status if they don't have it already
-- (This assumes all carriers should be active by default)
UPDATE carriers
SET status = 'Active'
WHERE user_email = 'Demo@AgentCommissionTracker.com'
    AND (status IS NULL OR status != 'Active');

-- Verify the update
SELECT 
    status,
    COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status;

-- Show sample of updated carriers
SELECT 
    carrier_id,
    carrier_name,
    status,
    created_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 10;