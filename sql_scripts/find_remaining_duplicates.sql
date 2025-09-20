-- FIND REMAINING DUPLICATES - Why do we still have high counts?

-- 1. Total count check
SELECT COUNT(*) as current_total FROM policies;

-- 2. Find duplicate Transaction IDs
SELECT 
    COUNT(*) as duplicate_ids,
    SUM(extra_copies) as total_extra_records
FROM (
    SELECT 
        "Transaction ID",
        COUNT(*) - 1 as extra_copies
    FROM policies
    GROUP BY "Transaction ID"
    HAVING COUNT(*) > 1
) dup;

-- 3. Show specific duplicates
SELECT 
    "Transaction ID",
    COUNT(*) as copies,
    STRING_AGG(DISTINCT "Customer", ' | ') as customers,
    STRING_AGG(DISTINCT "Policy Number", ' | ') as policies
FROM policies
GROUP BY "Transaction ID"
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 4. Check Perfect Lanais LLC specifically
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Transaction Type",
    updated_at
FROM policies
WHERE "Customer" = 'Perfect Lanais LLC'
ORDER BY "Transaction ID", updated_at;

-- 5. Are these true duplicates or different transactions?
WITH potential_duplicates AS (
    SELECT 
        "Customer",
        "Policy Number",
        "Transaction Type",
        "Effective Date",
        "Premium Sold",
        COUNT(*) as count,
        STRING_AGG(DISTINCT "Transaction ID", ', ') as transaction_ids
    FROM policies
    WHERE "Customer" = 'Perfect Lanais LLC'
    GROUP BY "Customer", "Policy Number", "Transaction Type", "Effective Date", "Premium Sold"
)
SELECT * FROM potential_duplicates
WHERE count > 1;