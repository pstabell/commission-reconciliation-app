-- CHECK DEMO USER COMMISSION RULES COUNT AND DETAILS

-- 1. Total count of commission rules for demo user
SELECT 'Total Commission Rules for Demo User' as description, COUNT(*) as count
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Count by carrier
SELECT '';
SELECT 'Commission Rules Count by Carrier:' as section;
SELECT 
    c.carrier_name,
    COUNT(cr.rule_id) as rule_count
FROM carriers c
LEFT JOIN commission_rules cr ON c.carrier_id = cr.carrier_id AND cr.user_email = 'Demo@AgentCommissionTracker.com'
WHERE c.user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY c.carrier_name
ORDER BY rule_count DESC, c.carrier_name;

-- 3. Count by MGA
SELECT '';
SELECT 'Commission Rules Count by MGA:' as section;
SELECT 
    COALESCE(m.mga_name, 'NO MGA') as mga_name,
    COUNT(cr.rule_id) as rule_count
FROM commission_rules cr
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY m.mga_name
ORDER BY rule_count DESC;

-- 4. Rules with NULL MGA
SELECT '';
SELECT 'Rules with NULL MGA:' as section;
SELECT COUNT(*) as count
FROM commission_rules
WHERE user_email = 'Demo@AgentCommissionTracker.com' 
AND mga_id IS NULL;

-- 5. Detailed list of all rules
SELECT '';
SELECT 'All Commission Rules Details:' as section;
SELECT 
    cr.rule_id,
    c.carrier_name,
    COALESCE(m.mga_name, 'NO MGA') as mga_name,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.rule_description
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY c.carrier_name, m.mga_name;

-- 6. Check for any orphaned rules (rules pointing to non-existent carriers)
SELECT '';
SELECT 'Orphaned Rules Check:' as section;
SELECT COUNT(*) as orphaned_rules
FROM commission_rules cr
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
AND NOT EXISTS (
    SELECT 1 FROM carriers c 
    WHERE c.carrier_id = cr.carrier_id 
    AND c.user_email = 'Demo@AgentCommissionTracker.com'
);

-- 7. Summary counts
SELECT '';
SELECT 'SUMMARY:' as section;
SELECT 
    (SELECT COUNT(*) FROM carriers WHERE user_email = 'Demo@AgentCommissionTracker.com') as total_carriers,
    (SELECT COUNT(*) FROM mgas WHERE user_email = 'Demo@AgentCommissionTracker.com') as total_mgas,
    (SELECT COUNT(*) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com') as total_rules,
    (SELECT COUNT(DISTINCT carrier_id) FROM commission_rules WHERE user_email = 'Demo@AgentCommissionTracker.com') as carriers_with_rules;