-- Count active vs inactive rules in PRIVATE database
SELECT 'RULE COUNTS:' as info;
SELECT 
    COUNT(*) as total_rules,
    SUM(CASE WHEN is_active = true THEN 1 ELSE 0 END) as active_rules,
    SUM(CASE WHEN is_active = false THEN 1 ELSE 0 END) as inactive_rules,
    SUM(CASE WHEN is_active IS NULL THEN 1 ELSE 0 END) as null_active_rules
FROM commission_rules;

-- Check rules with missing carriers
SELECT '';
SELECT 'RULES WITH MISSING CARRIERS:' as info;
SELECT 
    cr.rule_id,
    cr.carrier_id,
    cr.is_active,
    CASE 
        WHEN c.carrier_id IS NULL THEN 'CARRIER NOT FOUND'
        ELSE c.carrier_name 
    END as carrier_status
FROM commission_rules cr
LEFT JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE c.carrier_id IS NULL;

-- Count rules by active status and carrier presence
SELECT '';
SELECT 'EXPORTABLE RULES:' as info;
SELECT 
    COUNT(*) as total_exportable_rules
FROM commission_rules cr
INNER JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE cr.is_active = true OR cr.is_active IS NULL;