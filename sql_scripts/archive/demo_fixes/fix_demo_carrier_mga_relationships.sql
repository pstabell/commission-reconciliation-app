-- FIX USER_EMAIL FOR DEMO CARRIER-MGA RELATIONSHIPS
-- Run this after fixing carriers and MGAs user_email

-- First check if the carrier_mga_relationships table has a user_email column
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'carrier_mga_relationships'
ORDER BY ordinal_position;

-- If it has a user_email column, update relationships for demo carriers/MGAs
-- This query will only run if both the carrier and MGA belong to the demo user
UPDATE carrier_mga_relationships cmr
SET user_email = 'Demo@AgentCommissionTracker.com'
FROM carriers c, mgas m
WHERE cmr.carrier_id = c.carrier_id
  AND cmr.mga_id = m.mga_id
  AND c.user_email = 'Demo@AgentCommissionTracker.com'
  AND m.user_email = 'Demo@AgentCommissionTracker.com'
  AND (cmr.user_email IS NULL OR cmr.user_email != 'Demo@AgentCommissionTracker.com');

-- Verify the relationships
SELECT 'Carrier-MGA relationships for demo user:' as status;
SELECT 
    c.carrier_name,
    m.mga_name,
    cmr.is_direct,
    cmr.user_email
FROM carrier_mga_relationships cmr
JOIN carriers c ON cmr.carrier_id = c.carrier_id
JOIN mgas m ON cmr.mga_id = m.mga_id
WHERE c.user_email = 'Demo@AgentCommissionTracker.com'
   OR m.user_email = 'Demo@AgentCommissionTracker.com'
   OR cmr.user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY c.carrier_name, m.mga_name
LIMIT 20;