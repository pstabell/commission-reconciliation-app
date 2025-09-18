-- COUNT ALL DATA IN PRODUCTION DATABASE
-- Run this in your PRODUCTION Supabase to get exact counts

-- 1. Count total active rules
SELECT 'TOTAL ACTIVE COMMISSION RULES:' as info, COUNT(*) as count
FROM commission_rules
WHERE is_active = true;

-- 2. Count total carriers (all statuses)
SELECT 'TOTAL CARRIERS:' as info, COUNT(*) as count
FROM carriers;

-- 3. Count total MGAs (all statuses)
SELECT 'TOTAL MGAS:' as info, COUNT(*) as count
FROM mgas;

-- 4. Count unique carrier names from commission rules
SELECT 'UNIQUE CARRIERS IN RULES:' as info, COUNT(DISTINCT c.carrier_name) as count
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
WHERE cr.is_active = true;

-- 5. Count unique MGA names from commission rules
SELECT 'UNIQUE MGAS IN RULES:' as info, COUNT(DISTINCT m.mga_name) as count
FROM commission_rules cr
JOIN mgas m ON cr.mga_id = m.mga_id
WHERE cr.is_active = true;