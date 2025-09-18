-- FIX USER_EMAIL FOR DEMO CARRIERS AND MGAS
-- This script assigns the demo user email to carriers and MGAs that have NULL user_email

-- First, let's check the current state
SELECT 'BEFORE UPDATE - Carriers without user_email:' as status;
SELECT COUNT(*) as null_user_email_count FROM carriers WHERE user_email IS NULL;

SELECT 'BEFORE UPDATE - MGAs without user_email:' as status;
SELECT COUNT(*) as null_user_email_count FROM mgas WHERE user_email IS NULL;

-- Update carriers with NULL user_email to demo user
-- This assumes these are shared/demo carriers that should be visible to the demo user
UPDATE carriers 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE user_email IS NULL;

-- Update MGAs with NULL user_email to demo user
UPDATE mgas 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE user_email IS NULL;

-- Verify the updates
SELECT 'AFTER UPDATE - Demo user carriers:' as status;
SELECT COUNT(*) as demo_carrier_count 
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

SELECT 'AFTER UPDATE - Demo user MGAs:' as status;
SELECT COUNT(*) as demo_mga_count 
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- Show sample of updated carriers
SELECT 'Sample carriers for demo user:' as status;
SELECT carrier_name, user_email 
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 20;

-- Show sample of updated MGAs
SELECT 'Sample MGAs for demo user:' as status;
SELECT mga_name, user_email 
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY mga_name
LIMIT 20;

-- Also check carrier-MGA relationships that might need user_email
SELECT 'Checking carrier_mga_relationships table structure:' as status;
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'carrier_mga_relationships'
AND column_name = 'user_email';