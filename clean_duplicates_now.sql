-- EMERGENCY CLEANUP - Remove all duplicates created at 10:02:08

-- 1. Quick verification of what we'll remove
SELECT COUNT(*) as will_remove
FROM (
    SELECT _id,
           ROW_NUMBER() OVER (PARTITION BY "Transaction ID" ORDER BY 
               CASE 
                   WHEN "Customer" LIKE '%Oyster%' THEN 0  -- Prefer correct spelling
                   ELSE 1
               END,
               _id) as rn
    FROM policies
) ranked
WHERE rn > 1;

-- 2. REMOVE ALL DUPLICATES
WITH duplicates_to_remove AS (
    SELECT _id
    FROM (
        SELECT _id,
               ROW_NUMBER() OVER (PARTITION BY "Transaction ID" ORDER BY 
                   CASE 
                       WHEN "Customer" LIKE '%Oyster%' THEN 0  -- Keep correct spelling
                       ELSE 1
                   END,
                   _id) as rn
        FROM policies
    ) ranked
    WHERE rn > 1
)
DELETE FROM policies
WHERE _id IN (SELECT _id FROM duplicates_to_remove);

-- 3. Final count
SELECT COUNT(*) as final_count FROM policies;