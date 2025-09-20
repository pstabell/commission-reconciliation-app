-- Analyze the 537 transactions to understand the duplication

-- 1. Check transactions created in last 2 hours
SELECT 'Transactions by hour (last 6 hours):' as check;
SELECT 
    DATE_TRUNC('hour', updated_at) as hour,
    COUNT(*) as count
FROM policies
WHERE updated_at > NOW() - INTERVAL '6 hours'
GROUP BY DATE_TRUNC('hour', updated_at)
ORDER BY hour DESC;

-- 2. Find exact duplicates (same customer, policy, premium)
SELECT 'Duplicate groups:' as check;
WITH duplicate_groups AS (
    SELECT 
        "Customer",
        "Policy Number",
        "Premium Sold",
        "Effective Date",
        COUNT(*) as duplicate_count,
        STRING_AGG("Transaction ID", ', ' ORDER BY updated_at) as transaction_ids
    FROM policies
    GROUP BY "Customer", "Policy Number", "Premium Sold", "Effective Date"
    HAVING COUNT(*) > 1
)
SELECT * FROM duplicate_groups
ORDER BY duplicate_count DESC
LIMIT 20;

-- 3. Check if duplicates have exactly same data or differences
SELECT 'Sample duplicate pair:' as check;
WITH dup_pairs AS (
    SELECT "Customer", "Policy Number", COUNT(*) as cnt
    FROM policies
    GROUP BY "Customer", "Policy Number"
    HAVING COUNT(*) > 1
    LIMIT 1
)
SELECT 
    "Transaction ID",
    "Customer",
    "Policy Number",
    "Transaction Type",
    "Premium Sold",
    updated_at
FROM policies
WHERE ("Customer", "Policy Number") IN (SELECT "Customer", "Policy Number" FROM dup_pairs)
ORDER BY updated_at;

-- 4. How many were created today vs exist from before
SELECT 'Creation timeline:' as check;
SELECT 
    CASE 
        WHEN updated_at > NOW() - INTERVAL '2 hours' THEN 'Last 2 hours'
        WHEN DATE(updated_at) = CURRENT_DATE THEN 'Today (earlier)'
        WHEN updated_at > NOW() - INTERVAL '7 days' THEN 'This week'
        ELSE 'Older'
    END as period,
    COUNT(*) as count
FROM policies
GROUP BY period
ORDER BY 
    CASE period
        WHEN 'Last 2 hours' THEN 1
        WHEN 'Today (earlier)' THEN 2
        WHEN 'This week' THEN 3
        ELSE 4
    END;