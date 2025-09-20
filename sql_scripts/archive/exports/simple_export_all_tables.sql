-- SIMPLE EXPORT OF ALL DATA

-- 1. Export all carriers
SELECT 'CARRIERS TABLE:' as info;
SELECT * FROM carriers ORDER BY created_at;

-- 2. Export all MGAs
SELECT '';
SELECT 'MGAS TABLE:' as info;
SELECT * FROM mgas ORDER BY created_at;

-- 3. Export all active commission rules
SELECT '';
SELECT 'COMMISSION RULES TABLE:' as info;
SELECT * FROM commission_rules 
WHERE is_active = true 
ORDER BY carrier_id, mga_id, rule_priority;