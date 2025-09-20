-- COMPREHENSIVE DUPLICATE ANALYSIS (FIXED)
-- Let's understand all 171 duplicates before removing them

-- 1. Group duplicates by when they were created
WITH duplicates AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
),
time_grouped AS (
    SELECT 
        CASE 
            WHEN updated_at > NOW() - INTERVAL '1 hour' THEN 'Last hour'
            WHEN DATE(updated_at) = CURRENT_DATE THEN 'Today'
            WHEN updated_at > NOW() - INTERVAL '7 days' THEN 'This week'
            WHEN updated_at > NOW() - INTERVAL '30 days' THEN 'This month'
            ELSE 'Older than 30 days'
        END as time_period,
        updated_at
    FROM duplicates
    WHERE rn > 1
)
SELECT 
    time_period,
    COUNT(*) as duplicate_count
FROM time_grouped
GROUP BY time_period
ORDER BY 
    CASE time_period
        WHEN 'Last hour' THEN 1
        WHEN 'Today' THEN 2
        WHEN 'This week' THEN 3
        WHEN 'This month' THEN 4
        ELSE 5
    END;

-- 2. Show specific counts for today vs older
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
        WHEN DATE(updated_at) = CURRENT_DATE THEN 'Created Today'
        ELSE 'Older Duplicates'
    END as category,
    COUNT(*) as count
FROM duplicates
WHERE rn > 1
GROUP BY category;

-- 3. Show examples of today's duplicates
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
    updated_at::timestamp as updated_time
FROM duplicates
WHERE rn > 1 
  AND DATE(updated_at) = CURRENT_DATE
ORDER BY updated_at DESC
LIMIT 10;

-- 4. Which customers have the most duplicates?
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
ORDER BY duplicate_count DESC
LIMIT 10;

-- 5. Transaction types breakdown
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
ORDER BY duplicate_count DESC;