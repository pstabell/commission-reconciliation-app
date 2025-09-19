-- ADD MISSING BURLINGTON AND BURNS & WILCOX NOW

-- 1. Add Burlington carrier (it was in our list but somehow didn't import)
INSERT INTO carriers (carrier_id, carrier_name, status, user_email, created_at, updated_at)
VALUES (
    gen_random_uuid(),
    'Burlington',
    'Active',
    'Demo@AgentCommissionTracker.com',
    NOW(),
    NOW()
)
ON CONFLICT DO NOTHING;

-- 2. Add Burns & Wilcox MGA (existed since July but we missed it)
INSERT INTO mgas (mga_id, mga_name, status, user_email, created_at, updated_at)
VALUES (
    '5ffaad29-3891-4cbc-a933-ce4aa6d558cf',  -- Using same ID from private
    'Burns & Wilcox',
    'Active',
    'Demo@AgentCommissionTracker.com',
    NOW(),
    NOW()
)
ON CONFLICT (mga_id) DO UPDATE 
SET user_email = 'Demo@AgentCommissionTracker.com',
    status = 'Active';

-- 3. Show results
SELECT 'FINAL DEMO TOTALS:' as info;
SELECT 
    (SELECT COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com') as carriers,
    (SELECT COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com') as mgas,
    (SELECT COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com') as rules;

-- 4. Verify they exist
SELECT '';
SELECT 'BURLINGTON:' as check, COUNT(*) as found 
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com' AND carrier_name = 'Burlington'
UNION ALL
SELECT 'BURNS & WILCOX:', COUNT(*) 
FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com' AND mga_name = 'Burns & Wilcox';