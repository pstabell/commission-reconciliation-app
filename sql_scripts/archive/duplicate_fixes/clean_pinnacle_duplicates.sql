-- Clean up Pinnacle/Orion duplicates

-- 1. Check current total
SELECT COUNT(*) as current_total FROM policies;

-- 2. Look at the specific duplicates
SELECT 
    _id,
    "Client ID",
    "Transaction ID",
    "Customer",
    "Policy Number",
    updated_at
FROM policies
WHERE "Policy Number" = '3AA823427'
ORDER BY "Transaction ID", _id;

-- 3. Remove duplicates keeping the edited version
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
                        WHEN "Customer" = 'Pinnacle Investments LLC' THEN 0  -- Keep edited version
                        ELSE 1
                    END,
                    _id
            ) as rn
        FROM policies
        WHERE "Policy Number" = '3AA823427'
    ) ranked
    WHERE rn > 1
)
DELETE FROM policies
WHERE _id IN (SELECT _id FROM duplicates_to_remove);

-- 4. Remove ANY other duplicates from this session
WITH all_duplicates AS (
    SELECT _id
    FROM (
        SELECT 
            _id,
            "Transaction ID",
            ROW_NUMBER() OVER (
                PARTITION BY "Transaction ID" 
                ORDER BY _id
            ) as rn
        FROM policies
    ) ranked
    WHERE rn > 1
)
DELETE FROM policies
WHERE _id IN (SELECT _id FROM all_duplicates);

-- 5. Final count - should be back to 425
SELECT COUNT(*) as final_count FROM policies;

-- 6. Verify the edit was preserved
SELECT 
    "Transaction ID",
    "Customer"
FROM policies
WHERE "Policy Number" = '3AA823427'
ORDER BY "Transaction ID";