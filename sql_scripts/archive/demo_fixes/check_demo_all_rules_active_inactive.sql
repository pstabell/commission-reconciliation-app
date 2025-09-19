-- CHECK ALL COMMISSION RULES FOR DEMO USER (ACTIVE AND INACTIVE)

-- 1. Total count including inactive rules
SELECT 'COMMISSION RULES STATUS BREAKDOWN:' as section;
SELECT 
    CASE 
        WHEN is_active = true THEN 'Active Rules'
        WHEN is_active = false THEN 'Inactive Rules'
        WHEN is_active IS NULL THEN 'NULL Status Rules'
    END as status,
    COUNT(*) as count
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY is_active
ORDER BY is_active DESC NULLS LAST;

-- 2. Total count regardless of status
SELECT '';
SELECT 'Total Rules (Active + Inactive + NULL):' as description, COUNT(*) as count
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 3. Check if there are rules without is_active flag set
SELECT '';
SELECT 'Rules with NULL is_active flag:' as description, COUNT(*) as count
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND is_active IS NULL;

-- 4. List inactive rules if any
SELECT '';
SELECT 'INACTIVE RULES DETAILS (if any):' as section;
SELECT 
    cr.rule_id,
    c.carrier_name,
    COALESCE(m.mga_name, 'NO MGA') as mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.is_active,
    cr.created_at,
    cr.updated_at
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
AND (cr.is_active = false OR cr.is_active IS NULL)
ORDER BY c.carrier_name, m.mga_name;

-- 5. Compare with what we might expect
SELECT '';
SELECT 'EXPECTED VS ACTUAL:' as section;
SELECT 
    'Expected from user statement' as source,
    78 as count
UNION ALL
SELECT 
    'Actually found (all statuses)',
    COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Actually found (active only)',
    COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND is_active = true;

-- 6. Check for duplicates that might have been filtered out
SELECT '';
SELECT 'DUPLICATE CHECK:' as section;
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct') as mga_name,
    cr.policy_type,
    cr.state,
    COUNT(*) as duplicate_count
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY c.carrier_name, m.mga_name, cr.policy_type, cr.state
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, c.carrier_name;