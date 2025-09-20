-- CHECK CREATION VS UPDATE DATES
-- The Edit bug might have updated ALL timestamps

-- 1. Check if we have a created_at column separate from updated_at
SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'policies'
  AND column_name IN ('created_at', 'updated_at', 'inserted_at', '_created', 'creation_date')
ORDER BY column_name;

-- 2. Look at the date range of transactions
SELECT 
    MIN(updated_at) as earliest_update,
    MAX(updated_at) as latest_update,
    COUNT(DISTINCT DATE(updated_at)) as distinct_update_days,
    COUNT(DISTINCT DATE_TRUNC('hour', updated_at)) as distinct_update_hours
FROM policies;

-- 3. Group by update hour today
SELECT 
    DATE_TRUNC('hour', updated_at) as update_hour,
    COUNT(*) as transactions_updated
FROM policies
WHERE DATE(updated_at) = CURRENT_DATE
GROUP BY DATE_TRUNC('hour', updated_at)
ORDER BY update_hour;

-- 4. Look for patterns in "Effective Date" to understand real transaction dates
SELECT 
    DATE_TRUNC('month', "Effective Date") as effective_month,
    COUNT(*) as transaction_count
FROM policies
WHERE "Effective Date" IS NOT NULL
GROUP BY DATE_TRUNC('month', "Effective Date")
ORDER BY effective_month DESC
LIMIT 12;

-- 5. Find transactions with same details but different Transaction IDs
WITH duplicates AS (
    SELECT 
        "Customer",
        "Policy Number", 
        "Transaction Type",
        "Effective Date",
        COUNT(*) as count,
        COUNT(DISTINCT "Transaction ID") as unique_ids,
        MIN("Transaction ID") as first_id,
        MAX("Transaction ID") as last_id
    FROM policies
    GROUP BY "Customer", "Policy Number", "Transaction Type", "Effective Date"
    HAVING COUNT(*) > 1 AND COUNT(DISTINCT "Transaction ID") > 1
)
SELECT * FROM duplicates
ORDER BY count DESC
LIMIT 10;