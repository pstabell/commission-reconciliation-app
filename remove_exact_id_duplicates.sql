-- REMOVE EXACT TRANSACTION ID DUPLICATES
-- This will remove records with identical Transaction IDs

-- 1. Find Transaction IDs that appear more than once
WITH duplicate_ids AS (
    SELECT 
        "Transaction ID",
        COUNT(*) as occurrences
    FROM policies
    GROUP BY "Transaction ID"
    HAVING COUNT(*) > 1
)
SELECT 
    COUNT(*) as duplicate_transaction_ids,
    SUM(occurrences - 1) as records_to_remove
FROM duplicate_ids;

-- 2. Show examples of duplicate Transaction IDs
SELECT 
    "Transaction ID",
    COUNT(*) as occurrences,
    STRING_AGG(DISTINCT "Customer", '; ') as customers,
    STRING_AGG(DISTINCT "Policy Number", '; ') as policies
FROM policies
GROUP BY "Transaction ID"
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC
LIMIT 10;

-- 3. For each duplicate Transaction ID, keep only one (the one with lowest _id)
WITH duplicates_to_remove AS (
    SELECT _id
    FROM (
        SELECT 
            _id,
            "Transaction ID",
            ROW_NUMBER() OVER (PARTITION BY "Transaction ID" ORDER BY _id) as rn
        FROM policies
    ) ranked
    WHERE rn > 1
)
SELECT COUNT(*) as will_remove FROM duplicates_to_remove;

-- 4. REMOVE DUPLICATE TRANSACTION IDS (keeping the first one)
WITH duplicates_to_remove AS (
    SELECT _id
    FROM (
        SELECT 
            _id,
            "Transaction ID",
            ROW_NUMBER() OVER (PARTITION BY "Transaction ID" ORDER BY _id) as rn
        FROM policies
    ) ranked
    WHERE rn > 1
)
DELETE FROM policies
WHERE _id IN (SELECT _id FROM duplicates_to_remove);

-- 5. Verify no more duplicate Transaction IDs exist
SELECT 
    "Transaction ID",
    COUNT(*) as count
FROM policies
GROUP BY "Transaction ID"
HAVING COUNT(*) > 1;

-- 6. Check final count
SELECT COUNT(*) as final_count FROM policies;