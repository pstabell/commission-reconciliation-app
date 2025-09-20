-- CAREFUL DUPLICATE ANALYSIS
-- We need to understand why removing duplicates would drop count to 366 instead of 425

-- 1. What's our starting point?
SELECT 
    COUNT(*) as current_total,
    COUNT(DISTINCT "Transaction ID") as unique_transaction_ids
FROM policies;

-- 2. Look for EXACT duplicates (same Transaction ID)
SELECT 
    "Transaction ID",
    COUNT(*) as occurrences
FROM policies
GROUP BY "Transaction ID"
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC
LIMIT 10;

-- 3. Check if we have transactions with DIFFERENT IDs but same details
WITH potential_duplicates AS (
    SELECT 
        "Customer",
        "Policy Number",
        "Transaction Type",
        "Premium Sold",
        "Effective Date",
        COUNT(*) as group_count,
        COUNT(DISTINCT "Transaction ID") as unique_ids,
        STRING_AGG(DISTINCT "Transaction ID", ', ' ORDER BY "Transaction ID") as transaction_ids
    FROM policies
    GROUP BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
    HAVING COUNT(*) > 1
)
SELECT * FROM potential_duplicates
WHERE unique_ids > 1  -- Different Transaction IDs
ORDER BY group_count DESC
LIMIT 20;

-- 4. Let's see a specific example
WITH dup_example AS (
    SELECT 
        "Customer",
        "Policy Number",
        "Transaction Type",
        "Premium Sold",
        "Effective Date"
    FROM policies
    GROUP BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
    HAVING COUNT(*) > 2
    LIMIT 1
)
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Transaction Type",
    "Premium Sold",
    "Effective Date",
    "Total Agent Comm",
    updated_at
FROM policies
WHERE ("Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date") IN (SELECT * FROM dup_example)
ORDER BY updated_at;

-- 5. Key question: How many transactions were there before today's edits?
WITH before_today AS (
    SELECT COUNT(DISTINCT "Transaction ID") as count_before
    FROM policies
    WHERE updated_at < CURRENT_DATE
)
SELECT 
    count_before as transactions_before_today,
    (SELECT COUNT(*) FROM policies) as current_total,
    (SELECT COUNT(*) FROM policies) - count_before as added_today
FROM before_today;