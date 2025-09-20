-- INVESTIGATE: Why did we jump from 425 to 535 (110 extra records)?

-- 1. Check how many records were created/updated in the last hour
SELECT 
    'Records updated in last hour:' as info,
    COUNT(*) as count
FROM policies
WHERE updated_at > NOW() - INTERVAL '1 hour';

-- 2. Group by exact update timestamp to see if there was a batch creation
SELECT 
    updated_at,
    COUNT(*) as records_created,
    STRING_AGG(DISTINCT LEFT("Customer", 20), ', ' ORDER BY LEFT("Customer", 20)) as sample_customers
FROM policies
WHERE updated_at > NOW() - INTERVAL '2 hours'
GROUP BY updated_at
HAVING COUNT(*) > 1
ORDER BY updated_at DESC
LIMIT 20;

-- 3. Find ALL duplicates that exist right now
WITH duplicate_groups AS (
    SELECT 
        "Transaction ID",
        COUNT(*) as duplicate_count
    FROM policies
    GROUP BY "Transaction ID"
    HAVING COUNT(*) > 1
)
SELECT 
    'Total duplicate Transaction IDs:' as info,
    COUNT(DISTINCT "Transaction ID") as unique_ids_with_duplicates,
    SUM(duplicate_count - 1) as total_extra_records
FROM duplicate_groups;

-- 4. Show a sample of the duplicates
SELECT 
    "Transaction ID",
    COUNT(*) as count,
    STRING_AGG(DISTINCT "Customer", ', ' ORDER BY "Customer") as customers
FROM policies
GROUP BY "Transaction ID"
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 5. Check if entire dataset was duplicated by looking at common customers
WITH customer_counts AS (
    SELECT 
        "Customer",
        COUNT(*) as transaction_count
    FROM policies
    GROUP BY "Customer"
    HAVING COUNT(*) > 10
)
SELECT * FROM customer_counts
ORDER BY transaction_count DESC
LIMIT 10;