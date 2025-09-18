-- DELETE OLD DEMO DATA AND IMPORT NEW
-- Run this in PRODUCTION Supabase after getting export from private

-- 1. Delete existing demo data
DELETE FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com';
DELETE FROM carrier_mga_relationships WHERE user_email = 'Demo@AgentCommissionTracker.com';
DELETE FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com';
DELETE FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Verify deletion
SELECT 'After deletion:' as status;
SELECT 'Carriers: ' || COUNT(*) as remaining FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 'MGAs: ' || COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 'Rules: ' || COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 3. PASTE YOUR CARRIER INSERT STATEMENTS HERE
-- Example format:
-- INSERT INTO carriers (carrier_name, naic_code, producer_code, status, notes, user_email) VALUES ('Citizens', NULL, NULL, 'Active', NULL, 'Demo@AgentCommissionTracker.com');

-- 4. PASTE YOUR MGA INSERT STATEMENTS HERE
-- Example format:
-- INSERT INTO mgas (mga_name, status, notes, user_email) VALUES ('Direct Appointment', 'Active', NULL, 'Demo@AgentCommissionTracker.com');

-- 5. Verify import
SELECT 'After import:' as status;
SELECT 'Carriers: ' || COUNT(*) as imported FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 'MGAs: ' || COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com';