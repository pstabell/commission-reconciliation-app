-- CHECK WHEN DUPLICATES WERE CREATED
-- This will show if all 171 are from today or if some are older

-- 1. Simple breakdown: Today vs Older
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
        WHEN DATE(updated_at) = CURRENT_DATE THEN 'Today'
        WHEN DATE(updated_at) = CURRENT_DATE - INTERVAL '1 day' THEN 'Yesterday'
        WHEN DATE(updated_at) >= CURRENT_DATE - INTERVAL '7 days' THEN 'This Week'
        ELSE 'Older'
    END as when_created,
    COUNT(*) as duplicate_count,
    STRING_AGG(DISTINCT "Transaction Type", ', ') as transaction_types
FROM duplicates
WHERE rn > 1
GROUP BY when_created
ORDER BY 
    CASE when_created
        WHEN 'Today' THEN 1
        WHEN 'Yesterday' THEN 2
        WHEN 'This Week' THEN 3
        ELSE 4
    END;

-- 2. Show the actual timestamps of recent duplicates
WITH duplicates AS (
    SELECT 
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
    updated_at::timestamp as duplicate_created_at,
    "Transaction Type",
    LEFT("Customer", 30) as customer,
    LEFT("Policy Number", 15) as policy
FROM duplicates
WHERE rn > 1 
  AND updated_at > NOW() - INTERVAL '48 hours'
ORDER BY updated_at DESC
LIMIT 20;

-- 3. Check if you have any duplicates from before today
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
    'Duplicates from BEFORE today:' as info,
    COUNT(*) as older_duplicate_count
FROM duplicates
WHERE rn > 1 
  AND DATE(updated_at) < CURRENT_DATE;

-- 4. Total unique transactions after removing ALL duplicates
WITH duplicates AS (
    SELECT 
        _id,
        ROW_NUMBER() OVER (
            PARTITION BY "Customer", "Policy Number", "Transaction Type", "Premium Sold", "Effective Date"
            ORDER BY updated_at ASC
        ) as rn
    FROM policies
)
SELECT 
    'Current total:' as metric,
    COUNT(*) as count
FROM policies
UNION ALL
SELECT 
    'After removing ALL duplicates:' as metric,
    COUNT(*) as count
FROM policies
WHERE _id NOT IN (
    SELECT _id FROM duplicates WHERE rn > 1
);