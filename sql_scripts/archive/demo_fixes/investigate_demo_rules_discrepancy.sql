-- INVESTIGATE DEMO RULES DISCREPANCY (78 expected vs 63+ found)

-- 1. Count ALL rules regardless of any flags
SELECT 'ALL COMMISSION RULES (no filters):' as description, COUNT(*) as count
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com';

-- 2. Count by various criteria that might filter rules
SELECT '';
SELECT 'RULES BY VARIOUS FILTERS:' as section;
SELECT 
    'Active rules (is_active = true)' as filter,
    COUNT(*) as count
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND is_active = true
UNION ALL
SELECT 
    'Inactive rules (is_active = false)',
    COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND is_active = false
UNION ALL
SELECT 
    'Rules with NULL is_active',
    COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND is_active IS NULL
UNION ALL
SELECT 
    'Rules with state specified',
    COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND state IS NOT NULL
UNION ALL
SELECT 
    'Rules without state',
    COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
AND state IS NULL;

-- 3. Check if there are multiple rules per carrier/MGA combination
SELECT '';
SELECT 'CARRIERS WITH MULTIPLE RULES:' as section;
SELECT 
    c.carrier_name,
    COUNT(DISTINCT cr.rule_id) as rule_count,
    COUNT(DISTINCT COALESCE(m.mga_name, 'Direct')) as mga_variations,
    COUNT(DISTINCT cr.policy_type) as policy_type_variations,
    COUNT(DISTINCT cr.state) as state_variations
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY c.carrier_name
HAVING COUNT(DISTINCT cr.rule_id) > 1
ORDER BY rule_count DESC;

-- 4. Compare carriers that have rules vs total carriers
SELECT '';
SELECT 'CARRIER COVERAGE:' as section;
SELECT 
    'Total carriers for demo user' as description,
    COUNT(*) as count
FROM carriers 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Carriers with at least one rule',
    COUNT(DISTINCT c.carrier_id)
FROM carriers c
WHERE c.user_email = 'Demo@AgentCommissionTracker.com'
AND EXISTS (
    SELECT 1 FROM commission_rules cr 
    WHERE cr.carrier_id = c.carrier_id 
    AND cr.user_email = 'Demo@AgentCommissionTracker.com'
);

-- 5. List all rules with full details
SELECT '';
SELECT 'DETAILED RULE LIST:' as section;
SELECT 
    ROW_NUMBER() OVER (ORDER BY c.carrier_name, m.mga_name) as row_num,
    c.carrier_name,
    COALESCE(m.mga_name, 'NO MGA') as mga_name,
    cr.state,
    cr.policy_type,
    cr.new_rate,
    cr.renewal_rate,
    cr.is_active,
    cr.is_default,
    LEFT(cr.rule_description, 50) as rule_desc_preview
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY c.carrier_name, m.mga_name, cr.policy_type;

-- 6. Check created/updated timestamps
SELECT '';
SELECT 'RULES BY CREATION DATE:' as section;
SELECT 
    DATE(created_at) as created_date,
    COUNT(*) as rules_created
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
GROUP BY DATE(created_at)
ORDER BY created_date DESC;

-- 7. Final summary
SELECT '';
SELECT 'SUMMARY - WHERE ARE THE 78 RULES?' as section;
SELECT 
    'According to user statement' as source,
    78 as expected_count
UNION ALL
SELECT 
    'Found in database (all)',
    COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
UNION ALL
SELECT 
    'Found in import script',
    47
UNION ALL
SELECT 
    'Difference to investigate',
    78 - COUNT(*)
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com';