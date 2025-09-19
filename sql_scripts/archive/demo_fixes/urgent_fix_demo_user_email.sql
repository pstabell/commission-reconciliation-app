-- URGENT FIX: Set user_email for all demo data

-- 1. Check current status
SELECT 'BEFORE FIX - Demo user data:' as status;
SELECT 
    'Carriers with Demo email: ' || COUNT(*) as count
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Carriers with NULL email: ' || COUNT(*)
FROM carriers 
WHERE user_email IS NULL;

-- 2. Update all NULL user_emails to Demo account
UPDATE carriers 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE user_email IS NULL;

UPDATE mgas 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE user_email IS NULL;

UPDATE commission_rules 
SET user_email = 'Demo@AgentCommissionTracker.com'
WHERE user_email IS NULL;

-- 3. Also update carrier_mga_relationships if it has user_email column
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'carrier_mga_relationships' 
        AND column_name = 'user_email'
    ) THEN
        UPDATE carrier_mga_relationships 
        SET user_email = 'Demo@AgentCommissionTracker.com'
        WHERE user_email IS NULL;
    END IF;
END $$;

-- 4. Verify the fix
SELECT '';
SELECT 'AFTER FIX - Demo user now has:' as status;
SELECT 
    'Carriers: ' || COUNT(*) as count
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'MGAs: ' || COUNT(*)
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Commission Rules: ' || COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 5. Show sample data
SELECT '';
SELECT 'Sample carriers:' as info;
SELECT carrier_name 
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY carrier_name
LIMIT 5;

SELECT '';
SELECT 'IMPORTANT: After running this, the demo user needs to LOGOUT and LOGIN again to see the changes!' as reminder;