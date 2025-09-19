-- ALSO ADD BURNS & WILCOX MGA
-- Run this AFTER the carrier fix

-- Add Burns & Wilcox since it exists in your private database
INSERT INTO mgas (mga_id, mga_name, status, user_email, created_at, updated_at)
VALUES (
    '5ffaad29-3891-4cbc-a933-ce4aa6d558cf',
    'Burns & Wilcox',
    'Active',
    'Demo@AgentCommissionTracker.com',
    NOW(),
    NOW()
)
ON CONFLICT (mga_id) DO UPDATE 
SET user_email = 'Demo@AgentCommissionTracker.com',
    status = 'Active';

-- Verify
SELECT 'BURNS & WILCOX ADDED:' as info;
SELECT mga_name, status
FROM mgas
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND mga_name = 'Burns & Wilcox';

-- Final counts
SELECT '';
SELECT 'FINAL CORRECT TOTALS:' as info;
SELECT 
    (SELECT COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com') || ' carriers (including Burlington)' as carriers,
    (SELECT COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com') || ' MGAs (including Burns & Wilcox)' as mgas;