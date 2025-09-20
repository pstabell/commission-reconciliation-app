-- Remove TRUE duplicate transactions keeping only the oldest one

-- 1. First, let's see what we're going to delete
WITH duplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC  -- Keep the oldest
        ) as rn
    FROM policies
)
SELECT 'Transactions to delete:' as check;
SELECT COUNT(*) as will_delete
FROM duplicates
WHERE rn > 1;

-- 2. Show sample of what will be deleted
WITH duplicates AS (
    SELECT 
        "Transaction ID",
        "Customer",
        "Policy Number",
        "Transaction Type",
        updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Transaction Type",
    updated_at,
    'WILL DELETE' as status
FROM duplicates
WHERE rn > 1
ORDER BY "Customer", "Policy Number"
LIMIT 20;

-- 3. DELETE duplicates keeping the oldest of each group
WITH duplicates AS (
    SELECT 
        _id,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
DELETE FROM policies
WHERE _id IN (
    SELECT _id 
    FROM duplicates 
    WHERE rn > 1
);

-- 4. Verify final count
SELECT 'Final count after cleanup:' as check;
SELECT COUNT(*) as total_policies FROM policies;

-- 5. Verify no more duplicates exist
SELECT 'Remaining duplicates:' as check;
SELECT 
    "Customer",
    "Policy Number", 
    "Transaction Type",
    COUNT(*) as count
FROM policies
GROUP BY "Customer", "Policy Number", "Transaction Type"
HAVING COUNT(*) > 1
ORDER BY count DESC
LIMIT 5;