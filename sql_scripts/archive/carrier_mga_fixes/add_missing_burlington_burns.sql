-- ADD MISSING BURLINGTON CARRIER AND BURNS & WILCOX MGA TO DEMO

-- 1. Add Burlington carrier
INSERT INTO carriers (carrier_id, carrier_name, status, user_email, created_at, updated_at)
VALUES (
    gen_random_uuid(),
    'Burlington',
    'Active',
    'Demo@AgentCommissionTracker.com',
    NOW(),
    NOW()
)
ON CONFLICT (carrier_id) DO NOTHING;

-- 2. Add Burns & Wilcox MGA
INSERT INTO mgas (mga_id, mga_name, status, user_email, created_at, updated_at)
VALUES (
    gen_random_uuid(),
    'Burns & Wilcox',
    'Active',
    'Demo@AgentCommissionTracker.com',
    NOW(),
    NOW()
)
ON CONFLICT (mga_id) DO NOTHING;

-- 3. Verify they were added
SELECT 'VERIFICATION:' as info;
SELECT 'Burlington Carrier' as type, COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND carrier_name = 'Burlington'
UNION ALL
SELECT 'Burns & Wilcox MGA', COUNT(*)
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND mga_name = 'Burns & Wilcox';

-- 4. Show new totals
SELECT '';
SELECT 'NEW TOTALS FOR DEMO:' as info;
SELECT 'Carriers: ' || COUNT(*) as count
FROM carriers
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 'MGAs: ' || COUNT(*)
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com';