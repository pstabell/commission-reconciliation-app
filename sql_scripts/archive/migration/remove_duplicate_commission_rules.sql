-- Identify and Remove Duplicate Commission Rules
-- This finds rules with same carrier, mga, policy_type, and rates

-- Step 1: View duplicates before deletion
WITH duplicates AS (
    SELECT 
        carrier_id,
        mga_id,
        policy_type,
        new_rate,
        renewal_rate,
        state,
        COUNT(*) as duplicate_count,
        MIN(created_at) as first_created,
        MAX(created_at) as last_created
    FROM commission_rules
    GROUP BY carrier_id, mga_id, policy_type, new_rate, renewal_rate, state
    HAVING COUNT(*) > 1
)
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct') as mga,
    d.policy_type,
    d.new_rate || '%' as new_rate,
    d.renewal_rate || '%' as renewal_rate,
    d.duplicate_count,
    TO_CHAR(d.first_created, 'MM/DD/YYYY HH24:MI') as first_created,
    TO_CHAR(d.last_created, 'MM/DD/YYYY HH24:MI') as last_created
FROM duplicates d
JOIN carriers c ON d.carrier_id = c.carrier_id
LEFT JOIN mgas m ON d.mga_id = m.mga_id
ORDER BY c.carrier_name, d.policy_type;

-- Step 2: Delete duplicates, keeping only the earliest created rule
WITH duplicates AS (
    SELECT 
        rule_id,
        ROW_NUMBER() OVER (
            PARTITION BY carrier_id, mga_id, policy_type, new_rate, renewal_rate, state 
            ORDER BY created_at ASC
        ) as rn
    FROM commission_rules
)
DELETE FROM commission_rules
WHERE rule_id IN (
    SELECT rule_id 
    FROM duplicates 
    WHERE rn > 1
);

-- Step 3: Verify duplicates are removed
SELECT 
    'Duplicate rules removed:' as action,
    COUNT(*) as count
FROM (
    SELECT 
        carrier_id, mga_id, policy_type, new_rate, renewal_rate, state,
        COUNT(*) as cnt
    FROM commission_rules
    GROUP BY carrier_id, mga_id, policy_type, new_rate, renewal_rate, state
    HAVING COUNT(*) > 1
) dupes;

-- Step 4: Show current rule count
SELECT 
    'Total commission rules after cleanup:' as status,
    COUNT(*) as count
FROM commission_rules;

-- Step 5: Show cleaned up rules for carriers that had duplicates
SELECT 
    c.carrier_name,
    COALESCE(m.mga_name, 'Direct') as mga,
    cr.policy_type,
    cr.new_rate || '%' as new_rate,
    cr.renewal_rate || '%' as renewal_rate,
    TO_CHAR(cr.effective_date, 'MM/DD/YYYY') as effective_date,
    CASE 
        WHEN cr.end_date IS NULL THEN 'Current'
        ELSE TO_CHAR(cr.end_date, 'MM/DD/YYYY')
    END as end_date
FROM commission_rules cr
JOIN carriers c ON cr.carrier_id = c.carrier_id
LEFT JOIN mgas m ON cr.mga_id = m.mga_id
WHERE c.carrier_name IN ('AAA', 'Citizens', 'Progressive')
ORDER BY c.carrier_name, cr.policy_type;