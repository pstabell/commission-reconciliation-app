-- CHECK CREATION VS UPDATE DATES (FIXED)

-- 1. Check if we have a created_at column
SELECT 
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'policies'
  AND column_name LIKE '%creat%' OR column_name LIKE '%updat%'
ORDER BY column_name;

-- 2. Look at the date range of transactions
SELECT 
    MIN(updated_at) as earliest_update,
    MAX(updated_at) as latest_update,
    COUNT(DISTINCT DATE(updated_at)) as distinct_update_days
FROM policies;

-- 3. Group by update hour today
SELECT 
    DATE_TRUNC('hour', updated_at) as update_hour,
    COUNT(*) as transactions_updated
FROM policies
WHERE DATE(updated_at) = CURRENT_DATE
GROUP BY DATE_TRUNC('hour', updated_at)
ORDER BY update_hour;

-- 4. Check Effective Date patterns (with proper casting)
SELECT 
    DATE_TRUNC('month', "Effective Date"::date) as effective_month,
    COUNT(*) as transaction_count
FROM policies
WHERE "Effective Date" IS NOT NULL 
  AND "Effective Date" != ''
GROUP BY DATE_TRUNC('month', "Effective Date"::date)
ORDER BY effective_month DESC
LIMIT 12;

-- 5. Let's see if Transaction IDs have patterns indicating duplicates
SELECT 
    "Transaction ID",
    LENGTH("Transaction ID") as id_length,
    RIGHT("Transaction ID", 3) as last_3_chars,
    COUNT(*) OVER (PARTITION BY LEFT("Transaction ID", LENGTH("Transaction ID") - 2)) as similar_ids
FROM policies
ORDER BY similar_ids DESC, "Transaction ID"
LIMIT 20;

-- 6. Simple duplicate check
WITH dup_check AS (
    SELECT 
        "Policy Number",
        "Transaction Type",
        COUNT(*) as count,
        STRING_AGG("Transaction ID", ', ' ORDER BY "Transaction ID") as transaction_ids
    FROM policies
    GROUP BY "Policy Number", "Transaction Type"
    HAVING COUNT(*) > 1
)
SELECT * FROM dup_check
ORDER BY count DESC
LIMIT 10;