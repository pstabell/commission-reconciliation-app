-- COMPREHENSIVE DUPLICATE ANALYSIS
-- Let's understand all 171 duplicates before removing them

-- 1. Group duplicates by when they were created
SELECT 'Duplicates by time period:' as analysis;
WITH duplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
SELECT 
    CASE 
        WHEN updated_at > NOW() - INTERVAL '1 hour' THEN 'Last hour'
        WHEN DATE(updated_at) = CURRENT_DATE THEN 'Today'
        WHEN updated_at > NOW() - INTERVAL '7 days' THEN 'This week'
        WHEN updated_at > NOW() - INTERVAL '30 days' THEN 'This month'
        ELSE 'Older than 30 days'
    END as time_period,
    COUNT(*) as duplicate_count
FROM duplicates
WHERE rn > 1
GROUP BY time_period
ORDER BY 
    CASE time_period
        WHEN 'Last hour' THEN 1
        WHEN 'Today' THEN 2
        WHEN 'This week' THEN 3
        WHEN 'This month' THEN 4
        ELSE 5
    END;

-- 2. Show examples of the oldest duplicates
SELECT 'Sample of oldest duplicates:' as analysis;
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
    LEFT("Customer", 30) as customer,
    LEFT("Policy Number", 20) as policy,
    "Transaction Type",
    updated_at
FROM duplicates
WHERE rn > 1
ORDER BY updated_at ASC
LIMIT 10;

-- 3. Which customers have the most duplicates?
SELECT 'Customers with most duplicates:' as analysis;
WITH duplicates AS (
    SELECT 
        "Customer",
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
SELECT 
    "Customer",
    COUNT(*) as duplicate_count
FROM duplicates
WHERE rn > 1
GROUP BY "Customer"
ORDER BY COUNT(*) DESC
LIMIT 10;

-- 4. Transaction types breakdown
SELECT 'Duplicates by transaction type:' as analysis;
WITH duplicates AS (
    SELECT 
        "Transaction Type",
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
SELECT 
    "Transaction Type",
    COUNT(*) as duplicate_count
FROM duplicates
WHERE rn > 1
GROUP BY "Transaction Type"
ORDER BY COUNT(*) DESC;