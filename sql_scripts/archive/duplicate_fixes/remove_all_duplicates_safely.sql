-- SAFE REMOVAL OF ALL DUPLICATE TRANSACTION IDS
-- This will keep only one copy of each Transaction ID

-- 1. First, let's see exactly what we'll remove
WITH duplicates AS (
    SELECT 
        _id,
        "Transaction ID",
        "Customer",
        ROW_NUMBER() OVER (PARTITION BY "Transaction ID" ORDER BY _id) as rn
    FROM policies
)
SELECT 
    'Will remove:' as action,
    COUNT(*) as count
FROM duplicates
WHERE rn > 1;

-- 2. Show the breakdown
WITH duplicate_counts AS (
    SELECT 
        "Transaction ID",
        COUNT(*) as copies
    FROM policies
    GROUP BY "Transaction ID"
    HAVING COUNT(*) > 1
)
SELECT 
    copies as number_of_copies,
    COUNT(*) as transaction_ids_with_this_many
FROM duplicate_counts
GROUP BY copies
ORDER BY copies;

-- 3. Remove ALL duplicates (keeping first of each Transaction ID)
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

-- 4. Verify final count
SELECT 
    'Final count after removing all duplicates:' as info,
    COUNT(*) as total_policies
FROM policies;

-- 5. Confirm no duplicates remain
SELECT 
    'Remaining duplicates:' as check,
    COUNT(*) as count
FROM (
    SELECT "Transaction ID"
    FROM policies
    GROUP BY "Transaction ID"
    HAVING COUNT(*) > 1
) dup;