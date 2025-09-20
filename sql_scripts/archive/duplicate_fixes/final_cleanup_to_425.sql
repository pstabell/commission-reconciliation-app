-- FINAL CLEANUP - Remove ALL duplicates and get back to 425 records

-- 1. Current count
SELECT 'BEFORE:' as status, COUNT(*) as total_records FROM policies;

-- 2. Remove all duplicate Transaction IDs, keeping only the first one
WITH duplicates_to_remove AS (
    SELECT _id
    FROM (
        SELECT 
            _id,
            "Transaction ID",
            ROW_NUMBER() OVER (
                PARTITION BY "Transaction ID" 
                ORDER BY 
                    -- Keep edited versions first
                    CASE 
                        WHEN "Customer" IN ('Katie Oyster', 'Lee Hopper', 'Pinnacle Investments LLC') THEN 0
                        ELSE 1
                    END,
                    _id
            ) as rn
        FROM policies
    ) ranked
    WHERE rn > 1
)
DELETE FROM policies
WHERE _id IN (SELECT _id FROM duplicates_to_remove);

-- 3. Final count - should be 425
SELECT 'AFTER:' as status, COUNT(*) as final_count FROM policies;

-- 4. Verify no duplicates remain
SELECT 
    'DUPLICATES REMAINING:' as check,
    COUNT(*) as duplicate_count
FROM (
    SELECT "Transaction ID"
    FROM policies
    GROUP BY "Transaction ID"
    HAVING COUNT(*) > 1
) dup;

-- 5. Show your edited records
SELECT 
    "Customer",
    "Policy Number",
    "Transaction ID"
FROM policies
WHERE "Customer" IN ('Katie Oyster', 'Lee Hopper', 'Pinnacle Investments LLC')
ORDER BY "Customer";