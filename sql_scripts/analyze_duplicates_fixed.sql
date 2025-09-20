-- Analyze the 537 transactions to understand the duplication - FIXED

-- 1. Recent activity timeline
SELECT 'Recent updates by hour:' as check;
SELECT 
    DATE_TRUNC('hour', updated_at) as hour,
    COUNT(*) as count
FROM policies
WHERE updated_at > NOW() - INTERVAL '6 hours'
GROUP BY DATE_TRUNC('hour', updated_at)
ORDER BY hour DESC;

-- 2. Find policies with multiple transactions (potential duplicates)
SELECT 'Top duplicate groups:' as check;
SELECT 
    "Customer",
    "Policy Number",
    COUNT(*) as transaction_count,
    COUNT(DISTINCT "Transaction Type") as different_types,
    MIN(updated_at) as first_created,
    MAX(updated_at) as last_updated
FROM policies
GROUP BY "Customer", "Policy Number"
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC
LIMIT 15;

-- 3. Show a specific example of duplicates
SELECT 'Example duplicate set:' as check;
SELECT 
    "Transaction ID",
    "Transaction Type",
    "Customer",
    LEFT("Policy Number", 20) as policy_num,
    "Premium Sold",
    updated_at
FROM policies
WHERE "Policy Number" IN (
    SELECT "Policy Number"
    FROM policies
    GROUP BY "Policy Number"
    HAVING COUNT(*) > 2
    LIMIT 1
)
ORDER BY "Policy Number", updated_at;

-- 4. Count by update periods
SELECT 'When were policies updated:' as check;
WITH period_counts AS (
    SELECT 
        CASE 
            WHEN updated_at > NOW() - INTERVAL '2 hours' THEN 'Last 2 hours'
            WHEN DATE(updated_at) = CURRENT_DATE THEN 'Today (earlier)'
            WHEN updated_at > NOW() - INTERVAL '7 days' THEN 'This week'
            ELSE 'Older'
        END as time_period,
        COUNT(*) as count
    FROM policies
    GROUP BY 1
)
SELECT time_period, count
FROM period_counts
ORDER BY 
    CASE time_period
        WHEN 'Last 2 hours' THEN 1
        WHEN 'Today (earlier)' THEN 2
        WHEN 'This week' THEN 3
        ELSE 4
    END;

-- 5. The key question - true duplicates with same Transaction Type
SELECT 'TRUE duplicates (same type):' as check;
SELECT 
    "Customer",
    "Policy Number",
    "Transaction Type",
    COUNT(*) as duplicate_count
FROM policies
GROUP BY "Customer", "Policy Number", "Transaction Type"
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC
LIMIT 10;