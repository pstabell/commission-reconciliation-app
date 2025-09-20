-- Clean up the Katie Oyster duplicates
-- Shows the 4 duplicates and which to keep

-- 1. Show the duplicates
SELECT 
    _id,
    "Client ID",
    "Transaction ID",
    "Customer",
    "Carrier Name",
    "Policy Type",
    "Policy Number",
    "Transaction Type",
    updated_at
FROM policies
WHERE "Policy Number" = '443939914'
ORDER BY updated_at DESC;

-- 2. Delete the duplicates keeping only one of each Transaction ID
WITH duplicates_to_remove AS (
    SELECT _id
    FROM (
        SELECT 
            _id,
            "Transaction ID",
            "Customer",
            ROW_NUMBER() OVER (
                PARTITION BY "Transaction ID" 
                ORDER BY 
                    CASE 
                        WHEN "Customer" = 'Katie Oyster' THEN 0  -- Keep the correctly spelled one
                        WHEN "Customer" = 'Katie Oystor' THEN 1
                        ELSE 2
                    END,
                    _id
            ) as rn
        FROM policies
        WHERE "Policy Number" = '443939914'
    ) ranked
    WHERE rn > 1
)
DELETE FROM policies
WHERE _id IN (SELECT _id FROM duplicates_to_remove);

-- 3. Verify we're back to 2 records for this policy
SELECT COUNT(*) as remaining_count
FROM policies
WHERE "Policy Number" = '443939914';

-- 4. Check total count
SELECT COUNT(*) as total_policies FROM policies;