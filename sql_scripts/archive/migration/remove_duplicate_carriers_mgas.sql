-- REMOVE DUPLICATE CARRIERS AND MGAS
-- Run this after discovering the hidden data

-- 1. Show duplicate carriers (same name)
SELECT 'Duplicate Carriers:' as check;
SELECT 
    carrier_name,
    COUNT(*) as copies,
    STRING_AGG(carrier_id::text, ', ') as carrier_ids,
    STRING_AGG(created_at::text, ', ') as created_dates
FROM carriers
GROUP BY carrier_name
HAVING COUNT(*) > 1
ORDER BY carrier_name;

-- 2. Show duplicate MGAs
SELECT 'Duplicate MGAs:' as check;
SELECT 
    mga_name,
    COUNT(*) as copies,
    STRING_AGG(mga_id::text, ', ') as mga_ids,
    STRING_AGG(created_at::text, ', ') as created_dates
FROM mgas
GROUP BY mga_name
HAVING COUNT(*) > 1
ORDER BY mga_name;

-- 3. Delete the newer duplicates (keep the original ones)
-- This keeps the older records which likely have relationships
WITH duplicates AS (
    SELECT 
        carrier_id,
        carrier_name,
        created_at,
        ROW_NUMBER() OVER (PARTITION BY carrier_name ORDER BY created_at) as rn
    FROM carriers
)
DELETE FROM carriers
WHERE carrier_id IN (
    SELECT carrier_id 
    FROM duplicates 
    WHERE rn > 1
);

-- 4. Same for MGAs
WITH duplicates AS (
    SELECT 
        mga_id,
        mga_name,
        created_at,
        ROW_NUMBER() OVER (PARTITION BY mga_name ORDER BY created_at) as rn
    FROM mgas
)
DELETE FROM mgas
WHERE mga_id IN (
    SELECT mga_id 
    FROM duplicates 
    WHERE rn > 1
);

-- 5. Now fix the commission rules that might reference the deleted duplicate IDs
-- First, show orphaned commission rules
SELECT 'Orphaned Commission Rules (before fix):' as check;
SELECT 
    cr.rule_id,
    cr.user_email,
    cr.new_rate,
    cr.renewal_rate
FROM commission_rules cr
WHERE cr.carrier_id NOT IN (SELECT carrier_id FROM carriers)
   OR (cr.mga_id IS NOT NULL AND cr.mga_id NOT IN (SELECT mga_id FROM mgas));

-- 6. Fix orphaned commission rules by updating to correct carrier/mga IDs
-- Update commission rules to use the remaining carrier IDs
UPDATE commission_rules cr
SET carrier_id = c.carrier_id
FROM carriers c
WHERE cr.carrier_id NOT IN (SELECT carrier_id FROM carriers)
  AND c.carrier_name = (
      -- Try to match by the original carrier name
      SELECT carrier_name 
      FROM carriers 
      WHERE carrier_id = cr.carrier_id 
      LIMIT 1
  );

-- 7. Verify final state
SELECT 'Final Status:' as check;
SELECT 'Total Carriers:' as item, COUNT(*) as count FROM carriers
UNION ALL
SELECT 'Total MGAs:' as item, COUNT(*) as count FROM mgas
UNION ALL
SELECT 'Total Commission Rules:' as item, COUNT(*) as count FROM commission_rules
UNION ALL
SELECT 'Demo User Rules:' as item, COUNT(*) as count 
FROM commission_rules 
WHERE user_email = 'Demo@AgentCommissionTracker.com'
ORDER BY item;

-- 8. Show remaining carriers
SELECT 'Clean Carrier List:' as info;
SELECT carrier_name, created_at FROM carriers ORDER BY carrier_name;