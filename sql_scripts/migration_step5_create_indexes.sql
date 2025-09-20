-- STEP 5: Create indexes for performance
-- Run this last

CREATE INDEX IF NOT EXISTS idx_policies_user_id ON policies(user_id);
CREATE INDEX IF NOT EXISTS idx_carriers_user_id ON carriers(user_id);
CREATE INDEX IF NOT EXISTS idx_mgas_user_id ON mgas(user_id);
CREATE INDEX IF NOT EXISTS idx_commission_rules_user_id ON commission_rules(user_id);
CREATE INDEX IF NOT EXISTS idx_reconciliations_user_id ON reconciliations(user_id);
CREATE INDEX IF NOT EXISTS idx_carrier_mga_relationships_user_id ON carrier_mga_relationships(user_id);

-- Final verification
SELECT 
    u.id as user_id,
    u.email,
    COUNT(DISTINCT p."Transaction ID") as total_policies
FROM users u
LEFT JOIN policies p ON p.user_id = u.id
WHERE u.email = 'demo@agentcommissiontracker.com'
GROUP BY u.id, u.email;