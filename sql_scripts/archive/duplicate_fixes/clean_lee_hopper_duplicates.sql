-- Clean up Lee Hopper duplicates and all others

-- 1. Quick check of what we have
SELECT COUNT(*) as current_total FROM policies;

-- 2. Remove ALL duplicates, keeping the edited version where possible
WITH duplicates_to_remove AS (
    SELECT _id
    FROM (
        SELECT _id,
               "Transaction ID",
               ROW_NUMBER() OVER (
                   PARTITION BY "Transaction ID" 
                   ORDER BY 
                       CASE 
                           WHEN "Customer" = 'Lee Hopper' THEN 0  -- Keep the edited version
                           WHEN "Customer" LIKE '%Oyster%' THEN 0  -- Keep previous edits too
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

-- 3. Final count - should be back to 425
SELECT COUNT(*) as final_count FROM policies;

-- 4. Verify Lee Hopper records
SELECT 
    _id,
    "Transaction ID",
    "Customer",
    updated_at
FROM policies
WHERE "Policy Number" = 'GD0031606030'
ORDER BY "Transaction ID";