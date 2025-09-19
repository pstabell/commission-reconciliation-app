-- COMPARE PRIVATE TO DEMO DATABASES

-- Run this in PRODUCTION database to see what's missing

-- 1. What demo has
SELECT 'DEMO CURRENT TOTALS:' as info;
SELECT 
    (SELECT COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com') as carriers,
    (SELECT COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com') as mgas,
    (SELECT COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com') as rules;

-- 2. Check for specific missing items
SELECT '';
SELECT 'MISSING BURLINGTON?' as info;
SELECT COUNT(*) as found FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com' 
AND carrier_name = 'Burlington';

SELECT '';
SELECT 'MISSING BURNS & WILCOX?' as info;
SELECT COUNT(*) as found FROM mgas 
WHERE user_email = 'Demo@AgentCommissionTracker.com' 
AND mga_name = 'Burns & Wilcox';

-- 3. Add Burns & Wilcox with the exact same ID from private
INSERT INTO mgas (mga_id, mga_name, status, user_email, created_at, updated_at)
VALUES (
    '5ffaad29-3891-4cbc-a933-ce4aa6d558cf',
    'Burns & Wilcox',
    'Active', 
    'Demo@AgentCommissionTracker.com',
    '2025-07-13 04:45:26.432557+00',
    '2025-07-13 04:45:26.432557+00'
)
ON CONFLICT (mga_id) DO NOTHING;

-- 4. Verify after insert
SELECT '';
SELECT 'AFTER INSERT - NEW TOTALS:' as info;
SELECT 
    (SELECT COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com') as carriers,
    (SELECT COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com') as mgas;