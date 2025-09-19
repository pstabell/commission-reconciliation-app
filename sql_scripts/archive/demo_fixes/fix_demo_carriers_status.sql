-- Fix demo user's carriers status to ensure they show up in the app

-- First, check current status distribution
SELECT 
    'Before Update' as phase,
    status,
    COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY status;

-- Update all demo carriers to have 'Active' status if they don't already
UPDATE carriers 
SET 
    status = 'Active',
    updated_at = NOW()
WHERE 
    user_email = 'Demo@AgentCommissionTracker.com' 
    AND (status IS NULL OR status = '' OR status != 'Active');

-- Also ensure updated_at is set for proper sorting
UPDATE carriers 
SET 
    updated_at = COALESCE(updated_at, created_at, NOW())
WHERE 
    user_email = 'Demo@AgentCommissionTracker.com' 
    AND updated_at IS NULL;

-- Verify the update
SELECT 
    'After Update' as phase,
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
    updated_at
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 10;